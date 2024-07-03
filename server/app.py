#!/usr/bin/env python3
from models import db, Restaurant, Restaurant_pizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


class Restaurants(Resource):
    def get(self):
        rests = [r.to_dict() for r in Restaurant.query.all()]
        return make_response(rests, 200)        
        #return "<h1>Code challenge</h1>"
    
api.add_resource(Restaurants, '/restaurants')


class RestaurantById(Resource):
    def get(self, id):
        if rest := Restaurant.query.filter(Restaurant.id == id).first():
            return make_response(rest.to_dict(rules = ('restaurant_pizzas',)), 200)
        else:
            return make_response({"error": "Restaurant not found"}, 404)

api.add_resource(RestaurantById, '/restaurants/<int:id>')


if __name__ == "__main__":
    
    app.run(port=5555, debug=True)

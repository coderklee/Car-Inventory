from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/inventory', methods = ['POST'])
@token_required
def add_to_inventory(current_user_token):
    year = request.json['year']
    make = request.json['make']
    model = request.json['model']
    type = request.json['type']
    price = request.json['price']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    car = Car(year, make, model, type, price, user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/inventory', methods = ['GET'])
@token_required
def get_car(current_user_token):
    a_user = current_user_token.token
    car = Car.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(car)
    return jsonify(response)

#Update endpoint
@api.route('/inventory/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.type = request.json['type']
    car.price = request.json['price']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# Delete endpoint
@api.route('/inventory/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)


@api.route('/inventory/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)
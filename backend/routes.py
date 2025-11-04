from flask_restful import Api, Resource
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

api = Api()

class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, world! from flask restful'}
api.add_resource(HelloWorld, '/message')

from models import db, User, Item


# auth routes

class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email'); password = data.get('password')
        if not email or not password:
            return {'message': 'Both email and password required!'}, 400
        user = User.query.get(email)
        if not user or user.password != password:
            return {'message': 'Invalid credentials!'}, 400
        token = create_access_token(identity=user.email)
        user = {'name': user.name, 'role': user.role, 'email': user.email}
        return {'message': "Login success!", 'token': token, 'user': user}
api.add_resource(LoginAPI, '/login')

class RegisterAPI(Resource):
    def post(self):
        # logic to add user
        return {'message': "Account created, login to continue..."}, 201

# user routes

class ItemAPI(Resource):
    @jwt_required()
    def get(self, item_id=None):
        if item_id:
            item = Item.query.get(item_id)
            if not item:
                return {'message': 'item not found'}, 404
            item = {'id': item.id, 'name': item.name, 'color': item.color}
            return {'message': 'single item', 'item': item}
        items = Item.query.all()
        items = [{'id': item.id, 'name': item.name, 'color': item.color} for item in items]
        return {'message': 'fetched successfully', 'items': items}
    
    @jwt_required()
    def post(self):
        user = User.query.get(get_jwt_identity())
        if not user or user.role != 'admin':
            return {'message': "You're not authorized to access this!"}, 401
        
        data = request.get_json()
        item = Item(name=data['name'], color=data['color'])
        db.session.add(item); db.session.commit()
        return {'message': 'item created'}, 201
    
    @jwt_required()
    def put(self, item_id):
        user = User.query.get(get_jwt_identity())
        if not user or user.role != 'admin':
            return {'message': "You're not authorized to access this!"}, 401

        return {'message': 'put received'}
    @jwt_required()
    def delete(self, item_id):
        user = User.query.get(get_jwt_identity())
        if not user or user.role != 'admin':
            return {'message': "You're not authorized to access this!"}, 401

        item = Item.query.get(item_id)
        if not item:
            return {'message': 'item not found'}, 404
        db.session.delete(item); db.session.commit()
        return {'message': 'deleted item'}
    
api.add_resource(ItemAPI, '/items', '/items/<item_id>')

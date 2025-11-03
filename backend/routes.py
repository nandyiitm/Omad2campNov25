from flask_restful import Api, Resource
from flask import request

api = Api()

class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, world! from flask restful'}
api.add_resource(HelloWorld, '/message')

from models import db, Item

class ItemAPI(Resource):
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
    def post(self):
        data = request.get_json()
        item = Item(name=data['name'], color=data['color'])
        db.session.add(item); db.session.commit()
        return {'message': 'post received'}
    def put(self, item_id):
        return {'message': 'put received'}
    def delete(self, item_id):
        item = Item.query.get(item_id)
        if not item:
            return {'message': 'item not found'}, 404
        db.session.delete(item); db.session.commit()
        return {'message': 'deleted item'}
api.add_resource(ItemAPI, '/items', '/items/<item_id>')

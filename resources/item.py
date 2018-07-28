# -*- coding: utf-8 -*-

# -- Public Imports
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

# -- Private Imports
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='this field cannot be blank')
    parser.add_argument('store_id', type=int, required=True, help='the ID of the store in which item is placed')

    @jwt_required()
    def get(self, name):
        
        item = ItemModel.find_by_name(name)
        if item: 
            return item.json(), 201
        return {'message': 'Item not found'}, 404

    def post(self, name):
        
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{0}' already exists".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, float(data['price']), data['store_id'])
        item.save_to_db()

        return item.json(), 201 # just to let the app know that the itme has been added
    
    def delete(self, name):
        
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': "couldn't find '{0}' in the item table".format(name)}

    def put(self, name):
        
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class ItemList(Resource):
    @jwt_required()
    def get(self):
        items = ItemModel.query.all()
        return {'items': item.json() for item in items}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be empty")
    parser.add_argument('store_id', type=int, required=True, help="This field cannot be empty")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json()

        return {'message': 'item not found'}, 404
    
    @jwt_required()
    def post(self, name):
        if ItemModel.find_item_by_name(name):
            return {'message': 'An item with name {} already exist'.format(name)}, 400

        request_data = Item.parser.parse_args()
        item = ItemModel(name, **request_data)

        item.save_to_db()

        return item.json(), 201

    @jwt_required()
    def put(self, name):
        request_data = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)

        if item is None:
            item = ItemModel(name, **request_data)
        else:
            item.price = request_data['price']

        item.save_to_db()
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Record deleted'}, 200

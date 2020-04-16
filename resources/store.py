from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()

        return {'message': 'store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'An store with name {} already exist'.format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'Error inserting record'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Record deleted'}, 200


class StoreList(Resource):
    def get(self):
        stores = StoreModel.query.all()
        return {'stores': store.json() for store in stores}

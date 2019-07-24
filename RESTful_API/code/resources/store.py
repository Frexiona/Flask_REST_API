from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store
        else:
            {'message': 'Store Not Found'}, 404

    def post(self, name):
        pass

    def delete(self, name):
        pass


class StoreList(Resource):
    pass

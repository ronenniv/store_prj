from flask_restful import Resource
from models.store import StoreModel
from db import db

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {"message": f"store {name} not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"store {name} already exist"}, 400
        else:
            store = StoreModel(name)
            store.save_to_db()
            return store.json()

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": f"Store {name} deleted"}, 200
        else:
            return {"message": f"store not found"}, 404

class StoreList(Resource):

    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
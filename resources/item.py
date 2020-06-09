from flask_restful import Resource
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            print(f"item.json={item.json()}")
            return {'item': item.json()}, 200
        else:
            return {"message" : "item not found"}, 404 # 404 not found

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'Item {name} already exist'}, 400  # 400 for bad request

        data = ItemModel.parse_price()  # parse JSON for price
        # data = request.get_json(force=True) #force=True - do not look on the header. always process it as JSON. silent=True - in error return None, instead of error
        item = ItemModel(name, **data)
        print(item.json())

        item.save_to_db()
        print(f'saved to db with {item.name} and {item.price}')
        return {'item': item.json()}, 201  # 201 return code for created

    @jwt_required()
    def delete(self, name):
        # first find if item name exist in DB
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': f'Item {name} deleted'}, 200
        else:
            return {'message': f'Item {name} not found'}, 404

    @jwt_required()
    def put(self, name):
        data = ItemModel.parse_price()  # parse JSON for price
        item = ItemModel(name, **data)
        item.save_to_db()

        return {'item': item.json()}, 200


class ItemList(Resource):

    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}




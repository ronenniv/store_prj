import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT


from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turning off the flask sqlalchmey sync tracker
# geting url for PostgressDB in Heroku. default is sqlite3 if DATABASE_URL not defined
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.secret_key = 'ronen'
api = Api(app)

jwt = JWT(app, authenticate, identity) #JWT create new endpoint /auth

# name is the parmaters for the get function
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item/<name>
api.add_resource(ItemList, '/items') # http://127.0.0.1:5000/items
api.add_resource(UserRegister, '/register') # user authentication

api.add_resource(Store, '/store/<string:name>') # http://127.0.0.1:5000/item/<name>
api.add_resource(StoreList, '/stores') # http://127.0.0.1:5000/items


def main():
    '''connecting to SQLAlchemy'''
    from db import db
    db.init_app(app)

    #starting the app
    app.run(port=5000, debug=True)


if __name__ == '__main__':
    main()

import logging
import os

from flask import Flask

from flask_jwt import JWT

from flask_restful import Api

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister


from security import authenticate, identity


app = Flask(__name__)
# turning off the flask sqlalchmey sync tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# getting url for PostgresDB in Heroku. default is sqlite3 if DATABASE_URL not defined
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.secret_key = 'ronen'
api = Api(app)

# setting log configuration

log_index = \
    {'DEBUG': logging.DEBUG,
     'INFO': logging.INFO,
     'WARNING': logging.WARNING,
     'ERROR': logging.ERROR,
     'CRITICAL': logging.CRITICAL}
try:
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S',
                        level=log_index[os.environ.get('DEBUG_LEVEL', 'WARNING')])
except KeyError:
    app.logger.error('Incorrect DEBUG_LEVEL %s. Setting WARNING level'.format(os.environ.get('DEBUG_LEVEL')))
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S',
                        level=logging.WARNING)


jwt = JWT(app, authenticate, identity)  # JWT create new endpoint /auth

# name is the parameters for the get function
api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/item/<name>
api.add_resource(ItemList, '/items')  # http://127.0.0.1:5000/items
api.add_resource(UserRegister, '/register')  # user authentication

api.add_resource(Store, '/store/<string:name>')  # http://127.0.0.1:5000/item/<name>
api.add_resource(StoreList, '/stores')  # http://127.0.0.1:5000/items


def main():
    """connecting to SQLAlchemy"""
    from db import db

    db.init_app(app)

    # starting the app
    app.run(port=5000, debug=True)


if __name__ == '__main__':
    main()

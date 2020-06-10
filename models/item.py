from db import db

from flask_restful import reqparse


class ItemModel(db.Model):  # extend db.Model for SQLAlechemy

    __tablename__ = 'item'

    '''define the fields from the object and SQLAlchemy
    the column below name must match the object vars
    any additional vars to the object wont be saved to the db'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float(precision=2))

    # define the relationship between item table and store. . relationship needs to be defined also for store table
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))  # define foreign key to stores table
    store = db.relationship('StoreModel')  # define the relation to the object

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name": self.name, "price": self.price, "store_id": self.store_id}

    @classmethod
    def parse_price(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True, help="This field cannot be left blank")
        parser.add_argument('store_id', type=int, required=True, help="Every item needs store_id")
        return parser.parse_args()

    @classmethod
    def find_by_name(cls, name):
        """find in DB the item with name
        if found update price and return True, otherwise False"""
        return cls.query.filter_by(name=name).first()  # SQLAlchemy -> SELECT * FROM item WHERE name=name

    def save_to_db(self):
        """updade or insert to the DB new item"""
        if ItemModel.query.filter_by(name=self.name).first():
            ItemModel.query.filter_by(name=self.name).update(dict(price=self.price))
        else:
            db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """delete record from DB"""
        db.session.delete(self)
        db.session.commit()

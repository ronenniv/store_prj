from flask_restful import reqparse
from db import db

class StoreModel(db.Model): #extend db.Model for SQLAlechemy

    __tablename__ = 'stores'

    '''define the fields from the object and SQLAlchemy
    the column below name must match the object vars
    any additional vars to the object wont be saved to the db'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    items = db.relationship('ItemModel', lazy='dynamic') # this definition comes together with the define in StoreModel. Lazy will ask to note create entires for items


    def __init__(self, name):
        self.name = name

    def json(self):
        return {"name": self.name, "items": [item.json() for item in self.items.all()]}

    @classmethod
    def parse_price(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True, help="This field cannot be left blank")
        return parser.parse_args()

    @classmethod
    def find_by_name(cls, name):
        '''find in DB the store with name
        if found update price and return True, otherwise False'''
        return cls.query.filter_by(name=name).first() # SQLAlchemy -> SELECT * FROM item WHERE name=name

    def save_to_db(self):
        '''updade or insert to the DB new store'''
        if StoreModel.query.filter_by(name=self.name).first():
            StoreModel.query.filter_by(name=self.name).update(dict(price=self.price))
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        '''delete record from DB'''
        db.session.delete(self)
        db.session.commit()

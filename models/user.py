from db import db


class UserModel(db.Model):  # extend db.Model for SQLAlechemy

    __tablename__ = 'users'

    '''define the fields from the object and SQLAlchemy
    the column below name must match the object vars
    any additional vars to the object wont be saved to the db'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return UserModel.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return UserModel.query.filter_by(id=_id).first()

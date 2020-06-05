from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="Username cannot be left blank")
        parser.add_argument('password', type=str, required=True, help="Password cannot be left blank")
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": f"User {data['username']} already exist"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message" : f"User {data['username']} created succesfully"}, 201 # 201 for created
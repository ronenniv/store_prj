from models.user import UserModel


def authenticate(username, password):
    current_user = UserModel.find_by_username(username)
    if current_user and current_user.password == password:
        return current_user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)

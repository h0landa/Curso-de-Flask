from flask_restful import Resource, reqparse
from models.usuario import UserModel


class User(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('login', type=str, required=True, help="This field 'login' cannot be blank.")
    argumentos.add_argument('password', type=str, required=True, help="This field 'password' cannot be blank.")

    def internal_error(self, error='save'):
        if error == 'save':
            return {"message": "An internal error occurred trying to save hotel"}
        if error == 'delete':
            return {"message": "An internal error occurred trying to delete hotel"}

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404 #NOT FOUND

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_hotel()
            except:
                return User.internal_error('delete')
            return {"message": f"User id {user_id} deleted"}, 200
        return {'message': 'User not found.'}, 404

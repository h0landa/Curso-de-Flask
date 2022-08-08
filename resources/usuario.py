from flask_restful import Resource, reqparse
from models.usuario import UserModel
from models.modulos import internal_error
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from models.modulos import safe_str_cmp
from blacklist import BLACKLIST


atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="This field 'login' cannot be blank.")
atributos.add_argument('password', type=str, required=True, help="This field 'password' cannot be blank.")


class User(Resource):
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404 #NOT FOUND

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_hotel()
            except:
                return internal_error('delete')
            return {"message": f"User id {user_id} deleted"}, 200
        return {'message': 'User not found.'}, 404


class RegisterUser(Resource):

    def post(self):
        dados = atributos.parse_args()
        if UserModel.find_by_user(dados['login']):
            return {"message": "This user already exists."}
        else:
            user = UserModel(**dados)
            try:
                user.save_user()
                return {"message": "User created successfully."}, 201
            except:
                return internal_error()


class UserLogin(Resource):
    def post(self):
        dados = atributos.parse_args()
        user = UserModel.find_by_user(dados['login'])
        if user and safe_str_cmp(user.password, dados['password']):
            access_token = create_access_token(identity=user.user_id)
            return {"access_token": access_token}, 200
        else:
            print(user.password)
            return {"message": "The username or password is incorrect."}, 401 #Não autorizado


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {"message": "Logged out successfully."}

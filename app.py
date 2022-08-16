from flask import Flask, jsonify
from flask_restful import Api

import blacklist
from resources.hotel import Hoteis, Hotel, Hello
from resources.site import Sites, Site
from resources.usuario import User, RegisterUser, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'ultra_secreta'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=7)
jwt = JWTManager(app)


@app.before_request
def cria_banco():
    banco.create_all()


@jwt.token_in_blocklist_loader
def verify_blocklist(self, token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_access_invalid(jwt_header, jwt_payload):
    return jsonify({"message": "You have been logged out."}), 401


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hello, '/')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(RegisterUser, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)

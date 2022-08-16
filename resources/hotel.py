from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.modulos import internal_error
from flask_jwt_extended import jwt_required
import sqlite3
from resources.filtros import normalize_path_params, consulta_com_cidade, consulta_sem_cidade
from resources.site import SiteModel


path_params = reqparse.RequestParser()
path_params.add_argument("cidade", type=str, location="args")
path_params.add_argument("estrelas_min", type=float, location="args")
path_params.add_argument("estrelas_max", type=float, location="args")
path_params.add_argument("diaria_min", type=float, location="args")
path_params.add_argument("diaria_max", type=float, location="args")


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()
        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)
        if not parametros.get('cidade'):
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_com_cidade, tupla)
        else:
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_sem_cidade, tupla)
        hoteis = []
        for linha in resultado.fetchall():
            hoteis.append({
            'hotel_id': linha[0],
            'nome': linha[1],
            'estrelas': linha[2],
            'diaria': linha[3],
            'cidade': linha[4],
            'site_id': linha[5]
            })
        return {'hoteis': hoteis} # SELECT * FROM hoteis


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="This field 'nome' cannot be blank.")
    argumentos.add_argument('estrelas', type=float)
    argumentos.add_argument('diaria', type=str, required=True, help="This field 'diaria' cannot be blank.")
    argumentos.add_argument('cidade', type=str, required=True, help="This field 'cidade' cannot be blank.")
    argumentos.add_argument('site_id', type=int, required=True, help="Every hotel needs to be linked with a site.")

    @jwt_required()
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404 #NOT FOUND

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": f"Hotel id '{hotel_id}' already exists."}, 400 #BAD REQUEST
        dados = Hotel.argumentos.parse_args()
        print(dados)
        hotel = HotelModel(hotel_id, **dados)
        if not SiteModel.find_by_id(dados.get('site_id')):
            return {'message': 'There is no website with this id.'}, 400
        else:
            try:
                hotel.save_hotel()
            except:
                return internal_error(), 500  # Internal Error
            return hotel.json(), 201 #SUCCESS

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.update_hotel(**dados)
            try:
                hotel.save_hotel()
            except:
                return internal_error(), 500
            return hotel.json(), 200
        else:
            print('Hotel não encontrado. Um novo hotel foi criado!.')
            hotel = HotelModel(hotel_id, **dados)
            hotel.save_hotel()
            return hotel.json(), 201 #CRIATED ou CRIADO

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return internal_error('delete')
            return {"message": f"Hotel id {hotel_id} deleted"}, 200
        return {'message': 'Hotel not found.'}, 404


class Hello(Resource):
    def get(self):
        return {'message': 'Hello, World!'}

from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.modulos import internal_error
from flask_jwt_extended import jwt_required
import sqlite3


def normalize_path_params(cidade=None,
                          estrelas_min=0,
                          estrelas_max=5,
                          diaria_min=0,
                          diaria_max=10000,
                          limit=50,
                          offset=0):
    if cidade:
        return{
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset}
    return{
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset}

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
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        print('______dados___validos_____')
        print(dados_validos)
        parametros = normalize_path_params(**dados_validos)
        print('-----PARAMETROS------')
        print(parametros)
        if not parametros.get('cidade'):
            consulta = """SELECT * FROM hoteis
            WHERE (estrelas >= ? and estrelas <= ?) 
            and (diaria >= ? and diaria <= ?) LIMIT ? OFFSET ?"""
            tupla = tuple([parametros[chave] for chave in parametros])
            print('-------TUPLA------')
            print(tupla)
            resultado = cursor.execute(consulta, tupla)
        else:
            consulta = """SELECT * FROM hoteis
            WHERE (estrelas >= ? and estrelas <= ?) 
            and (diaria >= ? and diaria <= ?) 
            AND cidade = ? LIMIT ? OFFSET ?"""
            tupla = tuple([parametros[chave] for chave in parametros])
            print('-------TUPLA------')
            print(tupla)
            resultado = cursor.execute(consulta, tupla)
        hoteis = []
        for linha in resultado.fetchall():
            hoteis.append({
            'hotel_id': linha[0],
            'nome': linha[1],
            'estrelas': linha[2],
            'diaria': linha[3],
            'cidade': linha[4]
            })
        return {'hoteis': hoteis} # SELECT * FROM hoteis
class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="This field 'nome' cannot be blank.")
    argumentos.add_argument('estrelas', type=float)
    argumentos.add_argument('diaria', type=str, required=True, help="This field 'diaria' cannot be blank.")
    argumentos.add_argument('cidade', type=str, required=True, help="This field 'cidade' cannot be blank.")

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
        try:
            hotel.save_hotel()
        except:
            return internal_error(), 500 #Internal Error
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

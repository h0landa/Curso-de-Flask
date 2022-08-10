from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.modulos import internal_error
from flask_jwt_extended import jwt_required
import sqlite3


def normalize_path_params(cidade=None,
                          diaria_min=0,
                          diaria_max=10000,
                          estrelas_min=0,
                          estrelas_max=5,
                          limit=50,
                          offset=0, **dados):
    if cidade:
        return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset}
    return {
    'estrelas_min': estrelas_min,
    'estrelas_max': estrelas_max,
    'diaria_min': diaria_min,
    'diaria_max': diaria_max,
    'limit': limit,
    'offset': offset}


path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)
        if not parametros['cidade']:
            consulta = """SELECT * FROM hoteis WHERE 
            (estrelas > ? and estrelas < ?) and
            (diaria > ? and diaria < ?) LIMIT ? OFFSET ?"""
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)
        else:
            consulta = """
            SELECT * FROM hoteis WHERE 
            (estrelas >= ? and estrelas <= ?) and
            (diaria >= ? and diaria <= ?) 
            and cidade = ? LIMIT ? OFFSET ?
            """
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)
        hoteis = []
        for linha in resultado:
            hoteis.append({"hotel_id": linha[0],
                           "nome": linha[1],
                           "diaria": linha[2],
                           "estrelas": linha[3],
                           "cidade": linha[4]})
        print()

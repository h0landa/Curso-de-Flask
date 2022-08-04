from flask_restful import Resource, reqparse
from models.hotel import HotelModel

lista_hoteis = [
    {'hotel_id':'primavera',
    'nome':'Hotel Primavera',
    'diaria': 450,
    'estrelas': 4.6,
    'cidade':'Ceará-Mirim'
    },
    {'hotel_id':'outono',
    'nome':'Hotel Outono',
    'diaria': 350,
    'estrelas': 4.3,
    'cidade':'Maxaranguape'
    }
    ,
    {'hotel_id':'verao',
    'nome':'Hotel Verão',
    'diaria': 160,
    'estrelas': 2.0,
    'cidade':'Mossoró'
    }
    ,
    {'hotel_id':'inverno',
    'nome':'Hotel Inverno',
    'diaria': 600,
    'estrelas': 5.0,
    'cidade':'Garanhões'
    }
]
class Hoteis(Resource):
    def get(self):
        return {'hoteis': lista_hoteis}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('diaria')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('cidade')

    def encontrar_hotel(hotel_id):
        for hotel in lista_hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
    def get(self, hotel_id):
        hotel = Hotel.encontrar_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message':'Hotel not found.'}, 404 #NOT FOUND
    def post(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        objeto_hotel = HotelModel(hotel_id, **dados)
        novo_hotel = objeto_hotel.json()
        lista_hoteis.append(novo_hotel)
        return dados, 200 #SUCESS
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel = Hotel.encontrar_hotel(hotel_id)
        objeto_hotel = HotelModel(hotel_id, **dados)
        novo_hotel = objeto_hotel.json()
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200
        else:
            print('Hotel não encontrado. Um novo hotel foi criado!.')
            lista_hoteis.append(novo_hotel)
            return novo_hotel, 201 #CRIATED ou CRIADO
    def delete(self, hotel_id):
        global lista_hoteis
        lista_hoteis = [hotel for hotel in lista_hoteis if hotel['hotel_id'] != hotel_id]
        return {'message':'hotel deleted.'}, 200

class Hello(Resource):
    def get(self):
        return {'hello':'world'}

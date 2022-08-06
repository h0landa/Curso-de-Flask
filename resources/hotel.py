from flask_restful import Resource, reqparse
from models.hotel import HotelModel

class Hoteis(Resource):
    def get(self):
        lista_hoteis = []
        hoteis = HotelModel.buscar_hoteis()
        for hotel in hoteis:
            lista_hoteis.append(hotel.json())
        return lista_hoteis
class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('diaria')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.encontrar_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message':'Hotel not found.'}, 404 #NOT FOUND


    def post(self, hotel_id):
        if HotelModel.encontrar_hotel(hotel_id):
            return {"message":f"Hotel id '{hotel_id}' already exists."}, 400 #BAD REQUEST
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 200 #SUCCESS


    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel.encontrar_hotel(hotel_id)
        if hotel:
            hotel.update_hotel(**dados)
            hotel.save_hotel()
            return hotel.json(), 200
        else:
            print('Hotel não encontrado. Um novo hotel foi criado!.')
            hotel = HotelModel(hotel_id, **dados)
            hotel.save_hotel()
            return hotel.json() , 201 #CRIATED ou CRIADO


    def delete(self, hotel_id):
        hotel = HotelModel.encontrar_hotel(hotel_id)
        if hotel:
            hotel.excluir_hotel()
            return {"message":f"Hotel id {hotel_id} deleted"}, 200
        return {'message':'Hotel not found.'}, 404


class Hello(Resource):
    def get(self):
        return {'message':'Hello, World!'}

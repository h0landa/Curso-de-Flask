from flask_restful import Resource, reqparse
from models.hotel import HotelModel


class Hoteis(Resource):
    def get(self):
        lista_hoteis = []
        hoteis = HotelModel.search_hotels()
        for hotel in hoteis:
            lista_hoteis.append(hotel.json())
        return lista_hoteis


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="This field 'nome' cannot be blank.")
    argumentos.add_argument('diaria', type=str, required=True, help="This field 'diaria' cannot be blank.")
    argumentos.add_argument('estrelas')
    argumentos.add_argument('cidade', type=str, required=True, help="This field 'cidade' cannot be blank.")

    def internal_error(self, erro='save'):
        if erro == 'save':
            return {"message": "An internal error occurred trying to save hotel"}
        if erro == 'delete':
            return {"message": "An internal error occurred trying to delete hotel"}

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404 #NOT FOUND

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message":f"Hotel id '{hotel_id}' already exists."}, 400 #BAD REQUEST
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return Hotel.internal_error(), 500 #Internal Error
        return hotel.json(), 200 #SUCCESS

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.update_hotel(**dados)
            try:
                hotel.save_hotel()
            except:
                return Hotel.internal_error(), 500
            return hotel.json(), 200
        else:
            print('Hotel não encontrado. Um novo hotel foi criado!.')
            hotel = HotelModel(hotel_id, **dados)
            hotel.save_hotel()
            return hotel.json(), 201 #CRIATED ou CRIADO

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return Hotel.internal_error('delete')
            return {"message": f"Hotel id {hotel_id} deleted"}, 200
        return {'message': 'Hotel not found.'}, 404


class Hello(Resource):
    def get(self):
        return {'message': 'Hello, World!'}

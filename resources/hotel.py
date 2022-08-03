from flask_restful import Resource

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
    {'hotel_id':'verão',
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
    def get(self, hotel_id):
        for hotel in lista_hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return {'message':'Hotel not found.'}, 404 #not found
    def post(self, hotel_id):
        pass
    def put(self, hotel_id):
        pass
    def delet(self, hotel_id):
        pass


class Hello(Resource):
    def get(self):
        return {'hello':'world'}

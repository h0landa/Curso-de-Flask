from sql_alchemy import banco


class HotelModel(banco.Model):
    __tablename__ = 'hoteis'

    hotel_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    diaria = banco.Column(banco.Float(precision=2))
    estrelas = banco.Column(banco.Float(precision=1))
    cidade = banco.Column(banco.String(80))
    
    def __init__(self,hotel_id,nome,diaria,estrelas,cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.diaria = diaria
        self.estrelas = estrelas
        self.cidade = cidade
    

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'diaria': self.diaria,
            'estrelas': self.estrelas,
            'cidade': self.cidade
        }


    @classmethod
    def encontrar_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()
        if hotel:
            return hotel
        return None


    @classmethod
    def buscar_hoteis(cls):
        hoteis = cls.query.all()
        return hoteis


    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()


    def update_hotel(self, nome, diaria, estrelas, cidade):
        self.nome = nome
        self.diaria = diaria
        self. estrelas = estrelas
        self.cidade = cidade


    def excluir_hotel(self):
        banco.session.delete(self)
        banco.session.commit()
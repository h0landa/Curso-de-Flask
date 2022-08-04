class HotelModel():
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
from sql_alchemy import banco


class UserModel(banco.Model):
    __tablename__ = 'users'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    password = banco.Column(banco.String(40))

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
        }

    @classmethod
    def find_by_user(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def search_user(cls):
        user = cls.query.all()
        return user

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def update_user(self, login, password):
        self.login = login
        self.password = password

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()

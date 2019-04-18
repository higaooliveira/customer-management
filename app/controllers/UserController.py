from app.models.Tables import User
from app.controllers.CustomerController import CustomerController
from app import db


class UserController:

    def __init__(self, name = None, email = None, password = None):
        self.name = name
        self.email = email
        self.password = password

    def login_action(self, email, password):
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return user

    def register_action(self):
        try:
            userModel = User(self.name, self.email, self.password)
            if userModel:
                db.session.add(userModel)
                db.session.commit()
                db.session.delete(userModel)

                return ['Cadastrado com sucesso!', 'success']
            return ['Não foi possível cadastrar', 'error']
        except:
            return 	['Não foi possível cadastrar', 'error']

    def create_customer(self, name, date_birth, cpf, rg, phone):
        customer = CustomerController(name, date_birth, cpf, rg, phone)
        if customer:

            result = customer.create_customer()
            return result
        return 'Erro ao cadastrar cliente.'
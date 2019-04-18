from app.models.Tables import Customer
from app import db


class CustomerController:

    def __init__(self, name = None, date_birth = None, cpf = None, rg = None, phone = None):
        self.name = name
        self.date_birth = date_birth
        self.cpf = cpf
        self.rg = rg
        self.phone = phone

    def create_customer(self):
        try:
            customerModel = Customer(self.name, self.date_birth, self.cpf, self.rg, self.phone)
            if customerModel:
                db.session.add(customerModel)
                db.session.commit()
                db.session.delete(customerModel)
                return ['Cliente %s com sucesso!'.format(self.name), 'success']
            return ['Não foi possível cadastrar', 'error']
        except:
            return ['Não foi possível cadastrar', 'error']

    def get_all_customers(self):
        try:
            result = Customer.query.all()
            if result:
                return result
        except:
            return 'Não foi possível encontrar registro de clientes'
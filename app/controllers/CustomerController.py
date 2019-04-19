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
                return ['Cliente %s cadastrado com sucesso!'.format(self.name), 'success']
            return ['Não foi possível cadastrar', 'error']
        except:
            return ['Não foi possível cadastrar', 'error']

    def delete_customer(self, id):
        if not id:
            return ['Não foi possível excluir o cliente', 'error']

        try:
            db.session.delete(Customer.query.get(id))
            db.session.commit()

            return ['Cliente excluído com sucesso', 'success']
        except:
            ['Não foi possível excluir o cliente', 'error']


    def get_all_customers(self):
        try:
            result = Customer.query.all()
            if result:
                return result
        except:
            return 'Não foi possível encontrar registro de clientes'


    def get_customer_by_id(self, id):
        if not id:
            return "Erro"

        result = Customer.query.get(id)
        if result:
            return result

        return "Erro"

    def edit_customer(self,id,name, date_birth, cpf, rg, phone):
        try:
            customer = self.get_customer_by_id(id)
            if customer:
                customer.name = name
                customer.date_birth = date_birth
                customer.cpf = cpf
                customer.rg = rg
                customer.phone = phone
                db.session.commit()
                return ['Cliente %s editado com sucesso!'.format(name), 'success']
            return ['Não foi possível cadastrar', 'error']
        except:
            return ['Não foi possível cadastrar', 'error']

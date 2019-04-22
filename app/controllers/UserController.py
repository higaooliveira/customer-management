from app.models.Tables import User
from app.controllers.CustomerController import CustomerController
from app.controllers.AddressController import AddressController
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

                return True
            return False
        except:
            return 	False

    def create_customer(self, name, date_birth, cpf, rg, phone):
        customer = CustomerController(name, date_birth, cpf, rg, phone)
        if customer:
            result = customer.create_customer()
            return result

    def edit_customer(self,id ,name ,date_birth, cpf, rg, phone):
        customer = CustomerController()
        if customer:
            result = customer.edit_customer(id,name, date_birth, cpf, rg, phone)
            return result

    def new_customer_address(self, street, district, city, state, country,customer_id):
        address = AddressController(street, district, city, state, country,customer_id)
        if address:
            result = address.new_address()
            return result

    def edit_customer_address(self, id, street, district, city, state, country,customer_id):
        address = AddressController()
        if address:
            result = address.edit_address(id, street, district, city, state, country,customer_id)
            return result

    def get_all_users_count(self):
        return len(User.query.all())
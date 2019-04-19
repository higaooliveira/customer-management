from app.models.Tables import Addressess
from app import db

class AddressController:

    def __init__(self, street = None, district = None, city = None , state = None, country = None, customer_id = None):
        self.street = street
        self.district = district
        self.city = city
        self.state = state
        self.country = country
        self.customer_id = customer_id

    def new_address(self):
        try:
            addressModel = Addressess(self.street, self.district, self.city, self.state, self.country, self.customer_id)
            if addressModel:
                db.session.add(addressModel)
                db.session.commit()
                return ['Endereço cadastrado com sucesso!', 'success']
            return ['Não foi possível cadastrar', 'error']
        except:
            return ['Não foi possível cadastrar', 'error']

    def get_address_by_customer_id(self, customer_id):
        address = Addressess.query.filter_by(customer_id = customer_id).all()

        if address:
            return address

    def get_address_by_id(self, id):
        if not id:
            return "Erro"

        result = Addressess.query.get(id)
        if result:
            return result

        return "Erro"

    def edit_address(self,id, street, district, city, state, country,customer_id):
        try:
            address = self.get_address_by_id(id)
            if address:
                address.street = street
                address.district = district
                address.city = city
                address.state = state
                address.country = country
                address.customer_id = customer_id
                db.session.commit()
                return ['Endereço atualizado com sucesso!', 'success']
            return ['Não foi possível atualizar endereço', 'error']
        except:
            return ['Não foi possível atualizar endereço', 'error']

    def delete_address(self, id):
        if not id:
            return ['Não foi possível excluir o endereço', 'error']

        try:
            address = self.get_address_by_id(id)
            db.session.delete(self.get_address_by_id(id))
            db.session.commit()
            return ['Endereço excluído com sucesso', 'success', address.customer_id]
        except:
            return ['Não foi possível excluir o endereço', 'error']
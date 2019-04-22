from flask import render_template, request, url_for, session, redirect, flash
from app import app
from app.controllers.UserController import UserController
from app.controllers.CustomerController import CustomerController
from app.controllers.AddressController import AddressController


@app.route('/')
@app.route('/index')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return redirect(url_for('dashboard'))


@app.route('/login')
def login():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect(url_for('dashboard'))


@app.route('/loginaction', methods=["POST"])
def login_action():
    formData = request.form

    user = UserController()
    result = user.login_action(formData['email'], formData['password'])
    if result:
        session['logged_in'] = True
        session['user'] = result.name
        session['email'] = result.email
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logoutaction')
def logout_action():
    if session.get('logged_in'):
        session.pop('logged_in', None)
        session.pop('user', None)
        session.pop('email', None)
        session.clear()
        return redirect(url_for('login'))

@app.route('/register')
def register():
    return render_template('cadastro.html')


@app.route('/registeraction', methods=["POST"])
def register_action():
    if request.form :
        formData = request.form
        user = UserController(formData['name'], formData['email'], formData['password'])
        result = user.register_action()
        if result[1] is 'success':
            return redirect(url_for('login'))
    return redirect(url_for('register'))



@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        customer = CustomerController()
        user = UserController()
        customers = customer.get_all_customers_count()
        users = user.get_all_users_count()
        return render_template('dashboard.html',customers=customers, users=users ,user=session['user'])


@app.route('/newcustomer')
def new_customer():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('newcustomer.html',user=session['user'])


@app.route('/createcustomer', methods=["POST"])
def create_customer():
    if request.form :
        formData = request.form
        user = UserController()
        result = user.create_customer(formData['name'], formData['date_birth'], formData['cpf'], formData['rg'], formData['phone'])
        if result:
            return redirect(url_for('list_customers'))

    return redirect(url_for('new_customer'))


@app.route('/listcustomers')
def list_customers():
    customer = CustomerController()
    result = customer.get_all_customers()
    if result:
        return render_template('listcustomers.html', customers=result, user=session['user'])
    return "Não tem cliente"


@app.route('/viewcustomer/<int:id>')
def view_customer(id):
    customer = CustomerController()
    address = AddressController()
    result = customer.get_customer_by_id(id)
    locations = address.get_address_by_customer_id(id)
    if result:
        return render_template('customerview.html', customer=result, addresses=locations,user=session['user'] )
    return "Não tem cliente"


@app.route('/deletecustomer/<int:id>')
def delete_customer(id):
    customer = CustomerController()
    result = customer.delete_customer(id)

    return redirect(url_for('list_customers'))


@app.route('/editcustomer/<int:id>')
def edit_customer(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        customer = CustomerController()
        result = customer.get_customer_by_id(id)
        return render_template('editcustomer.html', customer=result,user=session['user'])


@app.route('/editcustomeraction', methods=["POST"])
def edit_customer_action():
    if request.form :
        formData = request.form
        user = UserController()
        result = user.edit_customer(formData['id'], formData['name'], formData['date_birth'], formData['cpf']
                                    , formData['rg'], formData['phone'])
        if result:
            return redirect(url_for('view_customer', id=formData['id']))


@app.route('/newaddress/<int:customer_id>')
def new_address(customer_id):
    if not customer_id:
        return redirect(url_for('list_customers'))

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('newaddress.html', customer_id = customer_id,user=session['user'])


@app.route('/newaddressaction', methods=["POST"])
def new_address_action():
    if request.form :
        formData = request.form
        user = UserController()
        result = user.new_customer_address(formData['street'], formData['district'], formData['city'], formData['state']
                                           , formData['country'], formData['customer_id'])
        if result:
            return redirect(url_for('view_customer', id=formData['customer_id']))

@app.route('/editaddress/<int:id>')
def edit_address(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        address = AddressController()
        result = address.get_address_by_id(id)
        return render_template('editaddress.html', address=result,user=session['user'])


@app.route('/editaddressaction', methods=['POST'])
def edit_address_action():
    if request.form:
        formData = request.form
        user = UserController()
        result = user.edit_customer_address(formData['id'], formData['street'], formData['district'], formData['city']
                                            , formData['state'] , formData['country'], formData['customer_id'])
        if result:
            return redirect(url_for('view_customer', id=formData['customer_id']))

@app.route('/deleteaddress/<int:id>')
def delete_address_action(id):
    address = AddressController()
    result = address.delete_address(id)
    if result:
        return redirect(url_for('view_customer', id=result))
    return redirect(url_for('list_customers'))
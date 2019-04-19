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
            flash(result[0], result[1])
            return redirect(url_for('login'))
    return redirect(url_for('register'))



@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('dashboard.html', user=session['user'])


@app.route('/newcustomer')
def new_customer():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('newcustomer.html')


@app.route('/createcustomer', methods=["POST"])
def create_customer():
    if request.form :
        formData = request.form
        user = UserController()
        result = user.create_customer(formData['name'], formData['date_birth'], formData['cpf'], formData['rg'], formData['phone'])
        if result:
            flash(result[0], result[1])
            return redirect(url_for('list_cutomers'))

    flash('Erro ao cadastrar cliente', 'error')
    return redirect(url_for('new_customer'))


@app.route('/listcustomers')
def list_customers():
    customer = CustomerController()
    result = customer.get_all_customers()
    if result:
        return render_template('listcustomers.html', customers=result)
    return "Não tem cliente"


@app.route('/viewcustomer/<int:id>')
def view_customer(id):
    customer = CustomerController()
    address = AddressController()
    result = customer.get_customer_by_id(id)
    locations = address.get_address_by_customer_id(id)
    if result:
        return render_template('customerview.html', customer=result, addresses=locations)
    return "Não tem cliente"


@app.route('/deletecustomer/<int:id>')
def delete_customer(id):
    customer = CustomerController()
    result = customer.delete_customer(id)
    if result:
        flash(result[0], result[1])
    flash
    return redirect(url_for('list_customers'))


@app.route('/editcustomer/<int:id>')
def edit_customer(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        customer = CustomerController()
        result = customer.get_customer_by_id(id)
        return render_template('editcustomer.html', customer=result)


@app.route('/editcustomeraction', methods=["POST"])
def edit_customer_action():
    if request.form :
        formData = request.form
        user = UserController()
        result = user.edit_customer(formData['id'], formData['name'], formData['date_birth'], formData['cpf']
                                    , formData['rg'], formData['phone'])
        if result:
            flash(result[0], result[1])
            return redirect(url_for('view_customer', id=formData['id']))


@app.route('/newaddress/<int:customer_id>')
def new_address(customer_id):
    if not customer_id:
        flash(['Não foi possível adicionar um novo endereço', 'error'])
        return redirect(url_for('list_customers'))

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('newaddress.html', customer_id = customer_id)


@app.route('/newaddressaction', methods=["POST"])
def new_address_action():
    if request.form :
        formData = request.form
        user = UserController()
        result = user.new_customer_address(formData['street'], formData['district'], formData['city'], formData['state']
                                           , formData['country'], formData['customer_id'])
        if result:
            flash(result[0], result[1])
            return redirect(url_for('view_customer', id=formData['customer_id']))

@app.route('/editaddress/<int:id>')
def edit_address(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        address = AddressController()
        result = address.get_address_by_id(id)
        return render_template('editaddress.html', address=result)


@app.route('/editaddressaction', methods=['POST'])
def edit_address_action():
    if request.form:
        formData = request.form
        user = UserController()
        result = user.edit_customer_address(formData['id'], formData['street'], formData['district'], formData['city']
                                            , formData['state'] , formData['country'], formData['customer_id'])
        if result:
            flash(result[0], result[1])
            return redirect(url_for('view_customer', id=formData['customer_id']))

@app.route('/deleteaddress/<int:id>')
def delete_address_action(id):
    address = AddressController()
    result = address.delete_address(id)
    print(result)
    if result:
        if len(result) == 3:
            flash(result[0], result[1])
            return redirect(url_for('view_customer', id=result[2]))
        flash(result[0], result[1])
        return redirect(url_for('list_customers'))
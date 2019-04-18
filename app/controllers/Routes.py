from flask import render_template, request, url_for, session, redirect, flash
from app import app
from app.controllers.UserController import UserController
from app.controllers.CustomerController import CustomerController


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

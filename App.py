from datetime import date, datetime
from pickle import FALSE
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_recaptcha import ReCaptcha
from babel.numbers import format_decimal
from authy.api import AuthyApiClient
 


# Models
from models.ModelUser import ModelUser
from models.ModelTransactions import ModelTransactions
from models.ModelCred import ModelCred
from models.ModelMenu import ModelMenu
from models.ModelHome import ModelHome
from models.ModelInserts import ModelInserts
from models.ModelUpdate import ModelUpdate

# Entities
from models.entities.User import User

# Initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'communitybankv2'


# Twilio config (verification code)
AUTHY_API_KEY = "6Bq2dnV0AVy53xHS2RpyNIIyR9SZmiUo"
api = AuthyApiClient(AUTHY_API_KEY)

csrf=CSRFProtect()
db = MySQL(app)

# Apps
login_manager_app = LoginManager(app)
recaptcha = ReCaptcha(app)

# Settings
app.secret_key = "8e1d1495f307f9254e9955a04f3ae537946a904db6a59d73"
app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_SITE_KEY = "6Le8DLUeAAAAALK0wKU246dW9I-PAtSYsVaj1G9R",
    RECAPTCHA_SECRET_KEY = "6Le8DLUeAAAAAOnYnPjBzAsq8K34a1tmc_tBeAQA",
))

recaptcha = ReCaptcha()
recaptcha.init_app(app)

# cargadores de datos del usuario logueado
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_data(db,id)

# Routes
@app.route('/')
def Index():
    session['page'] = 'home'
    return render_template('/pages/app-about.html')

# Convierte numero int a pesos colombianos
@app.template_filter()
def currencyFormat(value):
    return format_decimal(value, locale='es_CO')

# C
@app.template_filter()
def calculeStocks(len):
    stock_value = 10000
    return format_decimal(len * stock_value, locale='es_CO')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    else:
        return render_template('/login/app-login.html')
        
# if recaptcha.verify(): ,else: flash('Error ReCaptcha') return redirect(url_for('login'))
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        identity = request.form['identity']
        password = request.form['password']
        user = User(0,identity,password)
        logged_user=ModelUser.login(db,user)
        if logged_user != None:
            session['identity'] = identity
            session['password'] = password
            session['islogin'] = True
            return redirect(url_for('verification'))
        else:
            flash('Incorrect username or password')
            return redirect(url_for('login'))
        


@app.route('/verification', methods=['GET', 'POST'])
def verification():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    else:
        if session.get("islogin"):
            return render_template('/login/app-verification.html')
        else:
            return redirect(url_for('login'))


@app.route('/verifications', methods=['GET', 'POST'])
def verifications():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    else:
        if session.get("islogin"):
            identity = session.get("identity")
            country_code = "57"
            phone_number = ModelUser.getphone(db, identity)
            method = "sms"
            session['country_code'] = country_code
            session['phone_number'] = phone_number
            print("enviado")
            api.phones.verification_start(phone_number, country_code, via=method)
            return ("OK")
        else:
            return redirect(url_for('login'))
        
        
@app.route("/verify", methods=["GET", "POST"])
def verify():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    else:
        if session.get("islogin"):
            if request.method == "POST":
                token = request.form.get("token")
                phone_number = session.get("phone_number")
                country_code = session.get("country_code")
                
                verification = api.phones.verification_check(phone_number,
                                                            country_code,
                                                            token)

                if verification.ok():
                    identity = session.get("identity")
                    password = session.get("password")
                    user = User(0,identity,password)
                    logged_user=ModelUser.login(db,user)
                    login_user(logged_user)
                    return redirect(url_for('home'))
                else:
                    flash('Incorrect SMS verification code')
                    return redirect(url_for('verification'))

            return render_template('/login/app-verification.html')
        else:
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('Index'))


@app.route('/transactions', methods=["GET", "POST"])
@login_required
def transactions():
    session['page'] = 'trans'
    transactionsCuotas=ModelTransactions.transactions(session['identity'],db)
    transactionsIntereses=ModelTransactions.transactionsIntereses(session['identity'],db)
    transactionsStocks=ModelTransactions.transactionsStocks(session['identity'],db)
    transactionsLiq=ModelTransactions.transactionsLiqGa(session['identity'],db)
    transactions = transactionsCuotas + transactionsIntereses + transactionsStocks + transactionsLiq
    transactions.sort(reverse=True)
    earnings = ModelMenu.earnings(session['identity'],db)
    return render_template('/pages/transactions.html', transactions = transactions, earnings = earnings)


@app.route('/creditHist', methods=["GET", "POST"])
@login_required
def creditHist():
    session['page'] = 'credit'
    credits = ModelCred.ValueCre(session['identity'],db)
    earnings = ModelMenu.earnings(session['identity'],db)
    return render_template('/pages/creditHist.html', credits = credits, earnings = earnings)


@app.route('/buy_stocks', methods=["GET", "POST"])
@login_required
def buyStocks():
    session['page'] = 'stock'
    earnings = ModelMenu.earnings(session['identity'],db)
    return render_template('/pages/buyStocks.html', earnings = earnings)



@app.route('/make_credit', methods=["GET", "POST"])
@login_required
def checkCredit():
    loadcredit = ModelUser.credit(session['identity'], db)
    if loadcredit != None:
        flash('You already have a credit')
        return redirect(url_for('creditHist'))
    else:
        return redirect(url_for('makeCredit'))


@app.route('/make_credits', methods=["GET", "POST"])
@login_required
def makeCredit():
    session['page'] = 'credit'
    earnings = ModelMenu.earnings(session['identity'],db)
    return render_template('/pages/credits.html', earnings = earnings)

@app.route('/create_credit', methods=["GET", "POST"])
@login_required
def create_credit():
    if request.method == "POST":
        today = date.today()
        dateF = today.strftime("%Y-%m-%d")
        vCredito = request.form['ValorCredit']
        cuotas = request.form['cuotas']
        vCuotas = request.form['valorCuota']
        intereses = request.form['totalIntereses']
        valor_total = int(vCredito)+int(intereses)
        ModelInserts.InsertCredit(session['identity'],db, dateF, vCredito, cuotas, vCuotas, intereses)
        ModelInserts.InsertCreditOperation(session['identity'], db, dateF, vCredito)
        ModelInserts.InsertStatusPart(session['identity'], db, valor_total, cuotas, vCuotas)
        flash('Your credit has been created correctly')
        return redirect(url_for('creditHist'))


@app.route('/buy', methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        today = date.today()
        dateF = today.strftime("%Y-%m-%d")
        acts = request.form['stocks']
        ModelInserts.InsertStock(session['identity'],db,dateF, acts)
        ModelInserts.InsertStockhis(session['identity'],db,dateF, acts)
        ModelInserts.InsertStockStatus(session['identity'],db, acts)
        flash('Your shares have been successfully purchased')
        return redirect(url_for('home'))



@app.route('/home')
@login_required
def home():
    session['page'] = 'home'
    earnings = ModelMenu.earnings(session['identity'],db)
    currStock = ModelHome.ValueStoks(session['identity'],db)
    currCred = ModelHome.CreditActual(session['identity'],db)
    pendCuot = ModelHome.PendCuot(session['identity'],db)
    totalStocks = ModelHome.TotalStocks(session['identity'],db)
    valueCuot = ModelHome.ValueCuot(session['identity'],db)
    return render_template('/home/app-home.html', earnings = earnings,
                           currStock = currStock , currCred = currCred,
                           pendCuot = pendCuot, totalStocks = totalStocks,
                           valueCuot = valueCuot)



@app.route('/update', methods = ['GET', 'POST'])
@login_required
def update():
    earnings = ModelMenu.earnings(session['identity'],db)
    return render_template('/home/app-contact.html', earnings = earnings)

#############################################


@app.route('/admin_members', methods = ['GET', 'POST'])
@login_required
def admin_members():
    cur = db.connection.cursor()
    cur.execute("SELECT type FROM partner WHERE cc = '{}'".format(session['identity']))
    data = cur.fetchall()
    if data[0][0] == 1:
        session['page'] = 'admin'
        cur = db.connection.cursor()
        cur.execute('SELECT cc, Nombre, Email, Telefono FROM partner')
        data = cur.fetchall()
        cur.close()
        earnings = ModelMenu.earnings(session['identity'],db)
        return render_template('/crud/admin_members.html', earnings = earnings, dataUsers = data)
    else:
        flash('You are not the administrator')
        return redirect(url_for('home'))


@app.route('/partners', methods = ['GET', 'POST'])
@login_required
def partners():
    cur = db.connection.cursor()
    cur.execute("SELECT Nombre FROM partner")
    data = cur.fetchall()
    cur.close()
    earnings = ModelMenu.earnings(session['identity'],db)
    return render_template('/pages/partners.html', earnings = earnings, partners = data)


@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_users(id):
    session['page'] = 'editUser'
    cur = db.connection.cursor()
    cur.execute("SELECT Nombre, Email, Telefono FROM partner WHERE cc = '{}'".format(id))
    data = cur.fetchall()
    cur.close()

    earnings = ModelMenu.earnings(session['identity'],db)

    cur = db.connection.cursor()
    cur.execute("SELECT id, Fecha_credito, Valor_credito, Cuotas_credito, Valor_cuota, Interes_prestamo FROM credithis WHERE cc = '{}'".format(id))
    credit = cur.fetchall()
    cur.close()
    list_credts = [list(i) for i in credit]

    cur = db.connection.cursor()
    cur.execute("SELECT id, fecha_compra, cantidad FROM stockhis WHERE cc = '{}'".format(id))
    stocks = cur.fetchall()
    cur.close()
    list_stocks = [list(i) for i in stocks]

    return render_template('/crud/edit_person.html', earnings = earnings, contact = data[0], credit=list_credts, stock=list_stocks )


@app.route('/mark_paid/<id>', methods = ['GET', 'POST'])
@login_required
def mark_paid(id):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM credithis WHERE id = '{}'".format(id))
    data = cur.fetchall()
    db.connection.commit()
    cur.close()
    return redirect(url_for('admin_members'))


@app.route('/add_member', methods = ['GET', 'POST'])
@login_required
def add_member():
    session['page'] = 'add_member'
    earnings = ModelMenu.earnings(session['identity'],db)
    return render_template('/crud/add_person.html', earnings = earnings)


@app.route('/create_member', methods = ['GET', 'POST'])
@login_required
def create_member():
    if request.method == 'POST':
        session['page'] = 'add_member'
        cc = request.form['cc']
        nombre = request.form['nombre']
        email = request.form['email']
        tel = request.form['tel']
        password = request.form['password']

        cur = db.connection.cursor()
        cur.execute("INSERT INTO partner VALUES('{0}', '{1}', '{2}', '{3}', '{4}', 0)".format(cc, nombre, email, tel, password))
        db.connection.commit()
        cur.close()
        return redirect(url_for('admin_members'))



#############################################
@app.route('/update_data', methods = ['GET', 'POST'])
@login_required
def update_data():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        ModelUpdate.update(session['identity'], db, fullname, phone, email)
        return redirect(url_for('home'))

def status_401(error):
    return redirect(url_for('Index'))

def status_404(error):
    return render_template('/pages/404.html')

# Starting the app
if __name__ == "__main__":
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run(debug=True)

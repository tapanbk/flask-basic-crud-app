from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.secret_key = "Random Key"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


def logged_in(view_function):
    def wrapper(*args, **kwargs):
        if not session.get('username') and not session.get('is_logged_in'):
            flash("UnAuthorized")
            return redirect(url_for('login'))
        return view_function(*args, **kwargs)
    return wrapper


def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


def check_if_password_is_valid(database_password, input_password):
    return bcrypt.check_password_hash(database_password, input_password)


class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(200))
    address = db.Column(db.String(200))
    password = db.Column(db.String(200))

    def __init__(self, first_name, last_name, email, phone, address, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
        self.password = hash_password(password)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



@app.route('/')
def home():
        return render_template('home.html')


@app.route('/create/', methods=['POST', 'GET'], endpoint="create")
@logged_in
def create():
    form = {}
    if request.method == "POST":
        form = request.form
        try:
            user = User(**form)
            db.session.add(user)
            db.session.commit()
            message = 'Successfully inserted'
            flash(message)
            return redirect(url_for('home'))
        except Exception as e:
            message = 'Failed'
            flash(message)
        return render_template('create.html', user=form)
    return render_template('create.html', user=form)


@app.route('/user/<int:userId>/details/')
def details(userId):
    user = User.query.filter_by(id= userId).first()
    return render_template('details.html', user=user)



@app.route('/edit/<int:userId>/', methods=['GET',"POST"], endpoint="userEdit")
@logged_in
def userEdit(userId):
    # user_instance = User.query.filter_by(id=userId).first()
    user_instance = db.get_or_404(User, userId)
    if request.method == "POST":
        form = request.form
        try:
            user_instance.first_name = form.get('first_name')
            user_instance.last_name = form.get('last_name')
            user_instance.email = form.get('email')
            if form.get('password'):
                user_instance.password = hash_password(form.get('password'))
            user_instance.address = form.get('address')
            user_instance.phone = form.get('phone')
            db.session.commit()
            message = 'Successfully updated'
            flash(message, "info")
            return redirect(url_for('list'))
        except Exception as e:
            message = 'Failed'
            flash(message)
        return render_template('edit.html', user=form)
    return render_template('edit.html', user=user_instance)

@app.route('/list', endpoint='list')
@logged_in
def list():
    users = User.query.all()
    return render_template('list.html', users=users)


@app.route('/user/<int:userId>/', methods=['GET', "POST"])
def userDelete(userId):
    user_instance = db.get_or_404(User, userId)
    if request.method == "POST":
        try:
            db.session.delete(user_instance)
            db.session.commit()
            message = 'Successfully deleted'
            flash(message)
            return redirect(url_for('list'))
        except Exception as e:
            message = 'Failed'
            flash(message)
    return render_template('delete.html', user=user_instance)


@app.route('/login', methods=['GET', 'POST'])
def login():
    user_details = {
        "email": ""
    }
    if request.method == 'GET':
        return render_template('login.html', user_details=user_details)

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_details["email"] = email

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Credentials does not match")
            return render_template('login.html', user_details=user_details)
        if not check_if_password_is_valid(user.password, password):
            flash("Credentials does not match")
            return render_template('login.html', user_details=user_details)
        session['is_logged_in'] = True
        session['full_name'] = f'{user.first_name} {user.last_name}'
        flash("Successfully Logged in")
        return redirect(url_for('list'))


@app.route('/logout')
def logout():
    session.pop('is_logged_in', None)
    session.pop('username', None)
    flash("Successfully Logged out")
    return redirect(url_for('login'))


@app.errorhandler(404)
def invalid_route(e):
    return render_template('404.html')


@app.errorhandler(500)
def invalid_route(e):
    return render_template('500.html')

if __name__ == '__main__':
    app.run(debug=True)

import os
import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for, session, escape
from decorators import login_required, redirect_if_logged
from dotenv import load_dotenv
import bcrypt
from forms import RegistrationForm, LoginForm

from db import get_db, init_db


load_dotenv(dotenv_path='.env')

app = Flask(__name__, static_folder='assets')
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


def authenticate_user(username_email, password):

    if username_email != "" and password != "":
        with get_db() as conn:
            cur = conn.cursor()

            user = cur.execute(
                "SELECT * FROM users WHERE username = '%s' OR email = '%s'" % (username_email, username_email)).fetchone()
            if(user != None):
                if(bcrypt.checkpw(password.encode("utf-8"), user[3].encode("utf-8"))):
                    return True
            return False
    else:
        return False


def check_user_exists(username):
    with get_db() as conn:
        cur = conn.cursor()

        user = cur.execute(
            "SELECT * FROM users WHERE username = '%s'" % (username)).fetchone()
        if user:
            return True
        return False


def check_email_exists(email):
    with get_db() as conn:
        cur = conn.cursor()

        user = cur.execute(
            "SELECT * FROM users WHERE email = '%s'" % (email)).fetchone()
        if user:
            return True
        return False


def create_user(fields):
    with get_db() as conn:
        cur = conn.cursor()

        user = cur.execute("INSERT INTO users(username, email, password, created_at) VALUES('%s','%s','%s', datetime())" % (
            fields[0], fields[1], bcrypt.hashpw(fields[2].encode('utf-8'), bcrypt.gensalt(14)).decode('utf-8')))

        conn.commit()


def find_username(login_input):
    with get_db() as conn:
        cur = conn.cursor()

        username = cur.execute("SELECT username FROM users WHERE username = '%s' OR email = '%s'" % (
            login_input, login_input)).fetchone()
        return username


@ app.route("/")
@ redirect_if_logged
def index():
    return render_template("index.html")


@ app.route("/login", methods=['GET', 'POST'])
@ redirect_if_logged
def login():
    form = LoginForm()
    if request.method == 'POST':
        user = authenticate_user(
            escape(form.username_email.data.lower()), escape(form.password.data))
        if(user):
            session['user'] = user
            session['current_username'] = find_username(
                form.username_email.data)
            return redirect(url_for('dashboard'))
        flash("Brukernavnet eller passordet er feil", "error")

    return render_template("login.html", form=form)

# Register page


@ app.route("/register", methods=['GET', 'POST'])
@ redirect_if_logged
def register():
    form = RegistrationForm()  # Takes in the registration form
    if form.validate_on_submit():
        user = check_user_exists(
            escape(form.username.data))
        email = check_email_exists(escape(form.email.data))
        if not user:
            if not email:
                form_input = [escape(field.data) for field in form]
                create_user(form_input)
                flash(
                    f'Brukerkonto laget for {form.username.data}!', 'success')

                return redirect(url_for('login'))
            flash(f'Eposten er allerede i bruk', 'error')
            return redirect(url_for('register'))
        flash(f'Brukernavnet er allerede i bruk', 'error')
        return redirect(url_for('register'))
    return render_template('register.html', form=form)


@ app.route("/dashboard")
@ login_required
def dashboard():
    return render_template('dashboard.html', user=session['user'])


@ app.route("/logout")
@ login_required
def logout():
    session.clear()
    flash("Du har blitt logget ut!", "success")
    return redirect(url_for('index'))


@ app.route("/get")
def get_names():
    with get_db() as conn:
        cur = conn.cursor()

        for name in cur.execute("SELECT * FROM names"):
            print(name)

    return "True"


@app.route('/account')
@login_required
def account():
    return render_template('account.html')


if __name__ == "__main__":
    app.run()

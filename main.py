import psycopg2
from flask import Flask, render_template, redirect, url_for, flash, request
import sqlite3
from form import RegisterForm, LoginFarm
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "xcvxkbv45y3747w34yzb"
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

conn = psycopg2.connect(host="localhost", database="cafe", user="postgres", password=9992, port=5432)


class User(UserMixin):
    def __init__(self, id, name, email, password):
        self.id = id,
        self.name = name,
        self.email = email,
        self.password = password

@login_manager.user_loader
def load_user(id):
    pass

@app.route("/", methods=["GET", "POST"])
def home():
    con = sqlite3.connect('instance/cafes.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM cafe")
    cafes = cur.fetchall()
    con.close()

    cafe_data = []
    for cafe in cafes:
        cafe_data.append({
            "id": cafe[0],
            "name": cafe[1],
            "map_url": cafe[2],
            "img_url": cafe[3],
            "location": cafe[4],
            "has_sockets": cafe[5],
            "has_toilet": cafe[6],
            "has_wifi": cafe[7],
            "can_take_calls": cafe[8],
            "seats": cafe[9],
            "coffee_price": cafe[10]
        })

    return render_template("index.html", cafe_data=cafe_data)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    name = form.name.data
    email = form.email.data
    password = form.password.data


    if form.validate_on_submit():

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)

        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))

        if cur.fetchone():
            flash("User already exists please login instead.", "danger")
            return redirect("login")
        else:
            cur.execute("INSERT INTO users(name, email, password) VALUES(%s, %s, %s)", (name, email, hashed_password))
            conn.commit()
            flash("Registration successful (demo).", "success")
        return redirect(url_for('home'))

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginFarm()
    email = form.email.data
    password = form.password.data
    if form.validate_on_submit():
        # Demo login behavior: accept any credentials for now
        flash(f"Logged in as {email} (demo)", "success")
        return redirect(url_for('home'))

    return render_template("login.html", form=form)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")

@app.route("/cafe/<int:cafe_id>")
def cafe(cafe_id):
    con = sqlite3.connect('instance/cafes.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM cafe WHERE id = ?", (cafe_id,))
    cafe = cur.fetchone()
    con.close()

    if not cafe:
        flash("Cafe not found", "warning")
        return redirect(url_for('home'))

    cafe_data = {
        "id": cafe[0],
        "name": cafe[1],
        "map_url": cafe[2],
        "img_url": cafe[3],
        "location": cafe[4],
        "has_sockets": cafe[5],
        "has_toilet": cafe[6],
        "has_wifi": cafe[7],
        "can_take_calls": cafe[8],
        "seats": cafe[9],
        "coffee_price": cafe[10]
    }

    return render_template("cafe.html", cafe=cafe_data)



if __name__ == "__main__":
    app.run(debug=True)
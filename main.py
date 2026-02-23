import psycopg2
from flask import Flask, render_template, redirect, url_for, flash, request
import sqlite3
from form import RegisterForm, LoginFarm
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "xcvxkbv45y3747w34yzb"
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id, name, email, password):
        self.id = id,
        self.name = name,
        self.email = email,
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    try:
        conn = psycopg2.connect(host="localhost", database="cafe", user="postgres", password=9992, port=5432)

        cur = conn.cursor()
        cur.execute("""
                    SELECT u.id, u.name, u.email, u.password
                       FROM users u 
                       WHERE id = %s
                    """, (user_id,))

        user = cur.fetchone()

        if user:
            return User(id=user[0], name=user[1], email=user[2], password=user[3])
    except psycopg2.Error as e:
        print(f"There was a problem connecting to the database: {e}")
    return None


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

    return render_template("index.html", cafe_data=cafe_data, current_user=current_user)

@app.route("/register", methods=["GET", "POST"])
def register():
    conn = psycopg2.connect(host="localhost", database="cafe", user="postgres", password=9992, port=5432)

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

        cur.execute("INSERT INTO users(name, email, password) VALUES(%s, %s, %s)", (name, email, hashed_password))
        conn.commit()
        flash("Registration successful (demo).", "success")

        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        user_id = cur.fetchone()

        user = User(id=user_id, name=name, email=email, password=hashed_password)
        login_user(user)
        return redirect(url_for('home'))

    return render_template("auth/register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginFarm()
    conn = psycopg2.connect(host="localhost", database="cafe", user="postgres", password=9992, port=5432)

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, name, email, password FROM users WHERE email = %s",
                (email,)
            )
            user = cur.fetchone()

            if not user:
                flash("This email does not exist. Please register first.", "danger")
                return redirect(url_for("auth.login"))

            if not check_password_hash(user[3], password):
                flash("Incorrect password.", "danger")
                return redirect(url_for("auth.login"))

            user_obj = User(
                id=user[0],
                name=user[1],
                email=user[2],
                password=user[3]
            )

            login_user(user_obj)
            flash(f"Logged in as {email}", "success")
            return redirect(url_for("home"))

        except psycopg2.Error as error:
            conn.rollback()
            flash(f"Database error: {error}", "danger")

        finally:
            cur.close()

    return render_template("auth/login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("You have been successfully logged out.", "success")
    return redirect(url_for("home"))

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

    return render_template("cafe.html", cafe=cafe_data, current_user=current_user)



if __name__ == "__main__":
    app.run(debug=True)
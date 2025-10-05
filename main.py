from flask import Flask, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)


@app.route("/")
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

if __name__ == "__main__":
    app.run(debug=True)
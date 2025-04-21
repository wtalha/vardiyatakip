
from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)

def init_db():
    with sqlite3.connect("vardiyalar.db") as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS vardiyalar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT,
            vardiya TEXT,
            tarih TEXT
        )
        """)

@app.route("/", methods=["GET", "POST"])
def index():
    init_db()
    today = date.today().isoformat()

    if request.method == "POST":
        isim = request.form["isim"].strip()
        vardiya = request.form["vardiya"]
        if isim:
            with sqlite3.connect("vardiyalar.db") as con:
                con.execute("REPLACE INTO vardiyalar (id, isim, vardiya, tarih) VALUES ((SELECT id FROM vardiyalar WHERE isim=? AND tarih=?), ?, ?, ?)",
                            (isim, isim, vardiya, today))

    with sqlite3.connect("vardiyalar.db") as con:
        kayitlar = con.execute("SELECT isim, vardiya FROM vardiyalar WHERE tarih=?", (today,)).fetchall()

    return render_template("index.html", kayitlar=kayitlar)

if __name__ == "__main__":
    app.run(debug=True)

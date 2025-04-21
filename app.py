from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Veritabanı bağlantısı
def get_db_connection():
    conn = sqlite3.connect('vardiya.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ana sayfa ve form gönderimi
@app.route("/", methods=["GET", "POST"])
def index():
    tarih = datetime.now().strftime("%Y-%m-%d")  # Bugünün tarihi (GET ve POST isteklerinde kullanılacak)

    if request.method == "POST":
        # Formdan verileri al
        isim = request.form.get("isim")
        vardiya = request.form.get("vardiya")

        # Eğer isim ya da vardiya boşsa, hata döndür
        if not isim or not vardiya:
            return "İsim ve vardiya seçimi zorunludur.", 400

        # Veritabanına bağlan
        conn = get_db_connection()
        cursor = conn.cursor()

        # Kayıt işlemi (varsa güncelle, yoksa yeni ekle)
        cursor.execute("""
            INSERT OR REPLACE INTO vardiyalar (isim, vardiya, tarih)
            VALUES (?, ?, ?)
        """, (isim, vardiya, tarih))

        # Değişiklikleri kaydet ve bağlantıyı kapat
        conn.commit()
        conn.close()

    # Veritabanından tüm verileri çek
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vardiyalar WHERE tarih = ?", (tarih,))
    vardiyalar = cursor.fetchall()
    conn.close()

    # Ana sayfayı render et ve vardiya listelerini gönder
    return render_template("index.html", vardiyalar=vardiyalar)

if __name__ == "__main__":
    app.run(debug=True)

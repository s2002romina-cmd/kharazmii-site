from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import os  # اضافه کردن برای پورت

app = Flask(__name__)

# ساخت دیتابیس اگر وجود نداشته باشد
def init_db():
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            comment TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()  # اجرای اولیه

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        comment = request.form.get("comment")
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if name and comment:
            conn = sqlite3.connect('comments.db')
            c = conn.cursor()
            c.execute("INSERT INTO comments (name, comment, date) VALUES (?, ?, ?)", (name, comment, date))
            conn.commit()
            conn.close()

        return redirect("/")  # بعد ثبت، دوباره فرم خالی میشه

    # GET → فرم نمایش داده میشه
    return render_template("index.html")

# 🟢 تغییر اصلی برای Render
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",  # مهم برای دسترسی عمومی
        port=int(os.environ.get("PORT", 5000)),  # Render خودش پورت اختصاص میده
        debug=True
    )

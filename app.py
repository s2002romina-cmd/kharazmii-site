from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

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

    # اگر GET باشه فقط فرم نمایش داده میشه، نظرات تو صفحه اصلی دیده نمیشه
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

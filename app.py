from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# DATABASE CREATE
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # USERS TABLE
    c.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        password TEXT
    )
    ''')

    # CARS TABLE
    c.execute('''
    CREATE TABLE IF NOT EXISTS cars(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_name TEXT,
        model TEXT,
        rent TEXT,
        owner_name TEXT,
        phone TEXT
    )
    ''')

    conn.commit()
    conn.close()


init_db()


# HOME PAGE
@app.route('/')
def home():
    return render_template('home.html')


# REGISTER PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("""
        INSERT INTO users(username, email, password)
        VALUES (?, ?, ?)
        """, (username, email, password))

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("""
        SELECT * FROM users
        WHERE email=? AND password=?
        """, (email, password))

        user = c.fetchone()

        conn.close()

        if user:
            return redirect('/dashboard')
        else:
            return "Invalid Email or Password"

    return render_template('login.html')


# DASHBOARD PAGE
@app.route('/dashboard')
def dashboard():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM cars")
    cars = c.fetchall()

    conn.close()

    return render_template(
        'dashboard.html',
        cars=cars
    )


# ADD CAR PAGE
@app.route('/add_car', methods=['GET', 'POST'])
def add_car():

    if request.method == 'POST':

        car_name = request.form['car_name']
        model = request.form['model']
        rent = request.form['rent']
        owner_name = request.form['owner_name']
        phone = request.form['phone']

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("""
        INSERT INTO cars(
        car_name,
        model,
        rent,
        owner_name,
        phone
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            car_name,
            model,
            rent,
            owner_name,
            phone
        ))

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('add_car.html')


# DELETE CAR
@app.route('/delete/<int:id>')
def delete_car(id):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        "DELETE FROM cars WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard')


# LOGOUT
@app.route('/logout')
def logout():
    return redirect('/')


# RUN WEBSITE
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

con = psycopg2.connect(database='loginpractice',
                       user='postgres', password='')


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        with con:
            cur = con.cursor()
            cur.execute(
                'SELECT EXISTS ( SELECT * FROM users WHERE name = %s and password = %s )', (username, password))

            is_valid_user = cur.fetchone()[0]

            if is_valid_user:
                return redirect(url_for('winelist'))
            else:
                error = "No way sucker"

    return render_template('login.html', error=error)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html", error=None)

    if request.method == "POST":
        error = None
        password = request.form['password_input']
        confirm_password = request.form['confirm_password_input']

        if password != confirm_password:
            error = "Passwords don't match. Try again."
            return render_template("signup.html", error=error)

        username = request.form['username_input'].strip()
        with con:
            cur = con.cursor()
            cur.execute('SELECT * FROM users WHERE name = %s', (username,))
            existing_users = cur.fetchone()
            if existing_users == None:
                cur.execute(
                    'INSERT INTO users (name, password) VALUES (%s, %s)', (username, password))
                return redirect(url_for('winelist'))

            else:
                error = "That user already exists. Pick a different username."

        return render_template("signup.html", error=error)


@app.route('/winelist')
def winelist():
    return "Here is your wine. Isn't it nice?"


if __name__ == "__main__":
    app.run(debug=True)


# TODO
# Use a layout.html to render header and footer everywhere

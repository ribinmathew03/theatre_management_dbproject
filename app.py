from flask import Flask, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="abhijith@35"
app.config['MYSQL_DB']="movieextra"
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

# Set a secret key for session management
app.secret_key = 'your_secret_key'

from flask import flash

# Placeholder functions for database interactions
def validate_admin_credentials(username, password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admins WHERE username = %s AND password = %s", (username, password))
    admin = cur.fetchone()
    cur.close()
    return admin is not None

def validate_user_credentials(username, password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()
    return user is not None

def insert_movie_details(title, description, photo_url):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO movies (title, description, photo_url) VALUES (%s, %s, %s)",
                (title, description, photo_url))
    mysql.connection.commit()
    cur.close()
    flash('Movie details added successfully', 'success')

def get_all_movies():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM movies")
    movies = cur.fetchall()
    cur.close()
    return movies

def get_movie_details(movie_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
    movie = cur.fetchone()
    cur.close()
    return movie

def insert_booking_details(user_id, movie_id, num_tickets, booking_date):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO bookings (user_id, movie_id, num_tickets, booking_date) VALUES (%s, %s, %s, %s)",
                (user_id, movie_id, num_tickets, booking_date))
    mysql.connection.commit()
    cur.close()
    flash('Booking details added successfully', 'success')


from flask import flash, render_template, redirect, url_for, request, session

# Routes for login and main page
@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_admin_credentials(username, password):
            session['username'] = username
            return redirect(url_for('admin_page'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('admin_login.html')

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_user_credentials(username, password):
            session['username'] = username
            return redirect(url_for('user_page'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('user_login.html')

# Admin Page
@app.route('/admin_page', methods=['GET', 'POST'])
def admin_page():
    if 'username' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        photo_url = request.form['photo_url']  # Assuming you have an input for photo_url in the form
        insert_movie_details(title, description, photo_url)

    return render_template('admin_page.html')

# User Page
@app.route('/user_page')
def user_page():
    if 'username' not in session:
        return redirect(url_for('user_login'))

    movies = get_all_movies()
    return render_template('user_page.html', movies=movies)

# Movie Description Page
@app.route('/movie_description/<int:movie_id>')
def movie_description(movie_id):
    movie_details = get_movie_details(movie_id)
    return render_template('movie_description.html', movie=movie_details)

# Booking Tickets
@app.route('/book_ticket/<int:movie_id>', methods=['GET', 'POST'])
def book_ticket(movie_id):
    if 'username' not in session:
        return redirect(url_for('user_login'))

    if request.method == 'POST':
        user_id = 1  # Replace with the actual user ID from the session
        num_tickets = int(request.form['num_tickets'])
        booking_date = request.form['booking_date']
        insert_booking_details(user_id, movie_id, num_tickets, booking_date)

    return render_template('book_ticket.html', movie_id=movie_id)

if __name__ == '__main__':
    app.run(debug=True)

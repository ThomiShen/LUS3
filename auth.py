
from flask import Blueprint, render_template, redirect, url_for, flash, request
import pymysql
import hashlib

auth = Blueprint('auth', __name__)

def get_db_connection():
    return pymysql.connect(host='localhost', user='root', password='12345678', database='test', charset='utf8mb4')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            if password != confirm_password:
                flash('Passwords do not match!', 'danger')
                return render_template('register.html')
                # Check if username exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                flash('Username already exists!', 'danger')
                return render_template('register.html')

            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            connection.commit()
            flash('注册成功，请登录！！！', '成功')
            return redirect(url_for('auth.login'))
    finally:
        connection.close()
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
            user = cursor.fetchone()
            if user:
                flash('登录成功!', '成功')
                # TODO: Handle user session and redirect to a protected page
                return redirect(url_for('index'))
            else:
                flash('Invalid credentials.', 'danger')
    finally:
        connection.close()
    return render_template('login.html')

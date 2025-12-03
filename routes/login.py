from flask import Blueprint, request, jsonify, render_template
import psycopg2
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import os

login_bp = Blueprint('login' , __name__)

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

@login_bp.route('/login' , methods=['GET','POST'])
def login():
    data = request.form
    email = data.get('email')
    password = data.get('password')

    try:
        conn = psycopg2.connect(
            dbname = DB_NAME,
            user = DB_USER,
            password = DB_PASSWORD,
            host = DB_HOST,
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user is None:
            return jsonify({'message': 'User does not exist'}), 401
        else:
            stored_password = user[2]
            if check_password_hash(stored_password, password):
                api_key = user[3]
                return render_template('apipage.html', api_key=api_key)
            else:
                return jsonify({'message': 'Wrong Password'}), 401
    except Exception as e:
        return jsonify({'message': str(e)}), 500

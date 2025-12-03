from flask import Blueprint, request, jsonify, render_template
import psycopg2, string, secrets
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os
register_bp = Blueprint('register' , __name__)

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

@register_bp.route('/register', methods=['POST'])
def register():
    data = request.form
    email = data.get('email')
    password = data.get('password')
    confirm = data.get('confirm')

    if password != confirm:
        return jsonify({'message': 'Passwords must match'}), 401
    hashed_password = generate_password_hash(password)

    #api key generation
    characters = string.ascii_letters + string.digits
    api_key = ''.join(secrets.choice(characters) for x in range(32))

    try:
        conn = psycopg2.connect(
            dbname = DB_NAME,
            user = DB_USER,
            password = DB_PASSWORD,
            host = DB_HOST
        )
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (email, password, api_key) VALUES (%s, %s, %s)",
            (email, hashed_password, api_key)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    return render_template('apipage.html', api_key=api_key)

import os
from dotenv import load_dotenv
import psycopg2

# Load .env file (same as before)
load_dotenv()


def lambda_handler(event, context):
    headers = event.get('headers', {}) or {}

    api_key = headers.get('x-api-key')

    if not api_key:
        query = event.get('queryStringParameters') or {}
        api_key = query.get('api_key')

    if not api_key:
        return deny()

    try:
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD']
        )
        cur = conn.cursor()

        cur.execute('SELECT id FROM users WHERE api_key = %s', (api_key,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return allow(row[0])   # pass user id
        else:
            return deny()

    except Exception as e:
        print("DB error:", e)
        return deny()

def allow(user_id):
    return {
        "isAuthorized": True,
        "context": {
            "userId": str(user_id)
        }
    }

def deny():
    return {
        "isAuthorized": False
    }

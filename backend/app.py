from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# Database Config (We get these from Kubernetes later)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PASS = os.environ.get('DB_PASS', 'password')

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database="postgres", user="postgres", password=DB_PASS)
    return conn

@app.route('/messages', methods=['GET', 'POST'])
def handle_messages():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create table if not exists (Lazy way for homework)
    cur.execute('CREATE TABLE IF NOT EXISTS messages (id serial PRIMARY KEY, content text);')
    conn.commit()

    if request.method == 'POST':
        content = request.json['content']
        cur.execute('INSERT INTO messages (content) VALUES (%s)', (content,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success"}), 201

    cur.execute('SELECT content FROM messages;')
    messages = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([msg[0] for msg in messages])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
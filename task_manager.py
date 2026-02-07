import os
import sqlite3
import psycopg2
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import dj_database_url

app = Flask(__name__)
CORS(app)

# --- DATABASE LOGIC ---
# Render provides a 'DATABASE_URL'. If it's not there, we use local SQLite.
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    if DATABASE_URL:
        # Connect to Postgres on Render
        return psycopg2.connect(DATABASE_URL, sslmode='require')
    else:
        # Connect to SQLite locally
        conn = sqlite3.connect("tasks.db")
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    if DATABASE_URL:
        # Postgres Syntax
        cur.execute('''CREATE TABLE IF NOT EXISTS tasks 
                       (id SERIAL PRIMARY KEY, 
                        title TEXT NOT NULL, 
                        done BOOLEAN DEFAULT FALSE)''')
    else:
        # SQLite Syntax
        cur.execute('''CREATE TABLE IF NOT EXISTS tasks 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         title TEXT NOT NULL, 
                         done BOOLEAN NOT NULL CHECK (done IN (0, 1)))''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, done FROM tasks ORDER BY id ASC")
    rows = cur.fetchall()
    
    tasks = []
    for row in rows:
        tasks.append({"id": row[0], "title": row[1], "done": bool(row[2])})
    
    cur.close()
    conn.close()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id", (data['title'], False))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "title": data['title'], "done": False}), 201

@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def toggle_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET done = NOT done WHERE id = %s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Toggled"}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Deleted"}), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

init_db()
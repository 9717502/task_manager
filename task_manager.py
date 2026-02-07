import json
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
# CORS allows the browser to communicate between the frontend and backend ports
CORS(app)

FILE_NAME = "tasks.json"

def load_tasks():
    """Reads tasks from the JSON file."""
    try:
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as f:
                return json.load(f)
        return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    """Writes tasks to the JSON file."""
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)

# 1. THE HOME ROUTE
# This sends your index.html file to the browser when you visit the main URL
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 2. GET ALL TASKS
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(load_tasks())

# 3. ADD NEW TASK
@app.route('/tasks', methods=['POST'])
def add_task():
    tasks = load_tasks()
    data = request.json
    if not data or 'title' not in data:
        return jsonify({"error": "Missing title"}), 400
        
    new_task = {
        "id": int(os.urandom(2).hex(), 16), # Generates a random numeric ID
        "title": data['title'],
        "done": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201

# 4. TOGGLE TASK STATUS
@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def toggle_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['done'] = not task.get('done', False)
            save_tasks(tasks)
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

# 5. DELETE TASK
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    new_list = [t for t in tasks if t['id'] != task_id]
    save_tasks(new_list)
    return jsonify({"message": "Deleted"}), 200

if __name__ == "__main__":
    # host='0.0.0.0' is required for GitHub Codespaces to expose the port
    app.run(debug=True, host='0.0.0.0', port=5000)
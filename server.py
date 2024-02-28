from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('todo_list.db')
    return conn

conn = sqlite3.connect('todo_list.db')
conn.execute("""CREATE TABLE IF NOT EXISTS tasks
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    completed INTEGER
                )
             """)

@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    tasks = cursor.execute("SELECT * FROM tasks WHERE completed=0 ORDER BY name")
    return render_template('todo_list.html', tasks=tasks)

@app.route("/add/task", methods=['POST'])
def add_task():
    task = request.form['task']
    print(task)
    conn = get_db_connection()
    conn.execute("INSERT INTO tasks (name, completed) VALUES (?, ?)", (task, 0))
    conn.commit()
    return redirect("/")


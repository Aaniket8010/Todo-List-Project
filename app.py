from flask import Flask, render_template, redirect, url_for, request
from forms import TaskForm
import pandas as pd
import uuid
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

EXCEL_FILE = 'tasks.xlsx'

# Initialize Excel file if it doesn't exist
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Task ID", "Task Name", "Deadline", "Completed"])
    df.to_excel(EXCEL_FILE, index=False)

def read_tasks():
    return pd.read_excel(EXCEL_FILE)

def write_tasks(df):
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/')
def home():
    df = read_tasks()
    total = len(df)
    completed = df['Completed'].sum()
    percent = round((completed / total) * 100, 2) if total > 0 else 0
    return render_template("home.html", percent=percent, total=total, completed=completed)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        df = read_tasks()
        new_task = {
            "Task ID": str(uuid.uuid4()),
            "Task Name": form.task_name.data,
            "Deadline": form.deadline.data,
            "Completed": False
        }
        # ✅ Use concat instead of deprecated append
        df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)
        write_tasks(df)
        return redirect(url_for('view_tasks'))
    return render_template("add_task.html", form=form)

@app.route('/view')
def view_tasks():
    sort_by = request.args.get('sort', 'Deadline')
    df = read_tasks()

    # Ensure the column exists and sort
    if sort_by in df.columns:
        df = df.sort_values(by=sort_by)
    return render_template("view_tasks.html", tasks=df.to_dict(orient='records'))

@app.route('/complete/<task_id>')
def mark_complete(task_id):
    df = read_tasks()
    df.loc[df['Task ID'] == task_id, 'Completed'] = True
    write_tasks(df)
    return redirect(url_for('view_tasks'))

if __name__ == '__main__':
    app.run(debug=True)

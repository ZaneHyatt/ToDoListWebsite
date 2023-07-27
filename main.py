from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from forms import CreateToDoForm
from datetime import date
import random

today = date.today()


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
bootstrap = Bootstrap(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://todo_db_6jri_user:hnHq3HCVdXWF9CXe3lG8ePQ3C7OufvPe@dpg-cj0qjjaip7vkfo41nbrg-a/todo_db_6jri'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ToDo(db.Model):
    __tablename__ = "ToDos"
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=True, nullable=False)
    date = db.Column(db.String(250), nullable=False)
    time = db.Column(db.String(250), nullable=False)
    statis = db.Column(db.String(250), nullable=False)
    color = db.Column(db.String(250), nullable=False)

db.create_all()


@app.route("/")
def home():
    all_todos = (ToDo.query.order_by(ToDo.id).all())[:5]
    todo_true = False
    doing_true = False
    done_true = False
    for todo in all_todos:
        if todo.statis == "todo":
            todo_true = True
        elif todo.statis == "doing":
            doing_true = True
        elif todo.statis == "done":
            done_true = True
    today_todos = ToDo.query.filter_by(date=str(today)).all()
    return render_template("index.html", todos=all_todos, today_todos=today_todos, todo_true=todo_true, doing_true=doing_true, done_true=done_true)

@app.route("/add", methods=["GET", "POST"])
def add_todo():
    form = CreateToDoForm()
    if form.validate_on_submit():
        print("true")
        new_todo = ToDo(
            task_name=form.task_name.data,
            description=form.description.data,
            date=form.date.data,
            time=str(form.time.data),
            statis="todo",
            color=random.choice(["#E8FFCE", "#ACFADF", "#94ADD7", "#7C73C0"]),
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)

@app.route("/all-todos")
def show_all_todos():
    all_todos = (ToDo.query.order_by(ToDo.id).all())
    return render_template("all_todos.html", todos=all_todos)

@app.route("/all-doings")
def show_all_doings():
    all_todos = (ToDo.query.order_by(ToDo.id).all())
    return render_template("all_doings.html", todos=all_todos)

@app.route("/all-dones")
def show_all_dones():
    all_todos = (ToDo.query.order_by(ToDo.id).all())
    return render_template("all_dones.html", todos=all_todos)

@app.route("/all-tasks")
def show_all_tasks():
    all_todos = (ToDo.query.order_by(ToDo.id).all())
    return render_template("all_tasks.html", todos=all_todos)

@app.route("/edit-todo/<int:todo_id>", methods=["GET", "POST"])
def edit(todo_id):
    post = ToDo.query.get(todo_id)
    edit_form = CreateToDoForm(
        task_name=post.task_name,
        description=post.description,
        date="",
        time="",
    )
    if edit_form.validate_on_submit():
        post.task_name = edit_form.task_name.data
        post.description = edit_form.description.data
        post.date = edit_form.date.data
        post.time = str(edit_form.time.data)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add.html", form=edit_form, is_edit=True)

@app.route("/set-doing/<int:todo_id>", methods=["GET", "POST"])
def do_task(todo_id):
    post = ToDo.query.get(todo_id)

    post.statis = "doing"
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/set-done/<int:todo_id>", methods=["GET", "POST"])
def finish_task(todo_id):
    post = ToDo.query.get(todo_id)

    post.statis = "done"
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete-todo/<int:todo_id>", methods=["DELETE", 'GET', 'POST'])
def delete_todo(todo_id):
    todo = ToDo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for("home"))

@app.route("/delete-all", methods=["DELETE", 'GET', 'POST'])
def delete_all_tasks():
    all_todos = ToDo.query.order_by(ToDo.id).all()
    for todo in all_todos:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from .models import User, Task
from . import db
from sqlalchemy.exc import IntegrityError

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            flash('Login successful!', 'success')
            return redirect(url_for('main.tasks'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful!', 'success')
        return redirect(url_for('main.login'))
    return render_template('signup.html')

@main.route('/tasks')
def tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@main.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        new_task = Task(title=title)
        db.session.add(new_task)
        try:
            db.session.commit()
            flash('Task added successfully!', 'success')
            return redirect(url_for('main.tasks'))  # Redirect to tasks page
        except IntegrityError as e:
            db.session.rollback()
            flash('Error: Failed to add task. Please check your input.', 'danger')
            current_app.logger.error('IntegrityError: %s', e)
            return redirect(url_for('main.add_task'))
    return render_template('tasks.html', tasks=Task.query.all())


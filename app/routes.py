from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LoginForm, PostForm
from app.models import User, Post

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print("This form is valid and has been submitted.")
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)

        check_user = User.query.filter( (User.username == username) | (User.email == email) ).all()

        if check_user:
            flash('Sorry! A user with that email and/or username already exists', 'danger')
            return redirect(url_for('signup'))

        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)

        flash(f'Thank you, {new_user.first_name} {new_user.last_name}, for signing up! \nLog in to your account and add an address!', 'success')

        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"Hurray! {user.username}, you're now logged in", "success")
            return redirect(url_for('index'))
        else:
            flash("Incorrect username and/or password", "danger")
            redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", "warning")
    return redirect(url_for('index'))

@app.route('/add_address', methods=['GET', 'POST'])
@login_required
def add_address():
    form = PostForm()
    if form.validate_on_submit():
        address = form.address.data
        new_address = Post(address=address, user_id=current_user.id)
        flash(f"Your address, {new_address.address}, has been added to your address book!", "success")
    return render_template('add_address.html', form=form)

@app.route('/address_book')
def address_book():
    addresses = Post.query.all()
    return render_template('address_book.html', addresses=addresses)
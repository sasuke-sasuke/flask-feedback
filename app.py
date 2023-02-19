from flask import Flask, redirect, render_template, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import NewUserForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'mychickensteve'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()

@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register user form"""
    form = NewUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        session['c_user'] = new_user.username 
        flash('Successfully created new account!', 'success')
        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        c_user = User.authenticate(username, password)
        if c_user:
            flash(f'Welcome Back, {c_user.username}', 'success')
            session['c_user'] = c_user.username
            return redirect(f'/users/{c_user.username}')
        else:
            form.username.errors = ['Invalid username/password.']
    return render_template('login.html', form=form)

@app.route('/secret/<username>')
def secret(username):
    if 'c_user' not in session:
        flash('Please login!', 'danger')
        return redirect('/login')
    c_user = User.query.filter_by(username=username).first()
    return render_template('secret.html', user=c_user)

@app.route('/logout')
def logout():
    session.pop('c_user')
    flash('Goodbye!', 'primary')
    return redirect('/login')

@app.route('/users/<username>')
def user_page(username):
    if 'c_user' not in session:
            flash('Please login!', 'danger')
            return redirect('/login')
    c_user = User.query.filter_by(username=username).first()
    return render_template('secret.html', user=c_user)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if 'c_user' not in session or username != session['c_user']:
        flash('Unauthorized!', 'danger')
        return redirect(f'/users/{username}')
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('c_user')
    flash('User deleted!', 'primary')
    return redirect('/register')
    
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def edit_feedback(username):
    if 'c_user' not in session or username != session['c_user']:
        flash('Not Allowed', 'danger')
        return redirect(f'/users/{username}')
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Feedback successfully added!', 'success')
        return redirect(f'/users/{username}')
    return render_template('feedback-form.html', form=form)
    

@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'c_user' not in session or feedback.username != session['c_user']:
        flash('Not Allowed!', 'danger')
        return redirect(f'/users/{feedback.username}')
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        flash('Update successful!', 'success')
        return redirect(f'/users/{session["c_user"]}')
    return render_template('update-feedback.html', form=form)

@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'c_user' not in session or feedback.username != session['c_user']:
        flash('Not Allowed!', 'danger')
        return redirect(f'/users/{feedback.username}')
    db.session.delete(feedback)
    db.session.commit()
    flash('Successfully deleted!', 'success')
    return redirect(f'/users/{session["c_user"]}')

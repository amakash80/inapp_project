from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, EmailField, SelectField, PasswordField, SelectMultipleField, SubmitField, widgets, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo,Regexp
from config import Config  # Make sure to import your Config class
from flask_login import login_user, LoginManager, logout_user, current_user, login_required
from flask_login import UserMixin
from flask import session


# Initialize the Flask application
app = Flask(__name__)

app.config.from_object(Config)

# Initialize database and migration
mydb_obj = SQLAlchemy(app)
migrate = Migrate(app, mydb_obj)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)
@login_manager.user_loader

#User loader for Flask-Login
@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

# Define the models
class User(mydb_obj.Model, UserMixin):
    __tablename__ = 'user'
    uid = mydb_obj.Column(mydb_obj.Integer, primary_key=True, autoincrement=True)
    uname = mydb_obj.Column(mydb_obj.String(100), nullable=False)
    udob = mydb_obj.Column(mydb_obj.Date, nullable=False)
    uemail = mydb_obj.Column(mydb_obj.String(100), unique=True, nullable=False)
    uphone = mydb_obj.Column(mydb_obj.String(15), nullable=False)
    upassword = mydb_obj.Column(mydb_obj.String(100), nullable=False)
    ugender = mydb_obj.Column(mydb_obj.String(10), nullable=False)
    ustate = mydb_obj.Column(mydb_obj.String(50), nullable=False)
    ucity = mydb_obj.Column(mydb_obj.String(50), nullable=False)
    urole = mydb_obj.Column(mydb_obj.String(50), nullable=False, default='user') #'admin' or 'user'
    qualifications = mydb_obj.relationship('Qualification', backref='user', lazy=True)
    
    # Override the get_id method to return the correct primary key
    def get_id(self):
        return str(self.uid)

class Qualification(mydb_obj.Model):
    __tablename__ = 'qualification'
    qid = mydb_obj.Column(mydb_obj.Integer, primary_key=True)
    qualification_type = mydb_obj.Column(mydb_obj.String(50), nullable=False)
    user_id = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('user.uid'), nullable=False)
    
class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    birthday = DateField('Birthday', format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    state = StringField('State of Domicile', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    
    # Multiple qualifications as checkboxes
    qualifications = SelectMultipleField(
        'Qualifications',
        choices=[('Diploma', 'Diploma'), ('Bachelors', 'Bachelors'), ('Masters', 'Masters')],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )
    
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=20),
        Regexp(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$', 
               message="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
    ])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
#WTForms for login
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')


#Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    role = request.args.get('role')  # Get the role from the URL (admin or user)

    form = LoginForm()  # Assuming you have a LoginForm with email and password fields

    if form.validate_on_submit():
        user = User.query.filter_by(uemail=form.email.data).first()

        if user and user.upassword == form.password.data:
            # Check if the role matches
            if role == 'admin' and user.urole != 'admin':
                flash('You are not authorized to sign in as an admin.', 'danger')
                return redirect(url_for('login', role='admin'))
            elif role == 'user' and user.urole != 'user':
                flash('You are not authorized to sign in as a user.', 'danger')
                return redirect(url_for('login', role='user'))
            
            # Log in the user
            login_user(user)
            session['user_id'] = user.uid
            flash(f'Welcome {user.uname}!', 'success')

            # Redirect to admin or user dashboard based on role
            if user.urole == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))

        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', form=form)

# Define the routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(uemail=form.email.data).first():
            flash('Email address already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        try:
            # Create new user object
            new_user = User(
                uname=f"{form.firstname.data} {form.lastname.data}",
                udob=form.birthday.data,
                uemail=form.email.data,
                uphone=form.phone.data,
                upassword=form.password.data,  # Store hashed password in production
                ugender=form.gender.data,
                ustate=form.state.data,
                ucity=form.city.data
            )

            # Add new user to the session
            mydb_obj.session.add(new_user)
            mydb_obj.session.commit()  # Commit to generate the user ID

            # Now add qualifications
            if form.qualifications.data:
                for qualification in form.qualifications.data:
                    new_qualification = Qualification(
                        qualification_type=qualification,
                        user_id=new_user.uid  # Ensure the user's ID exists
                    )
                    mydb_obj.session.add(new_qualification)

                mydb_obj.session.commit()  # Commit the changes

            flash('Account created successfully! Please Login again', 'success')
            return redirect(url_for('login'))  # Redirect to home after success

        except Exception as e:
            # Rollback the session if there's an error
            mydb_obj.session.rollback()
            flash('An error occurred. Please try again later.', 'error')

    return render_template('register.html', form=form)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Contacts model
class contacts(mydb_obj.Model):
    id = mydb_obj.Column(mydb_obj.Integer, primary_key=True)
    name = mydb_obj.Column(mydb_obj.String(100))
    email = mydb_obj.Column(mydb_obj.String(150))
    message = mydb_obj.Column(mydb_obj.String(500))

# ContactForm
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Your message', validators=[DataRequired()])
    submit = SubmitField('Send message')

# Contact route
@app.route('/contact', methods=['GET', 'POST'])

def contact():
    form = ContactForm()

    if form.validate_on_submit():
        # Handle the form submission
        con_name = form.name.data
        con_email = form.email.data
        con_message = form.message.data

        contact = contacts(name=con_name, email=con_email, message=con_message )
        mydb_obj.session.add(contact)
        mydb_obj.session.commit()       
        flash(f'Thank you, {con_name}. Your message has been sent!')
        return redirect(url_for('contact'))  # Redirect to the same page after submission
    return render_template('contactus.html', form=form)

@app.route('/admin_signin')
def admin_signin():
    return render_template('admin_signin.html')

@app.route('/user_signin')
def user_signin():
    return render_template('user_signin.html')

@app.route('/user-dash')
def user_dashboard():
    user = current_user  # Fetching the first user for now; later use user-specific queries

    # Retrieve qualifications for the user
    qualifications = user.qualifications  # This accesses the related qualifications for the user

    return render_template('user-dash.html', user=user, qualifications=qualifications)

@app.route('/update-profile', methods=['POST'])
def update_profile():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id) #to fetch current user
        if user:
            # Update the user details
            user.uname = request.form.get('name')
            user.uphone = request.form.get('phone')
            user.ustate = request.form.get('state')
            user.ucity = request.form.get('city')
            mydb_obj.session.commit()
            flash('Profile updated successfully!', 'success')
        else:
            flash('User not found.', 'error')
    else:
        flash('You need to be logged in to update your profile.', 'error')
    return redirect(url_for('user_dashboard'))

@app.route('/delete_profile', methods=['POST'])
@login_required
def delete_profile():
    user_id = current_user.uid  # Get the ID of the currently logged-in user
    
    # Fetch the user and related qualifications
    user = User.query.get(user_id)
    
    if user:
        # Delete related qualifications
        Qualification.query.filter_by(user_id=user_id).delete()
        
        # Delete the user
        mydb_obj.session.delete(user)
        mydb_obj.session.commit()
        
        # Log out the user
        logout_user()
        
        # Redirect to the homepage
        return redirect(url_for('home'))
    
    flash('User not found.', 'danger')
    return redirect(url_for('user_dashboard'))

app.route('/debug')
def debug():
    return render_template('debug.html')

if __name__ == "__main__":
    app.run(debug=True)


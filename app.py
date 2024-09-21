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
from datetime import datetime, timezone

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Ensure the session is non-permanent, so it expires when the browser closes
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_NAME'] = 'your_session_name'
app.config['SESSION_TYPE'] = 'filesystem'

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
    enquiries = mydb_obj.relationship('Enquiry', backref='user', lazy=True)
    
    # Override the get_id method to return the correct primary key
    def get_id(self):
        return str(self.uid)


class Qualification(mydb_obj.Model):
    __tablename__ = 'qualification'
    qid = mydb_obj.Column(mydb_obj.Integer, primary_key=True)
    qualification_type = mydb_obj.Column(mydb_obj.String(50), nullable=False)
    user_id = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('user.uid'), nullable=False)
    
class Course(mydb_obj.Model):
    __tablename__ = 'course'
    cid = mydb_obj.Column(mydb_obj.Integer, primary_key=True, autoincrement=True)
    cname = mydb_obj.Column(mydb_obj.String(100), nullable=False)  # Name of the course
    cdescription = mydb_obj.Column(mydb_obj.String(500), nullable=False)  # Detailed description
    cduration = mydb_obj.Column(mydb_obj.String(50), nullable=False)  # Duration format (e.g., "3 months", "1 year")
    cfees = mydb_obj.Column(mydb_obj.Integer, nullable=False)  # Course fees
    enquiries = mydb_obj.relationship('Enquiry', backref='course', lazy=True)

class EnquiryStatus(mydb_obj.Model):
    __tablename__ = 'enquiry_status'
    statusid = mydb_obj.Column(mydb_obj.Integer, primary_key=True, autoincrement=True)
    statusname = mydb_obj.Column(mydb_obj.String(50), nullable=False)  # Status name (e.g., "Pending", "Approved")
    enquiries = mydb_obj.relationship('Enquiry', backref='enquiry_status', lazy=True)

class Enquiry(mydb_obj.Model):
    __tablename__ = 'enquiry'
    eid = mydb_obj.Column(mydb_obj.Integer, primary_key=True, autoincrement=True)
    user_id = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('user.uid'), nullable=False)
    course_id = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('course.cid'), nullable=False)
    status_id = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('enquiry_status.statusid'), nullable=False)
    ehighestqualification = mydb_obj.Column(mydb_obj.String(100), nullable=False)  # Highest qualification
    emarks = mydb_obj.Column(mydb_obj.Float, nullable=False)  # Marks obtained
    egraduateyear = mydb_obj.Column(mydb_obj.Integer, nullable=False)  # Year of graduation
    esource = mydb_obj.Column(mydb_obj.String(100), nullable=False)  # Source of enquiry (e.g., "Website", "Referral")
    edate = mydb_obj.Column(mydb_obj.DateTime, default=datetime.now(timezone.utc), nullable=False)  # Automatically store the current date and time

# Contacts model
class contacts(mydb_obj.Model):
    __tablename__= 'contact'
    id = mydb_obj.Column(mydb_obj.Integer, primary_key=True)
    name = mydb_obj.Column(mydb_obj.String(100))
    email = mydb_obj.Column(mydb_obj.String(150))
    message = mydb_obj.Column(mydb_obj.String(500))

#WTForms
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

# ContactForm
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Your message', validators=[DataRequired()])
    submit = SubmitField('Send message')


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
            login_user(user, remember=False) #remember = False ensures that the session expires
            # session['user_id'] = user.uid
            flash(f'Welcome {user.uname}!', 'success')

            # Redirect to admin or user dashboard based on role
            if user.urole == 'admin':
                return redirect(url_for('latest_enquiries'))
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
    if current_user.is_authenticated:
        # Redirect to dashboard if the user is already logged in
        return redirect(url_for('user_dashboard'))
    # Render the home page if not authenticated
    return render_template('home.html')


@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/about')
def about():
    return render_template('about.html')

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
    return render_template('contact.html', form=form)

#Route for user dashboard
@app.route('/user-dash')
def user_dashboard():
    user = current_user  # Fetching the first user for now; later use user-specific queries
    
    # Retrieve qualifications for the user
    qualifications = user.qualifications  # This accesses the related qualifications for the user
    user_enquiries = (
        mydb_obj.session.query(Enquiry, Course, EnquiryStatus)
        .join(Course, Enquiry.course_id == Course.cid)
        .join(EnquiryStatus, Enquiry.status_id == EnquiryStatus.statusid)
        .filter(Enquiry.user_id == user.uid)
        .all()
    )
    enabled_courses = Course.query.all() #retrieve all courses from the course table
    return render_template('user-dash.html', user=user, qualifications=qualifications, enabled_courses=enabled_courses, user_enquiries=user_enquiries, enumerate=enumerate)

#User edit profile
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

#User delete profile
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

#Route for user add enquiry
@app.route('/add-enquiry', methods=['POST'])
@login_required  # Ensure only logged-in users can add an enquiry
def add_enquiry():
    # Get current user using Flask-Login
    uid = current_user.uid  # Retrieve the currently logged-in user's ID
    
    # Get form data from the POST request
    qualification = request.form['highestQualification']
    percentage_marks = request.form['percentageMarks']
    year_of_graduation = request.form['yearOfGraduation']
    cid = request.form['enquiredCourse']  # Get the course ID from the form
    source = request.form['source']
    enquiry_status_id = 1    # Set default enquiry status to 'Pending' (status ID == 1)

    # Create a new enquiry instance
    new_enquiry = Enquiry(
        user_id=uid,
        course_id=cid,
        ehighestqualification=qualification,
        emarks=percentage_marks,
        egraduateyear=year_of_graduation,
        esource=source,
        status_id=enquiry_status_id  # Set status to 'Pending'
    )

    # Add the new enquiry to the database
    mydb_obj.session.add(new_enquiry)
    mydb_obj.session.commit()

    # Flash success message and redirect to user dashboard
    flash('Enquiry added successfully!')
    return redirect(url_for('user_dashboard'))

#Route for delete enquiry
@app.route('/delete-enquiry/<int:enquiry_id>', methods=['POST'])
@login_required
def delete_enquiry(enquiry_id):
    enquiry = Enquiry.query.get_or_404(enquiry_id)
    
    # Ensure the current user is the owner of the enquiry
    if enquiry.user_id == current_user.uid:
        mydb_obj.session.delete(enquiry)
        mydb_obj.session.commit()
        flash('Enquiry deleted successfully!', 'success')
    else:
        flash('You are not authorized to delete this enquiry.', 'error')
    
    return redirect(url_for('user_dashboard'))


#Route for Admin dashboard
@app.route('/latest-enquiries')
def latest_enquiries():
    latest_enquiries = (
        mydb_obj.session.query(Enquiry)
        .join(User, Enquiry.user_id == User.uid)
        .join(Course, Enquiry.course_id == Course.cid)
        .filter(Enquiry.status_id == 1)  # Assuming 1 is for 'Pending'
        .order_by(Enquiry.edate.desc())
        .limit(5)
        .all()
    )
    return render_template('latest-enquiries.html', latest_enquiries=latest_enquiries)


#All Enquiries Admin
@app.route('/admin-all-enquiries', methods=['GET', 'POST'])
@login_required  # Ensure only admins have access to this route
def admin_all_enquiries():
    search = request.args.get('search', '')

    # Construct a query to join the User, Course, Enquiry, and Enquiry Status tables
    query = mydb_obj.session.query(
        Enquiry, User, Course, EnquiryStatus
    ).join(User, Enquiry.user_id == User.uid) \
     .join(Course, Enquiry.course_id == Course.cid) \
     .join(EnquiryStatus, Enquiry.status_id == EnquiryStatus.statusid) \
     .order_by(Enquiry.edate.desc())  # Order by newest to oldest enquiries
    
    # Apply search filter (if any)
    if search:
        search = f"%{search}%"  # SQL LIKE query pattern
        query = query.filter(
            mydb_obj.or_(User.uname.ilike(search), Course.cname.ilike(search))
        )
    
    # Execute the query and get all results
    enquiries = query.all()
    
    # Fetch all enquiry statuses for the status update dropdown
    enquiry_statuses = EnquiryStatus.query.all()

    return render_template(
        'admin-all-enquiries.html', 
        enquiries=enquiries,
        enquiry_statuses=enquiry_statuses
    )

#Route to update enquiry status (admin)
@app.route('/update-enquiry-status', methods=['POST'])
@login_required  # Ensure only admins have access
def update_enquiry_status():
    enquiry_id = request.form.get('enquiry_id')
    new_status_id = request.form.get('status_id')

    # Fetch the enquiry and update the status
    enquiry = Enquiry.query.get(enquiry_id)
    if enquiry:
        enquiry.status_id = new_status_id
        mydb_obj.session.commit()
        flash('Enquiry status updated successfully!', 'success')
    else:
        flash('Enquiry not found.', 'error')

    return redirect(url_for('admin_all_enquiries'))

# Route to display all users via admin
@app.route('/all_users', methods=['GET'])
def all_users():
    search_query = request.args.get('search', '')
    users = User.query.filter(
        (User.uname.like(f'%{search_query}%')) |
        (User.uemail.like(f'%{search_query}%')) |
        (User.uphone.like(f'%{search_query}%')),
        User.urole != 'admin'
    ).all()
    form = RegistrationForm()  # Create an instance of the form
    return render_template('admin-all-users.html', users=users, form=form)

# Route to add a new user via admin
@app.route('/add_user', methods=['POST'])
def add_user():
    form = RegistrationForm()  # Use the same RegistrationForm

    if form.validate_on_submit():
        # Check if the email already exists
        if User.query.filter_by(uemail=form.email.data).first():
            flash('Email address already exists. Please choose a different one.', 'danger')
            return redirect(url_for('all_users'))  # Redirect back to the user list

        try:
            # Create new user object
            new_user = User(
                uname=f"{form.firstname.data} {form.lastname.data}",
                udob=form.birthday.data,
                uemail=form.email.data,
                uphone=form.phone.data,
                upassword=form.password.data, 
                ugender=form.gender.data,
                ustate=form.state.data,
                ucity=form.city.data
            )

            # Add new user to the session
            mydb_obj.session.add(new_user)
            mydb_obj.session.commit()  # Commit to generate the user ID

            # Now add qualifications if any
            if form.qualifications.data:
                for qualification in form.qualifications.data:
                    new_qualification = Qualification(
                        qualification_type=qualification,
                        user_id=new_user.uid  # Ensure the user's ID exists
                    )
                    mydb_obj.session.add(new_qualification)

                mydb_obj.session.commit()  # Commit the changes

            flash('User added successfully!', 'success')
            return redirect(url_for('all_users'))  # Redirect back to the user list

        except Exception as e:
            # Rollback the session if there's an error
            mydb_obj.session.rollback()
            flash('An error occurred. Please try again later.', 'error')

    return render_template('admin-all-users.html', form=form)  # Render the users page again

# Route to handle editing a user via admin
@app.route('/update_user', methods=['POST'])
def update_user():
    uid = request.form.get('uid')
    uname = request.form.get('uname')
    uemail = request.form.get('uemail')
    uphone = request.form.get('uphone')
    ustate = request.form.get('ustate')
    ucity = request.form.get('ucity')

    # Retrieve the user from the database
    user = User.query.get(uid)

    if user:
        # Update user details
        user.uname = uname
        user.uemail = uemail
        user.uphone = uphone
        user.ustate = ustate
        user.ucity = ucity
        
        # Save changes to the database
        mydb_obj.session.commit()

        flash('User details updated successfully.')
    else:
        flash('User not found.')

    return redirect(url_for('all_users'))


# Route to handle deleting a user
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        # Delete associated qualifications
        qualifications = Qualification.query.filter_by(user_id=user.uid).all()
        for qualification in qualifications:
            mydb_obj.session.delete(qualification)

        # Now delete the user
        mydb_obj.session.delete(user)
        mydb_obj.session.commit()
        flash('User deleted successfully!', 'success')
    else:
        flash('User not found!', 'error')
    
    return redirect(url_for('all_users'))

#Route to All Courses page
@app.route('/all_courses', methods=['GET', 'POST'])
def all_courses():
    search_query = request.args.get('search', '')
    if search_query:
        courses = Course.query.filter(Course.cname.ilike(f'%{search_query}%')).all()
    else:
        courses = Course.query.all()

    return render_template('admin-all-courses.html', courses=courses)

#Route to add courses
@app.route('/add_course', methods=['POST'])
def add_course():
    if request.method == 'POST':
        cname = request.form['cname']
        cdescription = request.form['cdescription']
        cduration = request.form['cduration']
        cfees = request.form['cfees']

        new_course = Course(
            cname=cname,
            cdescription=cdescription,
            cduration=cduration,
            cfees=cfees
        )

        mydb_obj.session.add(new_course)
        mydb_obj.session.commit()

        flash('Course added successfully!', 'success')
        return redirect(url_for('all_courses'))  # Adjust the redirect as needed


#Route to update courses
@app.route('/update-course', methods=['POST'])
def update_course():
    course_id = request.form.get('cid')
    course = Course.query.get_or_404(course_id)

    # Get the updated details from the form
    course.coursename = request.form['cname']
    course.description = request.form['cdescription']
    course.duration = request.form['cduration']
    course.fee = request.form['cfees']

    # Save changes to the database
    try:
        mydb_obj.session.commit()
        flash('Course updated successfully!', 'success')
    except Exception as e:
        mydb_obj.session.rollback()
        flash(f'Error updating course: {str(e)}', 'error')

    return redirect(url_for('all_courses'))


@app.route('/delete-course/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if course:
        # Check if there are any enquiries for this course
        if course.enquiries:
            flash('Cannot delete course with existing enquiries.', 'danger')
        else:
            mydb_obj.session.delete(course)
            mydb_obj.session.commit()
            flash('Course deleted successfully!', 'success')
    else:
        flash('Course not found!', 'danger')
    return redirect(url_for('all_courses'))

@app.route('/disable_qualifications')
def disable_qualifications():
    # Your logic here
    return render_template('disable_qualifications.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Log the user out
    return redirect(url_for('home'))  # Redirect to homepage or login


if __name__ == '__main__':
    app.run(debug=True)
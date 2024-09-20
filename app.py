from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 
import urllib 
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from flask import redirect, url_for, flash
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some secret key'

#defining the url string with parameters for mssql db connection
params = 'DRIVER={ODBC Driver 17 for SQL Server};Server=DESKTOP-FSS96T0\\SQLEXPRESS;DATABASE=course_enquiry;Trusted_Connection=yes;'
connection_string = urllib.parse.quote_plus(params)
#add database uri configuration to app.config dictionary
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mydb_obj = SQLAlchemy(app) #create an SQLAlchemy object
migrate = Migrate(app, mydb_obj)

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Courses route
@app.route('/courses')
def courses():
    return render_template('courses.html')

# About route
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

# Register route
@app.route('/register')
def register():
    return render_template('register.html')

# Admin Sign In route
@app.route('/admin_signin')
def admin_signin():
    return render_template('admin_signin.html')

# User Sign In route
@app.route('/user_signin')
def user_signin():
    return render_template('user_signin.html')

# User Dashboard route
@app.route('/user-dash')
def user_dashboard():
    return render_template('user-dash.html')

@app.route('/debug')
def debug():
    return render_template('debug.html')

if __name__ == "__main__":
    app.run(debug=True)
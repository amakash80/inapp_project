from flask import Flask, render_template

app = Flask(__name__)

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

# Contact route
@app.route('/contact')
def contact():
    return render_template('contact.html')

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
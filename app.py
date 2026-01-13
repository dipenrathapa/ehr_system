"""
Electronic Health Record (EHR) System
Flask Application with MySQL Database

This application provides:
- Doctor registration and login with password hashing
- Patient CRUD operations
- Dashboard showing only logged-in doctor's patients
- Image upload for medical reports
"""

import os
import re
import secrets
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from config import Config

# Initialize Flask application
app = Flask(__name__)

# Load configuration
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['MYSQL_HOST'] = Config.MYSQL_HOST
app.config['MYSQL_USER'] = Config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = Config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = Config.MYSQL_DB
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH

# Initialize MySQL
mysql = MySQL(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# ==================== HELPER FUNCTIONS ====================

def allowed_file(filename):
    """Check if uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def login_required(f):
    """Decorator to protect routes that require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'doctor_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def is_strong_password(password):
    """
    Check if password is strong enough:
    - At least 8 characters
    - One uppercase letter
    - One lowercase letter
    - One number
    - One special character
    """
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password) and
        re.search(r"[!@#$%^&*()_+=\-]", password)
    )


# ==================== STATIC PAGES ====================

@app.route('/')
def home():
    """Home page - public access."""
    return render_template('home.html')


@app.route('/about')
def about():
    """About page - public access."""
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page - public access."""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO contact_inquiries (name, email, message) VALUES (%s, %s, %s)",
                (name, email, message)
            )
            mysql.connection.commit()
            cur.close()
            flash("Thank you! Your message has been submitted. We will get back to you if needed.", "success")
            return redirect(url_for('contact'))

        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
            return redirect(url_for('contact'))

    return render_template('contact.html')


# ==================== AUTHENTICATION ====================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Doctor registration with password hashing."""
    if request.method == 'POST':
        # Get form data
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        specialty = request.form.get('specialty', '')
        phone = request.form.get('phone', '')
        
        # Validate passwords match
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        
        # Validate password strength
        if not is_strong_password(password):
            flash(
                "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character.",
                "danger"
            )
            return redirect(url_for('register'))
        
        # Hash the password using Werkzeug's security module
        password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        
        try:
            # Insert new doctor into database
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO doctors (full_name, email, password_hash, specialty, phone)
                VALUES (%s, %s, %s, %s, %s)
            """, (full_name, email, password_hash, specialty, phone))
            mysql.connection.commit()
            cur.close()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            # Handle duplicate email error
            flash('Email already registered. Please use a different email.', 'danger')
            return redirect(url_for('register'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Doctor login with password verification."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Query doctor by email
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, full_name, password_hash FROM doctors WHERE email = %s", (email,))
        doctor = cur.fetchone()
        cur.close()
        
        # Verify password using Werkzeug's check_password_hash
        if doctor and check_password_hash(doctor[2], password):
            # Store doctor info in session
            session['doctor_id'] = doctor[0]
            session['doctor_name'] = doctor[1]
            flash(f'Welcome back, Dr. {doctor[1]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM doctors WHERE email = %s", (email,))
        doctor = cur.fetchone()

        if doctor:
            # Generate secure token
            token = secrets.token_urlsafe(32)

            # Save token in database
            cur.execute(
                "UPDATE doctors SET reset_token = %s WHERE email = %s",
                (token, email)
            )
            mysql.connection.commit()

            # Simulated email (display link)
            reset_link = url_for('reset_password', token=token, _external=True)

            flash(f'Password reset link (simulated email): {reset_link}', 'info')
        else:
            flash('Email not found.', 'danger')

        cur.close()
        return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')


# @app.route('/reset-password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     cur = mysql.connection.cursor()
#     cur.execute(
#         "SELECT id FROM doctors WHERE reset_token = %s",
#         (token,)
#     )
#     doctor = cur.fetchone()

#     if not doctor:
#         flash('Invalid or expired reset link.', 'danger')
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']

#         if password != confirm_password:
#             flash('Passwords do not match.', 'danger')
#             return redirect(request.url)

#         password_hash = generate_password_hash(
#             password, method='pbkdf2:sha256', salt_length=8
#         )

#         # Update password & clear token
#         cur.execute("""
#             UPDATE doctors 
#             SET password_hash = %s, reset_token = NULL
#             WHERE reset_token = %s
#         """, (password_hash, token))

#         mysql.connection.commit()
#         cur.close()

#         flash('Password reset successful. Please log in.', 'success')
#         return redirect(url_for('login'))

#     cur.close()
#     return render_template('reset_password.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT id FROM doctors WHERE reset_token = %s",
        (token,)
    )
    doctor = cur.fetchone()

    if not doctor:
        flash('Invalid or expired reset link.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(request.url)

        # Check password strength: at least 8 chars, uppercase, lowercase, number, special char
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(pattern, password):
            flash('Password must be at least 8 characters long and include uppercase, lowercase, number, and special character.', 'danger')
            return redirect(request.url)

        # Hash the password
        password_hash = generate_password_hash(
            password, method='pbkdf2:sha256', salt_length=8
        )

        # Update password & clear token
        cur.execute("""
            UPDATE doctors 
            SET password_hash = %s, reset_token = NULL
            WHERE reset_token = %s
        """, (password_hash, token))

        mysql.connection.commit()
        cur.close()

        flash('Password reset successful. Please log in.', 'success')
        return redirect(url_for('login'))

    cur.close()
    return render_template('reset_password.html')


@app.route('/logout')
def logout():
    """Clear session and logout."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


# ==================== DASHBOARD & PATIENT CRUD ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard showing only the logged-in doctor's patients."""
    doctor_id = session['doctor_id']
    
    # Fetch only patients belonging to this doctor
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, full_name, age, gender, phone, last_visit_date, diagnosis
        FROM patients 
        WHERE doctor_id = %s 
        ORDER BY created_at DESC
    """, (doctor_id,))
    patients = cur.fetchall()
    cur.close()
    
    return render_template('dashboard.html', patients=patients)


@app.route('/patient/add', methods=['GET', 'POST'])
@login_required
def add_patient():
    """Add a new patient EHR record."""
    if request.method == 'POST':
        doctor_id = session['doctor_id']
        
        # Handle image upload
        report_image = None
        if 'report_image' in request.files:
            file = request.files['report_image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename to avoid duplicates
                filename = f"{doctor_id}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                report_image = filename
        
        # Get checkbox values (returns None if unchecked)
        has_allergies = 1 if request.form.get('has_allergies') else 0
        has_diabetes = 1 if request.form.get('has_diabetes') else 0
        has_hypertension = 1 if request.form.get('has_hypertension') else 0
        has_heart_disease = 1 if request.form.get('has_heart_disease') else 0
        is_smoker = 1 if request.form.get('is_smoker') else 0
        
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO patients (
                    doctor_id, full_name, age, weight, height, blood_type,
                    phone, email, address, gender,
                    has_allergies, has_diabetes, has_hypertension, has_heart_disease, is_smoker,
                    date_of_birth, admission_date, last_visit_date,
                    medical_history, current_medications, diagnosis, treatment_notes,
                    report_image
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                doctor_id,
                request.form['full_name'],
                request.form.get('age') or None,
                request.form.get('weight') or None,
                request.form.get('height') or None,
                request.form.get('blood_type'),
                request.form.get('phone'),
                request.form.get('email'),
                request.form.get('address'),
                request.form['gender'],
                has_allergies, has_diabetes, has_hypertension, has_heart_disease, is_smoker,
                request.form.get('date_of_birth') or None,
                request.form.get('admission_date') or None,
                request.form.get('last_visit_date') or None,
                request.form.get('medical_history'),
                request.form.get('current_medications'),
                request.form.get('diagnosis'),
                request.form.get('treatment_notes'),
                report_image
            ))
            mysql.connection.commit()
            cur.close()
            
            flash('Patient record added successfully!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            flash(f'Error adding patient: {str(e)}', 'danger')
    
    return render_template('add_patient.html')


@app.route('/patient/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_patient(id):
    """Edit an existing patient EHR record."""
    doctor_id = session['doctor_id']
    
    # Verify patient belongs to this doctor
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patients WHERE id = %s AND doctor_id = %s", (id, doctor_id))
    patient = cur.fetchone()
    
    if not patient:
        flash('Patient not found or access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Handle image upload
        report_image = patient[23]  # Keep existing image by default
        if 'report_image' in request.files:
            file = request.files['report_image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{doctor_id}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                report_image = filename
        
        # Get checkbox values
        has_allergies = 1 if request.form.get('has_allergies') else 0
        has_diabetes = 1 if request.form.get('has_diabetes') else 0
        has_hypertension = 1 if request.form.get('has_hypertension') else 0
        has_heart_disease = 1 if request.form.get('has_heart_disease') else 0
        is_smoker = 1 if request.form.get('is_smoker') else 0
        
        try:
            cur.execute("""
                UPDATE patients SET
                    full_name = %s, age = %s, weight = %s, height = %s, blood_type = %s,
                    phone = %s, email = %s, address = %s, gender = %s,
                    has_allergies = %s, has_diabetes = %s, has_hypertension = %s,
                    has_heart_disease = %s, is_smoker = %s,
                    date_of_birth = %s, admission_date = %s, last_visit_date = %s,
                    medical_history = %s, current_medications = %s, diagnosis = %s,
                    treatment_notes = %s, report_image = %s
                WHERE id = %s AND doctor_id = %s
            """, (
                request.form['full_name'],
                request.form.get('age') or None,
                request.form.get('weight') or None,
                request.form.get('height') or None,
                request.form.get('blood_type'),
                request.form.get('phone'),
                request.form.get('email'),
                request.form.get('address'),
                request.form['gender'],
                has_allergies, has_diabetes, has_hypertension, has_heart_disease, is_smoker,
                request.form.get('date_of_birth') or None,
                request.form.get('admission_date') or None,
                request.form.get('last_visit_date') or None,
                request.form.get('medical_history'),
                request.form.get('current_medications'),
                request.form.get('diagnosis'),
                request.form.get('treatment_notes'),
                report_image,
                id, doctor_id
            ))
            mysql.connection.commit()
            cur.close()
            
            flash('Patient record updated successfully!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            flash(f'Error updating patient: {str(e)}', 'danger')
    
    cur.close()
    return render_template('edit_patient.html', patient=patient)


@app.route('/patient/delete/<int:id>', methods=['POST'])
@login_required
def delete_patient(id):
    """Delete a patient EHR record."""
    doctor_id = session['doctor_id']
    
    try:
        cur = mysql.connection.cursor()
        # Delete only if patient belongs to this doctor
        cur.execute("DELETE FROM patients WHERE id = %s AND doctor_id = %s", (id, doctor_id))
        mysql.connection.commit()
        cur.close()
        
        flash('Patient record deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting patient: {str(e)}', 'danger')
    
    return redirect(url_for('dashboard'))


@app.route('/patient/view/<int:id>')
@login_required
def view_patient(id):
    """View detailed patient record."""
    doctor_id = session['doctor_id']
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patients WHERE id = %s AND doctor_id = %s", (id, doctor_id))
    patient = cur.fetchone()
    cur.close()
    
    if not patient:
        flash('Patient not found or access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('view_patient.html', patient=patient)


# @app.route('/sus', methods=['GET', 'POST'])
# def sus():
#     questions = [
#         "I think that I would like to use this system frequently.",
#         "I found the system unnecessarily complex.",
#         "I thought the system was easy to use.",
#         "I think that I would need the support of a technical person to be able to use this system.",
#         "I found the various functions in this system were well integrated.",
#         "I thought there was too much inconsistency in this system.",
#         "I would imagine that most people would learn to use this system very quickly.",
#         "I found the system very cumbersome to use.",
#         "I felt very confident using the system.",
#         "I needed to learn a lot of things before I could get going with this system."
#     ]

#     if request.method == 'POST':
#         try:
#             # Collect answers as integers
#             answers = [int(request.form.get(f"q{i}", 0)) for i in range(1, 11)]

#             # Compute SUS score
#             sus_score = 0
#             for idx, ans in enumerate(answers):
#                 if (idx + 1) % 2 != 0:  # odd questions
#                     sus_score += ans - 1
#                 else:  # even questions
#                     sus_score += 5 - ans
#             sus_score *= 2.5  # final score out of 100

#             # Insert into database
#             cur = mysql.connection.cursor()
#             cur.execute("""
#                 INSERT INTO sus_responses 
#                 (doctor_id, q1,q2,q3,q4,q5,q6,q7,q8,q9,q10, sus_score) 
#                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#             """, (session.get('doctor_id'), *answers, sus_score))
#             mysql.connection.commit()
#             cur.close()

#             flash(f"Thank you! Your responses have been recorded. SUS Score: {sus_score}", "success")
#             return redirect(url_for('home'))

#         except Exception as e:
#             flash(f"Error: {e}", "danger")
#             return redirect(url_for('sus'))

#     return render_template('sus.html', questions=questions)

@app.route('/sus', methods=['GET', 'POST'])
def sus():
    questions = [
        "I think that I would like to use this system frequently.",
        "I found the system unnecessarily complex.",
        "I thought the system was easy to use.",
        "I think that I would need the support of a technical person to be able to use this system.",
        "I found the various functions in this system were well integrated.",
        "I thought there was too much inconsistency in this system.",
        "I would imagine that most people would learn to use this system very quickly.",
        "I found the system very cumbersome to use.",
        "I felt very confident using the system.",
        "I needed to learn a lot of things before I could get going with this system."
    ]

    if request.method == 'POST':
        doctor_id = session.get('doctor_id')
        if not doctor_id:
            flash("You must be logged in to submit SUS.", "danger")
            return redirect(url_for('login'))

        try:
            # Collect answers and validate
            answers = []
            for i in range(1, 11):
                ans = int(request.form.get(f"q{i}", 0))
                if ans < 1 or ans > 5:
                    flash("All answers must be between 1 and 5.", "danger")
                    return redirect(url_for('sus'))
                answers.append(ans)

            # Compute SUS score
            sus_score = sum((ans - 1) if (idx + 1) % 2 != 0 else (5 - ans) 
                            for idx, ans in enumerate(answers)) * 2.5

            # Insert into database
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO sus_responses 
                (doctor_id, q1,q2,q3,q4,q5,q6,q7,q8,q9,q10, sus_score) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (doctor_id, *answers, sus_score))
            mysql.connection.commit()
            cur.close()

            flash(f"Thank you! Your responses have been recorded. SUS Score: {sus_score}", "success")
            return redirect(url_for('home'))

        except Exception as e:
            flash(f"Error: {e}", "danger")
            return redirect(url_for('sus'))

    return render_template('sus.html', questions=questions)



# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    # Run in debug mode for development
    app.run(debug=True, port=5000)

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'ehr_system'

mysql = MySQL(app)

# Folder for uploaded images
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# -------------------------
# Add Patient
# -------------------------
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if 'doctor_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        gender = request.form['gender']
        allergies = request.form['allergies']
        medication = request.form['medication']
        lab_results = request.form['lab_results']
        
        # Image Upload
        image_file = request.files['image']
        filename = None
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO patients (doctor_id, first_name, last_name, dob, gender, allergies, medication, lab_results, image)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''', (session['doctor_id'], first_name, last_name, dob, gender, allergies, medication, lab_results, filename))
        mysql.connection.commit()
        cursor.close()
        flash('Patient added successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('patient_form.html')

# -------------------------
# Edit Patient
# -------------------------
@app.route('/edit_patient/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    if 'doctor_id' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM patients WHERE id=%s AND doctor_id=%s", (id, session['doctor_id']))
    patient = cursor.fetchone()

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        gender = request.form['gender']
        allergies = request.form['allergies']
        medication = request.form['medication']
        lab_results = request.form['lab_results']

        # Image Upload
        image_file = request.files['image']
        filename = patient['image']
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cursor.execute('''
            UPDATE patients
            SET first_name=%s, last_name=%s, dob=%s, gender=%s, allergies=%s, medication=%s, lab_results=%s, image=%s
            WHERE id=%s AND doctor_id=%s
        ''', (first_name, last_name, dob, gender, allergies, medication, lab_results, filename, id, session['doctor_id']))
        mysql.connection.commit()
        cursor.close()
        flash('Patient updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    cursor.close()
    return render_template('patient_form.html', patient=patient)

# -------------------------
# Delete Patient
# -------------------------
@app.route('/delete_patient/<int:id>', methods=['GET'])
def delete_patient(id):
    if 'doctor_id' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM patients WHERE id=%s AND doctor_id=%s", (id, session['doctor_id']))
    mysql.connection.commit()
    cursor.close()
    flash('Patient deleted successfully!', 'danger')
    return redirect(url_for('dashboard'))

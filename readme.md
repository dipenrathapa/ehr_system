# Electronic Health Record (EHR) System

A **Flask-based Electronic Health Record (EHR) system** with a MySQL database backend.  
This application allows doctors to manage patient records, upload medical reports, and evaluate system usability with a SUS questionnaire.

---

## Features

- Doctor registration and login with **secure password hashing**
- Password reset via **secure token**
- Patient **CRUD operations** (Create, Read, Update, Delete)
- Upload and store patient **medical reports/images**
- Dashboard showing only logged-in doctor's patients
- SUS (System Usability Scale) questionnaire for feedback
- Contact form for inquiries

---

## Technologies Used

- **Backend:** Python 3, Flask, Flask-MySQLdb, Werkzeug
- **Frontend:** HTML, CSS, Bootstrap 5, Jinja2 templates
- **Database:** MySQL
- **Deployment:** PythonAnywhere (online) or local machine
- **Security:** Password hashing, token-based reset

---

## Prerequisites

- Python 3.9+
- MySQL server (for local run)
- pip (Python package manager)
- virtualenv (optional but recommended)

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/ehr-flask-app.git
cd ehr-flask-app

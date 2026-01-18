# Electronic Health Record (EHR) Information System

This project is a web-based Electronic Health Record (EHR) Information System developed for the course  
**Information Systems in Health Care (WS 25/26)**.

The system is designed for doctors to securely manage patient records through a web interface. It allows doctors to register, log in, and perform basic patient data management tasks.

---

## Project Description

The EHR system supports the digital storage and management of patient information. It replaces paper-based records with a secure database-driven solution. Each doctor can access and manage only their own patients’ data.

The system includes functionality for managing patient demographics, medical history, diagnosis, medications, immunization information, billing details, and medical report uploads. A usability evaluation using the System Usability Scale (SUS) is also included.

---

## Demo
https://dipendrathapa.pythonanywhere.com/

**Note:** email verification in demo is stillmissing(Tried but because of version incompatability maybe in PythonAnywhere, unable to work around. But I have anothere solution that works fine) 

## Technologies Used

**Frontend**
- HTML5  
- CSS3  
- Bootstrap 5  

**Backend**
- Python  
- Flask (version 3.0.0)  
- Flask-Mail (version 0.9.1)

**Database**
- MySQL (version 8.0.44)

---

## Main Features

- Doctor registration and login  
- Secure authentication and password reset  
- Patient record management (Create, Read, Update, Delete)  
- Uploading medical reports (images and PDF files)  
- Date selection for clinical information  
- System Usability Scale (SUS) questionnaire  

---


---

## Running the Project Locally

1. Clone the repository:
```bash
git clone <repository-url>
cd ehr_system

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt

python app.py

http://127.0.0.1:5000




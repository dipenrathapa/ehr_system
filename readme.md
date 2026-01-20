# Electronic Health Record (EHR) Information System

This project is a web-based Electronic Health Record (EHR) Information System developed for the course  
**Information Systems in Health Care (WS 25/26)**.

The system is designed for doctors to securely manage patient records through a web interface. It allows doctors to register, log in, and perform basic patient data management tasks.

---


## Demo
https://dipendrathapa.pythonanywhere.com/

**Note:** This demo functions correctly for all core features except email confirmation and validation. To ensure the website remains fully usable, these features have been temporarily disabled as a workaround.

While email confirmation and validation work as expected in the local development environment, integrating them into the demo deployment caused stability issues on PythonAnywhere, where the system frequently breaks despite compatible versions. The application otherwise runs smoothly and reliably.


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




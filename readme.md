# 🏥 Electronic Health Record (EHR) Information System

A secure, web-based **Electronic Health Record (EHR)** system built for the  
**Information Systems in Health Care (WS 25/26)** course.  
The platform enables healthcare providers to manage patient and doctor data, authentication, and password recovery securely using modern web technologies.

---

## 🌐 Live Demo

🔗 **Production Deployment:**  
👉 [https://dipendrathapa.pythonanywhere.com/](https://dipendrathapa.pythonanywhere.com/)

> Hosted on **PythonAnywhere** using Flask and MySQL.

---

## 🧰 Tech Stack

### Frontend
- HTML5  
- CSS3  
- Bootstrap 5  

### Backend
- Python 3  
- Flask (Web Framework)

### Database
- MySQL (PythonAnywhere MySQL Service)

### Security & Utilities
- Flask sessions  
- Password hashing  
- Token-based password reset  
- Environment-based configuration  

---

## ⚙️ Key Features

- Doctor **authentication** (login/logout)  
- Secure **password reset via token**  
- **MySQL database** integration  
- **File uploads** (reports, documents)  
- **Responsive UI** powered by Bootstrap 5  
- Production-ready **Flask app deployment**

---

## 🗂 Project Structure


---

## 🚀 Run the Project Locally

Follow these steps to set up and run the project on your local machine.

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd ehr_system

python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows


pip install -r requirements.txt
python app.py
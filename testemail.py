from flask_mail import Mail, Message
from flask import Flask

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dipendatacentric@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'  # the App Password you generated
app.config['MAIL_DEFAULT_SENDER'] = 'dipendatacentric@gmail.com'

mail = Mail(app)

with app.app_context():
    try:
        msg = Message("Test Email", recipients=["dipendatacentric@gmail.com"])
        msg.body = "This is a test email from Flask."
        mail.send(msg)
        print("Email sent!")
    except Exception as e:
        print(f"Email failed: {e}")

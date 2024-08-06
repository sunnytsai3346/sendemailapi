from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

FROM_EMAIL = os.getenv("FROM_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

def send_contact_email(to_email, subject, html_content, from_email, password):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        # Connect to the Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        
        # Send the email
        server.sendmail(from_email, to_email, msg.as_string())
        
        # Close the connection
        server.quit()
        
        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {e}"

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    name = data.get('name')
    email = data.get('sender_email')
    message = data.get('message')
    
    if not all([name, email, message]):
        return jsonify({'error': 'Missing required fields'}), 400

    subject = f"""
    {email} - {name}"""
    
    html_content = f"""
    <h2>New Contact Request</h2>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Message:</strong> {message}</p>
    """
    
    result = send_contact_email(TO_EMAIL, subject, html_content, FROM_EMAIL, APP_PASSWORD)
    return jsonify({'message': result})

if __name__ == '__main__':
    app.run(debug=True)
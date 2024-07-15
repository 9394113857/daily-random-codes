import os
from email.message import EmailMessage
import ssl
import smtplib
import sys
from datetime import datetime

credentials = [
    {'email_sender': 'commaccn@gmail.com', 'email_password': 'raghunadh'},
    {'email_sender': 'commaccn100@gmail.com', 'email_password': 'raghunadh'}
]

email_receiver = 'raghunadh28@gmail.com'
subject = "Test Mail"
body = "Test Body"

for cred in credentials:
    email_sender = cred['email_sender']
    email_password = cred['email_password']

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        print(f"Email sent successfully from {email_sender} to {email_receiver}!")
    except Exception as e:
        print(f"An error occurred while sending email from {email_sender} to {email_receiver}: {e}")
        sys.exit(1)

print("All emails sent successfully to", email_receiver)

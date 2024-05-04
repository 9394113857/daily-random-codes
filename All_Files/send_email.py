import os
from email.message import EmailMessage
import ssl
import smtplib
import sys
from datetime import datetime

# email_sender = "colabcode3@gmail.com"
# email_password = "dlhj byen lcqf pyux"

email_sender = 'practicesession3@gmail.com'
email_password = 'gpap kwxz sujc qxie'
email_recceiver = 'colabcode3@gmail.com'

subject = "Check out my new video"

# Update the body with current date and time
current_datetime = datetime.now().strftime("%d %B %Y %I:%M:%S %p")
formatted_datetime = datetime.now().strftime("%d %B %Y %I:%M:%S %p")
body = f"""
I've just published a new video on YouTube:
https://youtu.be/2cZzP9DLlkg

Published on: {current_datetime}
"""

# () this is parenthesis
em = EmailMessage() # em is the object and find some elements of the email to send mail
em['From'] = email_sender # '' these are the open single quotes
em['To'] = email_recceiver
em['Subject'] = subject # we were writing the body of the email after this line
em.set_content(body)

# with above, we have elements of the email body.
# In order to add a layer of security:-
# This is the standard technology for keeping the internet connection secured
# and safeguarding any sensitive data that has been sent between two systems
context = ssl.create_default_context()

# we have to find server port and the context:-
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_recceiver, em.as_string()) # Here em object with all email elements and giving proper format with as_string()

    print("Email sent successfully!")
    print(formatted_datetime)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)  # Exit with an error code

# Exit with a success code
sys.exit(0)
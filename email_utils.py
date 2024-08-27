import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from_email = "seaklav168@gmail.com"
password = os.getenv('EMAIL_PASSWORD')

def send_email_with_attachments(subject, body, attachments, to_email=None):
    if to_email is None:
        to_email = ["hratana261@gmail.com", "khengdalish21@gmail.com", "chlakhna702@gmail.com"]

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_email)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    for attachment in attachments:
        try:
            with open(attachment, "rb") as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
                msg.attach(part)
        except Exception as e:
            st.error(f"Failed to attach file {attachment}: {e}")

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        st.success(f"Email sent to {', '.join(to_email)}")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

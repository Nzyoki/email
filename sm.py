import os
import subprocess
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from skpy import Skype
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

def capture_screenshot(url, filename):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    driver.set_window_size(1800, 3400)
    driver.get(AMAZON_URL)
    driver.save_screenshot("amazon-screenshot.png")
    driver.quit()
def send_screenshot_to_skype(username, password, chat_id,filename):
    try:
        sk = Skype(username, password)
        chat = sk.chats[chat_id]
        chat.sendFile(open("amazon-screenshot.png", "rb"), os.path.basename("amazon-screenshot.png"), image=True)
        print("Screenshot sent to Skype successfully.")
    except Exception as e:
        print(f"Error sending screenshot to Skype: {e}")

def send_email(from_email, email_password, receiver_email, subject, body, attachment):
    

     msg=EmailMessage()
     msg.set_content(body)
     msg["subject"]=subject
     msg["From"]=from_email
     msg["To"]=receiver_email

     with open ("amazon-screenshot.png","rb") as fp:
         img_data=fp.read()
         msg.add_attachment(img_data,maintype='image',subtype='png',filename="amazon-screenshot.png")
     try:
        with smtplib.SMTP('smtp.gmail.com',587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(from_email,email_password)
            smtp.send_message(msg)
            print("email sent")

     except Exception as e:
      print(f"error sending email:{e}")
     
if __name__ == "__main__":
    SKYPE_CHAT_ID = os.getenv("SKYPE_CHAT_ID")
    SKYPE_USERNAME = os.getenv("SKYPE_USERNAME")
    SKYPE_PASSWORD = os.getenv("SKYPE_PASSWORD")
    AMAZON_URL = os.getenv("AMAZON_URL")
    SKYPE_SEND_INTERVAL = int(os.getenv("SKYPE_SEND_INTERVAL", 5)) 
    FROM_EMAIL = os.getenv("FROM_EMAIL")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

    try:
        print("Logging into Skype...")
        sk = Skype(SKYPE_USERNAME, SKYPE_PASSWORD)
        print("Skype login successful.")
    except Exception as e:
        print(f"Error logging into Skype: {e}")
        exit()

    while True:
        print("Capturing Amazon screenshot...")
        capture_screenshot(AMAZON_URL, "amazon-screenshot.png")

        print(f"Sending screenshot to Skype every {SKYPE_SEND_INTERVAL} seconds...")
        send_screenshot_to_skype(SKYPE_USERNAME, SKYPE_PASSWORD, SKYPE_CHAT_ID, "amazon-screenshot.png")

        print("Sending email with screenshot...")
        send_email(FROM_EMAIL, EMAIL_PASSWORD, RECEIVER_EMAIL, "Amazon Screenshot", "Please find the screenshot attached.", "amazon-screenshot.png")

        print("Waiting for next capture...")
        time.sleep(SKYPE_SEND_INTERVAL)

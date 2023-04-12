# source: https://stackoverflow.com/questions/13070038/attachment-image-to-send-by-mail-using-python
# https://stackoverflow.com/questions/64505/sending-mail-from-python-using-smtp
import imghdr
import os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def sendEmail(capturedFrame):
    message = MIMEMultipart()
    message["from"] = "Me"
    message["to"] = "email"
    message['subject'] = "Automatic Alarm System"
    message.attach(MIMEText("movement detected"))

    with open(capturedFrame, 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name
        # print(file_type)

    image = MIMEImage(file_data, name=os.path.basename(file_name))
    message.attach(image)

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login("Gmail", "password")
        smtp.send_message(message)
        print("email sent...")
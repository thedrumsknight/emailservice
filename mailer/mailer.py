#!/usr/bin/python3
import os
import sys
import codecs

from smtplib import SMTP

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from string import Template

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

def read_txt_template(filename):
    print('Reading txt file...')
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    print('Reading txt file... Success.')
    return Template(template_file_content)

def build_plain_message(path, recipient_email, sub, mesg):
    print('Building plain message...')
    # path is supposed to be relative to cwd
    MESSAGE='This is a default message.'
    if mesg != None:
        MESSAGE = mesg
    message_template = read_txt_template(os.path.join(os.getcwd(), path))
    message = message_template.substitute(MACHINE=os.getenv('MACHINE_NAME'), MESSAGE=MESSAGE)
    msg = MIMEMultipart('alternative')
    msg['From'] = os.getenv('SENDER_EMAIL')
    msg['To'] = recipient_email
    if sub != None:
        msg['Subject'] = sub
    else:
        msg['Subject'] = 'A message from the Pi'
    msg.attach(MIMEText(message, 'plain'))
    print('Building plain message... Success.')
    return msg

def build_html_message(path, recipient_email):
    print('Building HTML message...')
    EMAIL_SUBJECT = 'A message from the Pi'
    MACHINE_NAME = os.getenv('MACHINE_NAME')
    # path is supposed to be relative to cwd
    message_template = codecs.open(os.path.join(os.getcwd(), path), 'r').read()
    message = message_template.format(EMAIL_SUBJECT=EMAIL_SUBJECT, MACHINE=MACHINE_NAME)
    msg = MIMEMultipart('alternative')
    msg['From'] = os.getenv('SENDER_EMAIL')
    msg['To'] = recipient_email
    msg['Subject'] = EMAIL_SUBJECT
    msg.attach(MIMEText(message, 'html'))
    print('Building HTML message... Success.')
    return msg

def send_mail(msg):
    # Load .env vars
    SMTP_HOST = os.getenv('SMTP_HOST')
    SMTP_PORT = os.getenv('SMTP_PORT')
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    SENDER_EMAIL_PASSWORD = os.getenv('SENDER_EMAIL_PASSWORD')
    # Set SMTP server
    print('Setting up SMTP connection... host: ' + SMTP_HOST)
    server = SMTP(host=SMTP_HOST, port=SMTP_PORT)
    # Start TLS handshake
    server.starttls()
    # Login to SMTP host
    print('Logging in to account: ' + SENDER_EMAIL + '...')
    server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
    # Send message
    print('Sending message...')
    server.send_message(msg)
    print('Closing server connection...')
    # Close connection to host
    server.quit()
    print('Completed. Mail sent successfully.')

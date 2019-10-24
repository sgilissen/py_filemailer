"""
This Python script mails the file specified

NOTE: While the mails get sent over a secure layer, passwords are saved as plain JSON on the server!
      Please use a RANDOM and STRONG password, and use a generic email adress for the specific
      purpose of using this script. DO NOT use personal mailboxes!
"""

# --------------------------------------------
# IMPORTS AND LIBRARIES
# --------------------------------------------
import smtplib
import ssl
import json
import io
import os
import argparse
import getpass
import datetime

from email import encoders
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from os.path import basename
from email.mime.text import MIMEText

# --------------------------------------------
# VARIABLES
# --------------------------------------------

configfile = 'config.json'
port = 465

parser = argparse.ArgumentParser()
parser.add_argument("file", help="Filename to attach")
parser.add_argument("recipient", help="The recipient")
args = parser.parse_args()

now = datetime.datetime.now()


def config_check():
    if os.path.isfile(configfile) and os.access(configfile, os.R_OK):
        # checks if file exists
        print("[{0}] File exists and is readable".format(now))
        with open(configfile, 'r') as f:
            config = json.load(f)

        username = config['user']
        password = config['pass']
        from_email = config['from_email']
        subject_prefix = config['subject_prefix']
        server = config['server']
        msgbody = config['body']

        send_mail(username, password, from_email, args.recipient,
                  subject_prefix + " " + args.file, args.file, server, msgbody)

    else:
        print("[{0}] Either file is missing or is not readable, creating file...".format(now))
        server = input("Please provide the mailserver: ")
        username = input("Please provide your username: ")
        password = getpass.getpass("Please provide your password: ")
        from_email = input("From email: ")
        subject_prefix = input("Subject prefix: ")
        msgbody = input("Email body: ")

        with io.open(configfile, 'w') as db_file:
            db_file.write(json.dumps({'user': username, 'pass': password,
                                      'from_email': from_email, 'subject_prefix': subject_prefix,
                                      'server': server, 'msgbody': msgbody}))

        send_mail(username, password, from_email, args.recipient,
                  subject_prefix + " " + args.file, args.file, server, msgbody)


def send_mail(user, password, from_email, to_email, subject, attachment, server, msgbody):
    print("[{0}] Sending email to {1}...".format(now, to_email))
    print("[{0}] Attachment: {1}".format(now, attachment))

    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message["Bcc"] = from_email  # Recommended for mass emails

    with open(attachment, "rb") as file:
        # Add file as application/octet-stream
        # Email clients can usually download this automatically as attachment
        bodytxt = MIMEText(msgbody, 'plain')

        part = MIMEApplication(
            file.read(),
            name=basename(attachment)
        )

        # Encode file in ASCII characters to send by e-mail
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= %s" % basename(attachment),
        )

        # Add body of the text
        message.attach(bodytxt)
        # Add attachment to message and convert message to string
        message.attach(part)
        body = message.as_string()

        # Log in to the server using secure context and proceed to send e-mail
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(server, port, context=context) as mailserver:
            mailserver.login(user, password)
            mailserver.sendmail(from_email, to_email, body)


config_check()

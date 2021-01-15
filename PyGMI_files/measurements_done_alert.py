import smtplib
import time
import os

from zipfile import ZipFile

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

DEFAULT_MSG="Hi,\nOfficial time on the computer is "+time.ctime(time.time())+" \nPyGMI"

class Email_alert():
    def __init__(self,address="" ,message="",subject="",smtpadd="",login="",mdp="",smtpport=465):
        ### Create a text/plain message
        if message == "":
            msg = MIMEText(DEFAULT_MSG)
        else:
            msg = MIMEText(message)
        me = login #the sender's email address
        you = address #the recipient's email address
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = you
        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s = smtplib.SMTP_SSL(host=smtpadd,port=smtpport)
        #s.starttls()
        s.login(login, mdp)
        s.sendmail(me, [you], msg.as_string())
        s.quit()

class Email_one_file():
    def __init__(self,one_file='.',address="" ,message="",subject="",smtpadd="",login="",mdp="",smtpport=465):
        # Create the enclosing (outer) message
        me = login #the sender's email address
        you = address #the recipient's email address
        outer = MIMEMultipart()
        outer['Subject'] = subject
        outer['To'] = you
        outer['From'] = me

        ### Add a text/plain message
        if message == "":
            msg = MIMEText(DEFAULT_MSG)
        else:
            msg = MIMEText(message)
        outer.attach(msg)
        ### Add the directory as a zip file
        #zip the directory
        with ZipFile('data.zip', 'w') as myzip:
            #add the file at 'one_file' to the zip archive, and give it the name 'filename'
            #otherwise the full path structure is also included in the zip file
            myzip.write(one_file,arcname=os.path.basename(one_file))
        zipped_data='data.zip'
        # use a generic bag-of-bits type.
        ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        fp = open(zipped_data, 'rb')
        msg = MIMEBase(maintype, subtype)
        msg.set_payload(fp.read())
        fp.close()
        # Encode the payload using Base64
        encoders.encode_base64(msg)
        # Set the filename parameter
        msg.add_header('Content-Disposition', 'attachment', filename=zipped_data)
        outer.attach(msg)
        # Now send the message
        s = smtplib.SMTP_SSL(host=smtpadd,port=smtpport)
        #s.starttls()
        s.login(login, mdp)
        s.sendmail(me, [you], outer.as_string())
        s.quit()


class Email_directory():
    def __init__(self,directory='.',address="" ,message="",subject="",smtpadd="",login="",mdp="",smtpport=465):
        # Create the enclosing (outer) message
        me = login #the sender's email address
        you = address #the recipient's email address
        outer = MIMEMultipart()
        outer['Subject'] = subject
        outer['To'] = you
        outer['From'] = me

        ### Add a text/plain message
        if message == "":
            msg = MIMEText(DEFAULT_MSG)
        else:
            msg = MIMEText(message)
        outer.attach(msg)
        ### Add the directory as a zip file
        #zip the directory
        with ZipFile('data.zip', 'w') as myzip:
            for filename in os.listdir(directory):
                path = os.path.join(directory, filename)
                if not os.path.isfile(path):
                    continue
                #add the file at 'path' to the zip archive, and give it the name 'filename'
                #otherwise the full path structure is also included in the zip file
                myzip.write(filename=path,arcname=filename)
        zipped_data='data.zip'
        # use a generic bag-of-bits type.
        ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        fp = open(zipped_data, 'rb')
        msg = MIMEBase(maintype, subtype)
        msg.set_payload(fp.read())
        fp.close()
        # Encode the payload using Base64
        encoders.encode_base64(msg)
        # Set the filename parameter
        msg.add_header('Content-Disposition', 'attachment', filename=zipped_data)
        outer.attach(msg)

        # Now send the message
        s = smtplib.SMTP_SSL(host=smtpadd,port=smtpport)
        #s.starttls()
        s.login(login, mdp)
        s.sendmail(me, [you], outer.as_string())
        s.quit()


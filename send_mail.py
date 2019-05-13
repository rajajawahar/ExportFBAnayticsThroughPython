import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders


def send_mail(fromaddress, toaddress, subject, text, files):

    # instance of MIMEMultipart
    msg = MIMEMultipart()
    # storing the senders email address
    msg['From'] = fromaddress
    # storing the receivers email address
    msg['To'] = toaddress
    # storing the date
    msg['Date'] = formatdate(localtime=True)
    # storing the subject
    msg['Subject'] = subject
    # attach the body with the msg instance
    msg.attach(MIMEText(text))

    # open the file to be sent
    filename = "User Activity.xlsx"
    attachment = open(files, "rb")

    # instance of MIMEBase and named as part
    part = MIMEBase('application', "octet-stream")
    # To change the payload into encoded form
    part.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(part)

    part.add_header('Content-Disposition',
                    "attachment; filename= %s" % filename)

    msg.attach(part)

    # creates SMTP session
    smtp_session = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    smtp_session.starttls()

    # Authentication
    smtp_session.login(fromaddress, "*****")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    smtp_session.sendmail(fromaddress, toaddress, text)

    # terminating the session
    smtp_session.quit()

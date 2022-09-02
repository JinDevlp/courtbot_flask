from email import message
import smtplib
from email.mime.text import MIMEText


def send_mail(case_number, year_filed, county, phone_number, additional_phone_number, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '###'
    password = '###'
    message = f"< h3 > New Case Submitted < /h3 ><ul ><li > case_number: {case_number} </li><li > year_filed: {year_filed} </li><li > county: {county} </li><li > phone_number: {phone_number} </li><li > additional_phone_number: {additional_phone_number} </li><li > comments: {comments} </li></ul>"

    sender_email = '###'
    receiver_email = '###'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'New Case Submission'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

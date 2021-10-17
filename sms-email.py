import smtplib
from email.message import EmailMessage

def email_alert(subject, body, to):

    user     = "MIUSER"
    password = "MIPASS"

    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to']      = to
    msg['from']    = user

    server = smtplib.SMTP("box.123mail.es", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()

if __name__ == '__main__':
    email_alert("Asunto", "Cuerpo del mensaje", "info@informaticabyte.es")
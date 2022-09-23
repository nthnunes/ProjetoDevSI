import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pymongo import MongoClient

def sendEmail(email, token):
    subject = "Redefinição de senha"
    message = ("Para redefinir sua senha acesse: https://nthnunes.github.io/ProjetoDevSI/resetpassword e informe o TOKEN: " +
                token + "\n\nAtenção! Não responda esse email.")

    MY_ADDRESS = "devsiproject@airmail.cc"
    PASSWORD = ""

    mail = smtplib.SMTP(host='mail.cock.li', port="587")
    mail.starttls()
    mail.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()

    msg['From'] = MY_ADDRESS
    msg['To'] = email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))
    mail.send_message(msg)
        
    del msg


def dbConnection(username, password):
    CONNECTION_STRING = "mongodb+srv://" + username + ":" + password + "@cluster0.bbxnito.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)

    return client.get_database('devsi')
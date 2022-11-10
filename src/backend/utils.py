import smtplib
import email.message
from pymongo import MongoClient

def sendEmail(toMail, token):
    mail = ("Para redefinir sua senha acesse: https://nthnunes.github.io/ProjetoDevSI/src/frontend/pages/resetpassword.html e informe o TOKEN: " +
                token)

    msg = email.message.Message()
    msg['Subject'] = "Redefinição de senha - Não responda!"
    msg['From'] = "devsiproject@gmail.com"
    msg['To'] = toMail
    password = ""
    msg.add_header('Content-type', 'text/html')
    msg.set_payload(mail)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))


def dbConnection(username, password):
    CONNECTION_STRING = "mongodb+srv://" + username + ":" + password + "@cluster0.bbxnito.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)

    return client.get_database('devsi')


def dayDiff(year, month):
    if month == 2:
        if (year % 4) == 0:
            return 29
        else:
            return 28
    
    if (year % 2) == 0:
        diff = 31
        diff2 = 30
    else:
        diff = 30
        diff2 = 31

    if (month % 2) == 0:
        return diff
    else:
        return diff2
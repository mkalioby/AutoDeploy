#! /usr/bin/python
__author__ = 'mohamed'
import os
def send(to,subject,body,fromUser=None,cc="",bcc="",):
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoDeploy.settings")
    django.setup()

    from django.conf import settings
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    From=fromUser
    if fromUser==None:
        From="%s<%s>"%(settings.SMTP["FROM"],settings.SMTP["USERNAME"])
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = From
        #msg['To'] = to one email
        msg['Cc']= cc
        if type(to)==type([]):
            msg['To'] = ', '.join( to) #More than one email
        else:
            msg['To'] = to
        html = body
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        server = smtplib.SMTP(settings.SMTP["HOST"],settings.SMTP["PORT"])
        server.ehlo()
        server.starttls()
        server.login(settings.SMTP["USERNAME"], settings.SMTP["PASSWORD"])
        for t in to.split(";"):
            server.sendmail(From, t, msg.as_string())
        if cc!="":
            server.sendmail(From, cc, msg.as_string())
        if bcc!="":
            server.sendmail(From, bcc, msg.as_string())
        server.quit()
        return True

    except Exception as exp:
        return False


def getToken():
    from django.utils.crypto import get_random_string
    return get_random_string(length=32)
    return get_random_string(length=32)

if __name__=="__main__":
	send("mkalioby@mkalioby.com;mkalioby@gmail.com","Test","This is a test message")

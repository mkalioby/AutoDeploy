__author__ = 'mohamed'

def send(to,subject,body,fromUser=None,cc="",bcc="",):
    from django.conf import settings
    from django.core.mail import EmailMessage
    From = "%s<%s>" % (fromUser, settings.EMAIL_HOST_USER)
    if fromUser == None:
        From = "%s<%s>" % (settings.EMAIL_FROM, settings.EMAIL_HOST_USER)
    #     From = "%s <%s>" % (settings.EMAIL_FROM, settings.EMAIL_HOST_USER)
    # elif "@" in fromUser:
    #     From = fromUser
    # else:
    #     From = "%s <%s>" % (fromUser, settings.EMAIL_HOST_USER)
    if type(to) != type([]):
        to = [to]
    email = EmailMessage(
        subject,
        body,
        From,
        to, cc=cc, bcc=bcc)
    email.content_subtype = "html"
    return email.send(True)
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage
# Create your views here.
def mail(request):
    try:
        message= BaseEmailMessage(template_name="emails\hello.html", context={"nama":"Dede"})
        message.send(["template@yahoo.com"])
        # message= EmailMessage('File', 'Message', 'file@domain.com', ['filereceiver@domain.com'])
        # message.attach_file('playground/static/images/checkmatelogo.svg')
        # message.send()
        # send_mail('Test', 'message', 'd@gmail.com', ['receiver@domain.com'])
    except BadHeaderError:
        pass

    return HttpResponse("ok")
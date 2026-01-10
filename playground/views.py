from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers
# Create your views here.

def say_hello(request):
    notify_customers.delay('Hello')
    return render(request, 'hello.html', {'name' : 'dede'})

# def say_hello(request):
#     try: 
#         # send_mail('subject', 'message', 'dede@gmail.com', ['aul@gmail.com', 'apik@nahda.com', 'apang@haidar.com'])
        
#         # mail_admins('mail admins', 'lorem', html_message='<b>lorem ipsum dolor sit<b/>')

#         # message= EmailMessage('mail with file', 'lorem ipsum dolorsit amet', 'dede@gmail.com',  ['aul@gmail.com', 'apik@nahda.com', 'apang@haidar.com'])
#         # message.attach_file('playground/static/playground/Doraemon on a Camping Trip Coloring Page.jfif')
#         # message.send()

#         message = BaseEmailMessage(
#             template_name='emails/hello.email', 
#             context={
#                 'name' : 'Dede'
#             }
#         )
#         message.send(['dede@penerima.com'])
#     except BadHeaderError: 
#         pass 
#     return render(request, 'hello.html', {'name' : 'dede'})
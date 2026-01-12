from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers
from django.core.cache import cache
import requests
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
# Create your views here.

class HelloView(APIView):
    @method_decorator(cache_page(5*60))
    def get(self,request):
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        return render(request, 'hello.html', {'name' : data }) 


# @cache_page(5*60)
# def say_hello(request):
#     response = requests.get('https://httpbin.org/delay/2')
#     data = response.json()
#     return render(request, 'hello.html', {'name' : data }) 

# def say_hello(request):
#     notify_customers.delay('Hello')
#     return render(request, 'hello.html', {'name' : 'dede'})

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
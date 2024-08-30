from django.core.mail import send_mail
from django.conf import settings



def send_message_toemail(email,token,username):
    settings.EMAIL_HOST_USER=username
    subject = 'your password change like'
    message=  f'hi ,click the link to reset your password  http://127.0.0.1:8000/changepassword/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)
    return True
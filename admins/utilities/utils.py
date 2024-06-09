from django.core.mail import send_mail
from django.conf import settings


def send_teacher_email(user_instance, username, pen_no):
    subject = "Welcome to our site"
    message = f"Welcome {user_instance.username},\n\nYour account has been created successfully on our site.\n\nUsername: {username}\nPassword: {pen_no}"
    from_email = settings.EMAIL_HOST_USER
    to_email = [user_instance.email]
    send_mail(subject, message, from_email, to_email)

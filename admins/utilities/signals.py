from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from teacher.models import User
from django.conf import settings
from django.contrib.auth.hashers import make_password
from teacher.models import Teacher
import random
import string
import logging



logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def send_new_user_email(sender, instance, created, **kwargs):
    if created and instance.role.name == 'teacher':
        try:
            password = ''.join(random.choices( string.digits, k=6)) 
            subject = 'Welcome to our site'
            message = f"Welcome {instance.name},\n\nYour account has been created successfully on our site.\n\nUsername: {instance.username}\nPassword: {password}"
            from_email = settings.EMAIL_HOST_USER
            print(from_email)
            to_email = [instance.email]
            send_mail(subject, message, from_email, to_email)
            
            hashed_password = make_password(password)
            instance.set_password(hashed_password)
            instance.save()  
            
            # Teacher.objects.create(user=instance)
        except Exception as e:
              logger.exception("An error occurred while sending new user email:")
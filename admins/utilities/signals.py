# from django.core.mail import send_mail
# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from admins.models import User
# from django.conf import settings


# @receiver(post_save, sender=User)
# def send_new_user_email(sender, instance, created, **kwargs):
#     if created and instance.role.name == 'teacher':
#         subject = 'Welcome to our site'
#         message =  f"{'username': instance.username}"
#         from_email = settings.EMAIL_HOST_USER
#         to_email = [instance.email]
#         print(to_email)
#         send_mail(subject, message, from_email, to_email)

from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from admins.models import User
from django.conf import settings


@receiver(post_save, sender=User)
def send_new_user_email(sender, instance, created, **kwargs):
    print("****************************************************")
    if created and instance.role.name == 'teacher':
        try:
            print(instance.username,'333333')
            print(instance,'55555555555555')
            subject = 'Welcome to our site'
            message = f"Welcome {instance.username},\n\nYour account has been created successfully on our site."
            from_email = settings.EMAIL_HOST_USER
            print(from_email)
            to_email = [instance.email]
            print(to_email)
            send_mail(subject, message, from_email, to_email)
        except Exception as e:
            print(e)
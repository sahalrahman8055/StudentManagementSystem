from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from teacher.models import Teacher
from django.conf import settings


@receiver(post_save, sender=Teacher)
def send_teacher(sender, instance, created, **kwargs):
    if created:
        try:
            instance.user.set_password(instance.pen_no)
            instance.user.save()

            subject = "Your Teacher Account Credentials"
            message = f"Username: {instance.user.username}\nPassword: {instance.pen_no}"
            from_email = settings.EMAIL_HOST_USER
            to_email = instance.user.email
            send_mail(subject, message, from_email, [to_email])
        except Exception as e:
            print(f"An error occurred while sending email: {str(e)}")

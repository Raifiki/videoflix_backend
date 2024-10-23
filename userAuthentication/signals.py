

import secrets
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from userAuthentication.models import CustomUser
from rest_framework.authtoken.models import Token

from videoflix.settings import BACKEND_BASE_URL, EMAIL_HOST_USER

""" Signal that is called when a user is created --> A verification email is sent to the user"""
@receiver(post_save, sender=CustomUser)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        mail = instance.email
        from_mail = EMAIL_HOST_USER
        token = default_token_generator.make_token(instance)
        subject = 'Verify your email'
        context = {
            'username': mail.split('@')[0],
            'verification_url': BACKEND_BASE_URL + '/user/verify/?user_id=' + str(instance.pk) + '&token=' + token
        }
        text_content = 'Please verify your email'
        html_content = render_to_string('verification_email.html', context)
        send_mail(subject, text_content, from_mail, [mail], html_message=html_content)

""" Signal that is called when a user is created --> A token is generated for the user"""
@receiver(post_save, sender=CustomUser)
def gen_auth_token_for_user(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
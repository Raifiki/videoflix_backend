

import secrets
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from userAuthentication.models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        mail = 'leonard_weiss@web.de'# ToDo: change email to: instance.email
        from_mail = 'django@demomailtrap.com' # ToDo: change email to domain email
        token = default_token_generator.make_token(instance)
        print(token)
        print(instance.pk)
        #token = secrets.token_urlsafe(16)
        subject = 'Verify your email'
        
        context = {
            'username': mail.split('@')[0],
            'verification_url': 'http://127.0.0.1:8000/videoflix/v1/user/verify/' + str(instance.pk) + '/' + token
        }
        text_content = 'Please verify your email'
        html_content = render_to_string('verification_email.html', context)
      
        send_mail(subject, text_content, from_mail, [mail], html_message=html_content)
    
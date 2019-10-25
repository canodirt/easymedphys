#https://stackoverflow.com/questions/45845846/django-allauth-how-to-manually-send-a-reset-password-email

from allauth.account.views import PasswordResetView

from django.conf import settings
from django.dispatch import receiver
from django.http import HttpRequest
from django.middleware.csrf import get_token


#we need to do more of a for all users in CustomUser.objects.all()
#and roll


#@receiver(models.signals.post_save, sender=settings. AUTH_USER_MODEL)
def send_reset_password_email(sender, instance, created, **kwargs):

    if created:

        # First create a post request to pass to the view
        request = HttpRequest()
        request.method = 'POST'

        # add the absolute url to be be included in email
        if settings.DEBUG:
            request.META['HTTP_HOST'] = '127.0.0.1:8000'
        else:
            request.META['HTTP_HOST'] = 'www.mysite.com'

        # pass the post form data
        request.POST = {
            'email': instance.email,
            'csrfmiddlewaretoken': get_token(HttpRequest())
        }
        PasswordResetView.as_view()(request)  # email will be sent!
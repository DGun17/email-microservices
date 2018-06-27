import sys
from django.conf import settings
from django.core.mail import EmailMessage
from django.conf.urls import url
from django.http import HttpResponse

settings.configure(
    DEBUG=True,
    SECRET_KEY='thisisthesecretkey',
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
    EMAIL_USE_TLS=True,
    EMAIL_HOST='smtp.gmail.com',
    EMAIL_PORT=25,
    EMAIL_HOST_USER='<email>',
    EMAIL_HOST_PASSWORD='<password>',
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
)


def index(request):
    return HttpResponse('Hello World')


urlpatterns = (
    url(r'^$', index),
)


def message(subject, to, from_email, msj):
    e = EmailMessage()
    e.subject = subject
    e.to = [to]
    e.from_email = from_email
    e.body = msj
    e.send()


if __name__ == '__main__':
    message("Hola", ['johnflorez_1289@hotmail.com'], 'lmoncarisg@gmail.com')
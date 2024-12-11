from celery import shared_task
from django.core.mail import EmailMessage, send_mail
from django.conf import settings


@shared_task
def send_generic_email_test(subject, txt_, from_email, recipient_list, html_):
    pass


@shared_task
def send_generic_email(subject, txt_, from_email, recipient_list, html_):
    send_mail(
        subject,
        txt_,
        from_email,
        recipient_list,
        html_message=html_,
        fail_silently=False,
    )



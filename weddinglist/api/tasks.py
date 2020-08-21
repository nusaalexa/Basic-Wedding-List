from celery import task
from django.core.mail import send_mail

from .models import GiftList


@task
def gift_list_created():  # I need gift list id
    """
    Send email notification when gift list is created.
    """
    gift_list = GiftList.objects.get(id)
    subject = f'Gift List {gift_list.list_name}'
    message = f'Dear {gift_list.user}, \n' \
              f'You have successfully created a new giftlist!'
    mail_sent = send_mail(subject,
                          message,
                          'admin.weddinglist.com',
                          [gift_list.email])

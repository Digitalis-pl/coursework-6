import datetime
import smtplib
import pytz

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.http import request

from config.settings import EMAIL_HOST_USER
from newsletter_app.models import NewsLetterOptions, TrySend


def my_job():
    print('i am work')
    newsletters = NewsLetterOptions.objects.filter(status="started")
    for newsletter in newsletters:
        if newsletter:
            if newsletter.last_send_date.replace(tzinfo=pytz.utc) <= datetime.datetime.now().replace(tzinfo=pytz.utc):
                newsletter.status = 'finished'
                newsletter.save()
            elif datetime.datetime.now().replace(tzinfo=pytz.utc) < newsletter.next_send_date.replace(tzinfo=pytz.utc):
                continue
            else:
                try:
                    send_mail(subject=newsletter.message.subject,
                              message=newsletter.message.body,
                              from_email=EMAIL_HOST_USER,
                              recipient_list=[client.contact_email for client in newsletter.clients.all()],
                              fail_silently=False)
                    TrySend.objects.create(date_time_last_try=datetime.datetime.now(),
                                           status='success',
                                           server_answer='good',
                                           user=newsletter.newsletter_owner)
                    if newsletter.period == 'once':
                        newsletter.status = 'finished'
                        newsletter.save()
                    elif newsletter.period == 'every_day':
                        newsletter.next_send_date + datetime.timedelta(days=1)
                        newsletter.save()
                    elif newsletter.period == 'every_week':
                        newsletter.next_send_date + datetime.timedelta(days=7)
                        newsletter.save()
                    elif newsletter.period == 'every_month':
                        newsletter.next_send_date + datetime.timedelta(days=30)
                        newsletter.save()
                except smtplib.SMTPException as e:
                    TrySend.objects.create(date_time_last_try=datetime.datetime.now(),
                                           status='error',
                                           server_answer=e)


def start_sailing():
    print('start')
    scheduler = BackgroundScheduler()
    scheduler.add_job(my_job, 'interval', minutes=1)
    scheduler.start()

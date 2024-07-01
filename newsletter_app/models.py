from django.db import models
import datetime
from users.models import User

# Create your models here.

null_options = {'blank': True, 'null': True}


class Client(models.Model):
    name = models.CharField(max_length=150,
                            verbose_name='name',
                            help_text='имя пользователя')
    last_name = models.CharField(max_length=150,
                                 verbose_name='last_name',
                                 help_text='Фамилия пользователя')
    surname = models.CharField(max_length=150,
                               verbose_name='surname',
                               help_text='Отчество пользователя')
    contact_email = models.EmailField(verbose_name='email',
                                      help_text='email пользователя',
                                      unique=True)
    comment = models.TextField(verbose_name='Комментарий',
                               **null_options)

    newsletter_sender = models.ForeignKey(User,
                                          on_delete=models.SET_NULL,
                                          **null_options,
                                          verbose_name='Отправитель')

    def __str__(self):
        return f'{self.name} {self.last_name} {self.surname} {self.contact_email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['name', 'last_name', 'surname', 'contact_email']


class NewsLetterOptions(models.Model):
    STATUS = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("finished", "Завершена"),
        ("stopped", "Остановлена")
    ]

    PERIOD_CHOICES = [
        ("once", 'Единожды'),
        ("every_day", "Ежедневно"),
        ("every_week", "Еженедельно"),
        ("every_month", "Ежемесячно"),
    ]
    first_send_date = models.DateTimeField(verbose_name='дата создания',
                                           default=datetime.datetime.now())
    period = models.CharField(max_length=100,
                              verbose_name='Периодичность',
                              help_text='Периодичность',
                              choices=PERIOD_CHOICES,
                              default='once')
    status = models.CharField(max_length=100,
                              verbose_name='Статус',
                              help_text='Статус',
                              choices=STATUS,
                              default='created')
    message = models.ForeignKey('Message',
                                on_delete=models.SET_NULL,
                                **null_options)
    clients = models.ManyToManyField('Client',
                                     related_name='clients',
                                     blank=True)
    next_send_date = models.DateTimeField(verbose_name='дата следующей отправки',
                                          default=datetime.datetime.now())
    last_send_date = models.DateTimeField(verbose_name='дата окончания отправки',
                                          default=datetime.datetime.now())

    newsletter_owner = models.ForeignKey(User,
                                         verbose_name='владелец рассылки',
                                         on_delete=models.SET_NULL,
                                         **null_options)

    def __str__(self):
        return f'{self.first_send_date} {self.period} {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['first_send_date', 'status']


class Message(models.Model):
    body = models.TextField(verbose_name='Коментарий',
                            **null_options)
    subject = models.CharField(max_length=200,
                               verbose_name='Тема')

    message_owner = models.ForeignKey(User,
                                      verbose_name='владелец письма',
                                      on_delete=models.SET_NULL,
                                      **null_options)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['subject']


class TrySend(models.Model):
    STATUS = [
        ("success", "Ошибка"),
        ("error", "Успешно"),
    ]
    date_time_last_try = models.DateTimeField(auto_now=True,
                                              verbose_name='Последняя отправка')
    status = models.CharField(max_length=1000,
                              verbose_name='Статус')
    server_answer = models.CharField(max_length=1000,
                                     verbose_name='Ответ сервера', choices=STATUS)
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             **null_options,
                             verbose_name='Пользователь')

    def __str__(self):
        return f'{self.date_time_last_try} {self.status} {self.server_answer}'

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'


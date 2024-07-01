from django.db import models

# Create your models here.

null_options = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    content = models.TextField(verbose_name='Контент статьи')
    photo = models.ImageField(upload_to='articles/photo')
    view_counter = models.IntegerField(default=0, verbose_name='количество просмотров')
    published_date = models.DateTimeField(auto_now=True, **null_options, verbose_name='дата публикации')

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

    def __str__(self):
        return f'{self.title} {self.view_counter} {self.published_date}'

from django.apps import AppConfig


class NewsletterAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsletter_app'

    def ready(self):
        from newsletter_app.services import start_sailing
        start_sailing()
        print('start_sailing')
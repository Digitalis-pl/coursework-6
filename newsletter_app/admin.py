from django.contrib import admin
from newsletter_app.models import Client, NewsLetterOptions

# Register your models here.


@admin.register(NewsLetterOptions)
class AdminNewsletter(admin.ModelAdmin):
    list_display = ('first_send_date', 'period', 'status', 'message',)
    list_filter = ('status', 'first_send_date', 'period', 'message',)


@admin.register(Client)
class AdminNewsletter(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'surname', 'contact_email',)
    list_filter = ('name', 'last_name', 'surname', 'contact_email',)
    search_fields = ('name', 'last_name', 'surname', 'contact_email',)

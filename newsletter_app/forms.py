from django.forms import ModelForm, BooleanField

from newsletter_app.models import NewsLetterOptions, Client, Message

from users.forms import StyleFormMixin


class NewsletterForm(StyleFormMixin, ModelForm):
    class Meta:
        model = NewsLetterOptions
        exclude = ('newsletter_owner',)


class ClientsForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        exclude = ('newsletter_sender',)


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ('message_owner',)
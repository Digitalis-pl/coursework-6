import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from newsletter_app.models import Message, Client, NewsLetterOptions, TrySend
from django.shortcuts import redirect

from newsletter_app.forms import NewsletterForm, MessageForm, ClientsForm

# Create your views here.


def main_page(request):

    return render(request, 'newsletter_app/main_page.html')


def home_page(request):
    user = request.user
    newsletters = NewsLetterOptions.objects.filter(newsletter_owner=user)
    newsletter_counter = newsletters.count()
    print(newsletter_counter)
    active_newsletter = newsletters.filter(status="started").count()
    print(active_newsletter)
    clients = Client.objects.filter(newsletter_sender=user).count()
    print(clients)
    data = {'all_newsletter': newsletter_counter, 'active_newsletter': active_newsletter, 'clients': clients}
    return render(request, 'newsletter_app/admin_main.html', context=data)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter_app:admin_page')

    def form_valid(self, form): #почему тут form_valid?
        message = form.save()
        user = self.request.user
        message.message_owner = user
        message.save()


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('newsletter_app:message_detail', kwargs={'pk': self.object.pk})


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('newsletter_app:admin_page')


class MessageView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientsForm
    success_url = reverse_lazy('newsletter_app:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.newsletter_sender = user
        client.save()
        return super().form_valid(form)


class ClientListView(ListView):
    model = Client

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        queryset = queryset.filter(newsletter_sender=user)
        return queryset


class ClientDetailView(DetailView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientsForm

    def get_success_url(self):
        return reverse('newsletter_app:client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('newsletter_app:client_list')


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = NewsLetterOptions
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter_app:newsletter_list')

    def form_valid(self, form):  # почему тут form_valid?
        newsletter = form.save()
        user = self.request.user
        newsletter.newsletter_owner = user
        newsletter.save()
        return super().form_valid(form)

   # def form_valid(self, form):
   #     obj = form.save()
   #     send_letter(obj)
   #     return super().form_valid(form)


class NewsletterListView(LoginRequiredMixin, ListView):
    model = NewsLetterOptions

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        queryset = queryset.filter(newsletter_owner=user)
        return queryset


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = NewsLetterOptions
    form_class = NewsletterForm

    def get_success_url(self):
        return reverse('newsletter_app:newsletter_update', kwargs={'pk': self.object.pk})


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    model = NewsLetterOptions


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = NewsLetterOptions
    success_url = reverse_lazy('newsletter_app:newsletter_list')


class TrySendListView(ListView):
    model = TrySend

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        queryset = queryset.filter(user=user)
        return queryset


def sign_in(request):
    return render(request, 'newsletter_app/sign_in_page.html')


def activity_button(request):
    newsletters = NewsLetterOptions.objects.filter(status='created')
    for newsletter in newsletters:
        newsletter.status = 'started'
        newsletter.first_send_date = datetime.datetime.now()
        newsletter.save()
    return redirect(reverse('newsletter_app:newsletter_list'))


def status_button(request, pk):
    obj = get_object_or_404(NewsLetterOptions, pk=pk)
    if obj.status == 'started':
        obj.status = "finished"
        obj.save()
    elif obj.status == 'created':
        obj.status = "started"
    return redirect(reverse('newsletter_app:newsletter_list'))

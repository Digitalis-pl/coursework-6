from django.urls import path
from django.views.decorators.cache import cache_page

from newsletter_app.apps import NewsletterAppConfig
from newsletter_app import views

app_name = NewsletterAppConfig.name

urlpatterns = [
    path('status_button/<int:pk>', views.status_button, name='status_button'),
    path('', cache_page(60)(views.main_page), name='main_page'),
    path('sign_in/', views.sign_in, name='sign_in_page'),
    path('home/', views.home_page, name='home'),
    path('message_list/', cache_page(60)(views.MessageView.as_view()), name='admin_page'),
    path('create_message_page/', views.MessageCreateView.as_view(), name='message_create'),
    path('message_detail/<int:pk>', views.MessageDetailView.as_view(), name='message_detail'),
    path('message_update/<int:pk>', views.MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>', views.MessageDeleteView.as_view(), name='message_delete'),
    path('client_create', views.ClientCreateView.as_view(), name='client_create'),
    path('client_list/', cache_page(60)(views.ClientListView.as_view()), name='client_list'),
    path('client_detail/<int:pk>', views.ClientDetailView.as_view(), name='client_detail'),
    path('client_update/<int:pk>', views.ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>', views.ClientDeleteView.as_view(), name='client_delete'),
    path('newsletter_create/', views.NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newsletter_list/', cache_page(60)(views.NewsletterListView.as_view()), name='newsletter_list'),
    path('newsletter_detail/<int:pk>', views.NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('newsletter_update/<int:pk>', views.NewsletterUpdateView.as_view(), name='newsletter_update'),
    path('newsletter_delete/<int:pk>', views.NewsletterDeleteView.as_view(), name='newsletter_delete'),
    path('trysend_list/', cache_page(60)(views.TrySendListView.as_view()), name='trysend_list'),
]

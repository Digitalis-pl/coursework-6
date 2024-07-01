from django.urls import path
from django.views.decorators.cache import cache_page

from blog import views
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path('article_list', cache_page(60)(views.BlogListView.as_view()), name='blog_list'),
    path('', cache_page(60)(views.blog_main), name='main'),
    path('create_article/', views.BlogCreateView.as_view(), name='blog_create'),
    path('update_article/<int:pk>', views.BlogUpdateView.as_view(), name='blog_update'),
    path('article_detail/<int:pk>', cache_page(60)(views.BlogDetailView.as_view()), name='blog_detail'),
    path('delete_article/<int:pk>', views.BlogDeleteView.as_view(), name='blog_delete'),
]
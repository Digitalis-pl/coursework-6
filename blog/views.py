from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView

from blog.models import Blog
from blog.forms import BlogForm


# Create your views here.

class BlogCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    permission_required = 'blog.add_blog'
    success_url = reverse_lazy('blog:main')


class BlogListView(ListView):
    model = Blog


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    permission_required = 'blog.change_blog'

    def get_success_url(self):
        return reverse('blog:blog_update', kwargs={'pk': self.object.pk})


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
    permission_required = 'blog.delete_blog'


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_counter += 1
        self.object.save()
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['some_another_articles'] = Blog.objects.all()[:2]
        return context


def blog_main(request):
    view = []
    all_articles = Blog.objects.all().order_by("?")
    for article in all_articles:
        view.append(article.view_counter)
    top_views = max(view)
    some_another_articles = all_articles[:3]
    popular_article = all_articles.filter(view_counter=top_views).last()
    return render(request, 'blog/blog_main_page.html', {'popular_article': popular_article,
                                                        'some_another_articles': some_another_articles})
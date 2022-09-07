from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *


class GameHome(DataMixin, ListView):

    model = Game
    template_name = 'game/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Game.objects.filter(is_published=True).select_related('cat')


# def index(request):
#     posts = Game.objects.all()
#     template = 'game/index.html'
#     context = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, template, context)


def about(request):
    template = 'game/about.html'
    context = {
        'title': 'О сайте',
        'menu': menu,
    }
    return render(request, template, context)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'game/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     template = 'game/addpage.html'
#     context = {
#         'form': form,
#         'menu': menu,
#         'title': 'Добавление статьи про игры',
#     }
#     return render(request, template, context)


# def contact(request):
#     return HttpResponse('Обратная связь')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'game/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# def login(request):
#     return HttpResponse('Авторизация')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ShowPost(DataMixin, DeleteView):
    model = Game
    template_name = 'game/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self,*, object_list=None, **kwargs):
        context = super().get_context_data()
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

# def show_post(request, post_slug):
#     template = 'game/post.html'
#     post = get_object_or_404(Game, slug=post_slug)
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, template, context)


class GameCategory(DataMixin, ListView):
    model = Game
    template_name = 'game/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Game.objects.filter(
            cat__slug=self.kwargs['cat_slug'],
            is_published=True,
        ).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(
            title='Категория - ' + str(c.name),
            cat_selected=c.pk,
        )
        return dict(list(context.items()) + list(c_def.items()))

# def show_category(request, cat_slug):
#     cats = Category.objects.all()
#     cat = get_object_or_404(Category, slug=cat_slug)
#     posts = Game.objects.filter(cat_id=cat.id)
#     if len(posts) == 0:
#         raise Http404()
#     template = 'game/index.html'
#     context = {
#         'title': cat.name,
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': cat.id,
#         'cats': cats
#     }
#     return render(request, template, context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'game/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'game/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')

from django.db import transaction
from django.db.models import F
from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from .models import *
from .forms import *


def add_read(request, pk):
    post = get_object_or_404(NewsPost, id=pk)

    if not IsReadByUserStatus.objects.filter(post=post, user=request.user):
        with transaction.atomic():
            IsReadByUserStatus.objects.create(post=post, user=request.user)
            post.read += 1
            post.save()
            NSuser.objects.filter(id=request.user.id).update(news_read=F("news_read") + 1)
        data = {
            'read': int(post.read)
        }
        return JsonResponse(data)
    else:
        return HttpResponse(status=403)


class NSuserCabinet(View):
    form_class = NSuserCabinetForm
    template_name = 'cabinet.html'

    def get(self, request):
        form = self.form_class({'username': request.user.username,
                                'email': request.user.email,
                                'password': "",
                                'password_repeat': "",
                                'phone_number': request.user.phone_number})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        errors = {}

        if form.is_valid():
            nsuser = NSuser.objects.get(username=request.user.username)
            nsuser.username = form.cleaned_data['username']
            nsuser.phone_number = form.cleaned_data['phone_number']
            nsuser.email = form.cleaned_data['email']
            nsuser.save()

        else:
            errors = form.errors

        return render(request, self.template_name, {'form': form, 'errors': errors})


class NewsCategoryTape(ListView):
    model = Category
    template_name = 'main_page.html'

    def get_context_data(self, **kwargs):
        context = super(NewsCategoryTape, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class NewsDetail(ListView):
    model = Category
    template_name = 'posts.html'

    def get_context_data(self, **kwargs):

        context = super(NewsDetail, self).get_context_data(**kwargs)
        context['posts'] = NewsPost.objects.filter(
            post_category__category_name=self.kwargs['slug'].replace("_", " ")).order_by('-post_date')
        return context

    def get(self, request, *args, **kwargs):
        context = NewsPost.objects.filter(
            post_category__category_name=self.kwargs['slug'].replace("_", " ")).order_by('-post_date')
        category = get_object_or_404(Category, category_name=self.kwargs['slug'].replace("_", " "))

        if category.is_active is False:
            return redirect('main_page')
        return render(request, 'posts.html', context={'slug': self.kwargs['slug'].replace("_", " "),
                                                      'posts': context})


def registration(request):
    args = {}
    form = NSuserForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            NSuser.objects.create_user(username=request.POST['username'],
                                       password=request.POST['password'],
                                       email=request.POST['email'],
                                       phone_number=request.POST['phone_number'])
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            login(request, user)
            return redirect('main_page')
    else:
        form = NSuserForm()

    args['form'] = form
    return render(request, 'registration.html', {'form': form})


def userlogin(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main_page')
            else:
                error = 'something invalid'
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error': error})


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('main_page')

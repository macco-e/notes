from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from .models import Account


def sign_up_view(request):
    return render(request, 'notes/signup.html')


def create_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            Account.objects.create_user(username, password=password)
            return redirect('notes:signup')
        except IntegrityError:
            return redirect('notes:signup')

    if request.method == 'GET':
        return redirect('notes:signup')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'notes/login.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('notes:home')
        else:
            return render(request, 'notes/login.html',
                          {'error': 'ユーザ名かパスワードが間違っています'})


def logout_view(request):
    logout(request)
    return redirect('notes:login')


def redirect_to(request):
    return render(request, 'notes/login.html')


class HomeView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    model = Account
    template_name = 'notes/home.html'
    context_object_name = 'account_list'


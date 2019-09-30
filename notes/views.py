from django.db.utils import IntegrityError
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from .models import Account


def sign_up(request):
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


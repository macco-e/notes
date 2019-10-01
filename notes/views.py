from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .models import Account, Follow, NotesBetween20190930and20191006


def sign_up_view(request):
    return render(request, 'notes/signup.html')


def create_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            Account.objects.create_user(username, password=password)
            return redirect('notes:login')
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

    template_name = 'notes/home.html'
    context_object_name = 'notes_list'

    def get_queryset(self):
        login_id = self.request.user.id
        follows = Follow.objects.filter(follow_id=login_id)
        target_list = [str(login_id)] + [str(f.follower_id.id) for f in follows]
        return NotesBetween20190930and20191006.objects.filter(
            noted_user_id__in=target_list).order_by('-created_at')


class UserDetailView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    model = NotesBetween20190930and20191006
    template_name = 'notes/detail.html'
    context_object_name = 'notes_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_user'] = Account.objects.get(pk=self.kwargs['pk'])
        context['notes_list'] = self.model.objects.filter(noted_user_id=self.kwargs['pk'])
        return context


class PostNoteView(LoginRequiredMixin, CreateView):
    login_url = '/login/'

    model = NotesBetween20190930and20191006
    template_name = 'notes/post_note.html'

    fields = ['text']


class SettingsView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'

    model = Account
    template_name = 'notes/settings.html'
    fields = ['username', 'icon']
    success_url = reverse_lazy('notes:home')



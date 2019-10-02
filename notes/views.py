from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .models import Account, Follow, NotesBetween20190930and20191006


# auth -------------------------------------------------------------------------

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


# Home--------------------------------------------------------------------------

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


def search_home_redirect(request):
    if request.POST['search_word']:
        return redirect('notes:home_notes_search', request.POST['search_word'])
    else:
        return redirect('notes:home')


class HomeNotesSearchView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    template_name = 'notes/home.html'
    context_object_name = 'notes_list'

    def get_queryset(self):
        login_id = self.request.user.id
        follows = Follow.objects.filter(follow_id=login_id)
        target_list = [str(login_id)] + [str(f.follower_id.id) for f in follows]
        return NotesBetween20190930and20191006.objects.filter(
            noted_user_id__in=target_list, text__contains=self.kwargs['search_word']).order_by('-created_at')

# User -------------------------------------------------------------------------

class UserDetailView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    model = NotesBetween20190930and20191006
    template_name = 'notes/detail.html'
    context_object_name = 'notes_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_follow'] = Follow.objects.filter(follow_id=self.kwargs['pk']).count()
        context['num_follower'] = Follow.objects.filter(follower_id=self.kwargs['pk']).count()
        context['is_follow'] = Follow.objects.filter(follow_id=self.request.user.id).filter(follower_id=self.kwargs['pk']).count()
        context['target_user'] = Account.objects.get(pk=self.kwargs['pk'])
        context['notes_list'] = self.model.objects.filter(noted_user_id=self.kwargs['pk']).order_by('-created_at')
        context['self_pk'] = self.kwargs['pk']
        return context


def follow(request, pk):
    f = Follow.objects.create(follow_id=request.user,
                              follower_id=Account.objects.get(pk=pk))
    f.save()
    return redirect('notes:detail', pk=pk)


def unfollow(request, pk):
    f = Follow.objects.filter(follow_id=request.user).filter(follower_id=pk)
    f.delete()
    return redirect('notes:detail', pk=pk)


def search_user_redirect(request, self_pk):
    if request.POST['search_word']:
        return redirect('notes:user_notes_search', self_pk=self_pk, search_word=request.POST['search_word'])
    else:
        return redirect('notes:detail', pk=self_pk)


class UserNoteSearchView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    model = NotesBetween20190930and20191006
    template_name = 'notes/detail.html'
    context_object_name = 'notes_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_follow'] = Follow.objects.filter(follow_id=self.request.user.id).count()
        context['num_follow'] = Follow.objects.filter(follow_id=self.request.user.id).count()
        context['num_follower'] = Follow.objects.filter(follower_id=self.request.user.id).count()
        context['is_follow'] = Follow.objects.filter(follow_id=self.request.user.id).filter(follower_id=self.kwargs['self_pk']).count()
        context['target_user'] = Account.objects.get(pk=self.kwargs['self_pk'])
        context['notes_list'] = self.model.objects.filter(noted_user_id=self.kwargs['self_pk'], text__contains=self.kwargs['search_word']).order_by('-created_at')
        context['self_pk'] = self.kwargs['self_pk']
        return context


# follow list ------------------------------------------------------------------

class UserFollowListView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    template_name = 'notes/follow_list.html'
    context_object_name = 'follow_list'

    def get_queryset(self):
        fs = Follow.objects.filter(follow_id=self.kwargs['pk'])
        follows = [str(f.follower_id.id) for f in fs]
        return Account.objects.filter(id__in=follows)


class UserFollowerListView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    template_name = 'notes/follower_list.html'
    context_object_name = 'follower_list'

    def get_queryset(self):
        fs = Follow.objects.filter(follower_id=self.kwargs['pk'])
        followers = [str(f.follow_id.id) for f in fs]
        return Account.objects.filter(id__in=followers)


# Search -----------------------------------------------------------------------

class SearchListView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    model = NotesBetween20190930and20191006
    template_name = 'notes/search.html'
    context_object_name = 'notes_list'

    def get_queryset(self):
        return NotesBetween20190930and20191006.objects.all().order_by('-created_at')


def search_notes_redirect(request):
    if request.POST['search_word']:
        return redirect('notes:searched', request.POST['search_word'])
    else:
        return redirect('notes:search')


class SearchedListView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    template_name = 'notes/home.html'
    context_object_name = 'notes_list'

    def get_queryset(self):
        return NotesBetween20190930and20191006.objects.filter(
            text__contains=self.kwargs['search_word']).order_by('-created_at')


# Users ------------------------------------------------------------------------

class UsersListView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    model = Account
    template_name = 'notes/users.html'
    context_object_name = 'users_list'


def search_redirect(request):
    if request.POST['search_word']:
        return redirect('notes:users_search', request.POST['search_word'])
    else:
        return redirect('notes:users')


class UsersSearchView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    model = Account
    template_name = 'notes/users.html'
    context_object_name = 'users_list'

    # queryにマッチしたものだけ返す
    def get_queryset(self):
        return Account.objects.filter(username__contains=self.kwargs['search_word'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_word'] = self.kwargs['search_word']
        return context

# Settings----------------------------------------------------------------------

class SettingsView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'

    model = Account
    template_name = 'notes/settings.html'
    fields = ['username', 'icon']
    success_url = reverse_lazy('notes:home')


# Create -----------------------------------------------------------------------

class PostNoteView(LoginRequiredMixin, CreateView):
    login_url = '/login/'

    model = NotesBetween20190930and20191006
    template_name = 'notes/post_note.html'

    fields = ['noted_user_id', 'text']
    success_url = reverse_lazy('notes:home')

# Node detail ------------------------------------------------------------------

class NoteDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'

    model = NotesBetween20190930and20191006
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'





# period -----------------------------------------------------------------------

def filter_1hour(request):
    pass


def filter_3hour(request):
    pass


def filter_6hour(request):
    pass


def filter_Today(request):
    pass


def filter_Thisweek(request):
    pass







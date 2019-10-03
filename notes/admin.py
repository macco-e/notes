from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Follow, Notes


class AccountCreationAdmin(forms.ModelForm):
    class Meta:
        model = Account
        fields = ()

    def save(self, commit=True):
        user = super(AccountCreationAdmin, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class AccountAdmin(UserAdmin):
    add_form = AccountCreationAdmin

    fieldsets = [
        ('Auth', {'fields': ['username', 'password', 'icon']}),
    ]
    add_fieldsets = [
        ('Auth', {'fields': ['username', 'password', 'icon']}),
    ]

    list_display = ('id', 'username')
    list_filter = ('id', 'username')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('follow_id', 'follower_id')
    list_filter = ['follow_id', 'follower_id']


class NotesBetweenAdmin(admin.ModelAdmin):
    list_display = ('author', 'text')


admin.site.register(Account, AccountAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Notes, NotesBetweenAdmin)

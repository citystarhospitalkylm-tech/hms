from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Role

class UserCreateForm(UserCreationForm):
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'department', 'phone', 'roles']


class UserUpdateForm(UserChangeForm):
    password = None  # Hide password field

    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'department', 'phone', 'roles']
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='Введіть ваш нікнейм', required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']

        if commit:
            user.save()

        return user
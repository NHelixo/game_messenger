from django import forms
from django.contrib.auth.models import User
from .models import UserPicture
import os

class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label="Нікнейм")
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False, label='Фото профілю')
    old_password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput, label="Старий пароль")
    new_password = forms.CharField(max_length=100, required=False, widget=forms.PasswordInput, label="Новий пароль")

    class Meta:
        model = User
        fields = ['first_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            old_picture = UserPicture.objects.get(pk=self.instance.profile.id)
            if old_picture:
                if os.path.isfile(old_picture.profile_picture.path):
                    os.remove(old_picture.profile_picture.path)
            user_picture, created = UserPicture.objects.get_or_create(user=user)

            extension = profile_picture.name.split('.')[-1]
            profile_picture.name = f"ava_{user.id}.{extension}"

            user_picture.profile_picture = profile_picture
            user_picture.save()

        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)
            user.save()

        if commit:
            user.save()

        return user

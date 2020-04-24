from django import forms
from django.contrib.auth.models import User
class NewArticleForm(forms.Form):
 head = forms.CharField(label = "Заголовок", max_length=50)
 text = forms.CharField(label = "Описание", max_length=None, widget=forms.Textarea)

class LoginForm(forms.Form):
    username = forms.CharField(label = "Логин", max_length=200)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='ПарольR', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
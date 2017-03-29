from django import forms

from member.models import MyUser


class SignupForm(forms.Form):
    username = forms.CharField(max_length=30)
    nickname = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=30, required=True)
    gender = forms.ChoiceField(
        choices=MyUser.CHOICES_GENDER,
        widget=forms.RadioSelect(),
    )
    age = forms.IntegerField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)

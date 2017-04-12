from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class SignupForm(forms.Form):
    # username = forms.CharField(max_length=30)
    nickname = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=255, required=True)
    gender = forms.ChoiceField(
        choices=User.CHOICES_GENDER,
        widget=forms.RadioSelect(),
    )
    age = forms.IntegerField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email already exists')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('password1 does not match with password2')
        return password2

    def create_user(self):
        print('self.cleaned_data:{}'.format(self.cleaned_data))

        # username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password2 = self.cleaned_data['password2']
        gender = self.cleaned_data['gender']
        age = self.cleaned_data['age']
        nickname = self.cleaned_data['nickname']

        user = User.objects.create_user(
            # username=username,
            # username을 email로(email을 user id로 사용)
            # username=email,
            email=email,
            nickname=nickname,
            password=password2,
        )

        user.gender = gender
        user.age = age
        # user.nickname = nickname
        user.save()

        user = authenticate(
            email=email,
            password=password2
        )
        return user


class LoginForm(forms.Form):
    # username = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
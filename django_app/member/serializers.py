from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions

UserModel = get_user_model()


class SignupSerializer(serializers.Serializer):
    # username = serializers.CharField(max_length=255)
    password1 = serializers.CharField(
        style={'input_type': 'password'},
        min_length=8
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        min_length=8
    )
    email = serializers.EmailField()
    nickname = serializers.CharField(max_length=255, required=True)
    gender = serializers.ChoiceField(choices=UserModel.CHOICES_GENDER, required=False)
    age = serializers.IntegerField(max_value=200, required=False)

    class Meta:
        model = UserModel
        fields = (
            # 'username',
            'nickname', 'email',
            'gender', 'age', 'password1', 'password2'
        )

    def validate_email(self, email):
        # print('\nvalidate_email\n')
        if UserModel.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address. so try another one"))
        return email

    def validate_nickname(self, nickname):
        if UserModel.objects.filter(nickname__iexact=nickname).exists():
            raise serializers.ValidationError(
                _("A user is already registered with this nickname. so try another one"))
        return nickname

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password1 != password2:
            msg = _('Two passwords do not match. Are you sure?...')
            raise exceptions.ValidationError(msg)
        return attrs

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    # nickname = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = UserModel
        fields = (
            # 'nickname',
            'email', 'password',
        )

    def _validate_password(self, email, password):
        user = None

        if email and password:
            user = authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        if user is None:
            # we assume that email is already validated in 'validate_email',
            # so, we assume that only password does not match
            msg = _('Your password does not match. Are your sure?')
            raise exceptions.ValidationError(msg)

        return user

    # def _validate_username(self, username, password):
    #     user = None
    #
    #     if username and password:
    #         user = authenticate(username=username, password=password)
    #     else:
    #         msg = _('Must include "username" and "password".')
    #         raise exceptions.ValidationError(msg)
    #
    #     return user

    def _validate_username_email(self, username, email, password):
        user = None

        if email and password:
            user = authenticate(email=email, password=password)
        elif username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate_email(self, email):
        # print('validate_email:{}'.format(email))

        try:
            UserModel.objects.get(email__iexact=email).get_username()
        except UserModel.DoesNotExist:
            msg = _('A user using this email does not exist, check the email again.')
            raise exceptions.ValidationError(msg)
        return email

    def validate(self, attrs):
        # print('\nvalidate:{}'.format(attrs))

        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

            # Authentication through username
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
                user = self._validate_username(username, password)

            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, email, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = UserModel.objects.get(email__iexact=email).get_username()
                except UserModel.DoesNotExist:
                    pass

                user = self._validate_password(email, password)

            if username:
                user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs


class UserInfoSerializer(serializers.Serializer):
    email = serializers.EmailField()
    nickname = serializers.CharField(max_length=255)
    gender = serializers.ChoiceField(choices=UserModel.CHOICES_GENDER, required=False)
    age = serializers.IntegerField(max_value=200, required=False)

    class Meta:
        model = UserModel
        fields = ('nickname', 'email', 'gender', 'age',)

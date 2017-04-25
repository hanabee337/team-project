from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            'nickname', 'email',
            'age', 'gender',
            'password',
            'user_type',
        )

    def save(self, **kwargs):
        # print('save self.validated_data:{}'.format(self.validated_data))

        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )
        # print('validated_data:{}'.format(validated_data))

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance

    def create(self, validated_data):
        print('\ncreate validated_data:{}\n'.format(validated_data))
        user = UserModel.objects.create_user(**validated_data)
        return user


class SignupSerializer(serializers.Serializer):
    password1 = serializers.CharField(
        style={'input_type': 'password'},
        min_length=8
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        min_length=8
    )
    email = serializers.EmailField(required=True)
    nickname = serializers.CharField(max_length=255, required=True)
    gender = serializers.ChoiceField(choices=UserModel.CHOICES_GENDER)
    age = serializers.IntegerField(max_value=200, required=False, allow_null=True)

    def validate_email(self, email):
        if UserModel.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                # _("A user is already registered with this e-mail address. so try another one"))
                _("이미 가입된 이메일입니다. 다른 이메일로 가입해 주세요"))
        return email

    def validate_nickname(self, nickname):
        if UserModel.objects.filter(nickname__iexact=nickname).exists():
            raise serializers.ValidationError(
                # _("A user is already registered with this nickname. so try another one"))
                _("이미 등록된 닉네임입니다. 다른 닉네임으로 등록해 주세요."))
        return nickname

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password1 != password2:
            # msg = _('Two passwords do not match. Are you sure?...')
            msg = _('두 개의 패스워드가 일치하지 않습니다. 확인해 주세요')
            raise exceptions.ValidationError(msg)
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = UserModel
        fields = (
            'email', 'password',
        )

    def _validate_password(self, email, password):
        user = None

        if email and password:
            user = authenticate(email=email, password=password)
        else:
            # msg = _('Must include "email" and "password".')
            msg = _('반드시 이메일과 패스워드를 입력해 주세요.')
            raise exceptions.ValidationError(msg)

        if user is None:
            # we assume that email is already validated in 'validate_email',
            # so, we assume that only password does not match
            # msg = _('Your password does not match. Are your sure?')
            msg = _('입력하신 패스워드가 맞지 않습니다.')
            raise exceptions.ValidationError(msg)

        return user

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
            # msg = _('A user using this email does not exist, check the email again.')
            msg = _('입력하신 이메일은 등록되어 있지 않습니다. 이메일을 확인해 주세요.')
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
        fields = ('nickname', 'email', 'gender', 'age', 'user_type')


class Facebook_SignUp_Serializer(serializers.Serializer):
    # access_token = serializers.CharField(max_length=255, required=True, allow_blank=False, allow_null=False)

    # email field works as Facebook user id
    email = serializers.CharField(max_length=255, required=True, allow_blank=False, allow_null=False)
    nickname = serializers.CharField(max_length=255, required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data):
        # print('\ncreate validated_data:{}\n'.format(validated_data))
        user = UserModel.objects.create_user(**validated_data)
        user.user_type = 'F'
        user.save()
        # print('user.user_type: {}'.format(user.user_type))
        return user

    def save(self, **kwargs):
        # print('save self.validated_data:{}'.format(self.validated_data))

        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )
        # print('validated_data:{}'.format(validated_data))

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance

    def validate_email(self, email):
        if UserModel.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                # _("A user is already registered with this e-mail address. so try another one"))
                _("이미 가입된 이메일입니다. 다른 이메일로 가입해 주세요"))
        return email

    def validate_nickname(self, nickname):
        if UserModel.objects.filter(nickname__iexact=nickname).exists():
            raise serializers.ValidationError(
                # _("A user is already registered with this nickname. so try another one"))
                _("이미 등록된 닉네임입니다. 다른 닉네임으로 등록해 주세요."))
        return nickname

    def validate(self, attrs):
        # print('validate file: {}'.format(__file__))
        # print('attrs:{}'.format(attrs))
        #
        # # email field is considered as facebook user id
        # user_id = attrs.get('email')
        #
        # # 해당 USER_ID로 graph API에 유저정보를 요청
        # url_api_user = 'https://graph.facebook.com/{user_id}'.format(
        #     user_id=user_id
        # )
        # fields = [
        #     'id',
        #     'first_name',
        #     'last_name',
        #     'gender',
        #     'picture',
        #     'email',
        # ]
        #
        # params = {
        #     'fields': ','.join(fields),
        #     'access_token': USER_ACCESS_TOKEN,
        # }
        # r = requests.get(url_api_user, params)
        # dict_user_info = r.json()
        # pprint(dict_user_info)
        #
        # print('f/b email:{}'.format(dict_user_info['email']))

        return attrs


class Facebook_LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)

    class Meta:
        model = UserModel
        fields = (
            'email', 'password',
        )

    def _validate_password(self, email, password):
        user = None

        if email and password:
            user = authenticate(email=email, password=password)
        else:
            # msg = _('Must include "email" and "password".')
            msg = _('반드시 이메일과 패스워드를 입력해 주세요.')
            raise exceptions.ValidationError(msg)

        if user is None:
            # we assume that email is already validated in 'validate_email',
            # so, we assume that only password does not match
            # msg = _('Your password does not match. Are your sure?')
            msg = _('입력하신 패스워드가 맞지 않습니다.')
            raise exceptions.ValidationError(msg)

        return user

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
            # msg = _('A user using this email does not exist, check the email again.')
            msg = _('입력하신 이메일은 등록되어 있지 않습니다. 이메일을 확인해 주세요.')
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


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8, required=True)
    password1 = serializers.CharField(
        style={'input_type': 'password'},
        min_length=8,
        required=True
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        min_length=8,
        required=True
    )

    def validate_old_password(self, old_password):
        # print('old_password:{}'.format(old_password))

        self.request = self.context.get('request')
        self.user = self.request.user

        # print('self.user:{}'.format(self.user))

        pw_valid = self.user.check_password(old_password)
        # print('pw_valid:{}'.format(pw_valid))

        if pw_valid:
            return old_password
        else:
            msg = _('입력하신 패스워드가 맞지 않습니다. 패스워드를 다시 확인해 주세요.')
            raise exceptions.ValidationError(msg)

    def validate(self, attrs):
        # print('attrs:{}'.format(attrs))
        if attrs.get('password1') != attrs.get('password2'):
            msg = _('새로 입력하신 패스워드가 동일하지 않습니다. 패스워드를 확인해 주세요.')
            raise exceptions.ValidationError(msg)
        if attrs.get('old_password') == attrs.get('password2'):
            msg = _('패스워드가 기존 패스워드와 동일합니다. 패스워드를 변경해 주세요.')
            raise exceptions.ValidationError(msg)
        return attrs

    def save(self, **kwargs):
        # print('kwargs:{}'.format(kwargs))
        new_password = kwargs.get('password')
        # print('new_password:{}'.format(new_password))
        # print('self.user:{}'.format(self.user))
        self.user.set_password(new_password)
        self.user.save()

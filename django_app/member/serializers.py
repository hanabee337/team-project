from rest_framework import serializers

from .models import MyUser


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(
        style={'input_type': 'password'},
        min_length=8,
    )
    # extra_kwargs = {
    #     'password': {'write_only': True}
    # }
    email = serializers.EmailField()
    age = serializers.IntegerField(max_value=200)
    nickname = serializers.CharField(max_length=30)
    gender = serializers.ChoiceField(choices=MyUser.CHOICES_GENDER)

    class Meta:
        model = MyUser
        fields = (
            'username', 'nickname', 'email',
            'gender', 'age', 'password',
        )

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        return user
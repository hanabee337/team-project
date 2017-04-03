from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


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
    nickname = serializers.CharField(max_length=30)
    gender = serializers.ChoiceField(choices=User.CHOICES_GENDER, required=False)
    age = serializers.IntegerField(max_value=200, required=False)

    class Meta:
        model = User
        fields = (
            'username', 'nickname', 'email',
            'gender', 'age', 'password',
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

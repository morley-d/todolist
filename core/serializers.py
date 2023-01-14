from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from core.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
         UniqueValidator(queryset=User.objects.all())
        ]
    )
    password = serializers.CharField(min_length=1, write_only=True, validators=[validate_password])
    password_repeat = serializers.CharField(min_length=1, write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password_repeat'
        ]

    def validate(self, attrs: dict) -> dict:
        """
        Переопределил пустой validate для проверки пароля, так же достаю и удаляю password_repeat.
        """
        password_repeat = attrs.pop('password_repeat', None)
        password = attrs.get('password')

        if password_repeat != password:
            raise ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data: dict) -> User:
        user = User.objects.create_user(**validated_data)
        return user


class RetrieveUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict) -> dict:
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError('password or username is not correct')
        attrs["user"] = user
        return attrs


class PasswordUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(min_length=1, write_only=True)
    new_password = serializers.CharField(min_length=1, write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('old_password', 'new_password')

    def validate(self, attrs: dict) -> dict:
        """
        Переопределил пустой validate для проверки пароля, так же достаю и удаляю password_repeat.
        """
        password_old = attrs.get('old_password')

        user: User = self.instance
        if not user.check_password(password_old):
            raise ValidationError({'old_password': 'is incorrect'})
        return attrs

    def update(self, instance: User, validated_data: dict) -> User:
        instance.set_password(validated_data['new_password'])
        instance.save(update_fields=['password'])
        return instance

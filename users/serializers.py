from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class UserValidateSerializer(serializers.Serializer):
    username = serializers.RegexField(regex=r'^[a-zA-Zа-яА-Я0-9 ]*$', max_length=255,
                                            error_messages={'invalid': "only letters and numbers"})
    password = serializers.CharField()


class AuthorizationValidateSerializer(UserValidateSerializer):
    pass


class RegistrationValidateSerializer(UserValidateSerializer):

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
            raise ValidationError('User already exists')
        except User.DoesNotExist:
            return username

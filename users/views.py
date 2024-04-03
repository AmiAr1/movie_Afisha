from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from .serializers import *
from django.contrib.auth.models import User


@api_view(['POST'])
def registration_api_view(request):
    # 0. проверка данных
    serializer = RegistrationValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # 1. на основе этих данных создаем пользователя

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    # 2. создаем пользователя

    user = User.objects.create_user(username=username, password=password)

    # 3. возвращаем
    return Response(status=201, data={'user_id': user.id})


@api_view(['POST'])
def authorization_api_view(request):
    # 0. шаг: Validation
    serializer = AuthorizationValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # 1. шаг: провести аутентификацию, поиск пользователя по учетным данным
    # 2. шаг провести аунтефикацию, поиск пользователя по учетным данным
    user = authenticate(**serializer.validated_data)  # по этим данным будем искать пользователя

    # 3. если пользователь существует возращаем ключ

    if user is not None:
        # возвращаем ключ
        token_, created = Token.objects.get_or_create(user=user)
        return Response(data={'key': token_.key})
        # return error
    return Response(status=401, data={'message': 'User not found'})
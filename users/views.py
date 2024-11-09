import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import TelegramUser
import hashlib
import hmac
from django.conf import settings

class AuthView(APIView):
    permission_classes = []

    def post(self, request):
        init_data = request.data.get('initData')
        print("Received initData:", init_data)
        if not init_data:
            return Response({'error': 'initData is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_data = self.parse_init_data(init_data)
            telegram_id = user_data['id']
            first_name = user_data['first_name']
            last_name = user_data.get('last_name', '')
            username = user_data.get('username', '')

            user, created = User.objects.get_or_create(username=username, defaults={
                'first_name': first_name,
                'last_name': last_name,
            })

            if created:
                user.set_unusable_password()
                user.save()

            telegram_user, created = TelegramUser.objects.get_or_create(
                telegram_id=telegram_id,
                defaults={
                    'user': user,
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username,
                }
            )

            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key}, status=status.HTTP_200_OK)

        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Invalid initData.'}, status=status.HTTP_400_BAD_REQUEST)

    def parse_init_data(self, init_data):
        params = init_data.copy()
        hash_received = params.pop('hash', None)

        if not hash_received:
            raise ValueError('Hash is missing.')

        # Преобразуем user в JSON-строку для корректного сравнения
        if 'user' in params and isinstance(params['user'], dict):
            params['user'] = json.dumps(params['user'], separators=(',', ':'))

        # Создаем строку для проверки данных
        data_check_string = '\n'.join([f"{key}={params[key]}" for key in sorted(params)])

        # Формируем секретный ключ с "WebAppData" в качестве ключа
        secret_key = hmac.new(b"WebAppData", settings.TELEGRAM_BOT_TOKEN.encode(), hashlib.sha256).digest()

        # Вычисляем hash
        hmac_obj = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)
        hash_calculated = hmac_obj.hexdigest()

        print("Data check string:", data_check_string)
        print("Computed hash:", hash_calculated)
        print("Received hash:", hash_received)

        # Сравниваем полученный hash с вычисленным
        if not hmac.compare_digest(hash_received, hash_calculated):
            raise ValueError('Invalid signature.')

        # Извлекаем данные пользователя
        user_data = json.loads(params['user'])
        return {
            'id': user_data['id'],
            'first_name': user_data['first_name'],
            'last_name': user_data.get('last_name', ''),
            'username': user_data.get('username', ''),
        }

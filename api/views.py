from rest_framework.views import APIView
from rest_framework.response import Response

class GreetingView(APIView):
    def get(self, request):
        name = request.GET.get('name', 'Гость')
        message = f'Привет, {name}!'
        return Response({'name': name, 'message': message})

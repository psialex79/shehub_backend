from rest_framework import generics, permissions
from .models import Meeting
from .serializers import MeetingSerializer
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class MeetingCreateView(generics.CreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        telegram_user = self.request.user.telegram_profile
        serializer.save(author=telegram_user, isNew=True)

class MeetingListView(generics.ListAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logger.info(f"Заголовок Authorization: {self.request.headers.get('Authorization')}")
        if not self.request.user.is_authenticated:
            return Response({"error": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)
        return Meeting.objects.filter(author=self.request.user.telegram_profile)

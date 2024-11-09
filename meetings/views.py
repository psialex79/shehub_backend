from rest_framework import generics, permissions
from .models import Meeting
from .serializers import MeetingSerializer

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
        return Meeting.objects.filter(author=self.request.user.telegram_profile)

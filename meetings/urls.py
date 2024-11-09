from django.urls import path
from .views import MeetingCreateView, MeetingListView

urlpatterns = [
    path('add/', MeetingCreateView.as_view(), name='add_meeting'),
    path('list/', MeetingListView.as_view(), name='list_meetings'),
]

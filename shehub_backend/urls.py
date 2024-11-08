from django.contrib import admin
from django.urls import path

from api.views import GreetingView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/greeting/', GreetingView.as_view()),
]

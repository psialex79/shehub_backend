from django.db import models
from users.models import TelegramUser

class Meeting(models.Model):
    author = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, related_name='meetings'
    )
    invitee_name = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    isNew = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Встреча {self.author} с {self.invitee_name} в {self.place} на {self.date} в {self.time}'

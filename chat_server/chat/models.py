from django.db import models

from chat_server.chat_server.models import CoreModel


# Create your models here.


class Messages(CoreModel):
    sender = models.ForeignKey("users.Users", on_delete=models.CASCADE)
    receiver = models.ForeignKey("users.Users", on_delete=models.CASCADE)
    message = models.TextField(max_length=1200, null=True, blank=True)
    has_seen = models.BooleanField(default=False)

    class Meta:
        ordering = ('create_time',)

    def __str__(self):
        return
        return f"To: {self.receiver_name} From: {self.sender_name} Message: {self.message}"

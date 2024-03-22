from django.db import models

from chat_server.chat_server.models import CoreModel


# Create your models here.

class Friends(CoreModel):
    user = models.ForeignKey("users.Users", on_delete=models.DO_NOTHING, verbose_name="用户", help_text="用户")
    friend = models.ForeignKey("users.Users", on_delete=models.DO_NOTHING, verbose_name="好友id", null=False)

    def __str__(self):
        return self.friend.__str__()

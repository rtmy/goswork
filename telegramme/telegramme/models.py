from django.db import models


class Message(models.Model):
    received = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)

    # read_by_sender = models.BooleanField(default=False)
    # read_by_receiver = models.BooleanField(default=False)

    sender_address = models.CharField(max_length=255, blank=False, null=False)
    receiver_address = models.CharField(max_length=255, blank=False, null=False)

    content = models.CharField(max_length=1000, blank=False, null=False)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

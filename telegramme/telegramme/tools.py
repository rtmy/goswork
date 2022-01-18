from channels.db import database_sync_to_async

from telegramme import models 


def register_message_sync(**message):
    print('registering message', message)
    
    obj, cr = models.Message.objects.get_or_create(
        **message
    )
    return cr


@database_sync_to_async
def register_message(**message):
    print('registering message', message)
    
    obj, cr = models.Message.objects.get_or_create(
        **message
    )
    return cr
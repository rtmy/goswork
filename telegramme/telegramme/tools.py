from channels.db import database_sync_to_async

from telegramme import models 


@database_sync_to_async
def register_message(**message):
    print('registering message', message)
    
    obj, cr = models.Message.objects.get_or_create(
        **message
    )
    return cr
from django.http import JsonResponse
import datetime

from telegramme import models 
from telegramme.outconnections import OutConnectionSignleton


def get_server_state():
    return 'connected'


def current_state(request):
    return JsonResponse({'state': get_server_state()})


def init_connection(request):
    s = OutConnectionSignleton()
    # Todo: change state
    return JsonResponse({'state': get_server_state()})


def send_message(request):
    message = 'sent from APIshka'
    
    obj, cr = models.Message.objects.get_or_create(
        content=message,
        received=False,
        datetime=datetime.datetime.now()
    )
    
    OutConnectionSignleton().connection.ws.send(message)

    return JsonResponse({'state': get_server_state()})


def message_list(request):
    qs = models.Message.objects.all()
    messages = [dict(
        content=m.content,
        received=m.received,
        
    ) for m in qs]
    
    # qs.update(read=True)
    
    # Todo: отправить сообщение о прочитке  
    
    return JsonResponse({'messages': messages})

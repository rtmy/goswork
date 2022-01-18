import os
from django.http import JsonResponse
import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from telegramme.outconnections import OutConnectionSignleton
from telegramme.tools import register_message
from telegramme import models


def get_server_state():
    with open('statefile', 'r') as file:
        return file.read()


def current_state(request):
    return JsonResponse({'state': get_server_state()})


def init_connection(request):
    s = OutConnectionSignleton()
    # Todo: change state
    return JsonResponse({'state': get_server_state()})


# слить два следующих метода в один, чтобы они работали через проверку текущего режима
# режимы:
# на каждый из хендлеров заглушки
# при установке соединения устаналивается режим и пишется в файл

# отправка: GET с query-параметром
def send_message_as_node(request):
    message = 'sent from APIshka'
    
    register_message(
        content=message,
        received=False,
        datetime=datetime.datetime.now()
    )
    
    OutConnectionSignleton().connection.ws.send(message)

    return JsonResponse({'state': get_server_state()})
    

def send_message_as_master(request):
    channel_layer = get_channel_layer()
    with open('channel_name', 'r') as file:
        channel_name = file.read()
    print('sending to', channel_name)
    async_to_sync(channel_layer.send)(channel_name, {'type': 'chat.message', 'text': 'Hello hrustiki'})
    
    return JsonResponse({'state': get_server_state()})


def message_list(request):
    # читаем состояние приложения, фильтруем

    qs = models.Message.objects.all().order_by('datetime')
    messages = [dict(
        content=m.content,
        received=m.received,
        
    ) for m in qs]
    
    # qs.update(read=True)
    
    # Todo: отправить сообщение о прочитке  
    
    return JsonResponse({'messages': messages})


def clear_history(request):
    models.Message.objects.all().delete()
    
    return JsonResponse({'status': 'ok'})

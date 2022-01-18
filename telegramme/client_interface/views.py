import os
from django.http import JsonResponse
import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from telegramme.outconnections import OutConnectionSignleton
from telegramme.tools import register_message, register_message_sync
from telegramme import models


def get_server_state():
    """Режим сервера - при отсутствии подключения 0, иначе node (первым подключался я), или master (первыми подключались ко мне)"""
    with open('statefile', 'r') as file:
        return file.read()


def current_state(request):
    """Показ режима сервера"""
    return JsonResponse({'state': get_server_state()})


def init_connection(request):
    """Попытка установить соединение, отправка технического сообщения"""
    OutConnectionSignleton().connection.ws.send('init_announcement')
    return JsonResponse({'state': get_server_state()})


def send(request):
    """Отправка сообщений разными путями, в зависимости от режима сервера, регистрация в базе"""

    server_state = get_server_state()
    
    message = request.GET.get('message', None)
    print('msg', message)
    if not message:
        return JsonResponse({'state': get_server_state(), 'status': 'fail', 'error': 'no message'})

    if server_state == 'master':
        channel_layer = get_channel_layer()
        with open('channel_name', 'r') as file:
            channel_name = file.read()
        async_to_sync(channel_layer.send)(channel_name, {'type': 'chat.message', 'text': message})
        return JsonResponse({'state': get_server_state(), 'status': 'ok'})

    elif server_state == 'node':
        register_message_sync(
            content=message,
            received=False,
            datetime=datetime.datetime.now()
        )
        OutConnectionSignleton().connection.ws.send(message)
        return JsonResponse({'state': get_server_state(), 'status': 'ok'})

    else:
        return JsonResponse({'state': get_server_state(), 'status': 'fail', 'error': 'server is not running'})

def message_list(request):
    """Показ списка сообщений"""
    qs = models.Message.objects.all().order_by('datetime')
    messages = [dict(
        content=m.content,
        received=m.received,
        
    ) for m in qs]

    return JsonResponse({'messages': messages})


def clear_history(request):
    """Очистка списка сообщений"""
    
    models.Message.objects.all().delete()
    
    return JsonResponse({'status': 'ok'})

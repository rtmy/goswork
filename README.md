# Telegramme
Система умеет работать как в режиме хоста (master), так в режиме клиента (node).

# Запуск
Требуется развернуть репозиторий дважды на двух "серверах" (это может быть одна машина), которые отличаются "адресами" (адресными портами).
Например, 127.0.0.1:8000 и 127.0.0.1:9000.

## Сервер

Предлагается склонировать репозиторий дважды (в две отдельные папки) и выполнить следующую инструкцию для обеих копий.  
Для создания виртуального окружения  использовать Pipenv или pip (если устанавливается на виртуальную машину).
### 1.a pipenv
``pipenv install``
### 1.b pip
``pip3 install -r requirements.txt``

### 2
Из папки telegramme запустить:
``python3 manage.py runserver <address>``


## Клиент
В каждой из двух папок требуется установить "адрес" собеседника
``python3 client.py``

# Архитектура
Сервера выполняют подключение и обмен сообщениями при помощи веб-сокетов. Обмен административными данными и данными с CLI -- через HTTP.

Код:  
Python3  
Django  
Django Channels
requests


# Оговорки
Сервер по умолчанию запускается в режиме debug, а не в режиме production
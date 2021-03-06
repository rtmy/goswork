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
``python3 manage.py migrate`` -- для создания БД для хранения истории сообщений  
``python3 manage.py runserver <address>``


## Клиент
В каждой из двух папок требуется установить "адрес" собеседника ``SERVER_ADDR`` и вызвать  
``python3 client.py``

# Архитектура
Сервера выполняют подключение и обмен сообщениями при помощи веб-сокетов. Обмен административными данными и данными с CLI -- через HTTP.

Код:  
* Python3  
* Django  
* Django Channels
* websocket-client
* requests
* redis

# Документация
Подробнее описано в комментариях
## telegramme
1. websocket-server, класс хэндлера для работы в качестве мастера - [consumers.py](https://github.com/rtmy/goswork/blob/master/telegramme/telegramme/consumers.py)
2. websocket-client, класс для работы в качестве клиента - [outconnections.py](https://github.com/rtmy/goswork/blob/master/telegramme/telegramme/outconnections.py)
3. Регистрация сообщений - [tools.py](https://github.com/rtmy/goswork/blob/master/telegramme/telegramme/tools.py)
4. Сопоставление методов с адресами (эндпоинты) - [urls.py](https://github.com/rtmy/goswork/blob/master/telegramme/telegramme/urls.py)
## client_interface
Методы инициализации, отправки сообщений - [views.py](https://github.com/rtmy/goswork/blob/master/telegramme/client_interface/views.py)
## client
Единственный файл консольного клиента - [client.py](https://github.com/rtmy/goswork/blob/master/client.py)

# Оговорки
* Для обновления истории (и получения последних сообщений) надо нажать Enter
* Сервер по умолчанию запускается в режиме debug, а не в режиме production
* Аутентификации между серверами и между клиентом и сервером нет, ее можно добавить благодаря поддержке компонентов аутенификации Django в Channels

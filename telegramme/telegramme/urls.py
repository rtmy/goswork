"""telegramme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from client_interface import views as client_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/init/', client_views.init_connection),
    path('chat/state/', client_views.current_state),
    path('chat/list/', client_views.message_list),

    path('chat/send/', client_views.send_message_as_node),
    path('chat/send_message_as_master/', client_views.send_message_as_master),    
    path('chat/clear/', client_views.clear_history),
    # path('messages/', client_views.current_datetime),
]

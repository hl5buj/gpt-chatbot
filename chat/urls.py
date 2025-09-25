from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('send-message/', views.send_message, name='send_message'),
    path('new-conversation/', views.new_conversation, name='new_conversation'),
    path('delete-conversation/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
]
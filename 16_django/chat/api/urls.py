from django.urls import path
from .views import  chat_message, chat_message_streaming
from django.views.generic import TemplateView
urlpatterns = [
    path('chat_message/<str:message>/', chat_message, name='chat_message'),
    path('stream_view/', TemplateView.as_view(template_name="api/chat.html"), name='stream_view'),
    path('stream/<str:message>/', chat_message_streaming, name='generate_llm_stream'),
]
# api/chat_message/안녕하세요.
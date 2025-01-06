from django.urls import path
from . import views   # polls/views.py 모듈 import
app_name = "polls"

# 요청 url - 실행할 view 
## path("url", view함수, name="이 설정이름")
urlpatterns = [
    path("welcome", views.welcome, name="welcome"),
    path("list", views.list, name="list"),
]

# http://127.0.0.1:8000/polls/list
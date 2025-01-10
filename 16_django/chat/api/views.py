from django.http import JsonResponse
from datetime import datetime

from django.views.decorators.http import require_GET
from .llm import Chatting, add_message_to_history

@require_GET
def chat_message(request, message):
    """
    대화를 수행하는 API 엔드포인트.
    path parameter로 사용자의 메시지를 받아서 AI의 응답을 반환한다.
    session을 이용해 대화 기록을 관리한다.
    """
    chat = Chatting()
    history = request.session.get("chatting_history", [])
    
    response = chat.send_message(message, history)


    add_message_to_history(history, ("human", message))
    add_message_to_history(history, ("ai", response))

    request.session["chatting_history"] = history
    return JsonResponse({'response': response})


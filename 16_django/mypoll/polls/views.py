# polls/views.py
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

from polls.models import Question

# welcome page
# View 함수 -> 1개 이상 파라미터선언(HttpRequest객체를 받는 파라미터)
def welcome_old(request):
    print("Welcome 실행")
    # 응답: string
    now = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    res_html = f"""
        <html>
            <head><title>Welcome</title></head>
            <body>
                <h1>환영합니다.</h1>
                <h2>현재시간: {now}</h2>
            </body>
        </html>
    """
    return HttpResponse(res_html)

# template 저장할 디렉토리를 생성 - app/templates
## polls/templates/polls
def welcome(request):
    now = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    # welcome.html 템플릿을 실행한 결과 html을 받아오기.
    res = render(
        request,  # HttpRequest (Http 요청정보를 담은 객체)
        "polls/welcome.html", # 호출할 template파일경로.
        {"current":now, "name":"홍길동"} 
        # context value: view가 template에 전달하는 값들.
    ) #welcome.html의 결과를 가지고 있는 HttpResponse를 반환.  
    print("res type:", type(res))
    return res


# 설문 목록을 응답하는 View
## 전체 Question을 조회해서 목록 html을 반환.
## url:  polls/list
## view함수: list
## template: polls/list.html   # polls/templates/[polls/list.html]
def list(request):
    # DB에서 question들을 조회
    question_list = Question.objects.all().order_by("-pub_date")
    # 질문 목록 template을 호출.
    return render(
        request,
        "polls/list.html",
        {"question_list":question_list}
    )
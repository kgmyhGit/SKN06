# polls/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse # url path설정의 name을 가지고 url을 만들어주는 함수.

from datetime import datetime
from polls.models import Question, Choice

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

# 설문폼 페이지로 이동하는 View
## 설문 문항(문제)의 id(pk)를 받아서 설문폼을 응답.
## 문제 ID를 path parameter로 입력받는다.
##    http://url:port/vote_form?pk=3 => 요청파라미터(QueryString)
##    http://url:port/polls/vote_form/문제번호 => 패스 파라미터
# 요청URL: /polls/voteform
# view: vote_form
# 응답 template: polls/vote_form.html
def vote_form(request, question_id):
    # question_id: path parameter로 문제 id값을 받을 변수
    #  -> urls.py에 path 설정시 지정.

    # 1. question_id로 Question 조회
    question = Question.objects.get(pk=question_id)

    # 2. 조회결과로 응답 페이지를 생성
    return render(
        request, "polls/vote_form.html", {"question":question}
    )
    # print("없는 문제를 조회했습니다. -> error 응답페이지로 이동.")


# 투표 처리
## 요청URL: /polls/vote
## view : vote
## 응답: - 정상 처리: vote_result view를 호출 (redirect방식)
##       - 요청파라미터 검증 실패(선택안하고 투표) -> polls/vote_form.html 

# View 에서 요청파라미터 조회
## GET 요청: request.GET['요청파라미터이름'], request.GET.get("요청파라미터이름")
## POST 요청: request.POST['요청파라미터이름'], request.POST.get("요청파라미터이름")
# []: 요청파라미터이름으로 넘어온게 없으면 Exception 발생
# get: 요청파라미터이름으로 넘어온게 없으면 None 반환.

def vote(request):
    # post 요청파라미터 - name: choice
    choice_id = request.POST.get("choice")
    question_id = request.POST.get("question_id")

    if choice_id is not None:
        # 보기의 votes를 1 증가하도록 update
        choice = Choice.objects.get(pk=choice_id)
        choice.votes += 1
        choice.save()

        # q = Question.objects.get(pk=question_id)
        # return render(
        #     request, "polls/vote_result.html", {"question":q}
        # )

        # 투표결과 페이지로 이동 -> view를 호출
        # url = f"/polls/vote_result/{question_id}" # view의 url
        url = reverse("polls:vote_result", args=[question_id])
        print(url)
        return redirect(url)
        # redirect(url): Redirect 방식 응답. 
        # Web Browser가 지정한 url로  다시 요청하도록 응답. 

    else: # choice요청파라미터가 없는 경우.
        question = Question.objects.get(pk=question_id)
        return render(
            request, 
            "polls/vote_form.html",
            {"question":question, "error_msg":"보기를 선택하세요."}
            
        )


# 투표결과를 응답하는 View
# 요청 url: poll/vote_result/question_id
# view : vote_result
# 응답: polls/vote_result.html

def vote_result(request, question_id):
    question = Question.objects.get(pk=question_id)
    return render(request, 'polls/vote_result.html', {"question":question})


# 설문 등록 처리 View
# 요청 url: /polls/vote_create
# view: vote_create
##     - GET요청: 문제-보기 등록 폼 페이지를 응답
##     - POST요청: 등록 처리.
# 응답 - GET: polls/vote_create.html
#        POST: list view 를 호출 => redirect() 이동(새로고침 해도 추가 되지 않게.)
## HTTP 요청방식을 조회 - request.method: "POST", "GET"
def vote_create(request):
    http_method = request.method
    if http_method == "GET": # 등록폼을 반환
        return render(request, "polls/vote_create.html")

    elif http_method == "POST":# 등록처리
        #1. 요청파라미터(제목, 보기) 읽기.
        question_text = request.POST.get('question_text')
        # 같은이름으로 여러개 값이 넘어온 경우(choice_text=aaa&choice_text=bbb&)
        ## request.GET/POST.getlist('요청파라미터이름'): list
        choice_list = request.POST.getlist("choice_text")

        #2. DB에 저장(insert)
        q = Question(question_text=question_text)
        q.save() # 문제 저장
        for choice_text in choice_list: # 보기들 저장
            choice = Choice(choice_text=choice_text, question=q)
            choice.save()
        
        # 응답 페이지로 이동 - 목록페이지(list)
        # url = "/polls/list"
        # return redirect(url)
        return redirect(reverse("polls:list"))
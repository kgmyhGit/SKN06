from django.shortcuts import render
from .forms import CustomUserCreationForm
# account/views.py

# 사용자 가입 (요청파라미터-CustomUserCreationForm-ModelForm 이용)
## 요청url:  /account/create
###  요청방식: GET - 가입 양식화면을 반환(templates/accout/create.html)
###           POST - 가입처리. 메인페이지로 이동 (templates/home.html)
def create(request):
    if request.method == "GET":
        # 가입 화면을 응답.
        ## 빈 Form객체를 Context Data로 template에 전달.
        return render(
            request, "account/create.html", {"form":CustomUserCreationForm()}
        )
    elif request.method == "POST":
        # 가입처리.
        # 1. 요청파라미터 조회. request.POST.get("name")->Form
        form = CustomUserCreationForm(request.POST, request.FILES)
        # request.POST: post방식으로 넘어온 요청파라미터들
        # request.FILES: 파일업로드시 업로드된 파일 정보.
        ## 객체 생성 -> 요청파라미터들을 attribute로 저장. 검증처리.
        
        # 2. 요청파라미터 검증

        # 3. DB에 저장

        # 4. 응답 - 성공: home.html, 실패(검증): 가입화면으로 이동동
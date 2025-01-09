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
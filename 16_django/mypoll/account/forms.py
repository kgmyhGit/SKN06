# account/forms.py
## Form/ModelForm 클래스들을 정의
##  - 입력 폼당 하나씩 생성. 보통 등록폼, 수정폼 두가지를 만든다.

# Form
# class MyForm(forms.Form)

# ModelForm
# class MyForm(forms.ModelForm)

from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,  # 사용자 등록/생성 폼
    UserChangeForm     # 사용자  정보 수정 폼. 둘다 ModelForm
)
from .models import User

# 사용자 가입(등록)시 사용할 Form을 구성 
#                  - UserCreationForm 상속(username, pwd1, pwd2) + 추가항목
class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User  # User model의 field를 이용해서 form field를 구성
        # fields = "__all__" # 모델의 모든 field들을 사용해서 form field구성
        fields = ["username", "password1", "password2", 
                "name", "email", "birthday"] # form field로 구성할 것들들을 명시.
        # exclude = ["필드명"] # 지정한 필드명을 제외한 나머지 필드드로 form 필드 구성.
        # fields와 exclude는 같이 설정할 수 없다.
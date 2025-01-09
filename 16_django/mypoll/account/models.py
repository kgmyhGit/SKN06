# account/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import forms

## 확장 User 모델 
# - AbstractUser로 구현: 기본 User(username, password)에 필드들을 추가하는 방식
# - AbstractUser 상속. 필드들 정의(username, password빼고 정의)
class User(AbstractUser):
    
    # Field들 정의 - table컬럼
    name = models.CharField(
        verbose_name="이름", # Form관련설정(label) - Form을 ModelForm을 만들 경우 form관련설정을 Model에 한다.
        max_length=50 # varchar(50)
    )
    email = models.EmailField(verbose_name="Email", max_length=100)
    # EmailField: varchar(100) -> 값이 이메일 형식인지(@ 가 있는지)를 검증.
    birthday = models.DateField(
        verbose_name="생일",
        null=True, # Null허용 (default: False - Not Null)
        blank=True # Form - 필수가 아니다.(default: False - required)
    )
    # ModelForm에서 기본 검증을 처리
    ## name: required
    ## email: required, email형식 체크
    ## birthday: 날짜 형식 체크
    
    # 사용자 정의 검증 (Form을 만들경우에는 Form에 작성. ModelForm은 Model에 만들 수 있다.)
    # - clean(), clean_검증필드명()
    ## name은 두 글자 이상 입력
    def clean_name(self):
        # self.cleaned_data: dict - 기본 검증을 통과한 요청파라미터들.
        name = self.cleaned_data['name']
        if len(name) < 2 :
            raise forms.ValidationError("이름은 2글자 이상 입력하세요.")
        return name # 리턴해주는 값이 View가 사용하는 값.
    
    def __str__(self):
        return f"username: {self.username}, name: {self.name}"


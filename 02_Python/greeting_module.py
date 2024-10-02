# 인사말 관련 모듈. => 패키지가 없는 모듈.
__version__ = 1.0

def print_greeting(name):
    print(f"{name}님 안녕하세요.")

def print_welcome(name):
    print(f"{name}님 환영합니다.")

def get_greeting(name):
    return f"{name}님 안녕하세요."

class Hello:

    def __init__(self, name):
        self.name = name

    def kor_greet(self):
        return f"{self.name}님 안녕하세요."

    def eng_greet(self):
         return f"Hello {self.name}~!"

if __name__ == "__main__":
    
    h = Hello("aaa")
    print_greeting()





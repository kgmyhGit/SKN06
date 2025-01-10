from django.apps import AppConfig
from dotenv import load_dotenv
from config.settings import BASE_DIR


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        """
        Callback 메소드로 Django 애플리케이션이 준비되었을 때 호출된다.
        python-dotenv 패키지의 load_dotenv() 함수를 사용하여 .env 파일에서 시스템 환경 변수로 로드한다.
        """
        r = load_dotenv(BASE_DIR / '.env')
        print("OPENAPI KEY Load:", r)
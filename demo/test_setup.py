# 필요한 라이브러리 임포트
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# API 키 확인 (처음 4글자만 출력)
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"✅ API 키 로드 성공: {api_key[:4]}...")
else:
    print("❌ API 키를 찾을 수 없습니다.")
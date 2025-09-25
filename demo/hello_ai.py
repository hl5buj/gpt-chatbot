# 1. 필요한 것들 가져오기
from openai import OpenAI
import os
from dotenv import load_dotenv

# 2. API 키 로드
load_dotenv()

# 3. OpenAI 클라이언트 생성
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 4. AI에게 인사하기
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "미국의 대통령 이름을 말해줘"}
    ]
)

# 5. 응답 출력
print(response.choices[0].message.content)
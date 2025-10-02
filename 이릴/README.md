SnapLink(가안)

외국인 관광객-한국 포토그래퍼 중개 플랫폼

- U1 (관광객) 포토그래퍼 검색, 필터링, 즐겨찾기
- U2 (포토그래퍼)프로필 관리, 인스타그램 인증, 가격 설정
- AI 번역: 실시간 영어-한국어 번역
- 챗봇: 포토그래퍼와의 자동 상담
- 인스타인증 시 포토그래퍼의 인스타 자동 리스트 등재


#설치 및 실행

1. 저장소 클론
```bash
git clone https://github.com/your-username/snaplink-photographer-platform.git
cd snaplink-photographer-platform
```

2. 가상환경 설정
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. 의존성 설치
```bash
pip install -r backend/requirements.txt
```

4. 데이터베이스 초기화
```bash
python backend/seed.py
```

5. 서버 실행
```bash
uvicorn backend.app.main:app --reload --port 8001
```

6. 웹사이트 접속
http://127.0.0.1:8001


로그인 정보

U1 (관광객)
- 이메일: `tourist@example.com`
- 비밀번호: `Pass1234`

U2 (포토그래퍼)
- 이메일: `p1@example.com` / `p2@example.com`
- 비밀번호: `Pass1234`


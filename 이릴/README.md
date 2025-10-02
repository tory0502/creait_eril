# SnapLink - 포토그래퍼 연결 플랫폼

외국인 관광객과 한국 포토그래퍼를 연결하는 AI 기반 플랫폼입니다.

## 🌟 주요 기능

- **U1 (관광객)**: 포토그래퍼 검색, 필터링, 즐겨찾기
- **U2 (포토그래퍼)**: 프로필 관리, 인스타그램 인증, 가격 설정
- **AI 번역**: 실시간 영어-한국어 번역
- **챗봇**: 포토그래퍼와의 자동 상담
- **즐겨찾기**: 마음에 드는 포토그래퍼 저장

## 🚀 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/snaplink-photographer-platform.git
cd snaplink-photographer-platform
```

### 2. 가상환경 설정
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. 의존성 설치
```bash
pip install -r backend/requirements.txt
```

### 4. 데이터베이스 초기화
```bash
python backend/seed.py
```

### 5. 서버 실행
```bash
uvicorn backend.app.main:app --reload --port 8001
```

### 6. 웹사이트 접속
http://127.0.0.1:8001

## 🔑 로그인 정보

### U1 (관광객)
- 이메일: `tourist@example.com`
- 비밀번호: `Pass1234`

### U2 (포토그래퍼)
- 이메일: `p1@example.com` / `p2@example.com`
- 비밀번호: `Pass1234`

## 🤖 AI 기능 설정

OpenAI API 키를 설정하여 번역 기능을 사용할 수 있습니다:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 📱 사용법

1. **로그인** 후 포토그래퍼 목록 확인
2. **필터링**: 도시, 무드, 예산으로 검색
3. **상세보기**: 포토그래퍼 클릭하여 상세 정보 확인
4. **챗봇**: 영어로 질문하면 자동으로 한국어로 번역되어 답변
5. **즐겨찾기**: 하트 버튼으로 마음에 드는 포토그래퍼 저장

## 🛠️ 기술 스택

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: HTML, CSS, JavaScript
- **AI**: OpenAI GPT-3.5-turbo
- **Authentication**: JWT

## 📝 라이선스

MIT License

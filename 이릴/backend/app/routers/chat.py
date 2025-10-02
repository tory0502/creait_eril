from typing import Dict, List
import os
import openai
from fastapi import APIRouter, HTTPException

router = APIRouter()

# OpenAI API 키 설정 (환경변수에서 가져오기)
openai.api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")

@router.post("/translate")
def translate_text(payload: Dict[str, str]):
    text = payload.get("text", "")
    target_lang = payload.get("target", "en")
    
    if not text.strip():
        return {"translated": "", "original": text}
    
    try:
        # OpenAI를 사용한 번역
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": f"Translate the following text to {target_lang}. Only return the translated text, no explanations."
                },
                {"role": "user", "content": text}
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        translated = response.choices[0].message.content.strip()
        return {"translated": translated, "original": text}
        
    except Exception as e:
        # API 키가 없거나 오류 시 기본 번역 (간단한 키워드 매핑)
        return translate_fallback(text, target_lang)

def translate_fallback(text: str, target_lang: str) -> Dict[str, str]:
    """간단한 폴백 번역 (API 키가 없을 때)"""
    translations = {
        "en": {
            "안녕하세요": "Hello",
            "감사합니다": "Thank you",
            "예약": "Reservation",
            "가격": "Price",
            "환불": "Refund",
            "촬영": "Photography",
            "시간": "Time",
            "장소": "Location"
        },
        "ko": {
            "Hello": "안녕하세요",
            "Thank you": "감사합니다",
            "Reservation": "예약",
            "Price": "가격",
            "Refund": "환불",
            "Photography": "촬영",
            "Time": "시간",
            "Location": "장소"
        }
    }
    
    if target_lang in translations:
        for k, v in translations[target_lang].items():
            if k in text:
                text = text.replace(k, v)
    
    return {"translated": f"[{target_lang}] {text}", "original": text}

@router.post("/chat")
def chat_with_photographer(payload: Dict[str, str]):
    """작가와의 채팅 (통역 + 추천)"""
    message = payload.get("message", "")
    photographer_id = payload.get("photographer_id", "")
    user_lang = payload.get("user_lang", "en")
    
    if not message.strip():
        return {"response": "", "translated": ""}
    
    try:
        # 작가 정보에 따른 맞춤 응답 생성
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a helpful assistant for a photographer platform. 
                    Respond to customer inquiries about photography services, pricing, refund policies, 
                    equipment costs, and venue fees. Be friendly and professional.
                    Current language: {user_lang}"""
                },
                {"role": "user", "content": message}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # 필요시 번역
        if user_lang != "en":
            translated = translate_text({"text": response_text, "target": user_lang})
            return {
                "response": response_text,
                "translated": translated["translated"]
            }
        
        return {"response": response_text, "translated": response_text}
        
    except Exception as e:
        return {
            "response": "I'm sorry, I'm having trouble responding right now. Please try again later.",
            "translated": "죄송합니다. 지금 응답에 문제가 있습니다. 나중에 다시 시도해주세요."
        }

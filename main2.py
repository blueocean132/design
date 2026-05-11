import streamlit as st
import requests

# 1. 웹사이트의 기본 설정 (디자인)
st.set_page_config(page_title="실시간 환율 조회기", page_icon="💰", layout="centered")

# --- HTML/CSS 꾸미기 시작 ---
st.markdown("""
    <style>
    /* Streamlit 전체 배경에 워터마크 추가 (가장 확실한 방법) */
    [data-testid="stAppViewContainer"]::before {
        content: '1509송기석';
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 8rem;
        color: rgba(0, 0, 0, 0.1); /* 연한 투명도 */
        z-index: 999999; /* 무조건 맨 앞에 오도록 */
        pointer-events: none; /* 클릭 방해 없음 */
        white-space: nowrap;
        font-weight: bold;
        user-select: none;
    }
    
    /* 배경색과 폰트 설정 */
    .main {
        background-color: #f0f2f6;
    }
    h1 {
        color: #2e4053;
        text-align: center;
        font-family: 'Nanum Gothic', sans-serif;
    }
    .stButton>button {
        width: 100%;
        background-color: #2e86de;
        color: white;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    .result-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 20px;
        position: relative;
    }
    .rate-text {
        color: #e74c3c;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
# --- HTML/CSS 꾸미기 끝 ---

st.title("💰 실시간 국가별 환율 조회")
st.write("한국수출입은행 데이터를 기반으로 실시간 환율을 알려드립니다.")

# 입력창 (HTML 스타일링이 적용됨)
user_input = st.text_input("조회하고 싶은 나라 이름이나 통화 코드를 입력하세요", placeholder="예: 미국, 일본, EUR")

if st.button("조회하기"):
    if user_input:
        api_key = "PSnnFDZjnKZmnYoIN6lwQoH067QBpOIC" # 회원님의 API 키
        url = "https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON"
        params = {"authkey": api_key, "data": "AP01"}
        
        try:
            with st.spinner('데이터를 가져오는 중입니다...'):
                response = requests.get(url, params=params)
                data = response.json()
            
            if not data:
                st.warning("⚠️ 현재 은행 영업시간이 아니거나 데이터를 불러올 수 없습니다. (주말/공휴일 제외)")
            else:
                found = False
                target = user_input.upper()
                
                for item in data:
                    if (target in item.get("cur_unit", "")) or (target in item.get("cur_nm", "")):
                        unit = item.get("cur_

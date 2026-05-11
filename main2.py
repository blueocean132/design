import streamlit as st
import requests
import urllib.parse

# 1. 페이지 기본 설정 (디자인 및 탭 설정)
st.set_page_config(page_title="글로벌 환율 조회", page_icon="💸", layout="centered")

# 2. 확실한 워터마크를 위한 SVG 배경 생성
# 이 방식은 Streamlit의 최상단 배경 자체에 이미지를 입히는 것이라 절대 가려지지 않습니다.
svg_background = """
<svg xmlns='http://www.w3.org/2000/svg' width='100%' height='100%'>
  <text x='50%' y='50%' font-size='100' font-weight='900' fill='rgba(0, 0, 0, 0.06)' text-anchor='middle' dominant-baseline='middle' font-family='sans-serif' transform='rotate(-20, 50%, 50%)'>
    [1509 송기석]
  </text>
</svg>
"""
# SVG를 배경 이미지로 쓸 수 있도록 인코딩
svg_encoded = urllib.parse.quote(svg_background)

# 3. 전체 CSS 스타일링
css = f"""
<style>
/* 전체 배경에 텍스트 워터마크 박아넣기 */
.stApp {{
    background-image: url("data:image/svg+xml;utf8,{svg_encoded}");
    background-color: #f8f9fa;
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* 메인 타이틀 꾸미기 */
.main-title {{
    text-align: center;
    color: #2c3e50;
    font-weight: 900;
    margin-bottom: 5px;
    font-family: 'Malgun Gothic', sans-serif;
}}
.sub-title {{
    text-align: center;
    color: #7f8c8d;
    margin-bottom: 30px;
    font-size: 1.1rem;
}}

/* 결과창 카드 디자인 (반투명 글래스모피즘 효과) */
.result-card {{
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    text-align: center;
    margin-top: 20px;
    border: 1px solid rgba(255, 255, 255, 0.5);
}}
.currency-name {{
    font-size: 1.6rem;
    color: #34495e;
    font-weight: bold;
}}
.exchange-rate {{
    font-size: 2.8rem;
    color: #e74c3c;
    font-weight: 900;
    margin: 15px 0;
}}
.stButton>button {{
    background-color: #3498db;
    color: white;
    font-weight: bold;
    border-radius: 12px;
    height: 3.5rem;
    font-size: 1.2rem;
    border: none;
    transition: 0.3s;
}}
.stButton>button:hover {{
    background-color: #2980b9;
    transform: translateY(-2px);
}}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# 4. 화면 구성
st.markdown("<h1 class='main-title'>💸 글로벌 실시간 환율 조회</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>검색하고자 하는 국가명이나 통화코드(예: USD, 일본, 유럽)를 입력하세요.</p>", unsafe_allow_html=True)

# 검색창
user_input = st.text_input("", placeholder="🔍 국가명 또는 통화코드 입력", label_visibility="collapsed")

# 버튼 및 기능 구현
if st.button("환율 조회하기", use_container_width=True):
    if not user_input:
        st.warning("⚠️ 조회할 국가명이나 통화코드를 입력해주세요.")
    else:
        # API 설정
        api_key = "PSnnFDZjnKZmnYoIN6lwQoH067QBpOIC"
        url = "https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON"
        params = {"authkey": api_key, "data": "AP01"}
        
        with st.spinner("한국수출입은행에서 최신 환율 정보를 가져오고 있습니다..."):
            try:
                # API 호출
                response = requests.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if not data:
                        st.info("💡 현재 은행 영업시간이 아니거나, 오늘 날짜의 데이터가 아직 업데이트되지 않았습니다. (주말/공휴일 제외 평일 11시 이후 조회 권장)")
                    else:
                        search_target = user_input.strip().upper()
                        found = False
                        
                        # 데이터 검색
                        for item in data:
                            cur_nm = item.get("cur_nm", "")
                            cur_unit = item.get("cur_unit", "")
                            
                            if search_target in cur_nm.upper() or search_target in cur_unit.upper():
                                rate = item.get("deal_bas_r")
                                
                                # 예쁜 결과 카드 출력
                                st.markdown(f"""
                                <div class="result-card">
                                    <div class="currency-name">{cur_nm} ({cur_unit})</div>
                                    <div class="exchange-rate">{rate} 원</div>
                                    <div style="color: #7f8c8d; font-size: 1rem;">(매매기준율)</div>
                                </div>
                                """, unsafe_allow_html=True)
                                found = True
                                break
                                
                        if not found:
                            st.error(f"❌ '{user_input}'에 해당하는 국가나 통화를 찾을 수 없습니다.")
                else:
                    st.error("⚠️ API 서버와 통신하는 데 문제가 발생했습니다.")
            except Exception as e:
                st.error(f"⚠️ 데이터를 불러오는 중 오류가 발생했습니다: {e}")

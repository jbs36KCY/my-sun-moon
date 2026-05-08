import streamlit as st
import requests
from xml.etree import ElementTree

# 1. 인증키 설정 (본인 키로 교체하세요)
MY_API_KEY = "9870f159be582ffac2fa2479eaf7819d2ad3fd7771722c1a091456e62a4de87f"

def get_data(loc, date):
    url = "http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getAreaRiseSetInfo"
    params = {'serviceKey': MY_API_KEY, 'locdate': date, 'location': loc}
    
    try:
        response = requests.get(url, params=params)
        root = ElementTree.fromstring(response.text)
        item = root.find(".//item")
        
        if item is not None:
            sr = item.findtext("sunrise")
            ss = item.findtext("sunset")
            mr = item.findtext("moonrise")
            ms = item.findtext("moonset")

            # 1925 -> 19:25 변환 작업
            return {
                "일출": sr[:2] + ":" + sr[2:] if sr else "정보없음",
                "일몰": ss[:2] + ":" + ss[2:] if ss else "정보없음",
                "월출": mr[:2] + ":" + mr[2:] if (mr and len(mr)==4) else "정보없음",
                "월몰": ms[:2] + ":" + ms[2:] if (ms and len(ms)==4) else "정보없음"
            }
    except:
        return None
    return None

# --- 여기부터는 화면에 보여지는 부분입니다 ---
st.set_page_config(page_title="해와 달 대시보드", layout="centered")
st.title("☀️ 해와 달 출몰시간 대시보드")

# 입력창 구성
with st.sidebar:
    st.header("🔍 조회 설정")
    target_date = st.date_input("날짜 선택").strftime("%Y%m%d")
    target_loc = st.text_input("지역명 (예: 익산, 서울)", value="익산")
    btn = st.button("조회하기")

if btn:
    res = get_data(target_loc, target_date)
    
    if res:
        st.success(f"📍 {target_loc} 지역 ({target_date}) 정보")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🌅 일출 시각", res["일출"])
            st.metric("🌇 일몰 시각", res["일몰"])
        with col2:
            st.metric("🌝 월출 시각", res["월출"])
            st.metric("🌚 월몰 시각", res["월몰"])
    else:
        st.error("데이터를 불러오지 못했습니다. 인증키나 지역명을 확인해주세요.")

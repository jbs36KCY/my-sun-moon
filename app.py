import streamlit as st
import requests
import pandas as pd
from xml.etree import ElementTree

# 발급받은 인증키를 여기에 입력
MY_API_KEY = "9870f159be582ffac2fa2479eaf7819d2ad3fd7771722c1a091456e62a4de87f"

def get_data(loc, date):
    url = "http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getAreaRiseSetInfo"
    params = {'serviceKey': '9870f159be582ffac2fa2479eaf7819d2ad3fd7771722c1a091456e62a4de87f', 'locdate': date, 'location': loc}
    try:
        response = requests.get(url, params=params)
        root = ElementTree.fromstring(response.text)
        item = root.find(".//item")
if item is not None:
            # 1. 일단 데이터를 가져옵니다 (예: "1925")
            sr = item.findtext("sunrise")
            ss = item.findtext("sunset")
            mr = item.findtext("moonrise")
            ms = item.findtext("moonset")

            # 2. 글자를 쪼개서 합친 뒤 밖으로 내보냅니다 (예: "19:25")
            return {
                "일출": sr[:2] + ":" + sr[2:] if sr else "정보없음",
                "일몰": ss[:2] + ":" + ss[2:] if ss else "정보없음",
                "월출": (mr[:2] + ":" + mr[2:]) if (mr and len(mr)==4) else "정보없음",
                "월몰": (ms[:2] + ":" + ms[2:]) if (ms and len(ms)==4) else "정보없음"
            }
    except: return None

st.title("☀️ 해와 달 출몰시간 대시보드")
with st.sidebar:
    target_date = st.date_input("날짜 선택").strftime("%Y%m%d")
    target_loc = st.text_input("지역명 (예: 서울, 익산)", value="익산")
    btn = st.button("조회하기")

if btn:
    res = get_data(target_loc, target_date)
    if res:
        st.success(f"{res['지역']} 지역 결과")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🌅 일출", res["일출"])
        c2.metric("🌇 일몰", res["일몰"])
        c3.metric("🌝 월출", res["월출"])
        c4.metric("🌚 월몰", res["월몰"])
    else:
        st.error("데이터를 가져오지 못했습니다. 인증키를 확인하세요.")

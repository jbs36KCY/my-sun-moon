import streamlit as st
import requests
from xml.etree import ElementTree

# 1. 인증키 설정
MY_API_KEY = "9870f159be582ffac2fa2479eaf7819d2ad3fd7771722c1a091456e62a4de87f"

def get_data(loc, date):
    url = "http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getAreaRiseSetInfo"
    params = {'serviceKey': MY_API_KEY, 'locdate': date, 'location': loc}
    
    try:
        response = requests.get(url, params=params)
        # API 응답이 정상인지 확인
        if response.status_code != 200:
            return None
            
        root = ElementTree.fromstring(response.text)
        item = root.find(".//item")
        
        if item is not None:
            # 데이터를 가져오고 앞뒤 공백을 제거(.strip())
            sr = item.findtext("sunrise").strip() if item.findtext("sunrise") else ""
            ss = item.findtext("sunset").strip() if item.findtext("sunset") else ""
            mr = item.findtext("moonrise").strip() if item.findtext("moonrise") else ""
            ms = item.findtext("moonset").strip() if item.findtext("moonset") else ""

            # 시간을 00:00 형태로 바꿔주는 안전한 함수
            def format_time(t):
                if not t or t.strip() == "": return "정보없음"
                # 숫자가 아닌 값이 들어올 경우를 대비
                t = "".join(filter(str.isdigit, t))
                if len(t) < 3: return t
                return t[:-2] + ":" + t[-2:]

            return {
                "일출": format_time(sr),
                "일몰": format_time(ss),
                "월출": format_time(mr),
                "월몰": format_time(ms)
            }
    except Exception as e:
        return None
    return None

# --- 웹 화면 구성 ---
st.set_page_config(page_title="해와 달 대시보드", layout="wide")

st.title("☀️ 해와 달 출몰시간 대시보드")
st.markdown("---")

# 왼쪽 사이드바 설정
with st.sidebar:
    st.header("📍 지역 및 날짜 설정")
    target_loc = st.text_input("지역명을 입력하세요", value="익산")
    target_date = st.date_input("날짜를 선택하세요").strftime("%Y%m%d")
    search_btn = st.button("데이터 불러오기")

# 결과 출력
if search_btn:
    result = get_data(target_loc, target_date)
    
    if result:
        st.success(f"✅ {target_loc} 지역의 {target_date} 데이터입니다.")
        
        # 보기 좋게 4개의 칸으로 나눔
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🌅 일출", result["일출"])
        with col2:
            st.metric("🌇 일몰", result["일몰"])
        with col3:
            st.metric("🌝 월출", result["월출"])
        with col4:
            st.metric("🌚 월몰", result["월몰"])
            
        st.info("※ '정보없음'은 해당 날짜에 달이 뜨거나 지지 않는 천문 현상일 때 나타납니다.")
    else:
        st.error("데이터를 가져오는 데 실패했습니다. 잠시 후 다시 시도하거나 지역명을 확인해 주세요.")
else:
    st.write("측면 메뉴에서 설정을 완료한 후 [데이터 불러오기] 버튼을 눌러주세요.")

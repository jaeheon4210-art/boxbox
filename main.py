import pandas as pd
import plotly.express as px
import streamlit as st

# 1. 페이지 설정 (제목 및 넓은 레이아웃 적용)
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.caption("1년치(365일) 박스오피스 데이터를 바탕으로 시간 흐름에 따른 영화 관객 수 변화를 분석합니다.")

# 2. 데이터 불러오기 및 전처리 (캐싱 처리로 속도 향상)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # '날짜' 열을 YYYYMMDD 형태의 문자열에서 실제 datetime 날짜 타입으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")
    
    # 수치형 데이터가 문자열로 넘어올 수 있으므로 정수(int) 타입으로 캐스팅
    numeric_columns = ["순위", "일관객", "누적관객", "스크린수", "상영횟수"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
        
    return df

# 데이터 로딩
try:
    df = load_data()
except Exception as e:
    st.error(f"❌ 데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

st.divider()

# ==========================================
# 📌 구역 1: 개별 영화의 날짜별 일관객 변화
# ==========================================
st.header("📈 섹션 1. 개별 영화의 날짜별 일관객 변화")

# 1. 영화 선택 드롭다운 (가나다 순 정렬)
movie_list = sorted(df["영화명"].unique())
selected_movie = st.selectbox("조회할 영화를 선택하세요:", movie_list)

# 2. 선택한 영화 데이터 필터링 및 날짜순 정렬
movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

if movie_df.empty:
    st.warning("선택한 영화의 데이터가 없습니다.")
else:
    # 3. 플롯리(Plotly) 선 그래프 생성
    fig = px.line(
        movie_df,
        x="날짜",
        y="일관객",
        title=f"🍿 '{selected_movie}' 일일 관객 수 추이",
        markers=True,  # 데이터 지점에 점 표시
        labels={"날짜": "조회 날짜", "일관객": "일일 관객 수 (명)"}
    )

    # 마우스 호버 시 날짜와 관객 수가 세련되게 보이도록 서식 설정
    fig.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,}명<extra></extra>"
    )

    fig.update_layout(
        xaxis_title="날짜",
        yaxis_title="일일 관객 수 (명)",
        hovermode="x unified",
        xaxis=dict(tickformat="%Y-%m-%d")
    )

    # Streamlit 화면에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

    # 4. 그래프 해석 문구 자리
    st.info(
        "💡 **이 그래프로 알 수 있는 것:** "
        "영화 개봉 초기 관객 집중 현상, 주말과 평일 간의 주기적인 관객 수 변동 폭, "
        "그리고 흥행 유지 기간(관객 감소 속도)을 한눈에 파악할 수 있습니다."
    )

st.divider()

# ==========================================
# 📌 구역 2: 추가 그래프 구역 (향후 확장용)
# ==========================================
st.header("📊 섹션 2. 시간 흐름에 따른 추가 분석 (확장 구역)")
st.caption("새로운 관점의 시간 분석 그래프를 계속해서 추가할 수 있는 영역입니다.")

# 향후 추가될 그래프를 위한 플레이스홀더 용기
with st.container(border=True):
    st.subheader("🚧 다음 그래프 추가 예정 자리")
    st.write("예: 여러 영화의 개봉 후 일차별 누적 관객 수 비교 그래프 등")
    
    # 예시 해석 문구 자리
    st.info(
        "💡 **이 그래프로 알 수 있는 것:** "
        "(새로운 그래프가 추가되면 여기에 해당 그래프의 핵심 분석 결과 한 문장이 들어갑니다.)"
    )

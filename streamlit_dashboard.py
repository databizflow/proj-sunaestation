
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium
import matplotlib.font_manager as fm
import numpy as np
import os

# 한글 폰트 직접 설정
font_path = 'fonts/NotoSansKR-Regular.ttf'

# 폰트 파일이 있는지 확인하고 직접 적용
if os.path.exists(font_path):
    # matplotlib에 폰트 직접 등록
    fm.fontManager.addfont(font_path)
    
    # 폰트 속성 가져오기
    font_prop = fm.FontProperties(fname=font_path)
    
    # matplotlib 전역 설정
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': [font_prop.get_name()],
        'axes.unicode_minus': False
    })
    
    print(f"✅ 한글 폰트 적용 완료: {font_prop.get_name()}")
else:
    print("❌ 폰트 파일을 찾을 수 없습니다:", font_path)

# 페이지 설정
st.set_page_config(page_title="수내역 작업실 매물 대시보드", layout="wide")

# CSS 스타일 추가 - 메트릭 카드 가운데 정렬
st.markdown("""
<style>
.stHorizontalBlock.st-emotion-cache-rra9ig.e1msl4mp2 {
    background-color: rgba(230, 230, 230, 0.2);
    text-align: center !important;
    justify-content: center !important;
    padding:1.8em;
}

.stMetric {
    text-align: center !important;
}

.stMetric > div {
    justify-content: center !important;
}

.stMetric [data-testid="metric-container"] {
    text-align: center !important;
    border: 1px solid #000;
}
</style>
""", unsafe_allow_html=True)

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv("sunae_properties.csv")

df = load_data()



# 서브타이틀에 바탕색과 여백 추가
st.markdown("""
<div style="background-color: #dfdfdf; padding: 25px; border-radius: 15px; margin: 30px 0; border-left: 5px solid #1f77b4;">
   <h2 style="color: #1f77b4; margin: 0; text-align: center;">
        🏢  분당구 작업실 매물 분석 대시보드
    </h3>
</div><br>
""", unsafe_allow_html=True)

# 사이드바
st.sidebar.header("필터 옵션")
selected_dong = st.sidebar.multiselect("동 선택", df["동"].unique(), default=df["동"].unique())
price_range = st.sidebar.slider("㎡당 전세가 범위 (만원)", 
                                int(df["㎡당_전세가"].min()), 
                                int(df["㎡당_전세가"].max()),
                                (int(df["㎡당_전세가"].min()), int(df["㎡당_전세가"].max())))

# 필터링된 데이터
filtered_df = df[(df["동"].isin(selected_dong)) & 
                 (df["㎡당_전세가"] >= price_range[0]) & 
                 (df["㎡당_전세가"] <= price_range[1])]

# 메트릭 카드 (가운데 정렬)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("총 매물 수", len(filtered_df))

with col2:
    st.metric("평균 보증금", f"{filtered_df['보증금'].mean():.0f}만원")

with col3:
    st.metric("평균 월세", f"{filtered_df['월세'].mean():.0f}만원")

with col4:
    st.metric("주차 가능", f"{(filtered_df['주차여부']=='가능').mean()*100:.1f}%")


# 차트 섹션
col1, col2 = st.columns(2)

with col1:
    st.subheader("보증금 분포")
    fig, ax = plt.subplots()
    ax.hist(filtered_df['보증금'], bins=10, edgecolor='#c7c7c7', alpha=0.3)
    ax.set_xlabel('보증금 (만원)')
    ax.set_ylabel('매물 수')
    st.pyplot(fig)

with col2:
    st.subheader("동별 평균 보증금")
    dong_avg = filtered_df.groupby('동')['보증금'].mean()
    
    # 동별 색상 매핑
    dong_colors = {
        '서현동': '#024059',
        '수내동': '#026873', 
        '정자동': '#04BF8A'
    }
    
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = [dong_colors.get(dong, '#666666') for dong in dong_avg.index]
    bars = ax.bar(dong_avg.index, dong_avg.values, color=colors, alpha=0.8)
    
    ax.set_ylabel('평균 보증금 (만원)')
    ax.set_xlabel('동')
    ax.set_title('동별 평균 보증금')
    
    # 막대 위에 값 표시
    for bar, value in zip(bars, dong_avg.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + value*0.01,
               f'{value:,.0f}만원', ha='center', va='bottom', fontweight='bold')
    
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 실용적인 분석 섹션
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="background-color: #dfdfdf; padding: 25px; border-radius: 15px; margin: 30px 0; border-left: 5px solid #1f77b4;">
    <h2 style="color: #1f77b4; margin: 0; text-align: center;">
        💰 실용적인 매물 분석
    </h2>
    <p style="text-align: center; color: #666; margin: 10px 0 0 0; font-size: 14px;">
        작업실을 찾는 분들이 가장 궁금해하는 실용적인 정보들을 분석했습니다
    </p>
</div>
""", unsafe_allow_html=True)

# st.subheader("� 실용적인 매물 분석")  # 이 줄 삭제


# 예산별 매물 개수 분석
st.markdown("<br><br>", unsafe_allow_html=True)
st.subheader("💵 내 예산으로 볼 수 있는 매물은?")
budget_input = st.slider("예산 설정 (보증금, 만원)", 0, int(filtered_df['보증금'].max()), 5000, step=500)
budget_available = filtered_df[filtered_df['보증금'] <= budget_input]
st.info(f"💡 {budget_input:,}만원 예산으로 **{len(budget_available)}개** 매물을 볼 수 있어요!")

col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 style='text-align: center;'>💰 예산대별 매물 분포</h3>", unsafe_allow_html=True)
    budget_ranges = [0, 3000, 5000, 7000, 10000, float('inf')]
    budget_labels = ['3천만원\n이하', '3-5천만원', '5-7천만원', '7천-1억원', '1억원\n이상']
    
    budget_counts = []
    for i in range(len(budget_ranges)-1):
        count = len(filtered_df[(filtered_df['보증금'] > budget_ranges[i]) & 
                               (filtered_df['보증금'] <= budget_ranges[i+1])])
        budget_counts.append(count)
    
    # 0인 항목 제거
    non_zero_data = [(label, count) for label, count in zip(budget_labels, budget_counts) if count > 0]
    
    if non_zero_data:
        labels, counts = zip(*non_zero_data)
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # 도넛 차트 생성
        colors = ['#2E8B57', '#4682B4', '#DAA520', '#CD853F', '#DC143C'][:len(counts)]
        
        # autopct 함수 정의
        def autopct_format(pct):
            absolute = int(pct/100.*sum(counts))
            return f'{absolute}개\n({pct:.1f}%)'
        
        wedges, texts, autotexts = ax.pie(counts, labels=labels, autopct=autopct_format, 
                                         colors=colors, startangle=90, pctdistance=0.85)
        
        # 가운데 원 추가 (도넛 모양)
        centre_circle = plt.Circle((0,0), 0.70, fc='white')
        fig.gca().add_artist(centre_circle)
        
        # 가운데 텍스트 추가
        ax.text(0, 0, f'총 {sum(counts)}개\n매물', ha='center', va='center', 
               fontsize=16, fontweight='bold', color='#333')
        
        ax.set_title('예산대별 매물 분포', fontsize=14, fontweight='bold', pad=20)
        
        # 텍스트 스타일 조정
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        for text in texts:
            text.set_fontsize(11)
            text.set_fontweight('bold')
        
        st.pyplot(fig)
    else:
        st.write("표시할 데이터가 없습니다.")



with col2:
    st.markdown("<h3 style='text-align: center;'>📍 동별 매물 밀집도</h3>", unsafe_allow_html=True)
    dong_counts = filtered_df['동'].value_counts()
    
    if len(dong_counts) > 0:
        # 동별 색상 매핑 (보증금 차트와 동일)
        dong_colors = {
            '서현동': '#024059',
            '수내동': '#026873', 
            '정자동': '#04BF8A'
        }
        
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = [dong_colors.get(dong, '#666666') for dong in dong_counts.index]
        bars = ax.bar(dong_counts.index, dong_counts.values, color=colors, alpha=0.8)
        
        ax.set_ylabel('매물 수')
        ax.set_xlabel('동')
        ax.set_title('동별 매물 분포')
        
        # 막대 위에 숫자 표시
        for bar, count in zip(bars, dong_counts.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                   f'{count}개', ha='center', va='bottom', fontweight='bold')
        
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.write("표시할 데이터가 없습니다.")

# 월세 vs 전세 섹션을 아래로 이동
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>💸 월세 vs 전세 어떤게 나을까?</h3>", unsafe_allow_html=True)

# 월세를 전세로 환산 (월세 * 12개월 * 10년 가정)
monthly_to_jeonse = filtered_df['월세'] * 12 * 10
comparison_df = pd.DataFrame({
    '매물명': filtered_df['매물명'],
    '현재_보증금': filtered_df['보증금'],
    '월세_10년_환산': monthly_to_jeonse,
    '총_비용': filtered_df['보증금'] + monthly_to_jeonse
})

# 상위 5개 매물만 표시
top_5 = comparison_df.nsmallest(5, '총_비용')

fig, ax = plt.subplots(figsize=(12, 6))
x = range(len(top_5))
width = 0.35

ax.bar([i-width/2 for i in x], top_5['현재_보증금'], width, 
       label='보증금', alpha=0.8)
ax.bar([i+width/2 for i in x], top_5['월세_10년_환산'], width, 
       label='월세 10년 환산', alpha=0.8)

ax.set_ylabel('금액 (만원)')
ax.set_title('월세 vs 전세 비용 비교 (10년 기준)')
ax.set_xticks(x)
ax.set_xticklabels([name[:10]+'...' if len(name) > 10 else name 
                   for name in top_5['매물명']], rotation=45)
ax.legend(fontsize=14)

st.pyplot(fig)

# 추천 매물 섹션
st.markdown("<br><br>", unsafe_allow_html=True)
st.subheader("🎯 맞춤 추천 매물")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("**💰 가성비 최고**")
    if len(filtered_df) > 0:
        cheapest = filtered_df.nsmallest(3, '㎡당_전세가')[['매물명', '보증금', '월세', '면적']]
        for idx, row in cheapest.iterrows():
            st.write(f"• {row['매물명'][:20]}")
            st.write(f"  보증금 {row['보증금']:,}만원, 월세 {row['월세']}만원")

with col2:
    st.write("**🚗 주차 가능**")
    parking_available = filtered_df[filtered_df['주차여부'] == '가능'].nsmallest(3, '보증금')
    for idx, row in parking_available.iterrows():
        st.write(f"• {row['매물명'][:20]}")
        st.write(f"  보증금 {row['보증금']:,}만원, 월세 {row['월세']}만원")

with col3:
    st.write("**📏 넓은 공간**")
    spacious = filtered_df.nlargest(3, '면적')[['매물명', '보증금', '월세', '면적']]
    for idx, row in spacious.iterrows():
        st.write(f"• {row['매물명'][:20]}")
        st.write(f"  {row['면적']}㎡, 보증금 {row['보증금']:,}만원")

# 지도 섹션
st.markdown("<br><br>", unsafe_allow_html=True)
st.subheader("🗺️ 매물 위치 지도")
if len(filtered_df) > 0:
    map_center = folium.Map(location=[37.3838, 127.1240], zoom_start=15)

    for idx, row in filtered_df.iterrows():
        color = 'green' if row['㎡당_전세가'] < 1500 else 'orange' if row['㎡당_전세가'] < 1700 else 'red'
        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=f"{row['매물명']}<br>보증금: {row['보증금']:,}만원<br>월세: {row['월세']}만원",
            icon=folium.Icon(color=color)
        ).add_to(map_center)

    st_folium(map_center, width=600, height=600)

# 데이터 테이블
st.markdown("<br><br>", unsafe_allow_html=True)
st.subheader("📋 상세 매물 정보")
st.dataframe(filtered_df[['매물명', '동', '면적', '보증금', '월세', '주차여부', 'URL']])

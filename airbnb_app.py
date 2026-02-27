import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px
import koreanize_matplotlib
import matplotlib.pyplot as plt
import re

# 페이지 설정
st.set_page_config(page_title="서울 Airbnb 데이터 분석 대시보드", layout="wide")

def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'airbnb_scraping_seoul.db')
    
    if not os.path.exists(db_path):
        st.error(f"데이터베이스 파일을 찾을 수 없습니다: {db_path}")
        return pd.DataFrame()
        
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM stays", conn)
    conn.close()
    
    # 데이터 전처리: 가격 정보를 숫자로 변환
    def clean_price(price_str):
        if pd.isna(price_str):
            return 0
        # 숫자만 추출
        digits = re.sub(r'[^0-9]', '', str(price_str))
        return int(digits) if digits else 0
        
    df['price_numeric'] = df['price'].apply(clean_price)
    
    # 평점 전처리 (예: "4.74 (247)" -> 4.74)
    def clean_rating(rating_str):
        if pd.isna(rating_str) or not rating_str:
            return 0.0
        match = re.search(r'([0-9.]+)', str(rating_str))
        return float(match.group(1)) if match else 0.0
        
    df['rating_numeric'] = df['avg_rating'].apply(clean_rating)
    
    return df

st.title("🏙️ 서울 Airbnb 숙소 분석 대시보드")
st.markdown("수집된 데이터를 바탕으로 서울 지역의 Airbnb 숙소 현황을 분석합니다.")

df = load_data()

if not df.empty:
    # 사이드바 필터
    st.sidebar.header("🔍 필터 설정")
    price_range = st.sidebar.slider(
        "가격 범위 (₩)",
        min_value=int(df['price_numeric'].min()),
        max_value=int(df['price_numeric'].max()),
        value=(int(df['price_numeric'].min()), int(df['price_numeric'].max()))
    )
    
    rating_filter = st.sidebar.slider(
        "최소 평점",
        min_value=0.0,
        max_value=5.0,
        value=0.0,
        step=0.1
    )
    
    search_query = st.sidebar.text_input("숙소 이름 검색", "")

    # 데이터 필터링
    filtered_df = df[
        (df['price_numeric'] >= price_range[0]) & 
        (df['price_numeric'] <= price_range[1]) &
        (df['rating_numeric'] >= rating_filter)
    ]
    
    if search_query:
        filtered_df = filtered_df[filtered_df['subtitle'].str.contains(search_query, case=False, na=False) | 
                                filtered_df['title'].str.contains(search_query, case=False, na=False)]

    # 주요 지표 상단 배치
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("총 숙소 수", f"{len(filtered_df)}개")
    with col2:
        st.metric("평균 가격", f"₩{int(filtered_df['price_numeric'].mean()):,}")
    with col3:
        st.metric("평균 평점", f"{filtered_df['rating_numeric'].mean():.2f} / 5.0")

    st.divider()

    # 시각화 영역
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("💰 가격 분포")
        fig_price = px.histogram(filtered_df, x="price_numeric", nbins=30, labels={'price_numeric': '가격 (₩)'}, 
                               title="숙소 가격 분포 히스토그램", color_discrete_sequence=['#FF5A5F'])
        st.plotly_chart(fig_price, use_container_width=True)
        
    with col_right:
        st.subheader("⭐ 평점 분포")
        fig_rating = px.box(filtered_df, y="rating_numeric", labels={'rating_numeric': '평점'}, 
                          title="숙소 평점 분포 (Box Plot)", color_discrete_sequence=['#00A699'])
        st.plotly_chart(fig_rating, use_container_width=True)

    st.divider()

    st.subheader("📋 숙소 목록")
    st.dataframe(filtered_df[['title', 'subtitle', 'avg_rating', 'price', 'total_price_label']], use_container_width=True)

else:
    st.warning("분석할 데이터가 없습니다. 먼저 수집을 진행해 주세요.")

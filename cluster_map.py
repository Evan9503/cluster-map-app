import streamlit as st
import folium
import pandas as pd
import random
import os
from streamlit_folium import folium_static

# Streamlit UI 설정
st.title("📍 클러스터링 지도 시각화")
st.write("Excel 파일을 업로드하면 클러스터링된 데이터를 지도에서 확인할 수 있습니다.")

# 파일 업로드 위젯
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요 (xlsx 형식)", type=["xlsx"])

if uploaded_file:
    # 데이터 로드
    df = pd.read_excel(uploaded_file, sheet_name='result')
    st.success("데이터 로드 완료!")

    # 지도 초기화 (중심점은 데이터의 평균 좌표 사용)
    map_center = [df['lat'].mean(), df['lng'].mean()]
    m = folium.Map(location=map_center, zoom_start=12)

    # cluster_id별 색상 매핑
    cluster_ids = df['cluster_id'].unique()
    color_map = {cluster: "#6495ED" if 'B' in cluster else f"#{random.randint(0, 0xFFFFFF):06x}" for cluster in cluster_ids}

    # 마커 추가
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lng']],
            radius=5,
            color=color_map[row['cluster_id']],
            fill=True,
            fill_color=color_map[row['cluster_id']],
            fill_opacity=0.6,
            popup=f"Cluster: {row['cluster_no']}\nCluster ID: {row['cluster_id']}\nLat: {row['lat']}\nLng: {row['lng']}"
        ).add_to(m)

    # Folium 지도 렌더링
    folium_static(m)
    st.success("📍 지도 생성 완료! 아래에서 확인하세요.")

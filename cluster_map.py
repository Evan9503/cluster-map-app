import folium
import pandas as pd
import random
from tkinter import filedialog
import os

# GUI를 사용하여 파일 선택 창 열기
def select_file():
    root = tk.Tk()
    root.withdraw()  # GUI 창을 숨김
    file_path = filedialog.askopenfilename(
        title="클러스터링 엑셀 파일 선택", 
        filetypes=[("Excel Files", "*.xlsx")]
    )
    return file_path

# 단계 1: 사용자에게 파일 업로드 요청
print("[1/4] 파일을 선택하세요...")
file_path = select_file()
if not file_path:
    print("파일을 선택하지 않았습니다. 프로그램을 종료합니다.")
    exit()

print(f"[1/4] 데이터 로드 중... ({file_path})")
df = pd.read_excel(file_path, sheet_name='result')
print("[1/4] 데이터 로드 완료!")

# 단계 2: 지도 초기화 (중심점은 데이터의 평균 좌표 사용)
print("[2/4] 지도 초기화 중...")
map_center = [df['lat'].mean(), df['lng'].mean()]
m = folium.Map(location=map_center, zoom_start=12)
print("[2/4] 지도 초기화 완료!")

# cluster_id별 색상 매핑을 위한 컬러 리스트 생성
cluster_ids = df['cluster_id'].unique()
color_map = {}

for cluster in cluster_ids:
    if 'B' in cluster:
        color_map[cluster] = "#6495ED"  # 연한 파란색 (Cornflower Blue)
    else:
        color_map[cluster] = f"#{random.randint(0, 0xFFFFFF):06x}"  # 랜덤 색상

# 단계 3: 마커 추가 (군집화 제거 및 cluster_id별 색상 적용)
print("[3/4] 지도에 마커 추가 중...")
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lng']],
        radius=5,  # 마커 크기
        color=color_map[row['cluster_id']],
        fill=True,
        fill_color=color_map[row['cluster_id']],
        fill_opacity=0.6,
        popup=f"Cluster: {row['cluster_no']}\nCluster ID: {row['cluster_id']}\nLat: {row['lat']}\nLng: {row['lng']}"
    ).add_to(m)
print("[3/4] 마커 추가 완료!")

# 단계 4: 지도 저장 (업로드된 파일과 같은 폴더에 저장)
output_path = os.path.join(os.path.dirname(file_path), "cluster_map.html")
print("[4/4] 지도 저장 중...")
m.save(output_path)
print(f"[4/4] 지도 저장 완료! 파일 위치: {output_path}")

# EXE 파일로 변환할 때 GUI 창이 유지되도록 추가
print("업로드된 파일과 동일한 폴더에 cluster_map.html이 저장되었습니다. 파일을 열어보세요!")
input("Enter 키를 누르면 종료됩니다...")

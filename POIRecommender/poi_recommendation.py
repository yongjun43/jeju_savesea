# 3. 사용자 위치 정의
user_location = (33.540855, 126.690195)
print(f"\n사용자 위치: {user_location}")


cleaning_zones = pd.read_csv('/content/locations.csv')
recycling_centers = pd.read_csv('/content/recycling.csv')

# 4. 거리 계산 함수 정의
def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).kilometers

# 5. 가장 가까운 청소구역 찾기
if 'cleaning_zones' in locals():
    cleaning_zones['distance_to_user'] = cleaning_zones.apply(
        lambda row: calculate_distance(user_location, (row['latitude'], row['longitude'])), axis=1
    )
    
    nearest_cleaning_zone = cleaning_zones.loc[cleaning_zones['distance_to_user'].idxmin()]
    print("\n가장 가까운 청소구역:")
    print(nearest_cleaning_zone)
else:
    print("청소구역 데이터가 로드되지 않았습니다.")

# 6. 가장 가까운 재활용장 찾기
if 'nearest_cleaning_zone' in locals() and 'recycling_centers' in locals():
    nearest_cleaning_location = (nearest_cleaning_zone['latitude'], nearest_cleaning_zone['longitude'])
    print(f"\n가장 가까운 청소구역 위치: {nearest_cleaning_location}")
    
    recycling_centers['distance_to_cleaning'] = recycling_centers.apply(
        lambda row: calculate_distance(nearest_cleaning_location, (row['latitude'], row['longitude'])), axis=1
    )
    
    nearest_recycling_center = recycling_centers.loc[recycling_centers['distance_to_cleaning'].idxmin()]
    print("\n가장 가까운 재활용장:")
    print(nearest_recycling_center)
else:
    print("재활용장 데이터가 로드되지 않았거나 가장 가까운 청소구역을 찾지 못했습니다.")

# 7. 추천 결과 시각화
if 'nearest_cleaning_zone' in locals() and 'nearest_recycling_center' in locals():
    # 지도 생성 (사용자의 위치를 중심으로)
    map_center = user_location
    m = folium.Map(location=map_center, zoom_start=14)
    
    # 마커 클러스터 추가
    marker_cluster = MarkerCluster().add_to(m)
    
    # 사용자 위치 마커
    folium.Marker(
        location=user_location,
        popup='사용자 위치',
        icon=folium.Icon(color='blue', icon='user')
    ).add_to(marker_cluster)
    
    # 가장 가까운 청소구역 마커
    folium.Marker(
        location=nearest_cleaning_location,
        popup=f"가장 가까운 청소구역: {nearest_cleaning_zone['name']}",
        icon=folium.Icon(color='green', icon='trash')
    ).add_to(marker_cluster)
    
    # 가장 가까운 재활용장 마커
    folium.Marker(
        location=(nearest_recycling_center['latitude'], nearest_recycling_center['longitude']),
        popup=f"가장 가까운 재활용장: {nearest_recycling_center['name']}",
        icon=folium.Icon(color='red', icon='recycle')
    ).add_to(marker_cluster)
    
    # 사용자 위치에서 청소구역까지 선 그리기
    folium.PolyLine(
        locations=[user_location, nearest_cleaning_location],
        color='blue',
        weight=2.5,
        opacity=1
    ).add_to(m)
    
    # 청소구역에서 재활용장까지 선 그리기
    folium.PolyLine(
        locations=[nearest_cleaning_location, (nearest_recycling_center['latitude'], nearest_recycling_center['longitude'])],
        color='purple',
        weight=2.5,
        opacity=1
    ).add_to(m)
    
    # 지도 출력
m

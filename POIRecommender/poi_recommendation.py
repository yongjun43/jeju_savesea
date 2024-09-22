# 4. 거리 계산 함수 정의
def calculate_distance(coord1, coord2):
    """
    두 지점 간의 거리 (킬로미터)를 계산합니다.
    
    Parameters:
    coord1 (tuple): 첫 번째 지점의 위도와 경도 (latitude, longitude)
    coord2 (tuple): 두 번째 지점의 위도와 경도 (latitude, longitude)
    
    Returns:
    float: 두 지점 간의 거리 (킬로미터)
    """
    return geodesic(coord1, coord2).kilometers

# 5. 가장 가까운 청소구역 찾기
if 'cleaning_zones' in locals() and not cleaning_zones.empty:
    cleaning_zones['distance_to_user'] = cleaning_zones.apply(
        lambda row: calculate_distance(user_location, (row['latitude'], row['longitude'])), axis=1
    )
    
    nearest_cleaning_zone = cleaning_zones.loc[cleaning_zones['distance_to_user'].idxmin()]
    print("\n가장 가까운 청소구역:")
    print(nearest_cleaning_zone)
else:
    print("청소구역 데이터가 로드되지 않았거나 비어 있습니다.")

# 6. 가장 가까운 재활용장 찾기
if 'nearest_cleaning_zone' in locals() and 'recycling_centers' in locals() and not recycling_centers.empty:
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
    nearest_cleaning_location = (nearest_cleaning_zone['latitude'], nearest_cleaning_zone['longitude'])
    nearest_recycling_location = (nearest_recycling_center['latitude'], nearest_recycling_center['longitude'])
    
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
        location=nearest_recycling_location,
        popup=f"가장 가까운 재활용장: {nearest_recycling_center['name']}",
        icon=folium.Icon(color='red', icon='recycle')
    ).add_to(marker_cluster)
    
    # 사용자 위치에서 청소구역까지 선 그리기 (화살표 포함)
    folium.PolyLine(
        locations=[user_location, nearest_cleaning_location],
        color='blue',
        weight=2.5,
        opacity=1
    ).add_to(m)
    
    # 청소구역에서 재활용장까지 선 그리기 (화살표 포함)
    folium.PolyLine(
        locations=[nearest_cleaning_location, nearest_recycling_location],
        color='purple',
        weight=2.5,
        opacity=1
    ).add_to(m)
    
    # 화살표 추가를 위한 추가적인 방법: PolyLineTextPath 사용
    from folium.plugins import PolyLineTextPath
    from branca.element import Template, MacroElement

    # 사용자 위치에서 청소구역까지 화살표 추가
    polyline1 = folium.PolyLine(
        locations=[user_location, nearest_cleaning_location],
        color='blue',
        weight=2.5,
        opacity=1
    ).add_to(m)
    
    text_path1 = PolyLineTextPath(
        polyline1,
        '➤',
        repeat=True,
        offset=7,
        attributes={
            "fill": "blue",
            "font-weight": "bold",
            "font-size": "12"
        }
    )
    polyline1.add_child(text_path1)
    
    # 청소구역에서 재활용장까지 화살표 추가
    polyline2 = folium.PolyLine(
        locations=[nearest_cleaning_location, nearest_recycling_location],
        color='purple',
        weight=2.5,
        opacity=1
    ).add_to(m)
    
    text_path2 = PolyLineTextPath(
        polyline2,
        '➤',
        repeat=True,
        offset=7,
        attributes={
            "fill": "purple",
            "font-weight": "bold",
            "font-size": "12"
        }
    )
    polyline2.add_child(text_path2)
    
    # 지도 출력
    display(m)

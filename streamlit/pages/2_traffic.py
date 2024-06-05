import streamlit as st
from config.loader import config
import requests
import folium
from streamlit_folium import st_folium

st.title("Route Map")


if 'city_selection' not in st.session_state:
    st.session_state.city_selection = set()


inp = st.text_input("type the number of the cities you want to search for")
if inp:
    number = int(inp)

    for i in range(number):
        a = st.selectbox(f"Select city {i + 1}", config["cities"].keys(), index=None, key=f"city_{i}")
        if a:
            st.session_state.city_selection.add(a)

    if st.button("Search"):
        selected_cities = st.session_state.city_selection
        body = {"coordinates": [[config[city]["long"], config[city]["lat"]] for city in selected_cities]}
        response = requests.post(config["traffic"]["endpoint"], data=body,
                                 headers={"Authorization": config["traffic"]["api_key"]})
        if response.status_code == 200:
            api_response = response.json()
            route_geometry = api_response['routes'][0]['geometry']
            route_bbox = api_response['routes'][0]['bbox']
            route_segments = api_response['routes'][0]['segments']

            def decode_polyline(polyline_str):
                index, lat, lng, coordinates = 0, 0, 0, []
                changes = {'lat': 0, 'lng': 0}

                while index < len(polyline_str):
                    for key in changes.keys():
                        shift, result = 0, 0

                        while True:
                            byte = ord(polyline_str[index]) - 63
                            index += 1
                            result |= (byte & 0x1f) << shift
                            shift += 5
                            if not byte >= 0x20:
                                break

                        changes[key] = ~(result >> 1) if result & 1 else result >> 1

                    lat += changes['lat']
                    lng += changes['lng']
                    coordinates.append((lat / 1E5, lng / 1E5))

                return coordinates

            route_coords = decode_polyline(route_geometry)

            m = folium.Map(location=[(route_bbox[1] + route_bbox[3]) / 2, (route_bbox[0] + route_bbox[2]) / 2], zoom_start=14)

            folium.PolyLine(route_coords, color='blue', weight=5, opacity=0.7).add_to(m)

            for segment in route_segments:
                for step in segment['steps']:
                    start_point = route_coords[step['way_points'][0]]
                    folium.Marker(
                        location=start_point,
                        popup=step['instruction'],
                        icon=folium.Icon(color='green' if step['way_points'][0] == 0 else 'red' if step['way_points'][1] == len(route_coords) - 1 else 'blue')
                    ).add_to(m)

            st_folium(m, width=700, height=500)

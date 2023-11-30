import streamlit as st
from google.transit import gtfs_realtime_pb2
import requests
import pandas as pd
import time
import pydeck as pdk

def parse_gtfs_rt_data(data):
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(data)
    return feed

# Function to extract latitude and longitude from vehicle positions
def get_vehicle_positions(feed):
    positions = []
    for entity in feed.entity:
        if entity.HasField('vehicle'):
            position = entity.vehicle.position
            positions.append((position.latitude, position.longitude))
    return positions

# Sidebar for URL input
st.sidebar.title('GTFS-RT Data Visualization')
url = 'https://gtfs-rt.itsmarta.com/TMGTFSRealTimeWebService/vehicle/vehiclepositions.pb'

if url:
    st.subheader('Vehicle Positions on Map')

    # Use st.pydeck_chart() to create the initial map
    empty_map = st.pydeck_chart()

    while True:
        response = requests.get(url)
        if response.status_code == 200:
            gtfs_rt_feed = parse_gtfs_rt_data(response.content)
            vehicle_positions = get_vehicle_positions(gtfs_rt_feed)
            df = pd.DataFrame(vehicle_positions, columns=['LAT', 'LON'])

            # Use Pydeck to create a new map layer with updated data
            new_layer = pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[LON, LAT]',
                get_radius=100,
                get_fill_color=[255, 0, 0],
                pickable=True,
                auto_highlight=True,
            )

            # Update the map by replacing the initial empty map with the new layer
            empty_map.pydeck_chart(pdk.Deck(layers=[new_layer]))
        else:
            st.error("Failed to fetch GTFS-RT data. Please check the URL.")
            break

        # Wait for 1 second before updating again
        time.sleep(1)
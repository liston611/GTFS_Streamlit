import streamlit as st
from google.transit import gtfs_realtime_pb2
import requests
import pandas as pd

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
    # Fetch GTFS-RT data from URL
    response = requests.get(url)
    if response.status_code == 200:
        st.subheader('Vehicle Positions on Map')
        gtfs_rt_feed = parse_gtfs_rt_data(response.content)
        
        # Get vehicle positions
        vehicle_positions = get_vehicle_positions(gtfs_rt_feed)
        
        # Create DataFrame with 'LAT' and 'LON' columns
        df = pd.DataFrame(vehicle_positions, columns=['LAT', 'LON'])
        
        # Display vehicle positions on map
        st.map(df)
    else:
        st.error("Failed to fetch GTFS-RT data. Please check the URL.")

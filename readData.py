import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px

# Simulated sensor data function
def read_sensors():
    return {
        "Voltage": np.random.uniform(210, 250),  # Simulated voltage
        "Current": np.random.uniform(5, 20),     # Simulated current
        "Temperature": np.random.uniform(20, 80),  # Simulated temperature
        "Vibration": np.random.uniform(0.1, 5)   # Simulated vibration
    }

# Thresholds for alerts
VOLTAGE_RANGE = (220, 240)
CURRENT_RANGE = (8, 18)
TEMP_LIMIT = 70
VIBRATION_LIMIT = 3.5

# Streamlit UI
st.title("🏭 Industry Protection Monitoring Dashboard")
st.markdown("### Real-Time Sensor Data")

# Initialize data storage
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Time", "Voltage", "Current", "Temperature", "Vibration"])

placeholder = st.empty()

while True:
    # Read data
    sensor_data = read_sensors()
    timestamp = pd.Timestamp.now()
    
    # Append new data
    new_data = pd.DataFrame([{**sensor_data, "Time": timestamp}])
    st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
    
    # Keep only last 100 readings for performance
    st.session_state.data = st.session_state.data.tail(100)
    
    # Display real-time values
    with placeholder.container():
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Voltage (V)", f"{sensor_data['Voltage']:.2f}", "⚡" if not VOLTAGE_RANGE[0] <= sensor_data['Voltage'] <= VOLTAGE_RANGE[1] else "✅")
        col2.metric("Current (A)", f"{sensor_data['Current']:.2f}", "⚠️" if not CURRENT_RANGE[0] <= sensor_data['Current'] <= CURRENT_RANGE[1] else "✅")
        col3.metric("Temperature (°C)", f"{sensor_data['Temperature']:.2f}", "🔥" if sensor_data['Temperature'] > TEMP_LIMIT else "✅")
        col4.metric("Vibration (m/s²)", f"{sensor_data['Vibration']:.2f}", "🔴" if sensor_data['Vibration'] > VIBRATION_LIMIT else "✅")
    
    # Graphs
    st.markdown("### Live Sensor Data Trends")
    fig = px.line(st.session_state.data, x="Time", y=["Voltage", "Current", "Temperature", "Vibration"], title="Sensor Data Over Time")
    st.plotly_chart(fig, use_container_width=True)
    
    time.sleep(2)  # Refresh every 2 seconds

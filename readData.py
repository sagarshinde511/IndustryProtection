import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import time

# Database configuration
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students1",
    "password": "testStudents@123",
    "database": "u263681140_students1",
}

# Function to fetch last 50 entries from MySQL with caching
@st.cache_data(ttl=5)  # Cache results for 5 seconds
def fetch_data():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM IndustryProtection ORDER BY dateTime DESC LIMIT 50")
        data = cursor.fetchall()
        conn.close()
        return pd.DataFrame(data)
    except mysql.connector.Error as e:
        st.error(f"Database Connection Error: {e}")
        return pd.DataFrame()

# Streamlit UI
st.title("🏭 Industry Protection Monitoring Dashboard")
st.markdown("### Real-Time Sensor Data from MySQL")

# Placeholder containers for dynamic updates
placeholder = st.empty()
graph_placeholder = st.empty()  # Create a graph container

# Define alert thresholds
VOLTAGE_RANGE = (220, 240)
CURRENT_RANGE = (8, 18)
TEMP_LIMIT = 70
VIBRATION_LIMIT = 3.5

# Fetch data
df = fetch_data()

if not df.empty:
    df["dateTime"] = pd.to_datetime(df["dateTime"])  # Convert to datetime

    # Display real-time values
    latest_data = df.iloc[0]
    
    with placeholder.container():
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Voltage (V)", f"{latest_data['Voltage']}", "⚡" if not VOLTAGE_RANGE[0] <= float(latest_data['Voltage']) <= VOLTAGE_RANGE[1] else "✅")
        col2.metric("Current (A)", f"{latest_data['Current']}", "⚠️" if not CURRENT_RANGE[0] <= float(latest_data['Current']) <= CURRENT_RANGE[1] else "✅")
        col3.metric("Temperature (°C)", f"{latest_data['Temp']}", "🔥" if float(latest_data['Temp']) > TEMP_LIMIT else "✅")
        col4.metric("Vibration (m/s²)", f"{latest_data['Vibration']}", "🔴" if float(latest_data['Vibration']) > VIBRATION_LIMIT else "✅")

# Button to plot graph
if st.button("Show Graph"):
    fig = px.line(df.sort_values("dateTime"), x="dateTime", y=["Voltage", "Current", "Temp", "Vibration"], 
                  title="Last 50 Sensor Data Entries")
    graph_placeholder.plotly_chart(fig, use_container_width=True)

# Auto-refresh every 5 seconds
time.sleep(5)
st.experimental_rerun()

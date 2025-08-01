import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import base64
from io import BytesIO
import time
import pandas as pd

from weather_api import WeatherAPI
from location_detector import LocationDetector
from ui_components import UIComponents
from data_processor import DataProcessor

# Page configuration
st.set_page_config(
    page_title="Climatrack • Real-time Weather Intelligence",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import os
st.write("📂 CWD:", os.getcwd())
st.write("📄 Secrets file exists:", os.path.exists(".streamlit/secrets.toml"))
st.write("🔑 API Key loaded:", st.secrets.get("OPENWEATHER_API_KEY", "❌ Not Found"))

class WeatherApp:
    def __init__(self):
        self.weather_api = WeatherAPI()
        self.location_detector = LocationDetector()
        self.ui = UIComponents()
        self.data_processor = DataProcessor()
        
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'location_data' not in st.session_state:
            st.session_state.location_data = None
        if 'weather_data' not in st.session_state:
            st.session_state.weather_data = None
        if 'forecast_data' not in st.session_state:
            st.session_state.forecast_data = None
        if 'last_update' not in st.session_state:
            st.session_state.last_update = None
        if 'theme_mode' not in st.session_state:
            st.session_state.theme_mode = 'dark'
        if 'units' not in st.session_state:
            st.session_state.units = 'metric'
            
    def load_custom_css(self):
        """Load custom CSS for the application"""
        self.ui.load_custom_css()
        
    def detect_location(self):
        """Detect user location"""
        with st.spinner("🌍 Detecting your location..."):
            location_data = self.location_detector.get_location()
            if location_data:
                st.session_state.location_data = location_data
                return True
            return False
            
    def fetch_weather_data(self, lat, lon):
        """Fetch weather data for given coordinates"""
        with st.spinner("☁️ Fetching weather data..."):
            # Current weather
            current_weather = self.weather_api.get_current_weather(lat, lon, st.session_state.units)
            if current_weather:
                st.session_state.weather_data = current_weather
                
            # 5-day forecast
            forecast = self.weather_api.get_forecast(lat, lon, st.session_state.units)
            if forecast:
                st.session_state.forecast_data = forecast
                
            st.session_state.last_update = datetime.now()
            return current_weather and forecast
            
    def render_header(self):
        """Render the application header"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
                <div class="main-header">
                    <h1>🌤️ Climatrack</h1>
                    <p>Real-time Weather Intelligence</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            # Theme toggle and settings
            if st.button("⚙️", help="Settings", key="settings_btn"):
                self.show_settings_modal()
                
    def show_settings_modal(self):
        """Show settings modal"""
        with st.expander("⚙️ Settings", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                new_units = st.selectbox(
                    "Temperature Units",
                    ["metric", "imperial", "kelvin"],
                    index=["metric", "imperial", "kelvin"].index(st.session_state.units),
                    format_func=lambda x: {"metric": "Celsius (°C)", "imperial": "Fahrenheit (°F)", "kelvin": "Kelvin (K)"}[x]
                )
                
                if new_units != st.session_state.units:
                    st.session_state.units = new_units
                    if st.session_state.location_data:
                        self.fetch_weather_data(
                            st.session_state.location_data['lat'],
                            st.session_state.location_data['lon']
                        )
                        st.rerun()
                        
            with col2:
                if st.button("🔄 Refresh Data", key="refresh_btn"):
                    if st.session_state.location_data:
                        self.fetch_weather_data(
                            st.session_state.location_data['lat'],
                            st.session_state.location_data['lon']
                        )
                        st.rerun()
    
    def render_location_search(self):
        """Render location search interface"""
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "",
                placeholder="🔍 Search for a city... (e.g., New York, London, Tokyo)",
                key="location_search",
                label_visibility="collapsed"
            )
            
        with col2:
            search_clicked = st.button("Search", key="search_btn", use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Auto-detect location button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📍 Auto-detect my location", key="auto_detect", use_container_width=True):
                if self.detect_location():
                    lat, lon = st.session_state.location_data['lat'], st.session_state.location_data['lon']
                    if self.fetch_weather_data(lat, lon):
                        st.rerun()
                else:
                    st.error("❌ Could not detect your location. Please search manually.")
                    
        # Handle manual search
        if search_clicked and search_query:
            location_data = self.location_detector.search_location(search_query)
            if location_data:
                st.session_state.location_data = location_data
                lat, lon = location_data['lat'], location_data['lon']
                if self.fetch_weather_data(lat, lon):
                    st.rerun()
            else:
                st.error(f"❌ Could not find location: {search_query}")
                
    def render_current_weather(self):
        """Render current weather section"""
        if not st.session_state.weather_data:
            return
            
        weather = st.session_state.weather_data
        location = st.session_state.location_data
        
        # Main weather card
        st.markdown('<div class="weather-card current-weather">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"""
                <div class="location-info">
                    <h2>📍 {location['city']}, {location['country']}</h2>
                    <p class="timestamp">Last updated: {st.session_state.last_update.strftime('%H:%M, %d %B %Y')}</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            temp_unit = "°C" if st.session_state.units == "metric" else "°F" if st.session_state.units == "imperial" else "K"
            st.markdown(f"""
                <div class="temperature-display">
                    <span class="temp-main">{weather['main']['temp']:.1f}{temp_unit}</span>
                    <span class="temp-desc">{weather['weather'][0]['description'].title()}</span>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            # Weather icon and additional info
            icon_code = weather['weather'][0]['icon']
            st.markdown(f"""
                <div class="weather-icon">
                    <img src="http://openweathermap.org/img/wn/{icon_code}@4x.png" 
                         alt="{weather['weather'][0]['description']}" />
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Weather details grid
        self.render_weather_details(weather)
        
    def render_weather_details(self, weather):
        """Render detailed weather information"""
        temp_unit = "°C" if st.session_state.units == "metric" else "°F" if st.session_state.units == "imperial" else "K"
        speed_unit = "m/s" if st.session_state.units == "metric" else "mph"
        
        st.markdown('<div class="details-grid">', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        details = [
            ("🌡️", "Feels Like", f"{weather['main']['feels_like']:.1f}{temp_unit}"),
            ("💧", "Humidity", f"{weather['main']['humidity']}%"),
            ("🌬️", "Wind Speed", f"{weather['wind']['speed']:.1f} {speed_unit}"),
            ("👁️", "Visibility", f"{weather.get('visibility', 0)/1000:.1f} km"),
            ("🌅", "Sunrise", datetime.fromtimestamp(weather['sys']['sunrise']).strftime('%H:%M')),
            ("🌇", "Sunset", datetime.fromtimestamp(weather['sys']['sunset']).strftime('%H:%M')),
            ("📊", "Pressure", f"{weather['main']['pressure']} hPa"),
            ("☁️", "Cloudiness", f"{weather['clouds']['all']}%")
        ]
        
        for i, (icon, label, value) in enumerate(details):
            col = [col1, col2, col3, col4][i % 4]
            with col:
                st.markdown(f"""
                    <div class="detail-card">
                        <div class="detail-icon">{icon}</div>
                        <div class="detail-label">{label}</div>
                        <div class="detail-value">{value}</div>
                    </div>
                """, unsafe_allow_html=True)
                
        st.markdown('</div>', unsafe_allow_html=True)
        
    def render_forecast(self):
        """Render weather forecast"""
        if not st.session_state.forecast_data:
            return
            
        st.markdown('<div class="forecast-section">', unsafe_allow_html=True)
        st.markdown('<h3>📅 5-Day Forecast</h3>', unsafe_allow_html=True)
        
        # Process forecast data
        forecast_processed = self.data_processor.process_forecast_data(
            st.session_state.forecast_data, 
            st.session_state.units
        )
        
        # Forecast cards
        st.markdown('<div class="forecast-grid">', unsafe_allow_html=True)
        
        cols = st.columns(5)
        for i, day_data in enumerate(forecast_processed[:5]):
            with cols[i]:
                self.render_forecast_card(day_data)
                
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Temperature trend chart
        self.render_temperature_chart(forecast_processed)
        
    def render_forecast_card(self, day_data):
        """Render individual forecast card"""
        temp_unit = "°C" if st.session_state.units == "metric" else "°F" if st.session_state.units == "imperial" else "K"
        
        st.markdown(f"""
            <div class="forecast-card">
                <div class="forecast-day">{day_data['day']}</div>
                <div class="forecast-icon">
                    <img src="http://openweathermap.org/img/wn/{day_data['icon']}@2x.png" />
                </div>
                <div class="forecast-temps">
                    <span class="temp-high">{day_data['temp_max']:.1f}{temp_unit}</span>
                    <span class="temp-low">{day_data['temp_min']:.1f}{temp_unit}</span>
                </div>
                <div class="forecast-desc">{day_data['description']}</div>
                <div class="forecast-details">
                    <small>💧 {day_data['humidity']}% | 🌬️ {day_data['wind_speed']:.1f}</small>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    def render_temperature_chart(self, forecast_data):
        """Render temperature trend chart"""
        st.markdown('<div class="chart-section">', unsafe_allow_html=True)
        st.markdown('<h3>📈 Temperature Trend</h3>', unsafe_allow_html=True)
        
        # Prepare data for chart
        dates = [item['date'] for item in forecast_data]
        temp_max = [item['temp_max'] for item in forecast_data]
        temp_min = [item['temp_min'] for item in forecast_data]
        
        fig = go.Figure()
        
        # Max temperature line
        fig.add_trace(go.Scatter(
            x=dates, y=temp_max,
            mode='lines+markers',
            name='Max Temperature',
            line=dict(color='#ff6b6b', width=3),
            marker=dict(size=8, color='#ff6b6b')
        ))
        
        # Min temperature line
        fig.add_trace(go.Scatter(
            x=dates, y=temp_min,
            mode='lines+markers',
            name='Min Temperature',
            line=dict(color='#4ecdc4', width=3),
            marker=dict(size=8, color='#4ecdc4')
        ))
        
        # Fill area between lines
        fig.add_trace(go.Scatter(
            x=dates + dates[::-1],
            y=temp_max + temp_min[::-1],
            fill='toself',
            fillcolor='rgba(78, 205, 196, 0.1)',
            line=dict(color='rgba(255,255,255,0)'),
            showlegend=False,
            name='Temperature Range'
        ))
        
        temp_unit = "°C" if st.session_state.units == "metric" else "°F" if st.session_state.units == "imperial" else "K"
        
        fig.update_layout(
            title=f"Temperature Forecast ({temp_unit})",
            xaxis_title="Date",
            yaxis_title=f"Temperature ({temp_unit})",
            hovermode='x unified',
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    def render_air_quality_widget(self):
        """Render air quality information if available"""
        if not st.session_state.location_data:
            return
            
        lat, lon = st.session_state.location_data['lat'], st.session_state.location_data['lon']
        air_quality = self.weather_api.get_air_quality(lat, lon)
        
        if air_quality:
            st.markdown('<div class="air-quality-section">', unsafe_allow_html=True)
            st.markdown('<h3>🌬️ Air Quality Index</h3>', unsafe_allow_html=True)
            
            aqi = air_quality['list'][0]['main']['aqi']
            aqi_levels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
            aqi_colors = {1: "#4CAF50", 2: "#8BC34A", 3: "#FFC107", 4: "#FF9800", 5: "#F44336"}
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown(f"""
                    <div class="aqi-indicator" style="background-color: {aqi_colors[aqi]};">
                        <div class="aqi-value">{aqi}</div>
                        <div class="aqi-level">{aqi_levels[aqi]}</div>
                    </div>
                """, unsafe_allow_html=True)
                
            with col2:
                components = air_quality['list'][0]['components']
                st.markdown(f"""
                    <div class="aqi-details">
                        <div class="aqi-component">CO: {components.get('co', 'N/A')} μg/m³</div>
                        <div class="aqi-component">NO₂: {components.get('no2', 'N/A')} μg/m³</div>
                        <div class="aqi-component">O₃: {components.get('o3', 'N/A')} μg/m³</div>
                        <div class="aqi-component">PM2.5: {components.get('pm2_5', 'N/A')} μg/m³</div>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown('</div>', unsafe_allow_html=True)
            
    def render_footer(self):
        """Render application footer"""
        st.markdown("""
            <div class="footer">
                <p>Built with ❤️ using OpenWeatherMap API | Real-time weather intelligence</p>
                <p>🌍 Your weather, anywhere, anytime</p>
            </div>
        """, unsafe_allow_html=True)
        
    def run(self):
        """Main application runner"""
        self.initialize_session_state()
        self.load_custom_css()
        
        # Header
        self.render_header()
        
        # Main content
        if not st.session_state.weather_data:
            # Welcome screen
            st.markdown("""
                <div class="welcome-section">
                    <h2>🌤️ Welcome to Climatrack</h2>
                    <p>Get real-time weather data for any location worldwide</p>
                </div>
            """, unsafe_allow_html=True)
            
            self.render_location_search()
        else:
            # Weather dashboard
            self.render_current_weather()
            
            # Forecast section
            if st.session_state.forecast_data:
                self.render_forecast()
                
            # Air quality section
            self.render_air_quality_widget()
            
            # Location search (always available)
            st.markdown("---")
            st.markdown("### 🔍 Search Another Location")
            self.render_location_search()
            
        # Footer
        self.render_footer()

if __name__ == "__main__":
    app = WeatherApp()
    app.run()
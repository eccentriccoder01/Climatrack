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
import numpy as np

from weather_api import WeatherAPI
from location_detector import LocationDetector
from ui_components import UIComponents
from data_processor import DataProcessor

# Page configuration
st.set_page_config(
    page_title="Climatrack • Premium Weather Intelligence",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/eccentriccoder01/climatrack',
        'Report a bug': "https://github.com/eccentriccoder01/climatrack/issues",
        'About': "# Climatrack\nPremium weather intelligence platform"
    }
)

class WeatherApp:
    def __init__(self):
        self.weather_api = WeatherAPI()
        self.location_detector = LocationDetector()
        self.ui = UIComponents()
        self.data_processor = DataProcessor()
        
    def initialize_session_state(self):
        """Initialize session state variables with enhanced features"""
        defaults = {
            'location_data': None,
            'weather_data': None,
            'forecast_data': None,
            'hourly_data': None,
            'air_quality_data': None,
            'last_update': None,
            'theme_mode': 'aurora',
            'units': 'metric',
            'favorite_locations': [],
            'comparison_locations': [],
            'show_hourly': False,
            'show_map': False,
            'notifications_enabled': True,
            'auto_refresh': False,
            'refresh_interval': 300,  # 5 minutes
            'user_preferences': {
                'temperature_alerts': True,
                'rain_alerts': True,
                'wind_alerts': True,
                'air_quality_alerts': True
            }
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
                
    def load_custom_css(self):
        """Load premium CSS styling"""
        self.ui.load_premium_css()
        
    def detect_location(self):
        """Enhanced location detection with error handling"""
        try:
            with st.spinner("🌍 Detecting your location..."):
                location_data = self.location_detector.get_location()
                if location_data:
                    st.session_state.location_data = location_data
                    if st.session_state.notifications_enabled:
                        st.success(f"📍 Location detected: {location_data['city']}, {location_data['country']}")
                    return True
                return False
        except Exception as e:
            st.error(f"❌ Location detection failed: {str(e)}")
            return False
            
    def fetch_weather_data(self, lat, lon, show_loading=True):
        """Enhanced weather data fetching with comprehensive data"""
        if show_loading:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        try:
            # Current weather
            if show_loading:
                status_text.text("☁️ Fetching current weather...")
                progress_bar.progress(25)
            
            current_weather = self.weather_api.get_current_weather(lat, lon, st.session_state.units)
            if current_weather:
                st.session_state.weather_data = current_weather
                
            # 5-day forecast
            if show_loading:
                status_text.text("📅 Fetching forecast data...")
                progress_bar.progress(50)
                
            forecast = self.weather_api.get_forecast(lat, lon, st.session_state.units)
            if forecast:
                st.session_state.forecast_data = forecast
                st.session_state.hourly_data = self.data_processor.process_hourly_data(forecast)
                
            # Air quality
            if show_loading:
                status_text.text("🌬️ Fetching air quality data...")
                progress_bar.progress(75)
                
            air_quality = self.weather_api.get_air_quality(lat, lon)
            if air_quality:
                st.session_state.air_quality_data = air_quality
                
            if show_loading:
                status_text.text("✅ Data loaded successfully!")
                progress_bar.progress(100)
                time.sleep(0.5)
                progress_bar.empty()
                status_text.empty()
                
            st.session_state.last_update = datetime.now()
            return current_weather and forecast
            
        except Exception as e:
            if show_loading:
                progress_bar.empty()
                status_text.empty()
            st.error(f"❌ Failed to fetch weather data: {str(e)}")
            return False
            
    def render_header(self):
        """Render premium header with navigation"""
        st.markdown(self.ui.create_premium_header(), unsafe_allow_html=True)
        
        # Navigation and settings
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        
        with col1:
            if st.button("🏠 Dashboard", key="nav_dashboard", use_container_width=True):
                st.session_state.show_hourly = False
                st.session_state.show_map = False
                
        with col2:
            if st.button("⏰ Hourly", key="nav_hourly", use_container_width=True):
                st.session_state.show_hourly = True
                st.session_state.show_map = False
                
        with col3:
            if st.button("🗺️ Map", key="nav_map", use_container_width=True):
                st.session_state.show_map = True
                st.session_state.show_hourly = False
                
        with col4:
            if st.button("⭐ Favorites", key="nav_favorites", use_container_width=True):
                self.show_favorites_modal()
                
        with col5:
            if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
                self.show_settings_modal()
                
    def show_settings_modal(self):
        """Enhanced settings modal with premium features"""
        with st.expander("⚙️ Premium Settings", expanded=True):
            tab1, tab2, tab3, tab4 = st.tabs(["🌡️ Units", "🎨 Theme", "🔔 Alerts", "🔄 Auto-Refresh"])
            
            with tab1:
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
                                st.session_state.location_data['lon'],
                                show_loading=False
                            )
                            st.rerun()
                            
            with tab2:
                theme_options = list(self.ui.themes.keys())
                current_theme_index = theme_options.index(st.session_state.theme_mode) if st.session_state.theme_mode in theme_options else 0
                
                new_theme = st.selectbox(
                    "Color Theme",
                    theme_options,
                    index=current_theme_index,
                    format_func=lambda x: self.ui.themes[x]["name"]
                )
                
                if new_theme != st.session_state.theme_mode:
                    st.session_state.theme_mode = new_theme
                    st.rerun()
                    
            with tab3:
                st.checkbox("Temperature Alerts", value=st.session_state.user_preferences['temperature_alerts'], key="temp_alerts")
                st.checkbox("Rain Alerts", value=st.session_state.user_preferences['rain_alerts'], key="rain_alerts")
                st.checkbox("Wind Alerts", value=st.session_state.user_preferences['wind_alerts'], key="wind_alerts")
                st.checkbox("Air Quality Alerts", value=st.session_state.user_preferences['air_quality_alerts'], key="air_alerts")
                
            with tab4:
                st.session_state.auto_refresh = st.checkbox("Auto-refresh data", value=st.session_state.auto_refresh)
                if st.session_state.auto_refresh:
                    st.session_state.refresh_interval = st.selectbox(
                        "Refresh interval",
                        [300, 600, 900, 1800],
                        format_func=lambda x: f"{x//60} minutes"
                    ) * 1000
                    
                if st.button("🔄 Refresh Now", key="manual_refresh"):
                    if st.session_state.location_data:
                        self.fetch_weather_data(
                            st.session_state.location_data['lat'],
                            st.session_state.location_data['lon']
                        )
                        st.rerun()
    
    def show_favorites_modal(self):
        """Show favorites management modal"""
        with st.expander("⭐ Favorite Locations", expanded=True):
            if st.session_state.favorite_locations:
                for i, location in enumerate(st.session_state.favorite_locations):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"📍 {location['city']}, {location['country']}")
                    with col2:
                        if st.button("Load", key=f"load_fav_{i}", use_container_width=True):
                            st.session_state.location_data = location
                            self.fetch_weather_data(location['lat'], location['lon'])
                            st.rerun()
                    with col3:
                        if st.button("Remove", key=f"remove_fav_{i}", use_container_width=True):
                            st.session_state.favorite_locations.pop(i)
                            st.rerun()
            else:
                st.info("No favorite locations saved yet.")
                
            # Add current location to favorites
            if st.session_state.location_data:
                if st.button("⭐ Add Current Location to Favorites", use_container_width=True):
                    if st.session_state.location_data not in st.session_state.favorite_locations:
                        st.session_state.favorite_locations.append(st.session_state.location_data)
                        st.success("Location added to favorites!")
                        time.sleep(1)
                        st.rerun()
    
    def render_location_search(self):
        """Enhanced location search with autocomplete"""
        st.markdown('<div class="premium-search">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "",
                placeholder="🔍 Search for a city, country, or coordinates... (e.g., New York, London, 40.7128,-74.0060)",
                key="location_search",
                label_visibility="collapsed"
            )
            
        with col2:
            search_clicked = st.button("🔍 Search", key="search_btn", use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick location buttons
        col1, col2, col3, col4 = st.columns(4)
        quick_locations = [
            {"name": "📍 Auto-detect", "action": "auto"},
            {"name": "🗽 New York", "query": "New York, US"},
            {"name": "🏛️ London", "query": "London, UK"},
            {"name": "🗼 Tokyo", "query": "Tokyo, JP"}
        ]
        
        for i, location in enumerate(quick_locations):
            col = [col1, col2, col3, col4][i]
            with col:
                if st.button(location["name"], key=f"quick_{i}", use_container_width=True):
                    if location["action"] == "auto":
                        if self.detect_location():
                            lat, lon = st.session_state.location_data['lat'], st.session_state.location_data['lon']
                            if self.fetch_weather_data(lat, lon):
                                st.rerun()
                    else:
                        location_data = self.location_detector.search_location(location["query"])
                        if location_data:
                            st.session_state.location_data = location_data
                            lat, lon = location_data['lat'], location_data['lon']
                            if self.fetch_weather_data(lat, lon):
                                st.rerun()
                                
        # Handle manual search
        if search_clicked and search_query:
            # Check if it's coordinates
            if ',' in search_query and search_query.replace(',', '').replace('.', '').replace('-', '').replace(' ', '').isdigit():
                try:
                    coords = search_query.split(',')
                    lat, lon = float(coords[0].strip()), float(coords[1].strip())
                    if self.location_detector.validate_coordinates(lat, lon):
                        # Reverse geocode to get location name
                        location_data = self.location_detector.reverse_geocode(lat, lon)
                        if location_data:
                            st.session_state.location_data = location_data
                            if self.fetch_weather_data(lat, lon):
                                st.rerun()
                        else:
                            st.error("❌ Could not find location for these coordinates")
                    else:
                        st.error("❌ Invalid coordinates")
                except:
                    st.error("❌ Invalid coordinate format")
            else:
                # Regular location search
                location_data = self.location_detector.search_location(search_query)
                if location_data:
                    st.session_state.location_data = location_data
                    lat, lon = location_data['lat'], location_data['lon']
                    if self.fetch_weather_data(lat, lon):
                        st.rerun()
                else:
                    st.error(f"❌ Could not find location: {search_query}")
                    
    def render_current_weather(self):
        """Enhanced current weather display"""
        if not st.session_state.weather_data:
            return
            
        weather = st.session_state.weather_data
        location = st.session_state.location_data
        
        # Main weather card
        st.markdown('<div class="premium-weather-card">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"""
                <div class="location-info">
                    <h2>📍 {location['city']}, {location['country']}</h2>
                    <p class="timestamp">Last updated: {st.session_state.last_update.strftime('%H:%M, %d %B %Y')}</p>
                    <div style="margin-top: 1rem;">
                        <span style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">
                            🌐 {location['lat']:.4f}, {location['lon']:.4f}
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            temp_unit = "°C" if st.session_state.units == "metric" else "°F" if st.session_state.units == "imperial" else "K"
            feels_like = weather['main']['feels_like']
            
            st.markdown(f"""
                <div class="temperature-showcase">
                    <span class="temp-main">{weather['main']['temp']:.1f}{temp_unit}</span>
                    <span class="temp-desc">{weather['weather'][0]['description'].title()}</span>
                    <div style="margin-top: 0.5rem; font-size: 0.9rem; color: rgba(255,255,255,0.7);">
                        Feels like {feels_like:.1f}{temp_unit}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            # Enhanced weather icon
            icon_code = weather['weather'][0]['icon']
            condition = weather['weather'][0]['main'].lower()
            st.markdown(
                self.ui.create_weather_icon_enhanced(icon_code, condition), 
                unsafe_allow_html=True
            )
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced weather details
        self.render_weather_details_premium(weather)
        
        # Weather insights and recommendations
        self.render_weather_insights(weather)
        
    def render_weather_details_premium(self, weather):
        """Enhanced weather details with premium styling"""
        temp_unit = "°C" if st.session_state.units == "metric" else "°F" if st.session_state.units == "imperial" else "K"
        speed_unit = "m/s" if st.session_state.units == "metric" else "mph"
        
        st.markdown('<div class="premium-details-grid">', unsafe_allow_html=True)
        
        # Calculate additional metrics
        dew_point = weather['main']['temp'] - ((100 - weather['main']['humidity']) / 5)
        heat_index = self.data_processor.calculate_comfort_index(
            weather['main']['temp'], 
            weather['main']['humidity'], 
            weather['wind']['speed']
        )
        
        wind_direction = self.data_processor.format_wind_direction(weather['wind'].get('deg', 0))
        
        details = [
            ("🌡️", "Feels Like", f"{weather['main']['feels_like']:.1f}", temp_unit, "Apparent temperature"),
            ("💧", "Humidity", f"{weather['main']['humidity']}", "%", "Relative humidity"),
            ("🌬️", "Wind", f"{weather['wind']['speed']:.1f} {speed_unit}", f"{wind_direction}", "Wind speed & direction"),
            ("👁️", "Visibility", f"{weather.get('visibility', 0)/1000:.1f}", "km", "Horizontal visibility"),
            ("🌅", "Sunrise", datetime.fromtimestamp(weather['sys']['sunrise']).strftime('%H:%M'), "", "Local sunrise time"),
            ("🌇", "Sunset", datetime.fromtimestamp(weather['sys']['sunset']).strftime('%H:%M'), "", "Local sunset time"),
            ("📊", "Pressure", f"{weather['main']['pressure']}", "hPa", "Atmospheric pressure"),
            ("☁️", "Cloudiness", f"{weather['clouds']['all']}", "%", "Cloud coverage"),
            ("💎", "Dew Point", f"{dew_point:.1f}", temp_unit, "Dew point temperature"),
            ("🎯", "Comfort Index", f"{heat_index['score']:.0f}/100", f"({heat_index['level']})", "Weather comfort rating"),
            ("🌡️", "Min/Max", f"{weather['main']['temp_min']:.1f}/{weather['main']['temp_max']:.1f}", temp_unit, "Daily temperature range"),
            ("⚡", "UV Index", "Calculating...", "", "UV radiation level")
        ]
        
        cols = st.columns(4)
        for i, (icon, label, value, unit, description) in enumerate(details):
            col = cols[i % 4]
            with col:
                st.markdown(
                    self.ui.create_metric_card_premium(icon, label, value, unit, description=description),
                    unsafe_allow_html=True
                )
                
        st.markdown('</div>', unsafe_allow_html=True)
        
    def render_weather_insights(self, weather):
        """Render AI-powered weather insights and recommendations"""
        if not st.session_state.forecast_data:
            return
            
        forecast_processed = self.data_processor.process_forecast_data(
            st.session_state.forecast_data, 
            st.session_state.units
        )
        
        recommendations = self.data_processor.get_weather_recommendations(weather, forecast_processed)
        alerts = self.data_processor.get_weather_alerts(weather, forecast_processed)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div class="glass-card" style="padding: var(--space-lg);">
                    <h3 style="color: white; margin-bottom: var(--space-md);">🧠 Smart Recommendations</h3>
                </div>
            """, unsafe_allow_html=True)
            
            for rec in recommendations:
                st.markdown(f"""
                    <div class="glass-card hover-lift" style="padding: var(--space-md); margin: var(--space-sm) 0;">
                        <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem;">{rec}</p>
                    </div>
                """, unsafe_allow_html=True)
                
        with col2:
            st.markdown("""
                <div class="glass-card" style="padding: var(--space-lg);">
                    <h3 style="color: white; margin-bottom: var(--space-md);">⚠️ Weather Alerts</h3>
                </div>
            """, unsafe_allow_html=True)
            
            if alerts:
                for alert in alerts:
                    alert_colors = {
                        'warning': '#f59e0b',
                        'caution': '#3b82f6',
                        'info': '#10b981'
                    }
                    color = alert_colors.get(alert['type'], '#6b7280')
                    
                    st.markdown(f"""
                        <div class="glass-card hover-lift" style="
                            padding: var(--space-md); 
                            margin: var(--space-sm) 0;
                            border-left: 4px solid {color};
                        ">
                            <div style="display: flex; align-items: center; gap: var(--space-sm);">
                                <span style="font-size: 1.2rem;">{alert['icon']}</span>
                                <div>
                                    <strong style="color: white;">{alert['title']}</strong>
                                    <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.85rem;">{alert['message']}</p>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="glass-card" style="padding: var(--space-md); text-align: center;">
                        <p style="color: rgba(255,255,255,0.7); margin: 0;">✅ No weather alerts at this time</p>
                    </div>
                """, unsafe_allow_html=True)
                
    def render_hourly_forecast(self):
        """Render detailed hourly forecast"""
        if not st.session_state.hourly_data:
            return
            
        st.markdown('<div class="premium-forecast">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">⏰ 24-Hour Detailed Forecast</h2>', unsafe_allow_html=True)
        
        # Create interactive hourly chart
        hourly_data = st.session_state.hourly_data[:24]
        
        # Temperature and precipitation chart
        fig = go.Figure()
        
        times = [item['hour'] for item in hourly_data]
        temps = [item['temp'] for item in hourly_data]
        feels_like = [item['feels_like'] for item in hourly_data]
        precipitation = [item['pop'] for item in hourly_data]
        
        # Temperature line
        fig.add_trace(go.Scatter(
            x=times, y=temps,
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#ff6b35', width=3),
            marker=dict(size=6, color='#ff6b35'),
            hovertemplate='<b>%{x}</b><br>Temperature: %{y}°<extra></extra>'
        ))
        
        # Feels like line
        fig.add_trace(go.Scatter(
            x=times, y=feels_like,
            mode='lines',
            name='Feels Like',
            line=dict(color='#4facfe', width=2, dash='dash'),
            hovertemplate='<b>%{x}</b><br>Feels Like: %{y}°<extra></extra>'
        ))
        
        # Precipitation bars
        fig.add_trace(go.Bar(
            x=times, y=precipitation,
            name='Precipitation %',
            yaxis='y2',
            marker_color='rgba(6, 255, 165, 0.3)',
            hovertemplate='<b>%{x}</b><br>Precipitation: %{y}%<extra></extra>'
        ))
        
        temp_unit = "°C" if st.session_state.units == "metric" else "°F" if st.session_state.units == "imperial" else "K"
        
        fig.update_layout(
            title=f"Hourly Temperature & Precipitation Forecast",
            xaxis_title="Time",
            yaxis_title=f"Temperature ({temp_unit})",
            yaxis2=dict(
                title="Precipitation (%)",
                overlaying='y',
                side='right',
                range=[0, 100]
            ),
            hovermode='x unified',
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Hourly cards grid
        st.markdown('<div class="forecast-grid">', unsafe_allow_html=True)
        
        cols = st.columns(6)
        for i, hour_data in enumerate(hourly_data[:12]):  # Show first 12 hours
            col = cols[i % 6]
            with col:
                self.render_hourly_card(hour_data)
                
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    def render_hourly_card(self, hour_data):
        """Render individual hourly forecast card"""
        temp_unit = "°C" if st.session_state.units == "metric" else "°F" if st.session_state.units == "imperial" else "K"
        
        st.markdown(f"""
            <div class="forecast-card">
                <div class="forecast-day">{hour_data['hour']}</div>
                <div class="forecast-icon">
                    <img src="http://openweathermap.org/img/wn/{hour_data['icon']}@2x.png" />
                </div>
                <div class="forecast-temps">
                    <span class="temp-high">{hour_data['temp']:.0f}{temp_unit}</span>
                </div>
                <div class="forecast-desc">{hour_data['description']}</div>
                <div class="forecast-details">
                    <div>💧 {hour_data['pop']:.0f}%</div>
                    <div>🌬️ {hour_data['wind_speed']:.0f}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    def render_forecast(self):
        """Enhanced 5-day forecast with advanced features"""
        if not st.session_state.forecast_data:
            return
            
        st.markdown('<div class="premium-forecast">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">📅 5-Day Weather Forecast</h2>', unsafe_allow_html=True)
        
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
                self.render_forecast_card_premium(day_data, i == 0)
                
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Advanced temperature and weather trends chart
        self.render_advanced_temperature_chart(forecast_processed)
        
        # Weather trends analysis
        trends = self.data_processor.calculate_weather_trends(forecast_processed)
        self.render_trends_analysis(trends)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    def render_forecast_card_premium(self, day_data, is_today=False):
        """Render premium forecast card with enhanced details"""
        temp_unit = "°C" if st.session_state.units == "metric" else "°F" if st.session_state.units == "imperial" else "K"
        
        today_class = "today-highlight" if is_today else ""
        day_label = "Today" if is_today else day_data['day']
        
        st.markdown(f"""
            <div class="forecast-card {today_class}">
                <div class="forecast-day">{day_label}</div>
                <div class="forecast-date">{day_data['date'].strftime('%m/%d')}</div>
                <div class="forecast-icon">
                    <img src="http://openweathermap.org/img/wn/{day_data['icon']}@2x.png" />
                </div>
                <div class="forecast-temps">
                    <span class="temp-high">{day_data['temp_max']:.0f}{temp_unit}</span>
                    <span class="temp-low">{day_data['temp_min']:.0f}{temp_unit}</span>
                </div>
                <div class="forecast-desc">{day_data['description']}</div>
                <div class="forecast-details">
                    <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                        <span>💧 {day_data['humidity']:.0f}%</span>
                        <span>🌬️ {day_data['wind_speed']:.0f}</span>
                    </div>
                </div>
            </div>
            
            <style>
            .today-highlight {{
                border: 2px solid var(--primary) !important;
                background: rgba(0, 212, 255, 0.1) !important;
                transform: scale(1.02);
            }}
            
            .forecast-date {{
                font-size: 0.75rem;
                color: rgba(255, 255, 255, 0.6);
                margin-bottom: 0.5rem;
            }}
            </style>
        """, unsafe_allow_html=True)
        
    def render_advanced_temperature_chart(self, forecast_data):
        """Render advanced temperature chart with multiple metrics"""
        st.markdown('<div class="premium-chart">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">📈 Advanced Weather Trends</h3>', unsafe_allow_html=True)
        
        # Prepare data
        dates = [item['date'].strftime('%m/%d') for item in forecast_data]
        temp_max = [item['temp_max'] for item in forecast_data]
        temp_min = [item['temp_min'] for item in forecast_data]
        temp_avg = [item['temp_avg'] for item in forecast_data]
        humidity = [item['humidity'] for item in forecast_data]
        wind_speed = [item['wind_speed'] for item in forecast_data]
        
        # Create subplots
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Temperature Trends', 'Humidity Levels', 'Wind Speed'),
            vertical_spacing=0.08,
            specs=[[{"secondary_y": False}],
                   [{"secondary_y": False}],
                   [{"secondary_y": False}]]
        )
        
        # Temperature plot
        fig.add_trace(go.Scatter(
            x=dates, y=temp_max,
            mode='lines+markers',
            name='Max Temp',
            line=dict(color='#ff6b6b', width=3),
            marker=dict(size=8)
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=dates, y=temp_min,
            mode='lines+markers',
            name='Min Temp',
            line=dict(color='#4ecdc4', width=3),
            marker=dict(size=8)
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=dates, y=temp_avg,
            mode='lines+markers',
            name='Avg Temp',
            line=dict(color='#feca57', width=2, dash='dash'),
            marker=dict(size=6)
        ), row=1, col=1)
        
        # Fill area between max and min
        fig.add_trace(go.Scatter(
            x=dates + dates[::-1],
            y=temp_max + temp_min[::-1],
            fill='toself',
            fillcolor='rgba(78, 205, 196, 0.1)',
            line=dict(color='rgba(255,255,255,0)'),
            showlegend=False,
            name='Temperature Range'
        ), row=1, col=1)
        
        # Humidity plot
        fig.add_trace(go.Scatter(
            x=dates, y=humidity,
            mode='lines+markers',
            name='Humidity',
            line=dict(color='#00d4ff', width=3),
            marker=dict(size=8),
            showlegend=False
        ), row=2, col=1)
        
        # Wind speed plot
        fig.add_trace(go.Scatter(
            x=dates, y=wind_speed,
            mode='lines+markers',
            name='Wind Speed',
            line=dict(color='#7c3aed', width=3),
            marker=dict(size=8),
            showlegend=False
        ), row=3, col=1)
        
        temp_unit = "°C" if st.session_state.units == "metric" else "°F" if st.session_state.units == "imperial" else "K"
        speed_unit = "m/s" if st.session_state.units == "metric" else "mph"
        
        fig.update_yaxes(title_text=f"Temperature ({temp_unit})", row=1, col=1)
        fig.update_yaxes(title_text="Humidity (%)", row=2, col=1)
        fig.update_yaxes(title_text=f"Wind Speed ({speed_unit})", row=3, col=1)
        
        fig.update_layout(
            height=800,
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    def render_trends_analysis(self, trends):
        """Render weather trends analysis"""
        st.markdown("""
            <div class="glass-card" style="padding: var(--space-lg); margin: var(--space-lg) 0;">
                <h3 style="color: white; margin-bottom: var(--space-md);">📊 Weather Trends Analysis</h3>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            temp_trend = trends.get('temperature', {})
            trend_icon = "📈" if temp_trend.get('max_trend') == 'increasing' else "📉" if temp_trend.get('max_trend') == 'decreasing' else "➡️"
            
            st.markdown(f"""
                <div class="glass-card hover-lift" style="padding: var(--space-md); text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: var(--space-sm);">{trend_icon}</div>
                    <h4 style="color: white; margin-bottom: var(--space-sm);">Temperature</h4>
                    <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;">
                        {temp_trend.get('max_trend', 'stable').title()} trend<br>
                        Range: {temp_trend.get('max_change', 0):.1f}° variation
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            humidity_trend = trends.get('humidity', {})
            humidity_icon = "💧" if humidity_trend.get('avg', 0) > 70 else "🏜️" if humidity_trend.get('avg', 0) < 30 else "💨"
            
            st.markdown(f"""
                <div class="glass-card hover-lift" style="padding: var(--space-md); text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: var(--space-sm);">{humidity_icon}</div>
                    <h4 style="color: white; margin-bottom: var(--space-sm);">Humidity</h4>
                    <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;">
                        {humidity_trend.get('trend', 'stable').title()} pattern<br>
                        Average: {humidity_trend.get('avg', 0):.0f}%
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            wind_trend = trends.get('wind', {})
            wind_icon = "💨" if wind_trend.get('max', 0) > 10 else "🍃" if wind_trend.get('max', 0) > 5 else "😌"
            
            st.markdown(f"""
                <div class="glass-card hover-lift" style="padding: var(--space-md); text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: var(--space-sm);">{wind_icon}</div>
                    <h4 style="color: white; margin-bottom: var(--space-sm);">Wind</h4>
                    <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;">
                        {wind_trend.get('trend', 'stable').title()} conditions<br>
                        Peak: {wind_trend.get('max', 0):.1f} {speed_unit}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
    def render_air_quality_premium(self):
        """Enhanced air quality display with detailed metrics"""
        if not st.session_state.air_quality_data:
            return
            
        st.markdown('<div class="premium-air-quality">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">🌬️ Air Quality Index</h3>', unsafe_allow_html=True)
        
        aqi_data = st.session_state.air_quality_data['list'][0]
        aqi = aqi_data['main']['aqi']
        components = aqi_data['components']
        
        aqi_levels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
        aqi_colors = {1: "#4CAF50", 2: "#8BC34A", 3: "#FFC107", 4: "#FF9800", 5: "#F44336"}
        aqi_descriptions = {
            1: "Air quality is satisfactory for the general population",
            2: "Air quality is acceptable for most people",
            3: "Members of sensitive groups may experience health effects",
            4: "Health effects may be experienced by the general population",
            5: "Health warnings of emergency conditions for everyone"
        }
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
                <div class="aqi-indicator" style="background: linear-gradient(135deg, {aqi_colors[aqi]}, {aqi_colors[aqi]}cc);">
                    <div class="aqi-value">{aqi}</div>
                    <div class="aqi-level">{aqi_levels[aqi]}</div>
                    <div style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">
                        AQI Score
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
                <div style="padding: var(--space-lg);">
                    <h4 style="color: white; margin-bottom: var(--space-md);">Health Advisory</h4>
                    <p style="color: rgba(255,255,255,0.9); line-height: 1.5; margin-bottom: var(--space-md);">
                        {aqi_descriptions[aqi]}
                    </p>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: var(--space-sm);">
                        <div class="aqi-component">
                            <strong>CO</strong><br>
                            {components.get('co', 'N/A')} μg/m³
                        </div>
                        <div class="aqi-component">
                            <strong>NO₂</strong><br>
                            {components.get('no2', 'N/A')} μg/m³
                        </div>
                        <div class="aqi-component">
                            <strong>O₃</strong><br>
                            {components.get('o3', 'N/A')} μg/m³
                        </div>
                        <div class="aqi-component">
                            <strong>PM2.5</strong><br>
                            {components.get('pm2_5', 'N/A')} μg/m³
                        </div>
                        <div class="aqi-component">
                            <strong>PM10</strong><br>
                            {components.get('pm10', 'N/A')} μg/m³
                        </div>
                        <div class="aqi-component">
                            <strong>SO₂</strong><br>
                            {components.get('so2', 'N/A')} μg/m³
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    def render_weather_map(self):
        """Render interactive weather map"""
        if not st.session_state.location_data:
            return
            
        st.markdown('<div class="premium-chart">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">🗺️ Interactive Weather Map</h3>', unsafe_allow_html=True)
        
        lat, lon = st.session_state.location_data['lat'], st.session_state.location_data['lon']
        
        # Create map with current location
        fig = go.Figure(go.Scattermapbox(
            lat=[lat],
            lon=[lon],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=20,
                color='rgb(255, 0, 0)',
                symbol='circle'
            ),
            text=[f"{st.session_state.location_data['city']}, {st.session_state.location_data['country']}"],
            hoverinfo='text'
        ))
        
        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox=dict(
                center=go.layout.mapbox.Center(
                    lat=lat,
                    lon=lon
                ),
                zoom=10
            ),
            showlegend=False,
            height=500,
            margin={"r":0,"t":0,"l":0,"b":0}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    def render_footer(self):
        """Render premium footer"""
        st.markdown(f"""
            <div class="premium-footer">
                <p>🌤️ <strong>Climatrack Premium</strong> • Real-time Weather Intelligence Platform</p>
                <p>Built with ❤️ by eccentriccoder01 • Powered by OpenWeatherMap API</p>
                <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                <div style="margin-top: var(--space-md); display: flex; justify-content: center; gap: var(--space-md);">
                    <a href="https://github.com/eccentriccoder01/climatrack" style="color: var(--primary); text-decoration: none;">🔗 GitHub</a>
                    <a href="#" style="color: var(--primary); text-decoration: none;">📧 Support</a>
                    <a href="#" style="color: var(--primary); text-decoration: none;">📖 Documentation</a>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    def run(self):
        """Main application runner with enhanced features"""
        self.initialize_session_state()
        self.load_custom_css()
        
        # Auto-refresh logic
        if st.session_state.auto_refresh and st.session_state.location_data:
            time.sleep(st.session_state.refresh_interval / 1000)
            self.fetch_weather_data(
                st.session_state.location_data['lat'],
                st.session_state.location_data['lon'],
                show_loading=False
            )
            st.rerun()
        
        # Header
        self.render_header()
        
        # Main content based on navigation
        if not st.session_state.weather_data:
            # Welcome screen
            st.markdown("""
                <div class="glass-card" style="text-align: center; padding: var(--space-3xl) var(--space-xl); margin: var(--space-xl) 0;">
                    <h2 style="color: white; font-size: 2.5rem; margin-bottom: var(--space-md);">🌤️ Welcome to Climatrack Premium</h2>
                    <p style="color: rgba(255,255,255,0.8); font-size: 1.2rem; margin-bottom: var(--space-xl);">
                        Experience the most advanced weather intelligence platform with real-time data, AI-powered insights, and premium features.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            self.render_location_search()
        else:
            # Weather dashboard based on navigation
            if st.session_state.show_hourly:
                self.render_hourly_forecast()
            elif st.session_state.show_map:
                self.render_weather_map()
            else:
                # Main dashboard
                self.render_current_weather()
                
                # Forecast section
                if st.session_state.forecast_data:
                    self.render_forecast()
                    
                # Air quality section
                if st.session_state.air_quality_data:
                    self.render_air_quality_premium()
            
            # Always show location search at bottom
            st.markdown("---")
            st.markdown("### 🔍 Search Another Location")
            self.render_location_search()
            
        # Footer
        self.render_footer()

if __name__ == "__main__":
    app = WeatherApp()
    app.run()
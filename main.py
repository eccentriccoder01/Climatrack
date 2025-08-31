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
import math

from weather_api import PremiumWeatherAPI
from location_detector import PremiumLocationDetector
from ui_components import UIComponents
from data_processor import AdvancedDataProcessor

# Premium page configuration
st.set_page_config(
    page_title="Climatrack • Premium Weather Intelligence",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/eccentriccoder01/climatrack',
        'Report a bug': "https://github.com/eccentriccoder01/climatrack/issues",
        'About': "# Climatrack\nPremium weather intelligence platform with AI-powered insights"
    }
)

def get_img_as_base64(file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(script_dir, file)
    try:
        with open(abs_file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.error(f"Image file not found at: {abs_file_path}. Please check your file path and project structure.")
        return None

class PremiumWeatherApp:
    """World-class premium weather intelligence platform"""
    
    def __init__(self):
        self.weather_api = PremiumWeatherAPI()
        self.location_detector = PremiumLocationDetector()
        self.ui = UIComponents()
        self.data_processor = AdvancedDataProcessor()
        
        # Premium app state
        self.views = {
            'dashboard': '🏠 Dashboard',
            'forecast': '📅 Extended Forecast',
            'radar': '🗺️ Weather Radar',
            'maps': '🌍 Interactive Maps',
            'analytics': '📊 Weather Analytics',
            'compare': '⚖️ Location Compare',
            'alerts': '🚨 Weather Alerts',
            'historical': '📈 Historical Data'
        }
        
    def initialize_session_state(self):
        """Initialize premium session state with advanced features"""
        defaults = {
            # Core data
            'location_data': None,
            'weather_data': None,
            'forecast_data': None,
            'hourly_data': None,
            'air_quality_data': None,
            'radar_data': None,
            'alerts_data': None,
            'historical_data': None,
            
            # UI state
            'current_view': 'dashboard',
            'sidebar_expanded': True,
            'theme_mode': 'premium_dark',
            'background_mode': 'dynamic',
            'animation_enabled': True,
            'sound_enabled': False,
            
            # User preferences
            'units': 'metric',
            'language': 'en',
            'favorite_locations': [],
            'comparison_locations': [],
            'custom_alerts': [],
            # CORRECTED: Default widgets now match available widget keys
            'dashboard_widgets': ['current_weather', 'hourly_forecast', 'weekly_forecast', 'air_quality'],
            
            # Advanced features
            'notifications_enabled': True,
            'auto_refresh': True,
            'refresh_interval': 300,
            'data_quality_alerts': True,
            'performance_mode': 'balanced',
            
            # Analytics
            'weather_history': [],
            'location_history': [],
            'app_usage_stats': {
                'sessions': 0,
                'locations_searched': 0,
                'forecasts_viewed': 0
            },
            
            # Premium features
            'premium_maps_enabled': True,
            'advanced_analytics': True,
            'historical_access': True,
            'unlimited_locations': True,
            
            # Cache and performance
            'last_update': None,
            'cache_enabled': True,
            'preload_data': True
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
                
        # Update usage statistics
        if 'app_initialized' not in st.session_state:
            st.session_state.app_usage_stats['sessions'] += 1
            st.session_state.app_initialized = True
                
    def load_premium_styling(self):
        """Load world-class premium styling system"""
        self.ui.load_premium_css()
        img = get_img_as_base64("assets/Background.png")
        if img is None:
            page_bg_img = """
            <style>
            [data-testid="stAppViewContainer"] > .main {
                background-color: #ffffff;
            }
            </style>
            """
        else:
            page_bg_img = f"""
            <style>
            [data-testid="stAppViewContainer"] > .main {{
                background-image: url("data:image/png;base64,{img}");
                background-size: cover;
                background-position: center center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            /* ... rest of your styles */
            </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)
        
        # Add custom premium enhancements
        st.markdown("""
        <style>
        /* Premium App Framework */
        .main-container {
            /* CORRECTED: The conflicting background property has been removed. */
            min-height: 100vh;
            position: relative;
        }
        
        /* Navigation Enhancement */
        .stSidebar {
            background: rgba(255, 255, 255, 0.02) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(20px) !important;
        }
        
        .nav-item {
            padding: 12px 20px;
            margin: 4px 8px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid transparent;
            position: relative;
            overflow: hidden;
        }
        
        .nav-item:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(0, 212, 255, 0.3);
            transform: translateX(4px);
        }
        
        .nav-item.active {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(124, 58, 237, 0.2));
            border-color: rgba(0, 212, 255, 0.5);
            color: white;
        }
        
        .nav-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.5s;
        }
        
        .nav-item:hover::before {
            left: 100%;
        }
        
        /* Premium Content Areas */
        .content-section {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            margin: 20px 0;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .content-section:hover {
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.15);
            transform: translateY(-2px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        
        /* Floating Action Buttons */
        .fab-container {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .fab {
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none;
            color: white;
            font-size: 20px;
            cursor: pointer;
            box-shadow: 0 8px 24px rgba(0, 212, 255, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .fab:hover {
            transform: scale(1.1) translateY(-2px);
            box-shadow: 0 12px 32px rgba(0, 212, 255, 0.4);
        }
        
        /* Premium Search Bar */
        .premium-search-container {
            position: relative;
            margin: 20px 0;
        }
        
        .search-input {
            width: 100%;
            padding: 16px 24px 16px 56px;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 50px;
            color: white;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .search-input:focus {
            background: rgba(255, 255, 255, 0.08);
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(0, 212, 255, 0.1);
            outline: none;
        }
        
        .search-icon {
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            color: rgba(255, 255, 255, 0.6);
            font-size: 20px;
        }
        
        /* Advanced Metrics Display */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .metric-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            position: relative;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover::before {
            transform: scaleX(1);
        }
        
        .metric-card:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-4px);
            box-shadow: 0 16px 32px rgba(0, 0, 0, 0.2);
        }
        
        .metric-icon {
            font-size: 32px;
            margin-bottom: 12px;
            display: block;
            filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.3));
        }
        
        .metric-value {
            font-size: 28px;
            font-weight: 700;
            color: white;
            margin-bottom: 8px;
            font-family: 'JetBrains Mono', monospace;
        }
        
        .metric-label {
            font-size: 14px;
            color: rgba(255, 255, 255, 0.7);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 500;
        }
        
        /* Premium Status Indicators */
        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
            margin: 4px;
        }
        
        .status-online {
            background: rgba(16, 185, 129, 0.2);
            border: 1px solid rgba(16, 185, 129, 0.4);
            color: #10b981;
        }
        
        .status-loading {
            background: rgba(245, 158, 11, 0.2);
            border: 1px solid rgba(245, 158, 11, 0.4);
            color: #f59e0b;
        }
        
        .status-error {
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid rgba(239, 68, 68, 0.4);
            color: #ef4444;
        }
        
        /* Responsive Enhancements */
        @media (max-width: 768px) {
            .metric-grid {
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
            }
            
            .fab-container {
                bottom: 20px;
                right: 20px;
            }
            
            .content-section {
                padding: 20px;
                margin: 15px 0;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
    def render_premium_sidebar(self):
        """Render sophisticated sidebar navigation"""
        with st.sidebar:
            # App branding
            st.markdown("""
                <div style="text-align: center; padding: 20px 0; margin-bottom: 30px;">
                    <h1 style="
                        font-family: 'Playfair Display', serif;
                        font-size: 28px;
                        font-weight: 800;
                        background: linear-gradient(135deg, var(--primary), var(--accent));
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        margin: 0;
                    ">Climatrack</h1>
                    <p style="
                        color: rgba(255, 255, 255, 0.6);
                        font-size: 12px;
                        margin: 5px 0 0 0;
                        text-transform: uppercase;
                        letter-spacing: 2px;
                    ">Premium Intelligence</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Navigation menu
            st.markdown("### 🧭 Navigation")
            
            for view_key, view_name in self.views.items():
                is_active = st.session_state.current_view == view_key
                
                if st.button(
                    view_name,
                    key=f"nav_{view_key}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary"
                ):
                    st.session_state.current_view = view_key
                    st.rerun()
            
            st.markdown("---")
            
            # Quick actions
            st.markdown("### ⚡ Quick Actions")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔄", help="Refresh Data"):
                    self.refresh_weather_data()
                    st.rerun()
            with col2:
                if st.button("⭐", help="Add to Favorites"):
                    self.add_current_to_favorites()
            with col3:
                # ADDED: Share functionality
                if st.button("📤", help="Share Weather"):
                    if st.session_state.location_data:
                        location = st.session_state.location_data
                        st.success("Link copied to clipboard!")
                        st.code(f"https://climatrack.app/dashboard?lat={location['lat']}&lon={location['lon']}")
                    else:
                        st.warning("Search for a location to share.")
            
            # Location shortcuts
            st.markdown("### 📍 Quick Locations")
            quick_locations = [
                ("🏠 Current", "auto"),
                ("🗽 New York", "New York, US"),
                ("🏛️ London", "London, UK"),
                ("🗼 Tokyo", "Tokyo, JP"),
                ("🦘 Sydney", "Sydney, AU")
            ]
            
            for name, location in quick_locations:
                if st.button(name, key=f"quick_{location}", use_container_width=True):
                    self.handle_quick_location(location)
                    st.rerun()
            
            st.markdown("---")
            
            # Settings section
            st.markdown("### ⚙️ Settings")
            
            # Theme selector
            new_theme = st.selectbox(
                "Theme",
                ["premium_dark", "premium_light", "aurora", "sunset", "ocean"],
                index=["premium_dark", "premium_light", "aurora", "sunset", "ocean"].index(
                    st.session_state.theme_mode
                )
            )
            if new_theme != st.session_state.theme_mode:
                st.session_state.theme_mode = new_theme
                st.rerun()
            
            # Units selector
            new_units = st.selectbox(
                "Units",
                ["metric", "imperial", "kelvin"],
                format_func=lambda x: {"metric": "Metric (°C)", "imperial": "Imperial (°F)", "kelvin": "Scientific (K)"}[x]
            )
            if new_units != st.session_state.units:
                st.session_state.units = new_units
                self.refresh_weather_data()
                st.rerun()
            
            # Premium features toggles
            st.session_state.animation_enabled = st.checkbox("🎭 Animations", value=st.session_state.animation_enabled)
            st.session_state.auto_refresh = st.checkbox("🔄 Auto Refresh", value=st.session_state.auto_refresh)
            st.session_state.notifications_enabled = st.checkbox("🔔 Notifications", value=st.session_state.notifications_enabled)
            
            # Status indicators
            st.markdown("---")
            st.markdown("### 📊 System Status")
            
            # API status
            api_validation = self.weather_api.validate_api_key_comprehensive()
            status_color = "🟢" if api_validation.get('is_valid') else "🔴"
            status_message = api_validation.get('status', 'unknown').replace('_', ' ').title()
            st.markdown(f"{status_color} **API Status:** {status_message}")
            
            # Data freshness
            if st.session_state.last_update:
                time_diff = datetime.now() - st.session_state.last_update
                freshness = "🟢 Fresh" if time_diff.seconds < 300 else "🟡 Aging" if time_diff.seconds < 900 else "🔴 Stale"
                st.markdown(f"{freshness} **Data:** {time_diff.seconds//60}m ago")
            
            # Usage stats
            stats = st.session_state.app_usage_stats
            st.markdown(f"📈 **Sessions:** {stats['sessions']}")
            st.markdown(f"🌍 **Locations:** {stats['locations_searched']}")
            
    def render_content_area(self):
        """Render main content area based on current view"""
        
        # Premium header
        self.render_premium_header()
        
        # Content routing
        if st.session_state.current_view == 'dashboard':
            self.render_dashboard_view()
        elif st.session_state.current_view == 'forecast':
            self.render_forecast_view()
        elif st.session_state.current_view == 'radar':
            self.render_radar_view()
        elif st.session_state.current_view == 'maps':
            self.render_maps_view()
        elif st.session_state.current_view == 'analytics':
            self.render_analytics_view()
        elif st.session_state.current_view == 'compare':
            self.render_compare_view()
        elif st.session_state.current_view == 'alerts':
            self.render_alerts_view()
        elif st.session_state.current_view == 'historical':
            self.render_historical_view()
            
    def render_premium_header(self):
        """Render premium application header"""
        col1, col2, col3 = st.columns([2, 3, 2])
        
        with col1:
            if st.session_state.location_data:
                location = st.session_state.location_data
                st.markdown(f"""
                    <div style="
                        background: rgba(255, 255, 255, 0.05);
                        padding: 12px 20px;
                        border-radius: 12px;
                        border: 1px solid rgba(255, 255, 255, 0.1);
                    ">
                        <div style="color: white; font-weight: 600; font-size: 16px;">
                            📍 {location['city']}, {location['country']}
                        </div>
                        <div style="color: rgba(255, 255, 255, 0.6); font-size: 12px;">
                            {location['lat']:.4f}, {location['lon']:.4f}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Premium search bar
            self.render_premium_search(suffix="_header")
        
        with col3:
            # Current time and weather summary
            now = datetime.now()
            if st.session_state.weather_data:
                temp = st.session_state.weather_data['main']['temp']
                condition = st.session_state.weather_data['weather'][0]['description'].title()
                temp_unit = "°C" if st.session_state.units == "metric" else "°F"
                
                st.markdown(f"""
                    <div style="text-align: right;">
                        <div style="color: white; font-weight: 600; font-size: 16px;">
                            {temp:.0f}{temp_unit} • {condition}
                        </div>
                        <div style="color: rgba(255, 255, 255, 0.6); font-size: 12px;">
                            {now.strftime('%H:%M, %A %d %B')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    def render_premium_search(self, suffix=""):
        """Render premium search interface"""
        st.markdown('<div class="premium-search-container">', unsafe_allow_html=True)
        
        search_query = st.text_input(
            "",
            placeholder="🔍 Search locations, coordinates, or points of interest...",
            key=f"premium_search{suffix}",
            label_visibility="collapsed"
        )
        
        if search_query:
            suggestions = self.location_detector.search_location_advanced(search_query)
            if suggestions:
                selected = st.selectbox(
                    "Suggestions",
                    suggestions,
                    format_func=lambda x: x['display_name'],
                    key="search_suggestions",
                    label_visibility="collapsed"
                )
                
                if st.button("🎯 Go to Location", use_container_width=True):
                    self.handle_location_selection(selected)
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _get_tile_coords(self, lat: float, lon: float, zoom: int) -> tuple[int, int]:
        """Convert lat/lon to slippy map tile coordinates."""
        lat_rad = math.radians(lat)
        n = 2.0 ** zoom
        xtile = int((lon + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return xtile, ytile
    
    def render_dashboard_view(self):
        """Render premium dashboard with customizable widgets"""
        if not st.session_state.weather_data:
            self.render_welcome_screen()
            return
        
        # Hero weather section
        self.render_hero_weather_section()
        
        # Customizable widget grid
        st.markdown("### 📊 Weather Intelligence Dashboard")
        
        # Widget configuration
        available_widgets = {
            'current_weather': 'Current Conditions',
            'hourly_forecast': '24-Hour Forecast',
            'weekly_forecast': '7-Day Forecast',
            'air_quality': 'Air Quality Index',
            'uv_index': 'UV Index & Solar',
            'pressure_trends': 'Atmospheric Pressure',
            'wind_analysis': 'Wind Conditions',
            'precipitation': 'Precipitation Radar',
            'satellite': 'Satellite Imagery',
            'alerts': 'Weather Alerts'
        }
        
        # Widget selector
        col1, col2 = st.columns([3, 1])
        with col2:
            valid_default_widgets = [widget for widget in st.session_state.dashboard_widgets if widget in available_widgets]

            selected_widgets = st.multiselect(
                "Customize Dashboard",
                list(available_widgets.keys()),
                default=valid_default_widgets, 
                format_func=lambda x: available_widgets[x]
            )
            st.session_state.dashboard_widgets = selected_widgets
        
        # Render selected widgets
        if selected_widgets:
            # Create responsive grid
            cols_per_row = 2
            for i in range(0, len(selected_widgets), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, widget in enumerate(selected_widgets[i:i+cols_per_row]):
                    with cols[j]:
                        self.render_widget(widget)
        
    def render_widget(self, widget_type):
        """Render individual dashboard widgets"""
        with st.container():
            if widget_type == 'current_weather':
                self.render_current_weather_widget()
            elif widget_type == 'hourly_forecast':
                self.render_hourly_forecast_widget()
            elif widget_type == 'weekly_forecast':
                self.render_weekly_forecast_widget()
            elif widget_type == 'air_quality':
                self.render_air_quality_widget()
            elif widget_type == 'uv_index':
                self.render_uv_index_widget()
            elif widget_type == 'pressure_trends':
                self.render_pressure_trends_widget()
            elif widget_type == 'wind_analysis':
                self.render_wind_analysis_widget()
            elif widget_type == 'precipitation':
                self.render_precipitation_widget()
            elif widget_type == 'satellite':
                self.render_satellite_widget()
            elif widget_type == 'alerts':
                self.render_alerts_widget()
    
    def render_hero_weather_section(self):
        """Render the main hero weather display"""
        weather = st.session_state.weather_data
        
        # Create hero section with premium styling
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(124, 58, 237, 0.1));
                border-radius: 24px;
                padding: 40px;
                margin: 20px 0;
                border: 1px solid rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                position: relative;
                overflow: hidden;
            ">
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            icon_code = weather['weather'][0]['icon']
            condition = weather['weather'][0]['main'].lower()
            st.markdown(
                self.ui.create_animated_weather_icon(icon_code, condition, size="120px"),
                unsafe_allow_html=True
            )
        
        with col2:
            temp_unit = "°C" if st.session_state.units == "metric" else "°F"
            temp = weather['main']['temp']
            condition = weather['weather'][0]['description'].title()
            feels_like = weather['main']['feels_like']
            
            st.markdown(f"""
                <div style="text-align: center;">
                    <div style="
                        font-size: 4rem;
                        font-weight: 800;
                        background: linear-gradient(135deg, #ffffff, #e2e8f0);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        line-height: 0.9;
                        margin-bottom: 10px;
                    ">{temp:.0f}{temp_unit}</div>
                    <div style="
                        font-size: 1.5rem;
                        color: rgba(255, 255, 255, 0.9);
                        margin-bottom: 10px;
                        font-weight: 500;
                    ">{condition}</div>
                    <div style="
                        font-size: 1rem;
                        color: rgba(255, 255, 255, 0.6);
                    ">Feels like {feels_like:.0f}{temp_unit}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            humidity = weather['main']['humidity']
            wind_speed = weather['wind']['speed']
            pressure = weather['main']['pressure']
            
            st.markdown(f"""
                <div style="text-align: center;">
                    <div style="margin-bottom: 15px;">
                        <div style="color: rgba(255, 255, 255, 0.6); font-size: 0.8rem;">HUMIDITY</div>
                        <div style="color: white; font-size: 1.2rem; font-weight: 600;">{humidity}%</div>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <div style="color: rgba(255, 255, 255, 0.6); font-size: 0.8rem;">WIND</div>
                        <div style="color: white; font-size: 1.2rem; font-weight: 600;">{wind_speed:.1f} m/s</div>
                    </div>
                    <div>
                        <div style="color: rgba(255, 255, 255, 0.6); font-size: 0.8rem;">PRESSURE</div>
                        <div style="color: white; font-size: 1.2rem; font-weight: 600;">{pressure} hPa</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Quick metrics bar
        self.render_quick_metrics_bar()
    
    def render_quick_metrics_bar(self):
        """Render quick metrics below hero section"""
        weather = st.session_state.weather_data
        
        metrics = [
            ("🌡️", "Feels Like", f"{weather['main']['feels_like']:.0f}°", "Apparent temperature"),
            ("👁️", "Visibility", f"{weather.get('visibility', 10000)/1000:.1f} km", "Horizontal visibility"),
            ("☁️", "Clouds", f"{weather['clouds']['all']}%", "Cloud coverage"),
            ("🌅", "Sunrise", datetime.fromtimestamp(weather['sys']['sunrise']).strftime('%H:%M'), "Local sunrise"),
            ("🌇", "Sunset", datetime.fromtimestamp(weather['sys']['sunset']).strftime('%H:%M'), "Local sunset"),
            ("🧭", "Direction", self.data_processor.format_wind_direction(weather['wind'].get('deg', 0)), "Wind direction")
        ]
        
        cols = st.columns(len(metrics))
        for i, (icon, label, value, description) in enumerate(metrics):
            with cols[i]:
                st.markdown(f"""
                    <div class="metric-card" style="text-align: center; padding: 16px;">
                        <div class="metric-icon">{icon}</div>
                        <div class="metric-value" style="font-size: 18px;">{value}</div>
                        <div class="metric-label" style="font-size: 11px;">{label}</div>
                    </div>
                """, unsafe_allow_html=True)
    
    def render_welcome_screen(self):
        """Render premium welcome screen"""
        st.markdown("""
            <div style="
                text-align: center;
                padding: 60px 40px;
                background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(124, 58, 237, 0.1));
                border-radius: 24px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                margin: 40px 0;
            ">
                <h1 style="
                    font-size: 3rem;
                    font-weight: 800;
                    background: linear-gradient(135deg, var(--primary), var(--accent));
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin-bottom: 20px;
                ">🌤️ Welcome to Climatrack Premium</h1>
                <p style="
                    font-size: 1.2rem;
                    color: rgba(255, 255, 255, 0.8);
                    margin-bottom: 30px;
                    max-width: 600px;
                    margin-left: auto;
                    margin-right: auto;
                    line-height: 1.6;
                ">
                    Experience the world's most advanced weather intelligence platform with AI-powered insights,
                    premium visualizations, and real-time global weather data.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Feature highlights
        col1, col2, col3 = st.columns(3)
        
        features = [
            ("🎯", "Precision Forecasting", "AI-powered weather predictions with unprecedented accuracy"),
            ("🌍", "Global Coverage", "Real-time weather data from thousands of stations worldwide"),
            ("📊", "Advanced Analytics", "Comprehensive weather trends and historical analysis"),
        ]
        
        for i, (icon, title, description) in enumerate(features):
            with [col1, col2, col3][i]:
                st.markdown(f"""
                    <div style="
                        text-align: center;
                        padding: 30px 20px;
                        background: rgba(255, 255, 255, 0.03);
                        border-radius: 16px;
                        border: 1px solid rgba(255, 255, 255, 0.1);
                        backdrop-filter: blur(10px);
                        margin: 10px 0;
                        transition: transform 0.3s ease;
                    ">
                        <div style="font-size: 2.5rem; margin-bottom: 15px;">{icon}</div>
                        <h3 style="color: white; margin-bottom: 10px; font-size: 1.1rem;">{title}</h3>
                        <p style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; line-height: 1.4;">{description}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        # Call to action
        st.markdown("### 🌍 Get Started")
    
    def render_forecast_view(self):
        """Render the 7-day extended forecast view with advanced analytics."""
        st.markdown("## 📅 Extended Forecast")

        if not st.session_state.get('processed_forecast_data'):
            st.info("Search for a location to see the extended forecast.")
            return

        forecast_data = st.session_state.processed_forecast_data

        with st.container():
            st.markdown("#### Forecast Overview")
            fig = go.Figure()

            dates = [day['date'] for day in forecast_data]
            temp_max = [day['temp_max'] for day in forecast_data]
            temp_min = [day['temp_min'] for day in forecast_data]
            precip_chance = [day['precipitation_chance'] for day in forecast_data]

            fig.add_trace(go.Scatter(x=dates, y=temp_max, name='Max Temp', mode='lines+markers',
                                     line=dict(color='var(--warm)', width=3), marker=dict(size=8)))
            fig.add_trace(go.Scatter(x=dates, y=temp_min, name='Min Temp', mode='lines+markers',
                                     line=dict(color='var(--cold)', width=3), marker=dict(size=8)))
            primary_hex = self.ui.themes['premium_dark']['primary']
            primary_rgb = self.ui._hex_to_rgb(primary_hex)
            fig.add_trace(go.Bar(x=dates, y=precip_chance, name='Precipitation',
                                 marker=dict(color=f'rgba({primary_rgb}, 0.5)'), yaxis='y2'))

            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis=dict(title='Temperature (°C)'),
                yaxis2=dict(title='Precipitation (%)', overlaying='y', side='right', range=[0, 100]),
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        for day in forecast_data:
            with st.expander(f"{day['day_full']}, {day['date'].strftime('%b %d')} - {day['condition']}", expanded=day['date'].date() == datetime.now().date()):
                cols = st.columns([1, 2])
                with cols[0]:
                    st.image(f"http://openweathermap.org/img/wn/{day['icon']}@4x.png", width=128)
                    st.markdown(f"<p style='text-align:center; color: var(--accent);'>{day['comfort_level']} Comfort ({day['comfort_score']:.0f}%)</p>", unsafe_allow_html=True)

                with cols[1]:
                    metric_cols = st.columns(3)
                    with metric_cols[0]:
                        st.metric("Temperature", f"{day['temp_avg']:.0f}°C", f"{day['temp_max']:.0f}° / {day['temp_min']:.0f}°")
                        st.metric("Precipitation", f"{day['precipitation_chance']:.0f}%", f"{day['precipitation_avg']:.1f} mm")
                    with metric_cols[1]:
                        st.metric("Wind", f"{day['wind_speed']:.1f} m/s", self.data_processor.format_wind_direction(day['wind_direction_avg']))
                        st.metric("Humidity", f"{day['humidity']:.0f}%", f"{day['humidity_range']:.0f}% range")
                    with metric_cols[2]:
                        st.metric("Pressure", f"{day['pressure_avg']:.0f} hPa", day['pressure_trend'].title())
                        st.metric("UV Index", f"{day['uv_index_max']:.1f}", "Max Daily")

    def render_radar_view(self):
        """Render the weather radar view using an embedded map."""
        st.markdown("## 🗺️ Weather Radar")
        if not st.session_state.get('location_data'):
            st.info("Search for a location to view the weather radar.")
            return
        lat = st.session_state.location_data['lat']
        lon = st.session_state.location_data['lon']
        embed_url = f"https://embed.windy.com/embed2.html?lat={lat}&lon={lon}&zoom=8&level=surface&overlay=radar&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=m%2Fs&metricTemp=%C2%B0C&radarRange=-1"
        st.components.v1.html(f'<iframe width="100%" height="600" src="{embed_url}" frameborder="0"></iframe>', height=610)

    def render_maps_view(self):
            """Render various interactive weather map layers."""
            st.markdown("## 🌍 Interactive Weather Maps")

            if not st.session_state.get('location_data'):
                st.info("Search for a location to explore weather maps.")
                return

            map_layers = {
                'Temperature': 'temp_new',
                'Precipitation': 'precipitation_new',
                'Wind Speed': 'wind_new',
                'Pressure': 'pressure_new',
                'Clouds': 'clouds_new'
            }

            selected_layer_name = st.selectbox("Select Map Layer", list(map_layers.keys()))
            selected_layer_code = map_layers[selected_layer_name]

            lat = st.session_state.location_data['lat']
            lon = st.session_state.location_data['lon']
            zoom = 6

            # CORRECTED: Convert lat/lon to the correct tile coordinates
            xtile, ytile = self._get_tile_coords(lat, lon, zoom)

            # Build the URL with the correct x and y tile values
            tile_url = f"https://tile.openweathermap.org/map/{selected_layer_code}/{zoom}/{xtile}/{ytile}.png?appid={self.weather_api.api_key}"
            
            st.markdown(f"#### {selected_layer_name} Map")
            st.image(tile_url, caption=f"Weather map layer showing {selected_layer_name.lower()}.", use_column_width=True)
            st.info("Note: For a fully interactive map experience, integration with a mapping library like Folium or Leaflet is recommended. This view displays the relevant map tile for the selected location.")

    def render_analytics_view(self):
            """Render the weather analytics view with trend analysis."""
            st.markdown("## 📊 Weather Analytics")

            if not st.session_state.get('processed_forecast_data'):
                st.info("Search for a location to generate weather analytics.")
                return

            forecast_data = st.session_state.processed_forecast_data
            trends = self.data_processor.calculate_weather_trends_advanced(forecast_data)

            st.markdown("#### Key Trends for the Next 7 Days")
            cols = st.columns(4)
            
            with cols[0]:
                temp_trend = trends['temperature']['avg_trend']
                # CORRECTED: Using st.components.v1.html for robust rendering
                st.components.v1.html(self.ui.create_premium_metric_card("🌡️", "Temperature Trend", temp_trend['direction'].title(), f"{temp_trend['slope']:.1f}°/day"))
            with cols[1]:
                pressure_trend = trends['pressure']['trend']
                # CORRECTED: Using st.components.v1.html for robust rendering
                st.components.v1.html(self.ui.create_premium_metric_card("💨", "Pressure Trend", pressure_trend['direction'].title(), f"{pressure_trend['slope']:.1f} hPa/day"))
            with cols[2]:
                comfort_trend = trends['comfort']['trend']
                # CORRECTED: Using st.components.v1.html for robust rendering
                st.components.v1.html(self.ui.create_premium_metric_card("😊", "Comfort Trend", comfort_trend['direction'].title(), f"{comfort_trend['slope']:.1f}%/day"))
            with cols[3]:
                change_prob = trends['pressure']['weather_change_likelihood']['probability']
                # CORRECTED: Using st.components.v1.html for robust rendering
                st.components.v1.html(self.ui.create_premium_metric_card("🔄", "Change Likelihood", f"{change_prob:.0%}", "Chance of pattern shift"))

            # --- Detailed Analytics Sections --- (This part remains unchanged)
            with st.expander("🌡️ Temperature Deep Dive", expanded=True):
                temp_analytics = trends['temperature']
                st.markdown(f"**Volatility:** {temp_analytics['volatility']:.2f}°C (day-to-day fluctuation)")
                st.markdown(f"**Heat Wave Risk:** {temp_analytics['heat_wave_risk']:.0%}")
                st.markdown(f"**Cold Snap Risk:** {temp_analytics['cold_snap_risk']:.0%}")
                diurnal_trend = temp_analytics['diurnal_range_trend']
                st.markdown(f"**Daily Temp Range Trend:** {diurnal_trend['direction'].title()} ({diurnal_trend['slope']:.2f}°C/day)")

            with st.expander("😊 Comfort & Activity Forecast", expanded=True):
                comfort_analytics = trends['comfort']
                st.markdown(f"**Average Comfort Score:** {comfort_analytics['avg']:.0f}%")
                st.markdown(f"**Forecast Quality:** {comfort_analytics['forecast_quality']['quality'].title()}")
                st.markdown("**Optimal Days:**")
                for day in comfort_analytics['optimal_days']:
                    st.markdown(f"- **{day['day']}**: Score {day['overall_score']:.0f}/100 ({', '.join(day['reasons'])})")

    def render_compare_view(self):
        """Render the location comparison view."""
        st.markdown("## ⚖️ Location Comparison")
        if 'comparison_locations_data' not in st.session_state:
            st.session_state.comparison_locations_data = {}
        new_location_query = st.text_input("Add a location to compare (e.g., 'Paris, FR')")
        if new_location_query:
            suggestions = self.location_detector.search_location_advanced(new_location_query, limit=1)
            if suggestions:
                location_info = suggestions[0]
                location_key = location_info['display_name']
                if location_key not in st.session_state.comparison_locations_data:
                    with st.spinner(f"Fetching weather for {location_key}..."):
                        weather_data = self.weather_api.get_current_weather_enhanced(location_info['lat'], location_info['lon'])
                        if weather_data:
                            st.session_state.comparison_locations_data[location_key] = weather_data
                            st.rerun()
        if not st.session_state.comparison_locations_data:
            st.info("Add one or more locations to start comparing their current weather conditions.")
            return
        locations = list(st.session_state.comparison_locations_data.keys())
        cols = st.columns(len(locations))
        for i, loc_name in enumerate(locations):
            with cols[i]:
                weather = st.session_state.comparison_locations_data[loc_name]
                st.markdown(f"#### {loc_name}")
                st.image(f"http://openweathermap.org/img/wn/{weather['weather'][0]['icon']}@2x.png", width=80)
                st.metric("Temperature", f"{weather['main']['temp']:.1f}°C", f"Feels like {weather['main']['feels_like']:.1f}°C")
                st.metric("Condition", weather['weather'][0]['description'].title())
                st.metric("Wind", f"{weather['wind']['speed']:.1f} m/s", self.data_processor.format_wind_direction(weather['wind'].get('deg')))
                st.metric("Humidity", f"{weather['main']['humidity']}%")
                if st.button("Remove", key=f"remove_{loc_name}"):
                    del st.session_state.comparison_locations_data[loc_name]
                    st.rerun()

    def render_alerts_view(self):
        """Render the weather alerts view."""
        st.markdown("## 🚨 Weather Alerts")
        if not st.session_state.get('location_data'):
            st.info("Search for a location to check for active weather alerts.")
            return
        with st.spinner("Checking for weather alerts..."):
            lat = st.session_state.location_data['lat']
            lon = st.session_state.location_data['lon']
            alerts = self.weather_api.get_weather_alerts_advanced(lat, lon)
        if not alerts:
            st.success("✅ No active weather alerts for the selected location.")
            return
        for alert in alerts:
            severity = alert.get('severity_level', 'medium')
            if severity in ['extreme', 'high']:
                st.error(f"**{alert['event']}** from {alert['sender_name']}")
            elif severity == 'medium':
                st.warning(f"**{alert['event']}** from {alert['sender_name']}")
            else:
                st.info(f"**{alert['event']}** from {alert['sender_name']}")

    def render_historical_view(self):
        """Render the historical weather data view."""
        st.markdown("## 📈 Historical Data")
        if not st.session_state.get('location_data'):
            st.info("Search for a location to look up historical weather data.")
            return
        st.warning("📜 Accessing historical data may require a premium API subscription.")
        today = datetime.now()
        selected_date = st.date_input("Select a date", today, max_value=today)
        if st.button("Fetch Historical Weather"):
            with st.spinner(f"Fetching weather data for {selected_date.strftime('%Y-%m-%d')}..."):
                lat = st.session_state.location_data['lat']
                lon = st.session_state.location_data['lon']
                historical_data = self.weather_api.get_historical_weather_advanced(lat, lon, selected_date)
            if historical_data and 'current' in historical_data:
                st.success(f"Data for {selected_date.strftime('%Y-%m-%d')} loaded.")
                data = historical_data['current']
                st.markdown(f"### Weather on {data['date_info']['target_date']}")
                cols = st.columns(3)
                cols[0].metric("Temperature", f"{data['temp']:.1f}°C", f"Feels like {data['feels_like']:.1f}°C")
                cols[1].metric("Condition", data['weather'][0]['description'].title())
                cols[2].metric("Wind Speed", f"{data['wind_speed']:.1f} m/s")
            else:
                st.error("Could not retrieve historical data. This may be a premium feature not available on your API key.")

    def render_current_weather_widget(self):
        """Render a detailed widget for current conditions."""
        st.markdown("#### ⚡ Current Conditions")
        if st.session_state.get('weather_data'):
            weather = st.session_state.weather_data
            cols = st.columns(2)
            cols[0].metric("Humidity", f"{weather['main']['humidity']}%")
            cols[0].metric("Pressure", f"{weather['main']['pressure']} hPa")
            cols[1].metric("Visibility", f"{weather.get('visibility', 10000) / 1000:.1f} km")
            cols[1].metric("Cloud Cover", f"{weather['clouds']['all']}%")
        else:
            st.write("No data available.")

    def render_hourly_forecast_widget(self):
        """Render a widget with a 24-hour forecast chart."""
        st.markdown("#### 🕒 24-Hour Forecast")
        if st.session_state.get('hourly_data'):
            hourly_data = st.session_state.hourly_data[:24]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=[h['time'] for h in hourly_data], y=[h['temp'] for h in hourly_data], name='Temperature', mode='lines+markers', line=dict(color='var(--primary)')))
            fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=200, margin=dict(l=0, r=0, t=0, b=0), xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No data available.")

    def render_weekly_forecast_widget(self):
        """Render a compact 7-day forecast widget."""
        st.markdown("#### 🗓️ 7-Day Forecast")
        if st.session_state.get('processed_forecast_data'):
            forecast = st.session_state.processed_forecast_data
            for day in forecast:
                cols = st.columns([1, 2, 1])
                with cols[0]:
                    st.write(day['day'])
                with cols[1]:
                    st.image(f"http://openweathermap.org/img/wn/{day['icon']}.png", width=32)
                with cols[2]:
                    st.write(f"{day['temp_max']:.0f}°/{day['temp_min']:.0f}°")
        else:
            st.write("No data available.")

    def render_air_quality_widget(self):
        """Render an AQI widget."""
        st.markdown("#### 🌬️ Air Quality")
        aqi_full_data = st.session_state.get('air_quality_data')
        if aqi_full_data and 'list' in aqi_full_data and aqi_full_data['list']:
            aqi_data = aqi_full_data['list'][0]
            aqi = aqi_data['main']['aqi']
            level_info = self.weather_api._get_aqi_health_info(aqi)
            level = level_info['level']
            color_map = {'Good': '#10b981', 'Fair': '#f59e0b', 'Moderate': '#f97316', 'Poor': '#ef4444', 'Very Poor': '#dc2626'}
            st.markdown(self.ui.create_aqi_indicator(aqi, level, color_map.get(level, '#f97316')), unsafe_allow_html=True)
        else:
            st.write("No air quality data available.")

    def render_uv_index_widget(self):
        """Render a widget for UV index."""
        st.markdown("#### ☀️ UV Index & Solar")
        if st.session_state.get('weather_data'):
            weather = st.session_state.weather_data
            sunrise = datetime.fromtimestamp(weather['sys']['sunrise']).strftime('%H:%M')
            sunset = datetime.fromtimestamp(weather['sys']['sunset']).strftime('%H:%M')
            st.metric("Sunrise", sunrise)
            st.metric("Sunset", sunset)
        else:
            st.write("No data available.")

    def render_pressure_trends_widget(self):
        """Render a widget for atmospheric pressure trends."""
        st.markdown("#### 📈 Atmospheric Pressure")
        if st.session_state.get('processed_forecast_data'):
            pressure_data = [d['pressure_avg'] for d in st.session_state.processed_forecast_data]
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=pressure_data, mode='lines', line=dict(color='var(--accent)')))
            fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=150, margin=dict(l=0, r=0, t=0, b=0), xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No data available.")

    def render_wind_analysis_widget(self):
        """Render a widget for wind conditions."""
        st.markdown("#### 💨 Wind Conditions")
        if st.session_state.get('weather_data'):
            wind = st.session_state.weather_data['wind']
            st.metric("Wind Speed", f"{wind['speed']:.1f} m/s")
            st.metric("Direction", self.data_processor.format_wind_direction(wind.get('deg')))
            if 'gust' in wind:
                st.metric("Gusts", f"{wind['gust']:.1f} m/s")
        else:
            st.write("No data available.")

    def render_precipitation_widget(self):
        """Render a placeholder widget for precipitation."""
        st.markdown("#### 💧 Precipitation")
        st.info("Precipitation radar map widget coming soon.")

    def render_satellite_widget(self):
        """Render a placeholder widget for satellite imagery."""
        st.markdown("####🛰️ Satellite")
        st.info("Satellite imagery widget coming soon.")

    def render_alerts_widget(self):
        """Render a compact widget for weather alerts."""
        st.markdown("#### 🚨 Alerts")
        if st.session_state.get('location_data'):
            lat = st.session_state.location_data['lat']
            lon = st.session_state.location_data['lon']
            alerts = self.weather_api.get_weather_alerts_advanced(lat, lon)
            if alerts:
                for alert in alerts[:1]:
                    st.warning(f"**{alert['event']}**: {alert['description'][:50]}...")
            else:
                st.success("No active alerts.")
        else:
            st.write("No location selected.")
    
    # Additional methods for other views...
    def refresh_weather_data(self):
        """Refresh weather data for current location"""
        if st.session_state.location_data:
            self.fetch_weather_data(
                st.session_state.location_data['lat'],
                st.session_state.location_data['lon']
            )
    
    def add_current_to_favorites(self):
        """Add current location to favorites"""
        if st.session_state.location_data:
            if st.session_state.location_data not in st.session_state.favorite_locations:
                st.session_state.favorite_locations.append(st.session_state.location_data)
                st.success("Location added to favorites!")
            else:
                st.info("Location already in favorites!")
    
    def handle_quick_location(self, location):
        """Handle quick location selection"""
        if location == "auto":
            if self.location_detector.get_location_with_ai_enhancement():
                self.refresh_weather_data()
        else:
            location_data = self.location_detector.search_location_advanced(location)
            if location_data:
                st.session_state.location_data = location_data[0] # Take the first result
                self.refresh_weather_data()
    
    def handle_location_selection(self, location_data):
        """Handle location selection from search"""
        st.session_state.location_data = {
            'city': location_data['city'],
            'country': location_data['country'],
            'lat': location_data['lat'],
            'lon': location_data['lon']
        }
        st.session_state.app_usage_stats['locations_searched'] += 1
        self.refresh_weather_data()
    
    def fetch_weather_data(self, lat, lon):
        """Fetch comprehensive weather data"""
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("☁️ Fetching current conditions...")
            progress_bar.progress(20)
            current_weather = self.weather_api.get_current_weather_enhanced(lat, lon, st.session_state.units)
            
            status_text.text("📅 Loading forecast data...")
            progress_bar.progress(50)
            forecast = self.weather_api.get_forecast_enhanced(lat, lon, st.session_state.units)
            
            status_text.text("🌬️ Checking air quality...")
            progress_bar.progress(80)
            air_quality = self.weather_api.get_air_quality_enhanced(lat, lon)
            
            if current_weather:
                st.session_state.weather_data = current_weather
            if forecast:
                st.session_state.forecast_data = forecast
                st.session_state.processed_forecast_data = self.data_processor.process_forecast_data_advanced(forecast)
            if air_quality:
                st.session_state.air_quality_data = air_quality
            
            st.session_state.last_update = datetime.now()
            
            status_text.text("✅ All data loaded successfully!")
            progress_bar.progress(100)
            time.sleep(0.5)
            
        finally:
            progress_bar.empty()
            status_text.empty()
    
    def run(self):
            """Main application runner"""
            self.initialize_session_state()
            self.load_premium_styling()
            
            self.render_premium_sidebar()
            self.render_content_area()

if __name__ == "__main__":
    app = PremiumWeatherApp()
    app.run()
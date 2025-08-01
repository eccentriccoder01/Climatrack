import streamlit as st
from typing import Dict, Any

class UIComponents:
    """Handles UI components and custom styling"""
    
    def __init__(self):
        self.theme = "aurora"  # Unique aurora-inspired theme
    
    def load_custom_css(self):
        """Load custom CSS styling with aurora theme"""
        st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        /* Root Variables - Aurora Theme */
        :root {
            --aurora-primary: #00d4ff;
            --aurora-secondary: #7c3aed;
            --aurora-accent: #06ffa5;
            --aurora-warm: #ff6b35;
            --aurora-cold: #4facfe;
            --aurora-dark: #0a0a0f;
            --aurora-darker: #050507;
            --aurora-light: #ffffff;
            --aurora-gray: #6b7280;
            --aurora-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --aurora-glow: 0 0 20px rgba(0, 212, 255, 0.3);
            --aurora-glow-warm: 0 0 25px rgba(255, 107, 53, 0.4);
        }
        
        /* Global Styles */
        .main {
            background: linear-gradient(145deg, #0a0a0f 0%, #1a0b2e 50%, #16213e 100%);
            min-height: 100vh;
            font-family: 'Inter', sans-serif;
        }
        
        /* Hide Streamlit Elements */
        .stDeployButton {display: none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stAppViewBlockContainer {padding-top: 2rem;}
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--aurora-darker);
        }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, var(--aurora-primary), var(--aurora-secondary));
            border-radius: 4px;
        }
        
        /* Header Styles */
        .main-header {
            text-align: center;
            margin: 2rem 0 3rem 0;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 20px;
            border: 1px solid rgba(0, 212, 255, 0.1);
            backdrop-filter: blur(20px);
            box-shadow: var(--aurora-glow);
        }
        
        .main-header h1 {
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--aurora-primary), var(--aurora-accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
        }
        
        .main-header p {
            font-size: 1.2rem;
            color: var(--aurora-gray);
            font-weight: 300;
            margin: 0;
        }
        
        /* Welcome Section */
        .welcome-section {
            text-align: center;
            margin: 3rem 0;
            padding: 3rem 2rem;
            background: rgba(124, 58, 237, 0.05);
            border-radius: 25px;
            border: 1px solid rgba(124, 58, 237, 0.2);
            backdrop-filter: blur(15px);
        }
        
        .welcome-section h2 {
            font-size: 2.5rem;
            font-weight: 600;
            color: var(--aurora-light);
            margin-bottom: 1rem;
        }
        
        .welcome-section p {
            font-size: 1.1rem;
            color: var(--aurora-gray);
            margin: 0;
        }
        
        /* Search Container */
        .search-container {
            margin: 2rem 0;
            padding: 1.5rem;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 20px;
            border: 1px solid rgba(6, 255, 165, 0.1);
            backdrop-filter: blur(10px);
        }
        
        /* Input Styling */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 2px solid rgba(0, 212, 255, 0.3) !important;
            border-radius: 15px !important;
            color: var(--aurora-light) !important;
            font-size: 1rem !important;
            padding: 0.75rem 1rem !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: var(--aurora-primary) !important;
            box-shadow: var(--aurora-glow) !important;
            background: rgba(255, 255, 255, 0.08) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: var(--aurora-gray) !important;
        }
        
        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, var(--aurora-primary), var(--aurora-secondary)) !important;
            border: none !important;
            border-radius: 15px !important;
            color: white !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            padding: 0.75rem 2rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3) !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(0, 212, 255, 0.4) !important;
            background: linear-gradient(135deg, var(--aurora-accent), var(--aurora-primary)) !important;
        }
        
        /* Weather Cards */
        .weather-card {
            background: rgba(255, 255, 255, 0.04);
            border-radius: 25px;
            padding: 2rem;
            margin: 1.5rem 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        .weather-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 212, 255, 0.2);
            border-color: rgba(0, 212, 255, 0.3);
        }
        
        .current-weather {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(124, 58, 237, 0.1));
            border: 1px solid rgba(0, 212, 255, 0.2);
        }
        
        /* Location Info */
        .location-info h2 {
            font-size: 1.8rem;
            font-weight: 600;
            color: var(--aurora-light);
            margin-bottom: 0.5rem;
        }
        
        .timestamp {
            color: var(--aurora-gray);
            font-size: 0.9rem;
            font-family: 'JetBrains Mono', monospace;
            margin: 0;
        }
        
        /* Temperature Display */
        .temperature-display {
            text-align: center;
        }
        
        .temp-main {
            font-size: 4rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--aurora-warm), var(--aurora-cold));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: block;
            line-height: 1;
        }
        
        .temp-desc {
            font-size: 1.1rem;
            color: var(--aurora-gray);
            text-transform: capitalize;
            font-weight: 500;
        }
        
        /* Weather Icon */
        .weather-icon {
            text-align: center;
        }
        
        .weather-icon img {
            width: 120px;
            height: 120px;
            filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.3));
        }
        
        /* Details Grid */
        .details-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
        }
        
        .detail-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }
        
        .detail-card:hover {
            background: rgba(6, 255, 165, 0.1);
            border-color: rgba(6, 255, 165, 0.3);
            transform: translateY(-3px);
        }
        
        .detail-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        .detail-label {
            font-size: 0.9rem;
            color: var(--aurora-gray);
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        .detail-value {
            font-size: 1.3rem;
            color: var(--aurora-light);
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
        }
        
        /* Forecast Section */
        .forecast-section {
            margin: 3rem 0;
        }
        
        .forecast-section h3 {
            font-size: 2rem;
            font-weight: 600;
            color: var(--aurora-light);
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .forecast-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }
        
        .forecast-card {
            background: rgba(255, 255, 255, 0.04);
            border-radius: 20px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        
        .forecast-card:hover {
            background: rgba(255, 107, 53, 0.1);
            border-color: rgba(255, 107, 53, 0.3);
            transform: translateY(-5px);
            box-shadow: var(--aurora-glow-warm);
        }
        
        .forecast-day {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--aurora-light);
            margin-bottom: 1rem;
        }
        
        .forecast-icon img {
            width: 60px;
            height: 60px;
            margin: 0.5rem 0;
        }
        
        .forecast-temps {
            margin: 1rem 0;
        }
        
        .temp-high {
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--aurora-warm);
            margin-right: 0.5rem;
        }
        
        .temp-low {
            font-size: 1.1rem;
            font-weight: 500;
            color: var(--aurora-cold);
        }
        
        .forecast-desc {
            font-size: 0.9rem;
            color: var(--aurora-gray);
            margin: 0.5rem 0;
            text-transform: capitalize;
        }
        
        .forecast-details {
            font-size: 0.8rem;
            color: var(--aurora-gray);
            font-family: 'JetBrains Mono', monospace;
        }
        
        /* Chart Section */
        .chart-section {
            margin: 3rem 0;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 25px;
            padding: 2rem;
            border: 1px solid rgba(124, 58, 237, 0.2);
        }
        
        .chart-section h3 {
            font-size: 1.8rem;
            font-weight: 600;
            color: var(--aurora-light);
            margin-bottom: 1.5rem;
            text-align: center;
        }
        
        /* Air Quality Section */
        .air-quality-section {
            margin: 3rem 0;
            background: rgba(6, 255, 165, 0.05);
            border-radius: 25px;
            padding: 2rem;
            border: 1px solid rgba(6, 255, 165, 0.2);
        }
        
        .air-quality-section h3 {
            font-size: 1.8rem;
            font-weight: 600;
            color: var(--aurora-light);
            margin-bottom: 1.5rem;
        }
        
        .aqi-indicator {
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            color: white;
            font-weight: bold;
        }
        
        .aqi-value {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .aqi-level {
            font-size: 1.2rem;
            font-weight: 500;
        }
        
        .aqi-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1rem;
            align-items: center;
        }
        
        .aqi-component {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            color: var(--aurora-light);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin: 4rem 0 2rem 0;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--aurora-gray);
        }
        
        .footer p {
            margin: 0.5rem 0;
            font-size: 0.9rem;
        }
        
        /* Selectbox Styling */
        .stSelectbox > div > div > select {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 2px solid rgba(0, 212, 255, 0.3) !important;
            border-radius: 10px !important;
            color: var(--aurora-light) !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Expander Styling */
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.05) !important;
            border-radius: 10px !important;
            border: 1px solid rgba(0, 212, 255, 0.2) !important;
            color: var(--aurora-light) !important;
        }
        
        .streamlit-expanderContent {
            background: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(0, 212, 255, 0.1) !important;
            border-radius: 0 0 10px 10px !important;
        }
        
        /* Loading Animation */
        .stSpinner > div {
            border-top-color: var(--aurora-primary) !important;
        }
        
        /* Success/Error Messages */
        .stSuccess {
            background: rgba(6, 255, 165, 0.1) !important;
            border: 1px solid rgba(6, 255, 165, 0.3) !important;
            border-radius: 10px !important;
            color: var(--aurora-accent) !important;
        }
        
        .stError {
            background: rgba(255, 107, 53, 0.1) !important;
            border: 1px solid rgba(255, 107, 53, 0.3) !important;
            border-radius: 10px !important;
            color: var(--aurora-warm) !important;
        }
        
        .stWarning {
            background: rgba(255, 193, 7, 0.1) !important;
            border: 1px solid rgba(255, 193, 7, 0.3) !important;
            border-radius: 10px !important;
            color: #ffc107 !important;
        }
        
        .stInfo {
            background: rgba(0, 212, 255, 0.1) !important;
            border: 1px solid rgba(0, 212, 255, 0.3) !important;
            border-radius: 10px !important;
            color: var(--aurora-primary) !important;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .main-header h1 {
                font-size: 2.5rem;
            }
            
            .temp-main {
                font-size: 3rem;
            }
            
            .details-grid {
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            }
            
            .forecast-grid {
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            }
        }
        
        /* Animation keyframes */
        @keyframes aurora {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes glow {
            0%, 100% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.3); }
            50% { box-shadow: 0 0 30px rgba(0, 212, 255, 0.5); }
        }
        
        .main-header {
            animation: glow 3s ease-in-out infinite;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def create_weather_icon_html(self, icon_code: str, size: str = "60px") -> str:
        """Create HTML for weather icon"""
        return f"""
        <div class="weather-icon-container" style="text-align: center;">
            <img src="http://openweathermap.org/img/wn/{icon_code}@2x.png" 
                 style="width: {size}; height: {size}; filter: drop-shadow(0 0 10px rgba(255,255,255,0.3));" />
        </div>
        """
    
    def create_metric_card(self, icon: str, label: str, value: str, color: str = "var(--aurora-primary)") -> str:
        """Create a metric card HTML"""
        return f"""
        <div class="metric-card" style="
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
            <div style="font-size: 0.9rem; color: var(--aurora-gray); margin-bottom: 0.5rem;">{label}</div>
            <div style="font-size: 1.3rem; color: {color}; font-weight: 600; font-family: 'JetBrains Mono', monospace;">{value}</div>
        </div>
        """
    
    def create_gradient_text(self, text: str, gradient: str = "linear-gradient(135deg, var(--aurora-primary), var(--aurora-accent))") -> str:
        """Create gradient text HTML"""
        return f"""
        <span style="
            background: {gradient};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 600;
        ">{text}</span>
        """
    
    def show_loading_animation(self, message: str = "Loading..."):
        """Show loading animation with custom styling"""
        return st.markdown(f"""
        <div style="
            text-align: center;
            padding: 2rem;
            color: var(--aurora-gray);
            font-family: 'Inter', sans-serif;
        ">
            <div style="
                display: inline-block;
                width: 40px;
                height: 40px;
                border: 3px solid rgba(0, 212, 255, 0.3);
                border-radius: 50%;
                border-top-color: var(--aurora-primary);
                animation: spin 1s ease-in-out infinite;
                margin-bottom: 1rem;
            "></div>
            <p>{message}</p>
        </div>
        """, unsafe_allow_html=True)
import streamlit as st
from typing import Dict, Any, List
import json

class UIComponents:
    """Premium UI components with world-class design and animations"""
    
    def __init__(self):
        self.themes = {
            "aurora": {
                "name": "Aurora Borealis",
                "primary": "#00d4ff",
                "secondary": "#7c3aed",
                "accent": "#06ffa5",
                "warm": "#ff6b35",
                "cold": "#4facfe"
            },
            "sunset": {
                "name": "Golden Sunset",
                "primary": "#ff6b6b",
                "secondary": "#feca57",
                "accent": "#ff9ff3",
                "warm": "#ff7675",
                "cold": "#74b9ff"
            },
            "ocean": {
                "name": "Deep Ocean",
                "primary": "#0984e3",
                "secondary": "#00b894",
                "accent": "#00cec9",
                "warm": "#e17055",
                "cold": "#6c5ce7"
            },
            "forest": {
                "name": "Emerald Forest",
                "primary": "#00b894",
                "secondary": "#00a085",
                "accent": "#55efc4",
                "warm": "#fdcb6e",
                "cold": "#74b9ff"
            }
        }
        self.current_theme = "aurora"
    
    def load_premium_css(self):
        """Load premium CSS with advanced animations and glassmorphism"""
        st.markdown("""
        <style>
        /* Import Premium Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=JetBrains+Mono:wght@100;200;300;400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700;800;900&display=swap');
        
        /* CSS Custom Properties - Dynamic Theme System */
        :root {
            --primary: #00d4ff;
            --secondary: #7c3aed;
            --accent: #06ffa5;
            --warm: #ff6b35;
            --cold: #4facfe;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --info: #3b82f6;
            
            /* Glass Morphism */
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            --glass-backdrop: blur(20px);
            
            /* Spacing System */
            --space-xs: 0.25rem;
            --space-sm: 0.5rem;
            --space-md: 1rem;
            --space-lg: 1.5rem;
            --space-xl: 2rem;
            --space-2xl: 3rem;
            --space-3xl: 4rem;
            
            /* Border Radius */
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 20px;
            --radius-2xl: 24px;
            --radius-full: 9999px;
            
            /* Shadows */
            --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            --shadow-glow: 0 0 20px var(--primary);
            
            /* Animations */
            --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-normal: 300ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-slow: 500ms cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* Global Styles with Advanced Background */
        .main {
            background: 
                radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(120, 200, 255, 0.2) 0%, transparent 50%),
                linear-gradient(135deg, #0a0a0f 0%, #1a0b2e 25%, #16213e 50%, #0f3460 75%, #0a1a2e 100%);
            min-height: 100vh;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            position: relative;
            overflow-x: hidden;
        }
        
        /* Animated Background Particles */
        .main::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(2px 2px at 20px 30px, rgba(255, 255, 255, 0.15), transparent),
                radial-gradient(2px 2px at 40px 70px, rgba(255, 255, 255, 0.1), transparent),
                radial-gradient(1px 1px at 90px 40px, rgba(255, 255, 255, 0.1), transparent),
                radial-gradient(1px 1px at 130px 80px, rgba(255, 255, 255, 0.1), transparent),
                radial-gradient(2px 2px at 160px 30px, rgba(255, 255, 255, 0.1), transparent);
            background-repeat: repeat;
            background-size: 200px 100px;
            animation: sparkle 20s linear infinite;
            pointer-events: none;
            z-index: -1;
        }
        
        @keyframes sparkle {
            0% { transform: translateY(0px); }
            100% { transform: translateY(-100px); }
        }
        
        /* Hide Streamlit Elements */
        .stDeployButton, #MainMenu, footer, header { display: none !important; }
        .stAppViewBlockContainer { padding-top: var(--space-lg); }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.2);
            border-radius: var(--radius-full);
        }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, var(--primary), var(--secondary));
            border-radius: var(--radius-full);
            transition: var(--transition-normal);
        }
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, var(--accent), var(--primary));
        }
        
        /* Premium Header with Advanced Animations */
        .premium-header {
            text-align: center;
            margin: var(--space-xl) 0 var(--space-3xl) 0;
            padding: var(--space-3xl) var(--space-xl);
            background: var(--glass-bg);
            border-radius: var(--radius-2xl);
            border: 1px solid var(--glass-border);
            backdrop-filter: var(--glass-backdrop);
            box-shadow: var(--glass-shadow);
            position: relative;
            overflow: hidden;
        }
        
        .premium-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.03), transparent);
            transform: rotate(45deg);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        .premium-header h1 {
            font-family: 'Playfair Display', serif;
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), var(--accent), var(--secondary));
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: var(--space-md);
            animation: gradient-shift 4s ease-in-out infinite;
            position: relative;
            z-index: 1;
        }
        
        @keyframes gradient-shift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .premium-header p {
            font-size: 1.125rem;
            color: rgba(255, 255, 255, 0.7);
            font-weight: 300;
            letter-spacing: 0.5px;
            margin: 0;
            position: relative;
            z-index: 1;
        }
        
        /* Weather Status Indicator */
        .weather-status {
            display: inline-flex;
            align-items: center;
            gap: var(--space-sm);
            padding: var(--space-sm) var(--space-md);
            background: var(--glass-bg);
            border-radius: var(--radius-full);
            border: 1px solid var(--glass-border);
            font-size: 0.875rem;
            color: rgba(255, 255, 255, 0.8);
            margin-top: var(--space-md);
        }
        
        .status-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--success);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        /* Premium Search Container */
        .premium-search {
            margin: var(--space-xl) 0;
            padding: var(--space-xl);
            background: var(--glass-bg);
            border-radius: var(--radius-xl);
            border: 1px solid var(--glass-border);
            backdrop-filter: var(--glass-backdrop);
            position: relative;
            transition: var(--transition-normal);
        }
        
        .premium-search:hover {
            border-color: rgba(255, 255, 255, 0.2);
            box-shadow: var(--glass-shadow), 0 0 0 1px rgba(255, 255, 255, 0.1);
        }
        
        /* Enhanced Input Styling */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 2px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: var(--radius-lg) !important;
            color: white !important;
            font-size: 1rem !important;
            padding: var(--space-md) var(--space-lg) !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 400 !important;
            transition: var(--transition-normal) !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1), var(--shadow-glow) !important;
            background: rgba(255, 255, 255, 0.08) !important;
            transform: translateY(-1px) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.5) !important;
            font-weight: 300 !important;
        }
        
        /* Premium Button System */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
            border: none !important;
            border-radius: var(--radius-lg) !important;
            color: white !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            padding: var(--space-md) var(--space-xl) !important;
            transition: var(--transition-normal) !important;
            box-shadow: var(--shadow-lg) !important;
            font-family: 'Inter', sans-serif !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .stButton > button::before {
            content: '' !important;
            position: absolute !important;
            top: 0 !important;
            left: -100% !important;
            width: 100% !important;
            height: 100% !important;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent) !important;
            transition: var(--transition-normal) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-xl), var(--shadow-glow) !important;
            background: linear-gradient(135deg, var(--accent), var(--primary)) !important;
        }
        
        .stButton > button:hover::before {
            left: 100% !important;
        }
        
        .stButton > button:active {
            transform: translateY(0px) !important;
        }
        
        /* Premium Weather Cards */
        .premium-weather-card {
            background: var(--glass-bg);
            border-radius: var(--radius-xl);
            padding: var(--space-xl);
            margin: var(--space-lg) 0;
            border: 1px solid var(--glass-border);
            backdrop-filter: var(--glass-backdrop);
            box-shadow: var(--glass-shadow);
            transition: var(--transition-normal);
            position: relative;
            overflow: hidden;
        }
        
        .premium-weather-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--primary), var(--accent), var(--secondary));
            background-size: 200% 100%;
            animation: gradient-shift 3s ease-in-out infinite;
        }
        
        .premium-weather-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--glass-shadow), var(--shadow-xl);
            border-color: rgba(255, 255, 255, 0.15);
        }
        
        /* Advanced Temperature Display */
        .temperature-showcase {
            text-align: center;
            position: relative;
        }
        
        .temp-main {
            font-family: 'Inter', sans-serif;
            font-size: clamp(3rem, 8vw, 5rem);
            font-weight: 800;
            background: linear-gradient(135deg, var(--warm), var(--cold));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: block;
            line-height: 0.9;
            margin-bottom: var(--space-sm);
            position: relative;
        }
        
        .temp-desc {
            font-size: 1.125rem;
            color: rgba(255, 255, 255, 0.8);
            text-transform: capitalize;
            font-weight: 500;
            letter-spacing: 0.5px;
        }
        
        /* Weather Icon with Advanced Animation */
        .weather-icon-container {
            text-align: center;
            position: relative;
        }
        
        .weather-icon-container img {
            width: 120px;
            height: 120px;
            filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.3));
            transition: var(--transition-normal);
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .weather-icon-container:hover img {
            transform: scale(1.1) translateY(-5px);
            filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.5));
        }
        
        /* Premium Details Grid */
        .premium-details-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: var(--space-lg);
            margin-top: var(--space-xl);
        }
        
        .detail-card {
            background: rgba(255, 255, 255, 0.03);
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.08);
            transition: var(--transition-normal);
            position: relative;
            overflow: hidden;
        }
        
        .detail-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at center, var(--primary)20, transparent 70%);
            opacity: 0;
            transition: var(--transition-normal);
        }
        
        .detail-card:hover {
            background: rgba(255, 255, 255, 0.05);
            border-color: var(--primary);
            transform: translateY(-3px);
            box-shadow: var(--shadow-lg);
        }
        
        .detail-card:hover::before {
            opacity: 0.1;
        }
        
        .detail-icon {
            font-size: 2.5rem;
            margin-bottom: var(--space-md);
            filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.3));
            position: relative;
            z-index: 1;
        }
        
        .detail-label {
            font-size: 0.875rem;
            color: rgba(255, 255, 255, 0.6);
            margin-bottom: var(--space-sm);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            position: relative;
            z-index: 1;
        }
        
        .detail-value {
            font-size: 1.5rem;
            color: white;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            position: relative;
            z-index: 1;
        }
        
        /* Premium Forecast Section */
        .premium-forecast {
            margin: var(--space-3xl) 0;
            position: relative;
        }
        
        .section-title {
            font-family: 'Playfair Display', serif;
            font-size: 2.25rem;
            font-weight: 700;
            color: white;
            margin-bottom: var(--space-xl);
            text-align: center;
            position: relative;
        }
        
        .section-title::after {
            content: '';
            position: absolute;
            bottom: -8px;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            border-radius: var(--radius-full);
        }
        
        .forecast-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: var(--space-lg);
            margin: var(--space-xl) 0;
        }
        
        .forecast-card {
            background: var(--glass-bg);
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            text-align: center;
            border: 1px solid var(--glass-border);
            transition: var(--transition-normal);
            backdrop-filter: var(--glass-backdrop);
            position: relative;
            overflow: hidden;
        }
        
        .forecast-card::before {
            content: '';
            position: absolute;
            top: -100%;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(180deg, var(--primary)20, transparent);
            transition: var(--transition-slow);
        }
        
        .forecast-card:hover {
            transform: translateY(-8px);
            box-shadow: var(--shadow-xl), 0 0 30px rgba(0, 212, 255, 0.2);
            border-color: var(--primary);
        }
        
        .forecast-card:hover::before {
            top: 0;
        }
        
        .forecast-day {
            font-size: 1.125rem;
            font-weight: 600;
            color: white;
            margin-bottom: var(--space-md);
            position: relative;
            z-index: 1;
        }
        
        .forecast-icon img {
            width: 64px;
            height: 64px;
            margin: var(--space-sm) 0;
            filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.2));
            transition: var(--transition-normal);
            position: relative;
            z-index: 1;
        }
        
        .forecast-card:hover .forecast-icon img {
            transform: scale(1.1);
            filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.4));
        }
        
        .forecast-temps {
            margin: var(--space-md) 0;
            position: relative;
            z-index: 1;
        }
        
        .temp-high {
            font-size: 1.375rem;
            font-weight: 700;
            color: var(--warm);
            margin-right: var(--space-sm);
        }
        
        .temp-low {
            font-size: 1.125rem;
            font-weight: 500;
            color: var(--cold);
        }
        
        .forecast-desc {
            font-size: 0.875rem;
            color: rgba(255, 255, 255, 0.7);
            margin: var(--space-sm) 0;
            text-transform: capitalize;
            position: relative;
            z-index: 1;
        }
        
        .forecast-details {
            font-size: 0.75rem;
            color: rgba(255, 255, 255, 0.6);
            font-family: 'JetBrains Mono', monospace;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
            z-index: 1;
        }
        
        /* Premium Chart Section */
        .premium-chart {
            margin: var(--space-3xl) 0;
            background: var(--glass-bg);
            border-radius: var(--radius-xl);
            padding: var(--space-xl);
            border: 1px solid var(--glass-border);
            backdrop-filter: var(--glass-backdrop);
        }
        
        /* Premium Air Quality Section */
        .premium-air-quality {
            margin: var(--space-3xl) 0;
            background: var(--glass-bg);
            border-radius: var(--radius-xl);
            padding: var(--space-xl);
            border: 1px solid var(--glass-border);
            backdrop-filter: var(--glass-backdrop);
            position: relative;
            overflow: hidden;
        }
        
        .aqi-indicator {
            border-radius: var(--radius-lg);
            padding: var(--space-xl);
            text-align: center;
            color: white;
            font-weight: bold;
            position: relative;
            overflow: hidden;
        }
        
        .aqi-indicator::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            animation: shimmer 2s infinite;
        }
        
        .aqi-value {
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: var(--space-sm);
            position: relative;
            z-index: 1;
        }
        
        .aqi-level {
            font-size: 1.25rem;
            font-weight: 500;
            position: relative;
            z-index: 1;
        }
        
        .aqi-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: var(--space-md);
            align-items: center;
            margin-top: var(--space-lg);
        }
        
        .aqi-component {
            background: rgba(255, 255, 255, 0.05);
            border-radius: var(--radius-md);
            padding: var(--space-md);
            text-align: center;
            color: white;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.875rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: var(--transition-normal);
        }
        
        .aqi-component:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: var(--primary);
            transform: translateY(-2px);
        }
        
        /* Premium Footer */
        .premium-footer {
            text-align: center;
            margin: var(--space-3xl) 0 var(--space-xl) 0;
            padding: var(--space-xl);
            background: var(--glass-bg);
            border-radius: var(--radius-xl);
            border: 1px solid var(--glass-border);
            backdrop-filter: var(--glass-backdrop);
            color: rgba(255, 255, 255, 0.7);
        }
        
        .premium-footer p {
            margin: var(--space-sm) 0;
            font-size: 0.875rem;
        }
        
        /* Loading States */
        .skeleton {
            background: linear-gradient(90deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%);
            background-size: 200% 100%;
            animation: skeleton-loading 1.5s infinite;
            border-radius: var(--radius-md);
        }
        
        @keyframes skeleton-loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        /* Enhanced Selectbox */
        .stSelectbox > div > div > select {
            background: var(--glass-bg) !important;
            border: 2px solid var(--glass-border) !important;
            border-radius: var(--radius-md) !important;
            color: white !important;
            font-family: 'Inter', sans-serif !important;
            padding: var(--space-md) !important;
            transition: var(--transition-normal) !important;
        }
        
        .stSelectbox > div > div > select:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1) !important;
        }
        
        /* Enhanced Expander */
        .streamlit-expanderHeader {
            background: var(--glass-bg) !important;
            border-radius: var(--radius-md) !important;
            border: 1px solid var(--glass-border) !important;
            color: white !important;
            transition: var(--transition-normal) !important;
        }
        
        .streamlit-expanderHeader:hover {
            border-color: var(--primary) !important;
            background: rgba(255, 255, 255, 0.08) !important;
        }
        
        .streamlit-expanderContent {
            background: var(--glass-bg) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
        }
        
        /* Alert Messages */
        .stSuccess {
            background: rgba(16, 185, 129, 0.1) !important;
            border: 1px solid rgba(16, 185, 129, 0.3) !important;
            border-radius: var(--radius-md) !important;
            color: var(--success) !important;
        }
        
        .stError {
            background: rgba(239, 68, 68, 0.1) !important;
            border: 1px solid rgba(239, 68, 68, 0.3) !important;
            border-radius: var(--radius-md) !important;
            color: var(--error) !important;
        }
        
        .stWarning {
            background: rgba(245, 158, 11, 0.1) !important;
            border: 1px solid rgba(245, 158, 11, 0.3) !important;
            border-radius: var(--radius-md) !important;
            color: var(--warning) !important;
        }
        
        .stInfo {
            background: rgba(59, 130, 246, 0.1) !important;
            border: 1px solid rgba(59, 130, 246, 0.3) !important;
            border-radius: var(--radius-md) !important;
            color: var(--info) !important;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .premium-header h1 {
                font-size: 2.5rem;
            }
            
            .temp-main {
                font-size: 3.5rem;
            }
            
            .premium-details-grid {
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: var(--space-md);
            }
            
            .forecast-grid {
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: var(--space-md);
            }
            
            .premium-header,
            .premium-search,
            .premium-weather-card,
            .premium-chart,
            .premium-air-quality {
                padding: var(--space-lg);
                margin: var(--space-lg) 0;
            }
        }
        
        /* Utility Classes */
        .glass-card {
            background: var(--glass-bg);
            border-radius: var(--radius-lg);
            border: 1px solid var(--glass-border);
            backdrop-filter: var(--glass-backdrop);
            box-shadow: var(--glass-shadow);
        }
        
        .gradient-text {
            background: linear-gradient(135deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 600;
        }
        
        .hover-lift {
            transition: var(--transition-normal);
        }
        
        .hover-lift:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-xl);
        }
        
        /* Weather Condition Animations */
        .weather-sunny {
            animation: sunny-glow 3s ease-in-out infinite;
        }
        
        @keyframes sunny-glow {
            0%, 100% { filter: drop-shadow(0 0 20px rgba(255, 193, 7, 0.3)); }
            50% { filter: drop-shadow(0 0 30px rgba(255, 193, 7, 0.5)); }
        }
        
        .weather-rainy {
            animation: rainy-drip 2s ease-in-out infinite;
        }
        
        @keyframes rainy-drip {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(3px); }
        }
        
        .weather-cloudy {
            animation: cloudy-drift 4s ease-in-out infinite;
        }
        
        @keyframes cloudy-drift {
            0%, 100% { transform: translateX(0px); }
            50% { transform: translateX(5px); }
        }
        
        .weather-snowy {
            animation: snowy-fall 3s ease-in-out infinite;
        }
        
        @keyframes snowy-fall {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(5px) rotate(5deg); }
        }
        </style>
        """, unsafe_allow_html=True)
    
    def create_premium_header(self, title: str = "Climatrack", subtitle: str = "Real-time Weather Intelligence"):
        """Create premium animated header"""
        return f"""
        <div class="premium-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
            <div class="weather-status">
                <div class="status-indicator"></div>
                <span>Live Weather Data</span>
            </div>
        </div>
        """
    
    def create_weather_icon_enhanced(self, icon_code: str, condition: str = "clear", size: str = "120px") -> str:
        """Create enhanced weather icon with animations"""
        condition_class = f"weather-{condition.lower()}"
        return f"""
        <div class="weather-icon-container">
            <img src="http://openweathermap.org/img/wn/{icon_code}@4x.png" 
                 class="{condition_class}"
                 style="width: {size}; height: {size};" 
                 alt="{condition}" />
        </div>
        """
    
    def create_metric_card_premium(self, icon: str, label: str, value: str, unit: str = "", 
                                 color: str = "var(--primary)", description: str = "") -> str:
        """Create premium metric card with enhanced styling"""
        return f"""
        <div class="detail-card hover-lift">
            <div class="detail-icon">{icon}</div>
            <div class="detail-label">{label}</div>
            <div class="detail-value">{value}<small style="font-size: 0.8em; opacity: 0.8;">{unit}</small></div>
            {f'<div style="font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); margin-top: 0.5rem;">{description}</div>' if description else ''}
        </div>
        """
    
    def create_loading_skeleton(self, height: str = "100px", width: str = "100%") -> str:
        """Create loading skeleton animation"""
        return f"""
        <div class="skeleton" style="height: {height}; width: {width};"></div>
        """
    
    def create_gradient_text(self, text: str, gradient: str = "linear-gradient(135deg, var(--primary), var(--accent))") -> str:
        """Create gradient text"""
        return f"""
        <span class="gradient-text" style="background: {gradient}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{text}</span>
        """
    
    def create_glass_card(self, content: str, padding: str = "var(--space-lg)", 
                         border_radius: str = "var(--radius-lg)") -> str:
        """Create glassmorphism card"""
        return f"""
        <div class="glass-card" style="padding: {padding}; border-radius: {border_radius};">
            {content}
        </div>
        """
    
    def create_notification_toast(self, message: str, type: str = "info", duration: int = 5000) -> str:
        """Create notification toast"""
        icons = {
            "success": "✅",
            "error": "❌", 
            "warning": "⚠️",
            "info": "ℹ️"
        }
        
        return f"""
        <div class="toast toast-{type}" style="
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-md);
            padding: var(--space-md) var(--space-lg);
            backdrop-filter: var(--glass-backdrop);
            color: white;
            z-index: 1000;
            animation: slideIn 0.3s ease-out;
        ">
            <div style="display: flex; align-items: center; gap: var(--space-sm);">
                <span>{icons.get(type, "ℹ️")}</span>
                <span>{message}</span>
            </div>
        </div>
        
        <style>
        @keyframes slideIn {{
            from {{ transform: translateX(100%); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        </style>
        
        <script>
        setTimeout(() => {{
            const toast = document.querySelector('.toast');
            if (toast) {{
                toast.style.animation = 'slideIn 0.3s ease-out reverse';
                setTimeout(() => toast.remove(), 300);
            }}
        }}, {duration});
        </script>
        """
        
    def create_weather_comparison_card(self, locations: List[Dict]) -> str:
        """Create weather comparison card for multiple locations"""
        cards_html = ""
        for location in locations:
            cards_html += f"""
            <div class="comparison-item">
                <h4>{location['city']}</h4>
                <div class="temp">{location['temp']}°</div>
                <div class="condition">{location['condition']}</div>
            </div>
            """
        
        return f"""
        <div class="weather-comparison glass-card">
            <h3>Weather Comparison</h3>
            <div class="comparison-grid">
                {cards_html}
            </div>
        </div>
        
        <style>
        .weather-comparison {{
            padding: var(--space-xl);
            margin: var(--space-lg) 0;
        }}
        
        .comparison-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: var(--space-md);
            margin-top: var(--space-lg);
        }}
        
        .comparison-item {{
            text-align: center;
            padding: var(--space-md);
            background: rgba(255, 255, 255, 0.05);
            border-radius: var(--radius-md);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: var(--transition-normal);
        }}
        
        .comparison-item:hover {{
            background: rgba(255, 255, 255, 0.08);
            border-color: var(--primary);
            transform: translateY(-2px);
        }}
        
        .comparison-item h4 {{
            color: white;
            margin-bottom: var(--space-sm);
            font-size: 0.9rem;
        }}
        
        .comparison-item .temp {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: var(--space-xs);
        }}
        
        .comparison-item .condition {{
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.7);
        }}
        </style>
        """
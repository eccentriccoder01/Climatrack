import streamlit as st
from typing import Dict, Any, List, Optional
import json
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

class UIComponents:
    """World-class UI component library with premium animations and interactions"""
    
    def __init__(self):
        self.themes = {
            "premium_dark": {
                "name": "Premium Dark",
                "primary": "#00d4ff",
                "secondary": "#7c3aed",
                "accent": "#06ffa5",
                "warm": "#ff6b35",
                "cold": "#4facfe",
                "background": "#0a0a0f",
                "surface": "rgba(255, 255, 255, 0.05)",
                "text_primary": "#ffffff",
                "text_secondary": "rgba(255, 255, 255, 0.7)"
            },
            "premium_light": {
                "name": "Premium Light",
                "primary": "#0284c7",
                "secondary": "#7c3aed",
                "accent": "#059669",
                "warm": "#dc2626",
                "cold": "#2563eb",
                "background": "#ffffff",
                "surface": "rgba(0, 0, 0, 0.05)",
                "text_primary": "#1f2937",
                "text_secondary": "rgba(31, 41, 55, 0.7)"
            },
            "aurora": {
                "name": "Aurora Borealis",
                "primary": "#00d4ff",
                "secondary": "#7c3aed",
                "accent": "#06ffa5",
                "warm": "#ff6b35",
                "cold": "#4facfe",
                "background": "#0a0a0f",
                "surface": "rgba(255, 255, 255, 0.05)",
                "text_primary": "#ffffff",
                "text_secondary": "rgba(255, 255, 255, 0.7)"
            }
        }
        
        self.animation_presets = {
            "fade_in": "fadeIn 0.5s ease-out",
            "slide_up": "slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
            "scale_in": "scaleIn 0.2s cubic-bezier(0.34, 1.56, 0.64, 1)",
            "bounce": "bounce 2s infinite",
            "pulse": "pulse 2s infinite",
            "float": "float 6s ease-in-out infinite",
            "glow": "glow 3s ease-in-out infinite",
            "shimmer": "shimmer 2s linear infinite"
        }
        
    def load_premium_css(self):
        """Load world-class premium CSS with advanced features"""
        st.markdown("""
        <style>
        /* Import Premium Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=JetBrains+Mono:wght@100;200;300;400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
        
        /* Advanced CSS Custom Properties */
        :root {
            /* Color System */
            --primary: #00d4ff;
            --primary-rgb: 0, 212, 255;
            --secondary: #7c3aed;
            --secondary-rgb: 124, 58, 237;
            --accent: #06ffa5;
            --accent-rgb: 6, 255, 165;
            --warm: #ff6b35;
            --warm-rgb: 255, 107, 53;
            --cold: #4facfe;
            --cold-rgb: 79, 172, 254;
            
            /* Status Colors */
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --info: #3b82f6;
            
            /* Glass Morphism Advanced */
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-bg-hover: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.08);
            --glass-border-hover: rgba(255, 255, 255, 0.15);
            --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            --glass-shadow-hover: 0 16px 48px rgba(0, 0, 0, 0.4);
            --glass-backdrop: blur(20px);
            --glass-backdrop-strong: blur(40px);
            
            /* Spacing System (8px base) */
            --space-xs: 0.25rem;
            --space-sm: 0.5rem;
            --space-md: 1rem;
            --space-lg: 1.5rem;
            --space-xl: 2rem;
            --space-2xl: 3rem;
            --space-3xl: 4rem;
            --space-4xl: 6rem;
            --space-5xl: 8rem;
            
            /* Border Radius System */
            --radius-xs: 4px;
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 20px;
            --radius-2xl: 24px;
            --radius-3xl: 32px;
            --radius-full: 9999px;
            
            /* Shadow System */
            --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            --shadow-inner: inset 0 2px 4px rgba(0, 0, 0, 0.06);
            --shadow-glow: 0 0 20px rgba(var(--primary-rgb), 0.3);
            --shadow-glow-strong: 0 0 40px rgba(var(--primary-rgb), 0.5);
            
            /* Animation Timing */
            --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-normal: 300ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-slow: 500ms cubic-bezier(0.4, 0, 0.2, 1);
            --transition-bounce: 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
            
            /* Typography Scale */
            --text-xs: 0.75rem;
            --text-sm: 0.875rem;
            --text-base: 1rem;
            --text-lg: 1.125rem;
            --text-xl: 1.25rem;
            --text-2xl: 1.5rem;
            --text-3xl: 1.875rem;
            --text-4xl: 2.25rem;
            --text-5xl: 3rem;
            --text-6xl: 3.75rem;
            --text-7xl: 4.5rem;
            --text-8xl: 6rem;
            --text-9xl: 8rem;
            
            /* Z-Index Scale */
            --z-dropdown: 1000;
            --z-sticky: 1020;
            --z-fixed: 1030;
            --z-modal-backdrop: 1040;
            --z-modal: 1050;
            --z-popover: 1060;
            --z-tooltip: 1070;
            --z-toast: 1080;
        }
        
        /* Advanced Global Styles */
        .main {
            /* CORRECTED: The conflicting background property has been removed. */
            /* The background image from main.py will now be visible. */
            min-height: 100vh;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            position: relative;
            overflow-x: hidden;
        }
        
        /* Hide Streamlit Elements */
        .stDeployButton, #MainMenu, footer, header, .stDecoration {
            display: none !important;
        }
        
        .stAppViewBlockContainer {
            padding-top: var(--space-lg);
            max-width: none !important;
        }
        
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
            box-shadow: var(--shadow-glow);
        }
        
        /* Advanced Animations */
        @keyframes sparkle {
            0% { transform: translateY(0px); }
            100% { transform: translateY(-100px); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes scaleIn {
            from { opacity: 0; transform: scale(0.8); }
            to { opacity: 1; transform: scale(1); }
        }
        
        @keyframes bounce {
            0%, 20%, 53%, 80%, 100% { transform: translate3d(0,0,0); }
            40%, 43% { transform: translate3d(0, -30px, 0); }
            70% { transform: translate3d(0, -15px, 0); }
            90% { transform: translate3d(0, -4px, 0); }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.05); }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes glow {
            0%, 100% { 
                box-shadow: 0 0 20px rgba(var(--primary-rgb), 0.3);
                filter: brightness(1);
            }
            50% { 
                box-shadow: 0 0 40px rgba(var(--primary-rgb), 0.6);
                filter: brightness(1.1);
            }
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        @keyframes morphBackground {
            0%, 100% { border-radius: var(--radius-xl); }
            50% { border-radius: var(--radius-3xl); }
        }
        
        /* Premium Glass Cards */
        .glass-card {
            background: var(--glass-bg);
            backdrop-filter: var(--glass-backdrop);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-xl);
            box-shadow: var(--glass-shadow);
            transition: var(--transition-normal);
            position: relative;
            overflow: hidden;
        }
        
        .glass-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: var(--transition-slow);
        }
        
        .glass-card:hover {
            background: var(--glass-bg-hover);
            border-color: var(--glass-border-hover);
            box-shadow: var(--glass-shadow-hover);
            transform: translateY(-4px);
        }
        
        .glass-card:hover::before {
            left: 100%;
        }
        
        /* Interactive Elements */
        .interactive-card {
            transition: var(--transition-normal);
            cursor: pointer;
            position: relative;
            transform-style: preserve-3d;
        }
        
        .interactive-card:hover {
            transform: perspective(1000px) rotateX(2deg) translateY(-8px);
        }
        
        .interactive-card:active {
            transform: perspective(1000px) rotateX(0deg) translateY(-2px);
        }
        
        /* Premium Buttons */
        .premium-button {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none;
            border-radius: var(--radius-lg);
            color: white;
            font-weight: 600;
            padding: var(--space-md) var(--space-xl);
            font-size: var(--text-base);
            cursor: pointer;
            transition: var(--transition-normal);
            position: relative;
            overflow: hidden;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: var(--space-sm);
            box-shadow: var(--shadow-lg);
        }
        
        .premium-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: var(--transition-normal);
        }
        
        .premium-button:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-xl), var(--shadow-glow);
            background: linear-gradient(135deg, var(--accent), var(--primary));
        }
        
        .premium-button:hover::before {
            left: 100%;
        }
        
        .premium-button:active {
            transform: translateY(0px);
        }
        
        /* Premium Input Fields */
        .premium-input {
            width: 100%;
            padding: var(--space-md) var(--space-lg);
            background: var(--glass-bg);
            border: 2px solid var(--glass-border);
            border-radius: var(--radius-lg);
            color: white;
            font-size: var(--text-base);
            font-family: 'Inter', sans-serif;
            transition: var(--transition-normal);
            backdrop-filter: var(--glass-backdrop);
        }
        
        .premium-input:focus {
            background: var(--glass-bg-hover);
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(var(--primary-rgb), 0.1);
            outline: none;
            transform: translateY(-1px);
        }
        
        .premium-input::placeholder {
            color: rgba(255, 255, 255, 0.5);
            font-weight: 300;
        }
        
        /* Weather Display Components */
        .weather-hero {
            background: linear-gradient(135deg, 
                rgba(var(--primary-rgb), 0.1), 
                rgba(var(--secondary-rgb), 0.1)
            );
            border-radius: var(--radius-2xl);
            padding: var(--space-3xl);
            border: 1px solid var(--glass-border);
            backdrop-filter: var(--glass-backdrop);
            position: relative;
            overflow: hidden;
            animation: fadeIn 0.8s ease-out;
        }
        
        .weather-hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--accent), var(--secondary));
            background-size: 200% 100%;
            animation: gradientShift 4s ease-in-out infinite;
        }
        
        .weather-icon-animated {
            position: relative;
            display: inline-block;
            animation: float 6s ease-in-out infinite;
        }
        
        .weather-icon-animated img {
            width: 120px;
            height: 120px;
            filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.3));
            transition: var(--transition-normal);
        }
        
        .weather-icon-animated:hover img {
            transform: scale(1.1);
            filter: drop-shadow(0 0 30px rgba(255, 255, 255, 0.5));
        }
        
        /* Temperature Display */
        .temperature-display {
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(3rem, 8vw, 6rem);
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff, #e2e8f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            line-height: 0.9;
            margin: var(--space-md) 0;
            position: relative;
        }
        
        .temperature-display::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            border-radius: var(--radius-full);
            animation: shimmer 2s linear infinite;
        }
        
        /* Metric Cards */
        .metric-card-premium {
            background: var(--glass-bg);
            backdrop-filter: var(--glass-backdrop);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            text-align: center;
            position: relative;
            overflow: hidden;
            transition: var(--transition-normal);
            animation: slideUp 0.5s ease-out;
        }
        
        .metric-card-premium::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            transform: scaleX(0);
            transform-origin: left;
            transition: var(--transition-normal);
        }
        
        .metric-card-premium:hover::before {
            transform: scaleX(1);
        }
        
        .metric-card-premium:hover {
            background: var(--glass-bg-hover);
            border-color: var(--glass-border-hover);
            transform: translateY(-4px);
            box-shadow: var(--shadow-xl);
        }
        
        .metric-icon {
            font-size: var(--text-3xl);
            margin-bottom: var(--space-md);
            display: block;
            filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.3));
            animation: pulse 3s infinite;
        }
        
        .metric-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: var(--text-2xl);
            font-weight: 700;
            color: white;
            margin-bottom: var(--space-sm);
            position: relative;
        }
        
        .metric-label {
            font-size: var(--text-sm);
            color: rgba(255, 255, 255, 0.7);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 500;
        }
        
        /* Forecast Cards */
        .forecast-card-premium {
            background: var(--glass-bg);
            backdrop-filter: var(--glass-backdrop);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            text-align: center;
            position: relative;
            overflow: hidden;
            transition: var(--transition-normal);
            cursor: pointer;
        }
        
        .forecast-card-premium::before {
            content: '';
            position: absolute;
            top: -100%;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(180deg, 
                rgba(var(--primary-rgb), 0.2), 
                transparent
            );
            transition: var(--transition-slow);
        }
        
        .forecast-card-premium:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: var(--shadow-2xl), var(--shadow-glow);
            border-color: var(--primary);
        }
        
        .forecast-card-premium:hover::before {
            top: 0;
        }
        
        .forecast-day {
            font-size: var(--text-lg);
            font-weight: 600;
            color: white;
            margin-bottom: var(--space-md);
        }
        
        .forecast-icon img {
            width: 64px;
            height: 64px;
            margin: var(--space-sm) 0;
            filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.2));
            transition: var(--transition-normal);
        }
        
        .forecast-card-premium:hover .forecast-icon img {
            transform: scale(1.15) rotate(5deg);
            filter: drop-shadow(0 0 25px rgba(255, 255, 255, 0.4));
        }
        
        .forecast-temps {
            margin: var(--space-md) 0;
            display: flex;
            justify-content: center;
            gap: var(--space-sm);
            align-items: center;
        }
        
        .temp-high {
            font-family: 'JetBrains Mono', monospace;
            font-size: var(--text-xl);
            font-weight: 700;
            color: var(--warm);
        }
        
        .temp-low {
            font-family: 'JetBrains Mono', monospace;
            font-size: var(--text-lg);
            font-weight: 500;
            color: var(--cold);
        }
        
        /* Air Quality Display */
        .aqi-indicator-premium {
            position: relative;
            border-radius: var(--radius-lg);
            padding: var(--space-xl);
            text-align: center;
            color: white;
            font-weight: bold;
            overflow: hidden;
            background: linear-gradient(135deg, 
                rgba(var(--primary-rgb), 0.2), 
                rgba(var(--secondary-rgb), 0.2)
            );
            backdrop-filter: var(--glass-backdrop);
            border: 1px solid var(--glass-border);
        }
        
        .aqi-indicator-premium::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, 
                transparent, 
                rgba(255, 255, 255, 0.1), 
                transparent
            );
            animation: shimmer 3s linear infinite;
        }
        
        .aqi-value {
            font-family: 'Space Grotesk', sans-serif;
            font-size: var(--text-5xl);
            font-weight: 800;
            margin-bottom: var(--space-sm);
            position: relative;
            z-index: 1;
            animation: scaleIn 0.8s ease-out;
        }
        
        .aqi-level {
            font-size: var(--text-xl);
            font-weight: 500;
            position: relative;
            z-index: 1;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        /* Chart Containers */
        .chart-container-premium {
            background: var(--glass-bg);
            backdrop-filter: var(--glass-backdrop);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-xl);
            padding: var(--space-xl);
            margin: var(--space-lg) 0;
            position: relative;
            overflow: hidden;
        }
        
        .chart-container-premium::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--primary), var(--accent), var(--secondary));
            background-size: 200% 100%;
            animation: gradientShift 3s ease-in-out infinite;
        }
        
        /* Loading States */
        .loading-skeleton {
            background: linear-gradient(90deg, 
                rgba(255, 255, 255, 0.1) 0%, 
                rgba(255, 255, 255, 0.2) 50%, 
                rgba(255, 255, 255, 0.1) 100%
            );
            background-size: 200% 100%;
            animation: skeleton-loading 1.5s infinite;
            border-radius: var(--radius-md);
        }
        
        @keyframes skeleton-loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        .loading-spinner {
            width: 40px;
            height: 40px;
            border: 3px solid rgba(255, 255, 255, 0.1);
            border-top-color: var(--primary);
            border-radius: 50%;
            animation: rotate 1s linear infinite;
            margin: var(--space-lg) auto;
        }
        
        /* Status Indicators */
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
            margin-right: var(--space-sm);
        }
        
        .status-online { background: var(--success); animation: pulse 2s infinite; }
        .status-loading { background: var(--warning); animation: pulse 1s infinite; }
        .status-error { background: var(--error); animation: pulse 0.5s infinite; }
        
        /* Notification Toasts */
        .toast-notification {
            position: fixed;
            top: var(--space-lg);
            right: var(--space-lg);
            background: var(--glass-bg);
            backdrop-filter: var(--glass-backdrop-strong);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            color: white;
            z-index: var(--z-toast);
            max-width: 400px;
            box-shadow: var(--shadow-2xl);
            animation: slideUp 0.3s ease-out;
        }
        
        .toast-success { border-left: 4px solid var(--success); }
        .toast-warning { border-left: 4px solid var(--warning); }
        .toast-error { border-left: 4px solid var(--error); }
        .toast-info { border-left: 4px solid var(--info); }
        
        /* Modal Overlays */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(5px);
            z-index: var(--z-modal-backdrop);
            animation: fadeIn 0.3s ease-out;
        }
        
        .modal-content {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: var(--glass-bg);
            backdrop-filter: var(--glass-backdrop-strong);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-xl);
            padding: var(--space-2xl);
            z-index: var(--z-modal);
            max-width: 90vw;
            max-height: 90vh;
            overflow-y: auto;
            animation: scaleIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        
        /* Weather Condition Specific Animations */
        .weather-sunny {
            animation: glow 3s ease-in-out infinite;
            filter: drop-shadow(0 0 20px rgba(255, 193, 7, 0.4));
        }
        
        .weather-rainy {
            animation: float 2s ease-in-out infinite;
            filter: drop-shadow(0 0 15px rgba(59, 130, 246, 0.4));
        }
        
        .weather-snowy {
            animation: float 3s ease-in-out infinite reverse;
            filter: drop-shadow(0 0 20px rgba(229, 231, 235, 0.4));
        }
        
        .weather-cloudy {
            animation: float 4s ease-in-out infinite;
            filter: drop-shadow(0 0 10px rgba(156, 163, 175, 0.4));
        }
        
        .weather-stormy {
            animation: pulse 1s ease-in-out infinite;
            filter: drop-shadow(0 0 25px rgba(239, 68, 68, 0.4));
        }
        
        /* Responsive Design */
        @media (max-width: 1024px) {
            :root {
                --space-xs: 0.2rem;
                --space-sm: 0.4rem;
                --space-md: 0.8rem;
                --space-lg: 1.2rem;
                --space-xl: 1.6rem;
                --space-2xl: 2.4rem;
                --space-3xl: 3.2rem;
            }
            
            .weather-hero {
                padding: var(--space-2xl);
            }
            
            .temperature-display {
                font-size: clamp(2.5rem, 6vw, 4rem);
            }
        }
        
        @media (max-width: 768px) {
            .metric-card-premium {
                padding: var(--space-md);
            }
            
            .forecast-card-premium {
                padding: var(--space-md);
            }
            
            .chart-container-premium {
                padding: var(--space-lg);
            }
            
            .modal-content {
                margin: var(--space-lg);
                padding: var(--space-xl);
            }
            
            .toast-notification {
                top: var(--space-md);
                right: var(--space-md);
                left: var(--space-md);
                max-width: none;
            }
        }
        
        @media (max-width: 480px) {
            .weather-hero {
                padding: var(--space-xl);
            }
            
            .temperature-display {
                font-size: clamp(2rem, 8vw, 3rem);
            }
            
            .metric-icon {
                font-size: var(--text-2xl);
            }
            
            .metric-value {
                font-size: var(--text-xl);
            }
        }
        
        /* Accessibility Enhancements */
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
        
        /* Dark Mode Support */
        @media (prefers-color-scheme: light) {
            :root {
                --glass-bg: rgba(0, 0, 0, 0.03);
                --glass-bg-hover: rgba(0, 0, 0, 0.05);
                --glass-border: rgba(0, 0, 0, 0.08);
                --glass-border-hover: rgba(0, 0, 0, 0.15);
            }
        }
        
        /* High Contrast Mode */
        @media (prefers-contrast: high) {
            :root {
                --glass-border: rgba(255, 255, 255, 0.3);
                --glass-border-hover: rgba(255, 255, 255, 0.5);
            }
        }
        
        /* Print Styles */
        @media print {
            .glass-card, .metric-card-premium, .forecast-card-premium {
                background: white !important;
                color: black !important;
                border: 1px solid #ccc !important;
                box-shadow: none !important;
            }
            
            .temperature-display {
                color: black !important;
                -webkit-text-fill-color: black !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)
    
    def create_animated_weather_icon(self, icon_code: str, condition: str = "clear", size: str = "120px") -> str:
        """Create advanced animated weather icon with condition-specific effects"""
        condition_class = f"weather-{condition.lower()}"
        
        # Advanced icon mapping with special effects
        special_effects = {
            'sunny': 'weather-sunny',
            'clear': 'weather-sunny',
            'rain': 'weather-rainy',
            'drizzle': 'weather-rainy',
            'thunderstorm': 'weather-stormy',
            'snow': 'weather-snowy',
            'clouds': 'weather-cloudy',
            'mist': 'weather-cloudy',
            'fog': 'weather-cloudy'
        }
        
        effect_class = special_effects.get(condition.lower(), 'weather-clear')
        
        return f"""
        <div class="weather-icon-animated {effect_class}">
            <img src="http://openweathermap.org/img/wn/{icon_code}@4x.png" 
                 style="width: {size}; height: {size};" 
                 alt="{condition}" />
        </div>
        """
    
    def create_premium_metric_card(self, icon: str, label: str, value: str, unit: str = "", 
                                 color: str = "var(--primary)", description: str = "", 
                                 trend: str = None) -> str:
        """Create premium metric card with trend indicators and descriptions"""
        
        trend_indicator = ""
        if trend:
            trend_icons = {
                'up': '📈',
                'down': '📉',
                'stable': '➡️'
            }
            trend_colors = {
                'up': 'var(--success)',
                'down': 'var(--error)',
                'stable': 'var(--info)'
            }
            trend_indicator = f"""
                <div style="
                    position: absolute;
                    top: 12px;
                    right: 12px;
                    font-size: 14px;
                    color: {trend_colors.get(trend, 'var(--info)')};
                ">{trend_icons.get(trend, '➡️')}</div>
            """
        
        return f"""
        <div class="metric-card-premium interactive-card">
            {trend_indicator}
            <div class="metric-icon" style="color: {color};">{icon}</div>
            <div class="metric-value">
                {value}
                <small style="font-size: 0.7em; opacity: 0.8; margin-left: 2px;">{unit}</small>
            </div>
            <div class="metric-label">{label}</div>
            {f'<div style="font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); margin-top: 8px; line-height: 1.3;">{description}</div>' if description else ''}
        </div>
        """
    
    def create_premium_forecast_card(self, day_data: Dict, is_today: bool = False) -> str:
        """Create premium forecast card with enhanced styling and interactions"""
        today_class = "today-highlight" if is_today else ""
        day_label = "Today" if is_today else day_data.get('day', 'Unknown')
        
        temp_unit = "°C"  # Default, should be passed as parameter
        
        # Comfort score color
        comfort_score = day_data.get('comfort_score', 50)
        comfort_color = self._get_comfort_color(comfort_score)
        
        return f"""
        <div class="forecast-card-premium {today_class}">
            <div class="forecast-day">{day_label}</div>
            <div style="font-size: 0.75rem; color: rgba(255, 255, 255, 0.6); margin-bottom: 1rem;">
                {day_data.get('date', datetime.now()).strftime('%m/%d')}
            </div>
            
            <div class="forecast-icon">
                <img src="http://openweathermap.org/img/wn/{day_data.get('icon', '01d')}@2x.png" />
            </div>
            
            <div class="forecast-temps">
                <span class="temp-high">{day_data.get('temp_max', 0):.0f}{temp_unit}</span>
                <span style="color: rgba(255, 255, 255, 0.5); margin: 0 4px;">/</span>
                <span class="temp-low">{day_data.get('temp_min', 0):.0f}{temp_unit}</span>
            </div>
            
            <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.8); margin: 0.5rem 0; text-transform: capitalize;">
                {day_data.get('description', 'No description')}
            </div>
            
            <div style="display: flex; justify-content: space-between; margin-top: 1rem; font-size: 0.75rem;">
                <span style="color: rgba(255, 255, 255, 0.6);">💧 {day_data.get('humidity', 0):.0f}%</span>
                <span style="color: rgba(255, 255, 255, 0.6);">🌬️ {day_data.get('wind_speed', 0):.0f}</span>
            </div>
            
            <div style="
                margin-top: 0.75rem;
                padding: 4px 8px;
                background: rgba({comfort_color}, 0.2);
                border-radius: 12px;
                font-size: 0.7rem;
                text-align: center;
                color: rgb({comfort_color});
                border: 1px solid rgba({comfort_color}, 0.3);
            ">
                Comfort: {comfort_score:.0f}%
            </div>
        </div>
        """
    
    def _get_comfort_color(self, score: float) -> str:
        """Get RGB color based on comfort score"""
        if score >= 80:
            return "16, 185, 129"  # Green
        elif score >= 60:
            return "245, 158, 11"  # Yellow
        elif score >= 40:
            return "249, 115, 22"  # Orange
        else:
            return "239, 68, 68"   # Red
    
    def create_aqi_indicator(self, aqi: int, level: str, color: str) -> str:
        """Create premium AQI indicator with enhanced visuals"""
        return f"""
        <div class="aqi-indicator-premium" style="
            background: linear-gradient(135deg, 
                rgba({self._hex_to_rgb(color)}, 0.2), 
                rgba({self._hex_to_rgb(color)}, 0.1)
            );
            border: 2px solid rgba({self._hex_to_rgb(color)}, 0.3);
        ">
            <div class="aqi-value" style="color: {color};">{aqi}</div>
            <div class="aqi-level" style="color: {color};">{level}</div>
            <div style="
                font-size: 0.9rem;
                margin-top: 0.5rem;
                opacity: 0.9;
                color: rgba(255, 255, 255, 0.8);
            ">Air Quality Index</div>
        </div>
        """
    
    def _hex_to_rgb(self, hex_color: str) -> str:
        """Convert hex color to RGB values"""
        hex_color = hex_color.lstrip('#')
        return f"{int(hex_color[0:2], 16)}, {int(hex_color[2:4], 16)}, {int(hex_color[4:6], 16)}"
    
    def create_loading_skeleton(self, height: str = "100px", width: str = "100%") -> str:
        """Create advanced loading skeleton with shimmer effect"""
        return f"""
        <div class="loading-skeleton" style="height: {height}; width: {width};">
            <div style="height: 100%; width: 100%; border-radius: var(--radius-md);"></div>
        </div>
        """
    
    def create_loading_spinner(self, size: str = "40px", color: str = "var(--primary)") -> str:
        """Create premium loading spinner"""
        return f"""
        <div style="display: flex; justify-content: center; align-items: center; padding: var(--space-xl);">
            <div style="
                width: {size};
                height: {size};
                border: 3px solid rgba(255, 255, 255, 0.1);
                border-top-color: {color};
                border-radius: 50%;
                animation: rotate 1s linear infinite;
            "></div>
        </div>
        """
    
    def create_gradient_text(self, text: str, gradient: str = "linear-gradient(135deg, var(--primary), var(--accent))") -> str:
        """Create gradient text with premium styling"""
        return f"""
        <span style="
            background: {gradient};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 600;
        ">{text}</span>
        """
    
    def create_notification_toast(self, message: str, type: str = "info", duration: int = 5000) -> str:
        """Create premium notification toast"""
        icons = {
            "success": "✅",
            "error": "❌", 
            "warning": "⚠️",
            "info": "ℹ️"
        }
        
        return f"""
        <div class="toast-notification toast-{type}" id="toast-{int(datetime.now().timestamp())}">
            <div style="display: flex; align-items: center; gap: var(--space-sm);">
                <span style="font-size: 1.2rem;">{icons.get(type, "ℹ️")}</span>
                <div>
                    <div style="font-weight: 600; margin-bottom: 2px;">{type.title()}</div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">{message}</div>
                </div>
            </div>
        </div>
        
        <script>
        setTimeout(() => {{
            const toast = document.getElementById('toast-{int(datetime.now().timestamp())}');
            if (toast) {{
                toast.style.animation = 'slideUp 0.3s ease-out reverse';
                setTimeout(() => toast.remove(), 300);
            }}
        }}, {duration});
        </script>
        """
    
    def create_chart_container(self, title: str, content: str) -> str:
        """Create premium chart container with title and styling"""
        return f"""
        <div class="chart-container-premium">
            <h3 style="
                color: white;
                margin-bottom: var(--space-lg);
                font-size: var(--text-xl);
                font-weight: 600;
                text-align: center;
            ">{title}</h3>
            {content}
        </div>
        """
    
    def create_status_indicator(self, status: str, label: str) -> str:
        """Create premium status indicator"""
        return f"""
        <div style="display: inline-flex; align-items: center; gap: var(--space-sm);">
            <div class="status-dot status-{status}"></div>
            <span style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem;">{label}</span>
        </div>
        """
    
    def create_interactive_button(self, text: str, icon: str = "", onclick: str = "", 
                                variant: str = "primary") -> str:
        """Create premium interactive button"""
        return f"""
        <button class="premium-button" onclick="{onclick}" style="
            background: linear-gradient(135deg, var(--{variant}), var(--secondary));
        ">
            {f'<span style="margin-right: 8px;">{icon}</span>' if icon else ''}
            {text}
        </button>
        """
    
    def create_weather_comparison_grid(self, locations: List[Dict]) -> str:
        """Create premium weather comparison grid"""
        cards_html = ""
        for location in locations:
            cards_html += f"""
            <div class="glass-card interactive-card" style="padding: var(--space-lg); text-align: center;">
                <h4 style="color: white; margin-bottom: var(--space-md);">{location.get('city', 'Unknown')}</h4>
                <div style="
                    font-size: var(--text-3xl);
                    font-weight: 700;
                    color: var(--primary);
                    margin-bottom: var(--space-sm);
                ">{location.get('temp', 0):.0f}°</div>
                <div style="
                    font-size: var(--text-sm);
                    color: rgba(255, 255, 255, 0.7);
                    text-transform: capitalize;
                ">{location.get('condition', 'Unknown')}</div>
                <div style="
                    margin-top: var(--space-md);
                    padding-top: var(--space-md);
                    border-top: 1px solid rgba(255, 255, 255, 0.1);
                    display: flex;
                    justify-content: space-between;
                    font-size: var(--text-xs);
                    color: rgba(255, 255, 255, 0.6);
                ">
                    <span>💧 {location.get('humidity', 0)}%</span>
                    <span>🌬️ {location.get('wind', 0)} m/s</span>
                </div>
            </div>
            """
        
        return f"""
        <div style="
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: var(--space-lg);
            margin: var(--space-lg) 0;
        ">
            {cards_html}
        </div>
        """
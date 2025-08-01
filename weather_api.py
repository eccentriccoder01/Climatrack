import requests
import streamlit as st
from typing import Dict, Optional, List
import json

class WeatherAPI:
    """Handles all weather API interactions using OpenWeatherMap"""
    
    def __init__(self):
        # Using OpenWeatherMap free tier
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.air_quality_url = "http://api.openweathermap.org/data/2.5/air_pollution"
        # You'll need to get a free API key from https://openweathermap.org/api
        self.api_key = self._get_api_key()
        
    def _get_api_key(self) -> str:
        """Get API key from Streamlit secrets or environment"""
        try:
            # First try Streamlit secrets
            return st.secrets["OPENWEATHER_API_KEY"]
        except:
            # For demo purposes, using a placeholder
            # Users should replace this with their actual API key
            st.warning("⚠️ Please add your OpenWeatherMap API key to .streamlit/secrets.toml")
            st.info("Get your free API key at: https://openweathermap.org/api")
            # Demo key (won't work, user needs to replace)
            return "YOUR_API_KEY_HERE"
    
    def _make_request(self, url: str, params: Dict) -> Optional[Dict]:
        """Make HTTP request to API with error handling"""
        try:
            params['appid'] = self.api_key
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 401:
                st.error("❌ Invalid API key. Please check your OpenWeatherMap API key.")
                return None
            elif response.status_code == 404:
                st.error("❌ Location not found.")
                return None
            elif response.status_code != 200:
                st.error(f"❌ API Error: {response.status_code}")
                return None
                
            return response.json()
            
        except requests.exceptions.Timeout:
            st.error("❌ Request timeout. Please try again.")
            return None
        except requests.exceptions.ConnectionError:
            st.error("❌ Connection error. Please check your internet connection.")
            return None
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            return None
    
    def get_current_weather(self, lat: float, lon: float, units: str = "metric") -> Optional[Dict]:
        """Get current weather data for given coordinates"""
        url = f"{self.base_url}/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "units": units
        }
        
        return self._make_request(url, params)
    
    def get_forecast(self, lat: float, lon: float, units: str = "metric") -> Optional[Dict]:
        """Get 5-day weather forecast for given coordinates"""
        url = f"{self.base_url}/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "units": units
        }
        
        return self._make_request(url, params)
    
    def get_air_quality(self, lat: float, lon: float) -> Optional[Dict]:
        """Get air quality data for given coordinates"""
        params = {
            "lat": lat,
            "lon": lon
        }
        
        return self._make_request(self.air_quality_url, params)
    
    def get_weather_by_city(self, city_name: str, units: str = "metric") -> Optional[Dict]:
        """Get current weather by city name"""
        url = f"{self.base_url}/weather"
        params = {
            "q": city_name,
            "units": units
        }
        
        return self._make_request(url, params)
    
    def search_cities(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for cities using geocoding API"""
        url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {
            "q": query,
            "limit": limit,
            "appid": self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []
    
    def get_weather_alerts(self, lat: float, lon: float) -> Optional[Dict]:
        """Get weather alerts for given coordinates (if available)"""
        url = f"{self.base_url}/onecall"
        params = {
            "lat": lat,
            "lon": lon,
            "exclude": "current,minutely,hourly,daily"
        }
        
        return self._make_request(url, params)
    
    def get_historical_weather(self, lat: float, lon: float, dt: int, units: str = "metric") -> Optional[Dict]:
        """Get historical weather data (requires subscription)"""
        url = f"{self.base_url}/onecall/timemachine"
        params = {
            "lat": lat,
            "lon": lon,
            "dt": dt,
            "units": units
        }
        
        return self._make_request(url, params)
    
    def validate_api_key(self) -> bool:
        """Validate if the API key is working"""
        if self.api_key == "YOUR_API_KEY_HERE":
            return False
            
        url = f"{self.base_url}/weather"
        params = {
            "q": "London",
            "appid": self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            return response.status_code == 200
        except:
            return False
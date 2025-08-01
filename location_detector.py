import requests
import streamlit as st
from typing import Dict, Optional, List
import json

class LocationDetector:
    """Handles location detection and geocoding services"""
    
    def __init__(self):
        self.ip_api_url = "http://ip-api.com/json"
        self.geocoding_url = "http://api.openweathermap.org/geo/1.0"
        
    def get_location_by_ip(self) -> Optional[Dict]:
        """Get location based on IP address using ip-api.com (free service)"""
        try:
            response = requests.get(
                f"{self.ip_api_url}?fields=status,country,countryCode,region,regionName,city,lat,lon,timezone,query",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        'city': data.get('city', 'Unknown'),
                        'region': data.get('regionName', ''),
                        'country': data.get('country', 'Unknown'),
                        'country_code': data.get('countryCode', ''),
                        'lat': data.get('lat', 0),
                        'lon': data.get('lon', 0),
                        'timezone': data.get('timezone', ''),
                        'ip': data.get('query', '')
                    }
            return None
            
        except requests.exceptions.Timeout:
            st.warning("⏱️ Location detection timeout. Please search manually.")
            return None
        except requests.exceptions.ConnectionError:
            st.warning("🌐 Connection error during location detection.")
            return None
        except Exception as e:
            st.warning(f"⚠️ Location detection failed: {str(e)}")
            return None
    
    def get_location(self) -> Optional[Dict]:
        """Primary method to get user location"""
        return self.get_location_by_ip()
    
    def search_location(self, query: str) -> Optional[Dict]:
        """Search for a location by name using OpenWeatherMap geocoding"""
        try:
            # Get API key from weather API instance
            api_key = self._get_api_key()
            if not api_key or api_key == "YOUR_API_KEY_HERE":
                st.error("❌ API key required for location search")
                return None
                
            url = f"{self.geocoding_url}/direct"
            params = {
                "q": query,
                "limit": 1,
                "appid": api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    location = data[0]
                    return {
                        'city': location.get('name', 'Unknown'),
                        'region': location.get('state', ''),
                        'country': location.get('country', 'Unknown'),
                        'country_code': location.get('country', ''),
                        'lat': location.get('lat', 0),
                        'lon': location.get('lon', 0),
                        'timezone': '',
                        'ip': ''
                    }
            return None
            
        except Exception as e:
            st.error(f"❌ Location search failed: {str(e)}")
            return None
    
    def _get_api_key(self) -> str:
        """Get API key for geocoding"""
        try:
            return st.secrets["OPENWEATHER_API_KEY"]
        except:
            return "YOUR_API_KEY_HERE"
    
    def reverse_geocode(self, lat: float, lon: float) -> Optional[Dict]:
        """Convert coordinates to location name"""
        try:
            api_key = self._get_api_key()
            if not api_key or api_key == "YOUR_API_KEY_HERE":
                return None
                
            url = f"{self.geocoding_url}/reverse"
            params = {
                "lat": lat,
                "lon": lon,
                "limit": 1,
                "appid": api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    location = data[0]
                    return {
                        'city': location.get('name', 'Unknown'),
                        'region': location.get('state', ''),
                        'country': location.get('country', 'Unknown'),
                        'country_code': location.get('country', ''),
                        'lat': lat,
                        'lon': lon,
                        'timezone': '',
                        'ip': ''
                    }
            return None
            
        except Exception as e:
            return None
    
    def get_nearby_cities(self, lat: float, lon: float, radius: int = 50) -> List[Dict]:
        """Get nearby cities within specified radius (km)"""
        try:
            # This is a simplified implementation
            # In production, you might want to use a more comprehensive geocoding service
            api_key = self._get_api_key()
            if not api_key or api_key == "YOUR_API_KEY_HERE":
                return []
            
            # For demo, we'll just return some sample nearby locations
            # In production, integrate with a proper geocoding service
            return []
            
        except Exception:
            return []
    
    def validate_coordinates(self, lat: float, lon: float) -> bool:
        """Validate if coordinates are within valid ranges"""
        return -90 <= lat <= 90 and -180 <= lon <= 180
    
    def format_location_display(self, location_data: Dict) -> str:
        """Format location data for display"""
        city = location_data.get('city', 'Unknown')
        region = location_data.get('region', '')
        country = location_data.get('country', 'Unknown')
        
        if region and region != city:
            return f"{city}, {region}, {country}"
        else:
            return f"{city}, {country}"
    
    def get_timezone_info(self, lat: float, lon: float) -> Optional[str]:
        """Get timezone information for coordinates (basic implementation)"""
        # This is a simplified implementation
        # For production, consider using a dedicated timezone API
        try:
            # Using a simple mapping based on longitude
            # This is approximate and not accurate for all locations
            utc_offset = int(lon / 15)
            if utc_offset > 12:
                utc_offset = utc_offset - 24
            elif utc_offset < -12:
                utc_offset = utc_offset + 24
                
            if utc_offset >= 0:
                return f"UTC+{utc_offset}"
            else:
                return f"UTC{utc_offset}"
                
        except:
            return None
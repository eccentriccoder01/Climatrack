import requests
import streamlit as st
from typing import Dict, Optional, List, Tuple, Any
import json
import time
from datetime import datetime, timedelta
import hashlib

class WeatherAPI:
    """Advanced weather API handler with caching and enhanced features"""
    
    def __init__(self):
        # Enhanced API endpoints
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.air_quality_url = "http://api.openweathermap.org/data/2.5/air_pollution"
        self.geocoding_url = "http://api.openweathermap.org/geo/1.0"
        self.onecall_url = "https://api.openweathermap.org/data/3.0/onecall"  # Premium features
        
        # API configuration
        self.api_key = self._get_api_key()
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
        self.rate_limit_delay = 1  # 1 second between requests
        self.last_request_time = 0
        
        # Request tracking
        self.request_count = 0
        self.daily_limit = 1000  # Free tier limit
        
    def _get_api_key(self) -> str:
        """Enhanced API key retrieval with multiple fallbacks"""
        try:
            # Try different secret key formats
            api_key = None
            
            # First try the default format
            if hasattr(st.secrets, "default") and "OPENWEATHER_API_KEY" in st.secrets.default:
                api_key = st.secrets.default["OPENWEATHER_API_KEY"]
            elif "OPENWEATHER_API_KEY" in st.secrets:
                api_key = st.secrets["OPENWEATHER_API_KEY"]
            
            if api_key and api_key != "YOUR_API_KEY_HERE":
                return api_key
            else:
                st.warning("⚠️ Please add your OpenWeatherMap API key to .streamlit/secrets.toml")
                st.info("Get your free API key at: https://openweathermap.org/api")
                return "YOUR_API_KEY_HERE"
                
        except Exception as e:
            st.error(f"❌ Error accessing API key: {str(e)}")
            return "YOUR_API_KEY_HERE"
    
    def _rate_limit(self):
        """Implement rate limiting to respect API limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        self.last_request_time = time.time()
    
    def _get_cache_key(self, url: str, params: Dict) -> str:
        """Generate cache key for request"""
        # Create a unique key based on URL and parameters
        param_str = json.dumps(sorted(params.items()), default=str)
        return hashlib.md5(f"{url}{param_str}".encode()).hexdigest()
    
    def _is_cache_valid(self, cache_entry: Dict) -> bool:
        """Check if cache entry is still valid"""
        return (time.time() - cache_entry['timestamp']) < self.cache_duration
    
    def _make_request(self, url: str, params: Dict, use_cache: bool = True) -> Optional[Dict]:
        """Enhanced HTTP request with caching, rate limiting, and error handling"""
        
        # Check API key validity
        if self.api_key == "YOUR_API_KEY_HERE":
            st.error("❌ Please configure your OpenWeatherMap API key")
            return None
        
        # Check daily rate limit
        if self.request_count >= self.daily_limit:
            st.error("❌ Daily API request limit reached")
            return None
        
        # Add API key to parameters
        params = params.copy()
        params['appid'] = self.api_key
        
        # Check cache first
        cache_key = self._get_cache_key(url, params)
        if use_cache and cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            if self._is_cache_valid(cache_entry):
                return cache_entry['data']
        
        # Rate limiting
        self._rate_limit()
        
        try:
            # Make the request
            response = requests.get(url, params=params, timeout=15)
            self.request_count += 1
            
            # Enhanced error handling
            if response.status_code == 200:
                data = response.json()
                
                # Cache the successful response
                if use_cache:
                    self.cache[cache_key] = {
                        'data': data,
                        'timestamp': time.time()
                    }
                
                return data
                
            elif response.status_code == 401:
                st.error("❌ Invalid API key. Please check your OpenWeatherMap API key.")
                return None
            elif response.status_code == 404:
                st.error("❌ Location not found.")
                return None
            elif response.status_code == 429:
                st.error("❌ API rate limit exceeded. Please try again later.")
                return None
            elif response.status_code == 502:
                st.error("❌ OpenWeatherMap service temporarily unavailable.")
                return None
            else:
                st.error(f"❌ API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            st.error("❌ Request timeout. The weather service is taking too long to respond.")
            return None
        except requests.exceptions.ConnectionError:
            st.error("❌ Connection error. Please check your internet connection.")
            return None
        except requests.exceptions.JSONDecodeError:
            st.error("❌ Invalid response format from weather service.")
            return None
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            return None
    
    def get_current_weather(self, lat: float, lon: float, units: str = "metric") -> Optional[Dict]:
        """Enhanced current weather with additional data points"""
        url = f"{self.base_url}/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "units": units
        }
        
        return self._make_request(url, params)
    
    def get_forecast(self, lat: float, lon: float, units: str = "metric") -> Optional[Dict]:
        """Enhanced 5-day forecast with improved data processing"""
        url = f"{self.base_url}/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "units": units
        }
        
        return self._make_request(url, params)
    
    def get_air_quality(self, lat: float, lon: float) -> Optional[Dict]:
        """Enhanced air quality data with historical context"""
        params = {
            "lat": lat,
            "lon": lon
        }
        
        return self._make_request(self.air_quality_url, params)
    
    def get_air_quality_forecast(self, lat: float, lon: float) -> Optional[Dict]:
        """Get air quality forecast (premium feature)"""
        url = f"{self.air_quality_url}/forecast"
        params = {
            "lat": lat,
            "lon": lon
        }
        
        return self._make_request(url, params)
    
    def get_weather_by_city(self, city_name: str, units: str = "metric") -> Optional[Dict]:
        """Enhanced city-based weather lookup"""
        url = f"{self.base_url}/weather"
        params = {
            "q": city_name,
            "units": units
        }
        
        return self._make_request(url, params)
    
    def search_cities(self, query: str, limit: int = 5) -> List[Dict]:
        """Enhanced city search with improved results"""
        url = f"{self.geocoding_url}/direct"
        params = {
            "q": query,
            "limit": limit
        }
        
        try:
            result = self._make_request(url, params)
            return result if result else []
        except:
            return []
    
    def get_weather_alerts(self, lat: float, lon: float) -> Optional[Dict]:
        """Get official weather alerts (premium feature)"""
        try:
            # This requires OneCall 3.0 API (premium)
            url = f"{self.onecall_url}"
            params = {
                "lat": lat,
                "lon": lon,
                "exclude": "current,minutely,hourly,daily",
                "alerts": "true"
            }
            
            return self._make_request(url, params, use_cache=False)
        except:
            # Fallback to basic weather data
            return None
    
    def get_historical_weather(self, lat: float, lon: float, dt: int, units: str = "metric") -> Optional[Dict]:
        """Get historical weather data (premium feature)"""
        try:
            url = f"{self.onecall_url}/timemachine"
            params = {
                "lat": lat,
                "lon": lon,
                "dt": dt,
                "units": units
            }
            
            return self._make_request(url, params)
        except:
            return None
    
    def get_weather_maps(self, layer: str, lat: float, lon: float, zoom: int = 10) -> Optional[str]:
        """Get weather map tiles URL"""
        # Available layers: temp_new, precipitation_new, pressure_new, wind_new, clouds_new
        map_url = f"http://maps.openweathermap.org/maps/2.0/weather/{layer}/{zoom}/{lat}/{lon}"
        return f"{map_url}?appid={self.api_key}"
    
    def validate_api_key(self) -> Tuple[bool, str]:
        """Enhanced API key validation with detailed feedback"""
        if self.api_key == "YOUR_API_KEY_HERE":
            return False, "API key not configured"
            
        url = f"{self.base_url}/weather"
        params = {
            "q": "London",
            "appid": self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return True, "API key is valid and working"
            elif response.status_code == 401:
                return False, "Invalid API key"
            elif response.status_code == 429:
                return False, "API rate limit exceeded"
            else:
                return False, f"API error: {response.status_code}"
                
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def get_api_usage_stats(self) -> Dict[str, Any]:
        """Get API usage statistics"""
        remaining_requests = max(0, self.daily_limit - self.request_count)
        usage_percentage = (self.request_count / self.daily_limit) * 100
        
        return {
            'requests_made': self.request_count,
            'daily_limit': self.daily_limit,
            'remaining_requests': remaining_requests,
            'usage_percentage': round(usage_percentage, 1),
            'cache_entries': len(self.cache),
            'status': 'good' if usage_percentage < 80 else 'warning' if usage_percentage < 95 else 'critical'
        }
    
    def clear_cache(self):
        """Clear the request cache"""
        self.cache.clear()
        st.success("Cache cleared successfully!")
    
    def get_bulk_weather_data(self, locations: List[Tuple[float, float]], units: str = "metric") -> Dict[str, Dict]:
        """Get weather data for multiple locations efficiently"""
        results = {}
        
        for i, (lat, lon) in enumerate(locations):
            location_key = f"{lat:.4f},{lon:.4f}"
            
            # Add delay to respect rate limits
            if i > 0:
                time.sleep(0.5)
            
            current_weather = self.get_current_weather(lat, lon, units)
            if current_weather:
                results[location_key] = current_weather
            
            # Check if we're approaching rate limits
            if self.request_count >= self.daily_limit * 0.9:
                st.warning("⚠️ Approaching API rate limit. Some requests may be skipped.")
                break
        
        return results
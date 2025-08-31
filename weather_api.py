import requests
import streamlit as st
from typing import Dict, Optional, List, Tuple, Any
import json
import time
from datetime import datetime, timedelta
import hashlib
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import numpy as np

class PremiumWeatherAPI:
    """Premium weather API handler with advanced caching, rate limiting, and enhanced features"""
    
    def __init__(self):
        # Enhanced API endpoints with premium features
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.air_quality_url = "http://api.openweathermap.org/data/2.5/air_pollution"
        self.geocoding_url = "http://api.openweathermap.org/geo/1.0"
        self.onecall_url = "https://api.openweathermap.org/data/3.0/onecall"
        self.maps_url = "http://maps.openweathermap.org/maps/2.0/weather"
        
        # Premium API endpoints (if available)
        self.premium_endpoints = {
            'historical': 'https://api.openweathermap.org/data/2.5/onecall/timemachine',
            'climate': 'https://api.openweathermap.org/data/2.5/climate',
            'statistics': 'https://api.openweathermap.org/data/2.5/statistics'
        }
        
        # Advanced configuration
        self.api_key = self._get_api_key()
        self.cache = {}
        self.cache_duration = {
            'current': 300,    # 5 minutes for current weather
            'forecast': 1800,  # 30 minutes for forecast
            'air_quality': 900, # 15 minutes for air quality
            'geocoding': 86400, # 24 hours for geocoding
            'historical': 86400 # 24 hours for historical data
        }
        
        # Rate limiting and performance
        self.rate_limit_delay = 0.1  # 100ms between requests
        self.last_request_time = 0
        self.request_count = 0
        self.daily_limit = 1000
        self.burst_limit = 60  # requests per minute
        self.burst_window = []
        
        # Request tracking and analytics
        self.request_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'cache_hits': 0,
            'api_errors': {},
            'average_response_time': 0,
            'response_times': []
        }
        
        # Quality metrics
        self.data_quality_thresholds = {
            'temperature_range': (-50, 60),  # Reasonable temperature range
            'humidity_range': (0, 100),
            'pressure_range': (800, 1100),
            'wind_speed_max': 100,
            'visibility_max': 50000
        }
        
    def _get_api_key(self) -> str:
        """Enhanced API key retrieval with multiple fallbacks and validation"""
        try:
            api_key = None
            
            # Try different secret key formats
            if hasattr(st.secrets, "default") and "OPENWEATHER_API_KEY" in st.secrets.default:
                api_key = st.secrets.default["OPENWEATHER_API_KEY"]
            elif "OPENWEATHER_API_KEY" in st.secrets:
                api_key = st.secrets["OPENWEATHER_API_KEY"]
            
            # Validate API key format
            if api_key and len(api_key) == 32 and api_key.isalnum():
                return api_key
            elif api_key and api_key != "YOUR_API_KEY_HERE":
                st.warning("⚠️ API key format appears invalid. Please check your OpenWeatherMap API key.")
                return api_key
            else:
                self._show_api_key_setup_instructions()
                return "YOUR_API_KEY_HERE"
                
        except Exception as e:
            st.error(f"❌ Error accessing API key: {str(e)}")
            return "YOUR_API_KEY_HERE"
    
    def _show_api_key_setup_instructions(self):
        """Show detailed API key setup instructions"""
        st.error("🔑 OpenWeatherMap API Key Required")
        
        with st.expander("📖 How to set up your API key", expanded=True):
            st.markdown("""
            ### Steps to get your free API key:
            
            1. **Sign up** at [OpenWeatherMap](https://openweathermap.org/api)
            2. **Verify** your email address
            3. **Copy** your API key from the dashboard
            4. **Create** a `.streamlit/secrets.toml` file in your project folder
            5. **Add** the following content:
            
            ```toml
            [default]
            OPENWEATHER_API_KEY = "your_32_character_api_key_here"
            ```
            
            ### For Streamlit Cloud deployment:
            1. Go to your app settings
            2. Add the API key in the Secrets section
            3. Use the same format as above
            
            **Note:** It may take up to 2 hours for new API keys to activate.
            """)
    
    def _implement_rate_limiting(self):
        """Advanced rate limiting with burst protection"""
        current_time = time.time()
        
        # Remove old entries from burst window
        self.burst_window = [req_time for req_time in self.burst_window 
                           if current_time - req_time < 60]
        
        # Check burst limit
        if len(self.burst_window) >= self.burst_limit:
            sleep_time = 60 - (current_time - self.burst_window[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        # Check minimum delay between requests
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        # Update tracking
        self.burst_window.append(current_time)
        self.last_request_time = time.time()
    
    def _get_cache_key(self, url: str, params: Dict) -> str:
        """Generate cache key with parameter normalization"""
        # Normalize parameters for consistent caching
        normalized_params = {}
        for key, value in params.items():
            if key == 'appid':
                continue  # Don't include API key in cache key
            normalized_params[key] = str(value).lower() if isinstance(value, str) else value
        
        param_str = json.dumps(sorted(normalized_params.items()), default=str)
        return hashlib.md5(f"{url}{param_str}".encode()).hexdigest()
    
    def _is_cache_valid(self, cache_entry: Dict, cache_type: str = 'current') -> bool:
        """Check if cache entry is valid with different durations per data type"""
        duration = self.cache_duration.get(cache_type, 300)
        return (time.time() - cache_entry['timestamp']) < duration
    
    def _validate_data_quality(self, data: Dict, data_type: str) -> Tuple[bool, List[str]]:
        """Validate data quality and return issues found"""
        issues = []
        
        if data_type == 'current_weather' and 'main' in data:
            main_data = data['main']
            
            # Temperature validation
            temp = main_data.get('temp', 0)
            if not (self.data_quality_thresholds['temperature_range'][0] <= temp <= 
                   self.data_quality_thresholds['temperature_range'][1]):
                issues.append(f"Temperature out of reasonable range: {temp}")
            
            # Humidity validation
            humidity = main_data.get('humidity', 0)
            if not (0 <= humidity <= 100):
                issues.append(f"Humidity out of valid range: {humidity}")
            
            # Pressure validation
            pressure = main_data.get('pressure', 1013)
            if not (self.data_quality_thresholds['pressure_range'][0] <= pressure <= 
                   self.data_quality_thresholds['pressure_range'][1]):
                issues.append(f"Pressure out of reasonable range: {pressure}")
        
        if data_type == 'current_weather' and 'wind' in data:
            wind_speed = data['wind'].get('speed', 0)
            if wind_speed > self.data_quality_thresholds['wind_speed_max']:
                issues.append(f"Wind speed seems unreasonable: {wind_speed}")
        
        return len(issues) == 0, issues
    
    def _make_request_with_analytics(self, url: str, params: Dict, 
                                   cache_type: str = 'current', 
                                   use_cache: bool = True) -> Optional[Dict]:
        """Enhanced HTTP request with comprehensive analytics and error handling"""
        
        # Validate API key
        if self.api_key == "YOUR_API_KEY_HERE":
            st.error("❌ Please configure your OpenWeatherMap API key")
            return None
        
        # Check daily rate limit
        if self.request_count >= self.daily_limit:
            st.error("❌ Daily API request limit reached")
            return None
        
        # Prepare parameters
        params = params.copy()
        params['appid'] = self.api_key
        
        # Check cache first
        cache_key = self._get_cache_key(url, params)
        if use_cache and cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            if self._is_cache_valid(cache_entry, cache_type):
                self.request_stats['cache_hits'] += 1
                return cache_entry['data']
        
        # Implement rate limiting
        self._implement_rate_limiting()
        
        # Track request start time
        start_time = time.time()
        
        try:
            # Make the request
            response = requests.get(url, params=params, timeout=15)
            response_time = time.time() - start_time
            
            # Update analytics
            self.request_count += 1
            self.request_stats['total_requests'] += 1
            self.request_stats['response_times'].append(response_time)
            
            # Calculate average response time
            if len(self.request_stats['response_times']) > 100:
                self.request_stats['response_times'] = self.request_stats['response_times'][-100:]
            self.request_stats['average_response_time'] = np.mean(self.request_stats['response_times'])
            
            # Handle response
            if response.status_code == 200:
                data = response.json()
                
                # Validate data quality
                is_valid, issues = self._validate_data_quality(data, cache_type)
                if not is_valid:
                    st.warning(f"⚠️ Data quality issues detected: {'; '.join(issues)}")
                
                # Cache successful response
                if use_cache:
                    self.cache[cache_key] = {
                        'data': data,
                        'timestamp': time.time(),
                        'response_time': response_time,
                        'quality_score': 100 - len(issues) * 10
                    }
                
                self.request_stats['successful_requests'] += 1
                return data
                
            else:
                # Handle specific error codes
                error_messages = {
                    401: "Invalid API key. Please check your configuration.",
                    404: "Location not found. Please verify the coordinates or city name.",
                    429: "API rate limit exceeded. Please try again later.",
                    500: "OpenWeatherMap service error. Please try again later.",
                    502: "OpenWeatherMap service temporarily unavailable.",
                    503: "OpenWeatherMap service unavailable due to maintenance."
                }
                
                error_msg = error_messages.get(response.status_code, 
                                             f"API Error: {response.status_code}")
                
                # Track error statistics
                self.request_stats['failed_requests'] += 1
                error_code = str(response.status_code)
                self.request_stats['api_errors'][error_code] = \
                    self.request_stats['api_errors'].get(error_code, 0) + 1
                
                st.error(f"❌ {error_msg}")
                return None
                
        except requests.exceptions.Timeout:
            self.request_stats['failed_requests'] += 1
            self.request_stats['api_errors']['timeout'] = \
                self.request_stats['api_errors'].get('timeout', 0) + 1
            st.error("❌ Request timeout. The weather service is taking too long to respond.")
            return None
            
        except requests.exceptions.ConnectionError:
            self.request_stats['failed_requests'] += 1
            self.request_stats['api_errors']['connection'] = \
                self.request_stats['api_errors'].get('connection', 0) + 1
            st.error("❌ Connection error. Please check your internet connection.")
            return None
            
        except requests.exceptions.JSONDecodeError:
            self.request_stats['failed_requests'] += 1
            self.request_stats['api_errors']['json_decode'] = \
                self.request_stats['api_errors'].get('json_decode', 0) + 1
            st.error("❌ Invalid response format from weather service.")
            return None
            
        except Exception as e:
            self.request_stats['failed_requests'] += 1
            self.request_stats['api_errors']['unknown'] = \
                self.request_stats['api_errors'].get('unknown', 0) + 1
            st.error(f"❌ Unexpected error: {str(e)}")
            return None
    
    def get_current_weather_enhanced(self, lat: float, lon: float, 
                                   units: str = "metric") -> Optional[Dict]:
        """Enhanced current weather with additional processing"""
        url = f"{self.base_url}/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "units": units
        }
        
        data = self._make_request_with_analytics(url, params, 'current')
        
        if data:
            # Enhance data with additional calculations
            data = self._enhance_current_weather_data(data, units)
        
        return data
    
    def _enhance_current_weather_data(self, data: Dict, units: str) -> Dict:
        """Enhance current weather data with additional calculations"""
        if 'main' in data:
            main = data['main']
            
            # Calculate dew point
            temp = main['temp']
            humidity = main['humidity']
            dew_point = temp - ((100 - humidity) / 5)
            main['dew_point'] = dew_point
            
            # Calculate heat index or wind chill
            if 'wind' in data:
                wind_speed = data['wind']['speed']
                
                if temp >= 20:  # Heat index for warm weather
                    heat_index = self._calculate_heat_index(temp, humidity)
                    main['heat_index'] = heat_index
                elif temp <= 10 and wind_speed > 1:  # Wind chill for cold weather
                    wind_chill = self._calculate_wind_chill(temp, wind_speed)
                    main['wind_chill'] = wind_chill
            
            # Add comfort level
            comfort_score = self._calculate_simple_comfort(temp, humidity, 
                                                         data.get('wind', {}).get('speed', 0))
            main['comfort_score'] = comfort_score
        
        # Add data quality score
        is_valid, issues = self._validate_data_quality(data, 'current_weather')
        data['data_quality'] = {
            'score': 100 - len(issues) * 10,
            'issues': issues,
            'is_reliable': is_valid
        }
        
        # Add retrieval metadata
        data['metadata'] = {
            'retrieved_at': datetime.now().isoformat(),
            'api_response_time': self.request_stats.get('average_response_time', 0),
            'cache_status': 'miss',  # Will be updated if from cache
            'units': units
        }
        
        return data
    
    def _calculate_heat_index(self, temp: float, humidity: float) -> float:
        """Calculate heat index for warm weather"""
        # Simplified heat index calculation
        hi = temp + 0.5555 * (6.11 * np.exp(5417.7530 * ((1/273.16) - (1/(temp + 273.16)))) - 10)
        return round(hi, 1)
    
    def _calculate_wind_chill(self, temp: float, wind_speed: float) -> float:
        """Calculate wind chill for cold weather"""
        # Wind chill calculation (metric units)
        wind_kmh = wind_speed * 3.6  # Convert m/s to km/h
        wc = 13.12 + 0.6215 * temp - 11.37 * (wind_kmh ** 0.16) + 0.3965 * temp * (wind_kmh ** 0.16)
        return round(wc, 1)
    
    def _calculate_simple_comfort(self, temp: float, humidity: float, wind_speed: float) -> float:
        """Calculate simple comfort score (0-100)"""
        comfort = 100
        
        # Temperature comfort (optimal: 18-24°C)
        if not (18 <= temp <= 24):
            temp_penalty = min(abs(temp - 21) * 5, 50)
            comfort -= temp_penalty
        
        # Humidity comfort (optimal: 40-60%)
        if not (40 <= humidity <= 60):
            humidity_penalty = min(abs(humidity - 50) * 0.5, 25)
            comfort -= humidity_penalty
        
        # Wind comfort (optimal: < 5 m/s)
        if wind_speed > 5:
            wind_penalty = min((wind_speed - 5) * 3, 25)
            comfort -= wind_penalty
        
        return max(0, comfort)
    
    def get_forecast_enhanced(self, lat: float, lon: float, 
                            units: str = "metric") -> Optional[Dict]:
        """Enhanced forecast with extended analysis"""
        url = f"{self.base_url}/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "units": units
        }
        
        data = self._make_request_with_analytics(url, params, 'forecast')
        
        if data:
            # Enhance forecast data
            data = self._enhance_forecast_data(data, units)
        
        return data
    
    def _enhance_forecast_data(self, data: Dict, units: str) -> Dict:
        """Enhance forecast data with additional analysis"""
        if 'list' in data:
            enhanced_list = []
            
            for item in data['list']:
                # Add enhanced calculations to each forecast item
                item = self._enhance_current_weather_data(item, units)
                
                # Add forecast-specific enhancements
                if 'pop' in item:
                    # Convert probability of precipitation to percentage
                    item['precipitation_percentage'] = item['pop'] * 100
                
                # Add time-based insights
                dt = datetime.fromtimestamp(item['dt'])
                item['forecast_metadata'] = {
                    'day_of_week': dt.strftime('%A'),
                    'hour': dt.hour,
                    'is_daytime': 6 <= dt.hour <= 18,
                    'time_period': self._get_time_period(dt.hour)
                }
                
                enhanced_list.append(item)
            
            data['list'] = enhanced_list
            
            # Add forecast summary statistics
            data['forecast_summary'] = self._calculate_forecast_summary(enhanced_list)
        
        return data
    
    def _get_time_period(self, hour: int) -> str:
        """Get time period name for given hour"""
        if 6 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'afternoon'
        elif 18 <= hour < 22:
            return 'evening'
        else:
            return 'night'
    
    def _calculate_forecast_summary(self, forecast_list: List[Dict]) -> Dict:
        """Calculate summary statistics for forecast"""
        if not forecast_list:
            return {}
        
        temps = [item['main']['temp'] for item in forecast_list]
        humidity_values = [item['main']['humidity'] for item in forecast_list]
        wind_speeds = [item['wind']['speed'] for item in forecast_list]
        comfort_scores = [item['main'].get('comfort_score', 50) for item in forecast_list]
        
        return {
            'temperature': {
                'min': min(temps),
                'max': max(temps),
                'avg': sum(temps) / len(temps),
                'range': max(temps) - min(temps)
            },
            'comfort': {
                'avg_score': sum(comfort_scores) / len(comfort_scores),
                'best_periods': [
                    item['forecast_metadata']['time_period'] 
                    for item in forecast_list 
                    if item['main'].get('comfort_score', 0) > 80
                ]
            },
            'weather_patterns': self._analyze_forecast_patterns(forecast_list)
        }
    
    def _analyze_forecast_patterns(self, forecast_list: List[Dict]) -> Dict:
        """Analyze patterns in forecast data"""
        patterns = {
            'dominant_conditions': {},
            'temperature_trend': 'stable',
            'precipitation_days': 0,
            'high_wind_periods': 0
        }
        
        # Count weather conditions
        for item in forecast_list:
            condition = item['weather'][0]['main']
            patterns['dominant_conditions'][condition] = \
                patterns['dominant_conditions'].get(condition, 0) + 1
        
        # Analyze temperature trend
        temps = [item['main']['temp'] for item in forecast_list]
        if len(temps) > 1:
            temp_changes = [temps[i] - temps[i-1] for i in range(1, len(temps))]
            avg_change = sum(temp_changes) / len(temp_changes)
            
            if avg_change > 0.5:
                patterns['temperature_trend'] = 'increasing'
            elif avg_change < -0.5:
                patterns['temperature_trend'] = 'decreasing'
        
        # Count precipitation and high wind days
        for item in forecast_list:
            if item.get('precipitation_percentage', 0) > 50:
                patterns['precipitation_days'] += 1
            if item['wind']['speed'] > 10:
                patterns['high_wind_periods'] += 1
        
        return patterns
    
    def get_air_quality_enhanced(self, lat: float, lon: float) -> Optional[Dict]:
        """Enhanced air quality data with health recommendations"""
        params = {
            "lat": lat,
            "lon": lon
        }
        
        data = self._make_request_with_analytics(self.air_quality_url, params, 'air_quality')
        
        if data:
            data = self._enhance_air_quality_data(data)
        
        return data
    
    def _enhance_air_quality_data(self, data: Dict) -> Dict:
        """Enhance air quality data with health insights"""
        if 'list' in data and data['list']:
            aqi_data = data['list'][0]
            
            # Add health recommendations based on AQI
            aqi = aqi_data['main']['aqi']
            health_info = self._get_aqi_health_info(aqi)
            aqi_data['health_recommendations'] = health_info
            
            # Add component analysis
            if 'components' in aqi_data:
                components = aqi_data['components']
                aqi_data['component_analysis'] = self._analyze_air_components(components)
        
        return data
    
    def _get_aqi_health_info(self, aqi: int) -> Dict:
        """Get health information based on AQI level"""
        aqi_info = {
            1: {
                'level': 'Good',
                'description': 'Air quality is satisfactory',
                'recommendations': ['Perfect for outdoor activities', 'No health precautions needed'],
                'sensitive_groups': 'No restrictions'
            },
            2: {
                'level': 'Fair',
                'description': 'Air quality is acceptable',
                'recommendations': ['Outdoor activities are generally safe', 'Sensitive individuals should be aware'],
                'sensitive_groups': 'Very sensitive people might experience minor issues'
            },
            3: {
                'level': 'Moderate',
                'description': 'Sensitive groups may experience health effects',
                'recommendations': ['Reduce outdoor activities if you feel symptoms', 'Limit prolonged outdoor exertion'],
                'sensitive_groups': 'People with respiratory conditions should reduce outdoor activities'
            },
            4: {
                'level': 'Poor',
                'description': 'Health effects may be experienced by general population',
                'recommendations': ['Limit outdoor activities', 'Wear a mask when outdoors', 'Keep windows closed'],
                'sensitive_groups': 'Avoid outdoor activities'
            },
            5: {
                'level': 'Very Poor',
                'description': 'Health warnings of emergency conditions',
                'recommendations': ['Avoid outdoor activities', 'Stay indoors', 'Use air purifiers if available'],
                'sensitive_groups': 'Stay indoors and avoid any outdoor activities'
            }
        }
        
        return aqi_info.get(aqi, aqi_info[3])  # Default to moderate if unknown
    
    def _analyze_air_components(self, components: Dict) -> Dict:
        """Analyze individual air quality components"""
        analysis = {
            'primary_pollutants': [],
            'health_concerns': [],
            'component_levels': {}
        }
        
        # WHO air quality guidelines (µg/m³)
        who_guidelines = {
            'pm2_5': {'good': 15, 'moderate': 35, 'poor': 75},
            'pm10': {'good': 45, 'moderate': 100, 'poor': 150},
            'no2': {'good': 40, 'moderate': 100, 'poor': 200},
            'o3': {'good': 100, 'moderate': 180, 'poor': 240},
            'so2': {'good': 20, 'moderate': 80, 'poor': 250}
        }
        
        for component, value in components.items():
            if component in who_guidelines:
                guidelines = who_guidelines[component]
                
                if value > guidelines['poor']:
                    level = 'poor'
                    analysis['primary_pollutants'].append(component.upper())
                    analysis['health_concerns'].append(f'{component.upper()} levels are very high')
                elif value > guidelines['moderate']:
                    level = 'moderate'
                elif value > guidelines['good']:
                    level = 'fair'
                else:
                    level = 'good'
                
                analysis['component_levels'][component] = {
                    'value': value,
                    'level': level,
                    'guideline': guidelines['good']
                }
        
        return analysis
    
    def get_weather_maps_data(self, lat: float, lon: float, 
                            map_layers: List[str] = None) -> Dict[str, str]:
        """Get URLs for various weather map layers"""
        if map_layers is None:
            map_layers = ['temp_new', 'precipitation_new', 'pressure_new', 'wind_new', 'clouds_new']
        
        map_urls = {}
        
        for layer in map_layers:
            url = f"{self.maps_url}/{layer}/1/{lat}/{lon}"
            map_urls[layer] = f"{url}?appid={self.api_key}"
        
        return map_urls
    
    def get_bulk_weather_data_async(self, locations: List[Tuple[float, float]], 
                                  units: str = "metric") -> Dict[str, Dict]:
        """Get weather data for multiple locations efficiently using async requests"""
        
        async def fetch_weather(session, lat, lon):
            url = f"{self.base_url}/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "units": units,
                "appid": self.api_key
            }
            
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return f"{lat},{lon}", data
                    else:
                        return f"{lat},{lon}", None
            except Exception:
                return f"{lat},{lon}", None
        
        async def fetch_all_locations():
            async with aiohttp.ClientSession() as session:
                tasks = [fetch_weather(session, lat, lon) for lat, lon in locations]
                results = await asyncio.gather(*tasks)
                return dict(results)
        
        try:
            # Run async requests
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(fetch_all_locations())
            loop.close()
            
            # Filter out None results and enhance data
            enhanced_results = {}
            for location_key, data in results.items():
                if data:
                    enhanced_results[location_key] = self._enhance_current_weather_data(data, units)
            
            return enhanced_results
            
        except Exception as e:
            st.warning(f"Async request failed, falling back to sequential: {str(e)}")
            return self.get_bulk_weather_data_sequential(locations, units)
    
    def get_bulk_weather_data_sequential(self, locations: List[Tuple[float, float]], 
                                       units: str = "metric") -> Dict[str, Dict]:
        """Fallback sequential method for bulk weather data"""
        results = {}
        
        for i, (lat, lon) in enumerate(locations):
            location_key = f"{lat},{lon}"
            
            # Add delay to respect rate limits
            if i > 0:
                time.sleep(0.2)
            
            weather_data = self.get_current_weather_enhanced(lat, lon, units)
            if weather_data:
                results[location_key] = weather_data
            
            # Check if approaching rate limits
            if self.request_count >= self.daily_limit * 0.9:
                st.warning("⚠️ Approaching API rate limit. Some requests may be skipped.")
                break
        
        return results
    
    def get_historical_weather_advanced(self, lat: float, lon: float, 
                                      target_date: datetime.date,
                                      units: str = "metric") -> Optional[Dict]:
        """Get historical weather data with enhanced analysis"""
        target_datetime = datetime.combine(target_date, datetime.min.time())
        dt_timestamp = int(target_datetime.timestamp())
        
        try:
            url = self.premium_endpoints['historical']
            params = {
                "lat": lat,
                "lon": lon,
                "dt": dt_timestamp,
                "units": units
            }
            
            data = self._make_request_with_analytics(url, params, 'historical')
            
            if data:
                # Enhance historical data
                data = self._enhance_historical_data(data, target_date)
            
            return data
            
        except Exception as e:
            st.info("📊 Historical data requires premium API access")
            return None
    
    def _enhance_historical_data(self, data: Dict, target_date: datetime) -> Dict:
        """Enhance historical weather data"""
        if 'current' in data:
            current = data['current']
            
            # Add date context
            current['date_info'] = {
                'target_date': target_date.isoformat(),
                'day_of_week': target_date.strftime('%A'),
                'day_of_year': target_date.timetuple().tm_yday,
                'week_of_year': target_date.isocalendar()[1],
                'season': self._get_season(target_date.month)
            }
            
            # Calculate historical comfort score
            if 'temp' in current and 'humidity' in current:
                wind_speed = current.get('wind_speed', 0)
                comfort_score = self._calculate_simple_comfort(
                    current['temp'], 
                    current['humidity'], 
                    wind_speed
                )
                current['historical_comfort_score'] = comfort_score
        
        return data
    
    def _get_season(self, month: int) -> str:
        """Get season based on month"""
        if 3 <= month <= 5:
            return 'Spring'
        elif 6 <= month <= 8:
            return 'Summer'
        elif 9 <= month <= 11:
            return 'Autumn'
        else:
            return 'Winter'
    
    def get_weather_alerts_advanced(self, lat: float, lon: float) -> Optional[List[Dict]]:
        """Get advanced weather alerts with severity analysis"""
        try:
            url = f"{self.onecall_url}"
            params = {
                "lat": lat,
                "lon": lon,
                "exclude": "current,minutely,hourly,daily",
                "alerts": "true"
            }
            
            data = self._make_request_with_analytics(url, params, 'current', use_cache=False)
            
            if data and 'alerts' in data:
                enhanced_alerts = []
                for alert in data['alerts']:
                    enhanced_alert = self._enhance_alert_data(alert)
                    enhanced_alerts.append(enhanced_alert)
                
                return enhanced_alerts
            
            return []
            
        except Exception:
            # Fallback to basic alert detection from current weather
            return self._generate_basic_alerts(lat, lon)
    
    def _enhance_alert_data(self, alert: Dict) -> Dict:
        """Enhance alert data with additional analysis"""
        enhanced_alert = alert.copy()
        
        # Classify alert severity
        event = alert.get('event', '').lower()
        severity_keywords = {
            'extreme': ['extreme', 'severe', 'dangerous', 'life-threatening'],
            'high': ['warning', 'advisory', 'strong', 'heavy'],
            'medium': ['watch', 'moderate', 'light'],
            'low': ['minor', 'brief', 'isolated']
        }
        
        enhanced_alert['severity_level'] = 'medium'  # default
        for level, keywords in severity_keywords.items():
            if any(keyword in event for keyword in keywords):
                enhanced_alert['severity_level'] = level
                break
        
        # Add time context
        start_time = datetime.fromtimestamp(alert.get('start', 0))
        end_time = datetime.fromtimestamp(alert.get('end', 0))
        
        enhanced_alert['time_context'] = {
            'starts_in_hours': (start_time - datetime.now()).total_seconds() / 3600,
            'duration_hours': (end_time - start_time).total_seconds() / 3600,
            'is_active': start_time <= datetime.now() <= end_time
        }
        
        # Generate action recommendations
        enhanced_alert['recommendations'] = self._generate_alert_recommendations(alert)
        
        return enhanced_alert
    
    def _generate_alert_recommendations(self, alert: Dict) -> List[str]:
        """Generate action recommendations based on alert type"""
        event = alert.get('event', '').lower()
        recommendations = []
        
        if 'thunder' in event or 'storm' in event:
            recommendations.extend([
                "Stay indoors and away from windows",
                "Avoid using electrical appliances",
                "Do not go outside until the storm passes"
            ])
        elif 'wind' in event:
            recommendations.extend([
                "Secure loose outdoor objects",
                "Avoid driving high-profile vehicles",
                "Stay away from trees and power lines"
            ])
        elif 'heat' in event:
            recommendations.extend([
                "Stay hydrated and in air conditioning",
                "Avoid prolonged outdoor activities",
                "Check on elderly neighbors and relatives"
            ])
        elif 'cold' in event or 'freeze' in event:
            recommendations.extend([
                "Protect pipes from freezing",
                "Dress in layers when going outside",
                "Ensure adequate heating"
            ])
        elif 'snow' in event or 'ice' in event:
            recommendations.extend([
                "Avoid unnecessary travel",
                "Drive slowly and carefully if you must travel",
                "Keep emergency supplies in your vehicle"
            ])
        
        return recommendations
    
    def _generate_basic_alerts(self, lat: float, lon: float) -> List[Dict]:
        """Generate basic alerts from current weather conditions"""
        current_weather = self.get_current_weather_enhanced(lat, lon)
        alerts = []
        
        if current_weather and 'main' in current_weather:
            temp = current_weather['main']['temp']
            humidity = current_weather['main']['humidity']
            wind_speed = current_weather['wind'].get('speed', 0)
            condition = current_weather['weather'][0]['main'].lower()
            
            # Temperature-based alerts
            if temp > 35:
                alerts.append({
                    'event': 'Extreme Heat Warning',
                    'severity_level': 'high',
                    'description': f'Temperature is {temp}°C - dangerously hot conditions',
                    'recommendations': ['Stay hydrated', 'Avoid outdoor activities', 'Seek air conditioning']
                })
            elif temp < -10:
                alerts.append({
                    'event': 'Extreme Cold Warning',
                    'severity_level': 'high',
                    'description': f'Temperature is {temp}°C - dangerously cold conditions',
                    'recommendations': ['Dress warmly', 'Limit outdoor exposure', 'Protect pipes']
                })
            
            # Wind-based alerts
            if wind_speed > 20:
                alerts.append({
                    'event': 'High Wind Warning',
                    'severity_level': 'medium',
                    'description': f'Wind speed is {wind_speed} m/s - strong winds expected',
                    'recommendations': ['Secure loose objects', 'Avoid high-profile vehicles', 'Be cautious outdoors']
                })
            
            # Condition-based alerts
            if 'thunderstorm' in condition:
                alerts.append({
                    'event': 'Thunderstorm Alert',
                    'severity_level': 'medium',
                    'description': 'Thunderstorm conditions present',
                    'recommendations': ['Stay indoors', 'Avoid electrical appliances', 'Monitor weather updates']
                })
        
        return alerts
    
    def validate_api_key_comprehensive(self) -> Dict[str, Any]:
        """Comprehensive API key validation with detailed feedback"""
        if self.api_key == "YOUR_API_KEY_HERE":
            return {
                'is_valid': False,
                'status': 'not_configured',
                'message': 'API key not configured',
                'suggestions': ['Add OPENWEATHER_API_KEY to secrets.toml']
            }
        
        # Test API key with a simple request
        url = f"{self.base_url}/weather"
        params = {
            "q": "London",
            "appid": self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                # Test subscription level
                subscription_info = self._detect_subscription_level()
                
                return {
                    'is_valid': True,
                    'status': 'active',
                    'message': 'API key is valid and working',
                    'subscription_level': subscription_info['level'],
                    'features_available': subscription_info['features'],
                    'daily_calls_remaining': max(0, self.daily_limit - self.request_count)
                }
                
            elif response.status_code == 401:
                return {
                    'is_valid': False,
                    'status': 'invalid',
                    'message': 'Invalid API key',
                    'suggestions': ['Check API key spelling', 'Verify key is active', 'Generate new key if needed']
                }
                
            elif response.status_code == 429:
                return {
                    'is_valid': True,
                    'status': 'rate_limited',
                    'message': 'API key valid but rate limited',
                    'suggestions': ['Wait before making more requests', 'Consider upgrading subscription']
                }
                
            else:
                return {
                    'is_valid': False,
                    'status': 'error',
                    'message': f'API error: {response.status_code}',
                    'suggestions': ['Try again later', 'Check OpenWeatherMap service status']
                }
                
        except Exception as e:
            return {
                'is_valid': False,
                'status': 'connection_error',
                'message': f'Connection error: {str(e)}',
                'suggestions': ['Check internet connection', 'Verify firewall settings']
            }
    
    def _detect_subscription_level(self) -> Dict[str, Any]:
        """Detect subscription level and available features"""
        # Test various endpoints to determine subscription level
        features = {
            'current_weather': True,  # Available in free tier
            'forecast': True,         # Available in free tier
            'air_quality': True,      # Available in free tier
            'historical': False,      # Premium feature
            'maps': True,            # Available in free tier
            'alerts': False          # Premium feature
        }
        
        subscription_level = 'free'
        
        # Test premium endpoints
        try:
            # Test One Call API (premium)
            url = f"{self.onecall_url}"
            params = {
                "lat": 51.5074,
                "lon": -0.1278,
                "exclude": "minutely",
                "appid": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                features['alerts'] = True
                features['historical'] = True
                subscription_level = 'premium'
                
        except:
            pass  # Premium features not available
        
        return {
            'level': subscription_level,
            'features': features
        }
    
    def get_api_usage_analytics(self) -> Dict[str, Any]:
        """Get comprehensive API usage analytics"""
        
        # Calculate success rate
        total_requests = self.request_stats['total_requests']
        success_rate = (self.request_stats['successful_requests'] / total_requests * 100) if total_requests > 0 else 0
        
        # Calculate cache efficiency
        cache_hit_rate = (self.request_stats['cache_hits'] / 
                         (total_requests + self.request_stats['cache_hits']) * 100) if total_requests > 0 else 0
        
        # Analyze error patterns
        error_analysis = {}
        total_errors = self.request_stats['failed_requests']
        if total_errors > 0:
            for error_type, count in self.request_stats['api_errors'].items():
                error_analysis[error_type] = {
                    'count': count,
                    'percentage': (count / total_errors * 100)
                }
        
        # Performance metrics
        performance_metrics = {
            'average_response_time': self.request_stats['average_response_time'],
            'total_requests': total_requests,
            'successful_requests': self.request_stats['successful_requests'],
            'failed_requests': self.request_stats['failed_requests'],
            'cache_hits': self.request_stats['cache_hits']
        }
        
        # Rate limiting status
        rate_limit_status = {
            'daily_limit': self.daily_limit,
            'requests_used': self.request_count,
            'requests_remaining': max(0, self.daily_limit - self.request_count),
            'usage_percentage': (self.request_count / self.daily_limit * 100),
            'burst_window_usage': len(self.burst_window),
            'burst_limit': self.burst_limit
        }
        
        # Data quality metrics
        quality_scores = []
        for cache_entry in self.cache.values():
            if 'quality_score' in cache_entry:
                quality_scores.append(cache_entry['quality_score'])
        
        data_quality = {
            'average_quality_score': sum(quality_scores) / len(quality_scores) if quality_scores else 100,
            'total_cached_responses': len(self.cache),
            'quality_issues_detected': sum(1 for score in quality_scores if score < 90)
        }
        
        return {
            'performance': performance_metrics,
            'success_rate': success_rate,
            'cache_efficiency': cache_hit_rate,
            'error_analysis': error_analysis,
            'rate_limiting': rate_limit_status,
            'data_quality': data_quality,
            'recommendations': self._generate_usage_recommendations(
                success_rate, cache_hit_rate, rate_limit_status
            )
        }
    
    def _generate_usage_recommendations(self, success_rate: float, 
                                      cache_hit_rate: float, 
                                      rate_limit_status: Dict) -> List[str]:
        """Generate recommendations for API usage optimization"""
        recommendations = []
        
        if success_rate < 90:
            recommendations.append("Consider implementing retry logic for failed requests")
        
        if cache_hit_rate < 30:
            recommendations.append("Increase cache duration to reduce API calls")
        
        if rate_limit_status['usage_percentage'] > 80:
            recommendations.append("Consider upgrading API subscription or optimizing request frequency")
        
        if self.request_stats['average_response_time'] > 2:
            recommendations.append("Monitor API response times - consider implementing timeout adjustments")
        
        if len(self.request_stats['api_errors']) > 3:
            recommendations.append("Implement better error handling for different error types")
        
        return recommendations
    
    def clear_cache_selective(self, cache_types: List[str] = None):
        """Clear cache selectively by data type"""
        if cache_types is None:
            self.cache.clear()
            st.success("🗑️ All cache cleared successfully!")
            return
        
        keys_to_remove = []
        for key, cache_entry in self.cache.items():
            # This is a simplified approach - in a real implementation,
            # you'd need to track cache type in the cache entry
            for cache_type in cache_types:
                if cache_type in key:  # Simple heuristic
                    keys_to_remove.append(key)
                    break
        
        for key in keys_to_remove:
            del self.cache[key]
        
        st.success(f"🗑️ Cleared {len(keys_to_remove)} cache entries for types: {', '.join(cache_types)}")
    
    def export_usage_statistics(self) -> Dict[str, Any]:
        """Export usage statistics for analysis"""
        return {
            'export_timestamp': datetime.now().isoformat(),
            'request_statistics': self.request_stats,
            'cache_statistics': {
                'total_entries': len(self.cache),
                'cache_types': list(self.cache_duration.keys()),
                'average_cache_age': self._calculate_average_cache_age()
            },
            'rate_limiting': {
                'daily_limit': self.daily_limit,
                'current_usage': self.request_count,
                'burst_limit': self.burst_limit,
                'current_burst_usage': len(self.burst_window)
            },
            'configuration': {
                'cache_durations': self.cache_duration,
                'rate_limit_delay': self.rate_limit_delay,
                'quality_thresholds': self.data_quality_thresholds
            }
        }
    
    def _calculate_average_cache_age(self) -> float:
        """Calculate average age of cache entries in seconds"""
        if not self.cache:
            return 0
        
        current_time = time.time()
        ages = [current_time - entry['timestamp'] for entry in self.cache.values()]
        return sum(ages) / len(ages)
    
    def reset_statistics(self):
        """Reset all usage statistics"""
        self.request_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'cache_hits': 0,
            'api_errors': {},
            'average_response_time': 0,
            'response_times': []
        }
        self.request_count = 0
        self.burst_window = []
        
        st.success("📊 Usage statistics reset successfully!")
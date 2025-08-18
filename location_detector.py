import requests
import streamlit as st
from typing import Dict, Optional, List, Tuple, Any
import json
import time
import hashlib
from datetime import datetime, timezone
import re

class LocationDetector:
    """Premium location detection and geocoding services with advanced features"""
    
    def __init__(self):
        # Enhanced API endpoints
        self.ip_api_url = "http://ip-api.com/json"
        self.ipinfo_url = "https://ipinfo.io"
        self.geocoding_url = "http://api.openweathermap.org/geo/1.0"
        self.timezone_url = "http://worldtimeapi.org/api"
        
        # Caching system
        self.cache = {}
        self.cache_duration = 1800  # 30 minutes for location data
        
        # Location accuracy levels
        self.accuracy_levels = {
            'high': 'GPS/Precise coordinates',
            'medium': 'City/IP-based location',
            'low': 'Country/Region level',
            'unknown': 'Location accuracy unknown'
        }
        
        # Supported location formats
        self.coordinate_patterns = [
            r'^(-?\d+\.?\d*),\s*(-?\d+\.?\d*)$',  # lat,lon
            r'^(-?\d+\.?\d*)\s+(-?\d+\.?\d*)$',   # lat lon
            r'^\((-?\d+\.?\d*),\s*(-?\d+\.?\d*)\)$'  # (lat,lon)
        ]
        
    def _get_cache_key(self, method: str, params: str) -> str:
        """Generate cache key for location requests"""
        return hashlib.md5(f"{method}:{params}".encode()).hexdigest()
    
    def _is_cache_valid(self, cache_entry: Dict) -> bool:
        """Check if cache entry is still valid"""
        return (time.time() - cache_entry['timestamp']) < self.cache_duration
    
    def _cache_result(self, key: str, data: Dict):
        """Cache the result with timestamp"""
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
    
    def get_location_by_ip(self, use_fallback: bool = True) -> Optional[Dict]:
        """Enhanced IP-based location detection with multiple providers"""
        cache_key = self._get_cache_key("ip_location", "default")
        
        # Check cache first
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key]):
            return self.cache[cache_key]['data']
        
        # Primary IP location service
        location_data = self._try_ip_api_com()
        
        # Fallback to alternative services if primary fails
        if not location_data and use_fallback:
            location_data = self._try_ipinfo_io()
        
        if location_data:
            # Enhance with additional data
            location_data = self._enhance_location_data(location_data)
            # Cache the result
            self._cache_result(cache_key, location_data)
            
        return location_data
    
    def _try_ip_api_com(self) -> Optional[Dict]:
        """Try ip-api.com for location detection"""
        try:
            with st.spinner("🌍 Detecting your location..."):
                response = requests.get(
                    f"{self.ip_api_url}?fields=status,country,countryCode,region,regionName,city,lat,lon,timezone,query,isp,org,as",
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
                            'lat': float(data.get('lat', 0)),
                            'lon': float(data.get('lon', 0)),
                            'timezone': data.get('timezone', ''),
                            'ip': data.get('query', ''),
                            'isp': data.get('isp', ''),
                            'accuracy': 'medium',
                            'source': 'ip-api.com',
                            'detection_method': 'IP Geolocation'
                        }
                return None
                
        except requests.exceptions.Timeout:
            st.warning("⏱️ Location detection timeout. Trying alternative method...")
            return None
        except requests.exceptions.ConnectionError:
            st.warning("🌐 Connection error during location detection.")
            return None
        except Exception as e:
            st.warning(f"⚠️ Location detection failed: {str(e)}")
            return None
    
    def _try_ipinfo_io(self) -> Optional[Dict]:
        """Try ipinfo.io as fallback location service"""
        try:
            response = requests.get(f"{self.ipinfo_url}/json", timeout=8)
            
            if response.status_code == 200:
                data = response.json()
                
                # Parse location string (e.g., "37.7749,-122.4194")
                loc_parts = data.get('loc', '0,0').split(',')
                lat, lon = float(loc_parts[0]), float(loc_parts[1])
                
                return {
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('region', ''),
                    'country': data.get('country', 'Unknown'),
                    'country_code': data.get('country', ''),
                    'lat': lat,
                    'lon': lon,
                    'timezone': data.get('timezone', ''),
                    'ip': data.get('ip', ''),
                    'isp': data.get('org', ''),
                    'accuracy': 'medium',
                    'source': 'ipinfo.io',
                    'detection_method': 'IP Geolocation'
                }
            return None
            
        except Exception:
            return None
    
    def _enhance_location_data(self, location_data: Dict) -> Dict:
        """Enhance location data with additional information"""
        enhanced_data = location_data.copy()
        
        # Add timestamp
        enhanced_data['detected_at'] = datetime.now(timezone.utc).isoformat()
        
        # Calculate timezone offset if timezone name is available
        if enhanced_data.get('timezone'):
            enhanced_data['timezone_offset'] = self._get_timezone_offset(
                enhanced_data['lat'], 
                enhanced_data['lon']
            )
        
        # Add coordinate precision
        enhanced_data['coordinate_precision'] = self._assess_coordinate_precision(
            enhanced_data['lat'], 
            enhanced_data['lon']
        )
        
        # Add location confidence score
        enhanced_data['confidence_score'] = self._calculate_location_confidence(enhanced_data)
        
        return enhanced_data
    
    def _assess_coordinate_precision(self, lat: float, lon: float) -> str:
        """Assess the precision of coordinates"""
        lat_str, lon_str = str(lat), str(lon)
        
        lat_decimals = len(lat_str.split('.')[-1]) if '.' in lat_str else 0
        lon_decimals = len(lon_str.split('.')[-1]) if '.' in lon_str else 0
        
        avg_decimals = (lat_decimals + lon_decimals) / 2
        
        if avg_decimals >= 4:
            return "high"  # ~11m accuracy
        elif avg_decimals >= 3:
            return "medium"  # ~110m accuracy
        elif avg_decimals >= 2:
            return "low"  # ~1.1km accuracy
        else:
            return "very_low"  # >11km accuracy
    
    def _calculate_location_confidence(self, location_data: Dict) -> float:
        """Calculate confidence score for location data (0-1)"""
        confidence = 0.0
        
        # Base confidence from source
        if location_data.get('source') == 'ip-api.com':
            confidence += 0.3
        elif location_data.get('source') == 'ipinfo.io':
            confidence += 0.25
        
        # City availability
        if location_data.get('city') and location_data['city'] != 'Unknown':
            confidence += 0.2
        
        # Coordinate precision
        precision = location_data.get('coordinate_precision', 'very_low')
        precision_scores = {'high': 0.3, 'medium': 0.2, 'low': 0.1, 'very_low': 0.05}
        confidence += precision_scores.get(precision, 0)
        
        # ISP information available
        if location_data.get('isp'):
            confidence += 0.1
        
        # Timezone information
        if location_data.get('timezone'):
            confidence += 0.15
        
        return min(1.0, confidence)
    
    def get_location(self) -> Optional[Dict]:
        """Primary method to get user location with enhanced feedback"""
        location_data = self.get_location_by_ip()
        
        if location_data:
            confidence = location_data.get('confidence_score', 0)
            
            if confidence > 0.8:
                st.success(f"📍 High-accuracy location detected: {self.format_location_display(location_data)}")
            elif confidence > 0.6:
                st.info(f"📍 Location detected: {self.format_location_display(location_data)}")
            else:
                st.warning(f"📍 Approximate location: {self.format_location_display(location_data)} (Low accuracy)")
        
        return location_data
    
    def search_location(self, query: str) -> Optional[Dict]:
        """Enhanced location search with smart parsing"""
        # Check cache first
        cache_key = self._get_cache_key("search", query.lower().strip())
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key]):
            return self.cache[cache_key]['data']
        
        # Check if query is coordinates
        coords = self._parse_coordinates(query)
        if coords:
            location_data = self._handle_coordinate_search(coords[0], coords[1])
            if location_data:
                self._cache_result(cache_key, location_data)
            return location_data
        
        # Regular location name search
        location_data = self._search_by_name(query)
        if location_data:
            self._cache_result(cache_key, location_data)
        
        return location_data
    
    def _parse_coordinates(self, query: str) -> Optional[Tuple[float, float]]:
        """Parse coordinate strings in various formats"""
        query = query.strip()
        
        for pattern in self.coordinate_patterns:
            match = re.match(pattern, query)
            if match:
                try:
                    lat, lon = float(match.group(1)), float(match.group(2))
                    if self.validate_coordinates(lat, lon):
                        return lat, lon
                except ValueError:
                    continue
        
        return None
    
    def _handle_coordinate_search(self, lat: float, lon: float) -> Optional[Dict]:
        """Handle coordinate-based location search"""
        try:
            # Try reverse geocoding first
            location_data = self.reverse_geocode(lat, lon)
            
            if not location_data:
                # Create basic location data if reverse geocoding fails
                location_data = {
                    'city': f"Location {lat:.4f}, {lon:.4f}",
                    'region': '',
                    'country': 'Unknown',
                    'country_code': '',
                    'lat': lat,
                    'lon': lon,
                    'timezone': self._get_timezone_info(lat, lon),
                    'ip': '',
                    'accuracy': 'high',
                    'source': 'user_input',
                    'detection_method': 'Coordinates',
                    'coordinate_precision': 'high',
                    'confidence_score': 0.9
                }
            
            return location_data
            
        except Exception as e:
            st.error(f"❌ Invalid coordinates: {str(e)}")
            return None
    
    def _search_by_name(self, query: str) -> Optional[Dict]:
        """Search location by name using OpenWeatherMap geocoding"""
        try:
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
                    
                    # Get timezone information
                    timezone_info = self._get_timezone_info(
                        location.get('lat', 0), 
                        location.get('lon', 0)
                    )
                    
                    return {
                        'city': location.get('name', 'Unknown'),
                        'region': location.get('state', ''),
                        'country': location.get('country', 'Unknown'),
                        'country_code': location.get('country', ''),
                        'lat': float(location.get('lat', 0)),
                        'lon': float(location.get('lon', 0)),
                        'timezone': timezone_info,
                        'ip': '',
                        'accuracy': 'high',
                        'source': 'openweathermap',
                        'detection_method': 'Geocoding Search',
                        'coordinate_precision': 'high',
                        'confidence_score': 0.95,
                        'local_names': location.get('local_names', {}),
                        'search_query': query
                    }
            return None
            
        except requests.exceptions.Timeout:
            st.error("❌ Location search timeout. Please try again.")
            return None
        except requests.exceptions.ConnectionError:
            st.error("❌ Connection error during location search.")
            return None
        except Exception as e:
            st.error(f"❌ Location search failed: {str(e)}")
            return None
    
    def _get_api_key(self) -> str:
        """Get API key for geocoding with enhanced error handling"""
        try:
            # Try different secret key formats
            if hasattr(st.secrets, "default") and "OPENWEATHER_API_KEY" in st.secrets.default:
                return st.secrets.default["OPENWEATHER_API_KEY"]
            elif "OPENWEATHER_API_KEY" in st.secrets:
                return st.secrets["OPENWEATHER_API_KEY"]
            else:
                return "YOUR_API_KEY_HERE"
        except Exception:
            return "YOUR_API_KEY_HERE"
    
    def reverse_geocode(self, lat: float, lon: float) -> Optional[Dict]:
        """Enhanced reverse geocoding with detailed location information"""
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
                        'timezone': self._get_timezone_info(lat, lon),
                        'ip': '',
                        'accuracy': 'high',
                        'source': 'reverse_geocoding',
                        'detection_method': 'Reverse Geocoding',
                        'coordinate_precision': 'high',
                        'confidence_score': 0.9,
                        'local_names': location.get('local_names', {})
                    }
            return None
            
        except Exception:
            return None
    
    def get_nearby_cities(self, lat: float, lon: float, radius: int = 50, limit: int = 10) -> List[Dict]:
        """Get nearby cities within specified radius with enhanced data"""
        try:
            api_key = self._get_api_key()
            if not api_key or api_key == "YOUR_API_KEY_HERE":
                return []
            
            # Search for nearby locations using a bounding box
            lat_offset = radius / 111.32  # Approximate km to degrees conversion
            lon_offset = radius / (111.32 * abs(np.cos(np.radians(lat))))
            
            nearby_cities = []
            
            # Search in multiple directions to find nearby cities
            search_points = [
                (lat + lat_offset/2, lon),  # North
                (lat - lat_offset/2, lon),  # South
                (lat, lon + lon_offset/2),  # East
                (lat, lon - lon_offset/2),  # West
            ]
            
            for search_lat, search_lon in search_points:
                try:
                    result = self.reverse_geocode(search_lat, search_lon)
                    if result and result not in nearby_cities:
                        # Calculate distance
                        distance = self._calculate_distance(lat, lon, search_lat, search_lon)
                        if distance <= radius:
                            result['distance_km'] = round(distance, 1)
                            nearby_cities.append(result)
                except:
                    continue
            
            # Sort by distance and limit results
            nearby_cities.sort(key=lambda x: x.get('distance_km', float('inf')))
            return nearby_cities[:limit]
            
        except Exception:
            return []
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
        import math
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth's radius in kilometers
        r = 6371
        
        return r * c
    
    def validate_coordinates(self, lat: float, lon: float) -> bool:
        """Enhanced coordinate validation with detailed feedback"""
        try:
            # Basic range validation
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                return False
            
            # Check for obviously invalid coordinates
            # (0,0) is in the ocean but technically valid
            if lat == 0 and lon == 0:
                st.warning("⚠️ Coordinates (0,0) detected - this is in the ocean near Africa")
            
            return True
            
        except (TypeError, ValueError):
            return False
    
    def format_location_display(self, location_data: Dict) -> str:
        """Enhanced location display formatting with additional details"""
        if not location_data:
            return "Unknown Location"
        
        city = location_data.get('city', 'Unknown')
        region = location_data.get('region', '')
        country = location_data.get('country', 'Unknown')
        
        # Build display string
        parts = [city]
        
        if region and region != city and region.lower() != country.lower():
            parts.append(region)
        
        if country and country != 'Unknown':
            parts.append(country)
        
        location_str = ', '.join(parts)
        
        # Add accuracy indicator if available
        confidence = location_data.get('confidence_score', 0)
        if confidence < 0.6:
            location_str += " (approximate)"
        
        return location_str
    
    def get_timezone_info(self, lat: float, lon: float) -> Optional[str]:
        """Enhanced timezone detection with multiple methods"""
        timezone_info = self._get_timezone_info(lat, lon)
        
        if not timezone_info:
            # Fallback to simple calculation
            timezone_info = self._calculate_simple_timezone(lon)
        
        return timezone_info
    
    def _get_timezone_info(self, lat: float, lon: float) -> Optional[str]:
        """Get accurate timezone information from external API"""
        try:
            # Try WorldTimeAPI first
            response = requests.get(
                f"{self.timezone_url}/timezone/Etc/GMT",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('timezone', self._calculate_simple_timezone(lon))
            
        except:
            pass
        
        # Fallback to simple calculation
        return self._calculate_simple_timezone(lon)
    
    def _calculate_simple_timezone(self, lon: float) -> str:
        """Simple timezone calculation based on longitude"""
        try:
            utc_offset = round(lon / 15)
            
            # Clamp to valid range
            utc_offset = max(-12, min(14, utc_offset))
            
            if utc_offset >= 0:
                return f"UTC+{utc_offset}"
            else:
                return f"UTC{utc_offset}"
                
        except:
            return "UTC+0"
    
    def _get_timezone_offset(self, lat: float, lon: float) -> Optional[int]:
        """Get timezone offset in hours"""
        timezone_str = self._get_timezone_info(lat, lon)
        
        if timezone_str and 'UTC' in timezone_str:
            try:
                offset_str = timezone_str.replace('UTC', '').replace('+', '')
                return int(offset_str) if offset_str else 0
            except:
                return None
        
        return None
    
    def get_location_suggestions(self, partial_query: str, limit: int = 5) -> List[Dict]:
        """Get location suggestions for autocomplete"""
        if len(partial_query) < 2:
            return []
        
        try:
            api_key = self._get_api_key()
            if not api_key or api_key == "YOUR_API_KEY_HERE":
                return []
            
            url = f"{self.geocoding_url}/direct"
            params = {
                "q": partial_query,
                "limit": limit,
                "appid": api_key
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                suggestions = []
                
                for item in data:
                    suggestion = {
                        'display_name': self._format_suggestion_display(item),
                        'city': item.get('name', ''),
                        'country': item.get('country', ''),
                        'state': item.get('state', ''),
                        'lat': item.get('lat', 0),
                        'lon': item.get('lon', 0)
                    }
                    suggestions.append(suggestion)
                
                return suggestions
            
        except Exception:
            pass
        
        return []
    
    def _format_suggestion_display(self, location_data: Dict) -> str:
        """Format location for suggestion display"""
        name = location_data.get('name', '')
        state = location_data.get('state', '')
        country = location_data.get('country', '')
        
        parts = [name]
        
        if state and state != name:
            parts.append(state)
        
        if country:
            parts.append(country)
        
        return ', '.join(parts)
    
    def get_location_analytics(self) -> Dict[str, Any]:
        """Get analytics about location detection performance"""
        total_cached = len(self.cache)
        
        # Analyze cache data
        high_confidence = sum(1 for entry in self.cache.values() 
                            if entry['data'].get('confidence_score', 0) > 0.8)
        
        sources = {}
        for entry in self.cache.values():
            source = entry['data'].get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        return {
            'total_locations_cached': total_cached,
            'high_confidence_locations': high_confidence,
            'confidence_percentage': round((high_confidence / total_cached * 100) if total_cached > 0 else 0, 1),
            'sources_used': sources,
            'cache_hit_potential': round((total_cached / max(total_cached, 1)) * 100, 1)
        }
    
    def clear_cache(self):
        """Clear the location cache"""
        self.cache.clear()
        st.success("Location cache cleared successfully!")
    
    def export_location_history(self) -> List[Dict]:
        """Export cached location history"""
        history = []
        
        for cache_entry in self.cache.values():
            location_data = cache_entry['data'].copy()
            location_data['cached_at'] = datetime.fromtimestamp(cache_entry['timestamp']).isoformat()
            history.append(location_data)
        
        # Sort by cache timestamp
        history.sort(key=lambda x: x.get('cached_at', ''), reverse=True)
        
        return history
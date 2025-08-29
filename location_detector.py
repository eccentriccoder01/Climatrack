import requests
import streamlit as st
from typing import Dict, Optional, List, Tuple, Any
import json
import time
import hashlib
from datetime import datetime, timezone
import re
import numpy as np
from geopy.distance import geodesic
import asyncio
import aiohttp

class PremiumLocationDetector:
    """Premium location detection and geocoding services with advanced AI features"""
    
    def __init__(self):
        # Enhanced API endpoints with premium providers
        self.primary_providers = {
            'ip_api': {
                'url': "http://ip-api.com/json",
                'fields': "status,country,countryCode,region,regionName,city,lat,lon,timezone,query,isp,org,as,mobile,proxy,hosting",
                'accuracy': 'medium',
                'rate_limit': 45  # requests per minute
            },
            'ipinfo': {
                'url': "https://ipinfo.io",
                'accuracy': 'medium',
                'rate_limit': 50
            },
            'ipgeolocation': {
                'url': "https://api.ipgeolocation.io/ipgeo",
                'accuracy': 'high',
                'rate_limit': 100
            }
        }
        
        # Geocoding providers
        self.geocoding_providers = {
            'openweathermap': {
                'direct': "http://api.openweathermap.org/geo/1.0/direct",
                'reverse': "http://api.openweathermap.org/geo/1.0/reverse",
                'accuracy': 'high',
                'rate_limit': 60
            },
            'nominatim': {
                'search': "https://nominatim.openstreetmap.org/search",
                'reverse': "https://nominatim.openstreetmap.org/reverse",
                'accuracy': 'high',
                'rate_limit': 60
            }
        }
        
        # Advanced caching system
        self.cache = {}
        self.cache_duration = {
            'ip_location': 3600,    # 1 hour for IP location
            'geocoding': 86400,     # 24 hours for geocoding
            'reverse_geocoding': 86400,  # 24 hours for reverse geocoding
            'timezone': 604800      # 1 week for timezone
        }
        
        # Location accuracy and confidence system
        self.accuracy_levels = {
            'gps': {'confidence': 0.95, 'radius': 10},
            'wifi': {'confidence': 0.85, 'radius': 100},
            'cell': {'confidence': 0.75, 'radius': 1000},
            'ip': {'confidence': 0.60, 'radius': 10000},
            'manual': {'confidence': 0.90, 'radius': 100}
        }
        
        # Enhanced coordinate validation
        self.coordinate_patterns = [
            r'^(-?\d+\.?\d*),\s*(-?\d+\.?\d*)$',  # lat,lon
            r'^(-?\d+\.?\d*)\s+(-?\d+\.?\d*)$',   # lat lon
            r'^\((-?\d+\.?\d*),\s*(-?\d+\.?\d*)\)$',  # (lat,lon)
            r'^(-?\d+\.?\d*)[,\s]+(-?\d+\.?\d*)$',  # flexible separator
            r'^lat:\s*(-?\d+\.?\d*)[,\s]+lon:\s*(-?\d+\.?\d*)$',  # labeled
            r'^(-?\d+\.?\d*)°?\s*[NS][,\s]+(-?\d+\.?\d*)°?\s*[EW]$'  # with cardinal directions
        ]
        
        # Location intelligence features
        self.location_intelligence = {
            'population_data': {},
            'timezone_cache': {},
            'administrative_boundaries': {},
            'points_of_interest': {}
        }
        
        # Performance analytics
        self.performance_metrics = {
            'detection_attempts': 0,
            'successful_detections': 0,
            'failed_detections': 0,
            'average_detection_time': 0,
            'provider_success_rates': {},
            'accuracy_scores': []
        }
    
    def get_location_with_ai_enhancement(self, method: str = 'auto') -> Optional[Dict]:
        """AI-enhanced location detection with multiple fallbacks and confidence scoring"""
        
        start_time = time.time()
        self.performance_metrics['detection_attempts'] += 1
        
        location_candidates = []
        
        if method in ['auto', 'ip']:
            # Try multiple IP-based providers
            for provider_name, provider_config in self.primary_providers.items():
                try:
                    location = self._get_location_from_provider(provider_name, provider_config)
                    if location:
                        location['provider'] = provider_name
                        location['detection_method'] = 'ip_geolocation'
                        location_candidates.append(location)
                except Exception as e:
                    st.warning(f"Provider {provider_name} failed: {str(e)}")
        
        if method in ['auto', 'browser']:
            # Browser geolocation API (if available)
            browser_location = self._try_browser_geolocation()
            if browser_location:
                location_candidates.append(browser_location)
        
        # AI-powered location selection and validation
        best_location = self._select_best_location_ai(location_candidates)
        
        if best_location:
            # Enhance with additional intelligence
            enhanced_location = self._enhance_location_with_ai(best_location)
            
            # Update performance metrics
            detection_time = time.time() - start_time
            self.performance_metrics['successful_detections'] += 1
            self.performance_metrics['average_detection_time'] = (
                (self.performance_metrics['average_detection_time'] * (self.performance_metrics['successful_detections'] - 1) + detection_time) /
                self.performance_metrics['successful_detections']
            )
            
            # Cache the result
            cache_key = self._get_cache_key('auto_location', 'default')
            self._cache_result(cache_key, enhanced_location, 'ip_location')
            
            return enhanced_location
        else:
            self.performance_metrics['failed_detections'] += 1
            return None
    
    def _get_location_from_provider(self, provider_name: str, provider_config: Dict) -> Optional[Dict]:
        """Get location from specific provider with enhanced error handling"""
        
        if provider_name == 'ip_api':
            return self._get_location_ip_api_enhanced(provider_config)
        elif provider_name == 'ipinfo':
            return self._get_location_ipinfo_enhanced(provider_config)
        elif provider_name == 'ipgeolocation':
            return self._get_location_ipgeolocation_enhanced(provider_config)
        
        return None
    
    def _get_location_ip_api_enhanced(self, config: Dict) -> Optional[Dict]:
        """Enhanced IP-API location detection"""
        try:
            url = f"{config['url']}?fields={config['fields']}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    
                    # Calculate confidence based on available data
                    confidence = self._calculate_ip_location_confidence(data)
                    
                    # Detect connection type for accuracy estimation
                    connection_type = self._detect_connection_type(data)
                    
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
                        'organization': data.get('org', ''),
                        'as_number': data.get('as', ''),
                        'is_mobile': data.get('mobile', False),
                        'is_proxy': data.get('proxy', False),
                        'is_hosting': data.get('hosting', False),
                        'accuracy': config['accuracy'],
                        'confidence_score': confidence,
                        'connection_type': connection_type,
                        'source': 'ip-api.com',
                        'detection_method': 'IP Geolocation Enhanced'
                    }
            return None
            
        except Exception:
            return None
    
    def _calculate_ip_location_confidence(self, data: Dict) -> float:
        """Calculate confidence score for IP-based location"""
        confidence = 0.5  # base confidence
        
        # City availability increases confidence
        if data.get('city') and data['city'] != 'Unknown':
            confidence += 0.2
        
        # ISP information availability
        if data.get('isp'):
            confidence += 0.1
        
        # Timezone consistency
        if data.get('timezone'):
            confidence += 0.1
        
        # Mobile connections are generally less accurate
        if data.get('mobile', False):
            confidence -= 0.1
        
        # Proxy/VPN detection reduces confidence
        if data.get('proxy', False) or data.get('hosting', False):
            confidence -= 0.2
        
        # Organization data suggests business location (more stable)
        if data.get('org'):
            confidence += 0.05
        
        return max(0.1, min(1.0, confidence))
    
    def _detect_connection_type(self, data: Dict) -> str:
        """Detect connection type for accuracy estimation"""
        if data.get('mobile', False):
            return 'mobile'
        elif data.get('proxy', False):
            return 'proxy'
        elif data.get('hosting', False):
            return 'datacenter'
        elif 'university' in data.get('org', '').lower() or 'college' in data.get('org', '').lower():
            return 'institutional'
        elif 'cable' in data.get('isp', '').lower() or 'fiber' in data.get('isp', '').lower():
            return 'broadband'
        else:
            return 'unknown'
    
    def _try_browser_geolocation(self) -> Optional[Dict]:
        """Attempt to use browser geolocation API"""
        # This would typically be implemented with JavaScript
        # For now, we'll return None as this requires browser integration
        return None
    
    def _select_best_location_ai(self, candidates: List[Dict]) -> Optional[Dict]:
        """AI-powered selection of the best location from candidates"""
        if not candidates:
            return None
        
        if len(candidates) == 1:
            return candidates[0]
        
        # Score each candidate
        scored_candidates = []
        
        for candidate in candidates:
            score = self._calculate_location_score(candidate)
            scored_candidates.append((score, candidate))
        
        # Sort by score (highest first)
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        
        # Check for consensus among top candidates
        best_score, best_candidate = scored_candidates[0]
        
        # If multiple candidates are close in score, check for geographic consensus
        if len(scored_candidates) > 1:
            second_score = scored_candidates[1][0]
            if abs(best_score - second_score) < 0.1:
                consensus_location = self._find_geographic_consensus(candidates)
                if consensus_location:
                    return consensus_location
        
        return best_candidate
    
    def _calculate_location_score(self, location: Dict) -> float:
        """Calculate comprehensive score for location candidate"""
        score = 0.0
        
        # Base confidence score
        score += location.get('confidence_score', 0.5) * 40
        
        # Provider reliability bonus
        provider_bonuses = {
            'ip-api.com': 20,
            'ipinfo.io': 18,
            'ipgeolocation.io': 22,
            'browser_geolocation': 25
        }
        score += provider_bonuses.get(location.get('source', ''), 10)
        
        # Data completeness bonus
        data_fields = ['city', 'region', 'country', 'timezone', 'isp']
        complete_fields = sum(1 for field in data_fields if location.get(field))
        score += (complete_fields / len(data_fields)) * 20
        
        # Connection type penalty/bonus
        connection_penalties = {
            'proxy': -15,
            'datacenter': -10,
            'mobile': -5,
            'broadband': 5,
            'institutional': 3
        }
        score += connection_penalties.get(location.get('connection_type', ''), 0)
        
        # Geographic validity check
        lat, lon = location.get('lat', 0), location.get('lon', 0)
        if self._is_valid_geographic_location(lat, lon):
            score += 10
        else:
            score -= 20
        
        return max(0, min(100, score))
    
    def _is_valid_geographic_location(self, lat: float, lon: float) -> bool:
        """Validate if coordinates represent a plausible location"""
        # Basic coordinate range check
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return False
        
        # Check for obviously invalid locations
        invalid_locations = [
            (0, 0),  # Null Island
        ]
        
        for invalid_lat, invalid_lon in invalid_locations:
            if abs(lat - invalid_lat) < 0.1 and abs(lon - invalid_lon) < 0.1:
                return False
        
        # Check if location is in ocean (simplified check)
        # This would ideally use a proper land/sea dataset
        if abs(lat) > 80:  # Arctic/Antarctic regions
            return lat != 0  # Exclude exact poles unless specifically valid
        
        return True
    
    def _find_geographic_consensus(self, candidates: List[Dict]) -> Optional[Dict]:
        """Find geographic consensus among location candidates"""
        if len(candidates) < 2:
            return None
        
        # Calculate centroid of all candidates
        lats = [c.get('lat', 0) for c in candidates]
        lons = [c.get('lon', 0) for c in candidates]
        
        centroid_lat = sum(lats) / len(lats)
        centroid_lon = sum(lons) / len(lons)
        
        # Find candidate closest to centroid
        best_candidate = None
        min_distance = float('inf')
        
        for candidate in candidates:
            distance = geodesic((centroid_lat, centroid_lon), 
                              (candidate.get('lat', 0), candidate.get('lon', 0))).kilometers
            
            if distance < min_distance:
                min_distance = distance
                best_candidate = candidate
        
        # Add consensus metadata
        if best_candidate:
            best_candidate['consensus_metadata'] = {
                'num_candidates': len(candidates),
                'centroid_distance_km': min_distance,
                'consensus_confidence': 1.0 - (min_distance / 100)  # Normalize distance to confidence
            }
        
        return best_candidate
    
    def _enhance_location_with_ai(self, location: Dict) -> Dict:
        """Enhance location with AI-powered additional data"""
        enhanced = location.copy()
        
        # Add timestamp and detection metadata
        enhanced['detected_at'] = datetime.now(timezone.utc).isoformat()
        enhanced['detection_session_id'] = hashlib.md5(
            f"{enhanced['lat']}{enhanced['lon']}{time.time()}".encode()
        ).hexdigest()[:8]
        
        # Calculate precision radius
        enhanced['precision_radius_m'] = self._estimate_precision_radius(location)
        
        # Add timezone intelligence
        timezone_data = self._get_enhanced_timezone_data(location['lat'], location['lon'])
        if timezone_data:
            enhanced.update(timezone_data)
        
        # Add administrative boundaries
        admin_data = self._get_administrative_boundaries(location['lat'], location['lon'])
        if admin_data:
            enhanced['administrative'] = admin_data
        
        # Calculate location quality score
        enhanced['location_quality_score'] = self._calculate_location_quality_score(enhanced)
        
        # Add nearest major city reference
        nearest_city = self._find_nearest_major_city(location['lat'], location['lon'])
        if nearest_city:
            enhanced['nearest_major_city'] = nearest_city
        
        return enhanced
    
    def _estimate_precision_radius(self, location: Dict) -> float:
        """Estimate precision radius in meters"""
        connection_type = location.get('connection_type', 'unknown')
        confidence = location.get('confidence_score', 0.5)
        
        # Base radius by connection type
        base_radius = {
            'broadband': 1000,
            'mobile': 5000,
            'institutional': 500,
            'datacenter': 10000,
            'proxy': 50000,
            'unknown': 10000
        }.get(connection_type, 10000)
        
        # Adjust by confidence
        adjusted_radius = base_radius * (2 - confidence)
        
        return max(100, min(100000, adjusted_radius))
    
    def _get_enhanced_timezone_data(self, lat: float, lon: float) -> Optional[Dict]:
        """Get enhanced timezone data with DST information"""
        cache_key = self._get_cache_key('timezone', f"{lat:.4f},{lon:.4f}")
        
        # Check cache
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key], 'timezone'):
            return self.cache[cache_key]['data']
        
        try:
            # Use a timezone API (example with WorldTimeAPI)
            url = f"http://worldtimeapi.org/api/timezone"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                timezones = response.json()
                
                # Find closest timezone (simplified)
                # In production, you'd use a proper timezone boundary dataset
                timezone_name = self._find_closest_timezone(lat, lon, timezones)
                
                if timezone_name:
                    # Get detailed timezone info
                    tz_url = f"http://worldtimeapi.org/api/timezone/{timezone_name}"
                    tz_response = requests.get(tz_url, timeout=5)
                    
                    if tz_response.status_code == 200:
                        tz_data = tz_response.json()
                        
                        timezone_info = {
                            'timezone_name': tz_data.get('timezone'),
                            'utc_offset': tz_data.get('utc_offset'),
                            'dst_active': tz_data.get('dst', False),
                            'dst_from': tz_data.get('dst_from'),
                            'dst_until': tz_data.get('dst_until'),
                            'local_time': tz_data.get('datetime'),
                            'week_number': tz_data.get('week_number')
                        }
                        
                        # Cache the result
                        self._cache_result(cache_key, timezone_info, 'timezone')
                        return timezone_info
            
        except Exception:
            pass
        
        # Fallback to simple UTC offset calculation
        utc_offset_hours = round(lon / 15)
        return {
            'timezone_name': f"UTC{'+' if utc_offset_hours >= 0 else ''}{utc_offset_hours}",
            'utc_offset': f"{'+' if utc_offset_hours >= 0 else ''}{utc_offset_hours:02d}:00",
            'dst_active': False,
            'estimated': True
        }
    
    def _find_closest_timezone(self, lat: float, lon: float, timezones: List[str]) -> str:
        """Find closest timezone (simplified implementation)"""
        # This is a simplified implementation
        # In production, you'd use proper timezone boundary data
        
        # Basic regional mapping
        if -180 <= lon < -120:
            return "America/Los_Angeles"
        elif -120 <= lon < -75:
            return "America/Denver"
        elif -75 <= lon < -45:
            return "America/New_York"
        elif -15 <= lon < 45:
            return "Europe/London"
        elif 45 <= lon < 90:
            return "Asia/Kolkata"
        elif 90 <= lon < 135:
            return "Asia/Shanghai"
        elif 135 <= lon <= 180:
            return "Asia/Tokyo"
        else:
            return "UTC"
    
    def search_location_advanced(self, query: str, limit: int = 10) -> List[Dict]:
        """Advanced location search with AI-powered ranking and filtering"""
        cache_key = self._get_cache_key('search_advanced', f"{query.lower().strip()}_{limit}")
        
        # Check cache
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key], 'geocoding'):
            return self.cache[cache_key]['data']
        
        # Parse query to detect different input types
        query_type = self._analyze_search_query(query)
        
        results = []
        
        if query_type['type'] == 'coordinates':
            # Handle coordinate input
            coords = self._parse_coordinates_advanced(query)
            if coords:
                location_data = self._handle_coordinate_search_advanced(coords[0], coords[1])
                if location_data:
                    results = [location_data]
        else:
            # Handle location name search
            results = self._search_by_name_advanced(query, limit)
        
        # AI-powered result ranking and enhancement
        enhanced_results = self._enhance_search_results(results, query)
        
        # Cache results
        self._cache_result(cache_key, enhanced_results, 'geocoding')
        
        return enhanced_results
    
    def _analyze_search_query(self, query: str) -> Dict[str, Any]:
        """Analyze search query to determine input type and characteristics"""
        query_lower = query.lower().strip()
        
        analysis = {
            'type': 'location_name',
            'characteristics': [],
            'confidence': 0.8
        }
        
        # Check for coordinate patterns
        for pattern in self.coordinate_patterns:
            if re.match(pattern, query_lower):
                analysis['type'] = 'coordinates'
                analysis['confidence'] = 0.95
                return analysis
        
        # Check for postal codes
        postal_patterns = [
            r'^\d{5}(-\d{4})?$',  # US ZIP
            r'^[A-Z]\d[A-Z] \d[A-Z]\d$',  # Canadian postal
            r'^\d{4,5}$',  # European postal
        ]
        
        for pattern in postal_patterns:
            if re.match(pattern, query.upper()):
                analysis['type'] = 'postal_code'
                analysis['characteristics'].append('postal_code')
                analysis['confidence'] = 0.9
                break
        
        # Check for airport codes
        if len(query) == 3 and query.isalpha():
            analysis['characteristics'].append('possible_airport_code')
            analysis['confidence'] = 0.7
        
        # Check for well-known location patterns
        if ',' in query:
            parts = [part.strip() for part in query.split(',')]
            if len(parts) == 2:
                analysis['characteristics'].append('city_country_format')
                analysis['confidence'] = 0.85
        
        return analysis
    
    def _parse_coordinates_advanced(self, query: str) -> Optional[Tuple[float, float]]:
        """Advanced coordinate parsing with support for multiple formats"""
        query = query.strip()
        
        for pattern in self.coordinate_patterns:
            match = re.match(pattern, query, re.IGNORECASE)
            if match:
                try:
                    groups = match.groups()
                    if len(groups) >= 2:
                        lat_str, lon_str = groups[0], groups[1]
                        
                        # Handle cardinal directions
                        if query.upper().endswith('N') or query.upper().endswith('S'):
                            if query.upper().endswith('S'):
                                lat_str = '-' + lat_str.lstrip('-')
                        if query.upper().endswith('W'):
                            lon_str = '-' + lon_str.lstrip('-')
                        
                        lat, lon = float(lat_str), float(lon_str)
                        
                        if self.validate_coordinates_advanced(lat, lon):
                            return lat, lon
                            
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def validate_coordinates_advanced(self, lat: float, lon: float) -> bool:
        """Advanced coordinate validation with detailed feedback"""
        try:
            # Basic range validation
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                return False
            
            # Check for common invalid coordinates
            invalid_coords = [
                (0, 0),      # Null Island
                (90, 0),     # North Pole (suspicious for user input)
                (-90, 0),    # South Pole (suspicious for user input)
            ]
            
            for invalid_lat, invalid_lon in invalid_coords:
                if abs(lat - invalid_lat) < 0.001 and abs(lon - invalid_lon) < 0.001:
                    st.warning(f"⚠️ Coordinates ({lat}, {lon}) point to an unusual location")
                    return True  # Still valid, just unusual
            
            # Check precision (too many decimal places might indicate error)
            lat_str, lon_str = str(lat), str(lon)
            lat_decimals = len(lat_str.split('.')[-1]) if '.' in lat_str else 0
            lon_decimals = len(lon_str.split('.')[-1]) if '.' in lon_str else 0
            
            if lat_decimals > 6 or lon_decimals > 6:
                st.info("ℹ️ Very precise coordinates detected - accuracy may exceed typical GPS precision")
            
            return True
            
        except (TypeError, ValueError):
            return False
    
    def get_location_analytics(self) -> Dict[str, Any]:
        """Comprehensive location detection analytics"""
        total_attempts = self.performance_metrics['detection_attempts']
        
        if total_attempts == 0:
            return {'status': 'no_data', 'message': 'No location detection attempts recorded'}
        
        success_rate = (self.performance_metrics['successful_detections'] / total_attempts) * 100
        
        # Provider success rates
        provider_stats = {}
        for provider in self.primary_providers.keys():
            provider_stats[provider] = self.performance_metrics['provider_success_rates'].get(provider, {
                'attempts': 0,
                'successes': 0,
                'success_rate': 0
            })
        
        # Cache statistics
        cache_stats = {
            'total_entries': len(self.cache),
            'cache_types': list(self.cache_duration.keys()),
            'average_cache_age': self._calculate_average_cache_age(),
            'cache_hit_rate': self._calculate_cache_hit_rate()
        }
        
        # Accuracy distribution
        accuracy_distribution = {}
        if self.performance_metrics['accuracy_scores']:
            scores = self.performance_metrics['accuracy_scores']
            accuracy_distribution = {
                'mean': np.mean(scores),
                'median': np.median(scores),
                'std': np.std(scores),
                'min': np.min(scores),
                'max': np.max(scores)
            }
        
        return {
            'performance': {
                'total_attempts': total_attempts,
                'successful_detections': self.performance_metrics['successful_detections'],
                'failed_detections': self.performance_metrics['failed_detections'],
                'success_rate': success_rate,
                'average_detection_time': self.performance_metrics['average_detection_time']
            },
            'providers': provider_stats,
            'cache': cache_stats,
            'accuracy': accuracy_distribution,
            'recommendations': self._generate_performance_recommendations(success_rate, provider_stats)
        }
    
    def _generate_performance_recommendations(self, success_rate: float, 
                                           provider_stats: Dict) -> List[str]:
        """Generate recommendations for improving location detection performance"""
        recommendations = []
        
        if success_rate < 80:
            recommendations.append("Consider adding more location providers for better reliability")
        
        # Check individual provider performance
        for provider, stats in provider_stats.items():
            if stats['success_rate'] < 70 and stats['attempts'] > 5:
                recommendations.append(f"Provider {provider} has low success rate - consider debugging or replacement")
        
        if self._calculate_cache_hit_rate() < 30:
            recommendations.append("Increase cache duration to improve performance")
        
        if self.performance_metrics['average_detection_time'] > 3:
            recommendations.append("Detection time is high - consider optimizing provider timeouts")
        
        return recommendations
    
    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        # This would need to be tracked during actual cache usage
        # For now, return a placeholder
        return 0.0
    
    def _calculate_average_cache_age(self) -> float:
        """Calculate average age of cache entries"""
        if not self.cache:
            return 0.0
        
        current_time = time.time()
        ages = [current_time - entry['timestamp'] for entry in self.cache.values()]
        return sum(ages) / len(ages)
    
    def _get_cache_key(self, method: str, params: str) -> str:
        """Generate cache key for location requests"""
        return hashlib.md5(f"{method}:{params}".encode()).hexdigest()
    
    def _is_cache_valid(self, cache_entry: Dict, cache_type: str) -> bool:
        """Check if cache entry is still valid"""
        duration = self.cache_duration.get(cache_type, 3600)
        return (time.time() - cache_entry['timestamp']) < duration
    
    def _cache_result(self, key: str, data: Dict, cache_type: str):
        """Cache the result with timestamp and metadata"""
        self.cache[key] = {
            'data': data,
            'timestamp': time.time(),
            'cache_type': cache_type,
            'access_count': 0
        }
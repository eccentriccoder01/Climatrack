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
        # Add other providers here if implemented
        
        return None
    
    def _get_location_ip_api_enhanced(self, config: Dict) -> Optional[Dict]:
        """Enhanced IP-API location detection"""
        try:
            url = f"{config['url']}?fields={config['fields']}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    confidence = self._calculate_ip_location_confidence(data)
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
        confidence = 0.5
        if data.get('city') and data['city'] != 'Unknown':
            confidence += 0.2
        if data.get('isp'):
            confidence += 0.1
        if data.get('timezone'):
            confidence += 0.1
        if data.get('mobile', False):
            confidence -= 0.1
        if data.get('proxy', False) or data.get('hosting', False):
            confidence -= 0.2
        if data.get('org'):
            confidence += 0.05
        return max(0.1, min(1.0, confidence))
    
    def _detect_connection_type(self, data: Dict) -> str:
        """Detect connection type for accuracy estimation"""
        if data.get('mobile', False): return 'mobile'
        if data.get('proxy', False): return 'proxy'
        if data.get('hosting', False): return 'datacenter'
        if 'university' in data.get('org', '').lower() or 'college' in data.get('org', '').lower(): return 'institutional'
        if 'cable' in data.get('isp', '').lower() or 'fiber' in data.get('isp', '').lower(): return 'broadband'
        return 'unknown'
    
    def _try_browser_geolocation(self) -> Optional[Dict]:
        return None
    
    def _select_best_location_ai(self, candidates: List[Dict]) -> Optional[Dict]:
        """AI-powered selection of the best location from candidates"""
        if not candidates:
            return None
        if len(candidates) == 1:
            return candidates[0]
        scored_candidates = sorted([(self._calculate_location_score(c), c) for c in candidates], reverse=True)
        return scored_candidates[0][1]

    def _calculate_location_score(self, location: Dict) -> float:
        score = location.get('confidence_score', 0.5) * 40
        data_fields = ['city', 'region', 'country', 'timezone', 'isp']
        complete_fields = sum(1 for field in data_fields if location.get(field))
        score += (complete_fields / len(data_fields)) * 20
        return max(0, min(100, score))

    def _is_valid_geographic_location(self, lat: float, lon: float) -> bool:
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return False
        if abs(lat) < 0.1 and abs(lon) < 0.1: # Null Island check
            return False
        return True
    
    def _enhance_location_with_ai(self, location: Dict) -> Dict:
        """Enhance location with AI-powered additional data"""
        enhanced = location.copy()
        enhanced['detected_at'] = datetime.now(timezone.utc).isoformat()
        enhanced['precision_radius_m'] = self._estimate_precision_radius(location)
        return enhanced
    
    def _estimate_precision_radius(self, location: Dict) -> float:
        """Estimate precision radius in meters"""
        connection_type = location.get('connection_type', 'unknown')
        confidence = location.get('confidence_score', 0.5)
        base_radius = {'broadband': 1000, 'mobile': 5000, 'datacenter': 10000, 'proxy': 50000}.get(connection_type, 10000)
        return max(100, base_radius * (2 - confidence))

    def search_location_advanced(self, query: str, limit: int = 10) -> List[Dict]:
        """Advanced location search with AI-powered ranking and filtering"""
        cache_key = self._get_cache_key('search_advanced', f"{query.lower().strip()}_{limit}")
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key], 'geocoding'):
            return self.cache[cache_key]['data']
        
        results = self._search_by_name_advanced(query, limit)
        self._cache_result(cache_key, results, 'geocoding')
        return results

    def _search_by_name_advanced(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for a location by name using Nominatim as a provider."""
        try:
            url = self.geocoding_providers['nominatim']['search']
            params = {'q': query, 'format': 'json', 'limit': limit}
            response = requests.get(url, params=params, headers={'User-Agent': 'ClimaTrackApp/1.0'})
            if response.status_code == 200:
                results = response.json()
                return [{
                    'lat': float(res.get('lat', 0)),
                    'lon': float(res.get('lon', 0)),
                    'display_name': res.get('display_name', 'Unknown'),
                    'city': res.get('name', ''),
                    'country': res.get('display_name', '').split(',')[-1].strip()
                } for res in results]
        except Exception as e:
            st.error(f"Geocoding search failed: {e}")
        return []

    def _get_cache_key(self, method: str, params: str) -> str:
        """Generate cache key for location requests"""
        return hashlib.md5(f"{method}:{params}".encode()).hexdigest()
    
    def _is_cache_valid(self, cache_entry: Dict, cache_type: str) -> bool:
        """Check if cache entry is still valid"""
        duration = self.cache_duration.get(cache_type, 3600)
        return (time.time() - cache_entry['timestamp']) < duration
    
    def _cache_result(self, key: str, data: Any, cache_type: str):
        """Cache the result with timestamp and metadata"""
        self.cache[key] = {
            'data': data,
            'timestamp': time.time(),
            'cache_type': cache_type
        }
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import json
import math
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class AdvancedDataProcessor:
    """Advanced weather data processor with AI-powered analytics and machine learning insights"""
    
    def __init__(self):
        # Enhanced units and conversions
        self.temperature_units = {
            'metric': {'symbol': '°C', 'name': 'Celsius'},
            'imperial': {'symbol': '°F', 'name': 'Fahrenheit'},
            'kelvin': {'symbol': 'K', 'name': 'Kelvin'}
        }
        
        self.speed_units = {
            'metric': {'symbol': 'm/s', 'name': 'Meters per second'},
            'imperial': {'symbol': 'mph', 'name': 'Miles per hour'},
            'kelvin': {'symbol': 'm/s', 'name': 'Meters per second'}
        }
        
        # Advanced weather pattern recognition
        self.weather_patterns = {
            'heat_wave': {
                'temp_threshold': 35,
                'duration': 3,
                'severity_levels': {
                    'moderate': {'temp': 35, 'duration': 3},
                    'severe': {'temp': 40, 'duration': 2},
                    'extreme': {'temp': 45, 'duration': 1}
                }
            },
            'cold_snap': {
                'temp_threshold': -5,
                'duration': 2,
                'severity_levels': {
                    'moderate': {'temp': -5, 'duration': 2},
                    'severe': {'temp': -15, 'duration': 1},
                    'extreme': {'temp': -25, 'duration': 1}
                }
            },
            'drought': {
                'humidity_threshold': 30,
                'duration': 7,
                'precipitation_threshold': 0.1
            },
            'storm_system': {
                'wind_threshold': 15,
                'pressure_drop': 10,
                'precipitation_threshold': 5
            }
        }
        
        # AI model configurations
        self.comfort_model_weights = {
            'temperature': 0.4,
            'humidity': 0.25,
            'wind': 0.2,
            'pressure': 0.1,
            'uv_index': 0.05
        }
        
        # Seasonal adjustments
        self.seasonal_factors = {
            'spring': {'temp_comfort_range': (15, 25), 'humidity_optimal': 50},
            'summer': {'temp_comfort_range': (20, 28), 'humidity_optimal': 45},
            'autumn': {'temp_comfort_range': (12, 22), 'humidity_optimal': 55},
            'winter': {'temp_comfort_range': (18, 24), 'humidity_optimal': 40}
        }
        
    def process_forecast_data_advanced(self, forecast_data: Dict, units: str = 'metric') -> List[Dict]:
        """Advanced forecast processing with machine learning insights"""
        if not forecast_data or 'list' not in forecast_data:
            return []
        
        daily_data = {}
        hourly_patterns = []
        
        # Group by day and analyze patterns
        for item in forecast_data['list']:
            dt = datetime.fromtimestamp(item['dt'])
            date_key = dt.strftime('%Y-%m-%d')
            
            if date_key not in daily_data:
                daily_data[date_key] = {
                    'date': dt,
                    'day': dt.strftime('%A'),
                    'temps': [],
                    'humidity': [],
                    'wind_speed': [],
                    'wind_direction': [],
                    'pressure': [],
                    'weather_conditions': [],
                    'icons': [],
                    'descriptions': [],
                    'precipitation': [],
                    'clouds': [],
                    'uv_index': [],
                    'visibility': []
                }
            
            # Collect hourly data for pattern analysis
            hourly_patterns.append({
                'datetime': dt,
                'temp': item['main']['temp'],
                'humidity': item['main']['humidity'],
                'wind_speed': item['wind']['speed'],
                'pressure': item['main']['pressure'],
                'condition': item['weather'][0]['main']
            })
            
            # Aggregate daily data
            daily_data[date_key]['temps'].append(item['main']['temp'])
            daily_data[date_key]['humidity'].append(item['main']['humidity'])
            daily_data[date_key]['wind_speed'].append(item['wind']['speed'])
            daily_data[date_key]['wind_direction'].append(item['wind'].get('deg', 0))
            daily_data[date_key]['pressure'].append(item['main']['pressure'])
            daily_data[date_key]['weather_conditions'].append(item['weather'][0]['main'])
            daily_data[date_key]['icons'].append(item['weather'][0]['icon'])
            daily_data[date_key]['descriptions'].append(item['weather'][0]['description'])
            daily_data[date_key]['precipitation'].append(item.get('pop', 0) * 100)
            daily_data[date_key]['clouds'].append(item['clouds']['all'])
            daily_data[date_key]['visibility'].append(item.get('visibility', 10000))
            
            # Calculate UV index based on conditions
            uv_estimate = self._estimate_uv_index(
                item['weather'][0]['main'],
                item['clouds']['all'],
                dt.hour
            )
            daily_data[date_key]['uv_index'].append(uv_estimate)
        
        # Process daily summaries with advanced analytics
        processed_forecast = []
        for date_key, data in daily_data.items():
            # Advanced statistical analysis
            temp_stats = self._calculate_temperature_statistics(data['temps'])
            humidity_stats = self._calculate_statistical_measures(data['humidity'])
            wind_stats = self._calculate_wind_statistics(data['wind_speed'], data['wind_direction'])
            pressure_stats = self._calculate_pressure_analysis(data['pressure'])
            
            # Weather condition analysis
            condition_analysis = self._analyze_weather_conditions(data['weather_conditions'])
            
            # Comfort and health indices
            comfort_analysis = self._calculate_advanced_comfort_index(data)
            health_index = self._calculate_health_weather_index(data)
            
            # Pattern recognition
            weather_patterns = self._detect_weather_patterns_daily(data)
            
            # Activity recommendations
            activity_score = self._calculate_activity_suitability(data)
            
            processed_day = {
                # Basic information
                'date': data['date'],
                'day': data['day'][:3],
                'day_full': data['day'],
                
                # Temperature analysis
                'temp_max': temp_stats['max'],
                'temp_min': temp_stats['min'],
                'temp_avg': temp_stats['mean'],
                'temp_median': temp_stats['median'],
                'temp_range': temp_stats['range'],
                'temp_variance': temp_stats['variance'],
                'temp_trend': temp_stats['trend'],
                
                # Humidity analysis
                'humidity': humidity_stats['mean'],
                'humidity_range': humidity_stats['range'],
                'humidity_stability': humidity_stats['stability'],
                
                # Wind analysis
                'wind_speed': wind_stats['avg_speed'],
                'wind_max': wind_stats['max_speed'],
                'wind_consistency': wind_stats['consistency'],
                'wind_direction_avg': wind_stats['avg_direction'],
                'wind_direction_stability': wind_stats['direction_stability'],
                
                # Atmospheric pressure
                'pressure_avg': pressure_stats['mean'],
                'pressure_trend': pressure_stats['trend'],
                'pressure_stability': pressure_stats['stability'],
                
                # Weather conditions
                'condition': condition_analysis['primary_condition'],
                'icon': condition_analysis['primary_icon'],
                'description': condition_analysis['primary_description'],
                'condition_confidence': condition_analysis['confidence'],
                'condition_diversity': condition_analysis['diversity'],
                
                # Precipitation and clouds
                'precipitation_chance': max(data['precipitation']),
                'precipitation_avg': sum(data['precipitation']) / len(data['precipitation']),
                'cloud_coverage': sum(data['clouds']) / len(data['clouds']),
                'cloud_variance': np.var(data['clouds']),
                
                # UV and visibility
                'uv_index_max': max(data['uv_index']),
                'uv_index_avg': sum(data['uv_index']) / len(data['uv_index']),
                'visibility_avg': sum(data['visibility']) / len(data['visibility']),
                
                # Advanced indices
                'comfort_score': comfort_analysis['score'],
                'comfort_level': comfort_analysis['level'],
                'comfort_factors': comfort_analysis['factors'],
                'health_index': health_index['score'],
                'health_concerns': health_index['concerns'],
                'activity_score': activity_score['overall'],
                'activity_recommendations': activity_score['recommendations'],
                
                # Pattern analysis
                'weather_patterns': weather_patterns,
                'stability_index': self._calculate_day_stability(data),
                'extremes_risk': self._assess_extreme_weather_risk(data),
                
                # Derived insights
                'best_time_periods': self._find_optimal_time_periods(hourly_patterns, data['date']),
                'weather_quality_score': self._calculate_overall_weather_quality(data)
            }
            
            processed_forecast.append(processed_day)
        
        return sorted(processed_forecast, key=lambda x: x['date'])[:7]  # Extended to 7 days
    
    def _calculate_temperature_statistics(self, temps: List[float]) -> Dict[str, float]:
        """Calculate comprehensive temperature statistics"""
        if not temps:
            return {'max': 0, 'min': 0, 'mean': 0, 'median': 0, 'range': 0, 'variance': 0, 'trend': 'stable'}
        
        temps_array = np.array(temps)
        
        # Basic statistics
        stats_dict = {
            'max': float(np.max(temps_array)),
            'min': float(np.min(temps_array)),
            'mean': float(np.mean(temps_array)),
            'median': float(np.median(temps_array)),
            'range': float(np.ptp(temps_array)),
            'variance': float(np.var(temps_array)),
            'std': float(np.std(temps_array))
        }
        
        # Trend analysis
        if len(temps) > 2:
            x = np.arange(len(temps))
            slope, _, r_value, _, _ = stats.linregress(x, temps)
            
            if abs(r_value) > 0.5:  # Significant correlation
                if slope > 0.5:
                    stats_dict['trend'] = 'increasing'
                elif slope < -0.5:
                    stats_dict['trend'] = 'decreasing'
                else:
                    stats_dict['trend'] = 'stable'
            else:
                stats_dict['trend'] = 'variable'
        else:
            stats_dict['trend'] = 'stable'
        
        return stats_dict
    
    def _calculate_statistical_measures(self, data: List[float]) -> Dict[str, float]:
        """Calculate advanced statistical measures for any dataset"""
        if not data:
            return {'mean': 0, 'range': 0, 'stability': 0}
        
        data_array = np.array(data)
        
        # Calculate coefficient of variation as stability measure
        mean_val = np.mean(data_array)
        std_val = np.std(data_array)
        cv = (std_val / mean_val) if mean_val != 0 else 0
        stability = max(0, 1 - cv)  # Higher stability = lower coefficient of variation
        
        return {
            'mean': float(mean_val),
            'median': float(np.median(data_array)),
            'range': float(np.ptp(data_array)),
            'std': float(std_val),
            'stability': float(stability),
            'cv': float(cv)
        }
    
    def _calculate_wind_statistics(self, speeds: List[float], directions: List[float]) -> Dict[str, float]:
        """Advanced wind analysis with directional statistics"""
        if not speeds or not directions:
            return {
                'avg_speed': 0, 'max_speed': 0, 'consistency': 0,
                'avg_direction': 0, 'direction_stability': 0
            }
        
        # Speed statistics
        speed_stats = self._calculate_statistical_measures(speeds)
        
        # Directional statistics (circular statistics)
        directions_rad = np.radians(directions)
        
        # Calculate mean direction using circular statistics
        sin_sum = np.sum(np.sin(directions_rad))
        cos_sum = np.sum(np.cos(directions_rad))
        mean_direction = np.degrees(np.arctan2(sin_sum, cos_sum))
        if mean_direction < 0:
            mean_direction += 360
        
        # Calculate directional consistency (R-value)
        n = len(directions)
        R = np.sqrt(sin_sum**2 + cos_sum**2) / n
        direction_stability = R  # R = 1 means all directions same, R = 0 means random
        
        return {
            'avg_speed': speed_stats['mean'],
            'max_speed': float(np.max(speeds)),
            'consistency': speed_stats['stability'],
            'avg_direction': float(mean_direction),
            'direction_stability': float(direction_stability),
            'speed_variance': speed_stats['std']
        }
    
    def _calculate_pressure_analysis(self, pressures: List[float]) -> Dict[str, Any]:
        """Advanced atmospheric pressure analysis"""
        if not pressures:
            return {'mean': 1013, 'trend': 'stable', 'stability': 1}
        
        pressure_stats = self._calculate_statistical_measures(pressures)
        
        # Trend analysis
        if len(pressures) > 2:
            x = np.arange(len(pressures))
            slope, _, r_value, _, _ = stats.linregress(x, pressures)
            
            if abs(r_value) > 0.4:  # Significant correlation for pressure
                if slope > 1:
                    trend = 'rising'
                elif slope < -1:
                    trend = 'falling'
                else:
                    trend = 'stable'
            else:
                trend = 'variable'
        else:
            trend = 'stable'
        
        # Pressure change rate (important for weather prediction)
        pressure_change_rate = 0
        if len(pressures) > 1:
            pressure_change_rate = (pressures[-1] - pressures[0]) / len(pressures)
        
        return {
            'mean': pressure_stats['mean'],
            'trend': trend,
            'stability': pressure_stats['stability'],
            'change_rate': float(pressure_change_rate),
            'range': pressure_stats['range']
        }
    
    def _analyze_weather_conditions(self, conditions: List[str]) -> Dict[str, Any]:
        """Analyze weather condition patterns and confidence"""
        if not conditions:
            return {
                'primary_condition': 'Unknown',
                'primary_icon': '01d',
                'primary_description': 'Unknown',
                'confidence': 0,
                'diversity': 0
            }
        
        # Count occurrences
        condition_counts = {}
        for condition in conditions:
            condition_counts[condition] = condition_counts.get(condition, 0) + 1
        
        # Find primary condition
        primary_condition = max(condition_counts, key=condition_counts.get)
        confidence = condition_counts[primary_condition] / len(conditions)
        diversity = len(condition_counts) / len(conditions)
        
        # Map to icon and description (simplified mapping)
        condition_mapping = {
            'Clear': {'icon': '01d', 'description': 'clear sky'},
            'Clouds': {'icon': '02d', 'description': 'few clouds'},
            'Rain': {'icon': '10d', 'description': 'light rain'},
            'Thunderstorm': {'icon': '11d', 'description': 'thunderstorm'},
            'Snow': {'icon': '13d', 'description': 'snow'},
            'Mist': {'icon': '50d', 'description': 'mist'}
        }
        
        mapping = condition_mapping.get(primary_condition, {'icon': '01d', 'description': 'unknown'})
        
        return {
            'primary_condition': primary_condition,
            'primary_icon': mapping['icon'],
            'primary_description': mapping['description'],
            'confidence': float(confidence),
            'diversity': float(diversity),
            'all_conditions': condition_counts
        }
    
    def _calculate_advanced_comfort_index(self, day_data: Dict) -> Dict[str, Any]:
        """Calculate advanced comfort index with multiple factors"""
        if not day_data['temps']:
            return {'score': 50, 'level': 'Unknown', 'factors': {}}
        
        # Get average values
        avg_temp = sum(day_data['temps']) / len(day_data['temps'])
        avg_humidity = sum(day_data['humidity']) / len(day_data['humidity'])
        avg_wind = sum(day_data['wind_speed']) / len(day_data['wind_speed'])
        avg_pressure = sum(day_data['pressure']) / len(day_data['pressure'])
        
        # Calculate individual comfort factors
        temp_comfort = self._calculate_temperature_comfort(avg_temp)
        humidity_comfort = self._calculate_humidity_comfort(avg_humidity)
        wind_comfort = self._calculate_wind_comfort(avg_wind)
        pressure_comfort = self._calculate_pressure_comfort(avg_pressure)
        
        # Weather condition penalty
        condition_penalty = self._calculate_condition_comfort_penalty(day_data['weather_conditions'])
        
        # Weighted comfort score
        weights = self.comfort_model_weights
        comfort_score = (
            temp_comfort * weights['temperature'] +
            humidity_comfort * weights['humidity'] +
            wind_comfort * weights['wind'] +
            pressure_comfort * weights['pressure']
        ) * 100
        
        # Apply condition penalty
        comfort_score = max(0, comfort_score - condition_penalty)
        
        # Determine comfort level
        comfort_level = self._determine_comfort_level(comfort_score)
        
        return {
            'score': float(comfort_score),
            'level': comfort_level,
            'factors': {
                'temperature': float(temp_comfort * 100),
                'humidity': float(humidity_comfort * 100),
                'wind': float(wind_comfort * 100),
                'pressure': float(pressure_comfort * 100),
                'condition_penalty': float(condition_penalty)
            }
        }
    
    def _calculate_temperature_comfort(self, temp: float) -> float:
        """Calculate temperature comfort factor (0-1)"""
        # Optimal temperature range: 18-24°C
        if 18 <= temp <= 24:
            return 1.0
        elif 15 <= temp <= 27:
            # Gradual decrease in comfort
            if temp < 18:
                return 1.0 - (18 - temp) / 10
            else:
                return 1.0 - (temp - 24) / 10
        else:
            # Significant discomfort
            if temp < 15:
                return max(0, 1.0 - (15 - temp) / 15)
            else:
                return max(0, 1.0 - (temp - 27) / 20)
    
    def _calculate_humidity_comfort(self, humidity: float) -> float:
        """Calculate humidity comfort factor (0-1)"""
        # Optimal humidity: 40-60%
        if 40 <= humidity <= 60:
            return 1.0
        elif 30 <= humidity <= 70:
            if humidity < 40:
                return 1.0 - (40 - humidity) / 20
            else:
                return 1.0 - (humidity - 60) / 20
        else:
            if humidity < 30:
                return max(0, 1.0 - (30 - humidity) / 30)
            else:
                return max(0, 1.0 - (humidity - 70) / 30)
    
    def _calculate_wind_comfort(self, wind_speed: float) -> float:
        """Calculate wind comfort factor (0-1)"""
        # Optimal wind: 1-5 m/s (light breeze)
        if 1 <= wind_speed <= 5:
            return 1.0
        elif wind_speed < 1:
            return 0.8  # Still air is slightly uncomfortable
        elif wind_speed <= 10:
            return 1.0 - (wind_speed - 5) / 10
        else:
            return max(0, 1.0 - (wind_speed - 10) / 15)
    
    def _calculate_pressure_comfort(self, pressure: float) -> float:
        """Calculate pressure comfort factor (0-1)"""
        # Normal pressure: 1010-1020 hPa
        if 1010 <= pressure <= 1020:
            return 1.0
        else:
            deviation = min(abs(pressure - 1015), 50)  # Cap at 50 hPa deviation
            return max(0, 1.0 - deviation / 50)
    
    def _calculate_condition_comfort_penalty(self, conditions: List[str]) -> float:
        """Calculate penalty based on weather conditions"""
        condition_penalties = {
            'Thunderstorm': 30,
            'Snow': 20,
            'Rain': 15,
            'Drizzle': 10,
            'Mist': 5,
            'Fog': 8,
            'Clear': 0,
            'Clouds': 2
        }
        
        if not conditions:
            return 0
        
        # Calculate average penalty
        total_penalty = sum(condition_penalties.get(condition, 5) for condition in conditions)
        return total_penalty / len(conditions)
    
    def _determine_comfort_level(self, score: float) -> str:
        """Determine comfort level based on score"""
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Very Good"
        elif score >= 70:
            return "Good"
        elif score >= 60:
            return "Fair"
        elif score >= 50:
            return "Poor"
        elif score >= 40:
            return "Very Poor"
        else:
            return "Extremely Poor"
    
    def _calculate_health_weather_index(self, day_data: Dict) -> Dict[str, Any]:
        """Calculate health-related weather index"""
        if not day_data['temps']:
            return {'score': 50, 'concerns': []}
        
        health_score = 100
        concerns = []
        
        # Temperature health factors
        avg_temp = sum(day_data['temps']) / len(day_data['temps'])
        temp_range = max(day_data['temps']) - min(day_data['temps'])
        
        if avg_temp > 35:
            health_score -= 30
            concerns.append("Heat exhaustion risk")
        elif avg_temp < -10:
            health_score -= 25
            concerns.append("Hypothermia risk")
        
        if temp_range > 15:
            health_score -= 10
            concerns.append("Large temperature variations")
        
        # Humidity health factors
        avg_humidity = sum(day_data['humidity']) / len(day_data['humidity'])
        if avg_humidity > 80:
            health_score -= 15
            concerns.append("High humidity discomfort")
        elif avg_humidity < 20:
            health_score -= 10
            concerns.append("Very dry air - respiratory irritation possible")
        
        # Wind health factors
        max_wind = max(day_data['wind_speed'])
        if max_wind > 20:
            health_score -= 20
            concerns.append("Strong winds - outdoor activity risk")
        
        # Pressure health factors
        pressure_range = max(day_data['pressure']) - min(day_data['pressure'])
        if pressure_range > 20:
            health_score -= 10
            concerns.append("Pressure changes may affect sensitive individuals")
        
        # Weather condition health factors
        for condition in day_data['weather_conditions']:
            if condition == 'Thunderstorm':
                health_score -= 15
                concerns.append("Storm conditions - stay indoors")
            elif condition in ['Snow', 'Rain']:
                health_score -= 5
                concerns.append("Wet conditions - slip/fall risk")
        
        return {
            'score': max(0, health_score),
            'concerns': list(set(concerns))  # Remove duplicates
        }
    
    def _calculate_activity_suitability(self, day_data: Dict) -> Dict[str, Any]:
        """Calculate suitability for various activities"""
        if not day_data['temps']:
            return {'overall': 50, 'recommendations': []}
        
        avg_temp = sum(day_data['temps']) / len(day_data['temps'])
        avg_humidity = sum(day_data['humidity']) / len(day_data['humidity'])
        avg_wind = sum(day_data['wind_speed']) / len(day_data['wind_speed'])
        max_precip = max(day_data['precipitation'])
        
        # Activity scores
        outdoor_sports = 100
        indoor_activities = 50
        water_activities = 100
        
        # Temperature adjustments
        if not (15 <= avg_temp <= 28):
            outdoor_sports -= 20
            water_activities -= 15
        
        # Precipitation adjustments
        if max_precip > 50:
            outdoor_sports -= 40
            water_activities -= 30
            indoor_activities += 20
        elif max_precip > 20:
            outdoor_sports -= 20
            water_activities -= 10
        
        # Wind adjustments
        if avg_wind > 15:
            outdoor_sports -= 25
            water_activities -= 35
        elif avg_wind > 8:
            outdoor_sports -= 10
            water_activities -= 15
        
        # Humidity adjustments
        if avg_humidity > 80:
            outdoor_sports -= 15
        elif avg_humidity < 30:
            outdoor_sports -= 10
        
        overall_score = (outdoor_sports + water_activities) / 2
        
        # Generate recommendations
        recommendations = []
        if overall_score > 80:
            recommendations.append("Excellent day for all outdoor activities")
        elif overall_score > 60:
            recommendations.append("Good conditions for most outdoor activities")
        else:
            recommendations.append("Consider indoor activities")
        
        return {
            'overall': max(0, min(100, overall_score)),
            'outdoor_sports': max(0, min(100, outdoor_sports)),
            'water_activities': max(0, min(100, water_activities)),
            'indoor_activities': max(0, min(100, indoor_activities)),
            'recommendations': recommendations
        }
    
    def calculate_weather_trends_advanced(self, forecast_data: List[Dict]) -> Dict[str, Any]:
        """Advanced weather trends analysis with machine learning insights"""
        if not forecast_data:
            return {}
        
        # Extract time series data
        temps_max = [item['temp_max'] for item in forecast_data]
        temps_min = [item['temp_min'] for item in forecast_data]
        temps_avg = [item['temp_avg'] for item in forecast_data]
        humidity = [item['humidity'] for item in forecast_data]
        wind_speed = [item['wind_speed'] for item in forecast_data]
        pressure = [item['pressure_avg'] for item in forecast_data]
        comfort_scores = [item['comfort_score'] for item in forecast_data]
        
        # Advanced trend analysis
        trends = {
            'temperature': {
                'max_trend': self._calculate_advanced_trend(temps_max),
                'min_trend': self._calculate_advanced_trend(temps_min),
                'avg_trend': self._calculate_advanced_trend(temps_avg),
                'volatility': self._calculate_volatility(temps_max),
                'heat_wave_risk': self._detect_pattern_risk('heat_wave', forecast_data),
                'cold_snap_risk': self._detect_pattern_risk('cold_snap', forecast_data),
                'temperature_momentum': self._calculate_momentum(temps_avg),
                'diurnal_range_trend': self._calculate_advanced_trend([max_t - min_t for max_t, min_t in zip(temps_max, temps_min)])
            },
            'humidity': {
                'trend': self._calculate_advanced_trend(humidity),
                'avg': sum(humidity) / len(humidity),
                'stability': self._calculate_stability_index(humidity),
                'drought_risk': self._detect_pattern_risk('drought', forecast_data),
                'comfort_correlation': self._calculate_correlation(humidity, comfort_scores)
            },
            'wind': {
                'trend': self._calculate_advanced_trend(wind_speed),
                'avg': sum(wind_speed) / len(wind_speed),
                'max': max(wind_speed),
                'variability': np.std(wind_speed),
                'storm_risk': self._detect_pattern_risk('storm_system', forecast_data),
                'consistency_trend': self._calculate_wind_consistency_trend(forecast_data)
            },
            'pressure': {
                'trend': self._calculate_advanced_trend(pressure),
                'avg': sum(pressure) / len(pressure),
                'stability': self._calculate_stability_index(pressure),
                'change_rate': self._calculate_pressure_change_rate(pressure),
                'weather_change_likelihood': self._predict_weather_changes_advanced(pressure)
            },
            'comfort': {
                'trend': self._calculate_advanced_trend(comfort_scores),
                'avg': sum(comfort_scores) / len(comfort_scores),
                'forecast_quality': self._assess_forecast_comfort_quality(comfort_scores),
                'optimal_days': self._find_optimal_days(forecast_data)
            },
            'patterns': {
                'seasonal_alignment': self._assess_seasonal_alignment(forecast_data),
                'weather_diversity': self._calculate_weather_diversity(forecast_data),
                'stability_forecast': self._predict_stability_changes(forecast_data),
                'extreme_event_probability': self._calculate_extreme_event_probability(forecast_data)
            }
        }
        
        # Add machine learning insights
        trends['ml_insights'] = self._generate_ml_insights(forecast_data, trends)
        
        return trends
    
    def _calculate_advanced_trend(self, data: List[float]) -> Dict[str, Any]:
        """Calculate advanced trend analysis with confidence intervals"""
        if len(data) < 3:
            return {'direction': 'insufficient_data', 'strength': 0, 'confidence': 0}
        
        x = np.arange(len(data))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, data)
        
        # Determine trend direction and strength
        if abs(r_value) < 0.3:
            direction = 'stable'
            strength = abs(r_value)
        elif slope > 0:
            direction = 'increasing'
            strength = r_value
        else:
            direction = 'decreasing'
            strength = abs(r_value)
        
        # Calculate confidence based on p-value and r-squared
        confidence = (1 - p_value) * (r_value ** 2)
        
        return {
            'direction': direction,
            'strength': float(strength),
            'confidence': float(confidence),
            'slope': float(slope),
            'r_squared': float(r_value ** 2),
            'p_value': float(p_value),
            'prediction_accuracy': self._estimate_prediction_accuracy(r_value, len(data))
        }
    
    def _calculate_volatility(self, data: List[float]) -> float:
        """Calculate volatility using standard deviation of changes"""
        if len(data) < 2:
            return 0.0
        
        changes = [abs(data[i] - data[i-1]) for i in range(1, len(data))]
        return float(np.std(changes))
    
    def _calculate_momentum(self, data: List[float]) -> float:
        """Calculate momentum using rate of change acceleration"""
        if len(data) < 3:
            return 0.0
        
        # Calculate first and second derivatives
        first_diff = np.diff(data)
        second_diff = np.diff(first_diff)
        
        # Momentum is the average of second derivatives
        return float(np.mean(second_diff))
    
    def _calculate_stability_index(self, data: List[float]) -> float:
        """Calculate stability index (0-1, higher = more stable)"""
        if len(data) < 2:
            return 1.0
        
        cv = np.std(data) / np.mean(data) if np.mean(data) != 0 else 0
        return float(max(0, 1 - cv))
    
    def _calculate_correlation(self, data1: List[float], data2: List[float]) -> float:
        """Calculate correlation between two datasets"""
        if len(data1) != len(data2) or len(data1) < 2:
            return 0.0
        
        correlation, _ = stats.pearsonr(data1, data2)
        return float(correlation) if not np.isnan(correlation) else 0.0
    
    def _detect_pattern_risk(self, pattern_type: str, forecast_data: List[Dict]) -> float:
        """Advanced pattern risk detection with severity assessment"""
        if pattern_type not in self.weather_patterns:
            return 0.0
        
        pattern_config = self.weather_patterns[pattern_type]
        
        if pattern_type == 'heat_wave':
            return self._detect_heat_wave_advanced(forecast_data, pattern_config)
        elif pattern_type == 'cold_snap':
            return self._detect_cold_snap_advanced(forecast_data, pattern_config)
        elif pattern_type == 'drought':
            return self._detect_drought_advanced(forecast_data, pattern_config)
        elif pattern_type == 'storm_system':
            return self._detect_storm_advanced(forecast_data, pattern_config)
        
        return 0.0
    
    def _detect_heat_wave_advanced(self, forecast_data: List[Dict], config: Dict) -> float:
        """Advanced heat wave detection with severity levels"""
        severity_levels = config['severity_levels']
        max_risk = 0.0
        
        for severity, params in severity_levels.items():
            consecutive_days = 0
            max_consecutive = 0
            
            for day in forecast_data:
                if day['temp_max'] > params['temp']:
                    consecutive_days += 1
                    max_consecutive = max(max_consecutive, consecutive_days)
                else:
                    consecutive_days = 0
            
            if max_consecutive >= params['duration']:
                severity_multiplier = {'moderate': 0.4, 'severe': 0.7, 'extreme': 1.0}
                risk = severity_multiplier[severity] * min(max_consecutive / params['duration'], 2.0)
                max_risk = max(max_risk, risk)
        
        return min(max_risk, 1.0)
    
    def _detect_cold_snap_advanced(self, forecast_data: List[Dict], config: Dict) -> float:
        """Advanced cold snap detection"""
        severity_levels = config['severity_levels']
        max_risk = 0.0
        
        for severity, params in severity_levels.items():
            consecutive_days = 0
            max_consecutive = 0
            
            for day in forecast_data:
                if day['temp_min'] < params['temp']:
                    consecutive_days += 1
                    max_consecutive = max(max_consecutive, consecutive_days)
                else:
                    consecutive_days = 0
            
            if max_consecutive >= params['duration']:
                severity_multiplier = {'moderate': 0.4, 'severe': 0.7, 'extreme': 1.0}
                risk = severity_multiplier[severity] * min(max_consecutive / params['duration'], 2.0)
                max_risk = max(max_risk, risk)
        
        return min(max_risk, 1.0)
    
    def _detect_drought_advanced(self, forecast_data: List[Dict], config: Dict) -> float:
        """Advanced drought condition detection"""
        dry_days = 0
        low_humidity_days = 0
        
        for day in forecast_data:
            if day['precipitation_chance'] < config['precipitation_threshold'] * 100:
                dry_days += 1
            if day['humidity'] < config['humidity_threshold']:
                low_humidity_days += 1
        
        dry_risk = min(dry_days / len(forecast_data), 1.0)
        humidity_risk = min(low_humidity_days / len(forecast_data), 1.0)
        
        return (dry_risk + humidity_risk) / 2
    
    def _detect_storm_advanced(self, forecast_data: List[Dict], config: Dict) -> float:
        """Advanced storm system detection"""
        storm_indicators = 0
        total_possible = len(forecast_data) * 3  # Three indicators per day
        
        for day in forecast_data:
            # High wind indicator
            if day['wind_speed'] > config['wind_threshold']:
                storm_indicators += 1
            
            # Pressure drop indicator
            if 'pressure_trend' in day and day['pressure_trend'] == 'falling':
                storm_indicators += 1
            
            # High precipitation indicator
            if day['precipitation_chance'] > config['precipitation_threshold'] * 10:
                storm_indicators += 1
        
        return min(storm_indicators / total_possible, 1.0)
    
    def _calculate_wind_consistency_trend(self, forecast_data: List[Dict]) -> Dict[str, float]:
        """Calculate wind consistency trend over forecast period"""
        consistency_values = [day.get('wind_consistency', 0.5) for day in forecast_data]
        
        return {
            'trend': self._calculate_advanced_trend(consistency_values)['direction'],
            'avg_consistency': float(np.mean(consistency_values)),
            'consistency_stability': self._calculate_stability_index(consistency_values)
        }
    
    def _calculate_pressure_change_rate(self, pressure_data: List[float]) -> float:
        """Calculate the rate of pressure change"""
        if len(pressure_data) < 2:
            return 0.0
        
        changes = [pressure_data[i] - pressure_data[i-1] for i in range(1, len(pressure_data))]
        return float(np.mean(changes))
    
    def _predict_weather_changes_advanced(self, pressure_data: List[float]) -> Dict[str, float]:
        """Advanced weather change prediction based on pressure patterns"""
        if len(pressure_data) < 3:
            return {'probability': 0.0, 'confidence': 0.0, 'type': 'unknown'}
        
        # Calculate pressure trend and volatility
        trend_info = self._calculate_advanced_trend(pressure_data)
        volatility = self._calculate_volatility(pressure_data)
        
        # Rapid pressure changes indicate weather system movement
        change_probability = min(volatility / 10, 1.0)  # Normalize to 0-1
        
        # Determine change type
        if trend_info['direction'] == 'decreasing' and trend_info['strength'] > 0.5:
            change_type = 'deteriorating'
        elif trend_info['direction'] == 'increasing' and trend_info['strength'] > 0.5:
            change_type = 'improving'
        else:
            change_type = 'variable'
        
        return {
            'probability': float(change_probability),
            'confidence': float(trend_info['confidence']),
            'type': change_type,
            'volatility': float(volatility)
        }
    
    def _assess_forecast_comfort_quality(self, comfort_scores: List[float]) -> Dict[str, Any]:
        """Assess the overall quality of forecast comfort"""
        if not comfort_scores:
            return {'average': 50, 'quality': 'unknown', 'consistency': 0}
        
        avg_comfort = sum(comfort_scores) / len(comfort_scores)
        comfort_stability = self._calculate_stability_index(comfort_scores)
        
        # Determine quality level
        if avg_comfort >= 80 and comfort_stability >= 0.8:
            quality = 'excellent'
        elif avg_comfort >= 70 and comfort_stability >= 0.6:
            quality = 'good'
        elif avg_comfort >= 60:
            quality = 'fair'
        else:
            quality = 'poor'
        
        return {
            'average': float(avg_comfort),
            'quality': quality,
            'consistency': float(comfort_stability),
            'range': float(max(comfort_scores) - min(comfort_scores))
        }
    
    def _find_optimal_days(self, forecast_data: List[Dict]) -> List[Dict]:
        """Find the optimal days in the forecast"""
        if not forecast_data:
            return []
        
        # Sort by comfort score and other factors
        scored_days = []
        for day in forecast_data:
            score = (
                day.get('comfort_score', 50) * 0.4 +
                day.get('activity_score', {}).get('overall', 50) * 0.3 +
                (100 - day.get('extremes_risk', 0)) * 0.2 +
                day.get('weather_quality_score', 50) * 0.1
            )
            
            scored_days.append({
                'date': day['date'],
                'day': day['day_full'],
                'overall_score': score,
                'comfort_score': day.get('comfort_score', 50),
                'activity_score': day.get('activity_score', {}).get('overall', 50),
                'reasons': self._generate_optimal_day_reasons(day)
            })
        
        # Return top 3 days
        return sorted(scored_days, key=lambda x: x['overall_score'], reverse=True)[:3]
    
    def _generate_optimal_day_reasons(self, day_data: Dict) -> List[str]:
        """Generate reasons why a day is optimal"""
        reasons = []
        
        if day_data.get('comfort_score', 0) > 80:
            reasons.append("Excellent comfort conditions")
        
        if day_data.get('temp_max', 0) <= 25 and day_data.get('temp_min', 0) >= 15:
            reasons.append("Ideal temperature range")
        
        if day_data.get('precipitation_chance', 100) < 20:
            reasons.append("Low chance of precipitation")
        
        if day_data.get('wind_speed', 0) < 5:
            reasons.append("Light winds")
        
        activity_score = day_data.get('activity_score', {}).get('overall', 0)
        if activity_score > 80:
            reasons.append("Perfect for outdoor activities")
        
        return reasons[:3]  # Limit to top 3 reasons
    
    def _assess_seasonal_alignment(self, forecast_data: List[Dict]) -> Dict[str, Any]:
        """Assess how well the forecast aligns with seasonal expectations"""
        if not forecast_data:
            return {'alignment': 'unknown', 'score': 0.5}
        
        # Determine current season (simplified)
        current_month = datetime.now().month
        if 3 <= current_month <= 5:
            season = 'spring'
        elif 6 <= current_month <= 8:
            season = 'summer'
        elif 9 <= current_month <= 11:
            season = 'autumn'
        else:
            season = 'winter'
        
        seasonal_config = self.seasonal_factors[season]
        
        # Calculate alignment score
        alignment_scores = []
        for day in forecast_data:
            temp_avg = day.get('temp_avg', 20)
            humidity_avg = day.get('humidity', 50)
            
            # Temperature alignment
            temp_range = seasonal_config['temp_comfort_range']
            if temp_range[0] <= temp_avg <= temp_range[1]:
                temp_alignment = 1.0
            else:
                deviation = min(abs(temp_avg - temp_range[0]), abs(temp_avg - temp_range[1]))
                temp_alignment = max(0, 1 - deviation / 15)
            
            # Humidity alignment
            optimal_humidity = seasonal_config['humidity_optimal']
            humidity_deviation = abs(humidity_avg - optimal_humidity)
            humidity_alignment = max(0, 1 - humidity_deviation / 30)
            
            day_alignment = (temp_alignment + humidity_alignment) / 2
            alignment_scores.append(day_alignment)
        
        avg_alignment = sum(alignment_scores) / len(alignment_scores)
        
        if avg_alignment > 0.8:
            alignment_level = 'excellent'
        elif avg_alignment > 0.6:
            alignment_level = 'good'
        elif avg_alignment > 0.4:
            alignment_level = 'fair'
        else:
            alignment_level = 'poor'
        
        return {
            'alignment': alignment_level,
            'score': float(avg_alignment),
            'season': season,
            'deviation_analysis': self._analyze_seasonal_deviations(forecast_data, seasonal_config)
        }
    
    def _calculate_weather_diversity(self, forecast_data: List[Dict]) -> Dict[str, Any]:
        """Calculate weather diversity index"""
        if not forecast_data:
            return {'diversity_index': 0, 'variety': 'low'}
        
        conditions = [day.get('condition', 'Unknown') for day in forecast_data]
        unique_conditions = len(set(conditions))
        total_days = len(conditions)
        
        diversity_index = unique_conditions / total_days
        
        if diversity_index > 0.8:
            variety = 'very_high'
        elif diversity_index > 0.6:
            variety = 'high'
        elif diversity_index > 0.4:
            variety = 'moderate'
        elif diversity_index > 0.2:
            variety = 'low'
        else:
            variety = 'very_low'
        
        return {
            'diversity_index': float(diversity_index),
            'variety': variety,
            'unique_conditions': unique_conditions,
            'condition_distribution': dict(pd.Series(conditions).value_counts())
        }
    
    def _predict_stability_changes(self, forecast_data: List[Dict]) -> Dict[str, Any]:
        """Predict stability changes over the forecast period"""
        if len(forecast_data) < 3:
            return {'prediction': 'insufficient_data', 'confidence': 0}
        
        # Calculate stability for each day
        daily_stability = []
        for day in forecast_data:
            stability_factors = [
                day.get('stability_index', 0.5),
                1 - (day.get('temp_range', 10) / 20),  # Lower range = higher stability
                day.get('pressure_stability', 0.5),
                day.get('wind_consistency', 0.5)
            ]
            daily_stability.append(sum(stability_factors) / len(stability_factors))
        
        # Analyze trend
        stability_trend = self._calculate_advanced_trend(daily_stability)
        
        if stability_trend['direction'] == 'increasing':
            prediction = 'improving_stability'
        elif stability_trend['direction'] == 'decreasing':
            prediction = 'decreasing_stability'
        else:
            prediction = 'stable_conditions'
        
        return {
            'prediction': prediction,
            'confidence': stability_trend['confidence'],
            'current_stability': float(daily_stability[0]) if daily_stability else 0.5,
            'forecast_stability': float(daily_stability[-1]) if daily_stability else 0.5,
            'stability_trend': stability_trend
        }
    
    def _calculate_extreme_event_probability(self, forecast_data: List[Dict]) -> Dict[str, float]:
        """Calculate probability of extreme weather events"""
        if not forecast_data:
            return {'heat_extreme': 0, 'cold_extreme': 0, 'wind_extreme': 0, 'precipitation_extreme': 0}
        
        probabilities = {
            'heat_extreme': 0,
            'cold_extreme': 0,
            'wind_extreme': 0,
            'precipitation_extreme': 0
        }
        
        for day in forecast_data:
            # Heat extreme (>35°C)
            if day.get('temp_max', 0) > 35:
                probabilities['heat_extreme'] += 1
            
            # Cold extreme (<-5°C)
            if day.get('temp_min', 0) < -5:
                probabilities['cold_extreme'] += 1
            
            # Wind extreme (>20 m/s)
            if day.get('wind_max', 0) > 20:
                probabilities['wind_extreme'] += 1
            
            # Precipitation extreme (>80%)
            if day.get('precipitation_chance', 0) > 80:
                probabilities['precipitation_extreme'] += 1
        
        # Convert to probabilities
        total_days = len(forecast_data)
        for key in probabilities:
            probabilities[key] = probabilities[key] / total_days
        
        return probabilities
    
    def _generate_ml_insights(self, forecast_data: List[Dict], trends: Dict) -> Dict[str, Any]:
        """Generate machine learning insights and predictions"""
        insights = {
            'weather_pattern_classification': self._classify_weather_pattern(forecast_data),
            'anomaly_detection': self._detect_weather_anomalies(forecast_data),
            'predictive_confidence': self._calculate_prediction_confidence(trends),
            'recommendation_engine': self._generate_smart_recommendations(forecast_data, trends)
        }
        
        return insights
    
    def _classify_weather_pattern(self, forecast_data: List[Dict]) -> Dict[str, Any]:
        """Classify the overall weather pattern"""
        if not forecast_data:
            return {'pattern': 'unknown', 'confidence': 0}
        
        # Extract features for classification
        temp_stability = np.std([day.get('temp_avg', 20) for day in forecast_data])
        avg_temp = np.mean([day.get('temp_avg', 20) for day in forecast_data])
        avg_humidity = np.mean([day.get('humidity', 50) for day in forecast_data])
        avg_wind = np.mean([day.get('wind_speed', 5) for day in forecast_data])
        
        # Simple rule-based classification
        if temp_stability < 3 and avg_temp > 25:
            pattern = 'stable_warm'
        elif temp_stability < 3 and avg_temp < 15:
            pattern = 'stable_cool'
        elif temp_stability > 8:
            pattern = 'highly_variable'
        elif avg_wind > 10:
            pattern = 'windy_period'
        elif avg_humidity > 80:
            pattern = 'humid_period'
        else:
            pattern = 'mixed_conditions'
        
        # Calculate confidence based on how well features match pattern
        confidence = min(1.0, 1 / (temp_stability + 1)) if pattern == 'stable_warm' or pattern == 'stable_cool' else 0.7
        
        return {
            'pattern': pattern,
            'confidence': float(confidence),
            'characteristics': {
                'temperature_stability': float(temp_stability),
                'average_temperature': float(avg_temp),
                'average_humidity': float(avg_humidity),
                'average_wind': float(avg_wind)
            }
        }
    
    def _detect_weather_anomalies(self, forecast_data: List[Dict]) -> List[Dict]:
        """Detect weather anomalies in the forecast"""
        anomalies = []
        
        if len(forecast_data) < 3:
            return anomalies
        
        # Calculate z-scores for temperature
        temps = [day.get('temp_avg', 20) for day in forecast_data]
        temp_mean = np.mean(temps)
        temp_std = np.std(temps)
        
        for i, day in enumerate(forecast_data):
            temp = day.get('temp_avg', 20)
            if temp_std > 0:
                z_score = abs(temp - temp_mean) / temp_std
                if z_score > 2:  # More than 2 standard deviations
                    anomalies.append({
                        'date': day['date'],
                        'type': 'temperature_anomaly',
                        'severity': 'high' if z_score > 2.5 else 'moderate',
                        'description': f"Temperature significantly {'higher' if temp > temp_mean else 'lower'} than period average",
                        'z_score': float(z_score)
                    })
        
        return anomalies
    
    def _calculate_prediction_confidence(self, trends: Dict) -> Dict[str, float]:
        """Calculate confidence levels for various predictions"""
        confidence_scores = {}
        
        # Temperature prediction confidence
        temp_trend = trends.get('temperature', {})
        confidence_scores['temperature'] = temp_trend.get('max_trend', {}).get('confidence', 0.5)
        
        # Pressure prediction confidence
        pressure_trend = trends.get('pressure', {})
        confidence_scores['pressure'] = pressure_trend.get('trend', {}).get('confidence', 0.5)
        
        # Overall pattern confidence
        pattern_stability = trends.get('patterns', {}).get('stability_forecast', {}).get('confidence', 0.5)
        confidence_scores['overall_pattern'] = pattern_stability
        
        return confidence_scores
    
    def _generate_smart_recommendations(self, forecast_data: List[Dict], trends: Dict) -> List[Dict]:
        """Generate smart recommendations based on ML analysis"""
        recommendations = []
        
        # Weather pattern based recommendations
        pattern_info = trends.get('ml_insights', {}).get('weather_pattern_classification', {})
        pattern = pattern_info.get('pattern', 'unknown')
        
        if pattern == 'stable_warm':
            recommendations.append({
                'category': 'activity',
                'priority': 'high',
                'recommendation': 'Excellent period for outdoor activities and sports',
                'reasoning': 'Stable warm weather pattern detected'
            })
        elif pattern == 'highly_variable':
            recommendations.append({
                'category': 'preparation',
                'priority': 'medium',
                'recommendation': 'Pack layers and check weather frequently',
                'reasoning': 'High temperature variability expected'
            })
        
        # Trend based recommendations
        temp_trend = trends.get('temperature', {}).get('max_trend', {})
        if temp_trend.get('direction') == 'increasing' and temp_trend.get('confidence', 0) > 0.7:
            recommendations.append({
                'category': 'health',
                'priority': 'medium',
                'recommendation': 'Prepare for increasingly warm conditions',
                'reasoning': 'Strong warming trend detected'
            })
        
        return recommendations
    
    def format_wind_direction(self, degrees: float) -> str:
        """Format wind direction from degrees to compass direction"""
        if degrees is None:
            return "Unknown"
        
        directions = [
            "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
        ]
        
        index = int((degrees + 11.25) / 22.5) % 16
        return directions[index]
    
    def _estimate_uv_index(self, weather_condition: str, cloud_cover: int, hour: int) -> float:
        """Estimate UV index based on weather conditions"""
        base_uv = 0
        
        # Time-based UV calculation
        if 6 <= hour <= 18:
            if 11 <= hour <= 13:
                base_uv = 9
            elif 10 <= hour <= 14:
                base_uv = 7
            elif 9 <= hour <= 15:
                base_uv = 5
            else:
                base_uv = 3
        
        # Weather condition adjustments
        condition_lower = weather_condition.lower()
        if 'rain' in condition_lower or 'storm' in condition_lower:
            base_uv *= 0.3
        elif 'cloud' in condition_lower:
            base_uv *= 0.7
        elif 'clear' in condition_lower:
            base_uv *= 1.1
        
        # Cloud cover adjustments
        cloud_factor = 1 - (cloud_cover / 100) * 0.7
        base_uv *= cloud_factor
        
        return max(0, min(11, base_uv))
    
    def _estimate_prediction_accuracy(self, r_value: float, data_points: int) -> float:
        """Estimate prediction accuracy based on correlation and sample size"""
        # Higher correlation and more data points = higher accuracy
        correlation_factor = r_value ** 2  # R-squared
        sample_size_factor = min(data_points / 10, 1.0)  # Normalize to 1.0
        
        return (correlation_factor + sample_size_factor) / 2
    
    def _analyze_seasonal_deviations(self, forecast_data: List[Dict], seasonal_config: Dict) -> Dict[str, Any]:
        """Analyze deviations from seasonal norms"""
        temp_deviations = []
        humidity_deviations = []
        
        temp_range = seasonal_config['temp_comfort_range']
        optimal_humidity = seasonal_config['humidity_optimal']
        
        for day in forecast_data:
            temp_avg = day.get('temp_avg', 20)
            humidity_avg = day.get('humidity', 50)
            
            # Temperature deviation
            if temp_avg < temp_range[0]:
                temp_deviations.append(temp_range[0] - temp_avg)
            elif temp_avg > temp_range[1]:
                temp_deviations.append(temp_avg - temp_range[1])
            else:
                temp_deviations.append(0)
            
            # Humidity deviation
            humidity_deviations.append(abs(humidity_avg - optimal_humidity))
        
        return {
            'avg_temp_deviation': float(np.mean(temp_deviations)),
            'max_temp_deviation': float(np.max(temp_deviations)),
            'avg_humidity_deviation': float(np.mean(humidity_deviations)),
            'max_humidity_deviation': float(np.max(humidity_deviations)),
            'days_within_normal': sum(1 for dev in temp_deviations if dev == 0)
        }
    
    def _calculate_day_stability(self, day_data: Dict) -> float:
        """Calculate overall stability index for a single day"""
        if not day_data['temps']:
            return 0.5
        
        # Temperature stability (lower range = higher stability)
        temp_range = max(day_data['temps']) - min(day_data['temps'])
        temp_stability = max(0, 1 - temp_range / 20)
        
        # Pressure stability
        pressure_range = max(day_data['pressure']) - min(day_data['pressure'])
        pressure_stability = max(0, 1 - pressure_range / 20)
        
        # Wind consistency
        wind_std = np.std(day_data['wind_speed'])
        wind_stability = max(0, 1 - wind_std / 10)
        
        # Overall stability (weighted average)
        stability = (temp_stability * 0.4 + pressure_stability * 0.3 + wind_stability * 0.3)
        return float(stability)
    
    def _assess_extreme_weather_risk(self, day_data: Dict) -> float:
        """Assess risk of extreme weather conditions"""
        risk_score = 0
        
        if not day_data['temps']:
            return risk_score
        
        max_temp = max(day_data['temps'])
        min_temp = min(day_data['temps'])
        max_wind = max(day_data['wind_speed'])
        
        # Temperature extremes
        if max_temp > 35:
            risk_score += 30
        elif max_temp > 30:
            risk_score += 15
        
        if min_temp < -10:
            risk_score += 25
        elif min_temp < 0:
            risk_score += 10
        
        # Wind extremes
        if max_wind > 20:
            risk_score += 25
        elif max_wind > 15:
            risk_score += 15
        
        # Weather conditions
        dangerous_conditions = ['Thunderstorm', 'Snow', 'Fog']
        for condition in day_data['weather_conditions']:
            if condition in dangerous_conditions:
                risk_score += 20
                break
        
        return min(risk_score, 100)
    
    def _find_optimal_time_periods(self, hourly_patterns: List[Dict], target_date: datetime) -> List[Dict]:
        """Find optimal time periods within a day"""
        # Filter hourly data for the target date
        day_hours = [
            hour for hour in hourly_patterns 
            if hour['datetime'].date() == target_date.date()
        ]
        
        if not day_hours:
            return []
        
        optimal_periods = []
        current_period = None
        
        for hour_data in day_hours:
            # Calculate hourly comfort score
            comfort_score = self._calculate_hourly_comfort(hour_data)
            
            if comfort_score > 70:  # Good comfort threshold
                if current_period is None:
                    current_period = {
                        'start_time': hour_data['datetime'].strftime('%H:%M'),
                        'end_time': hour_data['datetime'].strftime('%H:%M'),
                        'avg_comfort': comfort_score,
                        'conditions': [hour_data['condition']]
                    }
                else:
                    current_period['end_time'] = hour_data['datetime'].strftime('%H:%M')
                    current_period['avg_comfort'] = (current_period['avg_comfort'] + comfort_score) / 2
                    current_period['conditions'].append(hour_data['condition'])
            else:
                if current_period is not None:
                    optimal_periods.append(current_period)
                    current_period = None
        
        # Add the last period if it exists
        if current_period is not None:
            optimal_periods.append(current_period)
        
        return optimal_periods[:3]  # Return top 3 periods
    
    def _calculate_hourly_comfort(self, hour_data: Dict) -> float:
        """Calculate comfort score for a single hour"""
        temp = hour_data.get('temp', 20)
        humidity = hour_data.get('humidity', 50)
        wind_speed = hour_data.get('wind_speed', 5)
        
        # Simple comfort calculation
        temp_comfort = self._calculate_temperature_comfort(temp)
        humidity_comfort = self._calculate_humidity_comfort(humidity)
        wind_comfort = self._calculate_wind_comfort(wind_speed)
        
        return (temp_comfort + humidity_comfort + wind_comfort) / 3 * 100
    
    def _calculate_overall_weather_quality(self, day_data: Dict) -> float:
        """Calculate overall weather quality score for a day"""
        if not day_data['temps']:
            return 50
        
        # Factors contributing to weather quality
        factors = []
        
        # Temperature factor
        avg_temp = sum(day_data['temps']) / len(day_data['temps'])
        temp_quality = self._calculate_temperature_comfort(avg_temp) * 100
        factors.append(temp_quality)
        
        # Precipitation factor
        max_precip = max(day_data['precipitation'])
        precip_quality = max(0, 100 - max_precip)
        factors.append(precip_quality)
        
        # Wind factor
        avg_wind = sum(day_data['wind_speed']) / len(day_data['wind_speed'])
        wind_quality = self._calculate_wind_comfort(avg_wind) * 100
        factors.append(wind_quality)
        
        # Stability factor
        stability = self._calculate_day_stability(day_data)
        factors.append(stability * 100)
        
        return sum(factors) / len(factors)
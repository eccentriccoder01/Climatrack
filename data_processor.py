import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
import json

class DataProcessor:
    """Advanced weather data processing with AI-powered analytics"""
    
    def __init__(self):
        self.temperature_units = {
            'metric': '°C',
            'imperial': '°F',
            'kelvin': 'K'
        }
        self.speed_units = {
            'metric': 'm/s',
            'imperial': 'mph',
            'kelvin': 'm/s'
        }
        
        # Weather pattern recognition database
        self.weather_patterns = {
            'heat_wave': {'temp_threshold': 35, 'duration': 3},
            'cold_snap': {'temp_threshold': -5, 'duration': 2},
            'drought': {'humidity_threshold': 30, 'duration': 7},
            'storm_system': {'wind_threshold': 15, 'pressure_drop': 10}
        }
    
    def process_forecast_data(self, forecast_data: Dict, units: str = 'metric') -> List[Dict]:
        """Enhanced forecast processing with advanced analytics"""
        if not forecast_data or 'list' not in forecast_data:
            return []
        
        daily_data = {}
        
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
                    'clouds': []
                }
            
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
        
        # Process daily summaries with enhanced metrics
        processed_forecast = []
        for date_key, data in daily_data.items():
            # Get most common weather condition and icon
            most_common_condition = max(set(data['weather_conditions']), 
                                      key=data['weather_conditions'].count)
            most_common_icon = max(set(data['icons']), key=data['icons'].count)
            most_common_desc = max(set(data['descriptions']), key=data['descriptions'].count)
            
            # Calculate advanced metrics
            temp_range = max(data['temps']) - min(data['temps'])
            pressure_trend = self._calculate_pressure_trend(data['pressure'])
            wind_consistency = self._calculate_wind_consistency(data['wind_direction'])
            
            processed_forecast.append({
                'date': data['date'],
                'day': data['day'][:3],  # Short day name
                'temp_max': max(data['temps']),
                'temp_min': min(data['temps']),
                'temp_avg': sum(data['temps']) / len(data['temps']),
                'temp_range': temp_range,
                'humidity': sum(data['humidity']) / len(data['humidity']),
                'humidity_range': max(data['humidity']) - min(data['humidity']),
                'wind_speed': sum(data['wind_speed']) / len(data['wind_speed']),
                'wind_max': max(data['wind_speed']),
                'wind_consistency': wind_consistency,
                'pressure_avg': sum(data['pressure']) / len(data['pressure']),
                'pressure_trend': pressure_trend,
                'condition': most_common_condition,
                'icon': most_common_icon,
                'description': most_common_desc,
                'precipitation_chance': max(data['precipitation']),
                'cloud_coverage': sum(data['clouds']) / len(data['clouds']),
                'comfort_score': self._calculate_daily_comfort(data)
            })
        
        return sorted(processed_forecast, key=lambda x: x['date'])[:5]
    
    def _calculate_pressure_trend(self, pressure_data: List[float]) -> str:
        """Calculate pressure trend for weather prediction"""
        if len(pressure_data) < 2:
            return 'stable'
        
        first_half = pressure_data[:len(pressure_data)//2]
        second_half = pressure_data[len(pressure_data)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        diff = second_avg - first_avg
        
        if diff > 2:
            return 'rising'
        elif diff < -2:
            return 'falling'
        else:
            return 'stable'
    
    def _calculate_wind_consistency(self, wind_directions: List[float]) -> float:
        """Calculate wind direction consistency (0-1 scale)"""
        if not wind_directions:
            return 0.0
        
        # Convert to radians and calculate circular variance
        radians = [np.radians(d) for d in wind_directions]
        mean_sin = np.mean([np.sin(r) for r in radians])
        mean_cos = np.mean([np.cos(r) for r in radians])
        
        # Circular variance (0 = consistent, 1 = random)
        circular_variance = 1 - np.sqrt(mean_sin**2 + mean_cos**2)
        
        # Return consistency (inverse of variance)
        return 1 - circular_variance
    
    def _calculate_daily_comfort(self, day_data: Dict) -> float:
        """Calculate overall comfort score for a day"""
        temps = day_data['temps']
        humidity = day_data['humidity']
        wind_speed = day_data['wind_speed']
        
        # Temperature comfort (optimal: 18-24°C)
        temp_avg = sum(temps) / len(temps)
        temp_comfort = 1.0 - min(abs(temp_avg - 21) / 10, 1.0)
        
        # Humidity comfort (optimal: 40-60%)
        humidity_avg = sum(humidity) / len(humidity)
        if 40 <= humidity_avg <= 60:
            humidity_comfort = 1.0
        else:
            humidity_comfort = 1.0 - min(abs(humidity_avg - 50) / 50, 1.0)
        
        # Wind comfort (optimal: < 5 m/s)
        wind_avg = sum(wind_speed) / len(wind_speed)
        wind_comfort = 1.0 - min(wind_avg / 15, 1.0)
        
        # Overall comfort (weighted average)
        comfort_score = (temp_comfort * 0.5 + humidity_comfort * 0.3 + wind_comfort * 0.2) * 100
        return max(0, min(100, comfort_score))
    
    def calculate_weather_trends(self, forecast_data: List[Dict]) -> Dict[str, Any]:
        """Enhanced weather trends with pattern recognition"""
        if not forecast_data:
            return {}
        
        temps_max = [item['temp_max'] for item in forecast_data]
        temps_min = [item['temp_min'] for item in forecast_data]
        humidity = [item['humidity'] for item in forecast_data]
        wind_speed = [item['wind_speed'] for item in forecast_data]
        pressure = [item.get('pressure_avg', 1013) for item in forecast_data]
        
        trends = {
            'temperature': {
                'max_trend': self._calculate_trend(temps_max),
                'min_trend': self._calculate_trend(temps_min),
                'max_change': max(temps_max) - min(temps_max),
                'min_change': max(temps_min) - min(temps_min),
                'volatility': self._calculate_volatility(temps_max),
                'heat_wave_risk': self._detect_heat_wave(temps_max),
                'cold_snap_risk': self._detect_cold_snap(temps_min)
            },
            'humidity': {
                'trend': self._calculate_trend(humidity),
                'avg': sum(humidity) / len(humidity),
                'change': max(humidity) - min(humidity),
                'drought_risk': self._detect_drought_conditions(humidity),
                'comfort_days': sum(1 for h in humidity if 40 <= h <= 60)
            },
            'wind': {
                'trend': self._calculate_trend(wind_speed),
                'avg': sum(wind_speed) / len(wind_speed),
                'max': max(wind_speed),
                'storm_risk': self._detect_storm_conditions(wind_speed),
                'calm_days': sum(1 for w in wind_speed if w < 3)
            },
            'pressure': {
                'trend': self._calculate_trend(pressure),
                'avg': sum(pressure) / len(pressure),
                'stability': self._calculate_pressure_stability(pressure),
                'weather_change_likelihood': self._predict_weather_changes(pressure)
            },
            'overall': {
                'stability_index': self._calculate_overall_stability(forecast_data),
                'comfort_trend': self._calculate_comfort_trend(forecast_data),
                'best_day': self._find_best_weather_day(forecast_data),
                'weather_warnings': self._generate_weather_warnings(forecast_data)
            }
        }
        
        return trends
    
    def _calculate_volatility(self, data: List[float]) -> float:
        """Calculate temperature volatility"""
        if len(data) < 2:
            return 0.0
        
        changes = [abs(data[i] - data[i-1]) for i in range(1, len(data))]
        return sum(changes) / len(changes)
    
    def _detect_heat_wave(self, temps: List[float]) -> float:
        """Detect heat wave probability (0-1)"""
        threshold = self.weather_patterns['heat_wave']['temp_threshold']
        consecutive_hot_days = 0
        max_consecutive = 0
        
        for temp in temps:
            if temp > threshold:
                consecutive_hot_days += 1
                max_consecutive = max(max_consecutive, consecutive_hot_days)
            else:
                consecutive_hot_days = 0
        
        required_duration = self.weather_patterns['heat_wave']['duration']
        return min(max_consecutive / required_duration, 1.0)
    
    def _detect_cold_snap(self, temps: List[float]) -> float:
        """Detect cold snap probability (0-1)"""
        threshold = self.weather_patterns['cold_snap']['temp_threshold']
        consecutive_cold_days = 0
        max_consecutive = 0
        
        for temp in temps:
            if temp < threshold:
                consecutive_cold_days += 1
                max_consecutive = max(max_consecutive, consecutive_cold_days)
            else:
                consecutive_cold_days = 0
        
        required_duration = self.weather_patterns['cold_snap']['duration']
        return min(max_consecutive / required_duration, 1.0)
    
    def _detect_drought_conditions(self, humidity: List[float]) -> float:
        """Detect drought conditions probability (0-1)"""
        threshold = self.weather_patterns['drought']['humidity_threshold']
        low_humidity_days = sum(1 for h in humidity if h < threshold)
        return min(low_humidity_days / len(humidity), 1.0)
    
    def _detect_storm_conditions(self, wind_speeds: List[float]) -> float:
        """Detect storm conditions probability (0-1)"""
        threshold = self.weather_patterns['storm_system']['wind_threshold']
        high_wind_days = sum(1 for w in wind_speeds if w > threshold)
        return min(high_wind_days / len(wind_speeds), 1.0)
    
    def _calculate_pressure_stability(self, pressure: List[float]) -> float:
        """Calculate atmospheric pressure stability (0-1)"""
        if len(pressure) < 2:
            return 1.0
        
        pressure_range = max(pressure) - min(pressure)
        # Normalize to 0-1 scale (20 hPa = very unstable)
        stability = 1.0 - min(pressure_range / 20, 1.0)
        return stability
    
    def _predict_weather_changes(self, pressure: List[float]) -> float:
        """Predict likelihood of weather changes based on pressure trends"""
        if len(pressure) < 3:
            return 0.0
        
        # Calculate rate of pressure change
        changes = [pressure[i] - pressure[i-1] for i in range(1, len(pressure))]
        avg_change = sum(changes) / len(changes)
        
        # Rapid pressure changes indicate weather system movement
        change_likelihood = min(abs(avg_change) / 10, 1.0)
        return change_likelihood
    
    def _calculate_overall_stability(self, forecast_data: List[Dict]) -> float:
        """Calculate overall weather stability index"""
        if not forecast_data:
            return 0.0
        
        # Extract various metrics
        temp_ranges = [item.get('temp_range', 0) for item in forecast_data]
        wind_consistency = [item.get('wind_consistency', 1) for item in forecast_data]
        pressure_stability = [item.get('pressure_trend', 'stable') == 'stable' for item in forecast_data]
        
        # Calculate stability components
        temp_stability = 1.0 - (sum(temp_ranges) / len(temp_ranges)) / 20  # Normalize
        wind_stability = sum(wind_consistency) / len(wind_consistency)
        pressure_stability_score = sum(pressure_stability) / len(pressure_stability)
        
        # Weighted average
        overall_stability = (temp_stability * 0.4 + wind_stability * 0.3 + pressure_stability_score * 0.3)
        return max(0, min(1, overall_stability))
    
    def _calculate_comfort_trend(self, forecast_data: List[Dict]) -> str:
        """Calculate comfort trend over forecast period"""
        comfort_scores = [item.get('comfort_score', 50) for item in forecast_data]
        
        if len(comfort_scores) < 2:
            return 'stable'
        
        trend = self._calculate_trend(comfort_scores)
        return trend
    
    def _find_best_weather_day(self, forecast_data: List[Dict]) -> Dict:
        """Find the day with the best weather conditions"""
        if not forecast_data:
            return {}
        
        best_day = max(forecast_data, key=lambda x: x.get('comfort_score', 0))
        return {
            'date': best_day['date'],
            'day': best_day['day'],
            'comfort_score': best_day.get('comfort_score', 0),
            'reason': self._generate_best_day_reason(best_day)
        }
    
    def _generate_best_day_reason(self, day_data: Dict) -> str:
        """Generate reason why this day has the best weather"""
        reasons = []
        
        if day_data.get('temp_max', 0) <= 25 and day_data.get('temp_min', 0) >= 15:
            reasons.append("ideal temperature range")
        
        if 40 <= day_data.get('humidity', 0) <= 60:
            reasons.append("comfortable humidity")
        
        if day_data.get('wind_speed', 0) < 5:
            reasons.append("light winds")
        
        if day_data.get('precipitation_chance', 0) < 20:
            reasons.append("low chance of rain")
        
        if not reasons:
            reasons.append("relatively stable conditions")
        
        return ", ".join(reasons[:2])  # Limit to top 2 reasons
    
    def _generate_weather_warnings(self, forecast_data: List[Dict]) -> List[str]:
        """Generate weather warnings based on forecast analysis"""
        warnings = []
        
        # Temperature warnings
        temps_max = [item['temp_max'] for item in forecast_data]
        temps_min = [item['temp_min'] for item in forecast_data]
        
        if max(temps_max) > 35:
            warnings.append("🔥 Extreme heat expected - take precautions")
        elif max(temps_max) > 30:
            warnings.append("☀️ Hot weather ahead - stay hydrated")
        
        if min(temps_min) < 0:
            warnings.append("🧊 Freezing temperatures - protect pipes and plants")
        elif min(temps_min) < 5:
            warnings.append("❄️ Cold weather - dress warmly")
        
        # Wind warnings
        wind_speeds = [item['wind_speed'] for item in forecast_data]
        if max(wind_speeds) > 15:
            warnings.append("💨 Strong winds expected - secure loose objects")
        
        # Precipitation warnings
        precip_chances = [item.get('precipitation_chance', 0) for item in forecast_data]
        if max(precip_chances) > 70:
            warnings.append("🌧️ High chance of precipitation - carry umbrella")
        
        # Pressure warnings
        pressure_trends = [item.get('pressure_trend', 'stable') for item in forecast_data]
        if 'falling' in pressure_trends:
            warnings.append("📉 Falling pressure - weather changes likely")
        
        return warnings[:3]  # Limit to top 3 warnings
    
    def get_weather_recommendations(self, current_weather: Dict, forecast_data: List[Dict]) -> List[str]:
        """Enhanced AI-powered weather recommendations"""
        recommendations = []
        
        if not current_weather:
            return recommendations
        
        temp = current_weather['main']['temp']
        humidity = current_weather['main']['humidity']
        wind_speed = current_weather['wind']['speed']
        condition = current_weather['weather'][0]['main'].lower()
        pressure = current_weather['main']['pressure']
        
        # Advanced temperature-based recommendations
        if temp < -10:
            recommendations.append("🧥 CRITICAL: Extreme cold! Limit outdoor exposure, wear multiple layers, cover all exposed skin.")
        elif temp < 0:
            recommendations.append("🧣 Freezing conditions! Bundle up with winter gear and watch for icy surfaces.")
        elif temp < 10:
            recommendations.append("🧥 Cold weather - wear a warm jacket, gloves, and consider a hat.")
        elif temp > 40:
            recommendations.append("🔥 CRITICAL: Dangerous heat! Seek air conditioning, avoid outdoor activities.")
        elif temp > 35:
            recommendations.append("☀️ Extreme heat warning! Stay hydrated, wear light colors, seek shade frequently.")
        elif temp > 30:
            recommendations.append("🌡️ Very hot! Drink plenty of water, wear breathable clothing, limit sun exposure.")
        elif 20 <= temp <= 25:
            recommendations.append("🌤️ Perfect weather! Great day for outdoor activities and sports.")
        
        # Enhanced humidity recommendations
        if humidity > 90:
            recommendations.append("💧 Extremely humid! Stay in air-conditioned areas, wear moisture-wicking fabrics.")
        elif humidity > 80:
            recommendations.append("💦 Very humid - you may feel uncomfortable, stay cool and hydrated.")
        elif humidity < 20:
            recommendations.append("🏜️ Very dry air! Use moisturizer, drink extra water, consider a humidifier.")
        elif humidity < 30:
            recommendations.append("🌵 Low humidity - keep skin moisturized and stay hydrated.")
        
        # Enhanced wind recommendations
        if wind_speed > 20:
            recommendations.append("💨 DANGER: Very strong winds! Avoid driving high vehicles, stay indoors if possible.")
        elif wind_speed > 15:
            recommendations.append("🌪️ Strong winds! Secure outdoor items, be cautious with umbrellas.")
        elif wind_speed > 10:
            recommendations.append("🍃 Windy conditions - hold onto hats and be careful with light objects.")
        
        # Pressure-based recommendations
        if pressure < 1000:
            recommendations.append("📉 Low pressure system - weather changes likely, be prepared for storms.")
        elif pressure > 1025:
            recommendations.append("📈 High pressure - stable, clear weather expected.")
        
        # Advanced weather condition recommendations
        if 'thunderstorm' in condition:
            recommendations.append("⛈️ ALERT: Thunderstorms! Stay indoors, avoid water and high places.")
        elif 'rain' in condition:
            if wind_speed > 10:
                recommendations.append("🌧️💨 Stormy conditions! Umbrella may not help - wear waterproof gear.")
            else:
                recommendations.append("☔ Rain expected! Don't forget waterproof clothing and umbrella.")
        elif 'snow' in condition:
            recommendations.append("❄️ Snow conditions! Drive carefully, wear non-slip shoes, dress warmly.")
        elif 'fog' in condition:
            recommendations.append("🌫️ Foggy conditions! Reduce driving speed, use fog lights if available.")
        elif 'clear' in condition and temp > 25:
            recommendations.append("☀️ Beautiful clear weather! Perfect for outdoor activities - don't forget sunscreen!")
        
        # Forecast-based advanced recommendations
        if forecast_data:
            trends = self.calculate_weather_trends(forecast_data)
            
            # Temperature trend recommendations
            temp_trend = trends.get('temperature', {})
            if temp_trend.get('heat_wave_risk', 0) > 0.5:
                recommendations.append("🔥 Heat wave approaching! Prepare cooling strategies for the coming days.")
            elif temp_trend.get('cold_snap_risk', 0) > 0.5:
                recommendations.append("🧊 Cold snap coming! Prepare warm clothing and heating for several days.")
            elif temp_trend.get('max_trend') == 'increasing':
                recommendations.append("📈 Warming trend ahead - you can gradually wear lighter clothing.")
            elif temp_trend.get('max_trend') == 'decreasing':
                recommendations.append("📉 Cooling trend coming - prepare warmer clothes for the next few days.")
            
            # Weather stability recommendations
            stability = trends.get('overall', {}).get('stability_index', 0)
            if stability < 0.3:
                recommendations.append("🌪️ Unstable weather pattern! Be prepared for rapid changes.")
            elif stability > 0.8:
                recommendations.append("😌 Stable weather ahead - consistent conditions expected.")
            
            # Best day recommendation
            best_day = trends.get('overall', {}).get('best_day', {})
            if best_day:
                best_date = best_day.get('date', datetime.now()).strftime('%A')
                recommendations.append(f"⭐ {best_date} looks like the best weather day! Plan outdoor activities.")
        
        # Health and activity recommendations
        comfort_index = self.calculate_comfort_index(temp, humidity, wind_speed)
        comfort_score = comfort_index['score']
        
        if comfort_score > 80:
            recommendations.append("🏃‍♀️ Excellent conditions for outdoor exercise and sports!")
        elif comfort_score > 60:
            recommendations.append("🚶‍♂️ Good weather for walking and light outdoor activities.")
        elif comfort_score < 40:
            recommendations.append("🏠 Consider indoor activities - outdoor conditions may be uncomfortable.")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def calculate_comfort_index(self, temp: float, humidity: float, wind_speed: float) -> Dict[str, Any]:
        """Enhanced comfort index with detailed analysis"""
        # Advanced Heat Index calculation
        if temp >= 20:
            # More accurate heat index formula
            T = temp
            RH = humidity
            heat_index = (-42.379 + 
                         2.04901523 * T + 
                         10.14333127 * RH - 
                         0.22475541 * T * RH - 
                         6.83783e-3 * T**2 - 
                         5.481717e-2 * RH**2 + 
                         1.22874e-3 * T**2 * RH + 
                         8.5282e-4 * T * RH**2 - 
                         1.99e-6 * T**2 * RH**2)
            
            # Adjust for Celsius if needed
            if temp < 100:  # Assume Celsius
                heat_index = temp + 0.5555 * (6.11 * np.exp(5417.7530 * ((1/273.16) - (1/(temp + 273.16)))) - 10)
        else:
            heat_index = temp
        
        # Enhanced Wind Chill calculation
        if temp <= 10 and wind_speed > 1.34:
            # More accurate wind chill formula
            wind_kmh = wind_speed * 3.6  # Convert m/s to km/h
            wind_chill = (13.12 + 
                         0.6215 * temp - 
                         11.37 * (wind_kmh**0.16) + 
                         0.3965 * temp * (wind_kmh**0.16))
        else:
            wind_chill = temp
        
        # Advanced comfort assessment
        comfort_score = 100
        comfort_factors = {}
        
        # Temperature comfort analysis (optimal: 18-24°C)
        if temp < 10:
            temp_penalty = (10 - temp) * 8
            comfort_factors['temperature'] = f"Too cold ({temp:.1f}°)"
        elif temp < 18:
            temp_penalty = (18 - temp) * 3
            comfort_factors['temperature'] = f"Cool ({temp:.1f}°)"
        elif temp > 30:
            temp_penalty = (temp - 30) * 5
            comfort_factors['temperature'] = f"Too hot ({temp:.1f}°)"
        elif temp > 24:
            temp_penalty = (temp - 24) * 2
            comfort_factors['temperature'] = f"Warm ({temp:.1f}°)"
        else:
            temp_penalty = 0
            comfort_factors['temperature'] = f"Ideal ({temp:.1f}°)"
        
        comfort_score -= temp_penalty
        
        # Humidity comfort analysis (optimal: 40-60%)
        if humidity < 30:
            humidity_penalty = (30 - humidity) * 1.5
            comfort_factors['humidity'] = f"Too dry ({humidity:.0f}%)"
        elif humidity < 40:
            humidity_penalty = (40 - humidity) * 0.8
            comfort_factors['humidity'] = f"Dry ({humidity:.0f}%)"
        elif humidity > 80:
            humidity_penalty = (humidity - 80) * 2
            comfort_factors['humidity'] = f"Too humid ({humidity:.0f}%)"
        elif humidity > 60:
            humidity_penalty = (humidity - 60) * 1
            comfort_factors['humidity'] = f"Humid ({humidity:.0f}%)"
        else:
            humidity_penalty = 0
            comfort_factors['humidity'] = f"Comfortable ({humidity:.0f}%)"
        
        comfort_score -= humidity_penalty
        
        # Wind comfort analysis (optimal: 1-5 m/s)
        if wind_speed > 15:
            wind_penalty = (wind_speed - 15) * 5
            comfort_factors['wind'] = f"Too windy ({wind_speed:.1f} m/s)"
        elif wind_speed > 8:
            wind_penalty = (wind_speed - 8) * 2
            comfort_factors['wind'] = f"Windy ({wind_speed:.1f} m/s)"
        elif wind_speed < 0.5:
            wind_penalty = 5  # Stagnant air
            comfort_factors['wind'] = f"Still air ({wind_speed:.1f} m/s)"
        else:
            wind_penalty = 0
            comfort_factors['wind'] = f"Pleasant breeze ({wind_speed:.1f} m/s)"
        
        comfort_score -= wind_penalty
        
        # Ensure score is within bounds
        comfort_score = max(0, min(100, comfort_score))
        
        # Enhanced comfort level determination
        if comfort_score >= 90:
            comfort_level = "Perfect"
            comfort_color = "#22c55e"
            comfort_emoji = "🤩"
        elif comfort_score >= 80:
            comfort_level = "Excellent"
            comfort_color = "#4CAF50"
            comfort_emoji = "😊"
        elif comfort_score >= 70:
            comfort_level = "Very Good"
            comfort_color = "#8BC34A"
            comfort_emoji = "😌"
        elif comfort_score >= 60:
            comfort_level = "Good"
            comfort_color = "#CDDC39"
            comfort_emoji = "🙂"
        elif comfort_score >= 50:
            comfort_level = "Fair"
            comfort_color = "#FFC107"
            comfort_emoji = "😐"
        elif comfort_score >= 40:
            comfort_level = "Poor"
            comfort_color = "#FF9800"
            comfort_emoji = "😕"
        elif comfort_score >= 30:
            comfort_level = "Very Poor"
            comfort_color = "#FF5722"
            comfort_emoji = "😣"
        else:
            comfort_level = "Extremely Poor"
            comfort_color = "#F44336"
            comfort_emoji = "😵"
        
        return {
            'score': comfort_score,
            'level': comfort_level,
            'color': comfort_color,
            'emoji': comfort_emoji,
            'heat_index': heat_index,
            'wind_chill': wind_chill,
            'factors': comfort_factors,
            'recommendations': self._get_comfort_recommendations(comfort_score, comfort_factors)
        }
    
    def _get_comfort_recommendations(self, score: float, factors: Dict) -> List[str]:
        """Get specific recommendations based on comfort factors"""
        recommendations = []
        
        for factor, description in factors.items():
            if "Too cold" in description:
                recommendations.append("Wear warm layers and winter accessories")
            elif "Too hot" in description:
                recommendations.append("Seek air conditioning or shade, wear light clothing")
            elif "Too dry" in description:
                recommendations.append("Use moisturizer and stay hydrated")
            elif "Too humid" in description:
                recommendations.append("Stay in air-conditioned areas, wear breathable fabrics")
            elif "Too windy" in description:
                recommendations.append("Secure loose items, be cautious outdoors")
            elif "Still air" in description:
                recommendations.append("Consider indoor ventilation or fans")
        
        if score < 50:
            recommendations.append("Consider postponing outdoor activities")
        elif score > 80:
            recommendations.append("Perfect weather for outdoor activities!")
        
        return recommendations
    
    def process_hourly_data(self, forecast_data: Dict) -> List[Dict]:
        """Enhanced hourly forecast processing with advanced metrics"""
        if not forecast_data or 'list' not in forecast_data:
            return []
        
        hourly_data = []
        current_date = datetime.now().date()
        
        for item in forecast_data['list'][:40]:  # Extended to 40 hours
            dt = datetime.fromtimestamp(item['dt'])
            
            # Skip past hours for today
            if dt.date() == current_date and dt.hour < datetime.now().hour:
                continue
            
            # Calculate advanced metrics
            comfort_index = self.calculate_comfort_index(
                item['main']['temp'],
                item['main']['humidity'],
                item['wind']['speed']
            )
            
            uv_risk = self.calculate_uv_risk(
                item['weather'][0]['main'],
                item['clouds']['all'],
                dt.hour
            )
            
            hourly_data.append({
                'datetime': dt,
                'hour': dt.strftime('%H:%M'),
                'day': dt.strftime('%a'),
                'temp': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'wind_speed': item['wind']['speed'],
                'wind_direction': item['wind'].get('deg', 0),
                'wind_gust': item['wind'].get('gust', item['wind']['speed']),
                'weather': item['weather'][0]['main'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon'],
                'clouds': item['clouds']['all'],
                'visibility': item.get('visibility', 10000),
                'pop': item.get('pop', 0) * 100,  # Probability of precipitation
                'rain': item.get('rain', {}).get('3h', 0),
                'snow': item.get('snow', {}).get('3h', 0),
                'comfort_score': comfort_index['score'],
                'comfort_level': comfort_index['level'],
                'uv_index': uv_risk['index'],
                'uv_level': uv_risk['level'],
                'dewpoint': self._calculate_dewpoint(item['main']['temp'], item['main']['humidity']),
                'apparent_temp': self._calculate_apparent_temperature(
                    item['main']['temp'], 
                    item['main']['humidity'], 
                    item['wind']['speed']
                )
            })
        
        return hourly_data
    
    def _calculate_dewpoint(self, temp: float, humidity: float) -> float:
        """Calculate dewpoint temperature"""
        # Magnus formula for dewpoint
        a = 17.27
        b = 237.7
        
        alpha = ((a * temp) / (b + temp)) + np.log(humidity / 100.0)
        dewpoint = (b * alpha) / (a - alpha)
        
        return round(dewpoint, 1)
    
    def _calculate_apparent_temperature(self, temp: float, humidity: float, wind_speed: float) -> float:
        """Calculate apparent temperature (feels like) with enhanced accuracy"""
        # Use heat index for warm conditions
        if temp >= 20:
            return self.calculate_comfort_index(temp, humidity, wind_speed)['heat_index']
        # Use wind chill for cold conditions
        elif temp <= 10 and wind_speed > 1:
            return self.calculate_comfort_index(temp, humidity, wind_speed)['wind_chill']
        # For moderate conditions, adjust slightly for humidity
        else:
            humidity_factor = (humidity - 50) / 100  # -0.5 to +0.5
            return temp + (humidity_factor * 2)
    
    def get_weather_alerts(self, current_weather: Dict, forecast_data: List[Dict]) -> List[Dict]:
        """Enhanced weather alert system with severity levels"""
        alerts = []
        
        if not current_weather:
            return alerts
        
        temp = current_weather['main']['temp']
        wind_speed = current_weather['wind']['speed']
        condition = current_weather['weather'][0]['main'].lower()
        pressure = current_weather['main']['pressure']
        humidity = current_weather['main']['humidity']
        
        # Critical temperature alerts
        if temp < -20:
            alerts.append({
                'type': 'critical',
                'severity': 'extreme',
                'title': 'EXTREME COLD WARNING',
                'message': 'Life-threatening cold! Frostbite can occur in minutes. Avoid outdoor exposure.',
                'icon': '🧊',
                'action': 'Stay indoors, ensure heating is working'
            })
        elif temp > 45:
            alerts.append({
                'type': 'critical',
                'severity': 'extreme',
                'title': 'EXTREME HEAT WARNING',
                'message': 'Dangerous heat levels! Heat stroke risk is very high.',
                'icon': '🔥',
                'action': 'Seek immediate air conditioning'
            })
        elif temp < -10:
            alerts.append({
                'type': 'warning',
                'severity': 'high',
                'title': 'Severe Cold Warning',
                'message': 'Extremely cold temperatures. Frostbite risk is high.',
                'icon': '🥶',
                'action': 'Dress in layers, limit outdoor time'
            })
        elif temp > 35:
            alerts.append({
                'type': 'warning',
                'severity': 'high',
                'title': 'Heat Warning',
                'message': 'Very hot temperatures. Heat exhaustion risk is elevated.',
                'icon': '🔥',
                'action': 'Stay hydrated, avoid sun exposure'
            })
        
        # Wind alerts with enhanced severity
        if wind_speed > 25:
            alerts.append({
                'type': 'critical',
                'severity': 'extreme',
                'title': 'SEVERE WIND WARNING',
                'message': 'Extremely dangerous winds! Avoid all outdoor activities.',
                'icon': '🌪️',
                'action': 'Stay indoors, secure all outdoor items'
            })
        elif wind_speed > 20:
            alerts.append({
                'type': 'warning',
                'severity': 'high',
                'title': 'High Wind Warning',
                'message': 'Very strong winds expected. Power outages possible.',
                'icon': '💨',
                'action': 'Secure loose objects, avoid driving'
            })
        elif wind_speed > 15:
            alerts.append({
                'type': 'caution',
                'severity': 'medium',
                'title': 'High Wind Advisory',
                'message': 'Strong winds expected. Secure loose objects.',
                'icon': '💨',
                'action': 'Be cautious with umbrellas'
            })
        
        # Pressure-based storm alerts
        if pressure < 980:
            alerts.append({
                'type': 'warning',
                'severity': 'high',
                'title': 'Severe Storm Alert',
                'message': 'Very low pressure indicates severe weather approaching.',
                'icon': '⛈️',
                'action': 'Monitor weather updates closely'
            })
        elif pressure < 1000:
            alerts.append({
                'type': 'caution',
                'severity': 'medium',
                'title': 'Storm Watch',
                'message': 'Low pressure system may bring unstable weather.',
                'icon': '🌧️',
                'action': 'Be prepared for weather changes'
            })
        
        # Enhanced weather condition alerts
        if 'thunderstorm' in condition:
            alerts.append({
                'type': 'warning',
                'severity': 'high',
                'title': 'Thunderstorm Alert',
                'message': 'Thunderstorms in the area. Lightning and heavy rain possible.',
                'icon': '⛈️',
                'action': 'Stay indoors, avoid water and high places'
            })
        elif 'tornado' in condition:
            alerts.append({
                'type': 'critical',
                'severity': 'extreme',
                'title': 'TORNADO WARNING',
                'message': 'Tornado conditions detected! Seek immediate shelter.',
                'icon': '🌪️',
                'action': 'Go to lowest floor, interior room'
            })
        elif 'snow' in condition:
            if wind_speed > 10:
                alerts.append({
                    'type': 'warning',
                    'severity': 'high',
                    'title': 'Blizzard Conditions',
                    'message': 'Heavy snow with strong winds. Travel extremely dangerous.',
                    'icon': '❄️',
                    'action': 'Avoid all travel if possible'
                })
            else:
                alerts.append({
                    'type': 'info',
                    'severity': 'low',
                    'title': 'Snow Conditions',
                    'message': 'Snowy weather. Drive carefully and dress warmly.',
                    'icon': '❄️',
                    'action': 'Use winter driving precautions'
                })
        elif 'fog' in condition:
            alerts.append({
                'type': 'caution',
                'severity': 'medium',
                'title': 'Dense Fog Advisory',
                'message': 'Visibility significantly reduced. Drive with extreme caution.',
                'icon': '🌫️',
                'action': 'Use fog lights, reduce speed'
            })
        
        # Air quality alerts (if humidity is very high, pollution may be trapped)
        if humidity > 95:
            alerts.append({
                'type': 'info',
                'severity': 'low',
                'title': 'Air Quality Notice',
                'message': 'Very high humidity may trap pollutants near ground level.',
                'icon': '🌫️',
                'action': 'Consider indoor activities'
            })
        
        # Forecast-based alerts
        if forecast_data:
            trends = self.calculate_weather_trends(forecast_data)
            
            # Heat wave alert
            if trends.get('temperature', {}).get('heat_wave_risk', 0) > 0.7:
                alerts.append({
                    'type': 'warning',
                    'severity': 'high',
                    'title': 'Heat Wave Warning',
                    'message': 'Extended period of dangerous heat approaching.',
                    'icon': '🔥',
                    'action': 'Prepare cooling strategies'
                })
            
            # Cold snap alert
            if trends.get('temperature', {}).get('cold_snap_risk', 0) > 0.7:
                alerts.append({
                    'type': 'warning',
                    'severity': 'high',
                    'title': 'Cold Snap Warning',
                    'message': 'Extended period of dangerous cold approaching.',
                    'icon': '🧊',
                    'action': 'Prepare heating and warm clothing'
                })
            
            # Storm system alert
            if trends.get('wind', {}).get('storm_risk', 0) > 0.6:
                alerts.append({
                    'type': 'caution',
                    'severity': 'medium',
                    'title': 'Storm System Approaching',
                    'message': 'Weather patterns indicate stormy conditions ahead.',
                    'icon': '⛈️',
                    'action': 'Monitor forecasts closely'
                })
        
        # Sort alerts by severity
        severity_order = {'extreme': 4, 'high': 3, 'medium': 2, 'low': 1}
        alerts.sort(key=lambda x: severity_order.get(x['severity'], 0), reverse=True)
        
        return alerts[:5]  # Limit to top 5 most severe alerts
    
    def calculate_uv_risk(self, weather_condition: str, cloud_cover: int, hour: int) -> Dict[str, Any]:
        """Enhanced UV index calculation with seasonal and location factors"""
        base_uv = 0
        
        # Enhanced time-based UV calculation
        if 6 <= hour <= 18:  # Extended daylight hours
            # Peak UV is around solar noon (12-14)
            if 11 <= hour <= 13:
                base_uv = 10
            elif 10 <= hour <= 14:
                base_uv = 8
            elif 9 <= hour <= 15:
                base_uv = 6
            elif 8 <= hour <= 16:
                base_uv = 4
            else:
                base_uv = 2
        else:
            base_uv = 0
        
        # Weather condition adjustments
        condition_lower = weather_condition.lower()
        if any(word in condition_lower for word in ['rain', 'storm', 'thunderstorm']):
            base_uv *= 0.2
        elif 'drizzle' in condition_lower:
            base_uv *= 0.4
        elif 'snow' in condition_lower:
            base_uv *= 1.2  # Snow reflection increases UV
        elif 'clear' in condition_lower:
            base_uv *= 1.1
        
        # Cloud cover adjustments
        if cloud_cover > 90:
            base_uv *= 0.3
        elif cloud_cover > 75:
            base_uv *= 0.5
        elif cloud_cover > 50:
            base_uv *= 0.7
        elif cloud_cover > 25:
            base_uv *= 0.85
        elif cloud_cover < 10:
            base_uv *= 1.05  # Clear skies boost UV
        
        # Ensure reasonable bounds
        base_uv = max(0, min(12, base_uv))
        
        # Enhanced UV Index categories with detailed recommendations
        if base_uv <= 2:
            risk_level = "Low"
            risk_color = "#4CAF50"
            recommendation = "No protection needed for normal skin"
            protection_time = "60+ minutes"
        elif base_uv <= 5:
            risk_level = "Moderate"
            risk_color = "#FFC107"
            recommendation = "SPF 15+ sunscreen, hat recommended"
            protection_time = "30-45 minutes"
        elif base_uv <= 7:
            risk_level = "High"
            risk_color = "#FF9800"
            recommendation = "SPF 30+ sunscreen, hat, sunglasses essential"
            protection_time = "15-25 minutes"
        elif base_uv <= 10:
            risk_level = "Very High"
            risk_color = "#F44336"
            recommendation = "SPF 50+ sunscreen, protective clothing, avoid midday sun"
            protection_time = "10-15 minutes"
        else:
            risk_level = "Extreme"
            risk_color = "#9C27B0"
            recommendation = "Avoid outdoor activities, SPF 50+, full protection"
            protection_time = "< 10 minutes"
        
        return {
            'index': round(base_uv, 1),
            'level': risk_level,
            'color': risk_color,
            'recommendation': recommendation,
            'protection_time': protection_time,
            'burn_time': self._calculate_burn_time(base_uv)
        }
    
    def _calculate_burn_time(self, uv_index: float) -> str:
        """Calculate approximate time to sunburn for different skin types"""
        # Base burn time for fair skin (Type I)
        base_times = {
            1: 30, 2: 25, 3: 20, 4: 15, 5: 12, 6: 10, 7: 8, 8: 6, 9: 5, 10: 4, 11: 3, 12: 2
        }
        
        uv_rounded = max(1, min(12, round(uv_index)))
        fair_skin_time = base_times.get(uv_rounded, 2)
        
        return f"Fair skin: ~{fair_skin_time}min, Dark skin: ~{fair_skin_time * 3}min"
    
    def create_weather_summary(self, current_weather: Dict, forecast_data: List[Dict]) -> Dict[str, Any]:
        """Enhanced comprehensive weather summary with AI insights"""
        if not current_weather:
            return {}
        
        # Basic current conditions
        temp = current_weather['main']['temp']
        condition = current_weather['weather'][0]['description'].title()
        
        # Advanced analytics
        comfort_index = self.calculate_comfort_index(
            current_weather['main']['temp'],
            current_weather['main']['humidity'],
            current_weather['wind']['speed']
        )
        
        recommendations = self.get_weather_recommendations(current_weather, forecast_data)
        alerts = self.get_weather_alerts(current_weather, forecast_data)
        
        summary = {
            'current_condition': condition,
            'temperature': temp,
            'feels_like': current_weather['main']['feels_like'],
            'comfort_index': comfort_index,
            'recommendations': recommendations,
            'alerts': alerts,
            'data_quality': self._assess_data_quality(current_weather, forecast_data),
            'last_updated': datetime.now().isoformat()
        }
        
        if forecast_data:
            trends = self.calculate_weather_trends(forecast_data)
            summary.update({
                'trends': trends,
                'outlook': self._generate_detailed_outlook(forecast_data, trends),
                'weekly_summary': self._generate_weekly_summary(forecast_data),
                'activity_recommendations': self._generate_activity_recommendations(current_weather, forecast_data)
            })
        
        return summary
    
    def _assess_data_quality(self, current_weather: Dict, forecast_data: List[Dict]) -> Dict[str, Any]:
        """Assess the quality and completeness of weather data"""
        quality_score = 100
        missing_fields = []
        data_age_hours = 0
        
        # Check current weather completeness
        required_fields = ['main', 'weather', 'wind', 'clouds', 'sys']
        for field in required_fields:
            if field not in current_weather:
                missing_fields.append(f"current.{field}")
                quality_score -= 10
        
        # Check forecast data completeness
        if not forecast_data:
            missing_fields.append("forecast_data")
            quality_score -= 30
        elif len(forecast_data) < 5:
            quality_score -= 15
        
        # Calculate data freshness
        if 'dt' in current_weather:
            data_time = datetime.fromtimestamp(current_weather['dt'])
            data_age_hours = (datetime.now() - data_time).total_seconds() / 3600
            
            if data_age_hours > 3:
                quality_score -= min(data_age_hours * 5, 30)
        
        return {
            'score': max(0, min(100, quality_score)),
            'missing_fields': missing_fields,
            'data_age_hours': round(data_age_hours, 1),
            'status': 'excellent' if quality_score >= 90 else 'good' if quality_score >= 70 else 'fair' if quality_score >= 50 else 'poor'
        }
    
    def _generate_detailed_outlook(self, forecast_data: List[Dict], trends: Dict) -> str:
        """Generate detailed weather outlook with AI insights"""
        if not forecast_data or len(forecast_data) < 2:
            return "Weather outlook unavailable due to insufficient forecast data"
        
        outlook_parts = []
        
        # Temperature outlook
        temp_trend = trends.get('temperature', {})
        if temp_trend.get('heat_wave_risk', 0) > 0.5:
            outlook_parts.append("approaching heat wave conditions")
        elif temp_trend.get('cold_snap_risk', 0) > 0.5:
            outlook_parts.append("incoming cold snap")
        elif temp_trend.get('max_trend') == 'increasing':
            outlook_parts.append("gradually warming temperatures")
        elif temp_trend.get('max_trend') == 'decreasing':
            outlook_parts.append("cooling trend developing")
        else:
            outlook_parts.append("stable temperature pattern")
        
        # Precipitation outlook
        precip_days = sum(1 for day in forecast_data if day.get('precipitation_chance', 0) > 30)
        if precip_days >= 4:
            outlook_parts.append("frequent precipitation expected")
        elif precip_days >= 2:
            outlook_parts.append("some wet weather likely")
        elif precip_days == 1:
            outlook_parts.append("mostly dry with isolated showers")
        else:
            outlook_parts.append("predominantly dry conditions")
        
        # Wind outlook
        wind_trend = trends.get('wind', {})
        if wind_trend.get('storm_risk', 0) > 0.6:
            outlook_parts.append("windy and potentially stormy")
        elif wind_trend.get('avg', 0) > 8:
            outlook_parts.append("breezy to windy conditions")
        else:
            outlook_parts.append("generally light winds")
        
        # Comfort outlook
        comfort_trend = trends.get('overall', {}).get('comfort_trend', 'stable')
        if comfort_trend == 'increasing':
            outlook_parts.append("improving comfort levels")
        elif comfort_trend == 'decreasing':
            outlook_parts.append("declining comfort conditions")
        
        # Best day recommendation
        best_day = trends.get('overall', {}).get('best_day', {})
        if best_day:
            best_date = best_day.get('date', datetime.now()).strftime('%A')
            outlook_parts.append(f"best conditions expected on {best_date}")
        
        return f"5-day outlook: {', '.join(outlook_parts[:4])}"
    
    def _generate_weekly_summary(self, forecast_data: List[Dict]) -> Dict[str, Any]:
        """Generate weekly weather summary statistics"""
        if not forecast_data:
            return {}
        
        temps_max = [item['temp_max'] for item in forecast_data]
        temps_min = [item['temp_min'] for item in forecast_data]
        humidity = [item['humidity'] for item in forecast_data]
        wind_speeds = [item['wind_speed'] for item in forecast_data]
        precip_chances = [item.get('precipitation_chance', 0) for item in forecast_data]
        
        return {
            'temperature': {
                'highest': max(temps_max),
                'lowest': min(temps_min),
                'average_high': sum(temps_max) / len(temps_max),
                'average_low': sum(temps_min) / len(temps_min),
                'range': max(temps_max) - min(temps_min)
            },
            'conditions': {
                'rainy_days': sum(1 for p in precip_chances if p > 50),
                'windy_days': sum(1 for w in wind_speeds if w > 8),
                'comfortable_days': sum(1 for item in forecast_data if item.get('comfort_score', 0) > 70),
                'average_humidity': sum(humidity) / len(humidity)
            },
            'extremes': {
                'hottest_day': max(forecast_data, key=lambda x: x['temp_max'])['date'].strftime('%A'),
                'coldest_day': min(forecast_data, key=lambda x: x['temp_min'])['date'].strftime('%A'),
                'windiest_day': max(forecast_data, key=lambda x: x['wind_speed'])['date'].strftime('%A'),
                'most_humid_day': max(forecast_data, key=lambda x: x['humidity'])['date'].strftime('%A')
            }
        }
    
    def _generate_activity_recommendations(self, current_weather: Dict, forecast_data: List[Dict]) -> Dict[str, List[str]]:
        """Generate activity recommendations based on weather conditions"""
        if not current_weather:
            return {}
        
        current_temp = current_weather['main']['temp']
        current_condition = current_weather['weather'][0]['main'].lower()
        current_wind = current_weather['wind']['speed']
        
        recommendations = {
            'outdoor_sports': [],
            'indoor_activities': [],
            'best_days': [],
            'avoid_days': []
        }
        
        # Current day recommendations
        if 'clear' in current_condition and 15 <= current_temp <= 28 and current_wind < 8:
            recommendations['outdoor_sports'].extend([
                "Perfect for hiking and walking",
                "Great conditions for cycling",
                "Ideal for outdoor photography",
                "Excellent for picnics and BBQ"
            ])
        elif 'rain' in current_condition or current_wind > 15:
            recommendations['indoor_activities'].extend([
                "Perfect day for museums and galleries",
                "Great time for indoor fitness",
                "Ideal for shopping and cafes",
                "Good for reading and relaxation"
            ])
        
        # Multi-day recommendations
        if forecast_data:
            for i, day in enumerate(forecast_data):
                day_name = day['date'].strftime('%A')
                comfort_score = day.get('comfort_score', 50)
                
                if comfort_score > 80:
                    recommendations['best_days'].append(f"{day_name}: {day['description']} - Perfect for all outdoor activities")
                elif comfort_score < 40:
                    recommendations['avoid_days'].append(f"{day_name}: {day['description']} - Better to stay indoors")
        
        return recommendations
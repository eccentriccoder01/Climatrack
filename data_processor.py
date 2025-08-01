import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import numpy as np

class DataProcessor:
    """Handles weather data processing and analysis"""
    
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
    
    def process_forecast_data(self, forecast_data: Dict, units: str = 'metric') -> List[Dict]:
        """Process 5-day forecast data into daily summaries"""
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
                    'weather_conditions': [],
                    'icons': [],
                    'descriptions': []
                }
            
            daily_data[date_key]['temps'].append(item['main']['temp'])
            daily_data[date_key]['humidity'].append(item['main']['humidity'])
            daily_data[date_key]['wind_speed'].append(item['wind']['speed'])
            daily_data[date_key]['weather_conditions'].append(item['weather'][0]['main'])
            daily_data[date_key]['icons'].append(item['weather'][0]['icon'])
            daily_data[date_key]['descriptions'].append(item['weather'][0]['description'])
        
        # Process daily summaries
        processed_forecast = []
        for date_key, data in daily_data.items():
            # Get most common weather condition and icon
            most_common_condition = max(set(data['weather_conditions']), 
                                      key=data['weather_conditions'].count)
            most_common_icon = max(set(data['icons']), key=data['icons'].count)
            most_common_desc = max(set(data['descriptions']), key=data['descriptions'].count)
            
            processed_forecast.append({
                'date': data['date'],
                'day': data['day'][:3],  # Short day name
                'temp_max': max(data['temps']),
                'temp_min': min(data['temps']),
                'temp_avg': sum(data['temps']) / len(data['temps']),
                'humidity': sum(data['humidity']) / len(data['humidity']),
                'wind_speed': sum(data['wind_speed']) / len(data['wind_speed']),
                'condition': most_common_condition,
                'icon': most_common_icon,
                'description': most_common_desc
            })
        
        return sorted(processed_forecast, key=lambda x: x['date'])[:5]
    
    def calculate_weather_trends(self, forecast_data: List[Dict]) -> Dict[str, Any]:
        """Calculate weather trends from forecast data"""
        if not forecast_data:
            return {}
        
        temps_max = [item['temp_max'] for item in forecast_data]
        temps_min = [item['temp_min'] for item in forecast_data]
        humidity = [item['humidity'] for item in forecast_data]
        wind_speed = [item['wind_speed'] for item in forecast_data]
        
        trends = {
            'temperature': {
                'max_trend': self._calculate_trend(temps_max),
                'min_trend': self._calculate_trend(temps_min),
                'max_change': max(temps_max) - min(temps_max),
                'min_change': max(temps_min) - min(temps_min)
            },
            'humidity': {
                'trend': self._calculate_trend(humidity),
                'avg': sum(humidity) / len(humidity),
                'change': max(humidity) - min(humidity)
            },
            'wind': {
                'trend': self._calculate_trend(wind_speed),
                'avg': sum(wind_speed) / len(wind_speed),
                'max': max(wind_speed)
            }
        }
        
        return trends
    
    def _calculate_trend(self, data: List[float]) -> str:
        """Calculate trend direction from data series"""
        if len(data) < 2:
            return 'stable'
        
        # Simple linear regression slope
        x = list(range(len(data)))
        n = len(data)
        
        slope = (n * sum(x[i] * data[i] for i in range(n)) - sum(x) * sum(data)) / (n * sum(x[i]**2 for i in range(n)) - sum(x)**2)
        
        if slope > 0.5:
            return 'increasing'
        elif slope < -0.5:
            return 'decreasing'
        else:
            return 'stable'
    
    def get_weather_recommendations(self, current_weather: Dict, forecast_data: List[Dict]) -> List[str]:
        """Generate weather-based recommendations"""
        recommendations = []
        
        if not current_weather:
            return recommendations
        
        temp = current_weather['main']['temp']
        humidity = current_weather['main']['humidity']
        wind_speed = current_weather['wind']['speed']
        condition = current_weather['weather'][0]['main'].lower()
        
        # Temperature-based recommendations
        if temp < 0:
            recommendations.append("🧥 Bundle up! It's freezing outside. Wear layers and protect exposed skin.")
        elif temp < 10:
            recommendations.append("🧣 It's quite cold. A warm jacket and scarf are recommended.")
        elif temp > 30:
            recommendations.append("☀️ It's hot outside! Stay hydrated and wear light, breathable clothing.")
        elif temp > 25:
            recommendations.append("🌤️ Perfect weather for outdoor activities! Light clothing recommended.")
        
        # Humidity-based recommendations
        if humidity > 80:
            recommendations.append("💧 High humidity today. You might feel sticky - stay in air-conditioned areas when possible.")
        elif humidity < 30:
            recommendations.append("🏜️ Low humidity - remember to moisturize and stay hydrated.")
        
        # Wind-based recommendations
        if wind_speed > 10:
            recommendations.append("💨 It's quite windy. Secure loose items and be careful with umbrellas.")
        
        # Weather condition recommendations
        if 'rain' in condition:
            recommendations.append("🌧️ Rain expected! Don't forget your umbrella or raincoat.")
        elif 'snow' in condition:
            recommendations.append("❄️ Snow conditions - drive carefully and wear appropriate footwear.")
        elif 'clear' in condition and temp > 20:
            recommendations.append("🌞 Beautiful clear weather! Great day for outdoor activities.")
        elif 'cloud' in condition:
            recommendations.append("☁️ Cloudy skies - no need for sunscreen, but pleasant weather overall.")
        
        # Forecast-based recommendations
        if forecast_data:
            trends = self.calculate_weather_trends(forecast_data)
            
            if trends.get('temperature', {}).get('max_trend') == 'decreasing':
                recommendations.append("📉 Temperature dropping over the next few days - prepare warmer clothes.")
            elif trends.get('temperature', {}).get('max_trend') == 'increasing':
                recommendations.append("📈 Getting warmer! You might want lighter clothing for the coming days.")
        
        return recommendations[:4]  # Limit to 4 recommendations
    
    def calculate_comfort_index(self, temp: float, humidity: float, wind_speed: float) -> Dict[str, Any]:
        """Calculate weather comfort index"""
        # Heat Index calculation (simplified)
        if temp >= 20:  # Only calculate for warm weather
            heat_index = temp + (0.5555 * (6.11 * np.exp(5417.7530 * ((1/273.16) - (1/(temp + 273.16)))) - 10))
        else:
            heat_index = temp
        
        # Wind Chill calculation (for cold weather)
        if temp <= 10 and wind_speed > 1.34:
            wind_chill = 13.12 + 0.6215 * temp - 11.37 * (wind_speed * 3.6)**0.16 + 0.3965 * temp * (wind_speed * 3.6)**0.16
        else:
            wind_chill = temp
        
        # Comfort assessment
        comfort_score = 100
        
        # Temperature comfort (optimal range: 18-24°C)
        if temp < 18:
            comfort_score -= (18 - temp) * 5
        elif temp > 24:
            comfort_score -= (temp - 24) * 3
        
        # Humidity comfort (optimal range: 40-60%)
        if humidity < 40:
            comfort_score -= (40 - humidity) * 0.5
        elif humidity > 60:
            comfort_score -= (humidity - 60) * 0.8
        
        # Wind comfort (optimal: < 5 m/s)
        if wind_speed > 5:
            comfort_score -= (wind_speed - 5) * 3
        
        comfort_score = max(0, min(100, comfort_score))
        
        # Comfort level
        if comfort_score >= 80:
            comfort_level = "Excellent"
            comfort_color = "#4CAF50"
        elif comfort_score >= 60:
            comfort_level = "Good"
            comfort_color = "#8BC34A"
        elif comfort_score >= 40:
            comfort_level = "Fair"
            comfort_color = "#FFC107"
        elif comfort_score >= 20:
            comfort_level = "Poor"
            comfort_color = "#FF9800"
        else:
            comfort_level = "Very Poor"
            comfort_color = "#F44336"
        
        return {
            'score': comfort_score,
            'level': comfort_level,
            'color': comfort_color,
            'heat_index': heat_index,
            'wind_chill': wind_chill
        }
    
    def process_hourly_data(self, forecast_data: Dict) -> List[Dict]:
        """Process hourly forecast data for detailed analysis"""
        if not forecast_data or 'list' not in forecast_data:
            return []
        
        hourly_data = []
        current_date = datetime.now().date()
        
        for item in forecast_data['list'][:24]:  # Next 24 hours
            dt = datetime.fromtimestamp(item['dt'])
            
            # Skip past hours for today
            if dt.date() == current_date and dt.hour < datetime.now().hour:
                continue
            
            hourly_data.append({
                'datetime': dt,
                'hour': dt.strftime('%H:%M'),
                'temp': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'wind_speed': item['wind']['speed'],
                'wind_direction': item['wind'].get('deg', 0),
                'weather': item['weather'][0]['main'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon'],
                'clouds': item['clouds']['all'],
                'pop': item.get('pop', 0) * 100,  # Probability of precipitation
                'rain': item.get('rain', {}).get('3h', 0),
                'snow': item.get('snow', {}).get('3h', 0)
            })
        
        return hourly_data
    
    def get_weather_alerts(self, current_weather: Dict, forecast_data: List[Dict]) -> List[Dict]:
        """Generate weather alerts based on conditions"""
        alerts = []
        
        if not current_weather:
            return alerts
        
        temp = current_weather['main']['temp']
        wind_speed = current_weather['wind']['speed']
        condition = current_weather['weather'][0]['main'].lower()
        
        # Temperature alerts
        if temp < -10:
            alerts.append({
                'type': 'warning',
                'title': 'Extreme Cold Warning',
                'message': 'Extremely cold temperatures. Frostbite risk is high.',
                'icon': '🥶'
            })
        elif temp > 35:
            alerts.append({
                'type': 'warning',
                'title': 'Heat Warning',
                'message': 'Very hot temperatures. Heat exhaustion risk is elevated.',
                'icon': '🔥'
            })
        
        # Wind alerts
        if wind_speed > 15:
            alerts.append({
                'type': 'caution',
                'title': 'High Wind Advisory',
                'message': 'Strong winds expected. Secure loose objects.',
                'icon': '💨'
            })
        
        # Weather condition alerts
        if 'thunderstorm' in condition:
            alerts.append({
                'type': 'warning',
                'title': 'Thunderstorm Alert',
                'message': 'Thunderstorms in the area. Stay indoors if possible.',
                'icon': '⛈️'
            })
        elif 'snow' in condition:
            alerts.append({
                'type': 'info',
                'title': 'Snow Conditions',
                'message': 'Snowy weather. Drive carefully and dress warmly.',
                'icon': '❄️'
            })
        
        return alerts
    
    def format_wind_direction(self, degrees: float) -> str:
        """Convert wind direction degrees to compass direction"""
        directions = [
            "N", "NNE", "NE", "ENE",
            "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW",
            "W", "WNW", "NW", "NNW"
        ]
        
        index = round(degrees / 22.5) % 16
        return directions[index]
    
    def calculate_uv_risk(self, weather_condition: str, cloud_cover: int, hour: int) -> Dict[str, Any]:
        """Calculate UV risk level (simplified estimation)"""
        # This is a simplified UV index calculation
        # In production, you'd want to use a proper UV API
        
        base_uv = 0
        
        # Time-based UV (peak around noon)
        if 10 <= hour <= 14:
            base_uv = 8
        elif 9 <= hour <= 15:
            base_uv = 6
        elif 8 <= hour <= 16:
            base_uv = 4
        elif 7 <= hour <= 17:
            base_uv = 2
        else:
            base_uv = 0
        
        # Adjust for weather conditions
        if 'rain' in weather_condition.lower() or 'storm' in weather_condition.lower():
            base_uv *= 0.3
        elif cloud_cover > 75:
            base_uv *= 0.5
        elif cloud_cover > 50:
            base_uv *= 0.7
        elif cloud_cover > 25:
            base_uv *= 0.9
        
        # UV Index categories
        if base_uv <= 2:
            risk_level = "Low"
            risk_color = "#4CAF50"
            recommendation = "No protection needed"
        elif base_uv <= 5:
            risk_level = "Moderate"
            risk_color = "#FFC107"
            recommendation = "Wear sunscreen if outdoors"
        elif base_uv <= 7:
            risk_level = "High"
            risk_color = "#FF9800"
            recommendation = "Sunscreen and hat recommended"
        elif base_uv <= 10:
            risk_level = "Very High"
            risk_color = "#F44336"
            recommendation = "Avoid sun exposure 10AM-4PM"
        else:
            risk_level = "Extreme"
            risk_color = "#9C27B0"
            recommendation = "Avoid outdoor activities"
        
        return {
            'index': round(base_uv, 1),
            'level': risk_level,
            'color': risk_color,
            'recommendation': recommendation
        }
    
    def create_weather_summary(self, current_weather: Dict, forecast_data: List[Dict]) -> Dict[str, Any]:
        """Create a comprehensive weather summary"""
        if not current_weather:
            return {}
        
        summary = {
            'current_condition': current_weather['weather'][0]['description'].title(),
            'temperature': current_weather['main']['temp'],
            'feels_like': current_weather['main']['feels_like'],
            'recommendations': self.get_weather_recommendations(current_weather, forecast_data),
            'alerts': self.get_weather_alerts(current_weather, forecast_data),
            'comfort_index': self.calculate_comfort_index(
                current_weather['main']['temp'],
                current_weather['main']['humidity'],
                current_weather['wind']['speed']
            )
        }
        
        if forecast_data:
            summary['trends'] = self.calculate_weather_trends(forecast_data)
            summary['outlook'] = self._generate_outlook(forecast_data)
        
        return summary
    
    def _generate_outlook(self, forecast_data: List[Dict]) -> str:
        """Generate weather outlook text"""
        if not forecast_data or len(forecast_data) < 2:
            return "Weather outlook unavailable"
        
        trends = self.calculate_weather_trends(forecast_data)
        temp_trend = trends.get('temperature', {}).get('max_trend', 'stable')
        
        outlook_parts = []
        
        if temp_trend == 'increasing':
            outlook_parts.append("temperatures rising")
        elif temp_trend == 'decreasing':
            outlook_parts.append("cooling trend")
        else:
            outlook_parts.append("stable temperatures")
        
        # Check for precipitation in forecast
        rain_days = sum(1 for day in forecast_data if 'rain' in day.get('condition', '').lower())
        if rain_days > 2:
            outlook_parts.append("rainy conditions expected")
        elif rain_days > 0:
            outlook_parts.append("some rain possible")
        
        return f"Next few days: {', '.join(outlook_parts)}"
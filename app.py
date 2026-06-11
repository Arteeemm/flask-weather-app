from flask import Flask, render_template_string
import requests
import json
from datetime import datetime

app = Flask(__name__)

def get_weather_data():
    try:
        # Получаем данные в JSON формате
        response = requests.get('https://wttr.in/Зеленоград?format=j1&lang=ru')
        if response.status_code == 200:
            data = response.json()
            
            # Извлекаем нужные данные
            current = data['current_condition'][0]
            weather_info = {
                'temperature': current['temp_C'],
                'feels_like': current['FeelsLikeC'],
                'humidity': current['humidity'],
                'wind_speed': current['windspeedKmph'],
                'wind_dir': current['winddir16Point'],
                'pressure': current['pressure'],
                'clouds': current['cloudcover'],
                'weather_desc': current['lang_ru'][0]['value'],
                'uv_index': current['uvIndex'],
                'visibility': current['visibility'],
            }
            return weather_info
        else:
            return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def get_wind_direction_arrow(dir_ru):
    """Преобразует направление ветра в стрелку"""
    arrows = {
        'С': '⬆️', 'СВ': '↗️', 'В': '➡️', 'ЮВ': '↘️',
        'Ю': '⬇️', 'ЮЗ': '↙️', 'З': '⬅️', 'СЗ': '↖️'
    }
    return arrows.get(dir_ru, '➡️')

@app.route('/')
def weather():
    weather = get_weather_data()
    
    # HTML шаблон с красивым дизайном
    html_template = '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Погода в Зеленограде</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .weather-card {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 30px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                padding: 40px;
                max-width: 500px;
                width: 100%;
                transition: transform 0.3s ease;
            }
            
            .weather-card:hover {
                transform: translateY(-5px);
            }
            
            .city {
                text-align: center;
                font-size: 32px;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }
            
            .date {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
                font-size: 14px;
            }
            
            .temperature {
                text-align: center;
                margin-bottom: 30px;
            }
            
            .temp-value {
                font-size: 72px;
                font-weight: bold;
                color: #667eea;
            }
            
            .temp-unit {
                font-size: 36px;
                color: #666;
            }
            
            .weather-desc {
                text-align: center;
                font-size: 20px;
                color: #555;
                margin-top: -20px;
                margin-bottom: 30px;
            }
            
            .details {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .detail-item {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 15px;
                text-align: center;
                transition: all 0.3s ease;
            }
            
            .detail-item:hover {
                background: #e9ecef;
                transform: scale(1.05);
            }
            
            .detail-label {
                font-size: 12px;
                color: #888;
                margin-bottom: 5px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .detail-value {
                font-size: 20px;
                font-weight: bold;
                color: #333;
            }
            
            .detail-unit {
                font-size: 12px;
                color: #888;
            }
            
            .feels-like {
                text-align: center;
                padding-top: 20px;
                border-top: 1px solid #e0e0e0;
                color: #666;
                font-size: 14px;
            }
            
            .error-message {
                text-align: center;
                color: #e74c3c;
                padding: 40px;
                font-size: 18px;
            }
            
            @media (max-width: 480px) {
                .weather-card {
                    padding: 25px;
                }
                
                .temp-value {
                    font-size: 56px;
                }
                
                .details {
                    gap: 15px;
                }
                
                .detail-value {
                    font-size: 16px;
                }
            }
        </style>
    </head>
    <body>
        <div class="weather-card">
            {% if weather %}
                <div class="city">
                    🌍 Зеленоград
                </div>
                <div class="date">
                    {{ date }}
                </div>
                
                <div class="temperature">
                    <span class="temp-value">{{ weather.temperature }}</span>
                    <span class="temp-unit">°C</span>
                </div>
                
                <div class="weather-desc">
                    {{ weather.weather_desc }}
                </div>
                
                <div class="details">
                    <div class="detail-item">
                        <div class="detail-label">🌡️ Ощущается как</div>
                        <div class="detail-value">{{ weather.feels_like }}<span class="detail-unit">°C</span></div>
                    </div>
                    
                    <div class="detail-item">
                        <div class="detail-label">💧 Влажность</div>
                        <div class="detail-value">{{ weather.humidity }}<span class="detail-unit">%</span></div>
                    </div>
                    
                    <div class="detail-item">
                        <div class="detail-label">💨 Ветер</div>
                        <div class="detail-value">{{ weather.wind_speed }}<span class="detail-unit"> км/ч</span></div>
                        <div class="detail-label" style="font-size: 16px; margin-top: 5px;">{{ wind_arrow }} {{ weather.wind_dir }}</div>
                    </div>
                    
                    <div class="detail-item">
                        <div class="detail-label">☁️ Облачность</div>
                        <div class="detail-value">{{ weather.clouds }}<span class="detail-unit">%</span></div>
                    </div>
                    
                    <div class="detail-item">
                        <div class="detail-label">🔆 УФ-индекс</div>
                        <div class="detail-value">{{ weather.uv_index }}</div>
                    </div>
                    
                    <div class="detail-item">
                        <div class="detail-label">👁️ Видимость</div>
                        <div class="detail-value">{{ weather.visibility }}<span class="detail-unit"> км</span></div>
                    </div>
                </div>
                
                <div class="feels-like">
                    📊 Атмосферное давление: {{ weather.pressure }} гПа
                </div>
            {% else %}
                <div class="error-message">
                    😔 Извините, не удалось получить данные о погоде.<br>
                    Попробуйте обновить страницу позже.
                </div>
            {% endif %}
        </div>
    </body>
    </html>
    '''
    
    if weather:
        wind_arrow = get_wind_direction_arrow(weather['wind_dir'])
        current_date = datetime.now().strftime("%d %B %Y, %H:%M")
        return render_template_string(html_template, weather=weather, date=current_date, wind_arrow=wind_arrow)
    else:
        return render_template_string(html_template, weather=None, date="")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
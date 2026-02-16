from flask import Flask
import requests
import json

app = Flask(__name__)

def get_temperature():
    try:
        response = requests.get('https://wttr.in/Зеленоград?format=%t&lang=ru')
        if response.status_code == 200:
            return response.text.strip()
        else:
            return "Не удалось получить температуру"
    except:
        return "Ошибка получения данных"

@app.route('/')
def weather():
    temp = get_temperature()
    return f'Температура в Зеленограде: {temp}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

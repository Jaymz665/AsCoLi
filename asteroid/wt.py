import pyowm

def get_forecast_data(api_key, city_name):
    # Создаем объект OWM
    owm = pyowm.OWM(api_key)

    # Получаем менеджер погодных данных
    mgr = owm.weather_manager()

    # Получаем прогноз погоды на 5 дней с интервалами в 3 часа
    forecast = mgr.forecast_at_place(city_name, '3h')

    # Создаём словарь для хранения данных по дням
    temperatures_by_day = {}
    codes_by_day = {}

    # Проходим по всем прогнозам
    for weather in forecast.forecast.weathers:
        date = weather.reference_time('date').strftime('%Y-%m-%d')  # Берём только дату без времени
        temp_kelvin = weather.temperature('kelvin')['temp']
        code = weather.weather_code
        
        if date not in temperatures_by_day:
            temperatures_by_day[date] = []
            codes_by_day[date] = code  # Сохраняем первый попавшийся код погоды для данного дня
            
        temperatures_by_day[date].append(temp_kelvin)

    # Формируем итоговые данные
    weather_ids = []
    min_temp = []
    max_temp = []

    for date, temps in temperatures_by_day.items():
        min_temp.append(min(temps))  # Минимальная температура
        max_temp.append(max(temps))  # Максимальная температура
        weather_ids.append(codes_by_day[date])  # Код погоды

    # Ограничиваем длину списков до 5 элементов
    weather_ids = weather_ids[:5]
    min_temp = min_temp[:5]
    max_temp = max_temp[:5]

    return weather_ids, min_temp, max_temp

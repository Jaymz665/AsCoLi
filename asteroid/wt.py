import pyowm

def get_forecast_data(api_key, city_name):
    # Создаем объект OWM
    owm = pyowm.OWM(api_key)

    # Получаем менеджер погодных данных
    mgr = owm.weather_manager()

    # Получаем прогноз погоды на 5 дней с интервалами в 3 часа
    forecast = mgr.forecast_at_place(city_name, '3h')

    # Создаём списки для хранения данных
    max_temp = []
    min_temp = []
    weather_ids = []

    # Количество прогнозов
    total_weathers = len(forecast.forecast.weathers)

    # Проходим по каждому дню
    for i in range(min(total_weathers // 8, 5)):
        day_index_start = i * 8  # Начало дня
        day_index_end = (i + 1) * 8  # Конец дня
        
        # Определяем минимальный и максимальный индекс для данного дня
        start_index = max(day_index_start, 0)
        end_index = min(day_index_end, total_weathers)
        
        # Находим минимальную и максимальную температуру за данный день
        day_temps = [forecast.forecast.weathers[j].temperature('kelvin')['temp'] for j in range(start_index, end_index)]
        min_temp.append(min(day_temps))
        
        if i == 0:
            # Для первого дня сохраняем ближайшую температуру
            max_temp.append(day_temps[0])
        else:
            # Для остальных дней сохраняем максимальную температуру
            max_temp.append(max(day_temps))

        # Сохраняем идентификатор погоды для первого прогноза дня
        weather_ids.append(forecast.forecast.weathers[start_index].weather_code)

    # Убедимся, что длины списков совпадают
    length = min(len(weather_ids), len(min_temp), len(max_temp))

    # Возвращаем срезы списков до минимальной длины
    return weather_ids[:length], min_temp[:length], max_temp[:length]

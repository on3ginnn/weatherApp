from geopy.geocoders import Nominatim
import requests
import geocoder
import datetime
import pymorphy2



# класс для получения данных о погоде
class Weather:
    # функция для получения КООРДИНАТ используя НАЗВАНИЕ места
    def weather_get_location_by_address(self, address, app):
        try:
            out = app.geocode(address, language='ru').raw
        except Exception:
            out = False
        return out

    # функция для получения НАЗВАНИЯ используя КООРДИНАТЫ места
    def weather_get_address_by_location(self, latitude, longitude, app):
        coordinates = f"{latitude}, {longitude}"
        try:
            out = app.reverse(coordinates, language='ru').raw
        except Exception:
            out = False
        return out

    # главная функция получения данных о погоде
    def weather_main(self, address):
        # получение координат местонахождения пользователя, нужно в случае, если:
        # 1) название места не указано
        # 2) название места указано с ошибкой, которую не может исправить прогрмма(некоторые ошибки типа "мАсква" и тд,
        # исправляются автоматически)
        # 3) при 1 запуске программы
        default_location = geocoder.ip('me')
        lat = default_location.lat
        lon = default_location.lng
        app = Nominatim(user_agent="tutorial")
        if address:
            # исправление незначительных ошибок программы + постановка в начальную форму
            morph = pymorphy2.MorphAnalyzer()
            morph_address = morph.parse(address)[0]
            address = morph_address.normal_form
            location = self.weather_get_location_by_address(address, app)

            # в некоторых случаях попытка исправления незначительных ошибок не помогает, например при вводе
            # "нижней-мактамы"
            if not location:
                raise TypeError('Ничего не нашлось...')
            lat = location["lat"]
            lon = location["lon"]
            location = self.weather_get_address_by_location(lat, lon, app)
            if address.lower() != location['address']['country'].lower():
                keys = ['village', 'city', 'town', 'state']
                for i in keys:
                    if i in location['address']:
                        address = location['address'][i]
                        break
        else:
            location = self.weather_get_address_by_location(lat, lon, app)
            # получение названия поселка, города или штата
            keys = ['city', 'town', 'state']
            for i in keys:
                if i in location['address']:
                    address = location['address'][i]
                    break
        country = location['address']['country']
        # вывод города и страны, если нет города, только страны
        title_out = [address.title(), country.title()] if address.title() != country.title() else [country.title(), '']
        # получение дынных погоды по указанным координатам
        res = self.weather_data(lat, lon)
        return [title_out, res]

    # функция получения погоды
    def weather_data(self, lat, lon):
        weather_weekday_data = []

        url_day = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}" \
                  f"&units=metric&lang=ru&appid=b5e73057220b0f8b81885c7f33d11160"
        url_week = f"http://api.openweathermap.org/data/2.5/onecall?enclude=daily&lat={lat}&lon={lon}" \
                   f"&units=metric&lang=ru&appid=b5e73057220b0f8b81885c7f33d11160"

        dt = ''

        # получения дыных о погоде на сегодняшний день
        def today(url_day):
            global dt
            wind_degs = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ']
            weekday_lst = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресение']
            # получение данных о погоде с сервиса OpenWeatherMap
            responce = requests.get(url_day).json()
            # получение часового пояса указанного места
            dt = datetime.datetime.now(datetime.timezone(datetime.timedelta(seconds=int(responce['timezone']))))
            # вычисление напрваления ветра
            wind_deg = responce['wind']['deg'] / 45
            if wind_deg > int(wind_deg) + 0.5:
                wind_deg += 1
            wind_deg %= 8

            wind_speed = f'{responce["wind"]["speed"]} м/с'
            wind_deg = wind_degs[int(wind_deg)]
            # для установки иконки погоды (дневной)
            img_id = responce['weather'][0]['icon'][:-1:1]
            img_id += 'd'
            res = {
                'temp': str(int(responce['main']['temp'])),
                'lat': round(responce['coord']['lat'], 3),
                'lon': round(responce['coord']['lon'], 3),
                'description': responce['weather'][0]['description'],
                'feels_temp': str(int(responce['main']['feels_like'])),
                'press': str(round(responce['main']['pressure'] / 1000 * 750, 2)),
                'wind': {'wind_speed': wind_speed, 'wind_deg': wind_deg},
                'img_id': img_id,
                'time_timezone_now': f'{str(dt.hour).rjust(2, "0")}:{str(dt.minute).rjust(2, "0")}',
                'time_timezone_now_weekday': weekday_lst[dt.weekday()],
                'time_timezone_now_day': '.'.join(str(dt.date()).split('-'))
            }
            # возврат данных обернут в список для того, чтобы впоследствии не использовать метод append (слишком долго)
            return [res]

        # получения дыных о погоде на неделю (+6 дней)
        def week(url_week):
            global dt
            weekday_lst = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
            weather_weekday_data_lst = []
            req = requests.get(url_week).json()
            for i in range(1, 7):
                img_id = req['daily'][i]['weather'][0]['icon'][:-1:1]
                img_id += 'd'
                today_week = dt + datetime.timedelta(days=i)
                res = {
                    'temp': str(int(req['daily'][i]['temp']['day'])),
                    'description': req['daily'][i]['weather'][0]['description'],
                    'img_id': img_id,
                    'time_timezone_now_weekday': weekday_lst[today_week.weekday()],
                    'time_timezone_now_day': '.'.join(str(today_week.date()).split('-')),
                }
                weather_weekday_data_lst += [res]
            return weather_weekday_data_lst
        # складываем данные обернутые в список
        weather_weekday_data = today(url_day) + week(url_week)

        return weather_weekday_data


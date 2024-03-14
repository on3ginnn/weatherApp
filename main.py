#!/usr/bin/python3
#-*- coding: utf-8 -*-
'''
пакеты библиотек

pip install PyQt5
pip install requests
pip install geopy
pip install geocoder
pip install pymorphy2
pip install -U pymorphy2-dicts-ru
pip install pytz
pip install timezonefinder
'''

from weather_view import Ui_MainWindow
import sys
from weather import Weather
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap


class MainFunc(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.work = False
        self.alert_text = ['Наведите мышкой на описание погоды', 'rgba(80, 200, 120, 0.7)']
        # создание экземпляра класса Weather()
        self.out = Weather()
        self.setupUi(self)
        self.weather_data = self.repeat_weather_main()
        # изменение данных о погоде на виджете
        self.setData()

        # кнопка поиска погоды введенной местности
        self.address_btn.clicked.connect(self.change_address)

    def repeat_weather_main(self, address=False):
        try:
            out = self.out.weather_main(address)
            self.alert_text = ['Наведите мышкой на описание погоды', 'rgba(80, 200, 120, 0.7)']
            return out
        except TypeError as out_text:
            out = self.out.weather_main(False)
            self.alert_text = [out_text, 'rgba(255, 102, 112, 0.9)']
            return out
        except Exception as out_text:
            out = self.out.weather_main(False)
            self.alert_text = [out_text, 'rgba(255, 102, 112, 0.9)']
            return out

    def change_address(self):
        # проверка, чтобы во время поиска погоды нельзя было начать искать новую погоду
        if self.work == False:
            self.work = True
            address = self.address_input.text()
            self.address_input.clear()
            # отправление содержимого поля для ввода в функцию для получения данных о погоде
            self.weather_data = self.repeat_weather_main(address)
            self.setData()
            self.work = False

    def setData(self):
        # Замена данных о погоде на виджете
        self.alert.setStyleSheet(f"background: {self.alert_text[1]};\n"
                                 "border-radius: 15px;\n"
                                 "color: rgba(255, 255, 255, 0.9);\n"
                                 "padding: 0 10px;")

        self.alert.setText(str(self.alert_text[0]))
        self.alert.setToolTip(str(self.alert_text[0]))

        self.weather_title_address.setText(self.weather_data[0][0])
        self.weather_title_address.setToolTip(self.weather_data[0][0])

        self.weather_title_address_country.setText(self.weather_data[0][1])
        self.weather_title_address_country.setToolTip(self.weather_data[0][1])


        day_0 = self.weather_data[-1][0]
        self.weather_0_temp_value.setText(day_0['temp'])
        self.weather_0_description_img.setPixmap(QPixmap(f"weather_img/{day_0['img_id']}.png"))
        self.weather_0_description_text.setText(day_0['description'])
        self.weather_0_description_text.setToolTip(day_0['description'])
        self.weather_0_date_weekday.setText(day_0['time_timezone_now_weekday'])
        self.weather_0_date_date.setText(day_0['time_timezone_now_day'])
        self.weather_0_time.setText(day_0['time_timezone_now'])
        self.weather_0_wind_deg.setText(day_0['wind']['wind_deg'])
        self.weather_0_wind_speed.setText(day_0['wind']['wind_speed'])
        self.weather_0_coords_lat.setText(f'Широта: {day_0["lat"]}')
        self.weather_0_coords_lon.setText(f'Долгота: {day_0["lon"]}')
        self.weather_0_press_value.setText(f"{day_0['press']} мм рт. ст")

        day_1 = self.weather_data[-1][1]
        self.weather_1_date.setText(f"{day_1['time_timezone_now_weekday']}, {day_1['time_timezone_now_day']}")
        self.weather_1_date.setToolTip(f"{day_1['time_timezone_now_weekday']}, {day_1['time_timezone_now_day']}")
        self.weather_1_desc_img.setPixmap(QPixmap(f"weather_img/{day_1['img_id']}.png"))
        self.weather_1_desc_text.setText(day_1['description'])
        self.weather_1_desc_text.setToolTip(day_1['description'])
        self.weather_1_temp_value.setText(day_1['temp'])

        day_2 = self.weather_data[-1][2]
        self.weather_2_date.setText(f"{day_2['time_timezone_now_weekday']}, {day_2['time_timezone_now_day']}")
        self.weather_2_date.setToolTip(f"{day_2['time_timezone_now_weekday']}, {day_2['time_timezone_now_day']}")
        self.weather_2_desc_img.setPixmap(QPixmap(f"weather_img/{day_2['img_id']}.png"))
        self.weather_2_desc_text.setText(day_2['description'])
        self.weather_2_desc_text.setToolTip(day_2['description'])
        self.weather_2_temp_value.setText(day_2['temp'])

        day_3 = self.weather_data[-1][3]
        self.weather_3_date.setText(f"{day_3['time_timezone_now_weekday']}, {day_3['time_timezone_now_day']}")
        self.weather_3_date.setToolTip(f"{day_3['time_timezone_now_weekday']}, {day_3['time_timezone_now_day']}")
        self.weather_3_desc_img.setPixmap(QPixmap(f"weather_img/{day_3['img_id']}.png"))
        self.weather_3_desc_text.setText(day_3['description'])
        self.weather_3_desc_text.setToolTip(day_3['description'])
        self.weather_3_temp_value.setText(day_3['temp'])

        day_4 = self.weather_data[-1][4]
        self.weather_4_date.setText(f"{day_4['time_timezone_now_weekday']}, {day_4['time_timezone_now_day']}")
        self.weather_4_date.setToolTip(f"{day_4['time_timezone_now_weekday']}, {day_4['time_timezone_now_day']}")
        self.weather_4_desc_img.setPixmap(QPixmap(f"weather_img/{day_4['img_id']}.png"))
        self.weather_4_desc_text.setText(day_4['description'])
        self.weather_4_desc_text.setToolTip(day_4['description'])
        self.weather_4_temp_value.setText(day_4['temp'])

        day_5 = self.weather_data[-1][5]
        self.weather_5_date.setText(f"{day_5['time_timezone_now_weekday']}, {day_5['time_timezone_now_day']}")
        self.weather_5_date.setToolTip(f"{day_5['time_timezone_now_weekday']}, {day_5['time_timezone_now_day']}")
        self.weather_5_desc_img.setPixmap(QPixmap(f"weather_img/{day_5['img_id']}.png"))
        self.weather_5_desc_text.setText(day_5['description'])
        self.weather_5_desc_text.setToolTip(day_5['description'])
        self.weather_5_temp_value.setText(day_5['temp'])

        day_6 = self.weather_data[-1][6]
        self.weather_6_date.setText(f"{day_6['time_timezone_now_weekday']}, {day_6['time_timezone_now_day']}")
        self.weather_6_date.setToolTip(f"{day_6['time_timezone_now_weekday']}, {day_6['time_timezone_now_day']}")
        self.weather_6_desc_img.setPixmap(QPixmap(f"weather_img/{day_6['img_id']}.png"))
        self.weather_6_desc_text.setText(day_6['description'])
        self.weather_6_desc_text.setToolTip(day_6['description'])
        self.weather_6_temp_value.setText(day_6['temp'])

        days_temp = [day_0, day_1, day_2, day_3, day_4, day_5, day_6]
        days_temp_color = [self.weather_0_temp_value, self.weather_1_temp_value, self.weather_2_temp_value,
                           self.weather_3_temp_value,
                           self.weather_4_temp_value, self.weather_5_temp_value, self.weather_6_temp_value]
        for i in range(len(days_temp)):
            if int(days_temp[i]['temp']) > 28:
                days_temp_color[i].setStyleSheet("color: #FF4A22")
            elif int(days_temp[i]['temp']) > 18:
                days_temp_color[i].setStyleSheet("color: #1AFF6C")
            elif int(days_temp[i]['temp']) > 10:
                days_temp_color[i].setStyleSheet("color: #FFA31A")
            elif int(days_temp[i]['temp']) >= 5:
                days_temp_color[i].setStyleSheet("color: #FAC429")
            elif int(days_temp[i]['temp']) > 0:
                days_temp_color[i].setStyleSheet("color: #FFF785")
            elif int(days_temp[i]['temp']) == 0:
                days_temp_color[i].setStyleSheet("color: #FFFFFF")
            else:
                days_temp_color[i].setStyleSheet("color: #4769FF")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainFunc()
    ex.show()
    sys.exit(app.exec_())

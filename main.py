import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("City name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel("--°C", self)
        self.emoji_label = QLabel(self)
        self.emoji_label.setFont(QFont("Segoe UI Emoji", 100))  
        self.description_label = QLabel("Weather Description", self)
        self.forecast_label = QLabel("5-Day Forecast:", self)
        self.forecast_text = QTextEdit(self)
        self.forecast_text.setReadOnly(True)
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.forecast_label)
        vbox.addWidget(self.forecast_text)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.forecast_label.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
            QWidget { background-color: #A9CCE3; color: black; }
            QLabel, QPushButton { font-family: 'Arial'; color: black; }
            QLabel#city_label, QLabel#forecast_label { font-size: 30px; font-style: italic; }
            QLineEdit { font-size: 35px; border-radius: 8px; border: 2px solid #004080; padding: 5px; background-color: #87CEEB; color: black; }
            QPushButton { font-size: 30px; font-weight: bold; }
            QLabel#temperature_label { font-size: 70px; }
            QLabel#emoji_label { font-size: 90px; font-family: 'Segoe UI Emoji'; }
            QLabel#description_label { font-size: 40px; }
            QTextEdit { font-size: 20px; background-color: #E6F2FF; border-radius: 8px; padding: 5px; }
        """)
        
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "1a3e1b4cfaa61b5e9b9358b3dcf28a39"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == "200":
                self.display_weather(data)
        
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Error: {req_error}")

    def display_error(self, message):
        self.temperature_label.setText("--°C")
        self.emoji_label.setText("")
        self.description_label.setText(message)
        self.forecast_text.setText("")

    def display_weather(self, data):
        current_temp = data["list"][0]["main"]["temp"]
        weather_id = data["list"][0]["weather"][0]["id"]
        description = data["list"][0]["weather"][0]["description"].capitalize()
        
        self.temperature_label.setText(f"{current_temp:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoj(weather_id))
        self.description_label.setText(description)
        
        forecast_text = ""
        for i in range(0, len(data["list"]), 8): 
            temp_c = data["list"][i]["main"]["temp"]
            date = data["list"][i]["dt_txt"][:10]
            forecast_text += f"{date}: {self.get_weather_emoj(data['list'][i]['weather'][0]['id'])} {temp_c:.0f}°C\n"
        
        self.forecast_text.setText(forecast_text)

    @staticmethod
    def get_weather_emoj(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "🌬️"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return "🧐"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
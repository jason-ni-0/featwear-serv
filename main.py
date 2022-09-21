import requests
from bs4 import BeautifulSoup
from flask import Flask,request
from flask_restful import Resource, Api, reqparse
import ast
from datetime import date
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)
api = Api(app)

def getHoroscope(zodiac, day):
    URL = "https://trustedteller.com/horoscope/"+zodiac+"/horoscope-"+day+"/luck"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.find("p", class_="pre mb-0")

def getHex(colors):
    hexes = []
    for color in colors:
        color = color.replace(" ", "+")
        URL = "https://alexbeals.com/projects/colorize/search.php?q=" + color
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        hexes.append(soup.find("span", class_="hex").string)
    return hexes


class Color(Resource):
    def get(self):
        today = date.today()
        zodiac = request.args.get('zodiac')
        if zodiac == None:
            return {'message': 'Invalid Query'}

        horoscope = getHoroscope(zodiac, "today")

        dateElem = horoscope.find("span", class_="date-horscop").string[:-2]
        if dateElem[:2] != str(today)[-2:]:
            horoscope = getHoroscope(zodiac, "yesterday")
        dateElem = horoscope.find("span", class_="date-horscop").string[:-2]
        hexes = getHex(horoscope.find_all("p")[0].string[20:].split())
        return {'date': today.strftime("%B %d, %Y"), 'colors': horoscope.find_all("p")[0].string[20:].split(), 'hex':hexes}, 200  # return data and 200 OK code

class Weather(Resource):
    def get(self):
        API_KEY = os.getenv("WEATHER_API_KEY")
        lat = request.args.get('lat')
        long = request.args.get('long')
        if (lat == None) or (long == None):
            return {'message': 'Invalid Query'}
        URL = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={API_KEY}&units=imperial'
        weather = requests.get(URL)
        weather = weather.json()
        data = {'city': weather['name'], 'weather': weather['weather'][0]['description'], 'temp': round(weather['main']['temp']), 'min': round(weather['main']['temp_min']), 'max': round(weather['main']['temp_max'])}
        return data

api.add_resource(Color, '/color')
api.add_resource(Weather, '/weather')

if __name__ == '__main__':
    app.run()  # run our Flask app

import requests
from bs4 import BeautifulSoup
from flask import Flask,request
from flask_restful import Resource, Api, reqparse
import ast

app = Flask(__name__)
api = Api(app)

class Wear(Resource):
    def get(self):
        zodiac = request.args.get('zodiac')
        if zodiac == None:
            return {'message': 'Invalid Query'}
        URL = "https://trustedteller.com/horoscope/"+zodiac+"/horoscope-today/luck"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        horoscope = soup.find("p", class_="pre mb-0")
        #print(horoscope)

        #print(horoscope.find_all("p")[0].string)

        dateElem = horoscope.find("span", class_="date-horscop").string
        #print(dateElem.string)
        return {'date': dateElem, 'colors': horoscope.find_all("p")[0].string}, 200  # return data and 200 OK code

api.add_resource(Wear, '/wear')  # '/users' is our entry point

if __name__ == '__main__':
    app.run()  # run our Flask app

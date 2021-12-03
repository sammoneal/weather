from flask import Flask, render_template
from weather_api import WeatherAPI, Cords, geolocator

app = Flask(__name__)

weather_dummy = [("Cloudy",43,0.3),("Clear",50,0.4),("Sunny",60,0.0),("Overcast",46,0.1)]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home', weather=weather_dummy)

#@app.route('/search')
#    raise NotImplementedError

@app.route('/grid')
def grid():
    return render_template('grid.html')

@app.route('/grid2')
def grid2():
    return render_template('grid2.html')

@app.route('/grid3')
def grid3():
    return render_template('grid3.html')

if __name__ == '__main__':
    app.run(debug=True)

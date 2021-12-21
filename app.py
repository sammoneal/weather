from flask import Flask, render_template, request
from flask.helpers import url_for
from werkzeug.utils import redirect
from weather_api import WeatherAPI, Cords, geolocator
from forms import SearchForm

app = Flask(__name__)
app.secret_key = 'ac23959ac002afac32be8093c72920ea'

@app.route('/', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('weather', lat=form.geocoded.latitude, long=form.geocoded.longitude))
    return render_template('search.html', title='My Weather Site', form=form)

@app.route('/weather/<lat>/<long>')
def weather(lat, long):
    weather = WeatherAPI(lat, long)
    return render_template('weather.html', title=weather.city+' - Weather', weather=weather)







#CSS grid refs
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

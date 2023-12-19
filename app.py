from flask import Flask, render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
from weather_api.weather_api import WeatherAPI
from forms import SearchForm

app = Flask(__name__)
app.secret_key = "ac23959ac002afac32be8093c72920ea"


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
@app.route("/search", methods=["GET", "POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(
            url_for("weather", lat=form.geocoded.latitude, long=form.geocoded.longitude)
        )
    return render_template("search.html", title="Weather", form=form)


@app.route("/weather/<lat>/<long>",methods=["GET", "POST"])
def weather(lat, long):
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(
            url_for("weather", lat=form.geocoded.latitude, long=form.geocoded.longitude)
        )
    weather = WeatherAPI(lat, long)
    return render_template(
        "weather.html", title=weather.city + " - Weather", weather=weather, form=form
    )

@app.route("/demo")
def demo():
    return render_template('demo.html')


if __name__ == "__main__":
    app.run(debug=True, port=8000)

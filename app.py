"""Weather app backend and entrypoint
"""
import os
from flask import Flask, render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
from dotenv import load_dotenv
from weather_api import WeatherAPI
from forms import SearchForm

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/", methods=["GET", "POST"])
def home():
    """Home and splash page with hero search bar
    """
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(
            url_for("weather", lat=form.geocoded.latitude, long=form.geocoded.longitude)
        )
    return render_template("home.html", title="Weather", form=form)


@app.route("/weather/<lat>/<long>", methods=["GET", "POST"])
def weather(lat:float, long:float):
    """Weather dashboard

    Args:
        lat (float): Latitude
        long (float): Longitude
    """
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(
            url_for("weather", lat=form.geocoded.latitude, long=form.geocoded.longitude)
        )
    weather_data = WeatherAPI(lat, long)
    return render_template(
        "dashboard.html", title=weather_data.city + " - Weather", weather=weather_data
    )


if __name__ == "__main__":
    app.run(debug=True, port=8000)

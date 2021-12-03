from flask_wtf import FlaskForm
from geopy import geocoders
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from weather_api import geolocator

class SearchForm(FlaskForm):
    location = StringField('Enter a Location', validators=[DataRequired()])
    submit = SubmitField('Forecast')

    def validate_location(self, location):
        if not geolocator.geocode(location):
            raise ValidationError('Please enter a valid US location.')

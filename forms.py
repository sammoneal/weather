from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from weather_api import geolocator

class SearchForm(FlaskForm):
    location = StringField('Enter a Location', validators=[DataRequired()])
    submit = SubmitField('Forecast')

    def __init__(self):
        super().__init__()
        self.geocoded = None

    def validate_location(self, location):
        coded_loc = geolocator.geocode(location.data, country_codes='US')
        if coded_loc is None:
            raise ValidationError('Please enter a valid US location.')
        self.geocoded = coded_loc

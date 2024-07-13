# US Weather Dashboard

## Overview

This repository contains a web application built with Python Flask that displays weather information for a user-specified location in the United States.

## Features

* **Location Search:** Users can enter a US location in the search bar.
* **Dynamic URL:** Searching redirects to a dynamic URL displaying a server-side generated weather dashboard. Ping a latitude and longitude directly though path variables.
* **Jinja Templating:** The Flask application utilizes the Jinja templating engine to build an up to date dashboard.
* **Charts:** Easy to read charts made from vanilla HTML and CSS.

## Dependencies

### This project utilizes the following dependencies:

* [Flask](https://flask.palletsprojects.com/): A lightweight web framework for Python
* [Jinja2](https://palletsprojects.com/p/): Templating engine for Python
* [Requests](https://requests.readthedocs.io/): HTTP library for Python
* [pipenv](https://docs.pipenv.org/basics/): Virtual environment management tool with dependency locking
* [dotenv](https://www.dotenv.org/docs/): Manages environment variables in Python
* [OpenStreetMap Nominatim API](): Geolocation is performed using the OpenStreetMaps Nominatim API to retrieve latitude and longitude coordinates.
* [National Weather Service API](): Weather data is fetched from the National Weather Service API based on the retrieved coordinates.

**Note:** API keys for Nominatim and National Weather Service are not included.

## Usage

### Environment Setup

1. Clone this repository.
2. Install dependencies using pipenv:
   ```bash
   pipenv install
   ```
3. Create a file named `.env` in the project root directory.
4. Add your API keys for Nominatim and National Weather Service to the `.env` file according to the format specified by `dotenv`.

### Run

1. Activate the virtual environment:
   ```bash
   pipenv shell
   ```
2. Run the Flask application:
   ```bash
   python app.py
   ```
3. Access the application in your web browser at `localhost:8000/`

## Attribution

### Weather Icons

Weather icons used in this project are from [Erik Flowers](https://erikflowers.github.io/weather-icons/).

## To-Do

* Conditions based themes
* Weather station pages
* Improved chart legends
* Responsive dashboard
* User session and user prefs
* Accounts

## Contribution

Feel free to explore the code and consider making improvements! 
# amp-flask-poc

A simple Flask web application that calls the Blockstream AMP API to allow AMP asset issuers to demonstrate or test the platform.

The website doesn't allow you to issue an asset (that must be done using the AMP API) but it allows you to register users and
view some basic asset and user data. You can add more to the site by calling more of the API. The spec for the API can be found here:

https://docs.blockstream.com/blockstream-amp/api-specification.html

Before running, change the settings in config.py:

API_USERNAME, API_PASSWORD, API_URL, SECRET_KEY

To install requirements:

pip install -r requirements.txt

To run:

flask run

The website will then be avialable via:

http://127.0.0.1:5000/

To add more data to the website:

1. Add the endpoint you want to use to get the data to api_data_access.py.

2. Add the path to routes.py.

3. Create a template .html page that will display the data.

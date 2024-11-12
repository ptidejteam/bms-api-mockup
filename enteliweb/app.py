from flask import Flask
from flask_restx import Api
from flask_basicauth import BasicAuth
from isystem_resource import api as systems_api
from idot_data_resource import api as idot_data_api
from idot_multi_resource import api as idot_multi_api
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Configure basic authentication
app.config['BASIC_AUTH_USERNAME'] = os.getenv('USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('PASSWORD')
basic_auth = BasicAuth(app)

# Define the authorization scheme
authorizations = {
    'basicAuth': {
        'type': 'basic'
    }
}

# Initialize the API with the authorization scheme
api = Api(app, version='1.0', title='enteliWEB BMS API Mockup',
          description='enteliWEB BMS API Mockup',
          authorizations=authorizations,
          security='basicAuth'
          )

api.add_namespace(systems_api, path='/enteliweb/api/systems')
api.add_namespace(idot_data_api, path='/enteliweb/api/.data')
api.add_namespace(idot_multi_api, path='/enteliweb/api/.multi')


# Apply basic authentication to all requests
@app.before_request
def require_basic_auth():
    if not basic_auth.authenticate():
        return basic_auth.challenge()


if __name__ == '__main__':
    app.run(debug=True)

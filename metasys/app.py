from flask import Flask, request, jsonify
from flask_restx import Api
from dotenv import load_dotenv
import os
from space_resource import api as space_api
from equipment_resource import api as equipment_api
from time_series import api as time_series_api

load_dotenv()

app = Flask(__name__)

# Define the authorization scheme
authorizations = {
    'bearerAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

# Initialize the API with the authorization scheme
api = Api(app, version='1.0', title='Metasys BMS API MockUp',
          description='Metasys BMS API MockUp',
          authorizations=authorizations,
          security='bearerAuth'
          )

api.add_namespace(space_api, path='/api/v4/')
api.add_namespace(equipment_api, path='/api/v4/equipment')
api.add_namespace(time_series_api, path='/api/v4/objects')


def verify_bearer_token(token):
    # Implement your token verification logic here
    # For example, check if the token is valid and not expired
    return token == os.getenv('BEARER_TOKEN')


# Apply basic authentication to all requests
@app.before_request
def require_bearer_token():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]
        if verify_bearer_token(token):
            return  # Token is valid, proceed with the request
    response = jsonify({"message": "Unauthorized"})
    response.status_code = 401
    return response


if __name__ == '__main__':
    app.run(debug=True, port=6000)

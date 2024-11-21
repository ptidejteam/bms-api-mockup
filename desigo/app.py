from flask import Flask, request, jsonify
from flask_restx import Api
from dotenv import load_dotenv
import os
from desigo_resource import api as building_structure_api

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
api = Api(app, version='1.0', title='Desigo BMS API MockUp',
          description='Desigo BMS API MockUp',
          authorizations=authorizations,
          security='bearerAuth'
          )

api.add_namespace(building_structure_api, path='/structure/partitions/1')


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
    response = jsonify({
        "errors": [
            {
                "id": "1c083f76-e6a4-45c9-974b-9eb78ed05259",
                "code": "500-0102",
                "status": "401",
                "title": "Unauthorized",
                "detail": "The request has not been completed. Provide authentication credentials for the requested "
                          "resource."
            }
        ]
    })
    response.status_code = 401
    return response


if __name__ == '__main__':
    app.run(debug=True, port=7000)

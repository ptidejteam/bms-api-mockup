from flask_restx import Namespace, Resource
from util import Util
import json
from flask import jsonify, request, make_response
from datetime import datetime

api = Namespace('desigo addresses',
                description='API endpoints for Desigo Buiulding X')


@api.route('/')
class AddressList(Resource):
    def get(self):
        """List addresses
        """
        json_data = json.loads(Util.get_mock_data('data/addresses.json'))
        page_number = int(request.args.get('page[number]', 0))
        page_size = int(request.args.get('page[size]', 100))
        country_code = request.args.get('filter[countryCode]')
        continent_code = request.args.get('filter[continentCode]')
        filtered_data = [
            item for item in json_data['data']
            if (not country_code or item['attributes']['countryCode'] == country_code) and
               (not continent_code or item['attributes']['continentCode'] == continent_code)
        ]

        json_data['data'] = filtered_data[page_number:page_number + page_size]
        return jsonify(json_data)

    def post(self):
        address = json.loads(request.data.decode('utf-8'))
        address = address['data']
        now = datetime.utcnow()

        # Format the datetime as a string
        address['meta'] = {
            'createdAt': now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            'updatedAt': now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            'createdBy': 'Peter Yefi',
            'updatedBy': 'Peter Yefi'
        }
        json_data = json.loads(Util.get_mock_data('data/addresses.json'))
        json_data['data'].append(address)
        with open('data/addresses.json', 'w') as file:
            json.dump(json_data, file, indent=4)
        address['links'] = {
            'self': f'{request.url}/{address["id"]}'
        }
        return make_response(jsonify(address), 201)


@api.route('/<address_id>')
class Address(Resource):
    def get(self, address_id):
        json_data = json.loads(Util.get_mock_data('data/addresses.json'))
        for address in json_data['data']:
            if address['id'] == address_id:
                address['link'] = {
                    'self': f'{request.url}'
                }
                return jsonify(address)

    def patch(self, address_id):
        data = json.loads(request.data.decode('utf-8'))
        data = data['data']
        json_data = json.loads(Util.get_mock_data('data/addresses.json'))
        for address in json_data['data']:
            if address['id'] == address_id:
                for key, value in data['attributes'].items():
                    address['attributes'][key] = value
            with open('data/addresses.json', 'w') as file:
                json.dump(json_data, file, indent=4)
                return make_response(jsonify(address), 200)

    def delete(self, address_id):
        json_data = json.loads(Util.get_mock_data('data/addresses.json'))
        del_index = -1
        for i in range(len(json_data['data'])):
            if json_data['data'][i]['id'] == address_id:
                del_index = i
                break
        if del_index != -1:
            del json_data['data'][del_index]
            with open('data/addresses.json', 'w') as file:
                json.dump(json_data, file, indent=4)
                return make_response('', 204)
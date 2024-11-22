import random
from flask_restx import Namespace, Resource
from util import Util
import json
from flask import jsonify, request, make_response
import uuid
from datetime import datetime

api = Namespace('desigo devices',
                description='API endpoints for Desigo Buiulding X')


@api.route('/')
class DeviceList(Resource):
    def get(self):
        """Get devices in a partition
        Note: filter may not be applied in the same order as in the API implementation
        Also note that, this is not the entire set of filters
        """
        json_data = json.loads(Util.get_mock_data('data/devices.json'))
        page_size = int(request.args.get('page[limit]', 20))
        model_name = request.args.get('filter[modelName]')
        serial_number = request.args.get('filter[serialNumber]')
        profile_name = request.args.get('filter[profile.name]')
        data = json_data['data'][:page_size]

        # Filtering data based on provided criteria
        filtered_data = [
            item for item in data
            if (not model_name or item['attributes']['modelName'] == model_name) and
               (not serial_number or item['attributes']['serialNumber'] == serial_number) and
               (not profile_name or item['attributes']['profile']['name'] == profile_name)
        ]
        json_data['data'] = filtered_data
        return jsonify(json_data)

    def post(self):
        """Create a device"""
        data = json.loads(request.data.decode('utf-8'))
        device_id = str(uuid.uuid4())
        data = data['data']
        data['id'] = device_id
        data['attributes']['profile'] = {}
        data['attributes']['profile']['name'] = f'X{random.randint(000, 999)}-{random.randint(0, 9)}'
        data['attributes']['profile']['notes'] = 'Newly created device'
        data['relationships'] = {
            "hasGateway": {
                "data": {
                    "type": "Device",
                    "id": str(uuid.uuid4())
                }
            }
        }
        data['hasLocation'] = {
            "data": {
                "type": "Building",
                "id": str(uuid.uuid4())
            }
        }
        data['hasFeature'] = [
            {
                "type": "DeviceInfo",
                "id": str(uuid.uuid4())
            }
        ]

        # insert device to existing devices
        existing_devices = json.loads(Util.get_mock_data('data/devices.json'))
        existing_devices['data'].append(data)
        with open('data/devices.json', 'w') as file:
            json.dump(existing_devices, file, indent=4)
        data['links'] = {
            'self': f'{request.url}/{device_id}'
        }
        return make_response(jsonify(data), 201)


@api.route('/<device_id>')
class Device(Resource):
    def get(self, device_id):
        """Get device"""
        json_data = json.loads(Util.get_mock_data('data/devices.json'))

        for device in json_data['data']:
            if device['id'] == device_id:
                device['links'] = {
                    'self': f'{request.url}'
                }
                return jsonify(device)

        return jsonify({
            "errors": [
                {
                    "id": "e31f00cc-7a5d-46c2-a272-771e6a8d6ff0",
                    "code": "200-0201",
                    "status": "404",
                    "title": "Device not found",
                    "detail": "Device not found"
                }
            ]
        })

    def patch(self, device_id):
        data = json.loads(request.data.decode('utf-8'))
        data = data['data']
        existing_devices = json.loads(Util.get_mock_data('data/devices.json'))
        for device in existing_devices['data']:
            if device['id'] == device_id:
                device['attributes']['profile']['name'] = data['attributes']['profile']['name']
                device['attributes']['profile']['notes'] = data['attributes']['profile']['notes']
                device['attributes']['profile']['externalId'] = data['attributes']['profile']['externalId']
                with open('data/devices.json', 'w') as file:
                    json.dump(existing_devices, file, indent=4)
                    return make_response('Operation accepted', 202)

        return jsonify({
            "errors": [
                {
                    "id": "e31f00cc-7a5d-46c2-a272-771e6a8d6ff0",
                    "code": "200-0201",
                    "status": "403",
                    "title": "Forbidden to perform this action",
                    "detail": "Forbidden to perform this action"
                }
            ]
        })


@api.route('/<device_id>/points')
class DevicePoints(Resource):
    def get(self, device_id):
        """Get device points"""
        json_data = json.loads(Util.get_mock_data('data/points.json'))
        if json_data['links']['self'].split('/')[-2] == device_id:
            return jsonify(json_data)

        return jsonify({
            "errors": [
                {
                    "id": "e31f00cc-7a5d-46c2-a272-771e6a8d6ff0",
                    "code": "200-0201",
                    "status": "403",
                    "title": "Forbidden to perform this action",
                    "detail": "Forbidden to perform this action"
                }
            ]
        })

import random
from flask_restx import Namespace, Resource
from util import Util
import json
from flask import jsonify, request, make_response
import uuid
from datetime import datetime

api = Namespace('desigo',
                description='API endpoints for Desigo Buiulding X')


@api.route('/locations')
class LocationList(Resource):
    def get(self):
        """Get locations in a partition.
        Note: filter may not be applied in the same order as in the API implementation
        Also note that, this is not the entire set of filters
        """
        json_data = json.loads(Util.get_mock_data('data/locations.json'))
        page_number = int(request.args.get('page[number]', 0))
        page_size = int(request.args.get('page[size]', 100))
        building_type = request.args.get('filter[type]')
        data = json_data['data']
        if building_type:
            data = [location for location in json_data['data'] if location['type'].lower() == building_type.lower()]
        json_data['data'] = data[page_number:page_number + page_size]
        return jsonify(json_data)

    def post(self):
        location = json.loads(request.data.decode('utf-8'))
        if location:
            json_data = json.loads(Util.get_mock_data('data/locations.json'))
            json_data['data'].append(location['data'])
            with open('data/locations.json', 'w') as file:
                json.dump(json_data, file, indent=4)
                location['links'] = {
                    'self': f'{request.url}'
                }
                return jsonify(location)

        return jsonify({
            "errors": [
                {
                    "id": "e31f00cc-7a5d-46c2-a272-771e6a8d6ff0",
                    "code": "200-0201",
                    "status": "403",
                    "title": "Forbidden to perform this action",
                    "detail": "Missing permission",
                    "source": {
                        "pointer": "/data/attributes/title"
                    }
                }
            ]
        })


@api.route('/locations/<location_id>')
class Location(Resource):
    def get(self, location_id):
        """Get location"""
        json_data = json.loads(Util.get_mock_data('data/locations.json'))
        ret_data = {
            "links": {
                "self": f"/locations/{location_id}"
            }
        }
        include = request.args.get('include', '')
        for location in json_data['data']:
            if location['id'] == location_id:
                if include == 'hasPostalAddress':
                    try:
                        if location['relationships']['hasPostalAddress']['data']:
                            ret_data['data'] = location
                            return jsonify(ret_data)
                    except IndexError:
                        pass
                elif not include:
                    ret_data['data'] = location
                    return jsonify(ret_data)

        return jsonify({
            "errors": [
                {
                    "id": "e31f00cc-7a5d-46c2-a272-771e6a8d6ff0",
                    "code": "200-0201",
                    "status": "404",
                    "title": "Location not found",
                    "detail": "Location not found"
                }
            ]
        })

    def patch(self, location_id):
        json_data = json.loads(Util.get_mock_data('data/locations.json'))
        for location in json_data['data']:
            if location['id'] == location_id:
                data = json.loads(request.data.decode('utf-8'))
                for key, value in data['data'].items():
                    if key == 'id':
                        continue
                    if key == 'attributes':
                        for attr_key, attr_value in value.items():
                            location[key][attr_key] = attr_value
                    else:
                        location[key] = value
                with open('data/locations.json', 'w') as file:
                    json.dump(json_data, file, indent=4)
                    return jsonify({'data': location, 'link': {'self': request.url}})
        return jsonify({
            "errors": [
                {
                    "id": "e31f00cc-7a5d-46c2-a272-771e6a8d6ff0",
                    "code": "200-0201",
                    "status": "403",
                    "title": "Forbidden to perform this action",
                    "detail": "Missing permission",
                    "source": {
                        "pointer": "/data/attributes/title"
                    }
                }
            ]
        })


@api.route('/devices')
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


@api.route('/devices/<device_id>')
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


@api.route('/devices/<device_id>/points')
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


@api.route('/points/<point_id>')
class Point(Resource):
    def get(self, point_id):
        """Get points"""
        json_data = json.loads(Util.get_mock_data('data/points.json'))
        for point in json_data['data']:
            if point['id'] == point_id:
                return jsonify({
                    'links': {
                        'self': f'{request.url}'
                    },
                    'data': point
                })

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

    def patch(self, point_id):
        json_data = json.loads(Util.get_mock_data('data/points.json'))
        for point in json_data['data']:
            if point['id'] == point_id:
                data = json.loads(request.data.decode('utf-8'))
                point['attributes']['pointValue']['value'] = data['data']['attributes']['pointValue']['value']
                with open('data/points.json', 'w') as file:
                    json.dump(json_data, file, indent=4)
                    return make_response('', 204)

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


@api.route('/points/<point_id>/tags')
class PointTags(Resource):
    def put(self, point_id):
        """Get points"""
        json_data = json.loads(Util.get_mock_data('data/points.json'))
        for point in json_data['data']:
            if point['id'] == point_id:
                data = json.loads(request.data.decode('utf-8'))
                for key, value in data['data']['tags'].items():
                    point['attributes']['tags'][key] = value
                with open('data/points.json', 'w') as file:
                    json.dump(json_data, file, indent=4)
                    return make_response('', 204)

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


@api.route('/points/<point_id>/values')
class PointValues(Resource):
    def get(self, point_id):
        """
        Get Point values
        Note: Not all filters for this endpoint has been implemented
        """
        json_data = json.loads(Util.get_mock_data('data/point_values.json'))
        from_ts = request.args.get('filter[timestamp][from]')
        to_ts = request.args.get('filter[timestamp][to]')
        from_ts = datetime.strptime(from_ts, "%Y-%m-%dT%H:%M:%S.%fZ") if from_ts != 0 else None
        to_ts = datetime.strptime(to_ts, "%Y-%m-%dT%H:%M:%S.%fZ") if to_ts != 0 else None
        if json_data['links']['self'].split('/')[-2] == point_id:
            filtered_data = []
            for point_value in json_data['data']:
                ts = datetime.strptime(point_value['attributes']['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
                if from_ts and to_ts:
                    if from_ts <= ts <= to_ts:
                        filtered_data.append(point_value)
                elif from_ts:
                    if ts >= from_ts:
                        filtered_data.append(point_value)
                else:
                    filtered_data.append(point_value)
            json_data['data'] = filtered_data
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

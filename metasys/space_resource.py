from flask_restx import Namespace, Resource
from util import Util
import json
from flask import jsonify, request, make_response

api = Namespace('metasys_space', description='Get spaces served by a network device')


@api.route('/networkDevices/<device_id>/spaces')
class NetworkDeviceSpaces(Resource):
    def get(self, device_id):
        """Get spaces served by network devices"""
        json_data = json.loads(Util.get_mock_data('data/spaces.json'))
        # slight variation in the returned network devices
        if 'networkDevices' in request.path:
            json_data['items'] = json_data['items'][0]
            json_data['total'] = 1
        elif 'equipment' in request.path:
            json_data['items'] = json_data['items'][1]
            json_data['total'] = 1
        return jsonify(json_data)


@api.route('/equipment/<device_id>/spaces')
class EquipmentSpaces(NetworkDeviceSpaces):
    pass


@api.route('/spaces')
class SpaceList(Resource):
    def get(self):
        json_data = json.loads(Util.get_mock_data('data/spaces.json'))
        return jsonify(json_data)


@api.route('/spaces/<space_id>')
class Space(Resource):
    def get(self, space_id):
        json_data = json.loads(Util.get_mock_data('data/spaces.json'))
        for space in json_data['items']:
            if space['id'] == space_id:
                return jsonify(space)
        return make_response(jsonify({'error': 'space not found'}), 404)


@api.route('/spaces/<space_id>/spaces')
class SpaceChildren(Resource):
    def get(self, space_id):
        json_data = json.loads(Util.get_mock_data('data/spaces.json'))
        existing_parent_space = None
        for space in json_data['items']:
            if space['id'] == space_id:
                existing_parent_space = space
        if existing_parent_space:
            json_data['items'] = json_data['items'][-1]
            json_data['total'] = 1
            return jsonify(json_data)

        return make_response(jsonify({'error': 'parent space not found'}), 404)


@api.route('/spaces/<space_id>/equipment')
class EquipmentServingSpace(Resource):
    def get(self, space_id):
        print(f'Request parameter - space id: {space_id}')
        json_data = json.loads(Util.get_mock_data('data/equipment.json'))
        return jsonify(json_data)


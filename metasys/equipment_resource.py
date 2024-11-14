from flask_restx import Namespace, Resource
from util import Util
import json
from flask import jsonify, make_response

api = Namespace('metasys_equipment',
                description='This section describes the operations you can perform on equipment')


@api.route('/')
class EquipmentInstanceList(Resource):
    def get(self):
        """Get spaces served by network devices"""
        json_data = json.loads(Util.get_mock_data('data/equipment.json'))
        # slight variation in the returned network devices
        return jsonify(json_data)


@api.route('/<equipment_id>')
class EquipmentInstance(Resource):
    def get(self, equipment_id):
        """Get spaces served by network devices"""
        json_data = json.loads(Util.get_mock_data('data/equipment.json'))
        for equipment in json_data['items']:
            if equipment['id'] == equipment_id:
                return jsonify(equipment)
        return make_response(jsonify({'error': 'equipment not found'}), 404)


@api.route('/<equipment_id>/equipment')
class EquipmentChildrenInstance(Resource):
    def get(self, equipment_id):
        """Get spaces served by network devices"""
        json_data = json.loads(Util.get_mock_data('data/equipment.json'))
        # get a random equipment as a child for the equipment with the provided ID
        json_data['items'] = json_data['items'][2]
        json_data['total'] = 1
        return jsonify(json_data)


@api.route('/<equipment_id>/points')
class EquipmentPoints(Resource):
    def get(self, equipment_id):
        """Get spaces served by network devices"""
        json_data = json.loads(Util.get_mock_data('data/equipment_points.json'))
        # get a random equipment as a child for the equipment with the provided ID
        points = [point for point in json_data['items'] if point['id'] == equipment_id]
        json_data['items'] = points
        json_data['total'] = len(points)
        return jsonify(json_data)

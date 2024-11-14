from flask_restx import Namespace, Resource
from util import Util
import json
from flask import jsonify

api = Namespace('metasys_timeseries',
                description='Operations to retrieve time series data.')


@api.route('/<object_id>/trendedAttributes')
class ObjectAttributes(Resource):
    def get(self, object_id):
        """Get spaces served by network devices"""
        json_data = json.loads(Util.get_mock_data('data/timeseries.json'))
        json_data['trendedAttributes']['items'] = [attr for attr in json_data['trendedAttributes']['items'] if
                                                   object_id in attr['samplesUrl']]
        return jsonify(json_data['trendedAttributes'])


@api.route('/<object_id>/trendedAttributes/<attribute_id>')
class ObjectSamples(Resource):
    def get(self, object_id, attribute_id):
        """Get spaces served by network devices"""
        json_data = json.loads(Util.get_mock_data('data/timeseries.json'))
        return jsonify(json_data['trendedData'])


@api.route('/')
class ObjectList(Resource):
    def get(self):
        """Get spaces served by network devices"""
        json_data = json.loads(Util.get_mock_data('data/objects.json'))
        return jsonify(json_data['object'])


@api.route('/<object_id>/attributes')
class ObjectAttributes(Resource):
    def get(self, object_id):
        """Get spaces served by network devices"""
        json_data = json.loads(Util.get_mock_data('data/objects.json'))
        return jsonify(json_data['objectAttributes'])

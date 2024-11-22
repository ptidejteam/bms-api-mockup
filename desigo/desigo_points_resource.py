from flask_restx import Namespace, Resource
from util import Util
import json
from flask import jsonify, request, make_response
from datetime import datetime

api = Namespace('desigo points',
                description='API endpoints for Desigo Buiulding X')


@api.route('/<point_id>')
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


@api.route('/<point_id>/tags')
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


@api.route('/<point_id>/values')
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

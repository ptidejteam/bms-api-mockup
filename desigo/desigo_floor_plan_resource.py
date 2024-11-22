from flask_restx import Namespace, Resource
from util import Util
import json
from flask import jsonify, request, make_response
from datetime import datetime

api = Namespace('desigo floor plan',
                description='API endpoints for Desigo Buiulding X')


@api.route('/')
class FloorPlanList(Resource):
    def get(self):
        """
        List Floorplans, filtered by user provided parameters
        Note: not all filters have been included in this mockup implementation
        """
        json_data = json.loads(Util.get_mock_data('data/floor_plans.json'))
        page_number = int(request.args.get('page[number]', 0))
        page_size = int(request.args.get('page[size]', 100))
        json_data['data'] = json_data['data'][page_number:page_number + page_size]
        return jsonify(json_data)


@api.route('/<floor_plan_id>')
class FloorPlan(Resource):
    def get(self, floor_plan_id):
        """
        Get floor plan details by id
        """
        json_data = json.loads(Util.get_mock_data('data/floor_plans.json'))
        for plan in json_data['data']:
            if plan['id'] == floor_plan_id:
                ret_data = {
                    'data': plan
                }
                return jsonify(ret_data)


@api.route('/<floor_plan_id>/floorplan-images')
class FloorPlanImageList(Resource):
    def get(self, floor_plan_id):
        """
        List Floorplan Images, filtered by user provided parameters
        Note: not all filters have been included in this mockup implementation
        """
        json_data = json.loads(Util.get_mock_data('data/floor_plans.json'))
        for plan in json_data['data']:
            if plan['id'] == floor_plan_id:
                floor_plan_images = json.loads(Util.get_mock_data('data/floor_plan_images.json'))
                page_number = int(request.args.get('page[number]', 0))
                page_size = int(request.args.get('page[size]', 100))
                floor_plan_images['data'] = floor_plan_images['data'][page_number:page_number + page_size]
                return jsonify(floor_plan_images)


@api.route('/<floor_plan_id>/floorplan-images/<floor_plan_image_id>')
class FloorPlanImage(Resource):
    def get(self, floor_plan_id, floor_plan_image_id):
        """
        Get Floorplan Image by ID
        """
        json_data = json.loads(Util.get_mock_data('data/floor_plans.json'))
        for plan in json_data['data']:
            if plan['id'] == floor_plan_id:
                floor_plan_images = json.loads(Util.get_mock_data('data/floor_plan_images.json'))
                for image in floor_plan_images['data']:
                    if image['id'] == floor_plan_image_id:
                        ret_data = {
                            'data': image
                        }
                        return jsonify(ret_data)


@api.route('/<floor_plan_id>/geometry')
class FloorPlanGeometryList(Resource):
    def get(self, floor_plan_id):
        """
        List Geometry, filtered by user provided parameters
        Note: not all filters have been included in this mockup implementation
        """
        # ideally you will get the geometry related to the provide id
        print(f'Request Parameter: floor plan id - {floor_plan_id}')
        accept_header = request.headers.get('Accept', 'image/svg+xml')
        if accept_header == 'application/geo+json':
            json_data = json.loads(Util.get_mock_data('data/floor_plan_geometry.json'))
            response = make_response(json.dumps(json_data), 200)
            response.headers['Content-Type'] = 'application/geo+json'
            return response
        else:
            svg_data = Util.get_mock_data('data/floor_plan_geometry.svg')
            response = make_response(svg_data, 200)
            response.headers['Content-Type'] = 'image/svg+xml'
            return response


@api.route('/<floor_plan_id>/geometry/center-point')
class FloorPlanGeometryCenterPoint(Resource):
    def get(self, floor_plan_id):
        """
        Get Geometry Center Point for all the Geometry available on the Floorplan
        filtered with user provided parameters in ORG2D
        """
        json_data = json.loads(Util.get_mock_data('data/floor_plan_images.json'))
        for plan in json_data['data']:
            if plan['id'] == floor_plan_id:
                center_point = {
                    'data': {
                        'attributes': {
                            'centerPoint': plan['attributes']['centerPoint']
                        }
                    }
                }
                return jsonify(center_point)


@api.route('/<floor_plan_id>/geometry/<geometry_id>')
class FloorPlanGeometry(Resource):
    def get(self, floor_plan_id, geometry_id):
        """
        Get Geometry Center Point for all the Geometry available on the Floorplan
        filtered with user provided parameters in ORG2D
        """
        json_data = json.loads(Util.get_mock_data('data/floor_plans.json'))
        for plan in json_data['data']:
            if plan['id'] == floor_plan_id:
                geometries = json.loads(Util.get_mock_data('data/floor_plan_geometry.json'))
                for geometry in geometries['features']:
                    if geometry['properties']['geometryId'] == geometry_id:
                        now = datetime.utcnow()
                        del geometry['properties']['geometryId']
                        props_reps = geometry['properties']['represents']
                        del geometry['properties']['represents']
                        geometry_data = {
                            'link': {
                                'self': f'{request.url}'
                            },
                            'data': {
                                'type': 'Geometry',
                                'id': geometry_id,
                                'attributes': geometry['properties'],
                                'geometry': geometry['geometry'],
                                'meta': {
                                    'createdAt': now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                                    'updatedAt': now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                                    'createdBy': 'Peter Yefi',
                                    'updatedBy': 'Peter Yefi'
                                },
                                'included': [props_reps['data']],
                                'relationships': {
                                    'represents': {
                                        'data': {
                                            'id': props_reps['data']['id'],
                                            'type': props_reps['data']['type']
                                        }
                                    },
                                    'isPartOfPlan': {
                                        'data': {
                                            'id': props_reps['data']['id'],
                                            'type': props_reps['data']['type']
                                        }
                                    }
                                }
                            }
                        }
                        return jsonify(geometry_data)

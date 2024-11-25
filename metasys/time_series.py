import uuid

from flask_restx import Namespace, Resource
from util import Util
import json
from flask import jsonify, request, make_response

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
        """Returns the root object of the tree and, optionally, its children"""
        json_data = json.loads(Util.get_mock_data('data/objects.json'))
        return jsonify(json_data['objects'])

    def post(self):
        data = json.loads(request.data.decode('utf-8'))
        data['id'] = str(uuid.uuid4())
        with open('data/objects.json', 'r+') as file:
            json_data = json.load(file)
            json_data['objects']['items'].append(data)
            file.seek(0)
            json.dump(json_data, file, indent=4)
            file.truncate()
            response = make_response('', 200)
            response.headers['Location'] = f'{request.url}/{data["id"]}'
            return response


@api.route('/<object_id>')
class Object(Resource):
    def get(self, object_id):
        """Objects support one or more views. By default, this operation gets the default view of an object.
        """
        json_data = json.loads(Util.get_mock_data('data/objects.json'))
        objects = json_data['objects']['items']
        for obj in objects:
            if obj['id'] == object_id:
                return jsonify(obj)

    def patch(self, object_id):
        json_data = json.loads(Util.get_mock_data('data/objects.json'))
        objects = json_data['objects']['items']
        for obj in objects:
            if obj['id'] == object_id:
                data = json.loads(request.data.decode('utf-8'))
                for key, value in data['item'].items():
                    obj[key] = value
                with open('data/objects.json', 'w') as file:
                    json.dump(json_data, file, indent=4)
                    return make_response('Success', 200)

    def delete(self, object_id):
        json_data = json.loads(Util.get_mock_data('data/objects.json'))
        objects = json_data['objects']['items']
        del_index = -1
        for i in range(len(objects)):
            if objects[i]['id'] == object_id:
                del_index = i
                break
        if del_index != -1:
            del objects[del_index]
            with open('data/objects.json', 'w') as file:
                json.dump(json_data, file, indent=4)
                return make_response('Success', 204)


@api.route('/<object_id>/attributes')
class ObjectAttributes(Resource):
    def get(self, object_id):
        """Returns an object payload with a JSON schema that contains all
        of the properties of the object
        """
        json_data = json.loads(Util.get_mock_data('data/objects.json'))
        return jsonify(json_data['objectAttributes'])


@api.route('/<object_id>/commands')
class ObjectCommands(Resource):
    def get(self, object_id):
        """Returns a payload that lists all of the commands that an object supports
        """
        json_data = json.loads(Util.get_mock_data('data/commands.json'))
        return jsonify(json_data)


@api.route('/<object_id>/commands/<command_id>')
class ObjectCommands(Resource):
    def put(self, object_id, command_id):
        """Used to send a command to an object.
        """
        json_data = json.loads(Util.get_mock_data('data/commands.json'))
        existing_object_id = json_data['self'].split('/')[-2]
        if object_id == existing_object_id:
            for command in json_data['items']:
                if command['id'].split('.')[1] == command_id:
                    # get put data and command system
                    put_data = json.loads(request.data.decode('utf-8'))
                    return 'Success'

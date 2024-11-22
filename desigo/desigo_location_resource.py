from flask_restx import Namespace, Resource
from util import Util
import json
from flask import jsonify, request, make_response

api = Namespace('desigo',
                description='API endpoints for Desigo Buiulding X')


@api.route('/')
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


@api.route('/<location_id>')
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

    def delete(self, location_id):
        json_data = json.loads(Util.get_mock_data('data/locations.json'))
        del_index = -1
        for i in range(len(json_data['data'])):
            if json_data['data'][i]['id'] == location_id:
                del_index = i
                break
        if del_index != -1:
            del json_data['data'][del_index]
            with open('data/locations.json', 'w') as file:
                json.dump(json_data, file, indent=4)
                return make_response('', 204)


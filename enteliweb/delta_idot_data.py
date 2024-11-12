from flask import request, jsonify, make_response
import xml.etree.ElementTree as ET
from misc import Misc
from util import Util
import json

class DeltaIdotData:

    def get_trend_logs(self):
        # Check the query parameter for response format
        data_type = request.args.get('alt', 'xml')
        skip = int(request.args.get('skip', 0))
        max_results = int(request.args.get('max_results', 100))

        if data_type == 'xml':
            tree = ET.parse('data/trend_logs.xml')
            root = tree.getroot()

            # Define the namespace
            ns = {'csml': 'http://bacnet.org/csml/1.2'}

            # Find all Link elements
            links = root.findall('csml:Link', ns)
            # Apply skip and max_results
            links = links[skip:skip + max_results]

            # Create a new XML structure for the selected links
            new_root = ET.Element('List', name=root.get('name'), next=root.get('next'),
                                  xmlns=Misc.get_namespace(root))

            for link in links:
                ET.SubElement(new_root, '{http://bacnet.org/csml/1.2}Link',
                              name=link.get('name'), value=link.get('value'))

            response = make_response(Misc.process_xml(new_root))
            response.headers['Content-Type'] = 'application/xml'
            return response
        elif data_type == 'json':
            json_data = json.loads(Util.get_mock_data('data/trend_logs.json'))
            items = list(json_data.items())
            items = items[skip:skip + max_results]
            result = dict(items)
            return jsonify(result)


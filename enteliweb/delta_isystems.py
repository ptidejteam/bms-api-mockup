from flask import request, jsonify, make_response
import json
import xml.etree.ElementTree as ET
import re
from misc import Misc
from util import Util


class DeltaISystem:

    def get_systems(self):
        # Check the query parameter for response format
        data_type = request.args.get('alt', 'xml')
        file_path = 'data/isystems.xml' if data_type == 'xml' else 'data/isystems.json'
        return Misc.get_resource_data(file_path)

    def _find_struct(self, system_name):
        namespace = {'ns': 'http://bacnet.org/csml/1.2'}
        tree = ET.parse('data/isystems.xml')
        root = tree.getroot()
        for struct in root.findall('ns:Struct', namespace):
            if struct.get('name') == system_name:
                return struct, tree


    def write_multiple_property_values(self, system_name):
        data_type = request.args.get('alt', 'xml')
        if data_type == 'xml':
            try:
                xml_string = request.data.decode('utf-8').lstrip()
                parsed_xml_string = ET.fromstring(xml_string)
                ns_uri = 'http://bacnet.org/csml/1.2'
                namespace = {'ns': ns_uri}
                # Step 4: Find the target struct in the existing XML data
                struct, tree = self._find_struct(system_name)
                if struct:
                    # Step 5: Update or insert <Real> entries
                    for put_real_tag in parsed_xml_string.findall('ns:Real', namespace):
                        real_name = put_real_tag.get('name')
                        real_value = str(put_real_tag.get('value'))
                        existing_real_tag = struct.find(f'ns:Real[@name="{real_name}"]', namespace)

                        if existing_real_tag is not None:
                            # Update the value of the existing <Real> entry
                            existing_real_tag.set('value', real_value)
                        else:
                            # Insert the new <Real> entry with namespace
                            new_real = ET.Element(f'{{{ns_uri}}}Real',
                                                  attrib={k: v for k, v in put_real_tag.attrib.items()})
                            struct.append(new_real)

                    for struct_element in tree.getroot().findall('ns:Struct', namespace):
                        for elem in struct_element.iter():
                            elem.tag = re.sub(r'\{.*\}', '', elem.tag)

                    # Step 7: Save the updated XML data back to the file
                    tree.write('data/isystems.xml', encoding='utf-8', xml_declaration=True)

                    response = make_response(Misc.process_xml(struct), 200)
                    response.headers['Content-Type'] = 'application/xml'
                    return response
                else:
                    return make_response(jsonify({'error': 'system not found'}), 404)
            except ET.ParseError as e:
                print(e)
                return make_response(jsonify({'error': 'malformed input data'}), 500)
        elif data_type == 'json':
            data = json.loads(request.data.decode('utf-8'))
            existing_json = json.loads(Util.get_mock_data('data/isystems.json'))
            existing_record = existing_json.get(system_name, None)
            if existing_record:
                for key, value in data.items():
                    if key == '$base':
                        continue
                    # check if key exist in existing record
                    if existing_record.get(key, None):
                        existing_record[key]['value'] = value['value']
                    else:
                        existing_record[key] = value
                with open('data/isystems.json', 'w') as file:
                    json.dump(existing_json, file, indent=4)
                return jsonify(existing_record)
            else:
                return make_response(jsonify({'error': 'system not found'}), 404)

    def get_system_property(self, system_name):
        data_type = request.args.get('alt', 'xml')
        if data_type == 'xml':
            struct, _ = self._find_struct(system_name)
            if struct:
                response = make_response(Misc.process_xml(struct))
                response.headers['Content-Type'] = 'application/xml'
                return response
            return make_response('System not found', 404)
        elif data_type == 'json':
            json_data = json.loads(Util.get_mock_data('data/isystems.json'))
            if json_data.get(system_name):
                return jsonify(json_data.get(system_name))
            return make_response('System not found', 404)

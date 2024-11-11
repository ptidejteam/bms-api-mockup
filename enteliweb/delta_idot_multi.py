from flask import request, jsonify, make_response
import xml.etree.ElementTree as ET
from misc import Misc
import json
import random


class DeltaIdotMulti:

    def create_multi(self):
        # Check the query parameter for response format
        data_type = request.args.get('alt', 'xml')
        id_number = random.randint(1000000000, 9999999999)
        if data_type == 'xml':
            xml_string = request.data.decode('utf-8').lstrip()

            tree = ET.fromstring(xml_string)
            uri = 'http://bacnet.org/csml/1.2'
            ns = {'csml': uri}
            first_child = tree.find('.//csml:Real', ns)
            tree.set('xmlns', uri)
            if not first_child.get('value'):
                tree.set('name', str(id_number))
                res_code = 201
            else:
                list_element = tree.find('csml:List', ns)
                list_element.attrib['xmlns'] = ns['csml']
                tree = list_element
                res_code = 200

            response = make_response(Misc.process_xml(tree))
            response.headers['Content-Type'] = 'application/xml'
            response.status_code = res_code
            return response
        elif data_type == 'json':
            data = json.loads(request.data.decode('utf-8'))
            if data.get('lifetime', None):
                data['name'] = str(id_number)
                res_code = 201
            else:
                res_code = 200
                data = data['values']
            response = make_response(jsonify(data), res_code)
            return response

    def get_multi(self, values=None):
        data_type = request.args.get('alt', 'xml')
        if data_type == 'xml':
            multi = '''
                <?xml version="1.0" encoding="utf-8" ?>
                <List name="values" xmlns="http://bacnet.org/csml/1.2">
                    <Real name="1" value="33" via="/.bacnet/MainSite/5600/analog-value,1/present-value"/>
                    <Real name="2" value="44" via="/.bacnet/MainSite/5600/analog-value,2/present-value"/>
                </List>
            '''
            if not values:
                multi = '''
                    <?xml version="1.0" encoding="utf-8" ?>
                    <Struct xmlns="http://bacnet.org/csml/1.2">
                        <Unsigned name="lifetime" value="1200" />
                        <List name="values">
                            <Real name="1" value="33" via="/.bacnet/MainSite/5600/analog-value,1/present-value"/>
                            <Real name="2" value="44" via="/.bacnet/MainSite/5600/analog-value,2/present-value"/>
                        </List>
                    </Struct>
                '''
            response = make_response(multi)
            response.headers['Content-Type'] = 'application/xml'
            response.status_code = 200
            return response
        elif data_type == 'json':
            multi = '''
                {
                    "$base": "Struct",
                    "name": "1334888287",
                    "lifetime": {
                        "$base": "Unsigned",
                        "value": 1200
                    },
                    "values": {
                        "$base": "List",
                        "1": {
                            "$base": "Real",
                            "via": "/.bacnet/MainSite/5600/analog-value,1/present-value",
                            "value": "33"
                        },
                        "2": {
                            "$base": "Real",
                            "via": "/.bacnet/MainSite/5600/analog-value,2/present-value",
                            "value": "44"
                        }
                    }
                }
            '''
            if values:
                multi = '''
                    {
                        "$base": "List",
                        "1": {
                            "$base": "Real",
                            "via": "/.bacnet/MainSite/5600/analog-value,1/present-value",
                            "value": "33"
                        },
                        "2": {
                            "$base": "Real",
                            "via": "/.bacnet/MainSite/5600/analog-value,2/present-value",
                            "value": "44"
                        }          
                    }
                '''
            return jsonify(json.loads(multi))


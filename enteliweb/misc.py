from flask import request, jsonify, make_response
import json
import xml.etree.ElementTree as ET
import re


class Misc:

    @staticmethod
    def get_resource_data(file_path):
        # Check the query parameter for response format
        response_format = request.args.get('alt', 'xml')
        mock_data = Misc.get_mock_data(file_path)
        if response_format == 'xml':
            response = make_response(mock_data)
            response.headers['Content-Type'] = 'application/xml'
            return response
        return jsonify(json.loads(mock_data))

    @staticmethod
    def process_xml(struct):
        xml_str = ET.tostring(struct, encoding='unicode')
        # Remove namespace prefixes
        xml_str = re.sub(r'\sxmlns:ns0="[^"]+"', '', xml_str)
        xml_str = re.sub(r'ns0:', '', xml_str)
        xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_str
        return xml_str

    @staticmethod
    def get_namespace(element):
        # The namespace URI is enclosed in curly braces at the start of the tag
        if element.tag.startswith('{'):
            return element.tag.split('}')[0][1:]
        else:
            return ''

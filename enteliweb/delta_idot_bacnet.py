import copy

from flask import request, jsonify, make_response
import json
import xml.etree.ElementTree as ET
from misc import Misc
from util import Util
from datetime import datetime


class DeltaIDotBacnet:
    def __init__(self):
        self.ns = {'csml': 'http://bacnet.org/csml/1.2'}

    def get_sites(self):
        # Check the query parameter for response format
        data_type = request.args.get('alt', 'xml')
        file_path = 'data/sites.xml' if data_type == 'xml' else 'data/sites.json'
        return Misc.get_resource_data(file_path)

    def get_site_devices(self, site_name):
        data_type = request.args.get('alt', 'xml')
        skip = int(request.args.get('skip', 0))
        max_results = int(request.args.get('max_results', 100))

        if data_type == 'xml':
            tree = ET.parse('data/site_devices.xml')
            root = tree.getroot()
            if root.attrib.get('name') == site_name:
                # Define the namespace
                collections = root.findall('csml:Collection', self.ns)
                # Apply skip and max_results
                collections = collections[skip:skip + max_results]

                # Create a new XML structure for the selected links
                new_root = ET.Element('Collection', name=root.get('name'), xmlns=Misc.get_namespace(root))

                for collection in collections:
                    ET.SubElement(new_root, '{http://bacnet.org/csml/1.2}Collection',
                                  name=collection.get('name'), displayName=collection.get('displayName'),
                                  nodeType=collection.get('nodeType'), truncated=collection.get('truncated'))

                response = make_response(Misc.process_xml(new_root))
                response.headers['Content-Type'] = 'application/xml'
                return response
        elif data_type == 'json':
            json_data = json.loads(Util.get_mock_data('data/site_devices.json'))
            items = list(json_data.items())
            items = items[skip:skip + max_results]
            result = dict(items)
            return jsonify(result)

    def get_device_objects(self, site_name, device_number):
        data_type = request.args.get('alt', 'xml')
        skip = int(request.args.get('skip', 0))
        max_results = int(request.args.get('max_results', 100))
        if data_type == 'xml':
            tree = ET.parse('data/objects.xml')
            root = tree.getroot()
            root_attr = root.attrib.get('next').split('/')
            if root_attr[-2] == site_name and root_attr[-1].split('?')[-2] == device_number:
                # Define the namespace
                ns = {'csml': 'http://bacnet.org/csml/1.2'}
                collections = root.findall('csml:Object', ns)
                # Apply skip and max_results
                collections = collections[skip:skip + max_results]

                # Create a new XML structure for the selected links
                new_root = ET.Element('Collection', nodeType=root.get('nodeType'), next=root.get('next'),
                                      xmlns=Misc.get_namespace(root))

                for collection in collections:
                    ET.SubElement(new_root, '{http://bacnet.org/csml/1.2}Object',
                                  name=collection.get('name'), displayName=collection.get('displayName'),
                                  truncated=collection.get('truncated'))

                response = make_response(Misc.process_xml(new_root))
                response.headers['Content-Type'] = 'application/xml'
                return response
        elif data_type == 'json':
            json_data = json.loads(Util.get_mock_data('data/objects.json'))
            root_attr = json_data['next'].split('/')
            if root_attr[-2] == site_name and root_attr[-1].split('?')[-2] == device_number:
                items = list(json_data.items())
                items = items[skip:skip + max_results]
                result = dict(items)
                return jsonify(result)

    def get_object_properties(self, site_name, device_number, object_type, instance):
        data_type = request.args.get('alt', 'xml')
        # ideally, you will get the site and device before getting object properties
        print(f'Request parameters - site name: {site_name}, device number: {device_number}')
        if data_type == 'xml':
            tree = ET.parse('data/object_properties.xml')
            root = tree.getroot()
            if root.attrib.get('name') == f'{object_type},{instance}':
                return Misc.get_resource_data('data/object_properties.xml')
        elif data_type == 'json':
            return Misc.get_resource_data('data/object_properties.json')

    def get_trend_log_records(self, site_name, device_number, instance):
        data_type = request.args.get('alt', 'xml')
        # ideally, you will get the log records for the site, device and instance
        print(f'Request parameters - site name: {site_name}, device number: {device_number}, instance: {instance}')
        published_from = request.args.get('published-ge', 0)
        published_to = request.args.get('published-le', 0)
        sequence_from = int(request.args.get('sequence-ge', 0))
        sequence_to = int(request.args.get('sequence-le', 0))

        if data_type == 'xml':
            # implementation with timestamp of recorded data
            from_ts = datetime.strptime(published_from, "%Y-%m-%dT%H:%M:%S") if published_from != 0 else None
            to_ts = datetime.strptime(published_to, "%Y-%m-%dT%H:%M:%S") if published_to != 0 else None
            tree = ET.parse('data/trend_log_records.xml')
            root = tree.getroot()
            sequences = root.findall('csml:Sequence', self.ns)
            new_root = ET.Element('List', name=root.get('name'), xmlns=Misc.get_namespace(root))

            for sequence in sequences:
                sequence_ts = sequence.find('csml:DateTime', self.ns).attrib['value']
                sequence_ts = datetime.strptime(sequence_ts, "%Y-%m-%dT%H:%M:%S.%f")
                if from_ts and to_ts:
                    if from_ts <= sequence_ts <= to_ts:
                        new_root.append(copy.deepcopy(sequence))
                elif from_ts:
                    if sequence_ts >= from_ts:
                        new_root.append(copy.deepcopy(sequence))
                else:
                    new_root.append(copy.deepcopy(sequence))
            response = make_response(Misc.process_xml(new_root))
            response.headers['Content-Type'] = 'application/xml'
            return response
        elif data_type == 'json':
            # implementation with sequence numbers
            json_data = json.loads(Util.get_mock_data('data/trend_log_records.json'))
            del json_data['$base']
            filtered_json = {'$base': 'List'}
            for key, value in json_data.items():
                print(key, value)
                if sequence_from != 0 and sequence_to != 0:
                    if sequence_from <= int(key) <= sequence_to:
                        filtered_json[key] = value
                elif sequence_from != 0:
                    if int(key) >= sequence_from:
                        filtered_json[key] = value
                else:
                    filtered_json[key] = value
            return jsonify(filtered_json)

    def write_property_value(self, site_name, device_number, object_type, instance, property_name):
        data_type = request.args.get('alt', 'xml')
        priority = request.args.get('priority', 0)
        print(f'Request parameters - site name: {site_name}, device number: {device_number}, '
              f'object id: {object_type}, instance: {instance}, property name: {property_name}, '
              f'priority: {priority}')
        if data_type == 'xml':
            xml_string = request.data.decode('utf-8').lstrip()
            # ideally, you will update the object properties here.
            print(f'Request data: {xml_string}')
            res_xml = '''
                <?xml version="1.0" encoding="UTF-8"?>
<               <Real error="-1" errorText="OK" xmlns="http://bacnet.org/csml/1.2"/>
            '''
            response = make_response(res_xml)
            response.headers['Content-Type'] = 'application/xml'
            response.status_code = 200
            return response
        elif data_type == 'json':
            data = json.loads(request.data.decode('utf-8'))
            print(f'Request data: {data}')
            res_json = '''
                {
                    "$base" : "Real",
                    "error" : "-1",
                    "errorText" : "OK"
                }
            '''
            return jsonify(json.loads(res_json))

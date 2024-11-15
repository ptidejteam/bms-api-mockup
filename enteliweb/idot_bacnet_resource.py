from flask_restx import Namespace, Resource
from delta_idot_bacnet import DeltaIDotBacnet

i_dot_bacnet = DeltaIDotBacnet()

api = Namespace('enteliweb_i_dot_bacnet', description='Get bacnet network, device and object information')


@api.route('/')
class IDotBacnetSites(Resource):
    def get(self):
        """Get  list of sites resource returns a list of the sites known to enteliWEB"""
        return i_dot_bacnet.get_sites()


@api.route('/<site_name>')
class IDotBacnetSiteDevices(Resource):
    def get(self, site_name):
        """Get list of devices for site resource returns a list of devices for the specified site"""
        return i_dot_bacnet.get_site_devices(site_name)


@api.route('/<site_name>/<device_number>')
class IDotBacnetSiteDeviceObjects(Resource):
    def get(self, site_name, device_number):
        """Get list of objects from device resource returns a list of objects,
        both BACnet standard objects and Delta proprietary objects, on the specified device."""
        return i_dot_bacnet.get_device_objects(site_name, device_number)


@api.route('/<site_name>/<device_number>/<object_type>,<instance>')
class IDotBacnetSiteDeviceObjectProperties(Resource):
    def get(self, site_name, device_number, object_type, instance):
        """Get list of properties and values from object resource returns a list of all properties,
        both BACnet standard and proprietary, and their values for the specified object."""
        return i_dot_bacnet.get_object_properties(site_name, device_number, object_type, instance)


@api.route('/<site_name>/<device_number>/trend-log,<instance>/log-buffer')
class IDotBacnetTrendLogRecords(Resource):
    def get(self, site_name, device_number, instance):
        """The get log records from trend log object resource returns records from the TL object's
        log-buffer property. When requested log records are not held in the TL object, this
        resource gets log records that may be archived on a CopperCube, Historian or enteliVAULT archieve."""
        return i_dot_bacnet.get_trend_log_records(site_name, device_number, instance)


@api.route('/<site_name>/<device_number>/<object_type>,<instance>/<property_name>')
class IDotBacnetTrendLogRecords(Resource):
    def put(self, site_name, device_number, object_type, instance, property_name):
        """The write value to object property resource writes a value to a BACnet standard property for both commandable
        and non-commandable properties"""
        return i_dot_bacnet.write_property_value(site_name, device_number, object_type, instance, property_name)

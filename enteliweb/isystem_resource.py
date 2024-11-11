from flask_restx import Namespace, Resource
from delta_isystems import DeltaISystem

i_system = DeltaISystem()

api = Namespace('enteliweb_i_systems', description='Systems operations')


@api.route('/')
class ISystemListResource(Resource):
    def get(self):
        """List all systems"""
        return i_system.get_systems()


@api.route('/<system_name>')
class ISystemProperty(Resource):
    def get(self, system_name):
        """Get system properties"""
        return i_system.get_system_property(system_name)

    def put(self, system_name):
        """write multiple system properties"""
        return i_system.write_multiple_property_values(system_name)

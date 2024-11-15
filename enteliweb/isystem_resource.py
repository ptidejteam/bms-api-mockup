from flask_restx import Namespace, Resource
from delta_isystems import DeltaISystem

i_system = DeltaISystem()

api = Namespace('enteliweb_i_systems', description='Systems operations')


@api.route('/')
class ISystemListResource(Resource):
    def get(self):
        """The Get List of All Systems resource is represented by the properties described in the Delta_ISystems
        Properties table, except that it does not return object values."""
        return i_system.get_systems()


@api.route('/<system_name>')
class ISystemProperty(Resource):
    def get(self, system_name):
        """The Get All System Properties for a System resource returns all properties for the specified system,
        including object values."""
        return i_system.get_system_property(system_name)

    def put(self, system_name):
        """The Write Multiple Property Values in a System resource allows an application to change multiple properties
        in a system, in one web service request."""
        return i_system.write_multiple_property_values(system_name)

from flask_restx import Namespace, Resource
from delta_idot_multi import DeltaIdotMulti

i_dot_multi = DeltaIdotMulti()

api = Namespace('enteliweb_i_dot_multi', description='Idot Multi')


@api.route('/')
class IDotMultiCreate(Resource):
    def post(self):
        """The Create Multi resource creates a multi by POSTing a properly-constructed <Struct> structure
        specifying a non-zero lifetime. The presence of the <Any> elements indicates that nothing is written
        to the object properties."""
        return i_dot_multi.create_multi()


@api.route('/<int:id_number>/', defaults={'values': False})
@api.route('/<int:id_number>/values', defaults={'values': True})
class IDotMultiRead(Resource):
    def get(self, id_number, values):
        """The Get Values for Object Properties resource returns the values of the object properties
        defined by one multi or by all multis."""
        return i_dot_multi.get_multi(id_number, values)




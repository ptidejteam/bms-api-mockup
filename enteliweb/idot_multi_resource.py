from flask_restx import Namespace, Resource
from delta_idot_multi import DeltaIdotMulti

i_dot_multi = DeltaIdotMulti()

api = Namespace('enteliweb_i_dot_multi', description='Idot Multi')


@api.route('/')
class IDotMultiCreate(Resource):
    def post(self):
        """Get trend logs"""
        return i_dot_multi.create_multi()


@api.route('/<id_number>')
class IDotMultiRead(Resource):
    def get(self, id_number):
        """Get trend logs"""
        return i_dot_multi.get_multi()


@api.route('/<id_number>/values')
class IDotMultiRead(Resource):
    def get(self, id_number):
        """Get trend logs"""
        return i_dot_multi.get_multi('values')

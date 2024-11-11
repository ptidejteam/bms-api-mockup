from flask_restx import Namespace, Resource
from delta_idot_data import DeltaIdotData

i_dot_data = DeltaIdotData()

api = Namespace('enteliweb_i_dot_data', description='Idot Data')


@api.route('/histories')
class IDotDataTrendLogs(Resource):
    def get(self):
        """Get trend logs"""
        return i_dot_data.get_trend_logs()

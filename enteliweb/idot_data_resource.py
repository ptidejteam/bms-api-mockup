from flask_restx import Namespace, Resource
from delta_idot_data import DeltaIdotData

i_dot_data = DeltaIdotData()

api = Namespace('enteliweb_i_dot_data', description='Idot Data')


@api.route('/histories')
class IDotDataTrendLogs(Resource):
    def get(self):
        """The Get a List of Histories or Trend Log Objects resource returns a list of references to the BACnet
        standard trend log objects that the enteliWEB server is aware of on all devices on all sites."""
        return i_dot_data.get_trend_logs()

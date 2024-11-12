class Util:

    @staticmethod
    def get_mock_data(file_path):
        with open(file_path, 'r') as file:
            return file.read()

import json
from exporter.exporter import Exporter
from datetime import datetime


class JsonExporter(Exporter):

    def __init__(self, file_name):
        if file_name is None or file_name == '':
            file_name = f'export_{datetime.now().strftime("%Y%m%d%H%M")}.json'
        super().__init__(file_name)

    def export(self, results: list):
        with open(self.file_name, 'w') as json_file:
            json.dump(results, json_file, indent=4)

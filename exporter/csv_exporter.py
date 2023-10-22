import csv
from datetime import datetime
from exporter.exporter import Exporter


class CsvExporter(Exporter):

    def __init__(self, file_name):
        if file_name is None or file_name == '':
            file_name = f'export_{datetime.now().strftime("%Y%m%d%H%M")}.csv'
        super().__init__(file_name)

    def export(self, results: list):
        with open(self.file_name, 'w', newline='') as csv_file:
            field_names = ['source', 'to']
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            for result in results:
                writer.writerow(result)

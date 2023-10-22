from exporter.json_exporter import JsonExporter
from exporter.xml_exporter import XmlExporter
from exporter.csv_exporter import CsvExporter
from exporter.sql_exporter import SqlExporter


def load_exporter(export_type: str, file_name: str):
    if export_type is None or export_type == '':
        raise ValueError('Export type can not be a none or empty.')

    if export_type.lower() == 'json':
        return JsonExporter(file_name)
    elif export_type.lower() == 'csv':
        return CsvExporter(file_name)
    elif export_type.lower() == 'xml':
        return XmlExporter(file_name)
    elif export_type.lower() == 'sql':
        return SqlExporter(file_name)
    else:
        raise ValueError('Unsupported export type.')

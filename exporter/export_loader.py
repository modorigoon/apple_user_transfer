from exporter.migration_sql_exporter import MigrationSqlExporter
from exporter.transfer_json_exporter import TransferJsonExporter
from exporter.transfer_xml_exporter import TransferXmlExporter
from exporter.transfer_csv_exporter import TransferCsvExporter
from exporter.transfer_sql_exporter import TransferSqlExporter


def load_exporter(execute_mode: str, export_type: str, file_name: str):
    if export_type is None or export_type == '':
        raise ValueError('Export type can not be a none or empty.')

    if str(execute_mode).lower() == 'transfer':
        if export_type.lower() == 'json':
            return TransferJsonExporter(file_name)
        elif export_type.lower() == 'csv':
            return TransferCsvExporter(file_name)
        elif export_type.lower() == 'xml':
            return TransferXmlExporter(file_name)
        elif export_type.lower() == 'sql':
            return TransferSqlExporter(file_name)
        else:
            raise ValueError('Unsupported export type.')
    elif str(execute_mode).lower() == 'migration':
        if export_type.lower() == 'sql':
            return MigrationSqlExporter(file_name)

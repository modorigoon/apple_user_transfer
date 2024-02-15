from datetime import datetime
from exporter.exporter import Exporter


class TransferSqlExporter(Exporter):

    def __init__(self, file_name):
        if file_name is None or file_name == '':
            file_name = f'export_{datetime.now().strftime("%Y%m%d%H%M")}.sql'

        super().__init__(file_name)
        self.__table_name = 'subs'
        self.__column_name = 'sub'

    def set_table_name(self, table_name):
        if table_name is not None and table_name != '':
            self.__table_name = table_name

    def set_column_name(self, column_name):
        if column_name is not None and column_name != '':
            self.__column_name = column_name

    def generate_update_query(self, source_sub, transfer_sub):
        return f'UPDATE {self.__table_name} SET {self.__column_name}="{transfer_sub}" ' \
               f'WHERE {self.__column_name}="{source_sub}";'

    def export(self, results):
        with open(self.file_name, 'w') as sql_file:
            for result in results:
                sql_file.write(self.generate_update_query(result['source'], result['to']) + '\n')

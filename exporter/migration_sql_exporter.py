from datetime import datetime
from exporter.exporter import Exporter


class MigrationSqlExporter(Exporter):

    def __init__(self, file_name):
        if file_name is None or file_name == '':
            file_name = f'export_{datetime.now().strftime("%Y%m%d%H%M")}.sql'

        super().__init__(file_name)
        self.__table_name = 'subs'
        self.__email_column_name = 'email'
        self.__sub_column_name = 'sub'

    def set_table_name(self, table_name):
        if table_name is not None and table_name != '':
            self.__table_name = table_name

    def set_column_name(self, email_column_name, sub_column_name):
        if email_column_name is not None and email_column_name != '':
            self.__email_column_name = email_column_name
        if sub_column_name is not None and sub_column_name != '':
            self.__sub_column_name = sub_column_name

    def generate_update_query(self, transfer_sub, sub, email):
        update_email_query = ''
        if email is not None:
            update_email_query = f', {self.__email_column_name}="{email}" '
        return (f'UPDATE {self.__table_name} SET '
                f'{self.__sub_column_name}="{sub}"{update_email_query}'
                f' WHERE {self.__sub_column_name}="{transfer_sub}" AND id > 0;')

    def export(self, results):
        with open(self.file_name, 'w') as sql_file:
            for result in results:
                sql_file.write(self.generate_update_query(result['source'], result['to'], result['email']) + '\n')

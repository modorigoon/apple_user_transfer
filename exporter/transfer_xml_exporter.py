import xml.etree.ElementTree as Es
from datetime import datetime
from exporter.exporter import Exporter


class TransferXmlExporter(Exporter):

    def __init__(self, file_name):
        if file_name is None or file_name == '':
            file_name = f'export_{datetime.now().strftime("%Y%m%d%H%M")}.xml'
        super().__init__(file_name)

    def export(self, results: list):
        root = Es.Element('subs')
        for result in results:
            sub = Es.SubElement(root, 'sub')
            Es.SubElement(sub, 'source').text = result['source']
            Es.SubElement(sub, 'to').text = result['to']

        xml = Es.tostring(root, encoding='utf-8').decode('utf-8')

        with open(self.file_name, 'w') as xml_file:
            xml_file.write(xml)

import os
import xml.etree.ElementTree as ET
from datetime import datetime

class XMLLogger:
    def __init__(self, filename):
        self.filename = filename
        if os.path.exists(filename):
            tree = ET.parse(filename)
            self.root = tree.getroot()
        else:
            self.root = ET.Element('logs')

    def add_log(self, evento, messaggio):
        log_entry = ET.SubElement(self.root, 'log')
        timestamp = datetime.now().isoformat()
        ET.SubElement(log_entry, 'timestamp').text = timestamp
        ET.SubElement(log_entry, 'evento').text = evento
        ET.SubElement(log_entry, 'messaggio').text = messaggio

    def save(self):
        tree = ET.ElementTree(self.root)
        tree.write(self.filename, encoding='utf-8', xml_declaration=True)

def print_logs_as_table(filename):
    import xml.etree.ElementTree as ET
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        # Intestazione
        print(f"{'Timestamp':26} | {'Evento':11} | Messaggio")
        print('-'*70)
        for log in root.findall('log'):
            timestamp = log.find('timestamp').text if log.find('timestamp') is not None else ''
            evento = log.find('evento').text if log.find('evento') is not None else ''
            messaggio = log.find('messaggio').text if log.find('messaggio') is not None else ''
            print(f"{timestamp:25} | {evento:10} | {messaggio}")
    except Exception as e:
        print(f"Errore nella lettura del file XML: {e}")
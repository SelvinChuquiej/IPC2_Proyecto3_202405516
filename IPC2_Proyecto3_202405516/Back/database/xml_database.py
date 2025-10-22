import os
from typing import Dict, Optional 
import xml.etree.ElementTree as ET

class XMLDatabase:
    DEFAULT_FILES = {
        'recursos.xml': 'recursos',
        'categorias.xml': 'categorias',
        'clientes.xml': 'clientes',
        'instancias.xml': 'instancias',
        'facturas.xml': 'facturas',
    }

    def __init__(self, data_folder: str = "./database/databaseXML/"):
        self.data_folder = data_folder
        self.ensure_data_folder()

    def ensure_data_folder(self):
        os.makedirs(self.data_folder, exist_ok=True)

    def initialize_database(self, files: Optional[Dict[str, str]] = None):
        files = files or self.DEFAULT_FILES
        for filename, root_element in files.items():
            filepath = os.path.join(self.data_folder, filename)
            if not os.path.exists(filepath):
                root  = ET.Element(root_element)
                tree = ET.ElementTree(root)
                tree.write(filepath, encoding='utf-8', xml_declaration=True)

    def get_file_path(self, entity_name: str) -> str:
        name = os.path.basename(entity_name)
        if not name.endswith('.xml'):
            name = f"{name}.xml"
        return os.path.join(self.data_folder, name)
import os
from typing import Dict, Optional, Any, List
import xml.etree.ElementTree as ET

class XMLDatabase:
    DEFAULT_FILES = {
        'recursos.xml': 'recursos',
        'categorias.xml': 'categorias',
        'clientes.xml': 'clientes',
        'instancias.xml': 'instancias',
        'facturas.xml': 'facturas',
        'consumos.xml': 'consumos',
    }

    def __init__(self, data_folder: str = "./database/databaseXML/"):
        self.data_folder = data_folder
        self.ensure_data_folder()
        self.initialize_database()

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

    def guardar_recurso(self, recurso_data: Dict[str, Any]) -> bool:
        try:
            filepath = self.get_file_path('recursos.xml')
            tree = ET.parse(filepath)
            root = tree.getroot()

            recurso_existente = None
            for elem in root.findall('recurso'):
                if elem.get('id') == str(recurso_data['id_recurso']):
                    recurso_existente = elem
                    break

            if recurso_existente is not None:
                root.remove(recurso_existente)

            recurso_elem = ET.Element('recurso', id=str(recurso_data['id_recurso']))
            ET.SubElement(recurso_elem, 'nombre').text = recurso_data['nombre']
            ET.SubElement(recurso_elem, 'abreviatura').text = recurso_data['abreviatura']
            ET.SubElement(recurso_elem, 'metrica').text = recurso_data['metrica']
            ET.SubElement(recurso_elem, 'tipo').text = recurso_data['tipo']
            ET.SubElement(recurso_elem, 'valorXhora').text = str(recurso_data['valor_x_hora'])

            root.append(recurso_elem)
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
            return True

        except Exception as e:
            print(f"Error al guardar recurso: {e}")
            return False

    def guardar_cliente(self, cliente_data: Dict[str, Any]) -> bool:
        try:
            filepath = self.get_file_path('clientes.xml')
            tree = ET.parse(filepath)
            root = tree.getroot()

            cliente_existente = None
            for elem in root.findall('cliente'):
                if elem.get('nit') == cliente_data['nit']:
                    cliente_existente = elem
                    break

            if cliente_existente is not None:
                root.remove(cliente_existente)

            cliente_elem = ET.Element('cliente', nit=cliente_data['nit'])
            ET.SubElement(cliente_elem, 'nombre').text = cliente_data['nombre']
            ET.SubElement(cliente_elem, 'usuario').text = cliente_data['usuario']
            ET.SubElement(cliente_elem, 'clave').text = cliente_data['clave']
            ET.SubElement(cliente_elem, 'direccion').text = cliente_data['direccion']
            ET.SubElement(cliente_elem, 'correoElectronico').text = cliente_data['correo_electronico']

            '''if cliente_data.get('instancias'):
                lista_instancias = ET.SubElement(cliente_elem, 'listaInstancias')
                for instancia in cliente_data['instancias']:
                    instancia_elem = ET.SubElement(lista_instancias, 'instancia', id=str(instancia['id']))
                    ET.SubElement(instancia_elem, 'idConfiguracion').text = str(instancia['id_configuracion'])
                    ET.SubElement(instancia_elem, 'nombre').text = instancia['nombre']
                    ET.SubElement(instancia_elem, 'fechaInicio').text = instancia['fecha_inicio']
                    ET.SubElement(instancia_elem, 'estado').text = instancia['estado']
                    if instancia.get('fecha_final'):
                        ET.SubElement(instancia_elem, 'fechaFinal').text = instancia['fecha_final']'''

            root.append(cliente_elem)
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
            return True

        except Exception as e:
            print(f"Error al guardar cliente: {e}")
            return False
        
    def guardar_categoria(self, categoria_data: Dict[str, Any]) -> bool:
        try:
            filepath = self.get_file_path('categorias.xml')
            tree = ET.parse(filepath)
            root = tree.getroot()

            categoria_existente = None
            for elem in root.findall('categoria'):
                if elem.get('id') == str(categoria_data['id_Categoria']):
                    categoria_existente = elem
                    break

            if categoria_existente is not None:
                root.remove(categoria_existente)

            categoria_elem = ET.Element('categoria', id=str(categoria_data['id_Categoria']))
            ET.SubElement(categoria_elem, 'nombre').text = categoria_data['nombre']
            ET.SubElement(categoria_elem, 'descripcion').text = categoria_data['descripcion']
            ET.SubElement(categoria_elem, 'cargaTrabajo').text = categoria_data['carga_trabajo']

            root.append(categoria_elem)
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
            return True
        
        except Exception as e:
            print(f"Error al guardar categoria: {e}")
            return False

    def guardar_consumo(self, consumo_data: Dict[str, Any]) -> bool:
        try:
            filepath = self.get_file_path('consumos.xml')
            tree = ET.parse(filepath)
            root = tree.getroot()

            consumo_existente = False
            for elem in root.findall('consumo'):
                mismo_cliente = elem.get('nitCliente') == consumo_data['nit_cliente']
                misma_instancia = elem.get('idInstancia') == str(consumo_data['id_instancia'])
                tiempo_elem = elem.find('tiempo')
                fecha_elem = elem.find('fechahora')

                tiempo_exist = tiempo_elem.text if tiempo_elem is not None else ""
                fecha_exist = fecha_elem.text if fecha_elem is not None else ""

                if mismo_cliente and misma_instancia and fecha_exist == consumo_data['fecha_hora']:
                    consumo_existente = True
                    break

            if not consumo_existente:
                consumo_elem = ET.Element('consumo',  nitCliente=consumo_data['nit_cliente'], idInstancia=str(consumo_data['id_instancia']))
                ET.SubElement(consumo_elem, 'tiempo').text = str(consumo_data['tiempo'])
                ET.SubElement(consumo_elem, 'fechahora').text = consumo_data['fecha_hora']

                root.append(consumo_elem)
                tree.write(filepath, encoding='utf-8', xml_declaration=True)
                return True

        except Exception as e:
            print(f"Error al guardar consumo: {e}")
            return False

    def inicializar_sistema(self) -> bool:
        try:
            for filename in self.DEFAULT_FILES.keys():
                filepath = os.path.join(self.data_folder, filename)
                if os.path.exists(filepath):
                    os.remove(filepath)

            self.initialize_database()
            return True

        except Exception as e:
            print(f"Error al inicializar sistema: {e}")
            return False
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
        'configuraciones.xml': 'configuraciones'
    }

    def __init__(self, data_folder: str = "./database/databaseXML/"):
        self.data_folder = data_folder
        self.ensure_data_folder()
        self.initialize_database()

    # Asegurar que la carpeta de datos exista
    def ensure_data_folder(self):
        os.makedirs(self.data_folder, exist_ok=True)

    # Inicializar archivos XML si no existen
    def initialize_database(self, files: Optional[Dict[str, str]] = None):
        files = files or self.DEFAULT_FILES
        for filename, root_element in files.items():
            filepath = os.path.join(self.data_folder, filename)
            if not os.path.exists(filepath):
                root  = ET.Element(root_element)
                tree = ET.ElementTree(root)
                tree.write(filepath, encoding='utf-8', xml_declaration=True)

    # Obtener ruta del archivo XML correspondiente a una entidad
    def get_file_path(self, entity_name: str) -> str:
        name = os.path.basename(entity_name)
        if not name.endswith('.xml'):
            name = f"{name}.xml"
        return os.path.join(self.data_folder, name)

    # Guardar recurso en la base de datos XML
    def guardar_recurso(self, recurso_data: Dict[str, Any]) -> bool:
        try:
            filepath = self.get_file_path('recursos.xml')
            tree = ET.parse(filepath)
            root = tree.getroot()

            id_recurso = str(recurso_data.get('id_recurso') or recurso_data.get('id'))
            for recurso in root.findall('recurso'):
                if recurso.get('id') == id_recurso:
                    raise ValueError(f"El recurso con ID {id_recurso} ya existe.")

            recurso_elem = ET.Element('recurso', id=str(recurso_data.get('id_recurso', '')))
            ET.SubElement(recurso_elem, 'nombre').text = recurso_data.get('nombre', '')
            ET.SubElement(recurso_elem, 'abreviatura').text = recurso_data.get('abreviatura', '')
            ET.SubElement(recurso_elem, 'metrica').text = recurso_data.get('metrica', '')
            ET.SubElement(recurso_elem, 'tipo').text = recurso_data.get('tipo', '')
            ET.SubElement(recurso_elem, 'valorXhora').text = str(recurso_data.get('valor_x_hora', ''))

            root.append(recurso_elem)
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
            return True

        except ValueError as v:
            print(f"{v}")
            return "exists"
        except Exception as e:
            print(f"Error al guardar recurso: {e}")
            return False

    # Guardar cliente en la base de datos XML
    def guardar_cliente(self, cliente_data: Dict[str, Any]) -> bool:
        try:
            filepath = self.get_file_path('clientes.xml')
            tree = ET.parse(filepath)
            root = tree.getroot()

            nit_cliente = str(cliente_data.get('nit'))
            for cli in root.findall('cliente'):
                if cli.get('nit') == nit_cliente:
                    raise ValueError(f"El cliente con NIT {nit_cliente} ya existe.")
                
            cliente_elem = ET.Element('cliente', nit=nit_cliente)
            ET.SubElement(cliente_elem, 'nombre').text = cliente_data.get('nombre', '')
            ET.SubElement(cliente_elem, 'usuario').text = cliente_data.get('usuario', '')
            ET.SubElement(cliente_elem, 'clave').text = cliente_data.get('clave', '')
            ET.SubElement(cliente_elem, 'direccion').text = cliente_data.get('direccion', '')
            ET.SubElement(cliente_elem, 'correoElectronico').text = cliente_data.get('correo', '') or cliente_data.get('correo_electronico', '')

            root.append(cliente_elem)
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
            return True

        except ValueError as v: 
            print(f"{v}")
            return "exists"
        except Exception as e:
            print(f"Error al guardar cliente: {e}")
            return False
        
    # Guardar categoria en la base de datos XML
    def guardar_categoria(self, categoria_data: Dict[str, Any]) -> bool:
        try:
            filepath = self.get_file_path('categorias.xml')
            tree = ET.parse(filepath)
            root = tree.getroot()

            id_categoria = str(categoria_data.get('id_Categoria') or categoria_data.get('id'))
            for cat in root.findall('categoria'):
                if cat.get('id') == id_categoria:
                    raise ValueError(f"La categoría con ID {id_categoria} ya existe.")

            categoria_elem = ET.Element('categoria', id=str(categoria_data['id_Categoria']))
            ET.SubElement(categoria_elem, 'nombre').text = categoria_data.get('nombre', '')
            ET.SubElement(categoria_elem, 'descripcion').text = categoria_data.get('descripcion', '')
            ET.SubElement(categoria_elem, 'cargaTrabajo').text = categoria_data.get('carga_trabajo', '')

            root.append(categoria_elem)
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
            return True
        except ValueError as v:
            print(f"{v}")
            return "exists"
        except Exception as e:
            print(f"Error al guardar categoria: {e}")
            return False

    # Guardar consumo en la base de datos XML
    def guardar_consumo(self, consumo_data: Dict[str, Any]) -> bool:
        try:
            filepath = self.get_file_path('consumos.xml')
            tree = ET.parse(filepath)
            root = tree.getroot()

            consumo_existente = False
            for elem in root.findall('consumo'):
                mismo_cliente = elem.get('nitCliente') == consumo_data.get('nit_cliente', '')
                misma_instancia = elem.get('idInstancia') == str(consumo_data.get('id_instancia', ''))
                tiempo_elem = elem.find('tiempo')
                fecha_elem = elem.find('fechahora')

                tiempo_exist = tiempo_elem.text if tiempo_elem is not None else ""
                fecha_exist = fecha_elem.text if fecha_elem is not None else ""

                if mismo_cliente and misma_instancia and fecha_exist == consumo_data['fecha_hora']:
                    consumo_existente = True
                    break

            if not consumo_existente:
                consumo_elem = ET.Element('consumo',  nitCliente=consumo_data.get('nit_cliente', ''), idInstancia=str(consumo_data.get('id_instancia', '')))
                ET.SubElement(consumo_elem, 'tiempo').text = str(consumo_data.get('tiempo', ''))
                ET.SubElement(consumo_elem, 'fechahora').text = consumo_data.get('fecha_hora', '')

                root.append(consumo_elem)
                tree.write(filepath, encoding='utf-8', xml_declaration=True)
                return True

        except Exception as e:
            print(f"Error al guardar consumo: {e}")
            return False

    # Guardar configuracion en la base de datos XML
    def guardar_configuracion(self, configuracion_data: Dict[str, Any]) -> bool:
        try:
            filepath = self.get_file_path('configuraciones.xml')
            tree = ET.parse(filepath)
            root = tree.getroot()

            id_config = str(configuracion_data.get('id_configuracion') or configuracion_data.get('id') or '')
            id_categoria = str(configuracion_data.get('id_categoria', ''))
            for conf in root.findall('configuracion'):
                if conf.get('id') == id_config:
                    raise ValueError(f"La configuración con ID {id_config} ya existe.")

            configuracion_elem = ET.Element('configuracion', id=str(configuracion_data.get('id_configuracion', '')), idCategoria=id_categoria)
            ET.SubElement(configuracion_elem, 'nombre').text = configuracion_data.get('nombre', '')
            ET.SubElement(configuracion_elem, 'descripcion').text = configuracion_data.get('descripcion', '')

            recursos = configuracion_data.get('recursos', [])

            if recursos:
                recursos_elem = ET.SubElement(configuracion_elem, 'recursosConfiguracion')
                for recurso in recursos:
                    id_recurso = str(recurso.get('id'))
                    cantidad = str(recurso.get('cantidad'))
                    ET.SubElement(recursos_elem, 'recurso', id=id_recurso).text = cantidad

            root.append(configuracion_elem)
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
            return True

        except ValueError as v:
            print(f"{v}")
            return "exists"
        except Exception as e:
            print(f"Error al guardar configuracion: {e}")
            return False

    # Guardar instancia en la base de datos XML
    def guardar_instancia(self, instancia_data: Dict[str, Any]) -> bool:
        try:
            filepath = self.get_file_path('instancias.xml')
            tree = ET.parse(filepath)
            root = tree.getroot()

            id_instancia = str(instancia_data.get('id_instancia') or instancia_data.get('id'))
            id_configuracion = str(instancia_data.get('idConfiguracion') or instancia_data.get('id_configuracion') or '')
            nit_cliente = str(instancia_data.get('nitCliente') or instancia_data.get('nit_cliente') or '')

            for inst in root.findall('instancia'):
                if inst.get('id') == id_instancia:
                    raise ValueError(f"La instancia con ID {id_instancia} ya existe.")

            instancia_elem = ET.Element('instancia', id=id_instancia)
            ET.SubElement(instancia_elem, 'idConfiguracion').text = id_configuracion
            ET.SubElement(instancia_elem, 'nitCliente').text = nit_cliente
            ET.SubElement(instancia_elem, 'nombre').text = instancia_data.get('nombre', '')
            ET.SubElement(instancia_elem, 'fechaInicio').text = instancia_data.get('fecha_inicio', '')
            ET.SubElement(instancia_elem, 'estado').text = instancia_data.get('estado', '')
            if instancia_data.get('fecha_final'):
                ET.SubElement(instancia_elem, 'fechaFinal').text = instancia_data.get('fecha_final', '')

            root.append(instancia_elem)
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
            return True

        except ValueError as v:
            print(f"{v}")
            return "exists"
        except Exception as e:
            print(f"Error al guardar instancia: {e}")
            return False
    
    # Inicializar sistema
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
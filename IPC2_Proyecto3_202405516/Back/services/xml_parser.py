import xml.etree.ElementTree as ET
from utils import Validators
from models import Recurso, Categoria, Cliente, Configuracion, Instancia

class XMLParser:
    def __init__(self):
        self.validators = Validators()

    def procesar_configuracion(self, xml_content):
        try:
            root = ET.fromstring(xml_content)
            resultados = {
                'recursos_procesados': [],
                'categorias_procesadas': [],
                'clientes_procesados': [],
                'errores': []
            }
            
            #Procesar recursos
            lista_recursos = root.find('listaRecursos')
            if lista_recursos is not None:
                for recurso_elem in lista_recursos.findall('recurso'):
                    try:
                        recurso = self._procesar_recurso(recurso_elem)
                        resultados['recursos_procesados'].append(recurso)
                    except Exception as e:
                        resultados['errores'].append(f"Error en recurso {recurso_elem.get('id')}: {str(e)}")

            # Procesar categorias
            lista_categorias = root.find('listaCategorias')
            if lista_categorias is not None:
                for categoria_elem in lista_categorias.findall('categoria'):
                    try:
                        categoria = self._procesar_categoria(categoria_elem)
                        resultados['categorias_procesadas'].append(categoria)
                    except Exception as e:
                        resultados['errores'].append(f"Error en categoria {categoria_elem.get('id')}: {str(e)}")

            # Procesar clientes 
            lista_clientes = root.find('listaClientes') 
            if lista_clientes is not None:
                for cliente_elem in lista_clientes.findall('cliente'):
                    try:
                        cliente = self._procesar_clientes(cliente_elem)
                        resultados['clientes_procesados'].append(cliente)
                    except Exception as e:
                        resultados['errores'].append(f"Error en cliente {cliente_elem.get('nit')}: {str(e)}")

            return resultados

        except ET.ParseError as e:
            raise Exception(f"Error al parsear XML: {str(e)}")
        
    def _procesar_recurso(self, recurso_elem):
        id_recurso = int(recurso_elem.get('id'))
        nombre = recurso_elem.find('nombre').text.strip()
        abreviatura = recurso_elem.find('abreviatura').text.strip()
        metrica = recurso_elem.find('metrica').text.strip()
        tipo = recurso_elem.find('tipo').text.strip()
        valor_x_hora = float(recurso_elem.find('valorXhora').text.strip())

        if not self.validators.tipo_recurso(tipo):
            raise Exception(f"Tipo de recurso inválido: {tipo}")
        
        return Recurso(id_recurso, nombre, abreviatura, metrica, tipo, valor_x_hora)
    
    def _procesar_categoria(self, categoria_elem):
        id_categoria = int(categoria_elem.get('id'))
        nombre = categoria_elem.find('nombre').text.strip()
        descripcion = categoria_elem.find('descripcion').text.strip()
        carga_trabajo = categoria_elem.find('cargaTrabajo').text.strip()

        categoria = Categoria(id_categoria, nombre, descripcion, carga_trabajo)

        lista_configuraciones = categoria_elem.find('listaConfiguraciones')
        if lista_configuraciones is not None:
            for config_elem in lista_configuraciones.findall('configuracion'):
                configuracion = self._procesar_configuracion_element(config_elem)
                categoria.agregar_configuracion(configuracion)

        return categoria
    
    def _procesar_configuracion_element(self, config_elem):
        id_config = int(config_elem.get('id'))
        nombre = config_elem.find('nombre').text.strip()
        descripcion = config_elem.find('descripcion').text.strip()
        configuracion = Configuracion(id_config, nombre, descripcion)

        recursos_config = config_elem.find('recursosConfiguracion')
        if recursos_config is not None:
            for recurso_elem in recursos_config.findall('recurso'):
                id_recurso = int(recurso_elem.get('id'))
                recurso = float(recurso_elem.text.strip())
                configuracion.agregar_recurso(id_recurso, recurso)

        return configuracion
    
    def _procesar_clientes(self, cliente_elem):
        nit  = cliente_elem.get('nit').strip()
        nombre = cliente_elem.find('nombre').text.strip()
        usuario = cliente_elem.find('usuario').text.strip()
        clave = cliente_elem.find('clave').text.strip()
        direccion = cliente_elem.find('direccion').text.strip()
        correo = cliente_elem.find('correoElectronico').text.strip()

        if not self.validators.validar_nit(nit):
            raise Exception(f"NIT inválido: {nit}")
        
        cliente = Cliente(nit, nombre, usuario, clave, direccion, correo)

        #Procesar instancias
        lista_instancias = cliente_elem.find('listaInstancias')
        if lista_instancias is not None:
            for instancia_elem in lista_instancias.findall('instancia'):
                instancia = self._procesar_instancia(instancia_elem)
                cliente.agregar_instancia(instancia)

        return cliente
    
    def _procesar_instancia(self, instancia_elem):
        id_instancia = int(instancia_elem.get('id'))
        id_configuracion = int(instancia_elem.find('idConfiguracion').text.strip())
        nombre = instancia_elem.find('nombre').text.strip()
        
        fecha_inicio_text = instancia_elem.find('fechaInicio').text
        fecha_inicio = self.validators.extraer_primera_fecha(fecha_inicio_text)
        if not fecha_inicio:
            raise Exception(f"Fecha de inicio inválida: {fecha_inicio_text}")
        
        estado = instancia_elem.find('estado').text.strip()
        fecha_final_elem = instancia_elem.find('fechaFinal')
        fecha_final_text = fecha_final_elem.text if fecha_final_elem is not None else None
        fecha_final = self.validators.extraer_primera_fecha(fecha_final_text) if fecha_final_text else None

        estado, errores_estado = self.validators.validar_estado(estado, fecha_final)
        if errores_estado:
            raise Exception(f"Errores en estado de instancia: {', '.join(errores_estado)}")

        return Instancia(id_instancia, id_configuracion, nombre, fecha_inicio, estado, fecha_final)
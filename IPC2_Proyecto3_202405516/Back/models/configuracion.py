class Configuracion:
    def __init__(self, id_configuracion, nombre, descripcion, id_categoria=None):
        self.id_configuracion = id_configuracion
        self.nombre = nombre
        self.descripcion = descripcion
        self.id_categoria = None
        self.recursos = {}

    def agregar_recurso(self, id_recurso, cantidad):
        self.recursos[id_recurso] = cantidad

    def to_dict(self):
        return {
            "id_configuracion": self.id_configuracion,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "id_categoria": self.id_categoria,
        } 
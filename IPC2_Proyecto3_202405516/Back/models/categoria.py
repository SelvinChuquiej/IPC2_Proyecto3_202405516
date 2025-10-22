class Categoria:
    def __init__(self, id_Categoria, nombre, descripcion, carga_trabajo):
        self.id_Categoria = id_Categoria
        self.nombre = nombre
        self.descripcion = descripcion
        self.carga_trabajo = carga_trabajo
        self.configuraciones = []

    def agregar_configuracion(self, configuracion):
        self.configuraciones.append(configuracion)

    def to_dict(self):
        return {
            "id_Categoria": self.id_Categoria,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "carga_trabajo": self.carga_trabajo,
            "configuraciones": [config.to_dict() for config in self.configuraciones]
        }
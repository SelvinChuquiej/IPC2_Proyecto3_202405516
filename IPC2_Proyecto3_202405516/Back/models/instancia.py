class Instancia:
    def __init__(self, id_instancia, id_configuracion, nombre, fecha_inicio, estado, fecha_final=None):
        self.id_instancia = id_instancia
        self.id_configuracion = id_configuracion
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.estado = estado  # 'Vigente' o 'Cancelada'
        self.fecha_final = fecha_final
        self.consumos = []  # Lista de objetos Consumo
    
    def agregar_consumo(self, consumo):
        self.consumos.append(consumo)
    
    def to_dict(self):
        return {
            'id': self.id_instancia,
            'id_configuracion': self.id_configuracion,
            'nombre': self.nombre,
            'fecha_inicio': self.fecha_inicio,
            'estado': self.estado,
            'fecha_final': self.fecha_final,
            'consumos': [consumo.to_dict() for consumo in self.consumos]
        }
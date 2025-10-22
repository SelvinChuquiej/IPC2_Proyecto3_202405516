class Consumo:
    def __init__(self, nit_cliente, id_instancia, tiempo, fecha_hora):
        self.nit_cliente = nit_cliente
        self.id_instancia = id_instancia
        self.tiempo = float(tiempo)
        self.fecha_hora = fecha_hora
    
    def to_dict(self):
        return {
            'nit_cliente': self.nit_cliente,
            'id_instancia': self.id_instancia,
            'tiempo': self.tiempo,
            'fecha_hora': self.fecha_hora
        }
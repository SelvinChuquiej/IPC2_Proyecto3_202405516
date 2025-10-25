class DetalleFactura:
    def __init__(self, id_instancia, nombre_instancia, recurso, cantidad, costo_hora, horas):
        self.id_instancia = id_instancia
        self.nombre_instancia = nombre_instancia
        self.recurso = recurso
        self.cantidad = cantidad
        self.costo_hora = costo_hora
        self.horas = horas
        self.subtotal = cantidad * costo_hora * horas

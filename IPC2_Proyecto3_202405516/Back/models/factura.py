class Factura:
    contador_facturas = 1  # para generar número único

    def __init__(self, nit_cliente, fecha, detalles):
        self.numero = Factura.contador_facturas
        Factura.contador_facturas += 1
        self.nit_cliente = nit_cliente
        self.fecha = fecha
        self.detalles = detalles  # lista de DetalleFactura
        self.total = sum(detalle.subtotal for detalle in detalles)

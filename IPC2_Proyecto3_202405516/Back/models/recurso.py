class Recurso:
    def __init__(self, id_recurso, nombre, abreviatura, metrica, tipo, valor_x_hora):
            self.id_recurso = id_recurso
            self.nombre = nombre
            self.abreviatura = abreviatura
            self.metrica = metrica
            self.tipo = tipo
            self.valor_x_hora = float(valor_x_hora)

    def to_dict(self):
        return {
            "id_recurso": self.id_recurso,
            "nombre": self.nombre,
            "abreviatura": self.abreviatura,
            "metrica": self.metrica,
            "tipo": self.tipo,
            "valor_x_hora": self.valor_x_hora
        }    
    
    def __str__(self):
        return f"Recurso(id_recurso={self.id_recurso}, {self.nombre}, {self.tipo})"
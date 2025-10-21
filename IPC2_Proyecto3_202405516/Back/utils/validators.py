import re
from datetime import date

class Validators:
    @staticmethod
    def tipo_recurso(tipo) -> str:
        if not tipo:
            return None
        t = tipo.strip().lower()
        if t == 'hardware':
            return 'Hardware'
        if t == 'software':
            return 'Software'
        return None

    @staticmethod
    def fecha_valida(d:int, m:int, y:int) -> bool:
        try:
            date(y, m, d)
            return True
        except ValueError:
            return False
        
    @staticmethod
    def extraer_primera_fecha(text:str) -> str | None:
        if not text:
            return None
        for day_s, month_s, year_s in re.findall(r'(\d{1,2})/(\d{1,2})/(\d{4})', text):
            d = int(day_s)
            m = int(month_s)
            y = int(year_s)
            if Validators.fecha_valida(d, m, y):
                return f"{day_s}/{month_s}/{year_s}" 
        return None
    
    @staticmethod
    def extraer_primera_fechahora(text: str) -> str | None:
        if not text:
            return None
        for d_s, m_s, y_s, h_s, min_s in re.findall(r'(\d{1,2})/(\d{1,2})/(\d{4})\s+(\d{1,2}):(\d{2})', text):
            d = int(d_s)
            m = int(m_s)
            y = int(y_s)
            h = int(h_s)
            mi = int(min_s)
            if Validators.fecha_valida(d, m, y) and (0 <= h < 24) and (0 <= mi < 60):
                return f"{d_s}/{m_s}/{y_s} {h_s}:{min_s}"
        return None
    
    @staticmethod
    def validar_estado(estado_raw: str, fecha_final:str | None) -> tuple[str, list[str]]:
        errores = []
        if not estado_raw:
            errores.append("El estado no puede estar vacío.")
            return None, errores
        v = estado_raw.strip().lower()
        if v == 'vigente':
            estado = 'Vigente'
            if fecha_final:
                pass
        elif v == 'cancelada':
            estado = 'Cancelada'
            if not fecha_final:
                errores.append("Instancia cancelada requiere una fecha final.")
        else:
            errores.append("El estado debe ser 'Vigente' o 'Cancelada'.")
            estado = None
        return estado, errores
    
    @staticmethod
    def validar_nit(nit) -> bool:
        pattern = r'^\d{1,9}-[\dK]$'
        return bool(re.match(pattern, nit))
    
    @staticmethod
    def analizador_horas(text: str) -> float | None:
        _decimal_re = re.compile(r'^\s*([0-9]+(?:[.,][0-9]+)?)\s*(?:h|horas?|hrs?)?\s*$', re.I)
        _hm_re = re.compile(r'^\s*(\d{1,2}):(\d{2})(?::(\d{2}))?\s*$')
        _hm_words_re = re.compile(r'(?:(\d+)\s*h(?:oras?)?)?\s*(?:(\d+)\s*m(?:in(?:utos?)?)?)?', re.I)
        _minutes_re = re.compile(r'^\s*(\d+)\s*(?:m|minutos?)\s*$', re.I)

        if not text:
            return None
        t = text.strip().lower().replace(',', '.')
        m = _hm_re.match(t)
        if m:
            h = int(m.group(1))
            mi = int(m.group(2))
            s = int(m.group(3)) if m.group(3) else 0
            return h + mi / 60 + s / 3600
        m = _decimal_re.match(t)
        if m:
            return float(m.group(1))
        m = _hm_words_re.search(t)
        if m:
            h = int(m.group(1)) if m.group(1) else 0
            mi = int(m.group(2)) if m.group(2) else 0
            if h == 0 and mi == 0:
                pass
            else:
                return h + mi / 60
        m = _minutes_re.match(t)
        if m:
            mi = int(m.group(1))
            return mi / 60
        return None

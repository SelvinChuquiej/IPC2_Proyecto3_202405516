import os
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Any, Dict, List, Optional

class FacturacionService:
    def __init__(self, db):
        # db debe exponer get_file_path(filename: str) -> str
        self.db = db

    # ----------------- Helpers -----------------
    def _parse_dt(self, s: Optional[str]) -> Optional[datetime]:
        if not s:
            return None
        s = s.strip()
        for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(s, fmt)
            except Exception:
                continue
        return None

    def _valor_x_hora_recurso(self, id_recurso: str) -> float:
        try:
            path = self.db.get_file_path('recursos.xml')
            tree = ET.parse(path)
            root = tree.getroot()
            for r in root.findall('recurso'):
                if r.get('id') == str(id_recurso):
                    vxh = (r.findtext('valorXhora') or "0").strip()
                    return float(vxh)
        except Exception:
            pass
        return 0.0

    def _config_de_instancia(self, id_instancia: str) -> Optional[str]:
        try:
            path = self.db.get_file_path('instancias.xml')
            if not os.path.exists(path):
                return None
            tree = ET.parse(path)
            root = tree.getroot()
            for inst in root.findall('instancia'):
                if inst.get('id') == str(id_instancia):
                    return (inst.findtext('idConfiguracion') or "").strip() or inst.get('idConfiguracion')
        except Exception:
            pass
        return None

    def _precio_hora_instancia(self, id_instancia: str) -> float:
        id_cfg = self._config_de_instancia(id_instancia)
        if not id_cfg:
            return 0.0
        try:
            path_cfg = self.db.get_file_path('configuraciones.xml')
            if not os.path.exists(path_cfg):
                return 0.0
            tree = ET.parse(path_cfg)
            root = tree.getroot()
            cfg_elem = None
            for c in root.findall('configuracion'):
                if c.get('id') == str(id_cfg):
                    cfg_elem = c
                    break
            if cfg_elem is None:
                return 0.0

            parent = cfg_elem.find('recursos') or cfg_elem.find('recursosConfiguracion')
            if parent is None:
                return 0.0

            total = 0.0
            for r in parent.findall('recurso'):
                rid = r.get('id') or (r.findtext('id') or "").strip()
                cantidad_txt = r.get('cantidad') or (r.text or "").strip()
                try:
                    cantidad = float(cantidad_txt) if cantidad_txt else 0.0
                except Exception:
                    cantidad = 0.0
                vxh = self._valor_x_hora_recurso(rid) if rid else 0.0
                total += vxh * cantidad
            return total
        except Exception:
            return 0.0

    def _siguiente_numero_factura(self) -> int:
        path = self.db.get_file_path('facturas.xml')
        if not os.path.exists(path):
            return 1
        try:
            tree = ET.parse(path)
            root = tree.getroot()
            max_id = 0
            for f in root.findall('factura'):
                try:
                    max_id = max(max_id, int(f.get('id') or "0"))
                except Exception:
                    continue
            return max_id + 1
        except Exception:
            return 1

    # ----------------- Público -----------------
    def generar_facturas(self, fecha_inicio: str, fecha_fin: str) -> Dict[str, Any]:
        fi = self._parse_dt(fecha_inicio)
        ff = self._parse_dt(fecha_fin)
        if not fi or not ff or ff < fi:
            raise ValueError("Rango de fechas inválido")

        cons_path = self.db.get_file_path('consumos.xml')
        if not os.path.exists(cons_path):
            return {"generadas": 0, "facturas": []}

        c_tree = ET.parse(cons_path)
        c_root = c_tree.getroot()

        por_cliente: Dict[str, List[ET.Element]] = {}
        for c in c_root.findall('consumo'):
            if (c.get('facturado') or '').lower() == 'true' or (c.findtext('facturado') or '').lower() == 'true':
                continue

            nit = c.get('nitCliente') or c.findtext('nitCliente') or ''
            id_inst = c.get('idInstancia') or c.findtext('idInstancia') or ''
            tiempo_txt = (c.findtext('tiempo') or '').strip()
            fh_txt = (c.findtext('fechahora') or '').strip()
            if not nit or not id_inst or not tiempo_txt or not fh_txt:
                continue

            try:
                tiempo = float(tiempo_txt)
            except Exception:
                continue

            fh = self._parse_dt(fh_txt)
            if not fh or not (fi <= fh <= ff):
                continue

            c.set('_nit', nit)
            c.set('_idInstancia', str(id_inst))
            c.set('_tiempo', f"{tiempo}")
            por_cliente.setdefault(nit, []).append(c)

        if not por_cliente:
            return {"generadas": 0, "facturas": []}

        fpath = self.db.get_file_path('facturas.xml')
        if not os.path.exists(fpath):
            ET.ElementTree(ET.Element('facturas')).write(fpath, encoding='utf-8', xml_declaration=True)

        f_tree = ET.parse(fpath)
        f_root = f_tree.getroot()

        generadas = []
        for nit, lista in por_cliente.items():
            numero = self._siguiente_numero_factura()
            fecha_factura = ff.date().strftime("%Y-%m-%d")

            total = 0.0
            detalle = []

            for c in lista:
                id_inst = c.get('_idInstancia')
                tiempo = float(c.get('_tiempo') or "0")
                p_hora = self._precio_hora_instancia(id_inst)
                subtotal = tiempo * p_hora
                total += subtotal
                detalle.append({
                    "idInstancia": id_inst,
                    "fechahora": c.findtext('fechahora') or '',
                    "tiempo": tiempo,
                    "precioHora": p_hora,
                    "subtotal": subtotal
                })

            fac = ET.Element('factura', id=str(numero))
            ET.SubElement(fac, 'nitCliente').text = nit
            ET.SubElement(fac, 'fechaFactura').text = fecha_factura
            ET.SubElement(fac, 'montoTotal').text = f"{total:.2f}"

            det_elem = ET.SubElement(fac, 'detalle')
            for it in detalle:
                item = ET.SubElement(det_elem, 'item', idInstancia=str(it["idInstancia"]))
                item.set('tiempo', f"{it['tiempo']}")
                item.set('precioHora', f"{it['precioHora']:.4f}")
                item.set('subtotal', f"{it['subtotal']:.4f}")
                ET.SubElement(item, 'fechahora').text = it["fechahora"]

            f_root.append(fac)
            f_tree.write(fpath, encoding='utf-8', xml_declaration=True)

            # marcar consumos como facturados
            for c in lista:
                c.set('facturado', 'true')
                c.set('numeroFactura', str(numero))

            generadas.append({
                "numero": numero,
                "nit": nit,
                "fecha": fecha_factura,
                "monto": round(total, 2)
            })

        # persistir marcados
        c_tree.write(cons_path, encoding='utf-8', xml_declaration=True)

        return {"generadas": len(generadas), "facturas": generadas}
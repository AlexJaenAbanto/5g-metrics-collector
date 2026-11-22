import json
import zmq
import resources
from odu import scheduler, rlc, ru, mac, phy
from ocu import e1ap, pdcp, rrc, ngap

# Configuración del socket de publicación ZeroMQ (PUB)
_context = zmq.Context()
_pub = _context.socket(zmq.PUB)
_pub.bind("ipc:///tmp/5g_metrics.ipc")
_pub.bind("tcp://127.0.0.1:5555")

def dispatch(data):
    # RECURSOS GLOBALES (Energía, CPU, RAM)
    if "app_resource_usage" in data:
        resources.parse_resources(data)

    # ODU
    if "cells" in data:
        scheduler.parse_cells(data)
    if "rlc_metrics" in data:
        rlc.parse_rlc(data)
    if "ru" in data:
        ru.parse_ru(data)
    if "du_low" in data:
        phy.parse_phy(data)
    if "du" in data and "du_high" in data.get("du", {}) and "mac" in data["du"]["du_high"]:
        mac.parse_mac(data)

    # OCU
    if "cu-up" in data:
        cu_up_data = data["cu-up"]
        if "e1ap" in cu_up_data:
            e1ap.parse_e1ap(cu_up_data["e1ap"])
        if "pdcp" in cu_up_data:
            pdcp.parse_pdcp(cu_up_data["pdcp"])

    if "cu-cp" in data:
        cu_cp_data = data["cu-cp"]
        if "rrcs" in cu_cp_data:
            rrc.parse_rrc(cu_cp_data["rrcs"])
        if "ngaps" in cu_cp_data:
            ngap.parse_ngap(cu_cp_data["ngaps"])

    # Emisión directa hacia la xApp / Consumidores ML
    try:
        _pub.send_string(f"METRICS {json.dumps(data)}")
    except Exception:
        pass

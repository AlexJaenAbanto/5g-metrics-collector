import metrics

def parse_ngap(ngaps_data):
    # 1. Handovers globales NGAP
    if "nof_handover_preparations_requested" in ngaps_data:
        metrics.ocu_ngap_handover_preparations.labels(result="requested").set(ngaps_data["nof_handover_preparations_requested"])
    if "nof_successful_handover_preparations" in ngaps_data:
        metrics.ocu_ngap_handover_preparations.labels(result="successful").set(ngaps_data["nof_successful_handover_preparations"])

    # 2. Métricas NGAP por AMF
    for amf in ngaps_data.get("ngap", []):
        amf_name = str(amf.get("amf_name", "unknown"))

        # Estado de la conexión AMF
        is_connected = 1 if amf.get("connected", False) else 0
        metrics.ocu_ngap_amf_connected.labels(amf=amf_name).set(is_connected)

        # Paging (Añadido 'or {}' preventivo)
        paging = amf.get("paging_measurement") or {}
        if "nof_cn_initiated_paging_requests" in paging:
            metrics.ocu_ngap_paging_requests.labels(amf=amf_name).set(paging["nof_cn_initiated_paging_requests"])

        # PDU Sessions (Añadido 'or {}' para evitar el AttributeError con null)
        pdu = amf.get("pdu_session_management") or {}
        snssai = str(pdu.get("s-nssai", "unknown"))

        if "nof_pdu_sessions_requested_to_setup" in pdu:
            metrics.ocu_ngap_pdu_sessions.labels(amf=amf_name, snssai=snssai, result="requested").set(pdu["nof_pdu_sessions_requested_to_setup"])
        if "nof_pdu_sessions_successfully_setup" in pdu:
            metrics.ocu_ngap_pdu_sessions.labels(amf=amf_name, snssai=snssai, result="successful").set(pdu["nof_pdu_sessions_successfully_setup"])

        for cause, count in pdu.get("nof_pdu_sessions_failed_to_setup", {}).items():
            metrics.ocu_ngap_pdu_session_failures.labels(amf=amf_name, snssai=snssai, cause=cause).set(count)

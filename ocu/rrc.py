import metrics

def parse_rrc(rrc_data):
    # 1. Handovers globales de RRC
    if "nof_handover_executions_requested" in rrc_data:
        metrics.ocu_rrc_handover_executions.labels(result="requested").set(rrc_data["nof_handover_executions_requested"])
    if "nof_successful_handover_executions" in rrc_data:
        metrics.ocu_rrc_handover_executions.labels(result="successful").set(rrc_data["nof_successful_handover_executions"])

    # 2. Métricas RRC por DU
    for du in rrc_data.get("du", []):
        gnb_du_id = str(du.get("gnb_du_id", "unknown"))

        # Conexiones (establishments)
        estab = du.get("rrc_connection_establishment", {})
        for cause, count in estab.get("attempted_rrc_connection_establishments", {}).items():
            metrics.ocu_rrc_establishments.labels(gnb_du_id=gnb_du_id, cause=cause, result="attempted").set(count)

        for cause, count in estab.get("successful_rrc_connection_establishments", {}).items():
            metrics.ocu_rrc_establishments.labels(gnb_du_id=gnb_du_id, cause=cause, result="successful").set(count)

        for cause, count in estab.get("failed_rrc_connection_establishments", {}).items():
            metrics.ocu_rrc_establishment_failures.labels(gnb_du_id=gnb_du_id, cause=cause).set(count)

        # Estados de las conexiones
        conn_num = du.get("rrc_connection_number", {})
        
        # Saneamiento de underflow (valores absurdos mayores de 10000 se fuerzan a 0)
        def sanitize_underflow(val):
            return 0 if val > 10000 else val

        if "mean_nof_rrc_connections" in conn_num:
            val = sanitize_underflow(conn_num["mean_nof_rrc_connections"])
            metrics.ocu_rrc_connections.labels(gnb_du_id=gnb_du_id, state="active", statistic="mean").set(val)
            
        if "max_nof_rrc_connections" in conn_num:
            val = sanitize_underflow(conn_num["max_nof_rrc_connections"])
            metrics.ocu_rrc_connections.labels(gnb_du_id=gnb_du_id, state="active", statistic="max").set(val)
            
        if "mean_nof_inactive_rrc_connections" in conn_num:
            val = sanitize_underflow(conn_num["mean_nof_inactive_rrc_connections"])
            metrics.ocu_rrc_connections.labels(gnb_du_id=gnb_du_id, state="inactive", statistic="mean").set(val)
            
        if "max_nof_inactive_rrc_connections" in conn_num:
            val = sanitize_underflow(conn_num["max_nof_inactive_rrc_connections"])
            metrics.ocu_rrc_connections.labels(gnb_du_id=gnb_du_id, state="inactive", statistic="max").set(val)

        # Re-establishments
        reestab = du.get("rrc_connection_reestablishment", {})
        if "attempted_rrc_connection_reestablishments" in reestab:
            metrics.ocu_rrc_reestablishments.labels(gnb_du_id=gnb_du_id, result="attempted").set(reestab["attempted_rrc_connection_reestablishments"])
        if "successful_rrc_connection_reestablishments_with_ue_context" in reestab:
            metrics.ocu_rrc_reestablishments.labels(gnb_du_id=gnb_du_id, result="successful_with_context").set(reestab["successful_rrc_connection_reestablishments_with_ue_context"])
        if "successful_rrc_connection_reestablishments_without_ue_context" in reestab:
            metrics.ocu_rrc_reestablishments.labels(gnb_du_id=gnb_du_id, result="successful_without_context").set(reestab["successful_rrc_connection_reestablishments_without_ue_context"])

import metrics

# Almacenamos el estado de los túneles activos para detectar desconexiones
_active_bearers = set()

def parse_pdcp(pdcp_data):
    global _active_bearers
    current_bearers = set()

    # 1. Parseo por Bearer
    for bearer in pdcp_data.get("bearers", []):
        ue_idx = str(bearer.get("ue_index", "unknown"))
        rb_type = str(bearer.get("rb_type", "unknown"))
        rb_id = str(bearer.get("rb_id", "unknown"))

        for direction in ["dl", "ul"]:
            if direction in bearer:
                # Registrar este flujo como activo en la iteración actual
                current_bearers.add((ue_idx, rb_type, rb_id, direction))
                
                d_data = bearer[direction]
                l = {"ue_index": ue_idx, "rb_type": rb_type, "rb_id": rb_id, "direction": direction}

                # Métricas comunes
                if "num_sdus" in d_data: metrics.ocu_pdcp_sdus.labels(**l).set(d_data["num_sdus"])
                if "num_sdu_bytes" in d_data: metrics.ocu_pdcp_sdu_bytes.labels(**l).set(d_data["num_sdu_bytes"])
                if "num_pdus" in d_data: metrics.ocu_pdcp_pdus.labels(**l).set(d_data["num_pdus"])
                if "num_pdu_bytes" in d_data: metrics.ocu_pdcp_pdu_bytes.labels(**l).set(d_data["num_pdu_bytes"])
                if "sdu_throughput_mbps" in d_data: metrics.ocu_pdcp_sdu_throughput_mbps.labels(**l).set(d_data["sdu_throughput_mbps"])
                if "pdu_throughput_mbps" in d_data: metrics.ocu_pdcp_pdu_throughput_mbps.labels(**l).set(d_data["pdu_throughput_mbps"])
                if "cpu_usage_percent" in d_data: metrics.ocu_pdcp_cpu_usage_percent.labels(**l).set(d_data["cpu_usage_percent"])

                # Latencias (us -> s)
                l_lat = {"ue_index": ue_idx, "rb_type": rb_type, "rb_id": rb_id, "direction": direction}
                if "average_latency_us" in d_data:
                    metrics.ocu_pdcp_latency_seconds.labels(**l_lat, statistic="average").set(d_data["average_latency_us"] * 1e-6)
                if "min_latency_us" in d_data:
                    metrics.ocu_pdcp_latency_seconds.labels(**l_lat, statistic="min").set(d_data["min_latency_us"] * 1e-6)
                if "max_latency_us" in d_data:
                    metrics.ocu_pdcp_latency_seconds.labels(**l_lat, statistic="max").set(d_data["max_latency_us"] * 1e-6)

                # Histograma (us)
                if "latency_histogram" in d_data:
                    width = d_data.get("histogram_bin_width_us", 1)
                    is_overflow = d_data.get("histogram_last_bin_is_overflow", False)
                    hist = d_data["latency_histogram"]

                    for idx, count in enumerate(hist):
                        bin_start = idx * width
                        if idx == len(hist) - 1 and is_overflow:
                            bin_label = f">={bin_start} us"
                        else:
                            bin_label = f"[{bin_start}, {bin_start + width}) us"
                        metrics.ocu_pdcp_latency_bin.labels(**l, bin=bin_label).set(count)

                # Específicas DL
                if direction == "dl":
                    l_dl = {"ue_index": ue_idx, "rb_type": rb_type, "rb_id": rb_id}
                    if "num_dropped_sdus" in d_data: metrics.ocu_pdcp_dropped_sdus.labels(**l_dl).set(d_data["num_dropped_sdus"])
                    if "num_discard_timeouts" in d_data: metrics.ocu_pdcp_discard_timeouts.labels(**l_dl).set(d_data["num_discard_timeouts"])

                # Específicas UL
                if direction == "ul":
                    l_ul = {"ue_index": ue_idx, "rb_type": rb_type, "rb_id": rb_id}
                    if "num_dropped_pdus" in d_data: metrics.ocu_pdcp_dropped_pdus.labels(**l_ul).set(d_data["num_dropped_pdus"])
                    if "num_integrity_verified_pdus" in d_data: metrics.ocu_pdcp_integrity_pdus.labels(**l_ul, result="verified").set(d_data["num_integrity_verified_pdus"])
                    if "num_integrity_failed_pdus" in d_data: metrics.ocu_pdcp_integrity_pdus.labels(**l_ul, result="failed").set(d_data["num_integrity_failed_pdus"])
                    if "num_t_reordering_timeouts" in d_data: metrics.ocu_pdcp_reordering_timeouts.labels(**l_ul).set(d_data["num_t_reordering_timeouts"])
                    if "average_reordering_delay_us" in d_data: metrics.ocu_pdcp_reordering_delay_seconds.labels(**l_ul).set(d_data["average_reordering_delay_us"] * 1e-6)

    # 2. Resetear a 0 los túneles desconectados (Stale Metrics)
    disconnected = _active_bearers - current_bearers
    for ue_idx, rb_type, rb_id, direction in disconnected:
        l_stale = {"ue_index": ue_idx, "rb_type": rb_type, "rb_id": rb_id, "direction": direction}
        # Forzar métricas a 0 para el UE desconectado
        metrics.ocu_pdcp_pdu_throughput_mbps.labels(**l_stale).set(0)
        metrics.ocu_pdcp_sdu_throughput_mbps.labels(**l_stale).set(0)
        metrics.ocu_pdcp_cpu_usage_percent.labels(**l_stale).set(0)

    # Actualizar la memoria para el próximo ciclo
    _active_bearers = current_bearers

    # 3. Parseo Global
    for direction in ["dl", "ul"]:
        if direction in pdcp_data:
            g_data = pdcp_data[direction]
            if "num_sdus" in g_data: metrics.ocu_pdcp_global_sdus.labels(direction=direction).set(g_data["num_sdus"])
            if "sdu_throughput_mbps" in g_data: metrics.ocu_pdcp_global_sdu_throughput_mbps.labels(direction=direction).set(g_data["sdu_throughput_mbps"])
            if "average_latency_us" in g_data: metrics.ocu_pdcp_global_latency_seconds.labels(direction=direction, statistic="average").set(g_data["average_latency_us"] * 1e-6)
        
        # Resetear métricas globales si no hay ningún bearer activo en esa dirección
        elif not current_bearers:
            metrics.ocu_pdcp_global_sdu_throughput_mbps.labels(direction=direction).set(0)

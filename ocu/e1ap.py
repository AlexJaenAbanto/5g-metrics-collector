import metrics

def parse_e1ap(e1ap_data):
    # Operaciones (Setup y Mod pueden ser successful según el contrato, release es global)[cite: 1]
    if "successful_bearer_context_setups" in e1ap_data:
        metrics.ocu_e1ap_bearer_context_operations.labels(operation="setup", result="successful").set(e1ap_data["successful_bearer_context_setups"])
    if "successful_bearer_context_modifications" in e1ap_data:
        metrics.ocu_e1ap_bearer_context_operations.labels(operation="modification", result="successful").set(e1ap_data["successful_bearer_context_modifications"])
    if "bearer_context_releases" in e1ap_data:
        metrics.ocu_e1ap_bearer_context_operations.labels(operation="release", result="any").set(e1ap_data["bearer_context_releases"])

    # Latencias (us -> s)[cite: 1]
    lat_data = e1ap_data.get("release_latency", {})
    if "average_us" in lat_data:
        metrics.ocu_e1ap_release_latency_seconds.labels(statistic="average").set(lat_data["average_us"] * 1e-6)
    if "max_us" in lat_data:
        metrics.ocu_e1ap_release_latency_seconds.labels(statistic="max").set(lat_data["max_us"] * 1e-6)

    # Histograma (Gauge por bin)[cite: 1]
    if "histogram" in lat_data:
        width_ms = lat_data.get("histogram_bin_width_ms", 100)
        for idx, count in enumerate(lat_data["histogram"]):
            # Nombramos el bin en función de su anchura (ej. "[0, 100) ms")
            bin_label = f"[{idx * width_ms}, {(idx + 1) * width_ms}) ms"
            metrics.ocu_e1ap_release_latency_bin.labels(bin=bin_label).set(count)

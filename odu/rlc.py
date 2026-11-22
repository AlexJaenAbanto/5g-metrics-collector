import metrics

def parse_rlc(data):
    # La clave puede contener un objeto directo o una lista según el volumen de DRBs activos
    rlc_data = data.get("rlc_metrics", [])
    rlc_list = rlc_data if isinstance(rlc_data, list) else [rlc_data]
    
    for rlc in rlc_list:
        ue_id = str(rlc.get("ue_id", "unknown"))
        drb_id = str(rlc.get("drb_id", "unknown"))
        l_err = {"ue_id": ue_id, "drb_id": drb_id}

        # Procesar RX
        if "rx" in rlc:
            rx = rlc["rx"]
            l_rx = {"ue_id": ue_id, "drb_id": drb_id, "direction": "rx"}
            
            if "num_sdus" in rx: metrics.odu_rlc_sdus.labels(**l_rx).set(rx["num_sdus"])
            if "num_sdu_bytes" in rx: metrics.odu_rlc_sdu_bytes.labels(**l_rx).set(rx["num_sdu_bytes"])
            if "num_pdus" in rx: metrics.odu_rlc_pdus.labels(**l_rx).set(rx["num_pdus"])
            if "num_pdu_bytes" in rx: metrics.odu_rlc_pdu_bytes.labels(**l_rx).set(rx["num_pdu_bytes"])
            
            if "num_lost_pdus" in rx: metrics.odu_rlc_lost_pdus.labels(**l_err).set(rx["num_lost_pdus"])
            if "num_malformed_pdus" in rx: metrics.odu_rlc_malformed_pdus.labels(**l_err).set(rx["num_malformed_pdus"])

        # Procesar TX
        if "tx" in rlc:
            tx = rlc["tx"]
            l_tx = {"ue_id": ue_id, "drb_id": drb_id, "direction": "tx"}
            
            if "num_sdus" in tx: metrics.odu_rlc_sdus.labels(**l_tx).set(tx["num_sdus"])
            if "num_sdu_bytes" in tx: metrics.odu_rlc_sdu_bytes.labels(**l_tx).set(tx["num_sdu_bytes"])
            if "num_pdus" in tx: metrics.odu_rlc_pdus.labels(**l_tx).set(tx["num_pdus"])
            if "num_pdu_bytes" in tx: metrics.odu_rlc_pdu_bytes.labels(**l_tx).set(tx["num_pdu_bytes"])
            
            if "num_dropped_sdus" in tx: metrics.odu_rlc_dropped_sdus.labels(**l_err).set(tx["num_dropped_sdus"])
            if "num_discarded_sdus" in tx: metrics.odu_rlc_discarded_sdus.labels(**l_err).set(tx["num_discarded_sdus"])
            if "num_discard_failures" in tx: metrics.odu_rlc_discard_failures.labels(**l_err).set(tx["num_discard_failures"])

            # Conversión ns -> s para el contrato[cite: 1]
            if "max_pdu_latency_ns" in tx:
                metrics.odu_rlc_pdu_latency_seconds.labels(**l_err, statistic="max").set(tx["max_pdu_latency_ns"] * 1e-9)

            # Histograma de latencia (Gauge por bin)[cite: 1]
            if "pull_latency_histogram" in tx:
                for bin_data in tx["pull_latency_histogram"]:
                    bin_start = str(bin_data.get("pull_latency_bin_start_usec", 0))
                    count = bin_data.get("pull_latency_bin_count", 0)
                    metrics.odu_rlc_pull_latency_bin.labels(**l_err, bin_start_us=bin_start).set(count)

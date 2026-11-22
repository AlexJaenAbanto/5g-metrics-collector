import metrics

# Memoria de estado para rastrear UEs conectados por PCI
_active_ues = set()

def parse_cells(data):
    global _active_ues
    current_ues = set()

    cells = data.get("cells", [])
    for cell in cells:
        c_metrics = cell.get("cell_metrics", {})
        pci = str(c_metrics.get("pci", "unknown"))

        # Cell metrics (Asumiendo latencias base en ms -> *1e-3 para segundos)
        if "average_latency" in c_metrics: metrics.odu_scheduler_latency_seconds.labels(pci=pci, statistic="average").set(c_metrics["average_latency"] * 1e-3)
        if "max_latency" in c_metrics: metrics.odu_scheduler_latency_seconds.labels(pci=pci, statistic="max").set(c_metrics["max_latency"] * 1e-3)
        if "avg_prach_delay" in c_metrics: metrics.odu_scheduler_prach_delay_seconds.labels(pci=pci).set(c_metrics["avg_prach_delay"] * 1e-3)
        metrics.odu_scheduler_error_indications.labels(pci=pci).set(c_metrics.get("error_indication_count", 0))
        metrics.odu_scheduler_late_harqs.labels(pci=pci, direction="dl").set(c_metrics.get("late_dl_harqs", 0))
        metrics.odu_scheduler_late_harqs.labels(pci=pci, direction="ul").set(c_metrics.get("late_ul_harqs", 0))
        metrics.odu_scheduler_msg3.labels(pci=pci, result="ok").set(c_metrics.get("msg3_nof_ok", 0))
        metrics.odu_scheduler_msg3.labels(pci=pci, result="nok").set(c_metrics.get("msg3_nof_nok", 0))
        metrics.odu_scheduler_failed_allocations.labels(pci=pci, channel="pdcch").set(c_metrics.get("nof_failed_pdcch_allocs", 0))
        metrics.odu_scheduler_failed_allocations.labels(pci=pci, channel="uci").set(c_metrics.get("nof_failed_uci_allocs", 0))
        if "pucch_tot_rb_usage_avg" in c_metrics: metrics.odu_scheduler_pucch_rb_usage.labels(pci=pci).set(c_metrics["pucch_tot_rb_usage_avg"])

        # Extraer sumatorio de PRBs
        pdsch = c_metrics.get("pdsch_prbs_used_per_tdd_slot_idx", [])
        pusch = c_metrics.get("pusch_prbs_used_per_tdd_slot_idx", [])
        if pdsch: metrics.odu_mac_prbs_used.labels(pci=pci, direction="dl").set(sum(pdsch))
        if pusch: metrics.odu_mac_prbs_used.labels(pci=pci, direction="ul").set(sum(pusch))

        # Histograma de latencias
        histogram = c_metrics.get("latency_histogram", [])
        for i, val in enumerate(histogram):
            metrics.odu_mac_latency_histogram.labels(pci=pci, bin_index=str(i)).set(val)

        # UE list metrics
        for ue in cell.get("ue_list", []):
            ue_id = str(ue.get("ue", "unknown"))
            # Registrar el UE como activo en este ciclo
            current_ues.add((pci, ue_id))

            if "cqi" in ue: metrics.odu_scheduler_cqi.labels(pci=pci, ue_id=ue_id).set(ue["cqi"])
            if "dl_mcs" in ue: metrics.odu_scheduler_mcs.labels(pci=pci, ue_id=ue_id, direction="dl").set(ue["dl_mcs"])
            if "ul_mcs" in ue: metrics.odu_scheduler_mcs.labels(pci=pci, ue_id=ue_id, direction="ul").set(ue["ul_mcs"])
            if "dl_brate" in ue: metrics.odu_scheduler_bitrate_bps.labels(pci=pci, ue_id=ue_id, direction="dl").set(ue["dl_brate"])
            if "ul_brate" in ue: metrics.odu_scheduler_bitrate_bps.labels(pci=pci, ue_id=ue_id, direction="ul").set(ue["ul_brate"])
            if "dl_bs" in ue: metrics.odu_scheduler_buffer_bytes.labels(pci=pci, ue_id=ue_id, direction="dl").set(ue["dl_bs"])
            if "bsr" in ue: metrics.odu_scheduler_buffer_bytes.labels(pci=pci, ue_id=ue_id, direction="ul").set(ue["bsr"])
            if "dl_nof_ok" in ue: metrics.odu_scheduler_transmissions.labels(pci=pci, ue_id=ue_id, direction="dl", result="ok").set(ue["dl_nof_ok"])
            if "dl_nof_nok" in ue: metrics.odu_scheduler_transmissions.labels(pci=pci, ue_id=ue_id, direction="dl", result="nok").set(ue["dl_nof_nok"])
            if "ul_nof_ok" in ue: metrics.odu_scheduler_transmissions.labels(pci=pci, ue_id=ue_id, direction="ul", result="ok").set(ue["ul_nof_ok"])
            if "ul_nof_nok" in ue: metrics.odu_scheduler_transmissions.labels(pci=pci, ue_id=ue_id, direction="ul", result="nok").set(ue["ul_nof_nok"])
            if "dl_ri" in ue: metrics.odu_radio_rank_indicator.labels(pci=pci, ue_id=ue_id, direction="dl").set(ue["dl_ri"])
            if "ul_ri" in ue: metrics.odu_radio_rank_indicator.labels(pci=pci, ue_id=ue_id, direction="ul").set(ue["ul_ri"])
            if "pusch_snr_db" in ue: metrics.odu_radio_snr_db.labels(pci=pci, ue_id=ue_id, channel="pusch").set(ue["pusch_snr_db"])
            if "pucch_snr_db" in ue: metrics.odu_radio_snr_db.labels(pci=pci, ue_id=ue_id, channel="pucch").set(ue["pucch_snr_db"])
            if "pusch_rsrp_db" in ue: metrics.odu_radio_pusch_rsrp_db.labels(pci=pci, ue_id=ue_id).set(ue["pusch_rsrp_db"])
            if "last_phr" in ue: metrics.odu_radio_power_headroom_db.labels(pci=pci, ue_id=ue_id).set(ue["last_phr"])

            # Timing Advance (ns -> s)
            if "ta_ns" in ue: metrics.odu_radio_timing_advance_seconds.labels(pci=pci, ue_id=ue_id, source="ta").set(ue["ta_ns"] * 1e-9)
            if "pucch_ta_ns" in ue: metrics.odu_radio_timing_advance_seconds.labels(pci=pci, ue_id=ue_id, source="pucch").set(ue["pucch_ta_ns"] * 1e-9)
            if "pusch_ta_ns" in ue: metrics.odu_radio_timing_advance_seconds.labels(pci=pci, ue_id=ue_id, source="pusch").set(ue["pusch_ta_ns"] * 1e-9)
            if "srs_ta_ns" in ue: metrics.odu_radio_timing_advance_seconds.labels(pci=pci, ue_id=ue_id, source="srs").set(ue["srs_ta_ns"] * 1e-9)

            # Delays (ms -> s)
            delay_maps = [
                ("avg_ce_delay", "ce", "average"), ("max_ce_delay", "ce", "max"),
                ("avg_crc_delay", "crc", "average"), ("max_crc_delay", "crc", "max"),
                ("avg_pucch_harq_delay", "pucch_harq", "average"), ("max_pucch_harq_delay", "pucch_harq", "max"),
                ("avg_pusch_harq_delay", "pusch_harq", "average"), ("max_pusch_harq_delay", "pusch_harq", "max"),
                ("avg_sr_to_pusch_delay", "sr_to_pusch", "average"), ("max_sr_to_pusch_delay", "sr_to_pusch", "max")
            ]
            for key, proc, stat in delay_maps:
                if key in ue: metrics.odu_scheduler_delay_seconds.labels(pci=pci, ue_id=ue_id, procedure=proc, statistic=stat).set(ue[key] * 1e-3)

            # Invalid reports
            invalid_maps = [
                ("nof_pucch_f0f1_invalid_harqs", "pucch_f0f1", "harq"), ("nof_pucch_f2f3f4_invalid_csis", "pucch_f2f3f4", "csi"),
                ("nof_pucch_f2f3f4_invalid_harqs", "pucch_f2f3f4", "harq"), ("nof_pusch_invalid_csis", "pusch", "csi"),
                ("nof_pusch_invalid_harqs", "pusch", "harq")
            ]
            for key, chan, rep in invalid_maps:
                if key in ue: metrics.odu_scheduler_invalid_reports.labels(pci=pci, ue_id=ue_id, channel=chan, report=rep).set(ue[key])

    # ---------------------------------------------------------
    # STALE METRICS CLEANUP: Eliminación real de UEs desconectados
    # ---------------------------------------------------------
    disconnected = _active_ues - current_ues
    for pci, ue_id in disconnected:
        
        # Eliminación de métricas base
        try: metrics.odu_scheduler_cqi.remove(pci, ue_id)
        except KeyError: pass
        try: metrics.odu_radio_pusch_rsrp_db.remove(pci, ue_id)
        except KeyError: pass
        try: metrics.odu_radio_power_headroom_db.remove(pci, ue_id)
        except KeyError: pass

        # Eliminación por dirección
        for direction in ["dl", "ul"]:
            try: metrics.odu_scheduler_mcs.remove(pci, ue_id, direction)
            except KeyError: pass
            try: metrics.odu_scheduler_bitrate_bps.remove(pci, ue_id, direction)
            except KeyError: pass
            try: metrics.odu_scheduler_buffer_bytes.remove(pci, ue_id, direction)
            except KeyError: pass
            try: metrics.odu_radio_rank_indicator.remove(pci, ue_id, direction)
            except KeyError: pass
            for result in ["ok", "nok"]:
                try: metrics.odu_scheduler_transmissions.remove(pci, ue_id, direction, result)
                except KeyError: pass

        # Eliminación por canales
        for channel in ["pusch", "pucch"]:
            try: metrics.odu_radio_snr_db.remove(pci, ue_id, channel)
            except KeyError: pass

        # Eliminación de Timing Advance
        for source in ["ta", "pucch", "pusch", "srs"]:
            try: metrics.odu_radio_timing_advance_seconds.remove(pci, ue_id, source)
            except KeyError: pass

        # Eliminación de Delays
        delay_maps_cleanup = [
            ("ce", "average"), ("ce", "max"), ("crc", "average"), ("crc", "max"),
            ("pucch_harq", "average"), ("pucch_harq", "max"), ("pusch_harq", "average"), ("pusch_harq", "max"),
            ("sr_to_pusch", "average"), ("sr_to_pusch", "max")
        ]
        for proc, stat in delay_maps_cleanup:
            try: metrics.odu_scheduler_delay_seconds.remove(pci, ue_id, proc, stat)
            except KeyError: pass

        # Eliminación de Invalid Reports
        invalid_maps_cleanup = [
            ("pucch_f0f1", "harq"), ("pucch_f2f3f4", "csi"), ("pucch_f2f3f4", "harq"), 
            ("pusch", "csi"), ("pusch", "harq")
        ]
        for chan, rep in invalid_maps_cleanup:
            try: metrics.odu_scheduler_invalid_reports.remove(pci, ue_id, chan, rep)
            except KeyError: pass

    # Actualizamos el estado para el siguiente barrido
    _active_ues = current_ues

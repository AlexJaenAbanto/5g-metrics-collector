from prometheus_client import Gauge

# -- ODU: Scheduler & Cell Metrics --
odu_scheduler_latency_seconds = Gauge('odu_scheduler_latency_seconds', 'Cell latency', ['pci', 'statistic'])
odu_scheduler_prach_delay_seconds = Gauge('odu_scheduler_prach_delay_seconds', 'PRACH delay', ['pci'])
odu_scheduler_error_indications = Gauge('odu_scheduler_error_indications', 'Error indications', ['pci'])
odu_scheduler_late_harqs = Gauge('odu_scheduler_late_harqs', 'Late HARQs', ['pci', 'direction'])
odu_scheduler_msg3 = Gauge('odu_scheduler_msg3', 'MSG3 ok/nok', ['pci', 'result'])
odu_scheduler_failed_allocations = Gauge('odu_scheduler_failed_allocations', 'Failed allocations', ['pci', 'channel'])
odu_scheduler_pucch_rb_usage = Gauge('odu_scheduler_pucch_rb_usage', 'PUCCH RB usage avg', ['pci'])

# -- ODU: UE Scheduler & Radio Metrics --
odu_scheduler_cqi = Gauge('odu_scheduler_cqi', 'CQI', ['pci', 'ue_id'])
odu_scheduler_mcs = Gauge('odu_scheduler_mcs', 'MCS', ['pci', 'ue_id', 'direction'])
odu_scheduler_bitrate_bps = Gauge('odu_scheduler_bitrate_bps', 'Bitrate', ['pci', 'ue_id', 'direction'])
odu_scheduler_buffer_bytes = Gauge('odu_scheduler_buffer_bytes', 'Buffer size', ['pci', 'ue_id', 'direction'])
odu_scheduler_transmissions = Gauge('odu_scheduler_transmissions', 'Transmissions', ['pci', 'ue_id', 'direction', 'result'])
odu_radio_rank_indicator = Gauge('odu_radio_rank_indicator', 'Rank Indicator', ['pci', 'ue_id', 'direction'])
odu_radio_snr_db = Gauge('odu_radio_snr_db', 'SNR dB', ['pci', 'ue_id', 'channel'])
odu_radio_pusch_rsrp_db = Gauge('odu_radio_pusch_rsrp_db', 'PUSCH RSRP dB', ['pci', 'ue_id'])
odu_radio_power_headroom_db = Gauge('odu_radio_power_headroom_db', 'PHR dB', ['pci', 'ue_id'])
odu_radio_timing_advance_seconds = Gauge('odu_radio_timing_advance_seconds', 'Timing Advance', ['pci', 'ue_id', 'source'])
odu_scheduler_delay_seconds = Gauge('odu_scheduler_delay_seconds', 'Scheduler delays', ['pci', 'ue_id', 'procedure', 'statistic'])
odu_scheduler_invalid_reports = Gauge('odu_scheduler_invalid_reports', 'Invalid reports', ['pci', 'ue_id', 'channel', 'report'])

# -- OCU: E1AP Metrics --
ocu_e1ap_bearer_context_operations = Gauge('ocu_e1ap_bearer_context_operations', 'E1AP bearer context ops', ['operation', 'result'])
ocu_e1ap_release_latency_seconds = Gauge('ocu_e1ap_release_latency_seconds', 'E1AP release latency', ['statistic'])
ocu_e1ap_release_latency_bin = Gauge('ocu_e1ap_release_latency_bin', 'E1AP release latency histogram', ['bin'])

# -- OCU: PDCP Metrics (Per Bearer) --
l_bearer = ['ue_index', 'rb_type', 'rb_id', 'direction']
ocu_pdcp_sdus = Gauge('ocu_pdcp_sdus', 'PDCP SDUs', l_bearer)
ocu_pdcp_sdu_bytes = Gauge('ocu_pdcp_sdu_bytes', 'PDCP SDU bytes', l_bearer)
ocu_pdcp_pdus = Gauge('ocu_pdcp_pdus', 'PDCP PDUs', l_bearer)
ocu_pdcp_pdu_bytes = Gauge('ocu_pdcp_pdu_bytes', 'PDCP PDU bytes', l_bearer)
ocu_pdcp_sdu_throughput_mbps = Gauge('ocu_pdcp_sdu_throughput_mbps', 'PDCP SDU throughput Mbps', l_bearer)
ocu_pdcp_pdu_throughput_mbps = Gauge('ocu_pdcp_pdu_throughput_mbps', 'PDCP PDU throughput Mbps', l_bearer)
ocu_pdcp_cpu_usage_percent = Gauge('ocu_pdcp_cpu_usage_percent', 'PDCP CPU usage %', l_bearer)
ocu_pdcp_latency_seconds = Gauge('ocu_pdcp_latency_seconds', 'PDCP latency', ['ue_index', 'rb_type', 'rb_id', 'direction', 'statistic'])

# PDCP DL específicas
ocu_pdcp_dropped_sdus = Gauge('ocu_pdcp_dropped_sdus', 'PDCP dropped SDUs', ['ue_index', 'rb_type', 'rb_id'])
ocu_pdcp_discard_timeouts = Gauge('ocu_pdcp_discard_timeouts', 'PDCP discard timeouts', ['ue_index', 'rb_type', 'rb_id'])

# PDCP UL específicas
ocu_pdcp_dropped_pdus = Gauge('ocu_pdcp_dropped_pdus', 'PDCP dropped PDUs', ['ue_index', 'rb_type', 'rb_id'])
ocu_pdcp_integrity_pdus = Gauge('ocu_pdcp_integrity_pdus', 'PDCP integrity PDUs', ['ue_index', 'rb_type', 'rb_id', 'result'])
ocu_pdcp_reordering_timeouts = Gauge('ocu_pdcp_reordering_timeouts', 'PDCP reordering timeouts', ['ue_index', 'rb_type', 'rb_id'])
ocu_pdcp_reordering_delay_seconds = Gauge('ocu_pdcp_reordering_delay_seconds', 'PDCP reordering delay', ['ue_index', 'rb_type', 'rb_id'])

ocu_pdcp_latency_bin = Gauge('ocu_pdcp_latency_bin', 'PDCP latency histogram', ['ue_index', 'rb_type', 'rb_id', 'direction', 'bin'])

# -- OCU: PDCP Metrics (Globales) --
ocu_pdcp_global_sdus = Gauge('ocu_pdcp_global_sdus', 'Global PDCP SDUs', ['direction'])
ocu_pdcp_global_sdu_throughput_mbps = Gauge('ocu_pdcp_global_sdu_throughput_mbps', 'Global PDCP SDU Mbps', ['direction'])
ocu_pdcp_global_latency_seconds = Gauge('ocu_pdcp_global_latency_seconds', 'Global PDCP latency', ['direction', 'statistic'])

# -- ODU: RLC Metrics --
l_rlc = ['ue_id', 'drb_id', 'direction']
odu_rlc_sdus = Gauge('odu_rlc_sdus', 'RLC SDUs', l_rlc)
odu_rlc_sdu_bytes = Gauge('odu_rlc_sdu_bytes', 'RLC SDU bytes', l_rlc)
odu_rlc_pdus = Gauge('odu_rlc_pdus', 'RLC PDUs', l_rlc)
odu_rlc_pdu_bytes = Gauge('odu_rlc_pdu_bytes', 'RLC PDU bytes', l_rlc)

l_rlc_err = ['ue_id', 'drb_id']
odu_rlc_lost_pdus = Gauge('odu_rlc_lost_pdus', 'RLC lost PDUs (RX)', l_rlc_err)
odu_rlc_malformed_pdus = Gauge('odu_rlc_malformed_pdus', 'RLC malformed PDUs (RX)', l_rlc_err)
odu_rlc_dropped_sdus = Gauge('odu_rlc_dropped_sdus', 'RLC dropped SDUs (TX)', l_rlc_err)
odu_rlc_discarded_sdus = Gauge('odu_rlc_discarded_sdus', 'RLC discarded SDUs (TX)', l_rlc_err)
odu_rlc_discard_failures = Gauge('odu_rlc_discard_failures', 'RLC discard failures (TX)', l_rlc_err)

odu_rlc_pdu_latency_seconds = Gauge('odu_rlc_pdu_latency_seconds', 'RLC PDU latency', ['ue_id', 'drb_id', 'statistic'])
odu_rlc_pull_latency_bin = Gauge('odu_rlc_pull_latency_bin', 'RLC pull latency histogram', ['ue_id', 'drb_id', 'bin_start_us'])

# -- ODU: RU (Radio Unit) Metrics --
odu_ru_radio_events = Gauge('odu_ru_radio_events', 'RU radio events', ['event'])
odu_ru_power_db = Gauge('odu_ru_power_db', 'RU baseband power dB', ['pci', 'direction', 'statistic'])
odu_ru_papr_db = Gauge('odu_ru_papr_db', 'RU PAPR dB', ['pci', 'direction'])
odu_ru_clipping_ratio = Gauge('odu_ru_clipping_ratio', 'RU clipping probability', ['pci', 'direction'])

# -- OCU: RRC Metrics --
ocu_rrc_establishments = Gauge('ocu_rrc_establishments', 'RRC connection establishments', ['gnb_du_id', 'cause', 'result'])
ocu_rrc_establishment_failures = Gauge('ocu_rrc_establishment_failures', 'RRC connection establishment failures', ['gnb_du_id', 'cause'])
ocu_rrc_connections = Gauge('ocu_rrc_connections', 'RRC connections count', ['gnb_du_id', 'state', 'statistic'])
ocu_rrc_reestablishments = Gauge('ocu_rrc_reestablishments', 'RRC connection reestablishments', ['gnb_du_id', 'result'])
ocu_rrc_handover_executions = Gauge('ocu_rrc_handover_executions', 'RRC handover executions', ['result'])

# -- OCU: NGAP Metrics --
ocu_ngap_amf_connected = Gauge('ocu_ngap_amf_connected', 'AMF connection status (1=up, 0=down)', ['amf'])
ocu_ngap_paging_requests = Gauge('ocu_ngap_paging_requests', 'NGAP paging requests', ['amf'])
ocu_ngap_pdu_sessions = Gauge('ocu_ngap_pdu_sessions', 'NGAP PDU sessions', ['amf', 'snssai', 'result'])
ocu_ngap_pdu_session_failures = Gauge('ocu_ngap_pdu_session_failures', 'NGAP PDU session failures', ['amf', 'snssai', 'cause'])
ocu_ngap_handover_preparations = Gauge('ocu_ngap_handover_preparations', 'NGAP handover preparations', ['result'])

# ODU MAC Metrics
odu_mac_dl_average_latency_us = Gauge('odu_mac_dl_average_latency_us', 'MAC DL Average Latency (us)', ['pci'])
odu_mac_dl_max_latency_us = Gauge('odu_mac_dl_max_latency_us', 'MAC DL Max Latency (us)', ['pci'])
odu_mac_dl_min_latency_us = Gauge('odu_mac_dl_min_latency_us', 'MAC DL Min Latency (us)', ['pci'])

# --- ENERGÍA Y RECURSOS (Gymnasium) ---
app_cpu_usage = Gauge('app_cpu_usage_percent', 'Uso de CPU', ['nf'])
app_memory_usage = Gauge('app_memory_usage_mb', 'Uso de RAM', ['nf'])
app_power_consumption = Gauge('app_power_consumption_watts', 'Consumo en Vatios', ['nf'])

# --- PHY / BANDA BASE (du_low) ---
odu_phy_qpsk_mbps = Gauge('odu_phy_qpsk_throughput_mbps', 'QPSK Throughput', ['direction'])
odu_phy_ldpc_lat = Gauge('odu_phy_ldpc_average_latency_us', 'LDPC Latency', ['direction'])
odu_phy_precoding_lat = Gauge('odu_phy_precoding_average_latency_us', 'Precoding Latency', ['direction'])

# --- RU (SDR Tx/Rx) ---
odu_ru_tx_power = Gauge('odu_ru_tx_power_db', 'RU TX Power', ['pci'])
odu_ru_tx_papr = Gauge('odu_ru_tx_papr_db', 'RU TX PAPR', ['pci'])
odu_ru_rx_power = Gauge('odu_ru_rx_power_db', 'RU RX Power', ['pci'])

# --- SCHEDULER EXTRA (PRBs y Latencia MAC) ---
odu_mac_prbs_used = Gauge('odu_mac_prbs_used_total', 'PRBs Usados (Suma total del slot)', ['pci', 'direction'])
odu_mac_latency_histogram = Gauge('odu_mac_latency_histogram_bin', 'Distribucion de latencia', ['pci', 'bin_index'])

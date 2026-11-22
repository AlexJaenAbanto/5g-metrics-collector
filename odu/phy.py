import metrics

def parse_phy(data):
    du_low = data.get("du_low", {})
    
    # DOWNLINK
    dl = du_low.get("dl", {})
    if "modulation_mapper" in dl:
        metrics.odu_phy_qpsk_mbps.labels(direction="dl").set(dl["modulation_mapper"].get("qpsk_mod_throughput_mbps", 0))
    if "ldpc_encoder" in dl:
        metrics.odu_phy_ldpc_lat.labels(direction="dl").set(dl["ldpc_encoder"].get("average_latency_us", 0))
    if "precoding_layer_mapping" in dl:
        metrics.odu_phy_precoding_lat.labels(direction="dl").set(dl["precoding_layer_mapping"].get("average_latency_us", 0))
        
    # UPLINK
    ul = du_low.get("ul", {})
    if "demodulation_mapper" in ul:
        metrics.odu_phy_qpsk_mbps.labels(direction="ul").set(ul["demodulation_mapper"].get("qpsk_mod_throughput_mbps", 0))

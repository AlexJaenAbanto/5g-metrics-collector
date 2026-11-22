import json
from dispatcher import dispatch
from prometheus_client import REGISTRY

def run_test():
    with open('fixture_rlc.json', 'r') as f:
        data = json.load(f)
    
    dispatch(data)
    
    rx_sdu_bytes = REGISTRY.get_sample_value('odu_rlc_sdu_bytes', {'ue_id': '0', 'drb_id': '1', 'direction': 'rx'})
    tx_max_latency = REGISTRY.get_sample_value('odu_rlc_pdu_latency_seconds', {'ue_id': '0', 'drb_id': '1', 'statistic': 'max'})
    bin_1_us = REGISTRY.get_sample_value('odu_rlc_pull_latency_bin', {'ue_id': '0', 'drb_id': '1', 'bin_start_us': '1'})
    
    print(f"✅ Extracción RX SDU Bytes: {rx_sdu_bytes}")
    print(f"✅ Extracción TX Max Latency: {tx_max_latency} s")
    print(f"✅ Extracción TX Pull Latency (bin 1 us): {bin_1_us} eventos")

if __name__ == "__main__":
    run_test()

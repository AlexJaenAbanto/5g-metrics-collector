import json
from dispatcher import dispatch
from prometheus_client import REGISTRY

def run_test():
    with open('fixture_pdcp.json', 'r') as f:
        data = json.load(f)
    
    dispatch(data)
    
    # Extraemos valores para validar[cite: 1]
    dl_tput = REGISTRY.get_sample_value('ocu_pdcp_pdu_throughput_mbps', {'ue_index': '0', 'rb_type': 'DRB', 'rb_id': '1', 'direction': 'dl'})
    ul_reordering = REGISTRY.get_sample_value('ocu_pdcp_reordering_delay_seconds', {'ue_index': '0', 'rb_type': 'DRB', 'rb_id': '1'})
    bin_overflow = REGISTRY.get_sample_value('ocu_pdcp_latency_bin', {'ue_index': '0', 'rb_type': 'DRB', 'rb_id': '1', 'direction': 'dl', 'bin': '>=7 us'})
    global_sdu = REGISTRY.get_sample_value('ocu_pdcp_global_sdus', {'direction': 'ul'})
    
    print(f"✅ Extracción Throughput DL: {dl_tput} Mbps")
    print(f"✅ Extracción UL Reordering: {ul_reordering} s")
    print(f"✅ Extracción DL Overflow Bin (>=7 us): {bin_overflow} eventos")
    print(f"✅ Extracción Global SDUs UL: {global_sdu} SDUs")

if __name__ == "__main__":
    run_test()

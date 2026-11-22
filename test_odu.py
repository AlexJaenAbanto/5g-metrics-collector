import json
from dispatcher import dispatch
from prometheus_client import REGISTRY

def run_test():
    with open('fixture_cells.json', 'r') as f:
        data = json.load(f)
    
    dispatch(data)
    
    dl_brate = REGISTRY.get_sample_value('odu_scheduler_bitrate_bps', {'pci': '1', 'ue_id': '1', 'direction': 'dl'})
    ta_s = REGISTRY.get_sample_value('odu_radio_timing_advance_seconds', {'pci': '1', 'ue_id': '1', 'source': 'ta'})
    
    print(f"✅ Extracción DL Bitrate: {dl_brate} bps")
    print(f"✅ Extracción TA: {ta_s} segundos")

if __name__ == "__main__":
    run_test()

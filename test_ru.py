import json
from dispatcher import dispatch
from prometheus_client import REGISTRY

def run_test():
    with open('fixture_ru.json', 'r') as f:
        data = json.load(f)
    
    dispatch(data)
    
    rx_avg_power = REGISTRY.get_sample_value('odu_ru_power_db', {'pci': '1', 'direction': 'rx', 'statistic': 'average'})
    tx_clipping = REGISTRY.get_sample_value('odu_ru_clipping_ratio', {'pci': '1', 'direction': 'tx'})
    overflows = REGISTRY.get_sample_value('odu_ru_radio_events', {'event': 'overflow'})
    
    print(f"✅ Extracción RX Avg Power: {rx_avg_power} dB")
    print(f"✅ Extracción TX Clipping: {tx_clipping}")
    print(f"✅ Extracción Overflows: {overflows} eventos")

if __name__ == "__main__":
    run_test()

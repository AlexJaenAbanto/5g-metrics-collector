import json
from dispatcher import dispatch
from prometheus_client import REGISTRY

def run_test():
    with open('fixture_cu_up.json', 'r') as f:
        data = json.load(f)
    
    dispatch(data)
    
    # Extraemos el valor del primer bin del histograma
    bin_0 = REGISTRY.get_sample_value('ocu_e1ap_release_latency_bin', {'bin': '[0, 100) ms'})
    setup_ops = REGISTRY.get_sample_value('ocu_e1ap_bearer_context_operations', {'operation': 'setup', 'result': 'successful'})
    
    print(f"✅ Extracción E1AP Bin 0: {bin_0} eventos")
    print(f"✅ Extracción E1AP Setups: {setup_ops} eventos")

if __name__ == "__main__":
    run_test()

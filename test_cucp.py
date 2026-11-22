import json
from dispatcher import dispatch
from prometheus_client import REGISTRY

def run_test():
    with open('fixture_cucp.json', 'r') as f:
        data = json.load(f)
    
    dispatch(data)
    
    rrc_att = REGISTRY.get_sample_value('ocu_rrc_establishments', {'gnb_du_id': '0', 'cause': 'mps_prio_access', 'result': 'attempted'})
    rrc_succ = REGISTRY.get_sample_value('ocu_rrc_establishments', {'gnb_du_id': '0', 'cause': 'mps_prio_access', 'result': 'successful'})
    ngap_succ = REGISTRY.get_sample_value('ocu_ngap_pdu_sessions', {'amf': 'open5gs-amf0', 'snssai': '(sst=1 sd=na)', 'result': 'successful'})
    amf_conn = REGISTRY.get_sample_value('ocu_ngap_amf_connected', {'amf': 'open5gs-amf0'})
    
    print(f"✅ Extracción RRC Attempted (mps_prio_access): {rrc_att}")
    print(f"✅ Extracción RRC Successful (mps_prio_access): {rrc_succ}")
    print(f"✅ Extracción NGAP PDU Successful: {ngap_succ}")
    print(f"✅ Extracción AMF Connected: {amf_conn}")

if __name__ == "__main__":
    run_test()

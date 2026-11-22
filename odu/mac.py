import metrics

def parse_mac(data):
    # Navegar por la jerarquía: data -> du -> du_high -> mac -> dl
    du_high = data.get("du", {}).get("du_high", {})
    mac_data = du_high.get("mac", {})
    
    # Extraer las métricas del downlink (DL)
    for cell in mac_data.get("dl", []):
        pci = str(cell.get("pci", "unknown"))
        
        if "average_latency_us" in cell:
            metrics.odu_mac_dl_average_latency_us.labels(pci=pci).set(cell["average_latency_us"])
            
        if "max_latency_us" in cell:
            metrics.odu_mac_dl_max_latency_us.labels(pci=pci).set(cell["max_latency_us"])
            
        if "min_latency_us" in cell:
            metrics.odu_mac_dl_min_latency_us.labels(pci=pci).set(cell["min_latency_us"])

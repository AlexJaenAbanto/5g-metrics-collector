import metrics

def parse_ru(data):
    cells = data.get("ru", {}).get("sdr", {}).get("cells", [])
    for cell in cells:
        pci = str(cell.get("pci", "unknown"))
        tx = cell.get("tx", {})
        rx = cell.get("rx", {})
        
        if "average_power_db" in tx: metrics.odu_ru_tx_power.labels(pci=pci).set(tx["average_power_db"])
        if "papr_db" in tx: metrics.odu_ru_tx_papr.labels(pci=pci).set(tx["papr_db"])
        if "average_power_db" in rx: metrics.odu_ru_rx_power.labels(pci=pci).set(rx["average_power_db"])

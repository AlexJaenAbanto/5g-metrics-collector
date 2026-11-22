import metrics

def parse_resources(data):
    # Usamos la etiqueta que inyectamos en main.py (odu o ocu)
    nf = data.get("_source", "unknown")
    res = data.get("app_resource_usage", {})
    
    if "cpu_usage_percent" in res:
        metrics.app_cpu_usage.labels(nf=nf).set(res["cpu_usage_percent"])
    if "memory_usage_mb" in res:
        metrics.app_memory_usage.labels(nf=nf).set(res["memory_usage_mb"])
    if "power_consumption_watts" in res:
        metrics.app_power_consumption.labels(nf=nf).set(res["power_consumption_watts"])

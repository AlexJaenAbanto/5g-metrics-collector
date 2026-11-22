import json
import time
import threading
import traceback
import websocket
from prometheus_client import start_http_server, Gauge, Counter
from dispatcher import dispatch  # <--- IMPORTANTE: Importar el dispatcher

# KPI.3.4.1: Métricas de autoobservabilidad
COLLECTOR_UP = Gauge('collector_source_up', 'Estado de conexion WS (1=up, 0=down)', ['source'])
MSGS_RECEIVED = Counter('collector_messages_received_total', 'Mensajes totales recibidos', ['source'])
PARSE_ERRORS = Counter('collector_parse_errors_total', 'Errores de parseo JSON', ['source', 'family'])

def ws_worker(source_name, ws_url):
    """Worker persistente para consumir el WebSocket de telemetría."""
    while True:
        print(f"[{source_name}] Conectando a {ws_url}...")
        try:
            ws = websocket.create_connection(ws_url, timeout=10)
            COLLECTOR_UP.labels(source=source_name).set(1)
            print(f"[{source_name}] Conectado. Enviando suscripción...")
            ws.send(json.dumps({"cmd": "metrics_subscribe"}))

            while True:
                msg = ws.recv()

                MSGS_RECEIVED.labels(source=source_name).inc()

                try:
                    data = json.loads(msg)

                    # 2. GUARD CLAUSE: Evitar el error 'NoneType' verificando que es un diccionario
                    if not data or not isinstance(data, dict):
                        print(f"[{source_name}] Paquete ignorado (no es un diccionario válido)")
                        continue

                    if data.get("cmd") == "metrics_subscribe":
                        continue

                    # INYECTAR EL ORIGEN PARA PODER ETIQUETAR LA ENERGÍA
                    data["_source"] = source_name

                    # Enrutar el JSON a los parsers correspondientes
                    dispatch(data)

                except json.JSONDecodeError:
                    PARSE_ERRORS.labels(source=source_name, family="unknown").inc()
                    print(f"[{source_name}] Error decodificando JSON. Mensaje: {msg}")

        except Exception as e:
            print(f"[{source_name}] Desconectado: {e}")
            # 3. TRAZA COMPLETA: Muestra la línea exacta donde ocurre el crasheo
            traceback.print_exc()
        finally:
            COLLECTOR_UP.labels(source=source_name).set(0)
            print(f"[{source_name}] Reintentando en 5 segundos...")
            time.sleep(5)

if __name__ == "__main__":
    print("Iniciando 5G Metrics Collector v1...")

    start_http_server(9105)
    print("Servidor Prometheus expuesto en http://127.0.0.1:9105/metrics")

    odu_thread = threading.Thread(
        target=ws_worker,
        args=("odu", "ws://192.168.50.20:8001"),
        daemon=True
    )
    odu_thread.start()

    ocu_thread = threading.Thread(
        target=ws_worker,
        args=("ocu", "ws://192.168.50.21:8001"),
        daemon=True
    )
    ocu_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Deteniendo collector.")

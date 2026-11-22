import json
import websocket

def capture_pdcp_fixture():
    ws_url = "ws://192.168.50.21:8001"
    print(f"Conectando a {ws_url} para capturar PDCP...")
    
    ws = websocket.create_connection(ws_url, timeout=10)
    ws.send(json.dumps({"cmd": "metrics_subscribe"}))
    
    print("Suscrito. Generando captura... (Asegúrate de inyectar tráfico en la red)")
    
    while True:
        msg = ws.recv()
        # Filtramos explícitamente para asegurar que el frame contiene PDCP
        if '"pdcp":' in msg:
            parsed = json.loads(msg)
            with open("fixture_pdcp.json", "w") as f:
                json.dump(parsed, f, indent=2)
            print("¡Captura exitosa! Guardado en 'fixture_pdcp.json'.")
            break
            
    ws.close()

if __name__ == "__main__":
    capture_pdcp_fixture()

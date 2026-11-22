import json
import websocket

def capture_cucp_fixture():
    # Usamos la IP F1 de CU
    ws_url = "ws://192.168.50.21:8001"
    print(f"Conectando a {ws_url} para capturar Control Plane (CU-CP)...")
    
    ws = websocket.create_connection(ws_url, timeout=10)
    ws.send(json.dumps({"cmd": "metrics_subscribe"}))
    
    print("Suscrito. Esperando mensaje de la familia 'cu-cp'...")
    print("(Consejo: Pon un móvil en modo avión y quítalo para forzar eventos RRC/NGAP)")
    
    while True:
        msg = ws.recv()
        # Filtramos explícitamente para asegurar que el frame contiene cu-cp
        if '"cu-cp":' in msg:
            parsed = json.loads(msg)
            with open("fixture_cucp.json", "w") as f:
                json.dump(parsed, f, indent=2)
            print("¡Captura exitosa! Guardado en 'fixture_cucp.json'.")
            break
            
    ws.close()

if __name__ == "__main__":
    capture_cucp_fixture()

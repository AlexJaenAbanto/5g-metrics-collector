import json
import websocket

def capture_rlc_fixture():
    ws_url = "ws://192.168.50.20:8001"
    print(f"Conectando a {ws_url} para capturar RLC...")
    
    ws = websocket.create_connection(ws_url, timeout=10)
    ws.send(json.dumps({"cmd": "metrics_subscribe"}))
    
    print("Suscrito. Esperando mensaje de la familia 'rlc_metrics'...")
    
    while True:
        msg = ws.recv()
        # Buscamos la clave rlc_metrics en el string
        if '"rlc_metrics":' in msg:
            parsed = json.loads(msg)
            with open("fixture_rlc.json", "w") as f:
                json.dump(parsed, f, indent=2)
            print("¡Captura exitosa! Guardado en 'fixture_rlc.json'.")
            break
            
    ws.close()

if __name__ == "__main__":
    capture_rlc_fixture()

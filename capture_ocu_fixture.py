import json
import websocket

def capture_ocu_fixture():
    # Usamos la IP de la interfaz F1 de CU donde está escuchando el OCU
    ws_url = "ws://192.168.50.21:8001"
    print(f"Conectando a {ws_url} para capturar fixture OCU...")
    
    ws = websocket.create_connection(ws_url, timeout=10)
    ws.send(json.dumps({"cmd": "metrics_subscribe"}))
    
    print("Suscrito. Esperando mensaje de la familia 'cu-up'...")
    
    while True:
        msg = ws.recv()
        # Buscamos la clave cu-up para aislar ese payload específico
        if '"cu-up":' in msg:
            parsed = json.loads(msg)
            with open("fixture_cu_up.json", "w") as f:
                json.dump(parsed, f, indent=2)
            print("¡Captura exitosa! Guardado en 'fixture_cu_up.json'.")
            break
            
    ws.close()

if __name__ == "__main__":
    capture_ocu_fixture()

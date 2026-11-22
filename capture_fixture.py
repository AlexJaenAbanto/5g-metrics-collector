import json
import websocket

def capture_cells_fixture():
    ws_url = "ws://192.168.50.20:8001"
    print(f"Conectando a {ws_url} para capturar fixture...")
    
    ws = websocket.create_connection(ws_url, timeout=10)
    ws.send(json.dumps({"cmd": "metrics_subscribe"}))
    
    print("Suscrito. Esperando un mensaje de la familia 'cells'...")
    
    while True:
        msg = ws.recv()
        # Buscamos la clave "cells" en el string para no parsear todo
        if '"cells":' in msg:
            parsed = json.loads(msg)
            with open("fixture_cells.json", "w") as f:
                json.dump(parsed, f, indent=2)
            print("¡Captura exitosa! Guardado en 'fixture_cells.json'.")
            break
            
    ws.close()

if __name__ == "__main__":
    capture_cells_fixture()

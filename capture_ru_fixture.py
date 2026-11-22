import json
import websocket

def capture_ru_fixture():
    ws_url = "ws://192.168.50.20:8001"
    print(f"Conectando a {ws_url} para capturar métricas de Radio (RU)...")
    
    ws = websocket.create_connection(ws_url, timeout=10)
    ws.send(json.dumps({"cmd": "metrics_subscribe"}))
    
    print("Suscrito. Esperando mensaje de la familia 'ru'...")
    
    while True:
        msg = ws.recv()
        # Buscamos la familia ru que contiene la extensión sdr
        if '"ru":' in msg:
            parsed = json.loads(msg)
            with open("fixture_ru.json", "w") as f:
                json.dump(parsed, f, indent=2)
            print("¡Captura exitosa! Guardado en 'fixture_ru.json'.")
            break
            
    ws.close()

if __name__ == "__main__":
    capture_ru_fixture()

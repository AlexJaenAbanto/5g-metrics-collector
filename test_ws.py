import json
import websocket

def test_odu_ws():
    ws_url = "ws://192.168.50.20:8001"
    print(f"Conectando a {ws_url}...")
    
    try:
        ws = websocket.WebSocket()
        ws.connect(ws_url)
        print("Conectado. Enviando comando de suscripción...")
        
        subscribe_cmd = json.dumps({"cmd": "metrics_subscribe"})
        ws.send(subscribe_cmd)
        
        print("Esperando telemetría...")
        msg = ws.recv()
        
        print("\n--- Primer mensaje recibido ---")
        parsed = json.loads(msg)
        # Imprimimos los primeros 500 caracteres en formato compacto
        compact_json = json.dumps(parsed, separators=(",", ":"))
        print(compact_json[:500] + ("..." if len(compact_json) > 500 else ""))
        
        ws.close()
        print("\nConexión cerrada correctamente.")
        
    except Exception as e:
        print(f"Error durante la prueba: {e}")

if __name__ == "__main__":
    test_odu_ws()

import time
import requests

TOKEN = "8154770563:AAE7ezP0940cGF9eQ4Cpw0LDJ2qQH2AbDho"
CHAT_ID_GROUP = "-1003758191885"
CHAT_ID_PRIVADO_1 = "347020516"
CHAT_ID_PRIVADO_2 = "1718805531"  # Nuevo chat_id

def send_message(chat_id, text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": chat_id, "text": text}
        )
    except Exception as e:
        print(f"Error enviando mensaje: {e}")

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {'timeout': 60}
    if offset:
        params['offset'] = offset
    res = requests.get(url, params=params)
    if res.status_code == 200:
        return res.json().get('result', [])
    return []

def main():
    last_seen = time.time()
    heartbeat_timeout = 10  # segundos (ajustable)
    offset = None
    print("Bot escuchando cualquier mensaje en el grupo...")

    while True:
        updates = get_updates(offset)
        for upd in updates:
            offset = upd['update_id'] + 1
            msg = upd.get('message', {})
            chat_id = str(msg.get('chat', {}).get('id', ''))
            texto = msg.get('text', '')
            if chat_id == CHAT_ID_GROUP:
                last_seen = time.time()
                print("Recibido mensaje en el grupo, timer reseteado")
                # Si detecta "ERROR 500"
                if texto and "ERROR 500" in texto:
                    mensaje_error = f"⚠️ Detectado mensaje de ERROR 500 en el grupo: \"{texto}\""
                    send_message(CHAT_ID_PRIVADO_1, mensaje_error)
                    send_message(CHAT_ID_PRIVADO_2, mensaje_error)
                    print("Notificación privada enviada por error 500 a ambos usuarios.")
        if time.time() - last_seen > heartbeat_timeout:
            alerta = "¡Alerta BOT 2! No se recibió ningún mensaje en el grupo en los últimos 10 segundos."
            send_message(CHAT_ID_PRIVADO_1, alerta)
            send_message(CHAT_ID_PRIVADO_2, alerta)
            print("Alerta enviada por inactividad a ambos usuarios.")
            last_seen = time.time()
        time.sleep(2)

if __name__ == "__main__":
    main()

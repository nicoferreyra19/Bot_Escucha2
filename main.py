import time
import requests

TOKEN = "8154770563:AAE7ezP0940cGF9eQ4Cpw0LDJ2qQH2AbDho"  # Del nuevo bot
CHAT_ID_GROUP = "-4986505595"
CHAT_ID_PRIVADO_1 = "347020516"
CHAT_ID_PRIVADO_2 = "1718805531"

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
    heartbeat_timeout = 10
    offset = None
    print("Bot 2 escuchando 'PC Online 2' en el grupo...")

    while True:
        updates = get_updates(offset)
        for upd in updates:
            offset = upd['update_id'] + 1
            msg = upd.get('message', {})
            chat_id = str(msg.get('chat', {}).get('id', ''))
            texto = msg.get('text', '')
            if chat_id == CHAT_ID_GROUP and "PC Online 2" in texto:  # ← Cambio clave
                last_seen = time.time()
                print("Recibido 'PC Online 2', timer reseteado")
            elif chat_id == CHAT_ID_GROUP and "ERROR 500" in texto:
                mensaje_error = f"⚠️ ERROR 500 detectado en grupo: \"{texto}\""
                send_message(CHAT_ID_PRIVADO_1, mensaje_error)
                send_message(CHAT_ID_PRIVADO_2, mensaje_error)
        if time.time() - last_seen > heartbeat_timeout:
            alerta = "¡Alerta PC 2! No 'PC Online 2' en 10s."
            send_message(CHAT_ID_PRIVADO_1, alerta)
            send_message(CHAT_ID_PRIVADO_2, alerta)
            last_seen = time.time()
        time.sleep(2)

if __name__ == "__main__":
    main()

import os
import requests

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN не найден")

API = f"https://api.telegram.org/bot{TOKEN}"


def send_message(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        },
        timeout=30
    )


offset = 0

while True:
    response = requests.get(
        f"{API}/getUpdates",
        params={
            "offset": offset,
            "timeout": 30
        },
        timeout=40
    )

    data = response.json()

    for update in data.get("result", []):
        offset = update["update_id"] + 1

        message = update.get("message")
        if not message:
            continue

        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text == "/start":
            send_message(
                chat_id,
                "Привет! Я OSINT-бот.\n\n"
                "Отправь мне имя или никнейм, "
                "и я попробую найти информацию "
                "в открытых источниках."
            )
        else:
            send_message(
                chat_id,
                f"Получил запрос:\n{text}\n\n"
                "Модуль поиска пока подключается."
            )

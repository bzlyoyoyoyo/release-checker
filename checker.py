import requests
import os

URL = "https://api.mixtape.so/albums/earliest-release"

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

def main():
    res = requests.get(URL)
    data = res.json()

    current = data["contents"]["data"]["earliest_release_at"]

    try:
        with open("prev.txt", "r") as f:
            prev = f.read().strip()
    except:
        prev = None

    print("현재:", current)

    if prev and current != prev:
        send(f"🔥 발매 가능일 변경: {current}")

    with open("prev.txt", "w") as f:
        f.write(current)

if __name__ == "__main__":
    main()

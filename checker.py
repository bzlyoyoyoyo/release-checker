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

    print("현재:", current)

    # 테스트용 (무조건 전송)
    send(f"테스트 알림: {current}")

if __name__ == "__main__":
    main()

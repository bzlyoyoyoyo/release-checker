import requests
import os
from datetime import datetime

URL = "https://api.mixtape.so/albums/earliest-release"

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send(msg):
    # 강한 알림
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

def send_silent(msg):
    # 무음 알림
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg,
            "disable_notification": True
        }
    )

def main():
    res = requests.get(URL)
    data = res.json()
    current = data["contents"]["data"]["earliest_release_at"]

    now = datetime.now()
    current_hour = now.hour

    # 이전 값
    try:
        with open("prev.txt", "r") as f:
            prev = f.read().strip()
    except:
        prev = None

    # 마지막 무음 알림 시간 (중복 방지용)
    try:
        with open("last_silent.txt", "r") as f:
            last_sent = f.read().strip()
    except:
        last_sent = ""

    print("현재:", current)

    # 1️⃣ 변경 시 강한 알림
    if prev and current != prev:
        send(f"🔥 발매 가능일 변경: {current}")

    # 2️⃣ 특정 시간 무음 알림
    target_hours = [6, 12, 18, 0]

    today_key = now.strftime("%Y-%m-%d") + f"_{current_hour}"

    if current_hour in target_hours and last_sent != today_key:
        send_silent(f"현재 발매일: {current}")
        with open("last_silent.txt", "w") as f:
            f.write(today_key)

    # 값 저장
    with open("prev.txt", "w") as f:
        f.write(current)

if __name__ == "__main__":
    main()

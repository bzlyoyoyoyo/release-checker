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
    hour = now.hour
    minute = now.minute

    # 이전 값
    try:
        with open("prev.txt", "r") as f:
            prev = f.read().strip()
    except:
        prev = None

    # 마지막 무음 알림 기록
    try:
        with open("last_silent.txt", "r") as f:
            last_sent = f.read().strip()
    except:
        last_sent = ""

    print("현재:", current)

    # 1️⃣ 변경 시 강한 알림
    if prev and current != prev:
        send(f"🔥 발매 가능일 변경: {current}")

    # 2️⃣ 6:15 / 12:15 / 18:15 / 00:15 무음 알림
    target_times = [(6,15), (12,15), (18,15), (0,15)]

    time_key = now.strftime("%Y-%m-%d_%H_%M")

    for h, m in target_times:
        if hour == h and minute < 20:  # 15분 기준, 약간 여유
            unique_key = now.strftime("%Y-%m-%d") + f"_{h}_{m}"
            if last_sent != unique_key:
                send_silent(f"현재 발매일: {current}")
                with open("last_silent.txt", "w") as f:
                    f.write(unique_key)
            break

    # 값 저장
    with open("prev.txt", "w") as f:
        f.write(current)

if __name__ == "__main__":
    main()

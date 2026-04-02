import requests
import os
from datetime import datetime
from zoneinfo import ZoneInfo

URL = "https://api.mixtape.so/albums/earliest-release"

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send(msg):
    try:
        res = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg}
        )
        print("텔레그램 응답:", res.status_code, res.text)
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")

def send_silent(msg):
    try:
        res = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": msg,
                "disable_notification": True
            }
        )
        print("텔레그램 응답:", res.status_code, res.text)
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")

def main():
    # 🔥 무조건 테스트 메시지 보내기 (이게 핵심)
    send("🔥 테스트 메시지")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(URL, headers=headers, timeout=10)
        res.raise_for_status()
        data = res.json()
        current = data["contents"]["data"]["earliest_release_at"]
    except Exception as e:
        error_msg = f"⚠️ 서버 에러: {e}"
        print(error_msg)
        send(error_msg)
        return

    now = datetime.now(ZoneInfo("Asia/Seoul"))
    hour = now.hour
    minute = now.minute

    try:
        with open("prev.txt", "r", encoding="utf-8") as f:
            prev = f.read().strip()
    except FileNotFoundError:
        prev = None

    try:
        with open("last_silent.txt", "r", encoding="utf-8") as f:
            last_sent = f.read().strip()
    except FileNotFoundError:
        last_sent = ""

    print(f"현재 시간: {now} | 데이터: {current}")

    if prev is not None and current != prev:
        send(f"🔥 변경됨: {current}")

    target_times = [0, 6, 12, 18]

    for h in target_times:
        if hour == h and 0 <= minute < 20:
            key = now.strftime("%Y-%m-%d") + f"_{h}"

            if last_sent != key:
                send_silent(f"현재 발매일: {current}")
                with open("last_silent.txt", "w", encoding="utf-8") as f:
                    f.write(key)
            break

    with open("prev.txt", "w", encoding="utf-8") as f:
        f.write(current)

if __name__ == "__main__":
    main()

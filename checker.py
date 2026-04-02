import requests
import os
from datetime import datetime
from zoneinfo import ZoneInfo # 파이썬 3.9 이상 기본 모듈

URL = "https://api.mixtape.so/albums/earliest-release"

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send(msg):
    # 강한 알림
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg}
        )
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")

def send_silent(msg):
    # 무음 알림
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": msg,
                "disable_notification": True
            }
        )
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")

def main():
    try:
        res = requests.get(URL, timeout=10)
        res.raise_for_status()
        data = res.json()
        current = data["contents"]["data"]["earliest_release_at"]
    except Exception as e:
        print(f"API 호출 실패: {e}")
        return # API 에러 시 여기서 중단하여 파일 덮어쓰기 방지

    # 한국 시간(KST)으로 현재 시간 가져오기
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    hour = now.hour
    minute = now.minute

    # 이전 값 불러오기
    try:
        with open("prev.txt", "r", encoding="utf-8") as f:
            prev = f.read().strip()
    except FileNotFoundError:
        prev = None

    # 마지막 무음 알림 기록 불러오기
    try:
        with open("last_silent.txt", "r", encoding="utf-8") as f:
            last_sent = f.read().strip()
    except FileNotFoundError:
        last_sent = ""

    print(f"현재 KST 시간: {now.strftime('%Y-%m-%d %H:%M:%S')} | 데이터: {current}")

    # 1️⃣ 변경 시 강한 알림 (최초 실행 시 prev가 None이므로 알림 안 감)
    if prev is not None and current != prev:
        send(f"🔥 발매 가능일 변경: {current}")

    # 2️⃣ 06:15 / 12:15 / 18:15 / 00:15 무음 알림
    target_times = [6, 12, 18, 0]

    for h in target_times:
        # 깃허브 액션 지연을 고려해 15분 ~ 55분 사이에 실행되면 알림 발송
        if hour == h and 15 <= minute < 55:  
            unique_key = now.strftime("%Y-%m-%d") + f"_{h}_15"
            
            # 오늘 해당 시간대의 알림을 아직 안 보냈다면
            if last_sent != unique_key:
                send_silent(f"현재 발매일: {current}")
                # 보낸 기록 저장
                with open("last_silent.txt", "w", encoding="utf-8") as f:
                    f.write(unique_key)
            break # 조건에 맞으면 더 이상 반복할 필요 없음

    # 현재 값을 이전 값으로 저장
    with open("prev.txt", "w", encoding="utf-8") as f:
        f.write(current)

if __name__ == "__main__":
    main()

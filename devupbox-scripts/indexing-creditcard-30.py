"""
신용카드 30개 포스트 인덱싱 (IndexNow + Google Indexing API)
- Naver IndexNow
- Bing IndexNow
- Google Indexing API
"""
import json
import urllib.request
import urllib.error
import base64
import ssl
import time

from google.oauth2 import service_account
from googleapiclient.discovery import build

ssl._create_default_https_context = ssl._create_unverified_context

AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
WP_API = "https://devupbox.com/wp-json/wp/v2/posts"

# 신용카드 30개 포스트 ID (35350 ~ 35379)
POST_IDS = list(range(35350, 35380))


def fetch_post_url(post_id):
    url = f"{WP_API}/{post_id}?_fields=link"
    req = urllib.request.Request(url, headers={"Authorization": f"Basic {AUTH}"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("link")
    except Exception as e:
        print(f"  [WP ERROR] #{post_id}: {e}")
        return None


def submit_indexnow(urls):
    payload = {
        "host": "devupbox.com",
        "key": "8dbbd7d6729b4a65b7dce4b9083c65e3",
        "keyLocation": "https://devupbox.com/8dbbd7d6729b4a65b7dce4b9083c65e3.txt",
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")

    for engine_name, engine_url in [
        ("Naver", "https://searchadvisor.naver.com/indexnow"),
        ("Bing", "https://www.bing.com/indexnow"),
        ("Yandex", "https://yandex.com/indexnow"),
    ]:
        req = urllib.request.Request(engine_url, data=data, method="POST")
        req.add_header("Content-Type", "application/json; charset=utf-8")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                print(f"  {engine_name} IndexNow: HTTP {resp.status} ✅")
        except urllib.error.HTTPError as e:
            print(f"  {engine_name} IndexNow: HTTP {e.code}")
        except Exception as e:
            print(f"  {engine_name} IndexNow: {e}")


def submit_google_indexing(urls):
    SCOPES = ["https://www.googleapis.com/auth/indexing"]
    credentials = service_account.Credentials.from_service_account_file(
        "devupbox.json", scopes=SCOPES
    )
    service = build("indexing", "v3", credentials=credentials)

    success = 0
    fail = 0
    for i, url in enumerate(urls, 1):
        try:
            body = {"url": url, "type": "URL_UPDATED"}
            service.urlNotifications().publish(body=body).execute()
            print(f"  [{i:02d}/{len(urls)}] ✅ {url}")
            success += 1
        except Exception as e:
            print(f"  [{i:02d}/{len(urls)}] ❌ {url} | {str(e)[:80]}")
            fail += 1
        time.sleep(3)

    return success, fail


def main():
    # 1. URL 수집
    print("=" * 60)
    print("1단계: 포스트 URL 수집")
    print("=" * 60)
    urls = []
    for pid in POST_IDS:
        link = fetch_post_url(pid)
        if link:
            urls.append(link)
            print(f"  #{pid} → {link}")
        else:
            print(f"  #{pid} → ⚠️ 실패")
        time.sleep(0.2)
    print(f"\n총 {len(urls)}개 URL 수집 완료\n")

    # 2. IndexNow (Naver, Bing, Yandex)
    print("=" * 60)
    print("2단계: IndexNow (Naver, Bing, Yandex)")
    print("=" * 60)
    submit_indexnow(urls)
    print()

    # 3. Google Indexing API
    print("=" * 60)
    print("3단계: Google Indexing API")
    print("=" * 60)
    success, fail = submit_google_indexing(urls)
    print(f"\nGoogle 색인 요청: 성공 {success} / 실패 {fail}\n")

    print("=" * 60)
    print("완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

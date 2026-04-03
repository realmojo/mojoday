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
POST_IDS = list(range(35572, 35602))

def fetch_post_url(post_id):
    url = f"{WP_API}/{post_id}?_fields=link"
    req = urllib.request.Request(url, headers={"Authorization": f"Basic {AUTH}"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode()).get("link")
    except Exception as e:
        print(f"  [ERROR] #{post_id}: {e}")
        return None

def main():
    print("1단계: URL 수집")
    urls = []
    for pid in POST_IDS:
        link = fetch_post_url(pid)
        if link:
            urls.append(link)
            print(f"  #{pid} → {link}")
        time.sleep(0.2)
    print(f"\n총 {len(urls)}개 URL\n")

    print("2단계: IndexNow")
    payload = {"host": "devupbox.com", "key": "8dbbd7d6729b4a65b7dce4b9083c65e3", "keyLocation": "https://devupbox.com/8dbbd7d6729b4a65b7dce4b9083c65e3.txt", "urlList": urls}
    data = json.dumps(payload).encode("utf-8")
    for name, endpoint in [("Naver", "https://searchadvisor.naver.com/indexnow"), ("Bing", "https://www.bing.com/indexnow"), ("Yandex", "https://yandex.com/indexnow")]:
        req = urllib.request.Request(endpoint, data=data, method="POST")
        req.add_header("Content-Type", "application/json; charset=utf-8")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                print(f"  {name}: HTTP {resp.status}")
        except urllib.error.HTTPError as e:
            print(f"  {name}: HTTP {e.code}")
        except Exception as e:
            print(f"  {name}: {e}")

    print("\n3단계: Google Indexing API")
    creds = service_account.Credentials.from_service_account_file("devupbox.json", scopes=["https://www.googleapis.com/auth/indexing"])
    svc = build("indexing", "v3", credentials=creds)
    ok = 0
    for i, url in enumerate(urls, 1):
        try:
            svc.urlNotifications().publish(body={"url": url, "type": "URL_UPDATED"}).execute()
            print(f"  [{i:02d}/{len(urls)}] OK | {url}")
            ok += 1
        except Exception as e:
            print(f"  [{i:02d}/{len(urls)}] FAIL | {str(e)[:80]}")
        time.sleep(3)
    print(f"\nGoogle: {ok}/{len(urls)} 성공\n완료!")

if __name__ == "__main__":
    main()

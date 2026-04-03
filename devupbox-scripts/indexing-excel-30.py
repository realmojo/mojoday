import json, urllib.request, urllib.error, base64, ssl, time
from google.oauth2 import service_account
from googleapiclient.discovery import build
ssl._create_default_https_context = ssl._create_unverified_context
AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
WP_API = "https://devupbox.com/wp-json/wp/v2/posts"
POST_IDS = list(range(35664, 35694))

def fetch_url(pid):
    req = urllib.request.Request(f"{WP_API}/{pid}?_fields=link", headers={"Authorization": f"Basic {AUTH}"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r: return json.loads(r.read().decode()).get("link")
    except: return None

def main():
    print("1단계: URL 수집")
    urls = []
    for pid in POST_IDS:
        link = fetch_url(pid)
        if link: urls.append(link); print(f"  #{pid} → {link}")
        time.sleep(0.2)
    print(f"\n총 {len(urls)}개\n\n2단계: IndexNow")
    payload = {"host":"devupbox.com","key":"8dbbd7d6729b4a65b7dce4b9083c65e3","keyLocation":"https://devupbox.com/8dbbd7d6729b4a65b7dce4b9083c65e3.txt","urlList":urls}
    data = json.dumps(payload).encode()
    for n, ep in [("Naver","https://searchadvisor.naver.com/indexnow"),("Bing","https://www.bing.com/indexnow"),("Yandex","https://yandex.com/indexnow")]:
        req = urllib.request.Request(ep, data=data, method="POST"); req.add_header("Content-Type","application/json; charset=utf-8")
        try:
            with urllib.request.urlopen(req, timeout=30) as r: print(f"  {n}: HTTP {r.status}")
        except urllib.error.HTTPError as e: print(f"  {n}: HTTP {e.code}")
        except Exception as e: print(f"  {n}: {e}")
    print("\n3단계: Google Indexing API")
    creds = service_account.Credentials.from_service_account_file("devupbox.json", scopes=["https://www.googleapis.com/auth/indexing"])
    svc = build("indexing","v3",credentials=creds)
    ok=0
    for i,u in enumerate(urls,1):
        try: svc.urlNotifications().publish(body={"url":u,"type":"URL_UPDATED"}).execute(); print(f"  [{i:02d}/{len(urls)}] OK | {u}"); ok+=1
        except Exception as e: print(f"  [{i:02d}/{len(urls)}] FAIL | {str(e)[:80]}")
        time.sleep(3)
    print(f"\nGoogle: {ok}/{len(urls)}\n완료!")

if __name__=="__main__": main()

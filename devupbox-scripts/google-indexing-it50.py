import json
import urllib.request
import base64
import ssl
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

ssl._create_default_https_context = ssl._create_unverified_context

AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API = "https://devupbox.com/wp-json/wp/v2/posts"

# 1) 포스트 URL 수집
urls = []
for pid in range(34566, 34616):
    req = urllib.request.Request(f"{API}/{pid}?_fields=link")
    req.add_header("Authorization", f"Basic {AUTH}")
    with urllib.request.urlopen(req, timeout=15) as resp:
        r = json.loads(resp.read().decode())
        urls.append(r["link"])

# 트렌딩 5개 포스트 추가
urls += [
    "https://devupbox.com/kin/basic-pension-calculator-2026",
    "https://devupbox.com/kin/local-election-part-time-job-2026",
    "https://devupbox.com/kin/youth-rent-support-2026",
    "https://devupbox.com/finance/car-tax-refund-guide-2026",
    "https://devupbox.com/finance/capital-gains-tax-suspension-2026",
]

print(f"수집된 URL: {len(urls)}개\n")

# 2) Google Indexing API 인증
SCOPES = ["https://www.googleapis.com/auth/indexing"]
credentials = service_account.Credentials.from_service_account_file(
    "devupbox.json", scopes=SCOPES
)
service = build("indexing", "v3", credentials=credentials)

# 3) URL 제출
success = 0
fail = 0
for i, url in enumerate(urls, 1):
    try:
        body = {"url": url, "type": "URL_UPDATED"}
        response = service.urlNotifications().publish(body=body).execute()
        print(f"[{i}/{len(urls)}] OK | {url}")
        success += 1
    except Exception as e:
        print(f"[{i}/{len(urls)}] FAIL | {url} | {str(e)[:80]}")
        fail += 1
    time.sleep(3)

print(f"\n완료! 성공: {success}, 실패: {fail}")

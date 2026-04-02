"""
google-indexing-loan50.py
--------------------------
publish-loan-50-posts.py 로 발행된 50개 대출 포스트 (#34715~#34764)를
Google Indexing API 에 색인 요청.

사전 준비:
  pip install google-auth google-api-python-client
  devupbox.json (서비스 계정 키) 이 같은 폴더에 있어야 함.

Usage:
  python3 google-indexing-loan50.py
"""

import json
import urllib.request
import base64
import ssl
import time

from google.oauth2 import service_account
from googleapiclient.discovery import build

ssl._create_default_https_context = ssl._create_unverified_context

AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
WP_API = "https://devupbox.com/wp-json/wp/v2/posts"

# publish-loan-50-posts.py 로 발행된 포스트 ID 목록 (50개)
LOAN_POST_IDS = list(range(34715, 34765))  # 34715 ~ 34764


def fetch_post_url(post_id):
    """WP REST API 로 포스트 링크를 가져온다."""
    url = f"{WP_API}/{post_id}?_fields=link"
    req = urllib.request.Request(url, headers={"Authorization": f"Basic {AUTH}"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("link")
    except Exception as e:
        print(f"  [WP FETCH ERROR] post #{post_id}: {e}")
        return None


def submit_to_indexing_api(service, url):
    """Google Indexing API 에 URL_UPDATED 알림을 보낸다."""
    try:
        body = {"url": url, "type": "URL_UPDATED"}
        service.urlNotifications().publish(body=body).execute()
        return True
    except Exception as e:
        print(f"  [INDEXING ERROR] {url}: {str(e)[:120]}")
        return False


def main():
    # ── 1. WP API 로 실제 URL 수집 ──────────────────────────────────────────
    print(f"포스트 URL 수집 중 ({len(LOAN_POST_IDS)}개)...\n")
    urls = []
    for pid in LOAN_POST_IDS:
        link = fetch_post_url(pid)
        if link:
            urls.append(link)
            print(f"  #{pid} → {link}")
        else:
            print(f"  #{pid} → ⚠️  URL 조회 실패 (스킵)")
        time.sleep(0.3)

    print(f"\n총 {len(urls)}개 URL 수집 완료.\n")

    # ── 2. Google Indexing API 인증 ──────────────────────────────────────────
    SCOPES = ["https://www.googleapis.com/auth/indexing"]
    credentials = service_account.Credentials.from_service_account_file(
        "devupbox.json", scopes=SCOPES
    )
    service = build("indexing", "v3", credentials=credentials)

    # ── 3. 색인 요청 (일일 할당량 200개, 초당 200req 제한) ───────────────────
    print("Google Indexing API 색인 요청 중...\n")
    success = 0
    fail = 0
    for i, url in enumerate(urls, 1):
        ok = submit_to_indexing_api(service, url)
        status = "✅ OK  " if ok else "❌ FAIL"
        print(f"[{i:02d}/{len(urls)}] {status} | {url}")
        if ok:
            success += 1
        else:
            fail += 1
        time.sleep(3)  # API 할당량 준수

    print(f"\n{'=' * 60}")
    print(f"색인 요청 완료  |  성공: {success}  실패: {fail}  합계: {len(urls)}")
    print(f"{'=' * 60}")
    print("구글 Search Console > URL 검사에서 색인 상태를 확인하세요.")


if __name__ == "__main__":
    main()

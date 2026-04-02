"""
google-indexing-seo-boost.py
-----------------------------
seo-boost-gsc-posts.py 로 업데이트된 28개 포스트를 Google Indexing API 에 재색인 요청.

사전 준비:
  pip install google-auth google-api-python-client
  devupbox.json (서비스 계정 키) 이 같은 폴더에 있어야 함.

Usage:
  python3 google-indexing-seo-boost.py
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

# seo-boost-gsc-posts.py 에서 업데이트된 포스트 ID 목록 (28개)
UPDATED_POST_IDS = [
    20072,   # 인스타그램 게시물 음악 추가·수정·삭제
    20740,   # 카카오톡 챗봇 추가·삭제
    32608,   # 유튜브 쇼츠 노래 찾기
    34366,   # 인스타그램 활동 상태 오류
    33791,   # VRChat 아이폰 페이셜 트래킹
    28307,   # IBK 군적금 담보대출
    33785,   # 삼성 월렛 티머니 추가 오류
    32187,   # 카카오페이 상대 기관 오류
    34360,   # 카카오톡 구글 플레이 기프트카드
    20762,   # 갤럭시 에이닷 전화 단축번호
    20934,   # 카카오톡 멘션 알림 끄기
    21705,   # 트위터(X) 이름·아이디 바꾸기
    19453,   # 유튜브 프리미엄 남은 기간
    34109,   # 카카오톡 팀챗 제한·차단
    34085,   # 인스타그램 계정 추천 차단
    21822,   # 컴퓨터활용능력 자격증 사본 인쇄
    32682,   # 트위터 미디어 오류
    21876,   # 닌텐도 스위치 전원 끄기
    34342,   # 굿노트 폰트·아이콘 오류
    34208,   # 아이폰 문자·전화 차단 확인
    32857,   # 인스타 라이브 댓글 멈춤
    34193,   # 서든어택 마우스 렉 최적화
    21719,   # 엔비디아 FPS 표시 설정
    20040,   # 카카오톡 간편녹음 버튼
    33929,   # 알리페이 한국 결제 불가
    21473,   # 팟플레이어 AI 자막생성
    21908,   # 인스타그램 부계정 만들기
    24858,   # 엑셀 파일/시트 합치기
]


def fetch_post_url(post_id: int):
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


def submit_to_indexing_api(service, url: str) -> bool:
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
    print(f"포스트 URL 수집 중 ({len(UPDATED_POST_IDS)}개)...\n")
    urls = []
    for pid in UPDATED_POST_IDS:
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

    # ── 3. 색인 요청 ─────────────────────────────────────────────────────────
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
        time.sleep(3)  # API 할당량 준수 (초당 200req 제한)

    print(f"\n{'=' * 60}")
    print(f"색인 요청 완료  |  성공: {success}  실패: {fail}  합계: {len(urls)}")
    print(f"{'=' * 60}")
    print("구글 Search Console > URL 검사에서 색인 상태를 확인하세요.")


if __name__ == "__main__":
    main()

"""
seo-boost-gsc-posts.py
----------------------
WordPress SEO improvement script via WP REST API.
Processes GSC (Google Search Console) data and updates post titles/meta descriptions
to improve CTR for high-impression, low-CTR posts on devupbox.com.

Usage:
    python3 seo-boost-gsc-posts.py
    python3 seo-boost-gsc-posts.py --dry-run   (preview changes without applying)
    python3 seo-boost-gsc-posts.py --slug <slug>  (process single post)
"""

import json
import urllib.request
import urllib.error
import urllib.parse
import base64
import time
import ssl
import sys
import argparse
from typing import Optional, Tuple, List, Dict, Any

# ── SSL / Auth ──────────────────────────────────────────────────────────────
ssl._create_default_https_context = ssl._create_unverified_context

AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API  = "https://devupbox.com/wp-json/wp/v2"

# ── GSC Data ─────────────────────────────────────────────────────────────────
# Each entry: (url_path, clicks, impressions)
_RAW_GSC = [
    # TOP PRIORITY — high impressions, low CTR
    ("info/인스타그램-게시물-음악-수정-삭제-추가하는-7가지-방",              69,  2391),
    ("info/카카오톡-챗봇-추가와-제거-7단계-완벽-가이드-스마트",              33,  1174),
    ("kin/유튜브-쇼츠-노래-찾는-5가지-확실한-방법과-음악-검색",              33,   806),
    ("info/insta-activity-status-error-diagnosis",                           25,   641),
    ("info/kakaotalk-google-play-giftcard-barcode-exchange-guide",            16,   376),
    ("entry/카카오톡-챗봇-사용법-완벽-가이드-추가-제거-활용-방",             14,   499),
    ("info/samsung-wallet-tmoney-add-error-fix",                             13,   434),
    ("info/sudden-attack-mouse-lag-input-optimization",                      14,   152),
    ("info/goodnotes-font-icon-missing-fix-steps",                           14,   188),
    # MEDIUM
    ("info/vrchat-iphone-facial-tracking-setup",                             47,   650),
    ("finance/ibk-군적금-담보대출-신청이-안되는-7가지-이유와-해결책",         38,   504),
    ("kin/카카오페이-상대-기관-업무-개시-이전-오류-해결-7가지",               28,   396),
    ("entry/유튜브-프리미엄-남은기간-조회하는-방법",                          29,   288),
    ("info/트위터-x-이름-바꾸기-7단계-완벽-가이드-아이디-닉네",               3,   267),
    ("info/카카오톡-멘션-알림-끄는-3가지-설정-방법과-단톡방-무",               2,   271),
    ("info/갤럭시-에이닷-전화-단축번호-설정-해제-5가지-완벽-가",               2,   277),
    ("info/컴퓨터활용능력-자격증-사본-인쇄하는-4가지-간편한",                  3,   224),
    ("kin/트위터-미디어-오류-해결-7가지-방법-사진과-동영상이",                  2,   210),
    ("info/카카오톡-간편녹음-버튼-설정-해제하는-7가지-방법과",                  5,    95),
    ("info/instagram-account-recommendation-block-guide",                     2,   227),
    ("info/닌텐도-스위치-전원끄기-7가지-방법과-슬립모드-완벽",                  4,   206),
    ("info/아이폰-문자-차단-전화-차단-확인-후-메시지-전송-실패",                4,   168),
    ("info/인스타그램-부계정-만들기-7단계-완벽-가이드와-크리",                  3,    20),
    ("entry/유튜브-다른-계정으로-구독-및-저장정보-백업하는-방법",               4,   136),
    ("kin/인스타-라이브-댓글-멈춤-현상-해결하는-7가지-핵심-방",                14,   176),
    ("info/alipay-korea-payment-fail-7-reasons",                              2,    90),
    ("info/엔비디아-fps-표시-설정하는-5가지-핵심-방법과-게임-성",               2,   101),
    ("info/팟플레이어-ai-자막생성-7가지-설정-방법과-실시간-번역",               3,    84),
    ("info/kakaotalk-team-chat-restriction-ban-analysis",                    10,   263),
    ("excel/엑셀-파일-시트-합치기-10초-완벽-해결법-vba-매크로-코드",            3,    14),
    ("kin/아식스-노바블라스트5-정품-확인하는-7가지-확실한-방",                  43,   343),
]

# ── Hardcoded SEO improvements ───────────────────────────────────────────────
# key = substring(s) that uniquely identifies the slug
# value = (new_title, new_excerpt)
IMPROVEMENTS = {
    "인스타그램-게시물-음악": (
        "인스타그램 게시물 음악 추가·수정·삭제 방법 총정리 (2026)",
        "인스타그램 피드·릴스·스토리에서 음악을 추가하거나 바꾸는 방법 7가지. 이미 올린 게시물 음악 변경도 가능합니다.",
    ),
    "카카오톡-챗봇-추가와-제거": (
        "카카오톡 챗봇 추가·삭제 방법 7단계 완벽 가이드 (2026)",
        "카카오톡 챗봇을 추가하거나 삭제하는 방법을 7단계로 정리했습니다. 채널봇 설정부터 완전 제거까지 한 번에 해결.",
    ),
    "유튜브-쇼츠-노래": (
        "유튜브 쇼츠 노래 찾기 5가지 방법 총정리 (2026 앱 필요 없음)",
        "유튜브 쇼츠에서 나오는 노래를 찾는 5가지 확실한 방법. 앱 없이 바로 음악 제목 확인하는 꿀팁 포함.",
    ),
    "insta-activity-status-error": (
        "인스타그램 활동 상태 오류·안 보임 해결 방법 총정리 (2026)",
        "인스타그램 활동 상태가 보이지 않거나 오류가 발생하는 원인과 해결 방법 총정리. DM 읽음 표시 오류도 포함.",
    ),
    "kakaotalk-google-play-giftcard": (
        "카카오톡 구글 플레이 기프트카드 바코드 교환 방법 (2026)",
        "카카오톡으로 받은 구글 플레이 기프트카드 바코드를 잔액으로 전환하는 방법을 단계별로 설명합니다.",
    ),
    "카카오톡-챗봇-사용법": (
        "카카오톡 챗봇 사용법 완벽 가이드 추가·제거·활용 (2026)",
        "카카오톡 챗봇 추가부터 삭제, 자동응답 활용까지 완벽 정리. 2026년 최신 UI 기준으로 스크린샷과 함께 설명합니다.",
    ),
    "samsung-wallet-tmoney": (
        "삼성 월렛 티머니 추가 안 될 때 오류 해결 방법 (2026)",
        "삼성 월렛에 티머니가 추가되지 않는 오류 원인과 해결 방법. NFC 설정, 앱 초기화, 재설치까지 단계별 정리.",
    ),
    "트위터-x-이름-바꾸기": (
        "트위터(X) 이름·아이디 바꾸기 7단계 완벽 가이드 (2026)",
        "트위터(X)에서 표시 이름과 @아이디를 변경하는 방법을 7단계로 설명합니다. 변경 횟수 제한과 주의사항도 포함.",
    ),
    "카카오톡-멘션-알림": (
        "카카오톡 멘션 알림 끄기 3가지 방법 완벽 가이드 (2026)",
        "카카오톡 단체채팅방에서 @멘션 알림을 끄는 3가지 방법. 특정 채팅방만 알림 끄기, 전체 설정 변경 모두 포함.",
    ),
    "갤럭시-에이닷": (
        "갤럭시 에이닷 전화 단축번호 설정·해제 완벽 가이드 (2026)",
        "갤럭시 에이닷에서 전화 단축번호를 설정하거나 해제하는 5가지 방법. 설정이 안 될 때 해결법도 포함합니다.",
    ),
    "컴퓨터활용능력-자격증": (
        "컴퓨터활용능력 자격증 사본 인쇄 방법 4가지 (2026 최신)",
        "컴퓨터활용능력 자격증 사본을 인쇄하는 4가지 방법을 정리했습니다. Q-Net 온라인 발급부터 방문 발급까지.",
    ),
    "트위터-미디어-오류": (
        "트위터(X) 미디어 오류 해결 7가지 방법 (사진·동영상 안 열릴 때)",
        "트위터 사진·영상이 안 열리거나 '미디어를 불러올 수 없습니다' 오류 해결 방법 7가지를 정리했습니다.",
    ),
    "instagram-account-recommendation-block": (
        "인스타그램 계정 추천 차단 방법 (팔로워 추천 끄기 2026)",
        "인스타그램에서 내 계정이 다른 사람에게 추천되지 않게 하는 방법과 추천 계정 차단하는 방법을 안내합니다.",
    ),
    "닌텐도-스위치-전원끄기": (
        "닌텐도 스위치 전원 끄기 7가지 방법과 슬립모드 차이 (2026)",
        "닌텐도 스위치 전원을 완전히 끄는 방법과 슬립모드 차이를 설명합니다. 배터리 절약을 위한 올바른 전원 관리법.",
    ),
    "kakaotalk-team-chat-restriction": (
        "카카오톡 팀챗 제한·차단 이유와 해결 방법 총정리 (2026)",
        "카카오톡 팀채팅에서 메시지 제한이나 차단이 발생하는 원인과 해결 방법을 분석합니다.",
    ),
    "vrchat-iphone-facial-tracking": (
        "VRChat 아이폰 페이셜 트래킹 설정 방법 완벽 가이드 (2026)",
        "VRChat에서 아이폰으로 얼굴 표정 트래킹을 설정하는 방법을 단계별로 설명합니다. 필요한 앱과 설정까지 총정리.",
    ),
    "ibk-군적금-담보대출": (
        "IBK 군적금 담보대출 신청 안 될 때 7가지 이유와 해결책 (2026)",
        "IBK 군적금 담보대출 신청이 거절되거나 안 되는 7가지 원인과 해결 방법을 정리했습니다. 조건·한도·서류까지.",
    ),
    "카카오페이-상대-기관": (
        "카카오페이 상대 기관 업무 개시 이전 오류 해결 방법 (2026)",
        "카카오페이에서 '상대 기관 업무 개시 이전' 오류가 발생하는 원인과 해결 방법 7가지를 정리했습니다.",
    ),
    "유튜브-프리미엄-남은기간": (
        "유튜브 프리미엄 남은 기간 확인하는 방법 총정리 (2026)",
        "유튜브 프리미엄 남은 기간을 확인하는 방법을 PC·모바일 기준으로 정리했습니다. 구독 해지 방법도 포함.",
    ),
    "goodnotes-font-icon-missing": (
        "굿노트 폰트·아이콘 안 보일 때 해결 방법 총정리 (2026)",
        "굿노트에서 폰트나 아이콘이 사라지거나 표시되지 않을 때 해결하는 방법을 단계별로 안내합니다.",
    ),
    "sudden-attack-mouse-lag": (
        "서든어택 마우스 렉·딜레이 해결 방법 완벽 가이드 (2026)",
        "서든어택에서 마우스 입력 지연(렉) 현상을 해결하는 방법과 최적화 설정을 정리했습니다.",
    ),
    "아이폰-문자-차단": (
        "아이폰 문자·전화 차단 확인 방법 총정리 (2026)",
        "아이폰에서 문자나 전화가 차단됐는지 확인하는 방법과 메시지 전송 실패 원인을 알려드립니다.",
    ),
    "유튜브-다른-계정으로": (
        "유튜브 구독·저장 목록 다른 계정으로 백업하는 방법 (2026)",
        "유튜브 구독 채널과 저장된 재생목록을 다른 계정으로 옮기는 방법을 단계별로 설명합니다.",
    ),
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def _headers(extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    h = {
        "Authorization": f"Basic {AUTH}",
        "Content-Type":  "application/json",
        "Accept":        "application/json",
        "User-Agent":    "devupbox-seo-boost/1.0",
    }
    if extra:
        h.update(extra)
    return h


def _get(url: str) -> Optional[Any]:
    """HTTP GET; returns parsed JSON or None on error."""
    req = urllib.request.Request(url, headers=_headers())
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"    [GET ERROR {e.code}] {url}")
        return None
    except Exception as e:
        print(f"    [GET FAIL] {e}")
        return None


def _post(url: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """HTTP POST (WP uses POST for updates too); returns parsed JSON or None."""
    data = json.dumps(payload).encode()
    req  = urllib.request.Request(url, data=data, headers=_headers(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        print(f"    [POST ERROR {e.code}] {url}")
        print(f"    {body[:300]}")
        return None
    except Exception as e:
        print(f"    [POST FAIL] {e}")
        return None


def _slug_from_path(path: str) -> str:
    """Extract the last path segment (the WP slug) from a GSC URL path."""
    return path.rstrip("/").split("/")[-1]


def _search_keywords_from_slug(slug: str) -> List[str]:
    """
    Extract meaningful search keywords from a Korean/English slug.
    Returns up to 3 tokens usable for WP search.
    """
    parts = slug.split("-")
    # Filter out common filler words and short tokens
    stopwords = {"7가지", "5가지", "3가지", "4가지", "10가지", "방법", "완벽", "가이드",
                 "단계", "설정", "해결", "오류", "추가", "제거", "삭제", "수정",
                 "and", "or", "the", "a", "7", "5", "3", "4", "10"}
    meaningful = [p for p in parts if len(p) >= 2 and p not in stopwords]
    return meaningful[:3]


# ── WP API functions ──────────────────────────────────────────────────────────

def find_post_by_slug(slug_hint: str) -> Optional[Tuple[int, str]]:
    """
    Find a WP post by slug or keyword search.
    Returns (post_id, current_title) or None if not found.

    Strategy:
      1. Try exact slug lookup: GET /posts?slug=<slug>
      2. If slug is truncated (heuristic: ends with common Korean syllable pattern
         or has fewer than 30 chars), fall back to WP search with first 2-3 keywords
    """
    # Step 1: exact slug
    encoded = urllib.parse.quote(slug_hint, safe="")
    url = f"{API}/posts?slug={encoded}&status=publish,draft,private&_fields=id,title,slug"
    result = _get(url)
    if result and len(result) > 0:
        post = result[0]
        return post["id"], post["title"]["rendered"]

    # Step 2: keyword search fallback
    keywords = _search_keywords_from_slug(slug_hint)
    if not keywords:
        return None

    search_term = " ".join(keywords[:2])
    encoded_search = urllib.parse.quote(search_term, safe="")
    url = f"{API}/posts?search={encoded_search}&per_page=5&_fields=id,title,slug"
    results = _get(url)
    if not results:
        return None

    # Pick the best match: prefer slug that shares the most tokens with slug_hint
    hint_tokens = set(slug_hint.split("-"))
    best_id: Optional[int] = None
    best_title: Optional[str] = None
    best_score = 0

    for post in results:
        post_slug   = post.get("slug", "")
        post_tokens = set(post_slug.split("-"))
        score = len(hint_tokens & post_tokens)
        if score > best_score:
            best_score = score
            best_id    = post["id"]
            best_title = post["title"]["rendered"]

    if best_id and best_score >= 2:
        return best_id, best_title

    return None


def update_post_seo(
    post_id: int,
    new_title: str,
    new_excerpt: str,
    try_rankmath: bool = True,
    dry_run: bool = False,
) -> bool:
    """
    Update WP post title, excerpt, and optionally Rank Math meta fields.
    Returns True on success.

    Rank Math stores SEO title/description in post meta:
      - rank_math_title       → SEO title shown in SERP
      - rank_math_description → meta description shown in SERP
    """
    url     = f"{API}/posts/{post_id}"
    payload: Dict[str, Any] = {
        "title":   new_title,
        "excerpt": new_excerpt,
    }

    if try_rankmath:
        payload["meta"] = {
            "rank_math_title":       new_title,
            "rank_math_description": new_excerpt,
        }

    if dry_run:
        return True  # pretend success

    result = _post(url, payload)
    if result is None:
        # Retry without Rank Math meta in case the plugin is not active
        if try_rankmath:
            payload_fallback: Dict[str, Any] = {
                "title":   new_title,
                "excerpt": new_excerpt,
            }
            result = _post(url, payload_fallback)

    return result is not None


# ── SEO improvement lookup ────────────────────────────────────────────────────

def _auto_title(current_title: str, path: str) -> str:
    """
    If no hardcoded improvement exists and the title lacks a year,
    append ' (2026)' as a minimal CTR boost.
    Capped at 58 characters including the year suffix.
    """
    if "(2026)" in current_title or "(2025)" in current_title:
        return current_title
    base = current_title.strip()
    suffix = " (2026)"
    if len(base) + len(suffix) <= 58:
        return base + suffix
    # Truncate base to fit
    return base[: 58 - len(suffix)] + suffix


def _auto_excerpt(current_title: str) -> str:
    """
    Minimal auto-generated excerpt when no hardcoded one exists.
    Uses the title as the core and appends a generic CTA.
    """
    return f"{current_title.strip()} - 방법과 원인을 단계별로 정리했습니다. 지금 바로 확인하세요."


def get_improvement(path: str, current_title: str) -> Tuple[str, str]:
    """
    Look up hardcoded improvements by matching IMPROVEMENTS keys against the slug.
    Falls back to auto-generated title/excerpt if no match.
    Returns (new_title, new_excerpt).
    """
    slug = _slug_from_path(path)

    for key, (new_title, new_excerpt) in IMPROVEMENTS.items():
        if key in slug or key in path:
            return new_title, new_excerpt

    # No hardcoded match — apply automatic improvement
    return _auto_title(current_title, path), _auto_excerpt(current_title)


# ── Priority calculation ──────────────────────────────────────────────────────

def compute_missed_clicks(clicks: int, impressions: int) -> int:
    """Missed clicks = impressions * (1 - CTR) = impressions - clicks."""
    return max(0, impressions - clicks)


def compute_ctr(clicks: int, impressions: int) -> float:
    if impressions == 0:
        return 0.0
    return clicks / impressions * 100


# ── Main ──────────────────────────────────────────────────────────────────────

def build_gsc_records() -> List[Dict[str, Any]]:
    """Convert raw GSC tuples into structured records sorted by missed_clicks desc."""
    records: List[Dict[str, Any]] = []
    for path, clicks, impressions in _RAW_GSC:
        records.append({
            "path":          path,
            "slug":          _slug_from_path(path),
            "clicks":        clicks,
            "impressions":   impressions,
            "ctr":           compute_ctr(clicks, impressions),
            "missed_clicks": compute_missed_clicks(clicks, impressions),
        })
    records.sort(key=lambda r: r["missed_clicks"], reverse=True)
    return records


def print_summary(results: List[Dict[str, Any]]) -> None:
    """Print a formatted summary table of the top processed posts."""
    updated  = [r for r in results if r.get("status") == "updated"]
    skipped  = [r for r in results if r.get("status") == "skipped"]
    failed   = [r for r in results if r.get("status") == "failed"]
    not_found = [r for r in results if r.get("status") == "not_found"]

    print("\n" + "=" * 72)
    print(f"  SEO BOOST SUMMARY  |  Updated: {len(updated)}  Skipped: {len(skipped)}"
          f"  Failed: {len(failed)}  Not Found: {len(not_found)}")
    print("=" * 72)

    # Top 10 by missed clicks
    top10 = sorted(results, key=lambda r: r["missed_clicks"], reverse=True)[:10]
    print(f"\n{'#':<3} {'Status':<10} {'CTR':>6} {'Missed':>7}  {'Slug':<45}")
    print("-" * 72)
    for i, r in enumerate(top10, 1):
        status_icon = {
            "updated":   "✅",
            "skipped":   "⏭️ ",
            "failed":    "❌",
            "not_found": "🔍",
            "dry_run":   "🔍",
        }.get(r.get("status", ""), "?")
        slug_display = r["slug"][:43]
        print(f"{i:<3} {status_icon} {r.get('status','?'):<8} "
              f"{r['ctr']:>5.1f}% {r['missed_clicks']:>7}  {slug_display}")

    print("=" * 72)
    print(f"Total missed clicks across all posts: "
          f"{sum(r['missed_clicks'] for r in results):,}")
    print()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update WordPress post titles/meta for SEO CTR improvement"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing to WordPress",
    )
    parser.add_argument(
        "--slug",
        metavar="SLUG",
        default=None,
        help="Process only the post matching this slug hint",
    )
    return parser.parse_args()


def main() -> None:
    args     = parse_args()
    dry_run  = args.dry_run
    only_slug = args.slug

    records = build_gsc_records()

    if only_slug:
        records = [r for r in records if only_slug in r["slug"] or only_slug in r["path"]]
        if not records:
            print(f"No GSC record matches slug hint: {only_slug}")
            sys.exit(1)

    mode_label = " [DRY RUN]" if dry_run else ""
    print(f"\ndevupbox.com SEO Boost{mode_label} — {len(records)} posts to process")
    print(f"Sorted by missed clicks (impressions - clicks)\n")

    results: List[Dict[str, Any]] = []

    for idx, record in enumerate(records, 1):
        path    = record["path"]
        slug    = record["slug"]
        ctr     = record["ctr"]
        missed  = record["missed_clicks"]
        impr    = record["impressions"]
        clicks  = record["clicks"]

        prefix = f"[{idx}/{len(records)}]"
        print(f"{prefix} CTR {ctr:.1f}% | {impr} impr | {missed} missed | {slug[:50]}")

        # Step 1: find post
        post_info = find_post_by_slug(slug)
        time.sleep(0.3)  # be polite between reads

        if post_info is None:
            print(f"  -> NOT FOUND via slug or search")
            record["status"] = "not_found"
            results.append(record)
            continue

        post_id, current_title = post_info
        print(f"  -> Found post #{post_id}: {current_title[:60]}")

        # Step 2: determine new title/excerpt
        new_title, new_excerpt = get_improvement(path, current_title)

        # Skip if title is identical (already updated previously)
        if new_title == current_title and not dry_run:
            print(f"  -> SKIPPED (title already up to date)")
            record["status"]       = "skipped"
            record["post_id"]      = post_id
            record["current_title"] = current_title
            results.append(record)
            continue

        print(f"  -> New title  : {new_title}")
        print(f"  -> New excerpt: {new_excerpt[:80]}...")

        # Step 3: apply update
        success = update_post_seo(
            post_id,
            new_title,
            new_excerpt,
            try_rankmath=True,
            dry_run=dry_run,
        )

        status = "dry_run" if dry_run else ("updated" if success else "failed")
        icon   = "✅" if status in ("updated", "dry_run") else "❌"
        print(f"  -> {icon} {status.upper()}")

        record["status"]        = status
        record["post_id"]       = post_id
        record["current_title"] = current_title
        record["new_title"]     = new_title
        record["new_excerpt"]   = new_excerpt
        results.append(record)

        # Rate limit: 1 second between write operations
        if not dry_run and success:
            time.sleep(1.0)
        else:
            time.sleep(0.5)

    print_summary(results)


if __name__ == "__main__":
    main()

"""
WordPress 최근 포스트 → Blogger 발행 스크립트
.env.local에서 Google OAuth2 인증 정보를 읽어 Blogger API v3로 발행합니다.
"""
import json
import urllib.request
import urllib.error
import urllib.parse
import ssl
import time
import re
import os

ssl._create_default_https_context = ssl._create_unverified_context

# ========== 설정 ==========
ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env.local")

def load_env(path):
    env = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env

ENV = load_env(ENV_PATH)
GOOGLE_CLIENT_ID = ENV["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = ENV["GOOGLE_CLIENT_SECRET"]
GOOGLE_REFRESH_TOKEN = ENV["GOOGLE_REFRESH_TOKEN"]
BLOGGER_BLOG_URL = ENV["BLOGGER_BLOG_ID"]  # devupbox.blogspot.com

# WordPress
import base64
WP_AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
WP_API = "https://devupbox.com/wp-json/wp/v2/posts"


# ========== Google OAuth2 ==========
def get_access_token():
    """Refresh token으로 access token 발급"""
    data = urllib.parse.urlencode({
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "refresh_token": GOOGLE_REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=15) as resp:
        r = json.loads(resp.read().decode())
    return r["access_token"]


def get_blog_id(access_token):
    """블로그 URL로 numeric blog ID 조회"""
    blog_url = f"https://{BLOGGER_BLOG_URL}"
    api_url = f"https://www.googleapis.com/blogger/v3/blogs/byurl?url={urllib.parse.quote(blog_url, safe='')}"
    req = urllib.request.Request(api_url)
    req.add_header("Authorization", f"Bearer {access_token}")
    with urllib.request.urlopen(req, timeout=15) as resp:
        r = json.loads(resp.read().decode())
    return r["id"]


# ========== WordPress → Blogger 변환 ==========
def clean_wp_content(html):
    """WordPress Gutenberg 블록 주석 제거, Blogger에 맞게 정리"""
    html = re.sub(r'<!-- /?wp:\S+.*?-->\s*', '', html)
    html = re.sub(r'\n{3,}', '\n\n', html)
    return html.strip()


# ========== 태그 자동 추출 ==========
STOP_WORDS = {"2026", "2025", "총정리", "방법", "조건", "BEST", "TOP", "정리", "완벽", "가이드"}

def extract_labels(title):
    """제목에서 Blogger 라벨(태그) 자동 추출"""
    # 숫자, 영문 약어, 특수문자 제거 후 한글 키워드 추출
    clean = re.sub(r'[0-9]+|BEST|TOP|\(.*?\)', '', title)
    tokens = re.split(r'[\s,·/]+', clean)
    labels = []
    for t in tokens:
        t = t.strip()
        if len(t) >= 2 and t not in STOP_WORDS:
            labels.append(t)
    # 중복 제거, 최대 10개
    seen = set()
    unique = []
    for l in labels:
        if l not in seen:
            seen.add(l)
            unique.append(l)
    return unique[:10]


# ========== Blogger 발행 ==========
def publish_to_blogger(access_token, blog_id, title, content, labels=None):
    """Blogger API v3로 포스트 발행"""
    payload = {
        "kind": "blogger#post",
        "blog": {"id": blog_id},
        "title": title,
        "content": content,
    }
    if labels:
        payload["labels"] = labels

    data = json.dumps(payload).encode("utf-8")
    api_url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts"
    req = urllib.request.Request(api_url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(req, timeout=30) as resp:
        r = json.loads(resp.read().decode())
    return r.get("id"), r.get("url", "")


def get_blogger_posts(access_token, blog_id, max_results=50):
    """Blogger 기존 포스트 목록 조회 (제목 → postId 매핑용)"""
    posts = []
    url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts?maxResults={max_results}&fields=items(id,title,labels),nextPageToken"
    while url:
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {access_token}")
        with urllib.request.urlopen(req, timeout=30) as resp:
            r = json.loads(resp.read().decode())
        posts.extend(r.get("items", []))
        npt = r.get("nextPageToken")
        if npt and len(posts) < max_results:
            url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts?maxResults={max_results}&pageToken={npt}&fields=items(id,title,labels),nextPageToken"
        else:
            url = None
    return posts


def update_blogger_labels(access_token, blog_id, post_id, title, labels):
    """기존 Blogger 포스트에 라벨(태그) 추가 (PATCH)"""
    payload = {"labels": labels}
    data = json.dumps(payload).encode("utf-8")
    api_url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/{post_id}"
    req = urllib.request.Request(api_url, data=data, method="PATCH")
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        r = json.loads(resp.read().decode())
    return r.get("labels", [])


# ========== WordPress 포스트 가져오기 ==========
def fetch_wp_posts(count=14, page=1):
    """WordPress REST API에서 최근 포스트 가져오기"""
    url = f"{WP_API}?per_page={count}&page={page}&orderby=date&order=desc&_fields=id,title,content,slug,link"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Basic {WP_AUTH}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def fetch_wp_posts_offset(count=50, offset=0):
    """WordPress REST API에서 offset 기준으로 포스트 가져오기 (최대 100개씩 페이징)"""
    all_posts = []
    per_page = min(count, 100)
    page = (offset // per_page) + 1
    skip = offset % per_page
    remaining = count

    while remaining > 0:
        url = f"{WP_API}?per_page={per_page}&page={page}&orderby=date&order=desc&_fields=id,title,content,slug,link"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Basic {WP_AUTH}")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                posts = json.loads(resp.read().decode())
        except urllib.error.HTTPError:
            break
        if not posts:
            break
        # 첫 페이지에서 skip 처리
        if skip > 0:
            posts = posts[skip:]
            skip = 0
        all_posts.extend(posts[:remaining])
        remaining -= len(posts[:remaining])
        page += 1

    return all_posts


# ========== 메인 ==========
def main():
    import sys
    count = 14
    offset = 0
    # 인자 파싱: publish-to-blogger.py [count] [offset]
    args = [a for a in sys.argv[1:] if a != "tags"]
    if len(args) >= 1:
        count = int(args[0])
    if len(args) >= 2:
        offset = int(args[1])

    print("=" * 60)
    print("WordPress → Blogger 발행")
    print("=" * 60)

    # 1) Access Token 발급
    print("\n[1] Google Access Token 발급...")
    access_token = get_access_token()
    print("  OK")

    # 2) Blog ID 조회
    print("[2] Blog ID 조회...")
    blog_id = get_blog_id(access_token)
    print(f"  Blog ID: {blog_id}")

    # 3) WordPress 포스트 가져오기
    if offset > 0:
        print(f"[3] WordPress 포스트 가져오기 (offset={offset}, count={count})...")
        posts = fetch_wp_posts_offset(count, offset)
    else:
        print(f"[3] WordPress 최근 {count}개 포스트 가져오기...")
        posts = fetch_wp_posts(count)
    posts.reverse()  # 오래된 글부터 발행
    print(f"  {len(posts)}개 포스트 로드 완료")

    # 4) Blogger 발행
    published = []
    for idx, post in enumerate(posts, 1):
        title = post["title"]["rendered"]
        content = clean_wp_content(post["content"]["rendered"])

        labels = extract_labels(title)
        print(f"\n[{idx}/{len(posts)}] {title}")
        print(f"  태그: {labels}")

        # 429 rate limit 대응: 최대 3회 재시도, 대기 시간 증가
        success = False
        for attempt in range(3):
            try:
                bid, burl = publish_to_blogger(access_token, blog_id, title, content, labels=labels)
                print(f"  Blogger OK | ID:{bid}")
                print(f"  URL: {burl}")
                published.append(burl)
                success = True
                break
            except urllib.error.HTTPError as e:
                body = e.read().decode() if e.fp else ""
                if e.code == 429:
                    wait = 30 * (attempt + 1)
                    print(f"  Rate limit! {wait}초 대기 후 재시도 ({attempt+1}/3)...")
                    time.sleep(wait)
                else:
                    print(f"  Blogger FAIL | HTTP {e.code} | {body[:200]}")
                    break
            except Exception as e:
                print(f"  Blogger FAIL | {e}")
                break

        if not success and not published:
            pass  # 이미 에러 출력됨

        time.sleep(5)  # 글 사이 5초 대기 (rate limit 방지)

    print(f"\n{'='*60}")
    print(f"완료! 총 {len(published)}/{len(posts)}개 Blogger 발행")
    print("=" * 60)


def update_tags():
    """기존 Blogger 포스트에 태그(라벨) 일괄 추가"""
    print("=" * 60)
    print("Blogger 기존 포스트 태그 업데이트")
    print("=" * 60)

    print("\n[1] Google Access Token 발급...")
    access_token = get_access_token()
    print("  OK")

    print("[2] Blog ID 조회...")
    blog_id = get_blog_id(access_token)
    print(f"  Blog ID: {blog_id}")

    print("[3] 기존 포스트 목록 조회...")
    posts = get_blogger_posts(access_token, blog_id)
    print(f"  {len(posts)}개 포스트 발견")

    updated = 0
    for idx, post in enumerate(posts, 1):
        title = post["title"]
        existing_labels = post.get("labels", [])
        new_labels = extract_labels(title)

        if not new_labels:
            continue

        # 기존 라벨과 합치기 (중복 제거)
        merged = list(dict.fromkeys(existing_labels + new_labels))

        if set(merged) == set(existing_labels):
            print(f"  [{idx}] 이미 태그 있음: {title[:30]}...")
            continue

        print(f"\n  [{idx}] {title}")
        print(f"    태그: {merged}")
        try:
            result = update_blogger_labels(access_token, blog_id, post["id"], title, merged)
            print(f"    OK -> {result}")
            updated += 1
        except urllib.error.HTTPError as e:
            body = e.read().decode() if e.fp else ""
            if e.code == 429:
                print(f"    Rate limit! 30초 대기...")
                time.sleep(30)
                try:
                    result = update_blogger_labels(access_token, blog_id, post["id"], title, merged)
                    print(f"    OK -> {result}")
                    updated += 1
                except Exception as e2:
                    print(f"    FAIL | {e2}")
            else:
                print(f"    FAIL | HTTP {e.code} | {body[:200]}")
        except Exception as e:
            print(f"    FAIL | {e}")

        time.sleep(3)

    print(f"\n{'='*60}")
    print(f"완료! {updated}개 포스트 태그 업데이트")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "tags":
        update_tags()
    else:
        main()

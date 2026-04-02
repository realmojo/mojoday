import json
import urllib.request
import urllib.error
import urllib.parse
import base64
import time
import ssl
import os
import tempfile
import re

ssl._create_default_https_context = ssl._create_unverified_context

# ========== WordPress 설정 ==========
AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API = "https://devupbox.com/wp-json/wp/v2/posts"
MEDIA_API = "https://devupbox.com/wp-content/uploads/2026/03/"

MEDIA_API_URL = "https://devupbox.com/wp-json/wp/v2/media"

# ========== Blogger 설정 ==========
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
BLOGGER_BLOG_URL = ENV["BLOGGER_BLOG_ID"]

# ========== 이미지 함수 ==========
def download_image(photo_id):
    url = f"https://images.unsplash.com/{photo_id}?w=800&h=450&fit=crop&auto=format&q=80"
    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            tmp.write(resp.read())
        tmp.close()
        return tmp.name
    except Exception as e:
        tmp.close()
        os.unlink(tmp.name)
        print(f"  이미지 다운로드 실패: {e}")
        return None

def upload_image(file_path, filename, alt_text):
    with open(file_path, "rb") as f:
        data = f.read()
    req = urllib.request.Request(MEDIA_API_URL, data=data, method="POST")
    req.add_header("Authorization", f"Basic {AUTH}")
    req.add_header("Content-Type", "image/jpeg")
    req.add_header("Content-Disposition", f'attachment; filename="{filename}.jpg"')
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            r = json.loads(resp.read().decode())
            mid = r.get("id")
            murl = r.get("source_url", "")
            if mid:
                ud = json.dumps({"alt_text": alt_text}).encode()
                ur = urllib.request.Request(f"{MEDIA_API_URL}/{mid}", data=ud, method="POST")
                ur.add_header("Authorization", f"Basic {AUTH}")
                ur.add_header("Content-Type", "application/json")
                try: urllib.request.urlopen(ur, timeout=15)
                except: pass
            return mid, murl
    except Exception as e:
        print(f"  업로드 실패: {e}")
        return None, None

def img_block(url, alt):
    return f'''<!-- wp:image {{"sizeSlug":"large"}} -->
<figure class="wp-block-image size-large"><img src="{url}" alt="{alt}"/><figcaption class="wp-element-caption">{alt}</figcaption></figure>
<!-- /wp:image -->'''

def cta_block(text, desc, url, style="blue"):
    styles = {
        "blue": {"bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5", "border": "none"},
        "yellow": {"bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
        "green": {"bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1", "border": "none"},
    }
    s = styles[style]
    return f'''<div style="background:{s['bg']};border:{s['border']};border-radius:12px;padding:28px 32px;margin:32px 0;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;">
  <div>
    <p style="margin:0 0 6px;font-size:18px;font-weight:700;color:{s['text_color']};">{text}</p>
    <p style="margin:0;font-size:14px;color:{s['desc_color']};">{desc}</p>
  </div>
  <a href="{url}" target="_blank" rel="noopener noreferrer"
     style="background:{s['btn_bg']};color:{s['btn_color']};padding:12px 24px;border-radius:8px;font-weight:700;text-decoration:none;white-space:nowrap;font-size:15px;">
    바로가기 &rarr;
  </a>
</div>'''

# ========== URL 자동 링크 변환 ==========
def auto_link(html):
    """본문 내 URL 텍스트를 자동으로 <a> 태그로 변환 (태그 속성 안 URL은 제외)"""
    # HTML을 태그와 텍스트로 분리하여 텍스트 부분만 처리
    url_re = re.compile(r'(?<![a-zA-Z0-9/])((?:[a-zA-Z0-9-]+\.)+(?:com|co\.kr|or\.kr|go\.kr|kr|net|org)(?:/[^\s<"\')\]]*)?)')
    img_re = re.compile(r'\.(?:jpg|jpeg|png|gif|webp|svg|css|js)(?:\?|$)', re.I)

    def linkify_text(text):
        def replace_url(m):
            url = m.group(1)
            if img_re.search(url):
                return m.group(0)
            return f'<a href="https://{url}" target="_blank" rel="noopener noreferrer">{url}</a>'
        return url_re.sub(replace_url, text)

    # 태그(<...>)와 텍스트를 분리, 텍스트만 변환
    parts = re.split(r'(<[^>]+>)', html)
    result = []
    for part in parts:
        if part.startswith('<'):
            result.append(part)  # 태그는 그대로
        else:
            result.append(linkify_text(part))  # 텍스트만 변환
    return ''.join(result)

# ========== Google OAuth2 ==========
def get_access_token():
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
    blog_url = f"https://{BLOGGER_BLOG_URL}"
    api_url = f"https://www.googleapis.com/blogger/v3/blogs/byurl?url={urllib.parse.quote(blog_url, safe='')}"
    req = urllib.request.Request(api_url)
    req.add_header("Authorization", f"Bearer {access_token}")
    with urllib.request.urlopen(req, timeout=15) as resp:
        r = json.loads(resp.read().decode())
    return r["id"]

def clean_wp_content(html):
    html = re.sub(r'<!-- /?wp:\S+.*?-->\s*', '', html)
    html = re.sub(r'\n{3,}', '\n\n', html)
    return html.strip()

def publish_to_blogger(access_token, blog_id, title, content, labels=None):
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

# ========== 5개 포스트 정의 (IT정보 cat:5) ==========
POSTS = [
    # 6. 공유기 추천 와이파이 설정
    {
        "title": "공유기 추천 와이파이 느릴 때 해결법 공유기 설정 총정리",
        "cat": 5,
        "slug": "wifi-router-recommendation-speed-fix",
        "images": [
            ("photo-1544197150-b99a580bb7a8", "공유기 추천 와이파이 설정"),
            ("photo-1550751827-4bd374c3f58b", "와이파이 속도 최적화"),
            ("photo-1519389950473-47ba0277781c", "인터넷 네트워크 설정"),
        ],
        "labels": ["공유기추천", "와이파이느릴때", "공유기설정", "WiFi6", "메시와이파이", "인터넷속도", "공유기비교", "와이파이속도향상"],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">집에서 인터넷을 쓰는데 유독 와이파이만 느리거나 특정 방에서 신호가 약해 끊기는 경험을 해보셨나요? 문제의 원인은 <strong>공유기 설정, 설치 위치, 채널 간섭</strong> 등 다양합니다. 이 글에서는 와이파이가 느린 원인 5가지부터 <strong>공유기 추천 TOP 5</strong>, WiFi 6 비교, 최적 설치 위치, 채널 변경, DNS 설정까지 한 번에 정리합니다.</p>

{imgs[0]}

<h2>와이파이가 느린 원인 5가지</h2>
<p>속도 문제를 해결하려면 먼저 원인을 파악해야 합니다. 흔한 원인 다섯 가지를 살펴보겠습니다.</p>
<ol>
<li><strong>공유기 위치 문제</strong>: 벽, 가구, 전자기기 사이에 공유기가 가려지면 신호가 크게 약해집니다. 공유기는 집 중앙 높은 곳에 두는 것이 기본입니다.</li>
<li><strong>채널 간섭</strong>: 아파트처럼 이웃이 많은 환경에서는 같은 채널을 여러 공유기가 사용해 간섭이 발생합니다. 채널을 수동으로 바꾸면 해결되는 경우가 많습니다.</li>
<li><strong>공유기 노후화</strong>: 5년 이상 된 공유기는 칩셋 성능 자체가 낮아 최신 인터넷 속도를 따라가지 못합니다.</li>
<li><strong>2.4GHz 대역 과부하</strong>: 스마트폰, TV, 가전이 모두 2.4GHz에 몰리면 속도가 나눠집니다. 5GHz 대역으로 기기를 분산하세요.</li>
<li><strong>펌웨어 미업데이트</strong>: 공유기 펌웨어가 오래되면 보안 취약점과 성능 저하가 발생합니다. 관리자 페이지에서 최신 펌웨어로 업데이트하세요.</li>
</ol>

{cta_block("내 인터넷 속도 바로 측정하기", "Speedtest.net에서 현재 와이파이 속도를 무료로 확인하세요", "https://www.speedtest.net/", "blue")}

<h2>공유기 추천 TOP 5 비교표</h2>
<p>국내에서 가장 많이 사용하는 공유기 브랜드 5종을 가격, 속도, 커버리지 기준으로 비교했습니다.</p>
<table><thead><tr><th>브랜드/모델</th><th>가격대</th><th>최대 속도</th><th>커버리지</th><th>특징</th></tr></thead><tbody>
<tr><td>ipTIME AX3000</td><td>5~7만원</td><td>WiFi 6 / 3Gbps</td><td>중형 아파트</td><td>국내 1위 AS, 한글 UI 편리</td></tr>
<tr><td>ASUS RT-AX88U</td><td>20~25만원</td><td>WiFi 6 / 6Gbps</td><td>대형 주택</td><td>게임·스트리밍 최적화, AI 보호</td></tr>
<tr><td>TP-Link Archer AX73</td><td>10~13만원</td><td>WiFi 6 / 5.4Gbps</td><td>중대형 아파트</td><td>가성비 우수, 6안테나 구성</td></tr>
<tr><td>넷기어 RAX50</td><td>15~18만원</td><td>WiFi 6 / 5.4Gbps</td><td>중대형 주택</td><td>업무용 안정성, NETGEAR Armor</td></tr>
<tr><td>삼성 SmartThings Hub</td><td>8~12만원</td><td>WiFi 5 / 1.7Gbps</td><td>중형 아파트</td><td>SmartThings 연동, IoT 특화</td></tr>
</tbody></table>
<p>가성비를 원하면 <strong>ipTIME AX3000</strong>, 고성능이 필요하면 <strong>ASUS RT-AX88U</strong>, 중간 선택은 <strong>TP-Link Archer AX73</strong>을 추천합니다.</p>

{imgs[1]}

<h2>WiFi 6 vs WiFi 6E 차이점</h2>
<p>요즘 공유기 박스에 WiFi 6, WiFi 6E라는 표기가 많은데, 어떤 차이가 있을까요?</p>
<table><thead><tr><th>구분</th><th>WiFi 5 (802.11ac)</th><th>WiFi 6 (802.11ax)</th><th>WiFi 6E</th></tr></thead><tbody>
<tr><td>주파수 대역</td><td>2.4 / 5GHz</td><td>2.4 / 5GHz</td><td>2.4 / 5 / 6GHz</td></tr>
<tr><td>최대 속도</td><td>3.5Gbps</td><td>9.6Gbps</td><td>9.6Gbps+</td></tr>
<tr><td>간섭 감소</td><td>보통</td><td>우수 (OFDMA)</td><td>매우 우수</td></tr>
<tr><td>혼잡 환경 성능</td><td>낮음</td><td>높음</td><td>최고</td></tr>
<tr><td>가격대</td><td>3~10만원</td><td>7~25만원</td><td>25만원~</td></tr>
</tbody></table>
<p>아파트 같은 혼잡한 환경이라면 <strong>WiFi 6</strong>만으로도 체감 속도가 크게 향상됩니다. WiFi 6E는 6GHz 대역을 추가 지원하지만 현재 지원 단말이 제한적입니다.</p>

<h2>공유기 최적 설치 위치 & 채널 설정법</h2>
<h3>설치 위치 황금 규칙</h3>
<ul>
<li><strong>집 중앙</strong>에 설치 — 신호가 사방으로 퍼집니다</li>
<li><strong>높은 곳</strong>에 배치 — 책상 위보다 선반, TV장 위가 유리합니다</li>
<li><strong>벽과 거리 두기</strong> — 콘크리트 벽은 신호를 30~50% 감쇠시킵니다</li>
<li><strong>전자레인지, 무선전화기와 멀리</strong> — 2.4GHz 간섭 원인</li>
<li><strong>수직 안테나 배치</strong> — 안테나를 세우면 수평 방향 커버리지 증가</li>
</ul>
<h3>채널 수동 설정법 (ipTIME 기준)</h3>
<ol>
<li>브라우저에서 <strong>192.168.0.1</strong> 접속 → 관리자 로그인</li>
<li>고급 설정 → 무선 설정/보안 → 무선 채널 선택</li>
<li>2.4GHz: 1, 6, 11 채널 중 이웃이 안 쓰는 채널로 변경</li>
<li>5GHz: 36, 40, 44, 48 채널 중 선택 (DFS 채널은 피하세요)</li>
<li>저장 후 재시작</li>
</ol>

<h2>메시 와이파이 & DNS 변경으로 속도 높이기</h2>
<h3>메시 와이파이란?</h3>
<p>메시(Mesh) 와이파이는 여러 대의 공유기를 하나의 네트워크로 묶어 <strong>넓은 공간에서도 끊김 없이</strong> 연결되는 시스템입니다. 복층 주택이나 방이 많은 아파트에서 효과적입니다.</p>
<ul>
<li><strong>ipTIME Mesh</strong>: 기존 ipTIME 공유기끼리 메시 구성 가능</li>
<li><strong>TP-Link Deco</strong>: 국내 가장 인기 있는 메시 시스템 (Deco M4, XE75 등)</li>
<li><strong>ASUS ZenWiFi</strong>: 고성능 게이밍 메시, WiFi 6E 지원</li>
<li><strong>넷기어 Orbi</strong>: 기업급 안정성, 트라이밴드 구성</li>
</ul>
<h3>DNS 변경으로 속도 개선</h3>
<p>ISP(통신사) 기본 DNS 대신 빠른 공개 DNS로 변경하면 웹사이트 로딩이 빨라집니다.</p>
<table><thead><tr><th>DNS 서비스</th><th>기본 DNS</th><th>보조 DNS</th><th>특징</th></tr></thead><tbody>
<tr><td>Google DNS</td><td>8.8.8.8</td><td>8.8.4.4</td><td>빠른 응답, 글로벌 안정성</td></tr>
<tr><td>Cloudflare</td><td>1.1.1.1</td><td>1.0.0.1</td><td>최고 속도, 프라이버시 보호</td></tr>
<tr><td>KT DNS</td><td>168.126.63.1</td><td>168.126.63.2</td><td>국내 서비스 최적화</td></tr>
</tbody></table>
<p>DNS 변경은 공유기 관리자 페이지 → 인터넷 설정 → DNS 서버 항목에서 바꾸면 연결된 모든 기기에 자동 적용됩니다.</p>

{imgs[2]}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 공유기를 재시작하면 속도가 빨라지는 이유가 뭔가요?</h3>
<p>A. 공유기도 컴퓨터처럼 메모리를 사용합니다. 장시간 운영하면 <strong>메모리 누수</strong>가 발생해 처리 속도가 느려집니다. 재시작하면 메모리가 초기화되어 속도가 회복됩니다. 한 달에 한 번 정도 재시작하는 것을 권장합니다.</p>
<h3>Q. 5GHz가 빠른데 왜 2.4GHz도 필요한가요?</h3>
<p>A. 5GHz는 속도가 빠르지만 <strong>벽 투과율이 낮아 거리가 멀어지면 신호가 급격히 약해집니다</strong>. 2.4GHz는 느리지만 커버리지가 넓습니다. 스마트폰, 노트북은 5GHz, 스마트 TV나 먼 방 기기는 2.4GHz를 권장합니다.</p>
<h3>Q. 이웃집 와이파이 채널과 같으면 실제로 느려지나요?</h3>
<p>A. 네, 특히 <strong>2.4GHz 대역에서 채널 간섭이 심하면</strong> 속도가 30~50%까지 떨어질 수 있습니다. Wi-Fi Analyzer 앱(안드로이드)으로 주변 채널 현황을 확인하고 가장 덜 혼잡한 채널로 변경하세요.</p>
<h3>Q. 공유기 비밀번호를 바꾸면 속도에 영향이 있나요?</h3>
<p>A. 비밀번호 자체는 속도에 영향을 주지 않지만, <strong>WPA3 또는 WPA2 암호화 방식</strong>을 사용하는 것이 중요합니다. WEP 방식은 보안이 취약하고 성능도 낮으니 반드시 WPA2/WPA3으로 설정하세요.</p>

{cta_block("스피드테스트로 와이파이 속도 확인", "설정 변경 전후 속도를 비교해 개선 효과를 직접 확인하세요", "https://www.speedtest.net/", "green")}

<h2>마무리</h2>
<p>와이파이 속도 문제는 공유기 교체 없이도 <strong>위치 변경, 채널 설정, DNS 변경</strong>만으로도 크게 개선할 수 있습니다. 그래도 해결되지 않는다면 WiFi 6 지원 공유기로 교체하는 것이 장기적으로 유리합니다. 오늘 소개한 방법들을 순서대로 적용해보고 스피드테스트(speedtest.net)로 전후 속도를 비교해보세요.</p>'''
    },

    # 7. 무료 영상편집 프로그램 추천
    {
        "title": "무료 영상편집 프로그램 추천 캡컷 다빈치리졸브 비교 총정리",
        "cat": 5,
        "slug": "free-video-editing-software-capcut-davinci",
        "images": [
            ("photo-1574717024653-61fd2cf4d44d", "무료 영상편집 프로그램"),
            ("photo-1517694712202-14dd9538aa97", "영상편집 작업 화면"),
            ("photo-1531297484001-80022131f5a1", "동영상 편집 툴"),
        ],
        "labels": ["무료영상편집", "캡컷", "다빈치리졸브", "Shotcut", "영상편집추천", "유튜브편집", "숏폼편집", "무료동영상편집"],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">유튜브를 시작하고 싶은데 영상편집 프로그램 비용이 부담스럽다면? 걱정하지 마세요. 지금은 <strong>무료로 사용할 수 있는 고품질 영상편집 프로그램</strong>이 많습니다. 캡컷, 다빈치리졸브부터 Shotcut, OpenShot까지 무료 영상편집 TOP 5를 기능, 난이도, 워터마크, 지원 해상도 기준으로 상세 비교합니다.</p>

{imgs[0]}

<h2>무료 영상편집 프로그램 TOP 5 비교표</h2>
<table><thead><tr><th>프로그램</th><th>운영체제</th><th>난이도</th><th>워터마크</th><th>최대 해상도</th><th>추천 용도</th></tr></thead><tbody>
<tr><td>캡컷 (CapCut)</td><td>Win/Mac/모바일</td><td>매우 쉬움</td><td>없음 (PC)</td><td>4K</td><td>숏폼, SNS, 입문자</td></tr>
<tr><td>다빈치리졸브</td><td>Win/Mac/Linux</td><td>어려움</td><td>없음</td><td>8K+</td><td>유튜브, 전문가</td></tr>
<tr><td>Shotcut</td><td>Win/Mac/Linux</td><td>보통</td><td>없음</td><td>4K</td><td>PC 영상편집, 자막</td></tr>
<tr><td>OpenShot</td><td>Win/Mac/Linux</td><td>쉬움</td><td>없음</td><td>4K</td><td>간단한 편집, 입문</td></tr>
<tr><td>VSDC Free</td><td>Windows 전용</td><td>보통</td><td>없음 (무료)</td><td>4K</td><td>윈도우 사용자, 효과</td></tr>
</tbody></table>

<h2>캡컷 (CapCut) — 숏폼 최강자</h2>
<p>ByteDance(틱톡 모회사)에서 만든 캡컷은 현재 <strong>가장 빠르게 성장 중인 무료 영상편집 앱</strong>입니다.</p>
<h3>주요 기능</h3>
<ul>
<li><strong>자동 자막</strong>: 음성 인식으로 자동 자막 생성 (한국어 지원)</li>
<li><strong>AI 기능</strong>: 배경 제거, AI 보정, 스타일 변환</li>
<li><strong>템플릿</strong>: 수천 개의 트렌디한 템플릿 무료 제공</li>
<li><strong>모바일/PC 연동</strong>: 모바일에서 편집 후 PC에서 이어서 작업 가능</li>
</ul>
<h3>장단점</h3>
<table><thead><tr><th>장점</th><th>단점</th></tr></thead><tbody>
<tr><td>직관적인 UI, 빠른 학습 곡선</td><td>PC 버전 일부 유료 기능 있음</td></tr>
<tr><td>AI 자막, 배경 제거 등 최신 기능</td><td>개인정보 보안 우려 (중국 기업)</td></tr>
<tr><td>틱톡/릴스/쇼츠 최적화</td><td>복잡한 편집에는 기능 부족</td></tr>
</tbody></table>

{cta_block("캡컷 무료 다운로드", "PC/모바일 모두 무료로 사용 가능한 캡컷을 지금 시작하세요", "https://www.capcut.com/", "blue")}

{imgs[1]}

<h2>다빈치리졸브 — 전문가급 무료 편집툴</h2>
<p>블랙매직디자인의 다빈치리졸브는 할리우드 영화에도 사용되는 <strong>프로급 영상편집 소프트웨어</strong>입니다. 무료 버전만으로도 대부분의 기능을 사용할 수 있습니다.</p>
<h3>주요 기능</h3>
<ul>
<li><strong>컬러 그레이딩</strong>: 업계 최고 수준의 색보정 기능</li>
<li><strong>Fusion</strong>: 합성 및 VFX 효과 (Adobe After Effects 대체)</li>
<li><strong>Fairlight</strong>: 전문 오디오 믹싱 및 마스터링</li>
<li><strong>Cut 페이지</strong>: 빠른 편집을 위한 간소화 인터페이스</li>
<li><strong>협업 기능</strong>: 팀원과 동시 편집 가능</li>
</ul>
<h3>장단점</h3>
<table><thead><tr><th>장점</th><th>단점</th></tr></thead><tbody>
<tr><td>프리미어 프로 수준의 전문 기능</td><td>처음에는 UI가 복잡하고 학습 시간 필요</td></tr>
<tr><td>색보정 분야 업계 표준</td><td>고사양 PC가 필요 (RAM 16GB 권장)</td></tr>
<tr><td>무료 버전으로도 거의 모든 기능 사용</td><td>한국어 자막 자동 생성 기능 없음</td></tr>
</tbody></table>

{cta_block("다빈치리졸브 무료 다운로드", "전문가급 영상편집을 무료로 시작하세요", "https://www.blackmagicdesign.com/", "green")}

<h2>Shotcut — 오픈소스 PC 편집기</h2>
<p>Shotcut은 오픈소스 기반의 무료 영상편집 프로그램으로, <strong>윈도우, 맥, 리눅스</strong>를 모두 지원합니다.</p>
<ul>
<li>500개 이상의 효과 필터 무료 제공</li>
<li>타임라인 기반 편집, 멀티트랙 지원</li>
<li>4K 영상 편집 가능, 워터마크 없음</li>
<li>다양한 코덱 포맷 지원 (MP4, MOV, AVI 등)</li>
</ul>

<h2>OpenShot — 입문자 친화 편집기</h2>
<p>OpenShot은 직관적인 드래그&드롭 방식으로 <strong>처음 영상편집을 시작하는 분</strong>에게 최적화되어 있습니다.</p>
<ul>
<li>한국어 UI 지원</li>
<li>드래그&드롭으로 쉬운 편집</li>
<li>기본 자막, 전환 효과, 애니메이션 지원</li>
<li>무거운 프로젝트에서 렌더링이 느린 편</li>
</ul>

{imgs[2]}

<h2>용도별 추천 정리</h2>
<table><thead><tr><th>상황</th><th>추천 프로그램</th><th>이유</th></tr></thead><tbody>
<tr><td>처음 시작하는 입문자</td><td>캡컷 또는 OpenShot</td><td>직관적 UI, 빠른 학습</td></tr>
<tr><td>유튜브 롱폼 콘텐츠</td><td>다빈치리졸브</td><td>전문 편집, 색보정, 안정성</td></tr>
<tr><td>틱톡/릴스/쇼츠 숏폼</td><td>캡컷 모바일</td><td>템플릿, 자동 자막, 트렌드 반영</td></tr>
<tr><td>윈도우 PC 중급 편집</td><td>Shotcut 또는 VSDC</td><td>다양한 효과, 무워터마크</td></tr>
<tr><td>색보정·VFX 전문 작업</td><td>다빈치리졸브</td><td>업계 표준 컬러 그레이딩</td></tr>
</tbody></table>

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 캡컷 PC 버전에서도 워터마크가 없나요?</h3>
<p>A. 네, <strong>PC 버전 캡컷은 기본적으로 워터마크가 없습니다</strong>. 다만 일부 프리미엄 템플릿이나 효과를 사용하면 캡컷 로고가 붙을 수 있으니, 무료 에셋만 사용하면 워터마크 없이 출력할 수 있습니다.</p>
<h3>Q. 다빈치리졸브를 배우려면 얼마나 걸리나요?</h3>
<p>A. 기본 컷편집, 자막, 색보정 기초는 <strong>하루 이틀이면 습득</strong> 가능합니다. Fusion(합성), Fairlight(오디오) 등 전문 기능까지 마스터하려면 수개월이 필요하지만, 일반 유튜브 영상은 기초만으로도 충분합니다.</p>
<h3>Q. 맥북에서 쓸 수 있는 무료 편집기는 무엇인가요?</h3>
<p>A. 맥북에는 애플이 기본 제공하는 <strong>iMovie</strong>가 있어 간단한 편집에 충분합니다. 더 전문적인 작업은 다빈치리졸브 또는 캡컷 Mac 버전을 추천합니다.</p>
<h3>Q. 4K 영상 편집 시 컴퓨터 사양은 어떻게 되어야 하나요?</h3>
<p>A. 4K 편집을 위한 최소 권장 사양은 <strong>CPU: Intel i5/Ryzen 5 이상, RAM: 16GB, GPU: GTX 1060 이상, SSD 필수</strong>입니다. 다빈치리졸브는 GPU 가속을 적극 활용하므로 그래픽카드가 중요합니다.</p>

{cta_block("다빈치리졸브 공식 사이트에서 무료 다운로드", "스튜디오 버전(유료) 없이도 무료 버전으로 전문 편집 가능합니다", "https://www.blackmagicdesign.com/", "yellow")}

<h2>마무리</h2>
<p>무료 영상편집 프로그램은 이미 유료 프로그램 못지않은 수준까지 발전했습니다. <strong>숏폼은 캡컷, 유튜브 전문 편집은 다빈치리졸브</strong>를 기본 조합으로 시작해보세요. 처음에는 캡컷으로 편집 감각을 익히고, 점차 다빈치리졸브로 실력을 키우는 것을 추천합니다.</p>'''
    },

    # 8. 스마트폰 저장공간 부족 해결법
    {
        "title": "스마트폰 저장공간 부족 해결법 용량 확보 꿀팁 총정리",
        "cat": 5,
        "slug": "smartphone-storage-full-fix-tips",
        "images": [
            ("photo-1530319067432-f2a729c03db5", "스마트폰 저장공간 부족"),
            ("photo-1512941937669-90a1b58e7e9c", "휴대폰 용량 정리"),
            ("photo-1519389950473-47ba0277781c", "클라우드 백업 활용"),
        ],
        "labels": ["스마트폰저장공간", "핸드폰용량부족", "아이폰용량", "안드로이드용량", "카카오톡캐시", "구글포토", "iCloud", "스마트폰정리"],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">스마트폰 저장공간이 꽉 찼다는 알림이 뜨면 사진도 안 찍히고, 앱 업데이트도 안 되고, 심지어 카카오톡 파일도 못 받습니다. 이 글에서는 <strong>아이폰과 안드로이드 용량을 각각 7가지 방법으로 확보하는 꿀팁</strong>과 카카오톡 캐시 삭제, 구글포토·iCloud 활용법, 마이크로SD 사용법까지 총정리합니다.</p>

{imgs[0]}

<h2>스마트폰 용량을 잡아먹는 주범 4가지</h2>
<table><thead><tr><th>원인</th><th>일반적인 용량</th><th>해결 방법</th></tr></thead><tbody>
<tr><td>사진·동영상</td><td>10~30GB</td><td>클라우드 백업 후 삭제</td></tr>
<tr><td>앱 캐시</td><td>3~10GB</td><td>캐시 주기적 삭제</td></tr>
<tr><td>카카오톡 파일/사진</td><td>2~8GB</td><td>카톡 저장소 정리</td></tr>
<tr><td>사용 안 하는 앱</td><td>1~5GB</td><td>미사용 앱 삭제</td></tr>
</tbody></table>

<h2>아이폰 용량 확보법 7가지</h2>
<ol>
<li><strong>iCloud 사진 보관함 활성화</strong>: 설정 → Apple ID → iCloud → 사진 → iCloud 사진 켜기. 원본은 클라우드에 저장되고 기기에는 최적화된 버전만 남습니다.</li>
<li><strong>사용 안 하는 앱 자동 삭제 (오프로드)</strong>: 설정 → 일반 → iPhone 저장 공간 → 사용하지 않는 앱 자동 오프로드 켜기. 앱 데이터는 유지하면서 앱 파일만 삭제합니다.</li>
<li><strong>메시지 오래된 것 자동 삭제</strong>: 설정 → 메시지 → 메시지 보관 → 30일 또는 1년 선택. 오래된 메시지와 첨부파일이 자동 삭제됩니다.</li>
<li><strong>사진 중복 삭제</strong>: 사진 앱 → 앨범 → 중복 항목. iOS 16 이상에서 중복 사진을 자동 감지해 한 번에 삭제할 수 있습니다.</li>
<li><strong>HEIF 포맷 유지</strong>: 설정 → 카메라 → 포맷 → 높은 호환성 대신 고효율 선택. HEIF 형식은 JPG 대비 50% 용량 절약.</li>
<li><strong>팟캐스트·음악 다운로드 삭제</strong>: 오프라인 저장한 팟캐스트나 음악 파일이 용량을 차지합니다. 스트리밍으로 전환하세요.</li>
<li><strong>Safari 캐시 삭제</strong>: 설정 → Safari → 방문 기록 및 웹 사이트 데이터 지우기.</li>
</ol>

{cta_block("구글포토로 사진 무제한 백업하기", "스마트폰 사진을 클라우드에 안전하게 보관하고 용량을 확보하세요", "https://photos.google.com/", "blue")}

{imgs[1]}

<h2>안드로이드 용량 확보법 7가지</h2>
<ol>
<li><strong>구글포토 백업 후 기기에서 삭제</strong>: 구글포토 → 보관 공간 관리 → 기기 파일 삭제. 백업된 사진을 기기에서 지웁니다.</li>
<li><strong>앱 캐시 일괄 삭제</strong>: 설정 → 배터리 및 디바이스 케어 → 저장공간 → 정리. 삼성 기기는 디바이스 케어에서 한 번에 캐시 정리 가능.</li>
<li><strong>다운로드 폴더 정리</strong>: 파일 관리자 → 다운로드. 오래된 APK 파일, PDF, 영상 파일이 쌓여있습니다.</li>
<li><strong>마이크로SD 카드 활용</strong>: 삼성, LG 등 SD카드 슬롯 지원 기기는 128GB SD카드(약 1~2만원)로 용량을 크게 늘릴 수 있습니다.</li>
<li><strong>앱 이동 (SD카드로)</strong>: 설정 → 앱 → 해당 앱 → 저장공간 → SD카드로 이동. 일부 앱은 SD카드로 이동 가능합니다.</li>
<li><strong>인스타그램·유튜브 캐시 삭제</strong>: 설정 → 앱 → 인스타그램 → 저장공간 → 캐시 삭제. SNS 앱은 캐시가 수 GB씩 쌓입니다.</li>
<li><strong>WhatsApp·텔레그램 미디어 정리</strong>: 자동 저장된 사진·영상이 갤러리와 별도로 저장됩니다. 파일 관리자에서 DCIM 외 WhatsApp, Telegram 폴더를 정리하세요.</li>
</ol>

<h2>카카오톡 캐시 삭제 방법 (iOS/안드로이드 공통)</h2>
<p>카카오톡은 받은 사진, 동영상, 파일이 자동으로 저장되어 용량을 크게 차지합니다.</p>
<h3>단계별 삭제 방법</h3>
<ol>
<li>카카오톡 실행 → 우측 하단 <strong>더보기(⋯)</strong> 탭</li>
<li>설정(톱니바퀴) → <strong>개인정보 보호</strong></li>
<li><strong>캐시 데이터 삭제</strong> 탭 → 삭제 확인</li>
<li>추가로: 채팅방별로 들어가서 <strong>사진·동영상·파일 탭</strong>에서 불필요한 파일 선택 삭제</li>
</ol>
<p>카카오톡 캐시만 지워도 보통 <strong>1~3GB</strong> 용량이 확보됩니다.</p>

<h2>구글포토 vs iCloud 활용 비교</h2>
<table><thead><tr><th>서비스</th><th>무료 용량</th><th>추가 용량 요금</th><th>추천 대상</th></tr></thead><tbody>
<tr><td>구글포토</td><td>15GB (구글 계정 공유)</td><td>100GB: 월 2,900원</td><td>안드로이드 사용자, 무료 활용</td></tr>
<tr><td>iCloud</td><td>5GB</td><td>50GB: 월 1,100원</td><td>아이폰 사용자, 에코시스템 활용</td></tr>
<tr><td>네이버 MYBOX</td><td>30GB</td><td>100GB: 월 1,000원</td><td>국내 서비스 선호, 네이버 연동</td></tr>
</tbody></table>

{imgs[2]}

<h2>앱별 용량 확인법</h2>
<h3>아이폰</h3>
<p>설정 → 일반 → iPhone 저장 공간 → 앱 목록에서 용량 순으로 정렬 확인 가능</p>
<h3>안드로이드 (삼성 기준)</h3>
<p>설정 → 배터리 및 디바이스 케어 → 저장공간 → 앱별 용량 확인</p>

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 공장초기화 말고 방법이 없나요?</h3>
<p>A. 공장초기화는 최후의 수단입니다. 위에서 소개한 방법들을 순서대로 적용하면 대부분 <strong>10GB 이상의 용량을 확보</strong>할 수 있습니다. 특히 구글포토 백업 후 사진 삭제, 카카오톡 캐시 삭제만 해도 체감 효과가 큽니다.</p>
<h3>Q. 아이폰은 마이크로SD를 쓸 수 없나요?</h3>
<p>A. 네, <strong>아이폰은 마이크로SD 슬롯이 없습니다</strong>. 대신 iCloud 또는 외장 드라이브(Lightning/USB-C 연결형)를 활용할 수 있습니다.</p>
<h3>Q. 사진을 구글포토에 올리면 화질이 떨어지나요?</h3>
<p>A. 구글포토는 현재 <strong>원본 화질 그대로 저장</strong>됩니다. 다만 무료 15GB 한도를 초과하면 추가 요금이 발생하니 용량 관리가 필요합니다.</p>
<h3>Q. 앱 캐시를 지우면 로그인이 풀리나요?</h3>
<p>A. 캐시는 임시 데이터이므로 <strong>로그인 정보에는 영향이 없습니다</strong>. 단, 앱 데이터(데이터 삭제)를 지우면 로그인이 풀리므로 캐시와 데이터를 구분해서 삭제하세요.</p>

{cta_block("구글포토 시작하기", "15GB 무료 저장공간으로 스마트폰 사진을 안전하게 백업하세요", "https://photos.google.com/", "green")}

<h2>마무리</h2>
<p>스마트폰 저장공간 부족 문제는 <strong>구글포토/iCloud 백업 → 카카오톡 캐시 삭제 → 미사용 앱 제거</strong> 순으로 해결하면 대부분 해결됩니다. 한 번 정리하고 끝내지 말고, 한 달에 한 번 정기적으로 점검하는 습관을 들이면 용량 부족으로 고생하지 않을 수 있습니다.</p>'''
    },

    # 9. 노트북 발열 해결법
    {
        "title": "노트북 발열 해결법 쿨링 방법 서멀구리스 교체 총정리",
        "cat": 5,
        "slug": "laptop-overheating-fix-cooling-guide",
        "images": [
            ("photo-1593642702821-c8da6771f0c6", "노트북 발열 해결"),
            ("photo-1550751827-4bd374c3f58b", "노트북 쿨링패드"),
            ("photo-1531297484001-80022131f5a1", "노트북 내부 청소"),
        ],
        "labels": ["노트북발열", "노트북쿨링", "서멀구리스교체", "쿨링패드추천", "노트북뜨거울때", "노트북팬소음", "발열해결법", "노트북수명"],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">노트북을 사용하다 보면 바닥이 뜨거워지고 팬 소리가 시끄러워지는 경험을 하게 됩니다. 발열이 심하면 <strong>성능 저하(쓰로틀링), 배터리 수명 단축, 심하면 부품 손상</strong>까지 이어질 수 있습니다. 이 글에서는 노트북 발열 원인 분석부터 소프트웨어·하드웨어 해결법, 쿨링패드 추천, 서멀구리스 교체 방법까지 완벽하게 정리합니다.</p>

{imgs[0]}

<h2>노트북 발열의 주요 원인 4가지</h2>
<table><thead><tr><th>원인</th><th>설명</th><th>해결 방향</th></tr></thead><tbody>
<tr><td>내부 먼지 쌓임</td><td>팬과 방열판에 먼지가 쌓여 열 배출 막힘</td><td>내부 청소 (에어스프레이)</td></tr>
<tr><td>서멀구리스 노화</td><td>CPU/GPU와 방열판 사이 구리스 굳어서 열전달 저하</td><td>서멀구리스 교체</td></tr>
<tr><td>높은 CPU/GPU 사용률</td><td>백그라운드 앱, 악성코드 등으로 프로세서 과부하</td><td>작업관리자 확인 후 종료</td></tr>
<tr><td>환기구 막힘</td><td>침대·쿠션 위에서 사용 시 흡기/배기구 막힘</td><td>평평한 곳에서 사용, 쿨링패드</td></tr>
</tbody></table>

<h2>소프트웨어 해결법</h2>
<h3>1. 전원 관리 설정 변경</h3>
<p>윈도우의 전원 설정이 고성능으로 되어 있으면 CPU가 항상 최고 속도로 돌아 발열이 심해집니다.</p>
<ul>
<li>윈도우: 설정 → 시스템 → 전원 및 배터리 → <strong>균형 조정(권장)</strong> 선택</li>
<li>게임이나 고성능 작업 후에는 다시 균형으로 돌려놓는 습관을 들이세요</li>
<li>최대 프로세서 상태: 제어판 → 전원 옵션 → 고급 설정 → 프로세서 전원 관리 → <strong>최대 프로세서 상태를 80~90%</strong>로 설정</li>
</ul>
<h3>2. 백그라운드 앱 정리</h3>
<ul>
<li>작업 관리자(Ctrl+Shift+Esc) → CPU/메모리 사용률 높은 프로세스 확인</li>
<li>불필요한 시작 프로그램 제거: 작업 관리자 → 시작 프로그램 탭</li>
<li>Chrome은 탭이 많을수록 CPU를 많이 씁니다. 불필요한 탭을 닫으세요</li>
</ul>
<h3>3. 팬 속도 수동 제어</h3>
<ul>
<li><strong>HWMonitor</strong>: CPU/GPU 온도와 팬 속도 실시간 모니터링 (무료)</li>
<li><strong>SpeedFan</strong>: 팬 속도를 수동으로 조절 가능</li>
<li><strong>ThrottleStop</strong>: 인텔 CPU 언더볼팅으로 발열 감소 (고급 사용자)</li>
<li>삼성 노트북은 삼성 Settings 앱에서 성능 모드 조절 가능</li>
</ul>

{cta_block("쿠팡에서 노트북 쿨링패드 최저가 보기", "다양한 쿨링패드 중 내 노트북 크기에 맞는 제품을 찾아보세요", "https://www.coupang.com/", "blue")}

{imgs[1]}

<h2>쿨링패드 추천 TOP 3 비교표</h2>
<table><thead><tr><th>제품</th><th>팬 수/RPM</th><th>크기 지원</th><th>가격대</th><th>특징</th></tr></thead><tbody>
<tr><td>Havit HV-F2056</td><td>3팬 / 1000RPM</td><td>15.6인치</td><td>2~3만원</td><td>조용한 쿨링, USB 허브 내장</td></tr>
<tr><td>Thermaltake Massive TM</td><td>1팬(200mm) / 600~1000RPM</td><td>17인치</td><td>4~5만원</td><td>대형 팬으로 저소음 고효율</td></tr>
<tr><td>ipTIME NC15</td><td>2팬 / 1200RPM</td><td>15.6인치</td><td>2만원대</td><td>국내 인기, LED, USB 전원</td></tr>
</tbody></table>
<p>쿨링패드 선택 시 <strong>팬 크기가 클수록 소음이 적고 효율이 높습니다</strong>. RPM이 높으면 시끄럽지만 냉각 효과가 강합니다. 노트북 크기에 맞는 제품을 고르세요.</p>

<h2>서멀구리스 교체 방법 (DIY)</h2>
<p>서멀구리스(Thermal Paste)는 CPU/GPU와 방열판 사이에 발라 열을 효율적으로 전달하는 재료입니다. 3~5년이 지나면 굳거나 말라서 열전달 효율이 크게 떨어집니다.</p>
<h3>필요 준비물</h3>
<ul>
<li>서멀구리스: 아틱 MX-4, 딥쿨 Z9, 서멀라이트 TF7 등 (1~2만원)</li>
<li>정밀 드라이버 세트 (크로스, 토크스 등)</li>
<li>이소프로필 알코올 (기존 구리스 제거용)</li>
<li>면봉 또는 무보풀 천</li>
<li>정전기 방지 장갑</li>
</ul>
<h3>교체 단계</h3>
<ol>
<li><strong>노트북 전원 완전 차단 후 배터리 분리</strong></li>
<li>뒷면 나사 모두 제거 후 후면 커버 분리</li>
<li>팬 커넥터와 방열판 나사 제거 (십자/대각선 순서로)</li>
<li>이소프로필 알코올로 CPU/GPU 표면의 <strong>기존 구리스 완전 제거</strong></li>
<li>새 서멀구리스를 CPU 중앙에 쌀알 크기만큼 도포</li>
<li>방열판을 수직으로 내려놓으면 자연스럽게 퍼짐 (고루 펴 바를 필요 없음)</li>
<li>나사를 대각선 순서로 조여서 압력 균일하게 분산</li>
<li>조립 후 온도 확인 (HWMonitor)</li>
</ol>
<p>서멀구리스 교체 후 <strong>CPU 온도가 10~20도 내려가는</strong> 경우도 흔합니다.</p>

<h2>내부 먼지 청소 방법</h2>
<ul>
<li><strong>에어스프레이(캔)</strong>: 환기구 방향으로 먼지를 날려냄. 압축공기를 팬에 직접 쏘면 팬이 과회전할 수 있으니 손가락으로 팬 날개를 잡고 사용</li>
<li><strong>뒷면 커버 열기</strong>: 위 서멀구리스 교체와 같이 열면 팬과 방열판 직접 청소 가능</li>
<li><strong>청소 주기</strong>: 먼지가 많은 환경은 6개월, 일반 환경은 1년에 한 번 권장</li>
</ul>

{imgs[2]}

<h2>노트북 수명 늘리는 일상 습관</h2>
<ul>
<li><strong>평평한 곳에서만 사용</strong>: 침대, 소파에서 사용하면 환기구가 막혀 온도가 급상승합니다</li>
<li><strong>배터리 20~80% 유지</strong>: 항상 100% 충전 상태를 유지하면 배터리가 빨리 노화됩니다</li>
<li><strong>노트북 절전 모드 활용</strong>: 잠깐 자리를 비울 때 절전 모드를 사용하면 발열과 배터리 소모를 줄일 수 있습니다</li>
<li><strong>직사광선, 고온 환경 피하기</strong>: 차 안에 두거나 직사광선에 노출하면 부품 수명이 단축됩니다</li>
</ul>

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 노트북 온도가 몇 도 이상이면 위험한가요?</h3>
<p>A. CPU 기준으로 <strong>90도 이상이 지속되면 위험</strong>합니다. 70~80도는 고부하 작업 시 정상 범위이며, 쓰로틀링(성능 제한)은 보통 90~95도에서 발생합니다. 평소 유휴 상태에서 50~60도 이하가 이상적입니다.</p>
<h3>Q. 서멀구리스 교체가 너무 어렵습니다. 서비스센터에 맡기면 되나요?</h3>
<p>A. 네, 삼성·LG 서비스센터에서 <strong>내부 청소 및 서멀구리스 교체 서비스</strong>를 제공합니다. 비용은 2~5만원 정도이며, 보증 기간 내라도 먼지 청소는 유상인 경우가 많습니다.</p>
<h3>Q. 쿨링패드를 쓰면 얼마나 온도가 내려가나요?</h3>
<p>A. 제품과 환경에 따라 다르지만 <strong>평균 5~10도</strong> 정도 낮아집니다. 근본 원인(먼지, 구리스)을 해결하지 않으면 쿨링패드만으로는 한계가 있습니다.</p>
<h3>Q. 노트북 팬 소리가 갑자기 커졌습니다. 이유가 뭔가요?</h3>
<p>A. 팬 소리가 갑자기 커진 이유는 <strong>백그라운드 업데이트, 악성코드, 먼지로 인한 팬 과부하</strong>가 주원인입니다. 작업관리자에서 CPU 사용률을 확인하고, 먼지 청소도 함께 점검하세요.</p>

{cta_block("쿠팡에서 쿨링패드 최저가 비교하기", "다양한 브랜드의 쿨링패드를 최저가로 비교하고 구매하세요", "https://www.coupang.com/", "yellow")}

<h2>마무리</h2>
<p>노트북 발열 문제는 <strong>소프트웨어 설정 최적화 → 쿨링패드 사용 → 내부 청소 → 서멀구리스 교체</strong> 순으로 단계적으로 접근하는 것이 좋습니다. 가장 효과적인 방법은 내부 청소와 서멀구리스 교체이며, 이 두 가지만 해도 노트북이 새것처럼 시원해지는 경험을 할 수 있습니다.</p>'''
    },

    # 10. 크롬 확장프로그램 추천
    {
        "title": "크롬 확장프로그램 추천 업무 효율 높이는 필수 확장 TOP 10 총정리",
        "cat": 5,
        "slug": "chrome-extension-recommendation-top10",
        "images": [
            ("photo-1498049794561-7780e7231661", "크롬 확장프로그램 추천"),
            ("photo-1517694712202-14dd9538aa97", "크롬 브라우저 업무 효율"),
            ("photo-1519389950473-47ba0277781c", "생산성 툴 추천"),
        ],
        "labels": ["크롬확장프로그램", "크롬확장추천", "uBlockOrigin", "Bitwarden", "Grammarly", "NotionWebClipper", "OneTab", "업무효율"],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">크롬(Chrome) 브라우저는 확장프로그램 하나로 완전히 다른 도구가 됩니다. 광고 차단, 비밀번호 관리, 집중력 향상, 개발자 도구까지 <strong>업무 효율을 2배로 높여주는 크롬 확장프로그램 TOP 10</strong>을 카테고리별로 정리했습니다. 설치 방법과 악성 확장을 구별하는 방법도 함께 알려드립니다.</p>

{imgs[0]}

<h2>생산성 확장프로그램 (3종)</h2>

<h3>1. Notion Web Clipper</h3>
<p>웹 페이지, 기사, 유튜브 영상 등을 <strong>Notion 페이지로 바로 저장</strong>하는 확장입니다. 리서치, 스크랩, 아이디어 수집에 필수입니다.</p>
<table><thead><tr><th>항목</th><th>내용</th></tr></thead><tbody>
<tr><td>개발사</td><td>Notion Labs</td></tr>
<tr><td>평점</td><td>★★★★☆ (4.2/5)</td></tr>
<tr><td>사용자 수</td><td>400만+</td></tr>
<tr><td>주요 기능</td><td>웹 클리핑, 데이터베이스 저장, 태그 분류</td></tr>
<tr><td>가격</td><td>무료 (Notion 계정 필요)</td></tr>
</tbody></table>

<h3>2. Todoist</h3>
<p>브라우저에서 바로 할 일을 추가하고 마감일을 설정하는 <strong>할 일 관리 확장</strong>입니다. 웹 서핑 중 발견한 할 일을 즉시 기록할 수 있습니다.</p>
<table><thead><tr><th>항목</th><th>내용</th></tr></thead><tbody>
<tr><td>개발사</td><td>Doist</td></tr>
<tr><td>평점</td><td>★★★★☆ (4.5/5)</td></tr>
<tr><td>사용자 수</td><td>300만+</td></tr>
<tr><td>주요 기능</td><td>빠른 할 일 추가, 우선순위 설정, 팀 공유</td></tr>
<tr><td>가격</td><td>무료 / 프리미엄 월 4달러</td></tr>
</tbody></table>

<h3>3. Grammarly</h3>
<p>영어 문법, 맞춤법, 문체를 실시간으로 교정해주는 <strong>영어 작문 필수 도구</strong>입니다. 이메일, 구글 독스, SNS 입력창 어디서나 작동합니다.</p>
<table><thead><tr><th>항목</th><th>내용</th></tr></thead><tbody>
<tr><td>개발사</td><td>Grammarly Inc.</td></tr>
<tr><td>평점</td><td>★★★★★ (4.7/5)</td></tr>
<tr><td>사용자 수</td><td>1,000만+</td></tr>
<tr><td>주요 기능</td><td>문법 교정, 스타일 제안, 표절 검사(유료)</td></tr>
<tr><td>가격</td><td>무료 / 프리미엄 월 12달러</td></tr>
</tbody></table>

{cta_block("Chrome 웹스토어에서 확장 설치하기", "크롬 웹스토어에서 모든 확장프로그램을 무료로 설치할 수 있습니다", "https://chromewebstore.google.com/", "blue")}

{imgs[1]}

<h2>보안 확장프로그램 (2종)</h2>

<h3>4. uBlock Origin</h3>
<p>광고 차단 분야에서 <strong>가장 신뢰받는 무료 오픈소스 확장</strong>입니다. 광고뿐 아니라 트래커, 악성 스크립트까지 차단합니다.</p>
<table><thead><tr><th>항목</th><th>내용</th></tr></thead><tbody>
<tr><td>개발사</td><td>Raymond Hill (오픈소스)</td></tr>
<tr><td>평점</td><td>★★★★★ (4.8/5)</td></tr>
<tr><td>사용자 수</td><td>3,000만+</td></tr>
<tr><td>주요 기능</td><td>광고 차단, 트래커 차단, 팝업 차단, 커스텀 필터</td></tr>
<tr><td>가격</td><td>완전 무료 (오픈소스)</td></tr>
</tbody></table>
<p>AdBlock Plus와 달리 <strong>허용 광고 목록이 없어 더 강력한 차단</strong>이 가능합니다. 페이지 로딩도 눈에 띄게 빨라집니다.</p>

<h3>5. Bitwarden</h3>
<p>오픈소스 비밀번호 관리자로, <strong>모든 사이트의 아이디·비밀번호를 안전하게 저장</strong>하고 자동 입력해줍니다.</p>
<table><thead><tr><th>항목</th><th>내용</th></tr></thead><tbody>
<tr><td>개발사</td><td>Bitwarden Inc.</td></tr>
<tr><td>평점</td><td>★★★★★ (4.8/5)</td></tr>
<tr><td>사용자 수</td><td>500만+</td></tr>
<tr><td>주요 기능</td><td>비밀번호 저장/자동입력, 강력한 비밀번호 생성, 2FA 지원</td></tr>
<tr><td>가격</td><td>무료 / 프리미엄 연 10달러</td></tr>
</tbody></table>

<h2>개발자 확장프로그램 (2종)</h2>

<h3>6. React Developer Tools</h3>
<p>React로 만든 웹사이트의 컴포넌트 구조, 상태(State), Props를 <strong>실시간으로 검사</strong>하는 필수 개발 도구입니다.</p>
<ul>
<li>컴포넌트 트리 시각화 및 검색</li>
<li>State/Props 실시간 편집</li>
<li>렌더링 성능 프로파일링</li>
<li>React 18 이상 완벽 지원</li>
</ul>

<h3>7. JSON Viewer</h3>
<p>API 응답이나 JSON 파일을 <strong>보기 좋은 트리 구조로 자동 변환</strong>해줍니다. 개발자뿐 아니라 API를 자주 다루는 분께도 유용합니다.</p>
<ul>
<li>JSON을 색상 코드로 가독성 높게 표시</li>
<li>접기/펼치기로 원하는 부분만 확인</li>
<li>검색 기능으로 원하는 키값 빠르게 찾기</li>
</ul>

<h2>편의 확장프로그램 (3종)</h2>

<h3>8. Dark Reader</h3>
<p>모든 웹사이트에 <strong>다크 모드를 적용</strong>하는 확장입니다. 어두운 환경에서 눈의 피로를 크게 줄여줍니다.</p>
<ul>
<li>밝기, 명암, 세피아 색상 커스터마이징 가능</li>
<li>사이트별 다크모드 활성화/비활성화 설정</li>
<li>사용자 5,000만+ (크롬 스토어 최다 사용 확장 중 하나)</li>
</ul>

<h3>9. OneTab</h3>
<p>열려있는 탭을 한 번에 목록으로 변환하여 <strong>메모리를 최대 95%까지 절약</strong>하는 확장입니다. 리서치 중 탭이 20개 이상 열려도 OneTab 하나로 정리됩니다.</p>
<ul>
<li>모든 탭을 하나의 목록 페이지로 압축</li>
<li>그룹별 탭 관리, 링크 공유 기능</li>
<li>복원 시 원하는 탭만 선택해서 열기</li>
</ul>

<h3>10. GoFullPage</h3>
<p>웹 페이지 전체를 스크롤 없이 <strong>한 번에 캡처</strong>하는 스크린샷 확장입니다. PDF 저장도 가능합니다.</p>
<ul>
<li>무한 스크롤 페이지도 전체 캡처 가능</li>
<li>PNG, PDF로 저장</li>
<li>이미지 편집 기능 기본 내장</li>
</ul>

{imgs[2]}

<h2>크롬 확장프로그램 설치 방법</h2>
<ol>
<li>Chrome 브라우저에서 <strong>chromewebstore.google.com</strong> 접속</li>
<li>검색창에 원하는 확장 이름 입력</li>
<li>원하는 확장의 <strong>[Chrome에 추가]</strong> 버튼 클릭</li>
<li>권한 확인 후 <strong>[확장 프로그램 추가]</strong> 클릭</li>
<li>주소창 우측 퍼즐 아이콘(🧩)에서 고정 가능</li>
</ol>

<h2>악성 확장프로그램 구별법</h2>
<p>크롬 웹스토어에도 악성 확장이 있습니다. 설치 전 반드시 확인하세요.</p>
<table><thead><tr><th>확인 항목</th><th>안전한 확장</th><th>의심스러운 확장</th></tr></thead><tbody>
<tr><td>사용자 수</td><td>수십만 이상</td><td>수백~수천 명</td></tr>
<tr><td>리뷰</td><td>다양하고 진정성 있는 리뷰</td><td>짧은 5점 리뷰만 있음</td></tr>
<tr><td>개발자 정보</td><td>공식 회사명, 웹사이트</td><td>개인 이메일, 정보 없음</td></tr>
<tr><td>요청 권한</td><td>필요한 권한만 요청</td><td>과도한 권한 요청 (모든 사이트 데이터 등)</td></tr>
<tr><td>업데이트 주기</td><td>정기적 업데이트</td><td>오래 방치됨</td></tr>
</tbody></table>
<p>특히 <strong>"모든 사이트에서 데이터 읽기 및 변경"</strong> 권한을 요청하는 확장은 개인정보 수집 위험이 있으니 신중하게 설치하세요.</p>

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 확장프로그램이 많으면 크롬이 느려지나요?</h3>
<p>A. 네, 확장프로그램은 각각 메모리를 사용합니다. <strong>5~7개 이하로 필수 확장만 유지</strong>하는 것을 권장합니다. chrome://extensions에서 사용 안 하는 확장은 비활성화해두세요.</p>
<h3>Q. 확장프로그램 사용 중 개인정보가 유출될 수 있나요?</h3>
<p>A. 악성 확장의 경우 가능합니다. 공식 개발사가 명확하고, <strong>크롬 웹스토어 인증을 받은 확장(배지 확인)</strong>을 사용하고, 권한이 과도한 확장은 설치하지 마세요.</p>
<h3>Q. uBlock Origin과 AdBlock Plus 중 어떤 것이 더 좋나요?</h3>
<p>A. <strong>uBlock Origin</strong>을 추천합니다. 완전 무료 오픈소스이며, AdBlock Plus는 일부 광고주로부터 돈을 받고 '허용 광고'를 통과시키는 정책이 있습니다.</p>
<h3>Q. 크롬 확장프로그램을 다른 브라우저에서도 쓸 수 있나요?</h3>
<p>A. Microsoft Edge, Brave, Opera 등 <strong>크로미움 기반 브라우저는 크롬 웹스토어 확장을 대부분 그대로 사용</strong>할 수 있습니다. Firefox는 별도 스토어를 사용합니다.</p>

{cta_block("Chrome 웹스토어에서 확장프로그램 탐색", "필요한 확장을 Chrome 웹스토어에서 무료로 설치해보세요", "https://chromewebstore.google.com/", "green")}

<h2>마무리</h2>
<p>크롬 확장프로그램은 올바르게 선택하면 업무 효율을 크게 높여주는 강력한 도구입니다. 오늘 소개한 TOP 10 중에서 <strong>uBlock Origin(광고차단), Bitwarden(비밀번호), OneTab(탭 관리)</strong> 세 가지만 설치해도 브라우저 사용 경험이 완전히 달라집니다. 단, 무분별한 설치는 보안 위험과 성능 저하를 부를 수 있으니 신뢰할 수 있는 확장만 선택해서 사용하세요.</p>'''
    },
]


# ========== 실행 ==========
def main():
    published = []

    for idx, post in enumerate(POSTS, 1):
        print(f"\n{'='*60}")
        print(f"[{idx}/5] {post['title']}")
        print(f"{'='*60}")

        # 1) 이미지 업로드
        img_htmls = []
        first_media_id = None
        for j, (photo_id, alt) in enumerate(post["images"]):
            tmp = download_image(photo_id)
            if not tmp:
                img_htmls.append("")
                continue
            mid, murl = upload_image(tmp, f"{post['slug']}-{j+1}", alt)
            os.unlink(tmp)
            if murl:
                img_htmls.append(img_block(murl, alt))
                if first_media_id is None:
                    first_media_id = mid
                print(f"  이미지 {j+1} OK -> {murl}")
            else:
                img_htmls.append("")
            time.sleep(0.5)

        # 2) 콘텐츠 생성 + URL 자동 링크
        content = auto_link(post["content"](img_htmls))

        # 3) WordPress 발행
        print(f"\n[WordPress] 발행 중...")
        wp_payload = {
            "title": post["title"],
            "content": content,
            "status": "publish",
            "slug": post["slug"],
            "categories": [post["cat"]],
        }
        if first_media_id:
            wp_payload["featured_media"] = first_media_id

        data = json.dumps(wp_payload).encode("utf-8")
        req = urllib.request.Request(API, data=data, method="POST")
        req.add_header("Authorization", f"Basic {AUTH}")
        req.add_header("Content-Type", "application/json")
        wp_link = ""
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                r = json.loads(resp.read().decode())
                pid = r.get("id")
                wp_link = r.get("link", "")
                print(f"  WordPress OK | ID:{pid} | {wp_link}")
                if wp_link:
                    published.append(wp_link)
        except Exception as e:
            print(f"  WordPress FAIL | {e}")

        # 4) Blogger 발행
        print(f"\n[Blogger] 발행 중...")
        try:
            access_token = get_access_token()
            blog_id = get_blog_id(access_token)
            blogger_content = clean_wp_content(content)
            bid, burl = publish_to_blogger(access_token, blog_id, post["title"], blogger_content, labels=post["labels"])
            print(f"  Blogger OK | ID:{bid} | {burl}")
        except urllib.error.HTTPError as e:
            body = e.read().decode() if e.fp else ""
            print(f"  Blogger FAIL | HTTP {e.code} | {body[:300]}")
        except Exception as e:
            print(f"  Blogger FAIL | {e}")

        time.sleep(1)

    # 5) IndexNow 제출
    if published:
        print(f"\n{'='*60}")
        print("네이버/Bing/Yandex IndexNow 제출")
        print(f"{'='*60}")
        naver_payload = {
            "host": "devupbox.com",
            "key": "8dbbd7d6729b4a65b7dce4b9083c65e3",
            "keyLocation": "https://devupbox.com/8dbbd7d6729b4a65b7dce4b9083c65e3.txt",
            "urlList": published
        }
        ndata = json.dumps(naver_payload).encode("utf-8")
        for name, url in [("Naver", "https://searchadvisor.naver.com/indexnow"), ("Bing", "https://www.bing.com/indexnow"), ("Yandex", "https://yandex.com/indexnow")]:
            req = urllib.request.Request(url, data=ndata, method="POST")
            req.add_header("Content-Type", "application/json; charset=utf-8")
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    print(f"  {name}: HTTP {resp.status}")
            except urllib.error.HTTPError as e:
                print(f"  {name}: HTTP {e.code}")
            except Exception as e:
                print(f"  {name}: {e}")

    print(f"\n완료! 총 {len(published)}개 포스트 발행")


if __name__ == "__main__":
    main()

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

# ========== 포스트 정의 ==========
POST = {
    "title": "화물 유가보조금 받는 방법 금액 카드 리터당 환급 조회 신청방법 총정리",
    "cat": 13,
    "slug": "freight-fuel-subsidy-how-to-apply",
    "images": [
        ("photo-1558618666-fcd25c85f82e", "화물 유가보조금 신청"),
        ("photo-1504280390367-361c6d9f38f4", "유가보조금 카드 사용"),
        ("photo-1556742049-0cfed4f6a45d", "유가보조금 환급 조회"),
    ],
    "labels": ["화물유가보조금", "유가보조금", "유가보조금카드", "화물차보조금", "유류세환급", "화물운송", "리터당환급", "유가보조금신청", "유가보조금조회"],
    "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">화물차를 운행하는 운송사업자라면 반드시 알아야 할 제도가 바로 <strong>화물 유가보조금</strong>입니다. 유류비 부담을 줄이기 위해 정부에서 리터당 일정 금액을 돌려주는 제도인데, 생각보다 많은 분들이 신청 방법을 몰라 혜택을 놓치고 있습니다. 이 글에서는 화물 유가보조금의 <strong>신청 자격, 카드 발급, 리터당 환급 금액, 조회 방법</strong>까지 한 번에 정리합니다.</p>

{imgs[0]}

<h2>화물 유가보조금이란?</h2>
<p>화물 유가보조금은 <strong>화물자동차 운송사업자</strong>에게 유류비 일부를 보조해주는 정부 지원 제도입니다. 국제 유가 변동으로 인한 운송업계의 부담을 완화하기 위해 시행되고 있으며, <strong>유가보조금 전용 유류구매카드</strong>를 통해 주유 시 자동으로 보조금이 적립됩니다.</p>

<table><thead><tr><th>항목</th><th>내용</th></tr></thead><tbody>
<tr><td>제도명</td><td>화물자동차 유가보조금</td></tr>
<tr><td>지원 대상</td><td>화물자동차 운송사업 등록 차량</td></tr>
<tr><td>지원 방식</td><td>유류구매카드로 주유 시 리터당 보조금 환급</td></tr>
<tr><td>관할 기관</td><td>한국교통안전공단 (TS)</td></tr>
<tr><td>근거 법률</td><td>화물자동차 운수사업법</td></tr>
<tr><td>지급 주기</td><td>월 단위 (익월 지급)</td></tr>
</tbody></table>

<h2>유가보조금 지원 대상</h2>
<p>모든 화물차가 대상이 되는 것은 아닙니다. 아래 조건을 충족해야 유가보조금을 받을 수 있습니다.</p>
<h3>지원 대상</h3>
<ul>
<li><strong>영업용 화물자동차</strong>: 화물자동차 운송사업 허가를 받고 등록된 차량</li>
<li><strong>일반화물</strong>, <strong>개별화물</strong>, <strong>용달화물</strong> 모두 해당</li>
<li><strong>특수용도형 화물차</strong>: 덤프트럭, 콘크리트믹서트럭 등 건설기계도 포함</li>
<li><strong>경유, LPG, CNG 차량</strong> 모두 지원 (유종별 보조금 상이)</li>
</ul>
<h3>지원 제외 대상</h3>
<ul>
<li>자가용 화물차 (영업용이 아닌 개인 화물차)</li>
<li>운송사업 등록이 말소된 차량</li>
<li>유가보조금 부정수급으로 자격 정지된 자</li>
<li>차령 초과 차량 (일부 제한)</li>
</ul>

{cta_block("한국교통안전공단 유가보조금 안내", "유가보조금 대상 여부를 공식 사이트에서 확인하세요", "https://www.kotsa.or.kr/", "blue")}

<h2>리터당 유가보조금 금액</h2>
<p>유가보조금은 <strong>유종(경유, LPG, CNG)</strong>에 따라 리터당 지급 금액이 다릅니다. 국제 유가와 정부 정책에 따라 조정될 수 있습니다.</p>

<table><thead><tr><th>유종</th><th>리터당 보조금</th><th>월 한도</th><th>비고</th></tr></thead><tbody>
<tr><td>경유</td><td>약 183.48원/L</td><td>없음 (실주유량 기준)</td><td>가장 많은 화물차 해당</td></tr>
<tr><td>LPG</td><td>약 160.58원/L</td><td>없음</td><td>LPG 화물차 대상</td></tr>
<tr><td>CNG</td><td>약 178.56원/kg</td><td>없음</td><td>천연가스 차량</td></tr>
</tbody></table>

<h3>보조금 계산 예시</h3>
<table><thead><tr><th>구분</th><th>월 주유량</th><th>리터당 보조금</th><th>월 환급액</th><th>연간 환급액</th></tr></thead><tbody>
<tr><td>5톤 화물차</td><td>약 1,500L</td><td>183.48원</td><td>약 275,220원</td><td>약 3,302,640원</td></tr>
<tr><td>11톤 화물차</td><td>약 3,000L</td><td>183.48원</td><td>약 550,440원</td><td>약 6,605,280원</td></tr>
<tr><td>25톤 대형 화물차</td><td>약 5,000L</td><td>183.48원</td><td>약 917,400원</td><td>약 11,008,800원</td></tr>
</tbody></table>
<p>대형 화물차의 경우 <strong>연간 약 1,100만 원</strong>까지 환급받을 수 있어 반드시 신청해야 하는 제도입니다.</p>

{imgs[1]}

<h2>유가보조금 카드 발급 방법</h2>
<p>유가보조금을 받으려면 반드시 <strong>유류구매카드</strong>를 발급받아야 합니다. 일반 신용카드나 체크카드로 주유하면 보조금이 적용되지 않습니다.</p>

<h3>카드 발급 절차</h3>
<ol>
<li><strong>화물자동차 운송사업 등록</strong> 완료 (관할 시·군·구청)</li>
<li><strong>한국교통안전공단</strong>(TS) 화물운송 종사자격증 취득</li>
<li><strong>유류구매카드 신청</strong>: 아래 카드사에서 발급 가능
    <ul>
    <li>신한카드</li>
    <li>현대카드</li>
    <li>KB국민카드</li>
    <li>우리카드</li>
    <li>하나카드</li>
    </ul>
</li>
<li>카드 수령 후 <strong>한국교통안전공단 시스템에 카드 등록</strong></li>
<li>등록 완료 후 해당 카드로 주유하면 <strong>자동 보조금 적립</strong></li>
</ol>

<h3>카드 발급 시 필요 서류</h3>
<table><thead><tr><th>서류</th><th>비고</th></tr></thead><tbody>
<tr><td>사업자등록증 사본</td><td>화물운송사업 등록 확인</td></tr>
<tr><td>화물자동차 등록증 사본</td><td>차량 정보 확인</td></tr>
<tr><td>대표자 신분증</td><td>본인 확인</td></tr>
<tr><td>화물운송 종사자격증</td><td>한국교통안전공단 발급</td></tr>
<tr><td>통장 사본</td><td>보조금 입금 계좌</td></tr>
</tbody></table>

{cta_block("유류구매카드 발급 신청", "카드사별 유류구매카드 발급 조건과 혜택을 비교해보세요", "https://www.card.co.kr/", "yellow")}

<h2>유가보조금 카드 사용 방법</h2>
<p>유류구매카드 사용 시 주의할 점이 있습니다. 올바르게 사용해야 보조금이 정상 적립됩니다.</p>
<h3>올바른 사용법</h3>
<ul>
<li><strong>본인 차량에만 주유</strong>: 등록된 차량 번호와 일치하는 차량에만 사용</li>
<li><strong>지정 주유소 이용</strong>: 유가보조금 가맹 주유소에서만 적용 (대부분의 주유소 해당)</li>
<li><strong>1일 주유 한도</strong>: 차량 유종·톤급별 1일 최대 주유량 제한 있음</li>
<li><strong>주유 시 차량번호 입력</strong>: 주유소 POS에서 차량번호 확인 필수</li>
</ul>
<h3>주의사항</h3>
<ul>
<li><strong>타인 차량 주유 금지</strong>: 적발 시 부정수급으로 자격 정지 + 환수</li>
<li><strong>주유 후 되팔기 금지</strong>: 유류를 사서 타인에게 판매 시 형사처벌</li>
<li><strong>카드 대여 금지</strong>: 타인에게 카드를 빌려주면 자격 정지</li>
<li>부정수급 적발 시 <strong>보조금 전액 환수 + 최대 5년 자격 정지</strong></li>
</ul>

<h2>유가보조금 신청 방법 (단계별)</h2>
<h3>신규 신청</h3>
<ol>
<li><strong>화물자동차 운송사업 허가</strong> (관할 시·군·구청 방문)</li>
<li><strong>화물운송 종사자격증 취득</strong> (한국교통안전공단 시험 응시)</li>
<li><strong>유류구매카드 발급</strong> (카드사 방문 또는 온라인 신청)</li>
<li><strong>화물운송정보시스템 가입</strong> (efms.kotsa.or.kr)</li>
<li><strong>카드 등록 및 차량 정보 입력</strong></li>
<li><strong>등록 완료 후 주유 시 자동 적립 시작</strong></li>
</ol>

<h3>온라인 신청 (화물운송정보시스템)</h3>
<ol>
<li>화물운송정보시스템 <strong>efms.kotsa.or.kr</strong> 접속</li>
<li>회원가입 및 로그인</li>
<li>유가보조금 → 카드 등록 메뉴</li>
<li>차량 정보 및 카드 번호 입력</li>
<li>등록 완료 확인</li>
</ol>

{cta_block("화물운송정보시스템 바로가기", "유가보조금 신청, 카드 등록, 보조금 조회를 한곳에서 처리하세요", "https://efms.kotsa.or.kr/", "blue")}

{imgs[2]}

<h2>유가보조금 조회 방법</h2>
<p>내가 얼마나 보조금을 받았는지, 이번 달 적립 현황은 어떤지 쉽게 확인할 수 있습니다.</p>

<h3>조회 방법 3가지</h3>
<table><thead><tr><th>조회 방법</th><th>경로</th><th>확인 가능 정보</th></tr></thead><tbody>
<tr><td>화물운송정보시스템</td><td>efms.kotsa.or.kr → 유가보조금 → 지급내역 조회</td><td>월별 지급액, 주유 내역, 적립 현황</td></tr>
<tr><td>한국교통안전공단 콜센터</td><td>1588-0990</td><td>전화로 지급 내역 확인</td></tr>
<tr><td>카드사 앱/홈페이지</td><td>해당 카드사 로그인</td><td>카드 사용 내역, 보조금 적립액</td></tr>
</tbody></table>

<h3>지급 일정</h3>
<ul>
<li><strong>지급 주기</strong>: 월 단위 (전월 주유분을 익월에 지급)</li>
<li><strong>지급 방식</strong>: 등록된 통장으로 자동 입금</li>
<li><strong>지급일</strong>: 매월 중순경 (정확한 날짜는 공단 공지 확인)</li>
<li><strong>정산 기간</strong>: 주유일로부터 약 30~45일 소요</li>
</ul>

<h2>유가보조금 환급 절차</h2>
<p>유가보조금은 <strong>주유 → 적립 → 정산 → 입금</strong>의 과정을 거칩니다.</p>
<table><thead><tr><th>단계</th><th>내용</th><th>소요 기간</th></tr></thead><tbody>
<tr><td>1단계</td><td>유류구매카드로 주유</td><td>즉시</td></tr>
<tr><td>2단계</td><td>주유 데이터 전송 (주유소 → 공단)</td><td>1~3일</td></tr>
<tr><td>3단계</td><td>데이터 검증 및 보조금 산정</td><td>월말 정산</td></tr>
<tr><td>4단계</td><td>보조금 지급 (통장 입금)</td><td>익월 중순</td></tr>
</tbody></table>

<h2>유가보조금 부정수급 주의사항</h2>
<p>부정수급은 엄격하게 단속되고 있습니다. 아래 행위는 절대 하지 마세요.</p>
<table><thead><tr><th>부정수급 유형</th><th>처벌 내용</th></tr></thead><tbody>
<tr><td>타인 차량에 주유</td><td>보조금 전액 환수 + 자격 정지 1~5년</td></tr>
<tr><td>유류 되팔기</td><td>형사처벌 + 보조금 환수 + 영구 자격 정지</td></tr>
<tr><td>카드 대여/양도</td><td>보조금 환수 + 자격 정지 3년</td></tr>
<tr><td>허위 서류 제출</td><td>형사처벌 + 보조금 환수</td></tr>
<tr><td>폐업 후 계속 사용</td><td>보조금 전액 환수 + 형사처벌</td></tr>
</tbody></table>
<p>한국교통안전공단은 GPS, 주유소 CCTV, 카드 사용 패턴 분석 등으로 부정수급을 상시 모니터링하고 있습니다.</p>

{cta_block("유가보조금 부정수급 신고", "부정수급을 목격하셨다면 한국교통안전공단에 신고하세요 (1588-0990)", "https://www.kotsa.or.kr/", "green")}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 개인 화물차도 유가보조금을 받을 수 있나요?</h3>
<p>A. <strong>영업용(노란 번호판) 화물차만 대상</strong>입니다. 자가용(흰색 번호판) 화물차는 지원 대상이 아닙니다. 영업용으로 전환하려면 관할 시·군·구청에서 화물자동차 운송사업 허가를 받아야 합니다.</p>

<h3>Q. 유가보조금 카드를 분실했는데 어떻게 하나요?</h3>
<p>A. 즉시 해당 카드사에 <strong>분실 신고 및 재발급</strong>을 요청하세요. 재발급 후 화물운송정보시스템에서 새 카드 번호를 등록해야 보조금이 다시 적립됩니다. 분실 기간 중 주유분은 보조금이 지급되지 않으니 빠르게 처리하세요.</p>

<h3>Q. 주유소 아무 데서나 넣어도 되나요?</h3>
<p>A. 대부분의 주유소에서 가능하지만, <strong>유가보조금 가맹 주유소</strong>에서만 적용됩니다. 간혹 미가맹 주유소가 있으니 주유 전 확인하세요. 화물운송정보시스템에서 가맹 주유소 목록을 조회할 수 있습니다.</p>

<h3>Q. 경유 외에 요소수 비용도 보조되나요?</h3>
<p>A. 요소수는 유가보조금 <strong>지원 대상이 아닙니다</strong>. 유가보조금은 경유, LPG, CNG 등 연료비에 대해서만 지원됩니다. 다만 정부에서 요소수 수급 안정화를 위한 별도 대책을 시행하는 경우가 있으니 관련 공지를 확인하세요.</p>

<h3>Q. 유가보조금을 소급해서 받을 수 있나요?</h3>
<p>A. 카드 등록 <strong>이전 주유분은 소급 적용이 불가</strong>합니다. 카드를 발급받고 시스템에 등록한 시점부터 보조금이 적립되므로, 화물차를 등록하면 가능한 빨리 유류구매카드를 발급받는 것이 유리합니다.</p>

<h3>Q. 차량을 바꾸면 어떻게 하나요?</h3>
<p>A. 차량 변경 시 화물운송정보시스템에서 <strong>기존 차량 말소 → 신규 차량 등록</strong> 절차를 진행해야 합니다. 차량 변경 신고를 하지 않으면 보조금이 지급되지 않거나 부정수급으로 간주될 수 있습니다.</p>

<h2>마무리</h2>
<p>화물 유가보조금은 화물차 운전자에게 <strong>연간 수백만 원에서 천만 원 이상</strong>의 실질적인 혜택을 제공하는 제도입니다. 유류구매카드 발급과 시스템 등록만 완료하면 주유할 때마다 자동으로 보조금이 적립되니, 아직 신청하지 않은 분은 지금 바로 한국교통안전공단(1588-0990)에 문의하거나 화물운송정보시스템(efms.kotsa.or.kr)에서 신청하세요.</p>'''
}


# ========== 실행 ==========
def main():
    print("=" * 60)
    print(f"발행: {POST['title']}")
    print("=" * 60)

    # 1) 이미지 업로드
    img_htmls = []
    first_media_id = None
    for j, (photo_id, alt) in enumerate(POST["images"]):
        tmp = download_image(photo_id)
        if not tmp:
            img_htmls.append("")
            continue
        mid, murl = upload_image(tmp, f"{POST['slug']}-{j+1}", alt)
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
    content = auto_link(POST["content"](img_htmls))

    # ===== WordPress 발행 =====
    print(f"\n[WordPress] 발행 중...")
    wp_payload = {
        "title": POST["title"],
        "content": content,
        "status": "publish",
        "slug": POST["slug"],
        "categories": [POST["cat"]],
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
    except Exception as e:
        print(f"  WordPress FAIL | {e}")

    # ===== Blogger 발행 =====
    print(f"\n[Blogger] 발행 중...")
    try:
        access_token = get_access_token()
        blog_id = get_blog_id(access_token)
        blogger_content = clean_wp_content(content)
        bid, burl = publish_to_blogger(access_token, blog_id, POST["title"], blogger_content, labels=POST["labels"])
        print(f"  Blogger OK | ID:{bid} | {burl}")
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"  Blogger FAIL | HTTP {e.code} | {body[:300]}")
    except Exception as e:
        print(f"  Blogger FAIL | {e}")

    # ===== IndexNow 제출 =====
    if wp_link:
        print(f"\n[IndexNow] 제출 중...")
        naver_payload = {
            "host": "devupbox.com",
            "key": "8dbbd7d6729b4a65b7dce4b9083c65e3",
            "keyLocation": "https://devupbox.com/8dbbd7d6729b4a65b7dce4b9083c65e3.txt",
            "urlList": [wp_link]
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

    print(f"\n{'='*60}")
    print("완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

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
MEDIA_API_URL = "https://devupbox.com/wp-json/wp/v2/media"

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


# ========== 5개 포스트 정의 ==========
POSTS = [
    # 1. 윈도우 11 최적화
    {
        "title": "윈도우 11 최적화 설정법 느린 PC 빠르게 만드는 방법 총정리",
        "cat": 5,
        "slug": "windows-11-optimization-speed-up",
        "images": [
            ("photo-1517694712202-14dd9538aa97", "윈도우 11 최적화 설정 노트북"),
            ("photo-1550751827-4bd374c3f58b", "PC 성능 최적화 설정"),
            ("photo-1531297484001-80022131f5a1", "윈도우 속도 개선 방법"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">윈도우 11을 쓰다 보면 어느 순간 <strong>PC가 눈에 띄게 느려지는 것</strong>을 느끼게 됩니다. 새로 구입했을 때는 빠릿빠릿하던 컴퓨터가 몇 달 지나면 부팅도 느리고 프로그램 실행도 답답해지는 경우가 많습니다. 이 글에서는 돈 한 푼 쓰지 않고 윈도우 11 설정만으로 <strong>PC 속도를 눈에 띄게 빠르게 만드는 최적화 방법</strong>을 하나씩 정리합니다.</p>

{imgs[0]}

<h2>윈도우 11이 느려지는 주요 원인</h2>
<p>PC가 느려지는 이유는 대부분 소프트웨어적인 문제입니다. 하드웨어를 교체하기 전에 아래 원인들을 먼저 확인해보세요.</p>
<ul>
<li><strong>시작프로그램 과다</strong>: 부팅 시 자동으로 실행되는 프로그램이 많아질수록 부팅 시간이 길어집니다</li>
<li><strong>불필요한 시각 효과</strong>: 윈도우의 애니메이션, 그림자 효과 등이 CPU와 GPU를 차지합니다</li>
<li><strong>디스크 공간 부족</strong>: 저장공간이 80% 이상 차면 시스템이 눈에 띄게 느려집니다</li>
<li><strong>백그라운드 앱 실행</strong>: 사용하지 않는 앱이 백그라운드에서 메모리를 잡아먹습니다</li>
<li><strong>레지스트리 오류 누적</strong>: 프로그램 설치/삭제를 반복하면 레지스트리에 불필요한 항목이 쌓입니다</li>
<li><strong>드라이버 미업데이트</strong>: 오래된 드라이버가 하드웨어 성능을 제대로 끌어내지 못합니다</li>
</ul>

<table><thead><tr><th>원인</th><th>영향도</th><th>개선 난이도</th></tr></thead><tbody>
<tr><td>시작프로그램 과다</td><td>★★★★★</td><td>쉬움</td></tr>
<tr><td>시각 효과 활성화</td><td>★★★★☆</td><td>쉬움</td></tr>
<tr><td>디스크 공간 부족</td><td>★★★★☆</td><td>보통</td></tr>
<tr><td>백그라운드 앱</td><td>★★★☆☆</td><td>쉬움</td></tr>
<tr><td>레지스트리 오류</td><td>★★★☆☆</td><td>보통</td></tr>
<tr><td>드라이버 문제</td><td>★★☆☆☆</td><td>보통</td></tr>
</tbody></table>

<h2>1단계. 시작프로그램 정리</h2>
<p>부팅 속도 개선에 가장 효과가 큰 방법입니다. 사용하지 않는 시작프로그램을 비활성화하면 <strong>부팅 시간이 30~50% 단축</strong>되는 경우도 있습니다.</p>
<ol>
<li><strong>Ctrl + Shift + Esc</strong>로 작업 관리자 실행</li>
<li>상단 탭에서 <strong>[시작 프로그램]</strong> 클릭</li>
<li>시작 영향이 '높음'으로 표시된 항목 중 불필요한 것 선택</li>
<li>마우스 우클릭 → <strong>[사용 안 함]</strong> 선택</li>
</ol>
<p>카카오톡, 멜론, 웨일 같은 프로그램은 시작프로그램에서 꺼도 아이콘 클릭으로 언제든 실행할 수 있습니다. <strong>백신 프로그램과 드라이버 관련 항목은 비활성화하지 마세요.</strong></p>

<h2>2단계. 시각 효과 끄기</h2>
<p>윈도우 11은 기본적으로 다양한 애니메이션과 시각 효과를 제공합니다. 이 기능들은 GPU와 CPU 자원을 소모하므로, 저사양 PC에서는 끄는 것이 효과적입니다.</p>
<ol>
<li>시작 버튼 우클릭 → <strong>[시스템]</strong></li>
<li>오른쪽 상단 <strong>[고급 시스템 설정]</strong></li>
<li><strong>[성능]</strong> 탭 → <strong>[설정]</strong> 클릭</li>
<li><strong>[최고 성능으로 조정]</strong> 선택 또는 개별 항목 비활성화</li>
</ol>
<p>특히 '창 최소화 및 최대화 애니메이션', '작업 표시줄 애니메이션', '창 내 컨트롤 및 요소에 애니메이션 효과 적용' 항목을 끄면 체감 속도가 올라갑니다.</p>

{cta_block("마이크로소프트 공식 PC 최적화 가이드", "윈도우 11 공식 도움말에서 성능 향상 팁을 확인하세요", "https://www.microsoft.com/ko-kr/", "blue")}

{imgs[1]}

<h2>3단계. 디스크 정리 및 저장공간 최적화</h2>
<p>디스크가 가득 차면 윈도우가 임시 파일을 만들 공간이 부족해져 전반적인 속도가 저하됩니다. 최소 <strong>전체 용량의 20% 이상</strong>은 여유 공간으로 확보하세요.</p>
<h3>윈도우 내장 디스크 정리 사용법</h3>
<ol>
<li>시작 메뉴에서 <strong>'디스크 정리'</strong> 검색 후 실행</li>
<li>C 드라이브 선택</li>
<li>임시 파일, 다운로드한 프로그램 파일, 축소판 그림 등 체크</li>
<li><strong>[시스템 파일 정리]</strong>를 클릭하면 Windows 업데이트 이전 파일도 삭제 가능</li>
</ol>
<h3>저장소 센스 자동 정리 설정</h3>
<ol>
<li>설정 → 시스템 → <strong>[저장소]</strong></li>
<li><strong>[저장소 센스]</strong> 토글 켜기</li>
<li>자동으로 임시 파일, 휴지통을 정기 정리</li>
</ol>

<h2>4단계. 레지스트리 최적화</h2>
<p>레지스트리는 윈도우의 설정 데이터베이스입니다. 프로그램을 많이 설치하고 삭제할수록 불필요한 항목이 쌓여 시스템 응답 속도에 영향을 줍니다.</p>
<ul>
<li><strong>무료 툴 사용</strong>: CCleaner, Wise Registry Cleaner 등 무료 툴로 안전하게 정리 가능</li>
<li><strong>주의사항</strong>: 레지스트리 직접 수정은 시스템 오류를 유발할 수 있으므로 전문 툴을 사용하고 반드시 백업 후 진행</li>
<li><strong>레지스트리 백업</strong>: regedit 실행 → 파일 → 내보내기로 현재 상태 저장</li>
</ul>

<h2>5단계. 불필요한 앱 제거</h2>
<p>윈도우 11에는 기본 설치된 앱 외에도 제조사가 추가한 블로트웨어가 많습니다. 사용하지 않는 앱을 제거하면 저장 공간과 메모리를 확보할 수 있습니다.</p>
<ol>
<li>설정 → 앱 → <strong>[설치된 앱]</strong></li>
<li>사용 빈도가 낮은 앱 목록 확인</li>
<li>해당 앱 우측 점 3개(···) 클릭 → <strong>[제거]</strong></li>
</ol>
<p>Xbox 게임 바, Cortana, 3D 뷰어 등 사용하지 않는 기본 앱도 제거 대상입니다. 단, Microsoft Store와 Edge는 시스템 구성 요소라 제거가 어렵습니다.</p>

<h2>6단계. 메모리 관리 및 가상 메모리 설정</h2>
<p>RAM이 부족할 경우 윈도우는 디스크 일부를 메모리처럼 사용하는 <strong>가상 메모리(페이징 파일)</strong>를 활용합니다. 설정이 잘못되면 오히려 속도가 느려질 수 있습니다.</p>
<table><thead><tr><th>RAM 용량</th><th>권장 가상 메모리</th><th>비고</th></tr></thead><tbody>
<tr><td>4GB 이하</td><td>RAM × 1.5 ~ 3배</td><td>최소 설정 필수</td></tr>
<tr><td>8GB</td><td>시스템 관리 (자동)</td><td>윈도우 자동 설정 권장</td></tr>
<tr><td>16GB 이상</td><td>최소값으로 설정 가능</td><td>SSD라면 자동도 무방</td></tr>
</tbody></table>

{imgs[2]}

<h2>7단계. 전원 옵션 및 게임 모드 설정</h2>
<p>전원 옵션이 '절전 모드'로 설정되어 있으면 CPU 성능이 제한됩니다. 데스크탑 PC나 고사양 작업 시에는 <strong>'고성능' 또는 '균형 조정' 모드</strong>를 사용하세요.</p>
<ol>
<li>설정 → 시스템 → <strong>[전원 및 배터리]</strong></li>
<li>전원 모드를 <strong>[최고 성능]</strong> 선택</li>
</ol>
<h3>게임 모드 활성화</h3>
<p>게임이나 고사양 작업 시에는 게임 모드를 켜면 CPU/GPU 자원을 집중 배분합니다.</p>
<ol>
<li>설정 → <strong>[게임]</strong> → 게임 모드</li>
<li>토글을 <strong>[켜기]</strong>로 설정</li>
</ol>

<h2>SSD 교체 효과</h2>
<p>위의 모든 설정을 적용해도 HDD를 사용 중이라면 체감 속도 개선에 한계가 있습니다. <strong>HDD → SSD 교체</strong>는 가장 劇的인 성능 향상을 가져옵니다.</p>
<table><thead><tr><th>구분</th><th>HDD (7200RPM)</th><th>SATA SSD</th><th>NVMe SSD</th></tr></thead><tbody>
<tr><td>순차 읽기</td><td>약 120MB/s</td><td>약 550MB/s</td><td>약 3,500MB/s</td></tr>
<tr><td>부팅 시간</td><td>60~90초</td><td>15~25초</td><td>10~15초</td></tr>
<tr><td>프로그램 로딩</td><td>느림</td><td>빠름</td><td>매우 빠름</td></tr>
<tr><td>가격 (1TB 기준)</td><td>5만원대</td><td>8~10만원</td><td>10~15만원</td></tr>
</tbody></table>
<p>노트북 사용자라면 M.2 슬롯 유무를 확인하고, 데스크탑은 NVMe SSD 교체를 적극 추천합니다.</p>

{cta_block("윈도우 11 최신 업데이트 확인하기", "최신 업데이트는 성능 개선과 보안 패치를 포함합니다", "https://www.microsoft.com/ko-kr/", "green")}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 윈도우를 다시 설치하면 무조건 빨라지나요?</h3>
<p>A. 클린 설치를 하면 초기화된 상태로 빨라지지만, 같은 환경에서 사용하면 다시 느려집니다. <strong>위의 최적화 설정을 먼저 적용</strong>해보고, 그래도 안 되면 초기화를 고려하세요.</p>
<h3>Q. 램이 8GB인데 16GB로 늘리면 많이 빨라지나요?</h3>
<p>A. 멀티태스킹이 많거나 크롬 탭을 많이 열어두는 경우 체감 효과가 큽니다. 게임, 영상 편집, 개발 환경에서는 <strong>16GB가 실질적 차이</strong>를 만들어냅니다.</p>
<h3>Q. 레지스트리 청소 프로그램이 오히려 문제를 일으킬 수도 있나요?</h3>
<p>A. 저품질 무료 툴은 잘못된 항목을 삭제해 시스템 오류를 유발할 수 있습니다. <strong>CCleaner처럼 검증된 툴</strong>을 사용하고 반드시 백업 후 진행하세요.</p>
<h3>Q. 시각 효과를 모두 끄면 화면이 어색한가요?</h3>
<p>A. 애니메이션이 사라져 전환이 단순해집니다. 체감상 어색할 수 있지만, <strong>성능이 우선이라면 '최고 성능으로 조정'</strong>을 선택하고 필요한 항목만 개별 켜면 됩니다.</p>

<h2>마무리</h2>
<p>윈도우 11 최적화는 새 부품 구입 없이도 상당한 속도 개선을 가져옵니다. 시작프로그램 정리와 시각 효과 끄기만으로도 부팅 시간이 크게 줄어드는 것을 체감할 수 있습니다. 오늘 소개한 방법을 하나씩 적용해보고, 그래도 부족하다면 SSD 교체나 RAM 증설을 고려해보세요.</p>'''
    },

    # 2. 무료 VPN 추천
    {
        "title": "무료 VPN 추천 비교 안전한 VPN 선택 가이드 총정리",
        "cat": 5,
        "slug": "free-vpn-recommendation-comparison-guide",
        "images": [
            ("photo-1563986768609-322da13575f2", "무료 VPN 보안 설정"),
            ("photo-1519389950473-47ba0277781c", "VPN 선택 가이드"),
            ("photo-1531297484001-80022131f5a1", "안전한 인터넷 사용"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">해외 콘텐츠를 이용하거나 공공 와이파이에서 개인정보를 보호하고 싶을 때 <strong>VPN</strong>이 필요합니다. 유료 VPN이 좋은 건 알지만 매달 비용을 내기 부담스러운 분들을 위해, 실제로 써볼 만한 <strong>무료 VPN TOP 5</strong>를 비교 분석했습니다. 속도, 서버 수, 데이터 한도, 보안 수준까지 한눈에 정리합니다.</p>

{imgs[0]}

<h2>VPN이란?</h2>
<p>VPN(Virtual Private Network)은 인터넷 연결을 <strong>암호화된 터널</strong>로 보호하는 기술입니다. 내 IP 주소를 숨기고, 공공 와이파이에서도 데이터를 안전하게 전송할 수 있습니다.</p>
<table><thead><tr><th>VPN 주요 기능</th><th>설명</th></tr></thead><tbody>
<tr><td>IP 주소 숨기기</td><td>실제 위치와 IP를 VPN 서버 IP로 대체</td></tr>
<tr><td>트래픽 암호화</td><td>AES-256 암호화로 데이터 도청 방지</td></tr>
<tr><td>지역 제한 우회</td><td>특정 국가에서만 접근 가능한 콘텐츠 이용</td></tr>
<tr><td>공공 와이파이 보호</td><td>카페, 공항 등 보안 취약 네트워크에서 보호</td></tr>
<tr><td>검열 우회</td><td>특정 국가의 인터넷 검열 우회 가능</td></tr>
</tbody></table>

<h2>무료 VPN vs 유료 VPN 비교</h2>
<p>무료 VPN을 선택하기 전에 유료와의 차이점을 명확히 알아야 합니다.</p>
<table><thead><tr><th>항목</th><th>무료 VPN</th><th>유료 VPN</th></tr></thead><tbody>
<tr><td>데이터 한도</td><td>월 2~10GB 제한</td><td>무제한</td></tr>
<tr><td>서버 수</td><td>소수 (5~30개국)</td><td>다수 (60~100개국+)</td></tr>
<tr><td>속도</td><td>느림 (혼잡)</td><td>빠름 (전용 대역폭)</td></tr>
<tr><td>광고</td><td>있음</td><td>없음</td></tr>
<tr><td>동시 기기 수</td><td>1~5대</td><td>5~10대</td></tr>
<tr><td>고객 지원</td><td>제한적</td><td>24시간 지원</td></tr>
<tr><td>월 비용</td><td>무료</td><td>약 4,000~15,000원</td></tr>
</tbody></table>

{cta_block("ProtonVPN 무료 플랜 시작하기", "데이터 무제한 무료 VPN, ProtonVPN에서 지금 바로 시작하세요", "https://protonvpn.com/", "blue")}

{imgs[1]}

<h2>무료 VPN TOP 5 상세 비교</h2>

<h3>1. ProtonVPN (프로톤VPN) - 데이터 무제한</h3>
<p>스위스 프라이버시 법을 기반으로 한 ProtonVPN은 <strong>무료 플랜에서도 데이터 무제한</strong>을 제공하는 거의 유일한 서비스입니다. 속도는 유료보다 느리지만, 로그를 남기지 않는 엄격한 노로그 정책이 강점입니다.</p>
<ul>
<li><strong>데이터 한도</strong>: 무제한</li>
<li><strong>무료 서버</strong>: 미국, 네덜란드, 일본 (3개국)</li>
<li><strong>속도</strong>: 보통 (무료 사용자 혼잡)</li>
<li><strong>장점</strong>: 완전 무제한, 노로그, 오픈소스</li>
<li><strong>단점</strong>: 무료 서버가 3개국뿐, P2P 미지원</li>
</ul>

<h3>2. Windscribe (윈드스크라이브) - 월 10GB</h3>
<p>월 10GB 무료 데이터와 11개국 서버를 제공합니다. 이메일 인증 시 추가 5GB를 받을 수 있고, 트위터 공유로 추가 데이터도 확보 가능합니다.</p>
<ul>
<li><strong>데이터 한도</strong>: 월 10GB (이메일 인증 시 15GB)</li>
<li><strong>무료 서버</strong>: 11개국</li>
<li><strong>속도</strong>: 양호</li>
<li><strong>장점</strong>: 광고 차단 기능 포함, 서버 수 많음</li>
<li><strong>단점</strong>: 데이터 한도 초과 시 사용 불가</li>
</ul>

<h3>3. Atlas VPN - 월 5GB</h3>
<p>심플한 인터페이스와 빠른 속도로 인기 있는 VPN입니다. 무료 플랜도 광고 없이 사용할 수 있습니다.</p>
<ul>
<li><strong>데이터 한도</strong>: 월 5GB</li>
<li><strong>무료 서버</strong>: 미국, 네덜란드 (2개국)</li>
<li><strong>속도</strong>: 빠름</li>
<li><strong>장점</strong>: 광고 없음, 빠른 속도</li>
<li><strong>단점</strong>: 데이터 5GB 제한, 서버 2개국</li>
</ul>

<h3>4. Hide.me - 월 10GB</h3>
<p>말레이시아 기반으로 엄격한 노로그 정책을 유지하는 VPN입니다. 무료 플랜에서도 5개 서버 위치를 제공합니다.</p>
<ul>
<li><strong>데이터 한도</strong>: 월 10GB</li>
<li><strong>무료 서버</strong>: 5개 위치</li>
<li><strong>속도</strong>: 양호</li>
<li><strong>장점</strong>: 엄격한 노로그, 빠른 속도</li>
<li><strong>단점</strong>: 동시 접속 1기기 제한</li>
</ul>

<h3>5. TunnelBear - 월 500MB</h3>
<p>귀여운 곰 캐릭터로 유명한 TunnelBear는 사용법이 직관적이어서 VPN 처음 사용자에게 적합합니다. 다만 무료 데이터가 500MB로 매우 적습니다.</p>
<ul>
<li><strong>데이터 한도</strong>: 월 500MB (트윗 공유 시 1GB 추가)</li>
<li><strong>무료 서버</strong>: 47개국</li>
<li><strong>속도</strong>: 빠름</li>
<li><strong>장점</strong>: 직관적인 UI, 다양한 서버</li>
<li><strong>단점</strong>: 데이터 500MB는 너무 적음</li>
</ul>

<table><thead><tr><th>VPN</th><th>데이터 한도</th><th>서버 수</th><th>속도</th><th>노로그</th><th>추천 대상</th></tr></thead><tbody>
<tr><td>ProtonVPN</td><td>무제한</td><td>3개국</td><td>보통</td><td>엄격</td><td>장기 사용자</td></tr>
<tr><td>Windscribe</td><td>월 10~15GB</td><td>11개국</td><td>양호</td><td>있음</td><td>일반 사용자</td></tr>
<tr><td>Atlas VPN</td><td>월 5GB</td><td>2개국</td><td>빠름</td><td>있음</td><td>가끔 사용자</td></tr>
<tr><td>Hide.me</td><td>월 10GB</td><td>5개 위치</td><td>양호</td><td>엄격</td><td>보안 중시</td></tr>
<tr><td>TunnelBear</td><td>월 500MB</td><td>47개국</td><td>빠름</td><td>있음</td><td>VPN 입문자</td></tr>
</tbody></table>

{imgs[2]}

<h2>VPN 선택 기준</h2>
<p>무료 VPN을 고를 때는 단순히 데이터 한도만 볼 게 아니라 아래 기준을 종합적으로 고려해야 합니다.</p>
<ol>
<li><strong>노로그 정책(No-Log Policy)</strong>: 사용 기록을 저장하지 않는지 확인. 개인정보 보호의 핵심입니다</li>
<li><strong>암호화 수준</strong>: AES-256 암호화를 지원하는지 확인</li>
<li><strong>킬 스위치(Kill Switch)</strong>: VPN 연결이 끊겼을 때 인터넷도 자동 차단하는 기능</li>
<li><strong>DNS 누출 방지</strong>: 실제 DNS 쿼리가 외부로 노출되지 않는지 확인</li>
<li><strong>본사 국가</strong>: 미국, 영국, 호주, 캐나다(Five Eyes) 소속 업체는 정보 공유 의무가 있음</li>
</ol>

<h2>무료 VPN 사용 시 보안 주의사항</h2>
<ul>
<li><strong>광고 기반 무료 VPN 주의</strong>: 일부 무료 VPN은 사용자 데이터를 광고주에 판매합니다</li>
<li><strong>앱스토어 외 출처 설치 금지</strong>: 공식 스토어 이외에서 설치한 VPN 앱은 악성코드 위험</li>
<li><strong>은행/금융 거래 시 VPN 해제</strong>: 일부 금융기관은 VPN 사용 시 접속을 차단할 수 있습니다</li>
<li><strong>무료 VPN으로 토렌트 금지</strong>: 대부분의 무료 VPN은 P2P를 막고, 적발 시 계정 삭제</li>
</ul>

{cta_block("ProtonVPN 무료로 시작하기", "데이터 무제한 무료 VPN, 지금 바로 다운로드하세요", "https://protonvpn.com/", "green")}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. VPN을 쓰면 인터넷이 느려지나요?</h3>
<p>A. 암호화와 우회 과정으로 속도가 일부 저하됩니다. 유료 VPN은 5~20% 정도 저하되지만, <strong>무료 VPN은 서버 혼잡으로 30~50% 이상 느려질 수 있습니다.</strong></p>
<h3>Q. 한국에서 VPN 사용이 불법인가요?</h3>
<p>A. 개인 사용은 불법이 아닙니다. 다만 저작권법을 위반하거나 불법 콘텐츠에 접근하는 데 VPN을 사용하는 것은 별도로 처벌 대상이 됩니다.</p>
<h3>Q. 무료 VPN도 유료처럼 안전한가요?</h3>
<p>A. ProtonVPN처럼 검증된 오픈소스 무료 VPN은 비교적 안전합니다. 그러나 출처 불명의 무료 VPN은 <strong>개인정보를 수집해 판매하는 경우가 있어 위험합니다.</strong></p>
<h3>Q. 스마트폰에서도 VPN을 쓸 수 있나요?</h3>
<p>A. 네, iOS와 안드로이드 모두 공식 앱을 제공합니다. 각 앱스토어에서 공식 앱을 다운로드하여 사용하세요.</p>

<h2>마무리</h2>
<p>무료 VPN 중 가장 추천하는 서비스는 <strong>ProtonVPN(데이터 무제한, 보안 우수)</strong>과 <strong>Windscribe(월 10~15GB, 서버 다양)</strong>입니다. 사용 목적이 가끔 해외 콘텐츠 이용이라면 무료로도 충분하지만, 업무나 민감한 데이터를 다룬다면 유료 VPN 투자를 고려해보세요.</p>'''
    },

    # 3. 아이폰 안드로이드 데이터 이동
    {
        "title": "아이폰 안드로이드 데이터 이동 방법 기종변경 총정리",
        "cat": 5,
        "slug": "iphone-android-data-transfer-guide",
        "images": [
            ("photo-1512941937669-90a1b58e7e9c", "스마트폰 데이터 이동 방법"),
            ("photo-1611532736597-de2d4265fba3", "아이폰 안드로이드 데이터 전송"),
            ("photo-1530319067432-f2a729c03db5", "폰 기종변경 데이터 백업"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">새 스마트폰으로 기종을 바꿀 때 가장 걱정되는 것이 바로 <strong>데이터 이동</strong>입니다. 특히 안드로이드에서 아이폰으로, 또는 아이폰에서 안드로이드로 OS를 바꿀 때는 방법이 달라 헷갈립니다. 연락처, 사진, 카카오톡까지 빠짐없이 옮기는 <strong>완벽한 기종변경 데이터 이동 가이드</strong>를 정리합니다.</p>

{imgs[0]}

<h2>이동 방법 한눈에 비교</h2>
<table><thead><tr><th>이동 경로</th><th>공식 앱/방법</th><th>소요 시간</th><th>난이도</th></tr></thead><tbody>
<tr><td>안드로이드 → 아이폰</td><td>Move to iOS</td><td>20~60분</td><td>쉬움</td></tr>
<tr><td>아이폰 → 삼성 안드로이드</td><td>Samsung Smart Switch</td><td>20~60분</td><td>쉬움</td></tr>
<tr><td>아이폰 → 일반 안드로이드</td><td>Google Drive 백업</td><td>30~90분</td><td>보통</td></tr>
<tr><td>연락처만 이동</td><td>vCard / Google 연락처</td><td>5~10분</td><td>쉬움</td></tr>
<tr><td>사진만 이동</td><td>Google 포토 / iCloud</td><td>데이터 크기에 따라</td><td>쉬움</td></tr>
</tbody></table>

<h2>안드로이드 → 아이폰: Move to iOS 앱 사용법</h2>
<p>Apple이 공식 제공하는 <strong>Move to iOS</strong> 앱을 사용하면 와이파이 없이도 두 기기 간 직접 데이터를 전송할 수 있습니다.</p>
<h3>이동 가능한 데이터</h3>
<ul>
<li>연락처, 메시지 기록</li>
<li>사진 및 동영상</li>
<li>웹 북마크 (크롬 → 사파리)</li>
<li>메일 계정, 캘린더</li>
<li>무료 앱 (동일 앱이 앱스토어에 있을 경우)</li>
</ul>
<h3>단계별 이동 방법</h3>
<ol>
<li>안드로이드에서 <strong>Play 스토어</strong>에서 'Move to iOS' 앱 설치</li>
<li>새 아이폰을 켜고 <strong>앱 및 데이터 화면</strong>에서 'Android에서 데이터 이동' 선택</li>
<li>아이폰에 표시된 <strong>10자리 코드</strong>를 안드로이드 앱에 입력</li>
<li>두 기기가 임시 Wi-Fi로 연결됨 (기존 Wi-Fi 연결이 끊어지는 것은 정상)</li>
<li>이동할 데이터 항목 선택 후 <strong>[계속]</strong> 터치</li>
<li>전송 완료 후 아이폰 설정 계속 진행</li>
</ol>
<p><strong>주의:</strong> 아이폰을 새 기기로 처음 설정하는 단계에서만 사용 가능합니다. 이미 설정이 완료된 아이폰에는 적용할 수 없습니다.</p>

{cta_block("애플 공식 지원 페이지에서 자세히 알아보기", "Move to iOS 앱 사용법과 주의사항을 애플 공식 사이트에서 확인하세요", "https://support.apple.com/ko-kr/", "blue")}

{imgs[1]}

<h2>아이폰 → 삼성 안드로이드: Smart Switch</h2>
<p>삼성 갤럭시로 기종 변경 시에는 <strong>Samsung Smart Switch</strong>가 가장 편리합니다. 케이블 연결 또는 와이파이로 데이터를 옮길 수 있습니다.</p>
<h3>이동 가능한 데이터</h3>
<ul>
<li>연락처, 메시지, 통화 기록</li>
<li>사진, 동영상, 음악</li>
<li>캘린더, 메모</li>
<li>앱 목록 (안드로이드 동일 앱 자동 설치 제안)</li>
<li>Wi-Fi 비밀번호</li>
</ul>
<h3>케이블 이동 방법 (권장)</h3>
<ol>
<li>새 갤럭시에서 <strong>Smart Switch</strong> 앱 실행 (기본 설치)</li>
<li>USB-C to Lightning 케이블로 두 기기 연결</li>
<li>아이폰에서 <strong>[신뢰]</strong> 선택</li>
<li>이동할 데이터 선택 후 <strong>[전송]</strong></li>
<li>전송 완료 후 갤럭시에서 데이터 확인</li>
</ol>

<h2>아이폰 → 일반 안드로이드: Google Drive 백업</h2>
<p>삼성이 아닌 안드로이드 기기로 이동할 때는 Google Drive를 활용합니다.</p>
<h3>연락처 이동</h3>
<ol>
<li>아이폰에서 <strong>설정 → [이름] → iCloud → 연락처</strong> 켜기</li>
<li><strong>iCloud.com</strong> 접속 → 연락처 → vCard 내보내기</li>
<li>안드로이드에서 Google 연락처 앱 → vCard 가져오기</li>
</ol>
<h3>사진/동영상 이동</h3>
<ol>
<li>아이폰에 <strong>Google 포토</strong> 앱 설치 후 전체 사진 백업</li>
<li>안드로이드에서 같은 구글 계정으로 Google 포토 로그인</li>
<li>자동으로 모든 사진 동기화</li>
</ol>

<h2>카카오톡 백업 및 이동 방법</h2>
<p>카카오톡 대화 내용은 일반 데이터 이동 앱으로는 옮겨지지 않습니다. 별도로 <strong>카카오톡 채팅 백업</strong>을 해야 합니다.</p>
<table><thead><tr><th>이동 경로</th><th>대화 내용</th><th>사진/파일</th><th>방법</th></tr></thead><tbody>
<tr><td>안드로이드 → 아이폰</td><td>이동 불가</td><td>이동 불가</td><td>새로 시작해야 함</td></tr>
<tr><td>아이폰 → 안드로이드</td><td>이동 불가</td><td>이동 불가</td><td>새로 시작해야 함</td></tr>
<tr><td>안드로이드 → 안드로이드</td><td>가능</td><td>가능</td><td>카카오계정 백업/복원</td></tr>
<tr><td>아이폰 → 아이폰</td><td>가능</td><td>가능</td><td>iCloud 백업</td></tr>
</tbody></table>
<p>iOS ↔ 안드로이드 간 카카오톡 대화 내용 이동은 현재 <strong>공식적으로 지원되지 않습니다.</strong> 중요한 대화는 텍스트 파일로 내보내기 하여 보관하세요.</p>
<h3>카카오톡 대화 텍스트 내보내기</h3>
<ol>
<li>채팅방 → 우측 상단 ≡ 메뉴</li>
<li><strong>[대화 내용 내보내기]</strong> 선택</li>
<li>이메일 또는 다른 앱으로 저장</li>
</ol>

{imgs[2]}

<h2>데이터 이동 전 준비사항 및 주의사항</h2>
<ul>
<li><strong>충분한 배터리 확보</strong>: 두 기기 모두 최소 50% 이상 충전 후 진행</li>
<li><strong>기존 기기 백업 먼저</strong>: 이동 전 iCloud 또는 구글 드라이브 백업 필수</li>
<li><strong>스토리지 여유 공간 확인</strong>: 새 기기에 충분한 여유 공간 필요</li>
<li><strong>앱 재다운로드 필요</strong>: 앱 자체는 이동이 안 되므로 새로 설치해야 함</li>
<li><strong>게임 데이터 별도 확인</strong>: 각 게임사의 계정 연동 기능 활용</li>
<li><strong>은행 앱 재인증 필요</strong>: 보안 정책으로 새 기기에서 재인증 필수</li>
</ul>

{cta_block("삼성 Smart Switch 다운로드", "삼성 갤럭시로 기종 변경 시 Smart Switch로 간편하게 이동하세요", "https://support.apple.com/ko-kr/", "yellow")}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. Move to iOS를 쓰면 모든 앱이 아이폰으로 옮겨지나요?</h3>
<p>A. 앱 자체는 이동되지 않습니다. 다만 안드로이드에 설치된 앱 목록 중 <strong>앱스토어에 동일 앱이 있으면 자동으로 설치를 제안</strong>합니다. 유료 앱은 아이폰에서 다시 구매해야 합니다.</p>
<h3>Q. 사진이 너무 많아서 전송이 오래 걸리는데 방법이 없나요?</h3>
<p>A. Google 포토를 활용하면 Wi-Fi 연결 상태에서 백그라운드로 업로드/다운로드되므로 케이블 연결 없이 편리합니다. <strong>15GB 이하면 무료</strong>로 이용 가능합니다.</p>
<h3>Q. 기존 폰의 문자 메시지도 이동할 수 있나요?</h3>
<p>A. Move to iOS와 Smart Switch 모두 SMS 이동을 지원하지만, <strong>이동 경로(안드로이드↔아이폰)에 따라 일부 메시지는 제외</strong>될 수 있습니다.</p>
<h3>Q. 데이터 이동 중 전화가 오면 어떻게 되나요?</h3>
<p>A. 전송 중에는 가능하면 <strong>비행기 모드</strong>를 켜두는 것이 좋습니다. 전화 수신 시 전송이 중단될 수 있습니다.</p>

<h2>마무리</h2>
<p>스마트폰 기종 변경 시 데이터 이동은 미리 준비하면 어렵지 않습니다. 안드로이드 → 아이폰은 <strong>Move to iOS</strong>, 아이폰 → 삼성은 <strong>Smart Switch</strong>가 가장 편리합니다. 카카오톡 대화 내용은 OS 변경 시 이동이 불가하니 미리 텍스트로 내보내기 해두세요.</p>'''
    },

    # 4. 챗GPT 클로드 AI 활용법
    {
        "title": "챗GPT 클로드 AI 활용법 업무 생산성 높이는 프롬프트 작성법 총정리",
        "cat": 5,
        "slug": "chatgpt-claude-ai-prompt-productivity-guide",
        "images": [
            ("photo-1677442136019-21780ecad995", "챗GPT 클로드 AI 활용법"),
            ("photo-1519389950473-47ba0277781c", "AI 프롬프트 작성 가이드"),
            ("photo-1517694712202-14dd9538aa97", "업무 생산성 AI 도구"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">ChatGPT와 Claude는 현재 가장 많이 쓰이는 AI 어시스턴트입니다. 단순히 질문에 대답하는 수준을 넘어, 이메일 작성, 보고서 요약, 코딩, 번역까지 <strong>업무 전반의 생산성을 혁신적으로 높여줍니다.</strong> 두 AI의 특징을 비교하고, 실무에서 바로 쓸 수 있는 <strong>프롬프트 작성법과 템플릿 10가지</strong>를 소개합니다.</p>

{imgs[0]}

<h2>챗GPT vs 클로드 기본 비교</h2>
<table><thead><tr><th>항목</th><th>ChatGPT (GPT-4o)</th><th>Claude (Claude 3.5)</th></tr></thead><tbody>
<tr><td>개발사</td><td>OpenAI (미국)</td><td>Anthropic (미국)</td></tr>
<tr><td>무료 플랜</td><td>GPT-4o mini (제한)</td><td>Claude 3 Haiku (제한)</td></tr>
<tr><td>유료 플랜</td><td>월 $20 (Plus)</td><td>월 $20 (Pro)</td></tr>
<tr><td>컨텍스트 길이</td><td>최대 128K 토큰</td><td>최대 200K 토큰</td></tr>
<tr><td>강점</td><td>이미지 생성, 플러그인, 광범위한 생태계</td><td>긴 문서 분석, 자연스러운 한국어, 안전성</td></tr>
<tr><td>약점</td><td>긴 문서 처리 한계</td><td>이미지 생성 불가</td></tr>
<tr><td>한국어 품질</td><td>우수</td><td>매우 우수</td></tr>
<tr><td>인터넷 검색</td><td>가능 (유료)</td><td>가능 (일부)</td></tr>
</tbody></table>

<h2>프롬프트 작성의 기본 원칙 4가지</h2>
<p>AI에서 좋은 결과를 얻으려면 <strong>프롬프트(명령어)의 품질</strong>이 핵심입니다. 막연한 질문보다 구체적인 프롬프트가 훨씬 좋은 결과를 만들어냅니다.</p>
<ol>
<li><strong>역할 부여</strong>: "당신은 10년 경력의 마케터입니다"처럼 AI에게 역할을 먼저 부여하세요</li>
<li><strong>맥락 제공</strong>: 배경 정보, 대상 독자, 목적을 구체적으로 설명하세요</li>
<li><strong>출력 형식 지정</strong>: "표로 정리해줘", "3단락으로 작성해줘"처럼 형식을 명확히 하세요</li>
<li><strong>예시 포함</strong>: 원하는 결과의 예시를 보여주면 AI가 방향을 잡기 쉽습니다</li>
</ol>

{cta_block("ChatGPT 시작하기", "OpenAI ChatGPT 무료 계정으로 지금 바로 시작해보세요", "https://chat.openai.com/", "blue")}

{imgs[1]}

<h2>업무별 활용법 및 프롬프트 템플릿 10가지</h2>

<h3>1. 이메일 작성</h3>
<p>비즈니스 이메일은 AI가 가장 잘 도와주는 영역입니다. 어투, 길이, 목적을 지정하면 바로 사용 가능한 초안을 만들어줍니다.</p>
<p><strong>프롬프트 예시:</strong></p>
<p style="background:#f8f9fa;padding:16px;border-left:4px solid #4f46e5;border-radius:4px;font-family:monospace;">당신은 비즈니스 커뮤니케이션 전문가입니다. 다음 상황에 맞는 정중하고 간결한 이메일을 작성해주세요. [상황: 미팅 일정 변경 요청 / 수신자: 클라이언트 / 어투: 정중하고 전문적 / 길이: 3단락 이내]</p>

<h3>2. 보고서 요약</h3>
<p>긴 문서를 빠르게 요약하는 데 Claude가 특히 강합니다. 200K 토큰 컨텍스트로 긴 PDF나 문서도 처리 가능합니다.</p>
<p><strong>프롬프트 예시:</strong></p>
<p style="background:#f8f9fa;padding:16px;border-left:4px solid #4f46e5;border-radius:4px;font-family:monospace;">다음 보고서를 [핵심 주제 / 주요 수치 / 결론 / 액션 아이템] 4가지 항목으로 나눠 불릿 포인트로 요약해주세요. 각 항목은 3줄 이내로 작성하세요. [보고서 내용 붙여넣기]</p>

<h3>3. 코딩 도움</h3>
<p>코드 작성, 디버깅, 리뷰까지 모두 가능합니다. 사용 언어와 환경을 명시하면 더 정확한 코드를 받을 수 있습니다.</p>
<p><strong>프롬프트 예시:</strong></p>
<p style="background:#f8f9fa;padding:16px;border-left:4px solid #4f46e5;border-radius:4px;font-family:monospace;">Python 3.11 환경에서 [기능 설명]을 구현하는 코드를 작성해주세요. 주석을 한국어로 달고, 에러 처리도 포함해주세요.</p>

<h3>4. 번역 및 현지화</h3>
<p>단순 번역을 넘어 현지 문화에 맞는 표현으로 변환해줍니다.</p>
<p><strong>프롬프트 예시:</strong></p>
<p style="background:#f8f9fa;padding:16px;border-left:4px solid #4f46e5;border-radius:4px;font-family:monospace;">다음 한국어 텍스트를 영어로 번역해주세요. 직역이 아닌 자연스러운 영어 표현을 사용하고, 비즈니스 공식 문서 스타일로 작성하세요. [텍스트 붙여넣기]</p>

<h3>5. 데이터 분석 및 인사이트</h3>
<p>엑셀 데이터나 숫자 표를 붙여넣으면 패턴과 인사이트를 뽑아줍니다.</p>
<p><strong>프롬프트 예시:</strong></p>
<p style="background:#f8f9fa;padding:16px;border-left:4px solid #4f46e5;border-radius:4px;font-family:monospace;">아래 월별 매출 데이터를 분석하여 (1) 주요 트렌드 (2) 이상치 (3) 다음 달 예측 (4) 개선 제안을 각각 2~3줄로 정리해주세요. [데이터 붙여넣기]</p>

<h3>6. 아이디어 브레인스토밍</h3>
<p><strong>프롬프트 예시:</strong></p>
<p style="background:#f8f9fa;padding:16px;border-left:4px solid #4f46e5;border-radius:4px;font-family:monospace;">우리 팀의 [제품/서비스] 마케팅을 위한 아이디어를 10가지 제안해주세요. 각 아이디어는 실행 비용(저/중/고), 예상 효과(저/중/고), 실행 기간을 함께 표로 정리해주세요.</p>

<h3>7. SNS 게시물 작성</h3>
<p><strong>프롬프트 예시:</strong></p>
<p style="background:#f8f9fa;padding:16px;border-left:4px solid #4f46e5;border-radius:4px;font-family:monospace;">[제품명]의 [특징]을 강조하는 인스타그램 게시물을 작성해주세요. 이모지 포함, 300자 이내, 해시태그 10개도 추가해주세요. 타깃: 20~30대 직장인 여성.</p>

<h3>8. 면접 준비</h3>
<p><strong>프롬프트 예시:</strong></p>
<p style="background:#f8f9fa;padding:16px;border-left:4px solid #4f46e5;border-radius:4px;font-family:monospace;">[직무명] 면접관 역할을 해주세요. 자주 나오는 압박 질문 5가지와 STAR 기법을 활용한 모범 답변 예시를 작성해주세요. 내 경력: [경력 내용 입력]</p>

<h3>9. 계약서 / 법률 문서 검토</h3>
<p><strong>프롬프트 예시:</strong></p>
<p style="background:#f8f9fa;padding:16px;border-left:4px solid #4f46e5;border-radius:4px;font-family:monospace;">다음 계약서 조항을 검토하고 (1) 불리한 조항 (2) 불명확한 조항 (3) 협상 포인트를 각각 표로 정리해주세요. 단, 법적 조언이 아닌 일반적인 분석입니다. [계약서 내용]</p>

<h3>10. 학습 계획 수립</h3>
<p><strong>프롬프트 예시:</strong></p>
<p style="background:#f8f9fa;padding:16px;border-left:4px solid #4f46e5;border-radius:4px;font-family:monospace;">[목표 기술/자격증]을 [기간] 안에 취득하고 싶습니다. 현재 수준: [초급/중급]. 주당 [N]시간 공부 가능. 주차별 학습 계획을 표로 만들어주세요.</p>

{imgs[2]}

<h2>무료 vs 유료 플랜 비교</h2>
<table><thead><tr><th>항목</th><th>무료 플랜</th><th>유료 플랜 ($20/월)</th></tr></thead><tbody>
<tr><td>모델 품질</td><td>기본 모델</td><td>최상위 모델</td></tr>
<tr><td>사용 제한</td><td>시간당 제한</td><td>훨씬 높은 한도</td></tr>
<tr><td>파일 업로드</td><td>제한적</td><td>대용량 지원</td></tr>
<tr><td>이미지 생성 (GPT)</td><td>불가</td><td>가능 (DALL-E 3)</td></tr>
<tr><td>인터넷 검색</td><td>제한</td><td>실시간 검색</td></tr>
<tr><td>API 접근</td><td>불가</td><td>별도 API 플랜</td></tr>
</tbody></table>

{cta_block("Claude AI 시작하기", "Anthropic Claude AI로 한국어 글쓰기와 문서 분석을 경험해보세요", "https://claude.ai/", "green")}

<h2>AI 사용 시 주의사항</h2>
<ul>
<li><strong>할루시네이션 주의</strong>: AI는 틀린 정보를 자신있게 말할 수 있습니다. 중요 사실은 반드시 검증하세요</li>
<li><strong>개인정보 입력 금지</strong>: 주민번호, 계좌번호, 비밀번호 등은 절대 입력하지 마세요</li>
<li><strong>저작권 확인</strong>: AI 생성 콘텐츠의 저작권 귀속은 아직 법적으로 불명확한 영역입니다</li>
<li><strong>회사 기밀 주의</strong>: 기업 내부 데이터를 외부 AI 서비스에 입력하면 정보 유출 위험이 있습니다</li>
</ul>

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. ChatGPT와 Claude 중 어떤 것이 더 좋나요?</h3>
<p>A. 목적에 따라 다릅니다. <strong>이미지 생성이나 다양한 플러그인</strong>이 필요하면 ChatGPT, <strong>긴 문서 분석과 자연스러운 한국어</strong>가 필요하면 Claude가 유리합니다.</p>
<h3>Q. 프롬프트를 어떻게 작성해야 AI가 더 잘 이해할까요?</h3>
<p>A. 역할, 맥락, 형식, 제약 조건을 명확히 적어주세요. "~해줘"보다 "당신은 전문가입니다. [맥락]을 고려해 [형식]으로 작성해주세요"처럼 구체적일수록 좋습니다.</p>
<h3>Q. AI가 쓴 글을 그대로 제출해도 되나요?</h3>
<p>A. 학교 과제, 논문 등에서는 AI 사용 규정을 반드시 확인하세요. 직장에서도 <strong>AI 초안을 바탕으로 본인이 검토하고 수정하는 방식</strong>을 권장합니다.</p>
<h3>Q. 무료 플랜만으로도 업무에 충분히 활용할 수 있나요?</h3>
<p>A. 가벼운 업무에는 무료로 충분합니다. 단, 하루 사용량 제한이 있어 집중적으로 사용하는 분이라면 유료 플랜이 효율적입니다.</p>

<h2>마무리</h2>
<p>ChatGPT와 Claude는 잘 활용하면 하루 1~2시간의 업무 시간을 절약해주는 강력한 도구입니다. 오늘 소개한 프롬프트 템플릿을 그대로 복사해서 바로 사용해보세요. AI를 잘 다루는 능력, <strong>프롬프트 엔지니어링</strong>이 앞으로의 핵심 업무 역량이 될 것입니다.</p>'''
    },

    # 5. 컴퓨터 조립 견적 가이드
    {
        "title": "컴퓨터 조립 견적 가이드 용도별 부품 선택법 총정리",
        "cat": 5,
        "slug": "pc-build-guide-parts-selection",
        "images": [
            ("photo-1555255707-c07966088b7b", "컴퓨터 조립 부품 선택"),
            ("photo-1550751827-4bd374c3f58b", "PC 조립 견적 가이드"),
            ("photo-1531297484001-80022131f5a1", "컴퓨터 부품 추천"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">처음 컴퓨터를 조립하려는 분들이 가장 어려워하는 부분이 <strong>부품 선택과 예산 배분</strong>입니다. CPU, GPU, RAM, SSD, 파워, 케이스 각각 무엇을 골라야 할지 막막하죠. 이 글에서는 <strong>사무용, 게이밍, 고사양 작업용</strong> 3가지 용도별 견적과 부품 선택 기준을 완벽하게 정리합니다.</p>

{imgs[0]}

<h2>PC 주요 부품별 역할과 선택 기준</h2>

<h3>CPU (중앙처리장치)</h3>
<p>컴퓨터의 두뇌 역할. 멀티태스킹, 영상 편집, 코딩 성능에 직결됩니다.</p>
<ul>
<li><strong>인텔 vs AMD</strong>: 인텔 코어 i5/i7/i9, AMD 라이젠 5/7/9 시리즈가 주류</li>
<li><strong>선택 기준</strong>: 코어 수(멀티태스킹), 클럭 속도(단일 작업), 내장 그래픽(GPU 없을 때)</li>
<li><strong>소켓 확인 필수</strong>: CPU와 마더보드의 소켓 규격이 일치해야 합니다 (LGA1700, AM5 등)</li>
</ul>

<h3>GPU (그래픽카드)</h3>
<p>게임, 영상 편집, AI 작업의 핵심 부품. 예산의 큰 부분을 차지합니다.</p>
<ul>
<li><strong>NVIDIA vs AMD</strong>: NVIDIA RTX 시리즈(게임+AI), AMD RX 시리즈(가성비)</li>
<li><strong>VRAM 용량</strong>: 게임 최소 8GB, AI/영상 편집은 12GB 이상 권장</li>
<li><strong>사무용이라면</strong>: CPU 내장 그래픽으로 충분, GPU 불필요</li>
</ul>

<h3>RAM (메모리)</h3>
<p>동시에 처리할 수 있는 작업량을 결정합니다.</p>
<ul>
<li><strong>용량</strong>: 사무용 16GB, 게이밍 16~32GB, 영상 편집 32~64GB</li>
<li><strong>규격 확인</strong>: DDR5 (최신), DDR4 (이전 세대) - 마더보드 지원 확인 필수</li>
<li><strong>듀얼 채널</strong>: 같은 용량의 RAM 2개를 꽂으면 성능이 크게 향상됩니다</li>
</ul>

<h3>SSD (저장장치)</h3>
<p>부팅 속도와 프로그램 로딩 속도를 결정합니다.</p>
<ul>
<li><strong>NVMe M.2</strong>: 가장 빠른 규격, 최신 PC 표준 (읽기 속도 3,000~7,000MB/s)</li>
<li><strong>SATA SSD</strong>: NVMe보다 느리지만 가성비 우수 (읽기 속도 약 550MB/s)</li>
<li><strong>용량</strong>: 운영체제용 최소 512GB, 일반 사용 1TB, 게이밍/작업용 2TB</li>
</ul>

<h3>파워서플라이 (PSU)</h3>
<p>모든 부품에 안정적으로 전력을 공급하는 핵심 부품. 절약하면 안 됩니다.</p>
<ul>
<li><strong>80PLUS 인증</strong>: Bronze / Silver / Gold / Platinum - Gold 이상 권장</li>
<li><strong>용량 계산</strong>: PC 총 소비전력 × 1.2배 여유 용량 확보</li>
<li><strong>브랜드</strong>: 시소닉, 커세어, EVGA, 마이크로닉스 등 검증된 브랜드 사용</li>
</ul>

<h3>케이스와 쿨러</h3>
<ul>
<li><strong>케이스 폼팩터</strong>: 풀타워 / 미들타워 / 미니ITX - 마더보드 크기에 맞게 선택</li>
<li><strong>CPU 쿨러</strong>: 저발열 CPU는 기본 쿨러, 고성능 CPU는 타워형 쿨러 또는 수냉 쿨러</li>
<li><strong>에어플로우</strong>: 전면 흡기 / 후면 + 상단 배기 구성이 기본</li>
</ul>

{cta_block("다나와에서 부품 가격 비교하기", "최저가 PC 부품 가격을 다나와에서 실시간으로 비교해보세요", "https://www.danawa.com/", "blue")}

{imgs[1]}

<h2>용도별 PC 견적표 3가지</h2>

<h3>1. 사무용 PC (예산 약 50만원)</h3>
<p>문서 작업, 웹 서핑, 영상 시청 등 일반 사무 업무에 적합합니다.</p>
<table><thead><tr><th>부품</th><th>추천 제품</th><th>가격 (예시)</th></tr></thead><tbody>
<tr><td>CPU</td><td>Intel Core i5-13400 (내장그래픽)</td><td>약 17만원</td></tr>
<tr><td>마더보드</td><td>B760M 마이크로ATX</td><td>약 8만원</td></tr>
<tr><td>RAM</td><td>DDR4 16GB (8GB×2)</td><td>약 4만원</td></tr>
<tr><td>SSD</td><td>NVMe 512GB</td><td>약 5만원</td></tr>
<tr><td>파워</td><td>500W 80Plus Bronze</td><td>약 5만원</td></tr>
<tr><td>케이스</td><td>마이크로ATX 미니타워</td><td>약 4만원</td></tr>
<tr><td><strong>합계</strong></td><td></td><td><strong>약 43~50만원</strong></td></tr>
</tbody></table>

<h3>2. 게이밍 PC (예산 약 100만원)</h3>
<p>FHD~QHD 해상도에서 대부분의 최신 게임을 높은 설정으로 즐길 수 있습니다.</p>
<table><thead><tr><th>부품</th><th>추천 제품</th><th>가격 (예시)</th></tr></thead><tbody>
<tr><td>CPU</td><td>Intel Core i5-13600K / AMD Ryzen 5 7600X</td><td>약 23만원</td></tr>
<tr><td>GPU</td><td>NVIDIA RTX 4060 / AMD RX 7600</td><td>약 35만원</td></tr>
<tr><td>마더보드</td><td>B760 / B650 ATX</td><td>약 12만원</td></tr>
<tr><td>RAM</td><td>DDR5 32GB (16GB×2)</td><td>약 8만원</td></tr>
<tr><td>SSD</td><td>NVMe 1TB</td><td>약 8만원</td></tr>
<tr><td>파워</td><td>650W 80Plus Gold</td><td>약 8만원</td></tr>
<tr><td>케이스+쿨러</td><td>미들타워 + 타워형 쿨러</td><td>약 8만원</td></tr>
<tr><td><strong>합계</strong></td><td></td><td><strong>약 100~110만원</strong></td></tr>
</tbody></table>

<h3>3. 고사양 작업용 PC (예산 약 200만원)</h3>
<p>4K 영상 편집, 3D 렌더링, AI 딥러닝 등 전문 작업에 적합합니다.</p>
<table><thead><tr><th>부품</th><th>추천 제품</th><th>가격 (예시)</th></tr></thead><tbody>
<tr><td>CPU</td><td>Intel Core i9-13900K / AMD Ryzen 9 7900X</td><td>약 45만원</td></tr>
<tr><td>GPU</td><td>NVIDIA RTX 4070 Ti / RTX 4080</td><td>약 85만원</td></tr>
<tr><td>마더보드</td><td>Z790 / X670E ATX</td><td>약 20만원</td></tr>
<tr><td>RAM</td><td>DDR5 64GB (32GB×2)</td><td>약 18만원</td></tr>
<tr><td>SSD</td><td>NVMe 2TB (Gen4)</td><td>약 15만원</td></tr>
<tr><td>파워</td><td>850W 80Plus Gold 모듈러</td><td>약 12만원</td></tr>
<tr><td>케이스+쿨러</td><td>풀타워 + 240mm 수냉 쿨러</td><td>약 15만원</td></tr>
<tr><td><strong>합계</strong></td><td></td><td><strong>약 200~210만원</strong></td></tr>
</tbody></table>

{imgs[2]}

<h2>부품 호환성 체크리스트</h2>
<p>부품을 구매하기 전에 반드시 아래 호환성을 확인하세요. 하나라도 맞지 않으면 PC가 켜지지 않을 수 있습니다.</p>
<ul>
<li><strong>CPU ↔ 마더보드</strong>: 소켓 규격 일치 (인텔 LGA1700 / AMD AM5 등)</li>
<li><strong>RAM ↔ 마더보드</strong>: DDR4 또는 DDR5 지원 여부, 최대 용량 확인</li>
<li><strong>SSD ↔ 마더보드</strong>: M.2 슬롯 개수 및 PCIe 버전 확인</li>
<li><strong>GPU ↔ 케이스</strong>: 그래픽카드 길이와 케이스 최대 지원 길이 비교</li>
<li><strong>CPU 쿨러 ↔ 케이스</strong>: 쿨러 높이와 케이스 최대 쿨러 높이 확인</li>
<li><strong>파워 ↔ GPU</strong>: GPU 권장 파워 용량 이상인지 확인</li>
</ul>
<p>PCPartPicker(pcpartpicker.com) 사이트를 이용하면 <strong>자동으로 호환성을 체크</strong>해줘서 편리합니다.</p>

<h2>조립 순서 (초보자 가이드)</h2>
<ol>
<li>마더보드에 CPU 장착 (핀 방향 주의)</li>
<li>CPU 쿨러 장착 및 써멀 컴파운드 도포</li>
<li>RAM 슬롯에 메모리 장착 (2번, 4번 슬롯 우선)</li>
<li>M.2 슬롯에 SSD 장착</li>
<li>케이스에 마더보드 고정</li>
<li>파워서플라이 케이스에 고정</li>
<li>GPU 장착</li>
<li>케이블 연결 (24핀 메인, 8핀 CPU, PCIe 전원)</li>
<li>케이스 팬 및 전면 패널 연결</li>
<li>첫 부팅 및 BIOS 진입 확인</li>
</ol>

{cta_block("다나와 견적 시뮬레이터 사용해보기", "원하는 부품을 담고 견적을 실시간으로 비교해보세요", "https://www.danawa.com/", "yellow")}

<h2>초보 실수 방지 팁</h2>
<ul>
<li><strong>정전기 주의</strong>: 부품을 만지기 전 금속에 손을 대거나 정전기 방지 밴드 착용</li>
<li><strong>CPU 핀 확인</strong>: AMD는 CPU에 핀, 인텔은 마더보드에 핀 - 절대 구부리지 마세요</li>
<li><strong>써멀 컴파운드</strong>: 쌀알 크기만 CPU 중앙에 올리면 충분합니다</li>
<li><strong>케이블 정리</strong>: 조립 전 케이블 라우팅 계획 후 진행하면 훨씬 깔끔합니다</li>
<li><strong>나사 조이기</strong>: 너무 강하게 조이면 마더보드가 휠 수 있습니다. 적당히 조이세요</li>
<li><strong>BIOS 업데이트</strong>: 새 부품 장착 후 첫 부팅 시 최신 BIOS로 업데이트 권장</li>
</ul>

<h2>추천 구매처 비교</h2>
<table><thead><tr><th>구매처</th><th>장점</th><th>단점</th><th>추천 상황</th></tr></thead><tbody>
<tr><td>다나와</td><td>최저가 비교, 다양한 리뷰</td><td>직접 비교해야 함</td><td>가격 우선 구매</td></tr>
<tr><td>네이버 쇼핑</td><td>편리한 비교, 포인트 적립</td><td>다나와보다 비쌀 수 있음</td><td>빠른 배송 필요</td></tr>
<tr><td>컴퓨존</td><td>조립 전문, 품질 보증</td><td>최저가보다 약간 높음</td><td>조립 의뢰</td></tr>
<tr><td>쿠팡</td><td>로켓배송, 반품 편리</td><td>부품 선택 폭 좁음</td><td>급할 때</td></tr>
</tbody></table>

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. PC 조립이 처음인데 혼자 할 수 있나요?</h3>
<p>A. 네, 가능합니다. 유튜브에 각 부품별 조립 영상이 많습니다. 특히 <strong>Linus Tech Tips, JayzTwoCents</strong> 채널 영상을 참고하면 도움이 됩니다. 국내는 '쩐민정' 채널 등이 한국어로 잘 설명합니다.</p>
<h3>Q. 조립 PC vs 브랜드 완제품, 어느 것이 더 나은가요?</h3>
<p>A. 같은 예산이라면 조립 PC가 성능이 더 높습니다. 브랜드 완제품은 <strong>AS와 편의성</strong>이 장점이고, 조립 PC는 <strong>가성비와 업그레이드 유연성</strong>이 장점입니다.</p>
<h3>Q. 중고 부품을 써도 괜찮나요?</h3>
<p>A. SSD, RAM, 케이스는 중고를 써도 비교적 안전합니다. 그러나 <strong>파워서플라이와 GPU는 가급적 새것을 사용</strong>하세요. 특히 중고 GPU는 채굴용으로 혹사된 경우가 있어 주의가 필요합니다.</p>
<h3>Q. 조립 완료 후 PC가 켜지지 않으면 어떻게 하나요?</h3>
<p>A. 가장 먼저 파워 케이블, 24핀 메인, 8핀 CPU 전원 연결을 재확인하세요. 그 다음 RAM을 하나씩 제거하며 테스트, CMOS 배터리 탈착 초기화 순으로 점검합니다.</p>

<h2>마무리</h2>
<p>컴퓨터 조립은 처음엔 어렵게 느껴지지만, 부품 역할을 이해하고 호환성만 잘 확인하면 누구나 할 수 있습니다. 사무용 50만원부터 시작해 필요에 따라 업그레이드하는 방식으로 접근하면 비용 부담도 줄일 수 있습니다. 다나와 견적 시뮬레이터로 먼저 원하는 조합을 만들어보고, 커뮤니티에서 피드백을 받아보세요.</p>'''
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

        # 2) 콘텐츠 생성 + auto_link 적용
        content = auto_link(post["content"](img_htmls))

        # 3) 발행
        payload = {
            "title": post["title"],
            "content": content,
            "status": "publish",
            "slug": post["slug"],
            "categories": [post["cat"]],
        }
        if first_media_id:
            payload["featured_media"] = first_media_id

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(API, data=data, method="POST")
        req.add_header("Authorization", f"Basic {AUTH}")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                r = json.loads(resp.read().decode())
                pid = r.get("id")
                link = r.get("link", "")
                print(f"  발행 OK | ID:{pid} | {link}")
                published.append(link)
        except Exception as e:
            print(f"  발행 FAIL | {e}")

        time.sleep(1)

    # 4) IndexNow 제출 (네이버/Bing/Yandex)
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

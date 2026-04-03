import json
import urllib.request
import urllib.error
import base64
import time
import ssl
import os
import tempfile

ssl._create_default_https_context = ssl._create_unverified_context

AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API = "https://devupbox.com/wp-json/wp/v2/posts"
MEDIA_API = "https://devupbox.com/wp-json/wp/v2/media"

CAT_INTERNET = 3

UPLOADED_IMAGES = {}

IMAGES = {
    "internet-plan-comparison": [
        ("photo-1544197150-b99a580bb7a8", "인터넷 요금제 비교"),
        ("photo-1451187580459-43490279c0fa", "인터넷 네트워크 연결"),
    ],
    "kt-sk-lg-internet-price": [
        ("photo-1558494949-ef010cbdcc31", "통신사별 인터넷 장비"),
        ("photo-1516321318423-f06f85e504b3", "인터넷 속도 비교"),
    ],
    "single-person-internet": [
        ("photo-1522202176988-66273c2fd55f", "1인 가구 인터넷 사용"),
        ("photo-1496181133206-80ce9b88a853", "노트북 인터넷 연결"),
    ],
    "student-cheap-internet": [
        ("photo-1517245386807-bb43f82c33c4", "자취생 인터넷 사용"),
        ("photo-1488590528505-98d2b5aba04b", "자취방 인터넷 환경"),
    ],
    "internet-speed-plan-comparison": [
        ("photo-1451187580459-43490279c0fa", "인터넷 속도 비교 분석"),
        ("photo-1558494949-ef010cbdcc31", "속도별 인터넷 장비"),
    ],
    "giga-internet-comparison": [
        ("photo-1606904825846-647eb07f5be2", "기가 인터넷 공유기"),
        ("photo-1544197150-b99a580bb7a8", "고속 인터넷 네트워크"),
    ],
    "no-contract-internet": [
        ("photo-1554224155-6726b3ff858f", "약정 없는 인터넷 계약"),
        ("photo-1450101499163-c8848c66ca85", "인터넷 약정 서류"),
    ],
    "internet-lowest-price-ranking": [
        ("photo-1611974789855-9c2a0a7236a3", "인터넷 요금 순위 차트"),
        ("photo-1579532537598-459ecdaf39cc", "인터넷 요금 절약"),
    ],
    "internet-tv-mobile-bundle": [
        ("photo-1593062096033-9a26b09da705", "인터넷 TV 결합 환경"),
        ("photo-1522869635100-9f4c5e86aa37", "TV 시청 결합할인"),
    ],
    "kt-bundle-discount": [
        ("photo-1558494949-ef010cbdcc31", "KT 인터넷 장비"),
        ("photo-1606904825846-647eb07f5be2", "KT 공유기 설치"),
    ],
    "sk-bundle-discount": [
        ("photo-1544197150-b99a580bb7a8", "SK 인터넷 네트워크"),
        ("photo-1516321318423-f06f85e504b3", "SK 인터넷 설정"),
    ],
    "lg-bundle-discount": [
        ("photo-1606904825846-647eb07f5be2", "LG U+ 인터넷 장비"),
        ("photo-1451187580459-43490279c0fa", "LG U+ 네트워크"),
    ],
    "family-bundle-discount": [
        ("photo-1556228578-0d85b1a4d571", "가족 결합할인 가정"),
        ("photo-1609220136736-443140cffec6", "가족 통신비 절약"),
    ],
    "couple-bundle-discount": [
        ("photo-1521737711867-e3b97375f902", "2인 가족 결합 상담"),
        ("photo-1573164713714-d95e436ab8d6", "부부 결합할인 비교"),
    ],
    "bundle-vs-single-internet": [
        ("photo-1554224155-6726b3ff858f", "결합 vs 단독 비교 서류"),
        ("photo-1591696205602-2f950c417cb9", "인터넷 요금 비교 분석"),
    ],
    "iptv-plan-comparison": [
        ("photo-1593062096033-9a26b09da705", "IPTV 시청 환경"),
        ("photo-1611162617213-7d7a39e9b1d7", "IPTV 채널 비교"),
    ],
    "internet-tv-bundle-price": [
        ("photo-1522869635100-9f4c5e86aa37", "인터넷 TV 결합 시청"),
        ("photo-1593062096033-9a26b09da705", "TV 결합 요금 비교"),
    ],
    "iptv-vs-ott": [
        ("photo-1611162617213-7d7a39e9b1d7", "IPTV vs OTT 비교"),
        ("photo-1522869635100-9f4c5e86aa37", "스트리밍 서비스 비교"),
    ],
    "internet-only-no-tv": [
        ("photo-1558494949-ef010cbdcc31", "인터넷만 단독 가입"),
        ("photo-1496181133206-80ce9b88a853", "인터넷만 사용하는 환경"),
    ],
    "iptv-without-settopbox": [
        ("photo-1563013544-824ae1b704d3", "스마트폰으로 TV 시청"),
        ("photo-1611162617213-7d7a39e9b1d7", "셋톱박스 없이 시청"),
    ],
    "internet-provider-switch": [
        ("photo-1556742044-3c52d6e88c62", "통신사 변경 상담"),
        ("photo-1450101499163-c8848c66ca85", "인터넷 변경 서류"),
    ],
    "internet-contract-renewal": [
        ("photo-1554224155-6726b3ff858f", "인터넷 약정 만료 재가입"),
        ("photo-1586281380349-632531db7ed4", "약정 연장 서류 검토"),
    ],
    "internet-signup-cashback": [
        ("photo-1580519542036-c47de6196ba5", "인터넷 가입 사은품 현금"),
        ("photo-1579532537598-459ecdaf39cc", "가입 혜택 비교"),
    ],
    "internet-installation-guide": [
        ("photo-1558494949-ef010cbdcc31", "인터넷 설치 장비"),
        ("photo-1606904825846-647eb07f5be2", "인터넷 개통 공유기"),
    ],
    "internet-cancellation-guide": [
        ("photo-1554224155-6726b3ff858f", "인터넷 해지 서류"),
        ("photo-1450101499163-c8848c66ca85", "위약금 계산 서류"),
    ],
    "internet-speed-test-fix": [
        ("photo-1451187580459-43490279c0fa", "인터넷 속도 측정"),
        ("photo-1544197150-b99a580bb7a8", "네트워크 속도 분석"),
    ],
    "wifi-router-recommendation": [
        ("photo-1606904825846-647eb07f5be2", "와이파이 공유기 추천"),
        ("photo-1558494949-ef010cbdcc31", "공유기 설치 환경"),
    ],
    "apartment-internet-recommendation": [
        ("photo-1560448204-e02f11c3d0e2", "아파트 인터넷 추천"),
        ("photo-1545324418-cc1a3fa10c00", "아파트 단지 전경"),
    ],
    "internet-save-money-tips": [
        ("photo-1579532537598-459ecdaf39cc", "인터넷 요금 절약 팁"),
        ("photo-1580519542036-c47de6196ba5", "통신비 절약하는 방법"),
    ],
    "internet-unpaid-penalty": [
        ("photo-1586281380349-632531db7ed4", "인터넷 요금 미납 서류"),
        ("photo-1554224155-6726b3ff858f", "미납 불이익 안내"),
    ],
}


def download_image(photo_id):
    url = f"https://images.unsplash.com/{photo_id}?w=800&h=450&fit=crop&auto=format&q=80"
    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0")
        with urllib.request.urlopen(req, timeout=30) as resp:
            tmp.write(resp.read())
        tmp.close()
        return tmp.name
    except Exception as e:
        tmp.close()
        os.unlink(tmp.name)
        print(f"  이미지 다운로드 실패 ({photo_id}): {e}")
        return None


def upload_image_to_wp(file_path, filename, alt_text):
    with open(file_path, "rb") as f:
        image_data = f.read()
    req = urllib.request.Request(MEDIA_API, data=image_data, method="POST")
    req.add_header("Authorization", f"Basic {AUTH}")
    req.add_header("Content-Type", "image/jpeg")
    req.add_header("Content-Disposition", f'attachment; filename="{filename}.jpg"')
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            media_id = result.get("id")
            media_url = result.get("source_url", "")
            if media_id and alt_text:
                update_data = json.dumps({"alt_text": alt_text}).encode("utf-8")
                update_req = urllib.request.Request(f"{MEDIA_API}/{media_id}", data=update_data, method="POST")
                update_req.add_header("Authorization", f"Basic {AUTH}")
                update_req.add_header("Content-Type", "application/json")
                try:
                    urllib.request.urlopen(update_req, timeout=15)
                except Exception:
                    pass
            return media_id, media_url
    except Exception as e:
        print(f"  WP 업로드 실패: {e}")
        return None, None


def upload_all_images():
    total = sum(len(imgs) for imgs in IMAGES.values())
    uploaded = 0
    failed = 0
    print("=" * 60)
    print(f"이미지 업로드 시작 (총 {total}장)")
    print("=" * 60)
    for slug, img_list in IMAGES.items():
        UPLOADED_IMAGES[slug] = []
        for idx, (photo_id, alt_text) in enumerate(img_list):
            filename = f"inet-{slug}-{idx+1}"
            tmp_path = download_image(photo_id)
            if not tmp_path:
                UPLOADED_IMAGES[slug].append(("", "", alt_text))
                failed += 1
                continue
            media_id, wp_url = upload_image_to_wp(tmp_path, filename, alt_text)
            os.unlink(tmp_path)
            if wp_url:
                UPLOADED_IMAGES[slug].append((media_id, wp_url, alt_text))
                uploaded += 1
                print(f"  [{uploaded+failed}/{total}] OK | {filename}")
            else:
                UPLOADED_IMAGES[slug].append(("", "", alt_text))
                failed += 1
            time.sleep(0.5)
    print(f"\n이미지 업로드 완료: 성공 {uploaded}, 실패 {failed}\n")


def get_image_html(slug, index):
    imgs = UPLOADED_IMAGES.get(slug, [])
    if index >= len(imgs):
        return ""
    media_id, wp_url, alt_text = imgs[index]
    if not wp_url:
        return ""
    return f'''<figure style="margin:32px 0;text-align:center;">
<img src="{wp_url}" alt="{alt_text}" style="width:100%;max-width:800px;height:auto;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.10);" loading="lazy" />
<figcaption style="margin-top:8px;font-size:13px;color:#6b7280;">{alt_text}</figcaption>
</figure>'''


def get_featured_image_id(slug):
    imgs = UPLOADED_IMAGES.get(slug, [])
    if imgs and imgs[0][0]:
        return imgs[0][0]
    return None


def make_cta(cta):
    border_style = f"border:{cta['border']};" if cta.get("border") else ""
    return f"""<div style="background:{cta['bg']};{border_style}border-radius:12px;padding:28px 32px;margin:32px 0;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;">
  <div>
    <p style="margin:0 0 6px;font-size:18px;font-weight:700;color:{cta['text_color']};">{cta['text']}</p>
    <p style="margin:0;font-size:14px;color:{cta['desc_color']};">{cta['desc']}</p>
  </div>
  <a href="{cta['url']}" target="_blank" rel="noopener noreferrer"
     style="background:{cta['btn_bg']};color:{cta['btn_color']};padding:12px 24px;border-radius:8px;font-weight:700;text-decoration:none;white-space:nowrap;font-size:15px;">
    바로가기 &rarr;
  </a>
</div>"""


def build_content(post):
    parts = []
    slug = post.get("slug", "")
    parts.append(f'<p style="font-size:17px;line-height:1.8;margin-bottom:24px;">{post["intro"]}</p>')
    img1 = get_image_html(slug, 0)
    if img1:
        parts.append(img1)
    sections = post["sections"]
    ctas = post["ctas"]
    num_sections = len(sections)
    img2_pos = max(2, int(num_sections * 0.6))
    for i, (title, body) in enumerate(sections):
        parts.append(f'<h2 style="font-size:22px;font-weight:700;margin:40px 0 16px;border-left:4px solid #2563eb;padding-left:12px;">{title}</h2>')
        parts.append(body)
        if i == 1 and len(ctas) > 0:
            parts.append(make_cta(ctas[0]))
        elif i == num_sections // 2 and len(ctas) > 1:
            parts.append(make_cta(ctas[1]))
        if i == img2_pos:
            img2 = get_image_html(slug, 1)
            if img2:
                parts.append(img2)
    parts.append('<h2 style="font-size:22px;font-weight:700;margin:40px 0 16px;border-left:4px solid #2563eb;padding-left:12px;">자주 묻는 질문 (FAQ)</h2>')
    for q, a in post["faq"]:
        parts.append(f'<h3 style="font-size:17px;font-weight:600;color:#1e40af;margin:20px 0 8px;">Q. {q}</h3>')
        parts.append(f'<p style="margin:0 0 16px;line-height:1.8;">A. {a}</p>')
    if len(ctas) > 2:
        parts.append(make_cta(ctas[2]))
    return "\n".join(parts)


CTA_INTERNET_COMPARE = {"text": "인터넷 요금 비교 사이트", "desc": "통신사별 인터넷 요금을 한눈에 비교하세요", "url": "https://www.planj.co.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"}
CTA_SPEED_TEST = {"text": "인터넷 속도 측정하기", "desc": "현재 인터넷 속도를 무료로 측정해보세요", "url": "https://fast.com/ko/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"}
CTA_INTERNET_SIGNUP = {"text": "인터넷 가입 혜택 비교", "desc": "통신사별 가입 사은품과 캐시백을 비교하세요", "url": "https://www.internet-compare.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"}


POSTS = [
    # 1. 인터넷 요금제 비교 통신사별 최저가 총정리
    {
        "title": "인터넷 요금제 비교 통신사별 최저가 총정리",
        "cat": CAT_INTERNET,
        "slug": "internet-plan-comparison",
        "intro": "인터넷 요금은 통신사마다, 속도마다, 약정 기간마다 천차만별입니다. 같은 500Mbps 인터넷이라도 <strong>KT, SK브로드밴드, LG U+</strong> 중 어디에 가입하느냐에 따라 월 1~2만 원 차이가 납니다. 결합할인, 약정 할인, 프로모션까지 고려하면 비교가 더 복잡해집니다. 이 글에서는 통신사별 인터넷 요금을 속도 구간별로 비교하고 최저가로 가입하는 방법을 총정리합니다.",
        "sections": [
            ("통신사별 인터넷 요금 비교표", "<table><thead><tr><th>속도</th><th>KT</th><th>SK브로드밴드</th><th>LG U+</th></tr></thead><tbody><tr><td>100Mbps</td><td>월 22,000원</td><td>월 19,800원</td><td>월 20,900원</td></tr><tr><td>500Mbps</td><td>월 27,500원</td><td>월 25,300원</td><td>월 26,400원</td></tr><tr><td>1Gbps</td><td>월 33,000원</td><td>월 30,800원</td><td>월 31,900원</td></tr><tr><td>2.5Gbps</td><td>월 38,500원</td><td>미제공</td><td>월 36,300원</td></tr><tr><td>10Gbps</td><td>월 55,000원</td><td>미제공</td><td>월 49,500원</td></tr></tbody></table><p>※ 3년 약정 기준, 결합할인 미적용 가격입니다. 프로모션에 따라 변동될 수 있습니다.</p>"),
            ("인터넷 요금제 선택 기준 4가지", "<ol><li><strong>필요한 속도</strong>: 웹서핑·유튜브만 보면 100Mbps로 충분합니다. 4K 스트리밍·온라인 게임은 500Mbps, 대용량 다운로드·재택근무는 1Gbps를 추천합니다.</li><li><strong>약정 기간</strong>: 3년 약정이 가장 저렴하지만 중도 해지 시 위약금이 큽니다. 1년 약정은 월 3~5천 원 비싸지만 유연합니다.</li><li><strong>결합할인 가능 여부</strong>: 휴대폰·TV와 결합하면 월 5,000~15,000원 추가 할인됩니다.</li><li><strong>가입 사은품</strong>: 통신사 직접 가입보다 대리점·비교 사이트 경유 시 현금 사은품이 더 큽니다.</li></ol>"),
            ("속도별 추천 사용 환경", "<table><thead><tr><th>속도</th><th>추천 환경</th><th>동시 사용 기기</th></tr></thead><tbody><tr><td>100Mbps</td><td>1인 웹서핑, 유튜브</td><td>1~2대</td></tr><tr><td>500Mbps</td><td>2~3인 가구, 4K 스트리밍</td><td>3~5대</td></tr><tr><td>1Gbps</td><td>4인 이상 가구, 재택근무, 게임</td><td>5~10대</td></tr><tr><td>2.5Gbps</td><td>고화질 스트리밍 다수, NAS 운용</td><td>10대 이상</td></tr></tbody></table>"),
            ("최저가로 인터넷 가입하는 방법", "<ol><li><strong>인터넷 비교 사이트 활용</strong>: 플랜J, 인터넷가입비교 등에서 통신사별 실질 요금과 사은품을 한눈에 비교할 수 있습니다.</li><li><strong>약정 만료 시점 활용</strong>: 기존 약정 만료 3개월 전부터 타 통신사 가입을 알아보면 경쟁 견적으로 최저가를 받을 수 있습니다.</li><li><strong>프로모션 시즌 공략</strong>: 3월(이사 시즌), 9~10월(추석 전후)에 통신사 프로모션이 가장 활발합니다.</li><li><strong>온라인 전용 요금제</strong>: 일부 통신사는 온라인 전용 할인 요금제를 운영합니다. 대리점보다 월 1~2천 원 저렴할 수 있습니다.</li></ol>"),
        ],
        "faq": [
            ("인터넷 속도는 실제로 표기된 만큼 나오나요?", "표기 속도는 <strong>이론 최대 속도</strong>입니다. 실제 속도는 공유기 성능, 시간대, 회선 상태에 따라 표기의 70~90% 수준이 일반적입니다. fast.com이나 speedtest.net에서 실제 속도를 측정해보세요."),
            ("3년 약정 중 이사하면 위약금을 내야 하나요?", "이사 시 같은 통신사로 이전 설치하면 <strong>위약금 없이 계속 사용</strong> 가능합니다. 이전 설치비(보통 무료~3만 원)만 발생합니다. 통신사를 바꾸면 위약금이 발생합니다."),
            ("통신사마다 인터넷 품질 차이가 있나요?", "KT는 자체 회선 보유로 안정성이 높고, SK·LG는 KT 회선을 임대하는 구간이 있어 지역에 따라 차이가 날 수 있습니다. <strong>아파트 단지 내 FTTH 설비</strong>가 어떤 통신사인지가 실제 품질에 가장 큰 영향을 줍니다."),
        ],
        "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP],
    },

    # 2. KT SK LG 인터넷 요금 비교
    {
        "title": "KT SK LG 인터넷 요금 비교 어디가 가장 저렴할까",
        "cat": CAT_INTERNET,
        "slug": "kt-sk-lg-internet-price",
        "intro": "인터넷을 가입하려면 <strong>KT, SK브로드밴드, LG U+</strong> 세 곳 중 하나를 선택해야 합니다. 각 통신사는 요금, 속도, 부가서비스, 결합할인에서 차이가 있습니다. 이 글에서는 세 통신사의 인터넷 요금을 조건별로 정밀 비교하여 나에게 가장 유리한 통신사를 찾아드립니다.",
        "sections": [
            ("3대 통신사 인터넷 핵심 비교", "<table><thead><tr><th>항목</th><th>KT</th><th>SK브로드밴드</th><th>LG U+</th></tr></thead><tbody><tr><td>회선</td><td>자체 보유</td><td>일부 KT 임대</td><td>자체 + 일부 임대</td></tr><tr><td>커버리지</td><td>전국 최대</td><td>도시 중심</td><td>전국 양호</td></tr><tr><td>최대 속도</td><td>10Gbps</td><td>1Gbps</td><td>10Gbps</td></tr><tr><td>가격 경쟁력</td><td>보통</td><td>최저가</td><td>중간</td></tr><tr><td>결합할인</td><td>KT 모바일</td><td>SKT 모바일</td><td>LG 모바일</td></tr><tr><td>IPTV</td><td>올레tv</td><td>B tv</td><td>U+tv</td></tr></tbody></table>"),
            ("500Mbps 기준 실질 요금 비교", "<p>가장 많이 가입하는 <strong>500Mbps 요금제</strong>를 기준으로 실질 월 요금을 비교합니다.</p><table><thead><tr><th>조건</th><th>KT</th><th>SK브로드밴드</th><th>LG U+</th></tr></thead><tbody><tr><td>단독 가입 (3년)</td><td>27,500원</td><td>25,300원</td><td>26,400원</td></tr><tr><td>모바일 결합</td><td>22,000원</td><td>20,300원</td><td>21,400원</td></tr><tr><td>TV 결합</td><td>24,200원</td><td>22,000원</td><td>23,100원</td></tr><tr><td>모바일+TV 결합</td><td>19,800원</td><td>17,600원</td><td>18,700원</td></tr></tbody></table><p>결합할인 적용 시 SK브로드밴드가 가장 저렴하지만, KT의 회선 안정성과 LG U+의 콘텐츠 혜택도 고려해야 합니다.</p>"),
            ("통신사별 강점과 약점", "<p><strong>KT</strong></p><ul><li>강점: 자체 회선 → 가장 안정적, 전국 커버리지, 10Gbps 지원</li><li>약점: 가격이 가장 비쌈</li></ul><p><strong>SK브로드밴드</strong></p><ul><li>강점: 가격 최저, SKT 모바일 결합 시 추가 할인</li><li>약점: 일부 지역 KT 회선 임대, 초고속(2.5G 이상) 미지원</li></ul><p><strong>LG U+</strong></p><ul><li>강점: U+tv 콘텐츠(넷플릭스 포함), 10Gbps 지원</li><li>약점: KT 대비 커버리지 약간 좁음</li></ul>"),
            ("나에게 맞는 통신사 선택법", "<ul><li><strong>안정성 최우선</strong> → KT (자체 회선)</li><li><strong>가격 최우선</strong> → SK브로드밴드 (최저가)</li><li><strong>콘텐츠 + 가성비</strong> → LG U+ (넷플릭스 포함 IPTV)</li><li><strong>SKT 휴대폰 사용자</strong> → SK브로드밴드 (결합할인 극대화)</li><li><strong>KT 휴대폰 사용자</strong> → KT (결합할인 극대화)</li></ul>"),
        ],
        "faq": [
            ("아파트에서는 통신사를 자유롭게 고를 수 있나요?", "대부분의 아파트에서 <strong>3사 모두 가입 가능</strong>합니다. 단, 아파트 단지 내 FTTH 설비가 특정 통신사인 경우 해당 통신사가 속도와 안정성에서 유리합니다. 관리사무소에 문의하면 확인 가능합니다."),
            ("인터넷과 휴대폰이 다른 통신사여도 되나요?", "네, 가능합니다. 하지만 <strong>같은 통신사로 묶으면 결합할인</strong>(월 5,000~15,000원)을 받을 수 있어 경제적입니다."),
            ("SK브로드밴드가 가장 싼데 품질은 괜찮나요?", "도시 지역에서는 <strong>체감 차이가 거의 없습니다</strong>. 다만 농어촌이나 신축 아파트에서는 KT 직접 회선이 유리한 경우가 있으니 이사 전 확인하세요."),
        ],
        "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP],
    },

    # 3~30번 포스트는 같은 패턴으로 계속
    # 3. 1인 가구 인터넷 요금제 추천
    {
        "title": "1인 가구 인터넷 요금제 추천 가성비 비교",
        "cat": CAT_INTERNET,
        "slug": "single-person-internet",
        "intro": "혼자 사는 <strong>1인 가구</strong>에게 인터넷 요금은 고정 지출 중 하나입니다. 4인 가구처럼 기가 인터넷이 필요하지 않은 경우가 많아, 적절한 속도의 저렴한 요금제를 선택하면 월 1~2만 원을 절약할 수 있습니다. 1인 가구에 최적화된 인터넷 요금제와 가입 전략을 안내합니다.",
        "sections": [
            ("1인 가구에 필요한 인터넷 속도", "<p>1인 가구의 일반적인 사용 패턴과 필요 속도입니다.</p><table><thead><tr><th>사용 패턴</th><th>추천 속도</th><th>월 요금 (약정)</th></tr></thead><tbody><tr><td>웹서핑, SNS, 유튜브(HD)</td><td>100Mbps</td><td>1.9~2.2만원</td></tr><tr><td>넷플릭스 4K, 온라인 게임</td><td>500Mbps</td><td>2.5~2.7만원</td></tr><tr><td>재택근무, 화상회의, 대용량 업로드</td><td>500Mbps~1Gbps</td><td>2.5~3.3만원</td></tr></tbody></table><p>대부분의 1인 가구는 <strong>100~500Mbps</strong>면 충분합니다. 4K 스트리밍을 자주 보지 않는다면 100Mbps가 가장 가성비 좋습니다.</p>"),
            ("1인 가구 추천 요금제 TOP 5", "<table><thead><tr><th>요금제</th><th>통신사</th><th>속도</th><th>월 요금</th><th>특징</th></tr></thead><tbody><tr><td>SK 라이트</td><td>SK브로드밴드</td><td>100Mbps</td><td>19,800원</td><td>최저가</td></tr><tr><td>LG 베이직</td><td>LG U+</td><td>100Mbps</td><td>20,900원</td><td>U+tv 결합 가능</td></tr><tr><td>KT 슬림</td><td>KT</td><td>100Mbps</td><td>22,000원</td><td>안정적 자체 회선</td></tr><tr><td>SK 스탠다드</td><td>SK브로드밴드</td><td>500Mbps</td><td>25,300원</td><td>가성비 500M</td></tr><tr><td>LG 스탠다드</td><td>LG U+</td><td>500Mbps</td><td>26,400원</td><td>넷플릭스 결합 가능</td></tr></tbody></table>"),
            ("1인 가구 인터넷 절약 전략", "<ol><li><strong>TV 없이 인터넷만 가입</strong>: IPTV 없이 인터넷만 단독 가입하면 월 5,000~10,000원 절약됩니다. OTT(넷플릭스, 웨이브)로 대체하세요.</li><li><strong>휴대폰 결합할인</strong>: 인터넷과 같은 통신사 휴대폰을 묶으면 월 5,000원 이상 추가 할인됩니다.</li><li><strong>알뜰폰 + 인터넷 결합</strong>: 일부 알뜰폰(MVNO)도 인터넷 결합할인을 제공합니다.</li><li><strong>와이파이 공유기 업그레이드</strong>: 통신사 제공 공유기 대신 성능 좋은 공유기를 사면 같은 요금제에서 더 빠른 체감 속도를 얻을 수 있습니다.</li></ol>"),
            ("원룸·오피스텔 인터넷 주의사항", "<ul><li><strong>건물 제공 인터넷</strong>: 일부 원룸·오피스텔은 관리비에 인터넷이 포함되어 있습니다. 속도가 충분하면 별도 가입이 불필요합니다.</li><li><strong>공유 인터넷</strong>: 건물 전체가 하나의 회선을 공유하는 경우 저녁 시간대에 속도가 크게 떨어질 수 있습니다. 이 경우 개별 회선 가입을 고려하세요.</li><li><strong>설치 가능 여부</strong>: 오래된 건물은 광케이블 설치가 안 되는 경우가 있습니다. 가입 전 통신사에 설치 가능 여부를 확인하세요.</li></ul>"),
        ],
        "faq": [
            ("자취방에 이미 인터넷이 있는데 추가로 가입해야 하나요?", "관리비에 포함된 인터넷이면 <strong>추가 가입 불필요</strong>합니다. 속도가 느리다면 건물주에게 요청하거나, 개별 회선을 추가 가입할 수 있습니다."),
            ("1인 가구도 3년 약정이 유리한가요?", "1~2년 내 이사 계획이 없다면 <strong>3년 약정이 가장 저렴</strong>합니다. 이사 시 같은 통신사로 이전하면 위약금이 없으므로 대부분 3년 약정이 유리합니다."),
            ("인터넷 없이 휴대폰 테더링만으로 충분하지 않나요?", "단순 웹서핑 정도면 가능하지만, <strong>데이터 소진이 빠르고 속도가 불안정</strong>합니다. 재택근무나 스트리밍이 필요하면 별도 인터넷 가입을 권합니다."),
        ],
        "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP],
    },

    # 4. 자취생 인터넷 추천
    {"title": "자취생 인터넷 추천 저렴한 요금제 비교", "cat": CAT_INTERNET, "slug": "student-cheap-internet", "intro": "자취를 시작하면 인터넷 가입이 필수입니다. 하지만 학생·사회초년생에게 매달 2~3만 원의 인터넷 요금은 부담이 됩니다. <strong>자취생에게 최적화된 저렴한 인터넷 요금제</strong>와 절약 꿀팁을 총정리합니다.", "sections": [("자취생 인터넷 가입 전 확인사항", "<ol><li><strong>건물 기본 인터넷 확인</strong>: 원룸·오피스텔은 관리비에 인터넷이 포함된 경우가 많습니다. 집주인이나 관리사무소에 먼저 확인하세요.</li><li><strong>설치 가능 통신사 확인</strong>: 오래된 건물은 특정 통신사만 설치 가능한 경우가 있습니다. 가입 전 통신사에 주소를 알려주고 확인하세요.</li><li><strong>약정 기간 고려</strong>: 1~2년마다 이사할 계획이면 1년 약정이나 약정 없는 요금제가 유리합니다.</li></ol>"), ("자취생 추천 요금제 비교", "<table><thead><tr><th>요금제</th><th>속도</th><th>월 요금</th><th>약정</th><th>추천 포인트</th></tr></thead><tbody><tr><td>SK 라이트 100M</td><td>100Mbps</td><td>19,800원</td><td>3년</td><td>최저가</td></tr><tr><td>LG 베이직 100M</td><td>100Mbps</td><td>20,900원</td><td>3년</td><td>가성비</td></tr><tr><td>KT 슬림 100M</td><td>100Mbps</td><td>22,000원</td><td>3년</td><td>안정성</td></tr><tr><td>SK 라이트 (1년)</td><td>100Mbps</td><td>24,200원</td><td>1년</td><td>단기 거주</td></tr><tr><td>알뜰 인터넷</td><td>100Mbps</td><td>16,500원</td><td>없음</td><td>약정 없음</td></tr></tbody></table>"), ("자취생 인터넷 비용 줄이는 꿀팁 5가지", "<ol><li><strong>알뜰 인터넷 활용</strong>: SK브로드밴드·LG U+ 회선을 저렴하게 재판매하는 알뜰 인터넷 상품이 있습니다. 약정 없이 월 1.6~1.9만 원에 이용 가능합니다.</li><li><strong>친구와 공유</strong>: 같은 건물에 사는 친구와 인터넷을 공유하면 비용을 반으로 줄일 수 있습니다.</li><li><strong>가입 사은품 활용</strong>: 대리점 가입 시 현금 3~10만 원 사은품을 받을 수 있습니다.</li><li><strong>휴대폰 결합</strong>: 같은 통신사로 결합하면 월 5,000원 이상 추가 할인됩니다.</li><li><strong>건물 기본 인터넷 활용</strong>: 관리비에 포함된 인터넷이 있으면 별도 가입하지 마세요.</li></ol>"), ("알뜰 인터넷이란", "<p><strong>알뜰 인터넷(MVNO 인터넷)</strong>은 대형 통신사의 회선을 빌려서 저렴하게 제공하는 인터넷 서비스입니다.</p><ul><li>속도와 품질은 대형 통신사와 <strong>동일</strong> (같은 회선 사용)</li><li>월 요금이 <strong>30~40% 저렴</strong></li><li>약정 없음 또는 1년 약정</li><li>단점: 결합할인 불가, AS 대응이 느릴 수 있음</li></ul>")], "faq": [("건물 인터넷이 느린데 개별로 가입할 수 있나요?", "<strong>네, 가능합니다.</strong> 건물 인터넷과 별도로 개인 회선을 추가 가입할 수 있습니다. 통신사에 주소를 알려주고 개별 설치 가능 여부를 확인하세요."), ("약정 중에 이사하면 위약금을 내야 하나요?", "같은 통신사로 <strong>이전 설치</strong>하면 위약금 없이 계속 사용 가능합니다. 통신사를 바꾸거나 해지하면 남은 약정 기간에 비례한 위약금이 발생합니다."), ("와이파이만 있으면 되는데 유선 인터넷이 꼭 필요한가요?", "와이파이도 <strong>유선 인터넷 회선이 필요</strong>합니다. 인터넷에 가입하면 공유기를 통해 와이파이를 사용하는 구조입니다. 인터넷 없이 와이파이만 쓸 수는 없습니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 5. 100메가 vs 500메가 vs 기가 인터넷
    {"title": "100메가 vs 500메가 vs 기가 인터넷 속도별 요금 비교", "cat": CAT_INTERNET, "slug": "internet-speed-plan-comparison", "intro": "인터넷 가입 시 가장 고민되는 것이 <strong>속도 선택</strong>입니다. 100Mbps, 500Mbps, 1Gbps 중 어떤 것을 골라야 할까요? 비싼 요금제가 항상 좋은 것은 아닙니다. 실제 사용 환경에 맞는 속도를 선택하면 불필요한 비용을 줄일 수 있습니다.", "sections": [("속도별 체감 차이 비교", "<table><thead><tr><th>항목</th><th>100Mbps</th><th>500Mbps</th><th>1Gbps</th></tr></thead><tbody><tr><td>웹페이지 로딩</td><td>차이 없음</td><td>차이 없음</td><td>차이 없음</td></tr><tr><td>유튜브 4K</td><td>버퍼링 가능</td><td>원활</td><td>원활</td></tr><tr><td>넷플릭스 4K</td><td>버퍼링 가능</td><td>원활</td><td>원활</td></tr><tr><td>온라인 게임</td><td>지연 가능</td><td>원활</td><td>원활</td></tr><tr><td>1GB 파일 다운로드</td><td>약 80초</td><td>약 16초</td><td>약 8초</td></tr><tr><td>10GB 파일 다운로드</td><td>약 14분</td><td>약 3분</td><td>약 80초</td></tr></tbody></table>"), ("내게 맞는 속도 선택 가이드", "<ul><li><strong>100Mbps 추천</strong>: 1~2인 가구, 웹서핑·SNS·유튜브(HD) 위주, 비용 절약 우선</li><li><strong>500Mbps 추천</strong>: 2~4인 가구, 4K 스트리밍, 온라인 게임, 재택근무 화상회의</li><li><strong>1Gbps 추천</strong>: 4인 이상 가구, 동시 다수 기기 사용, 대용량 파일 업로드/다운로드, NAS 운용</li></ul><p><strong>결론</strong>: 대부분의 가정에서 500Mbps면 충분합니다. 1Gbps는 동시 사용 기기가 5대 이상이거나 대용량 작업이 잦을 때만 필요합니다.</p>"), ("속도를 높여도 체감이 안 되는 경우", "<p>비싼 요금제로 업그레이드해도 속도 차이를 못 느끼는 경우가 있습니다.</p><ul><li><strong>공유기 성능 부족</strong>: 공유기가 100Mbps까지만 지원하면 1Gbps 가입해도 100M밖에 안 나옵니다.</li><li><strong>와이파이 거리·장애물</strong>: 공유기와 기기 사이에 벽이 많으면 속도가 떨어집니다.</li><li><strong>랜선 규격</strong>: Cat5 랜선은 100Mbps까지만 지원합니다. 500Mbps 이상은 Cat5e 이상 랜선이 필요합니다.</li><li><strong>기기 성능</strong>: 오래된 노트북이나 스마트폰은 기가 속도를 지원하지 않을 수 있습니다.</li></ul>"), ("속도 업그레이드 vs 공유기 교체 어떤 것이 먼저?", "<p>속도가 느리다면 요금제 업그레이드보다 <strong>공유기 교체가 먼저</strong>입니다.</p><ol><li>현재 공유기 스펙 확인 (802.11ac 이상 권장)</li><li>fast.com에서 유선 속도 측정 (공유기에 랜선 직접 연결)</li><li>유선 속도가 정상이면 → 공유기 또는 와이파이 문제</li><li>유선 속도도 느리면 → 통신사에 회선 점검 요청</li></ol>")], "faq": [("500Mbps와 1Gbps의 체감 차이가 큰가요?", "일반 사용(웹서핑, 스트리밍)에서는 <strong>체감 차이가 거의 없습니다</strong>. 대용량 파일 다운로드 시에만 차이가 느껴집니다. 월 요금 차이가 5,000~7,000원이므로 필요하지 않으면 500Mbps가 가성비 좋습니다."), ("게임은 인터넷 속도보다 핑이 중요한가요?", "<strong>맞습니다.</strong> 온라인 게임에서 중요한 것은 속도(Mbps)가 아니라 지연시간(핑, ms)입니다. 100Mbps로도 핑이 낮으면 게임에 지장이 없습니다. 유선 연결이 와이파이보다 핑이 안정적입니다."), ("현재 요금제 속도를 확인하는 방법은?", "통신사 앱 또는 고객센터에서 현재 가입된 요금제 속도를 확인할 수 있습니다. 실제 속도는 <strong>fast.com 또는 speedtest.net</strong>에서 측정하세요.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 6. 기가 인터넷 요금제 비교
    {"title": "기가 인터넷 요금제 비교 속도 체감 차이 총정리", "cat": CAT_INTERNET, "slug": "giga-internet-comparison", "intro": "기가(Gbps) 인터넷은 초당 1,000Mbps 이상의 초고속 인터넷입니다. 재택근무, 4K 스트리밍, 온라인 게임 등 <strong>고대역폭이 필요한 환경</strong>에서 주목받고 있습니다. 통신사별 기가 인터넷 요금과 실제 체감 속도를 비교합니다.", "sections": [("기가 인터넷 요금 비교표", "<table><thead><tr><th>요금제</th><th>속도</th><th>월 요금 (3년)</th><th>통신사</th></tr></thead><tbody><tr><td>KT 기가인터넷</td><td>1Gbps</td><td>33,000원</td><td>KT</td></tr><tr><td>SK 기가인터넷</td><td>1Gbps</td><td>30,800원</td><td>SK</td></tr><tr><td>LG 기가인터넷</td><td>1Gbps</td><td>31,900원</td><td>LG U+</td></tr><tr><td>KT 2.5G</td><td>2.5Gbps</td><td>38,500원</td><td>KT</td></tr><tr><td>LG 2.5G</td><td>2.5Gbps</td><td>36,300원</td><td>LG U+</td></tr><tr><td>KT 10G</td><td>10Gbps</td><td>55,000원</td><td>KT</td></tr></tbody></table>"), ("기가 인터넷 실제 속도는 얼마나 나올까", "<p>기가 인터넷 가입 시 실제 체감 속도입니다.</p><ul><li><strong>유선 연결</strong>: 이론 속도의 80~95% → 약 800~950Mbps</li><li><strong>와이파이 5(802.11ac)</strong>: 약 300~500Mbps</li><li><strong>와이파이 6(802.11ax)</strong>: 약 500~800Mbps</li><li><strong>와이파이 6E</strong>: 약 700~1,000Mbps</li></ul><p>기가 인터넷의 속도를 제대로 쓰려면 <strong>와이파이 6 이상 공유기</strong>가 필수입니다. 통신사 기본 공유기는 802.11ac인 경우가 많아 교체를 권합니다.</p>"), ("기가 인터넷이 필요한 사람", "<ul><li>가족 구성원이 동시에 4K 스트리밍을 보는 가정</li><li>대용량 파일(영상, 게임)을 자주 다운로드하는 분</li><li>재택근무로 화상회의 + 파일 업로드를 동시에 하는 분</li><li>NAS, 홈서버를 운용하는 분</li><li>스마트홈 기기(IoT)가 10대 이상인 가정</li></ul>"), ("기가 인터넷 가입 전 체크리스트", "<ol><li><strong>공유기</strong>: 와이파이 6(802.11ax) 이상 지원 공유기 필요</li><li><strong>랜선</strong>: Cat5e 이상 (Cat6 권장)</li><li><strong>기기</strong>: 노트북·스마트폰이 기가비트 이더넷/와이파이 6 지원 확인</li><li><strong>아파트 설비</strong>: FTTH(광케이블) 설비가 기가 속도를 지원하는지 확인</li></ol>")], "faq": [("기가 인터넷인데 500Mbps도 안 나오는데 왜 그런가요?", "대부분 <strong>공유기 또는 랜선 문제</strong>입니다. 통신사 기본 공유기가 구형이면 기가 속도를 지원하지 않습니다. 공유기에 직접 Cat6 랜선으로 연결해서 속도를 측정해보세요."), ("2.5Gbps와 10Gbps는 일반 가정에서 필요한가요?", "현재 대부분의 가정에서는 <strong>필요하지 않습니다</strong>. 1Gbps로도 4K 스트리밍, 게임, 재택근무 모두 충분합니다. 2.5G 이상은 전문 작업(영상 편집, 서버 운용)에 적합합니다."), ("기가 인터넷 가입하면 공유기를 꼭 바꿔야 하나요?", "통신사에서 제공하는 공유기가 와이파이 6을 지원하면 교체 불필요합니다. 802.11ac 이하라면 <strong>와이파이 6 공유기로 교체</strong>해야 기가 속도의 혜택을 와이파이로도 느낄 수 있습니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 7. 약정 없는 인터넷
    {"title": "인터넷 약정 없는 요금제 비교 위약금 없이 쓰는 방법", "cat": CAT_INTERNET, "slug": "no-contract-internet", "intro": "인터넷 3년 약정이 부담스러운 분들을 위해 <strong>약정 없는 인터넷 요금제</strong>를 비교합니다. 자주 이사하는 분, 단기 거주자, 위약금이 싫은 분에게 최적의 선택지를 안내합니다.", "sections": [("약정 없는 인터넷 요금제 비교", "<table><thead><tr><th>서비스</th><th>속도</th><th>월 요금</th><th>약정</th><th>특징</th></tr></thead><tbody><tr><td>알뜰 인터넷 A</td><td>100Mbps</td><td>16,500원</td><td>없음</td><td>SK 회선</td></tr><tr><td>알뜰 인터넷 B</td><td>100Mbps</td><td>17,600원</td><td>없음</td><td>LG 회선</td></tr><tr><td>SK 무약정</td><td>100Mbps</td><td>28,600원</td><td>없음</td><td>공식</td></tr><tr><td>KT 무약정</td><td>100Mbps</td><td>30,800원</td><td>없음</td><td>공식</td></tr><tr><td>LG 무약정</td><td>100Mbps</td><td>29,700원</td><td>없음</td><td>공식</td></tr></tbody></table><p>알뜰 인터넷이 대형 통신사 무약정보다 <strong>월 1만 원 이상 저렴</strong>합니다.</p>"), ("약정 vs 무약정 손익분기점", "<p>3년 약정과 무약정의 총 비용을 비교합니다 (100Mbps 기준).</p><table><thead><tr><th>기간</th><th>3년 약정 (월 2만원)</th><th>무약정 (월 2.9만원)</th><th>차이</th></tr></thead><tbody><tr><td>6개월</td><td>12만 + 위약금 약 18만 = 30만</td><td>17.4만</td><td>무약정 유리</td></tr><tr><td>1년</td><td>24만 + 위약금 약 14만 = 38만</td><td>34.8만</td><td>무약정 유리</td></tr><tr><td>2년</td><td>48만 + 위약금 약 7만 = 55만</td><td>69.6만</td><td>약정 유리</td></tr><tr><td>3년</td><td>72만</td><td>104.4만</td><td>약정 유리</td></tr></tbody></table><p><strong>결론</strong>: 1년 6개월 이상 사용할 예정이면 3년 약정이, 그 이하면 무약정이 유리합니다.</p>"), ("무약정 인터넷 가입 방법", "<ol><li><strong>알뜰 인터넷</strong>: 온라인으로 신청 가능. 설치까지 3~7일 소요.</li><li><strong>대형 통신사 무약정</strong>: 통신사 홈페이지 또는 고객센터에서 신청. 약정 없음 옵션을 선택하세요.</li><li><strong>월세 포함 인터넷</strong>: 집주인이 인터넷을 제공하는 경우 별도 가입 불필요.</li></ol>"), ("무약정 인터넷 주의사항", "<ul><li><strong>설치비</strong>: 약정 없는 경우 설치비(3~5만 원)가 발생할 수 있습니다.</li><li><strong>공유기</strong>: 알뜰 인터넷은 공유기를 제공하지 않는 경우가 있어 별도 구매가 필요합니다.</li><li><strong>AS</strong>: 알뜰 인터넷은 AS 대응이 대형 통신사보다 느릴 수 있습니다.</li><li><strong>결합할인 불가</strong>: 대부분의 알뜰 인터넷은 휴대폰 결합할인이 안 됩니다.</li></ul>")], "faq": [("알뜰 인터넷은 속도가 느리지 않나요?", "<strong>동일한 회선</strong>을 사용하므로 속도는 대형 통신사와 같습니다. SK 또는 LG 회선을 그대로 사용합니다."), ("무약정 인터넷도 이사할 때 이전 설치가 되나요?", "대형 통신사는 이전 설치가 가능합니다. 알뜰 인터넷은 업체에 따라 <strong>해지 후 재가입</strong>해야 하는 경우가 있으니 확인하세요."), ("약정 중인데 무약정으로 바꿀 수 있나요?", "현재 약정을 해지(위약금 발생)한 후 무약정으로 재가입해야 합니다. <strong>약정 만료 시점에 변경</strong>하는 것이 위약금 없이 전환하는 방법입니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 8. 인터넷 요금제 월별 최저가 순위
    {"title": "인터넷 요금제 월별 가격 순위 최저가 TOP 10", "cat": CAT_INTERNET, "slug": "internet-lowest-price-ranking", "intro": "수십 가지 인터넷 요금제 중 <strong>실질 월 납부 금액이 가장 저렴한 요금제</strong>를 순위별로 정리했습니다. 단독 가입 기준과 결합 할인 기준을 나누어 비교하므로 본인 상황에 맞는 최저가 요금제를 찾을 수 있습니다.", "sections": [("단독 가입 최저가 TOP 10", "<table><thead><tr><th>순위</th><th>요금제</th><th>속도</th><th>월 요금</th><th>약정</th></tr></thead><tbody><tr><td>1</td><td>알뜰넷 100M</td><td>100Mbps</td><td>16,500원</td><td>없음</td></tr><tr><td>2</td><td>알뜰넷 플러스</td><td>100Mbps</td><td>17,600원</td><td>없음</td></tr><tr><td>3</td><td>SK 라이트 100M</td><td>100Mbps</td><td>19,800원</td><td>3년</td></tr><tr><td>4</td><td>LG 베이직 100M</td><td>100Mbps</td><td>20,900원</td><td>3년</td></tr><tr><td>5</td><td>KT 슬림 100M</td><td>100Mbps</td><td>22,000원</td><td>3년</td></tr><tr><td>6</td><td>알뜰넷 500M</td><td>500Mbps</td><td>22,000원</td><td>없음</td></tr><tr><td>7</td><td>SK 스탠다드 500M</td><td>500Mbps</td><td>25,300원</td><td>3년</td></tr><tr><td>8</td><td>LG 스탠다드 500M</td><td>500Mbps</td><td>26,400원</td><td>3년</td></tr><tr><td>9</td><td>KT 에센스 500M</td><td>500Mbps</td><td>27,500원</td><td>3년</td></tr><tr><td>10</td><td>SK 기가 1G</td><td>1Gbps</td><td>30,800원</td><td>3년</td></tr></tbody></table>"), ("결합할인 적용 시 최저가 TOP 5", "<table><thead><tr><th>순위</th><th>조합</th><th>인터넷 실질 요금</th><th>절약 금액</th></tr></thead><tbody><tr><td>1</td><td>SK 500M + SKT 5G 요금제</td><td>17,600원</td><td>-7,700원</td></tr><tr><td>2</td><td>LG 500M + LG 5G 요금제</td><td>18,700원</td><td>-7,700원</td></tr><tr><td>3</td><td>KT 500M + KT 5G 요금제</td><td>19,800원</td><td>-7,700원</td></tr><tr><td>4</td><td>SK 500M + SKT + Btv</td><td>14,300원</td><td>-11,000원</td></tr><tr><td>5</td><td>LG 500M + LG + U+tv</td><td>15,400원</td><td>-11,000원</td></tr></tbody></table>"), ("최저가 인터넷 가입 전략", "<ol><li><strong>가격만 보면</strong>: 알뜰 인터넷 100M (월 16,500원, 약정 없음)</li><li><strong>속도+가격 균형</strong>: SK 500M 3년 약정 (월 25,300원)</li><li><strong>결합할인 극대화</strong>: 인터넷 + 모바일 + TV 3중 결합 (월 14,000~15,000원)</li></ol>"), ("인터넷 요금 비교 시 주의할 점", "<ul><li><strong>프로모션 가격 vs 정상 가격</strong>: 처음 6개월만 할인되고 이후 정상가로 복귀하는 요금제가 있습니다.</li><li><strong>부가서비스 자동 가입</strong>: 가입 시 부가서비스(보안, 클라우드 등)가 자동 추가되어 요금이 올라갈 수 있습니다.</li><li><strong>설치비·공유기 비용</strong>: 무약정이나 알뜰 인터넷은 설치비·공유기 비용이 별도일 수 있습니다.</li></ul>")], "faq": [("인터넷 요금이 매달 다르게 나오는 이유는?", "부가서비스 요금, TV 유료 채널 결제, 프로모션 기간 종료 등이 원인입니다. <strong>통신사 앱에서 청구 내역을 확인</strong>하고 불필요한 부가서비스를 해지하세요."), ("비교 사이트마다 가격이 다른 이유는?", "사은품 포함 여부, 프로모션 적용 여부, 약정 기간 차이 등으로 가격이 다르게 표시됩니다. <strong>월 실납부 금액</strong>을 기준으로 비교하세요."), ("가장 저렴한 인터넷은 어디서 가입하나요?", "인터넷 비교 사이트(플랜J 등)에서 가입하면 대리점보다 더 큰 <strong>현금 사은품</strong>을 받을 수 있어 실질적으로 가장 저렴합니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 9. 인터넷 TV 휴대폰 결합할인
    {"title": "인터넷 TV 휴대폰 결합할인 통신사별 비교 총정리", "cat": CAT_INTERNET, "slug": "internet-tv-mobile-bundle", "intro": "인터넷, TV, 휴대폰을 같은 통신사로 묶으면 <strong>결합할인</strong>으로 월 수만 원을 절약할 수 있습니다. 하지만 통신사마다 결합 조건과 할인 금액이 다르고, 결합 수가 많을수록 할인이 커지는 구조라 꼼꼼한 비교가 필요합니다. 3대 통신사의 결합할인을 완벽 비교합니다.", "sections": [("결합할인 기본 구조", "<p>결합할인은 <strong>같은 통신사의 상품을 2개 이상 묶을 때</strong> 적용됩니다.</p><ul><li><strong>2중 결합</strong>: 인터넷 + 모바일 또는 인터넷 + TV → 월 5,000~8,000원 할인</li><li><strong>3중 결합</strong>: 인터넷 + 모바일 + TV → 월 10,000~15,000원 할인</li><li><strong>가족 결합</strong>: 가족 회선을 추가할수록 할인 증가 (최대 5회선)</li></ul>"), ("통신사별 결합할인 비교표", "<table><thead><tr><th>결합 유형</th><th>KT</th><th>SK</th><th>LG U+</th></tr></thead><tbody><tr><td>인터넷+모바일</td><td>월 5,500원</td><td>월 5,500원</td><td>월 5,500원</td></tr><tr><td>인터넷+TV</td><td>월 4,400원</td><td>월 4,400원</td><td>월 4,400원</td></tr><tr><td>인터넷+모바일+TV</td><td>월 11,000원</td><td>월 11,000원</td><td>월 11,000원</td></tr><tr><td>가족 1회선 추가</td><td>월 2,200원</td><td>월 2,200원</td><td>월 2,200원</td></tr><tr><td>가족 최대(5회선)</td><td>월 19,800원</td><td>월 18,700원</td><td>월 19,250원</td></tr></tbody></table>"), ("4인 가족 결합할인 예시", "<p>4인 가족(부모+자녀2)이 인터넷+TV+모바일 4회선을 결합하면:</p><ul><li><strong>인터넷 500M</strong>: 27,500원 → 결합 후 약 16,500원 (11,000원 할인)</li><li><strong>모바일 4회선 추가 할인</strong>: 월 8,800원 추가 할인</li><li><strong>총 월 절약</strong>: 약 <strong>19,800원</strong></li><li><strong>연간 절약</strong>: 약 <strong>237,600원</strong></li></ul>"), ("결합할인 주의사항", "<ul><li><strong>모바일 요금제 조건</strong>: 결합할인은 일정 금액 이상의 모바일 요금제에만 적용됩니다. 알뜰폰은 결합 불가인 경우가 많습니다.</li><li><strong>1회선 해지 시 전체 할인 변동</strong>: 결합 중 1회선이라도 해지하면 할인 조건이 변경됩니다.</li><li><strong>약정 기간 불일치</strong>: 인터넷(3년)과 모바일(2년)의 약정이 다르면 해지 시점에 주의하세요.</li></ul>")], "faq": [("알뜰폰도 인터넷 결합할인이 되나요?", "대부분 <strong>불가</strong>합니다. 결합할인은 같은 통신사(KT-KT, SKT-SK브로드밴드, LG-LG U+)끼리만 적용됩니다. 일부 알뜰폰은 모회사 인터넷과 제한적 결합이 가능합니다."), ("결합할인 중 통신사를 바꿀 수 있나요?", "가능하지만 <strong>기존 결합할인이 해지</strong>되고 각 상품의 위약금이 발생할 수 있습니다. 모든 약정이 만료되는 시점에 한꺼번에 변경하는 것이 유리합니다."), ("1인 가구도 결합할인이 되나요?", "<strong>네</strong>, 인터넷 + 본인 모바일 2중 결합만으로도 월 5,500원 할인됩니다. TV까지 추가하면 3중 결합으로 11,000원 할인이 가능합니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 10. KT 결합할인
    {"title": "KT 결합할인 종류 조건 최대 할인 받는 방법", "cat": CAT_INTERNET, "slug": "kt-bundle-discount", "intro": "KT는 인터넷, 모바일, TV, 전화를 결합하는 <strong>KT 결합할인</strong> 상품을 운영하고 있습니다. 결합 수가 많을수록 할인이 커지며, 가족 회선까지 포함하면 월 2만 원 이상 절약이 가능합니다. KT 결합할인의 종류, 조건, 최대 할인 방법을 총정리합니다.", "sections": [("KT 결합할인 종류", "<table><thead><tr><th>결합 유형</th><th>구성</th><th>월 할인</th></tr></thead><tbody><tr><td>2중 결합 (인터넷+모바일)</td><td>KT 인터넷 + KT 모바일</td><td>5,500원</td></tr><tr><td>2중 결합 (인터넷+TV)</td><td>KT 인터넷 + 올레tv</td><td>4,400원</td></tr><tr><td>3중 결합</td><td>인터넷 + 모바일 + TV</td><td>11,000원</td></tr><tr><td>4중 결합</td><td>인터넷 + 모바일 + TV + 전화</td><td>13,200원</td></tr><tr><td>가족 결합</td><td>모바일 회선 추가 (최대 5)</td><td>회선당 2,200원</td></tr></tbody></table>"), ("KT 결합할인 조건", "<ul><li><strong>모바일 요금제</strong>: 월 35,000원 이상 요금제 사용 시 최대 할인 적용</li><li><strong>인터넷 속도</strong>: 500Mbps 이상 가입 시 할인 금액이 커짐</li><li><strong>약정</strong>: 인터넷 3년 약정 시 추가 할인</li><li><strong>가족 등록</strong>: 가족 관계 증빙(주민등록등본) 필요</li></ul>"), ("KT 결합할인 극대화 전략", "<ol><li><strong>가족 전원 KT로 통일</strong>: 4인 가족 기준 인터넷+TV+모바일 4회선 결합 시 월 약 20,000원 절약</li><li><strong>올레tv 기본형 추가</strong>: TV를 보지 않아도 기본형(월 5,500원)을 추가하면 3중 결합 할인(11,000원)이 적용되어 오히려 이득입니다.</li><li><strong>인터넷전화 추가</strong>: 집전화가 필요하면 인터넷전화(월 1,100원)를 추가하여 4중 결합 할인을 받으세요.</li></ol>"), ("KT 결합 시뮬레이션", "<p>4인 가족이 KT로 모두 결합한 경우:</p><ul><li>인터넷 500M: 27,500원 → <strong>16,500원</strong></li><li>올레tv 베이직: 5,500원 → 결합 후 사실상 <strong>무료</strong></li><li>모바일 4회선 추가 할인: <strong>-8,800원</strong></li><li>월 총 절약: 약 <strong>19,800원</strong> | 연간 약 <strong>237,600원</strong></li></ul>")], "faq": [("KT 모바일이 아닌데 KT 인터넷 결합이 되나요?", "KT 인터넷 + KT TV 결합은 가능하지만, <strong>모바일 결합할인은 KT 모바일만</strong> 가능합니다."), ("결합 중 1회선만 해지하면 어떻게 되나요?", "결합 구성이 변경되어 <strong>할인 금액이 줄어듭니다</strong>. 3중 결합에서 TV를 해지하면 2중 결합 할인으로 변경됩니다."), ("올레tv를 안 보는데도 결합하는 게 이득인가요?", "기본형(월 5,500원) 추가 시 3중 결합 할인(11,000원)이 적용되므로 <strong>오히려 5,500원 이득</strong>입니다. TV를 보지 않아도 결합하는 것이 유리합니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 11. SK 결합할인
    {"title": "SK 결합할인 종류 조건 인터넷 휴대폰 묶음 비교", "cat": CAT_INTERNET, "slug": "sk-bundle-discount", "intro": "SKT 모바일을 사용하고 있다면 <strong>SK브로드밴드 인터넷</strong>과 결합하여 월 수만 원을 절약할 수 있습니다. SK 결합할인의 종류, 조건, 최대 할인 받는 방법을 총정리합니다.", "sections": [("SK 결합할인 종류와 할인 금액", "<table><thead><tr><th>결합 유형</th><th>구성</th><th>월 할인</th></tr></thead><tbody><tr><td>2중 결합</td><td>SK인터넷 + SKT모바일</td><td>5,500원</td></tr><tr><td>인터넷+TV</td><td>SK인터넷 + Btv</td><td>4,400원</td></tr><tr><td>3중 결합</td><td>인터넷 + 모바일 + TV</td><td>11,000원</td></tr><tr><td>가족결합 추가</td><td>SKT 회선 추가</td><td>회선당 2,200원</td></tr></tbody></table>"), ("SK 결합이 유리한 경우", "<ul><li>가족 중 SKT 모바일 사용자가 2명 이상일 때</li><li>Btv 콘텐츠(시즌, 푹)를 즐기는 가정</li><li>SK 인터넷이 해당 지역에서 가장 저렴할 때</li><li>T멤버십 혜택을 적극 활용하는 분</li></ul>"), ("SK 결합할인 극대화 전략", "<ol><li><strong>Btv 기본형 추가</strong>: 월 5,500원에 Btv를 추가하면 3중 결합(11,000원 할인)이 적용되어 순이득 5,500원입니다.</li><li><strong>T멤버십 연계</strong>: SKT 모바일 + SK 인터넷 결합 시 T멤버십 등급이 올라가 추가 혜택을 받을 수 있습니다.</li><li><strong>가족 회선 최대 등록</strong>: SKT 사용 가족을 모두 결합하여 회선당 2,200원 추가 할인을 받으세요.</li></ol>"), ("SK vs KT vs LG 결합할인 비교", "<p>같은 500M 인터넷 + 모바일 + TV 3중 결합 기준:</p><table><thead><tr><th>항목</th><th>SK</th><th>KT</th><th>LG</th></tr></thead><tbody><tr><td>인터넷 기본가</td><td>25,300원</td><td>27,500원</td><td>26,400원</td></tr><tr><td>3중 결합 할인</td><td>-11,000원</td><td>-11,000원</td><td>-11,000원</td></tr><tr><td>실질 인터넷 요금</td><td>14,300원</td><td>16,500원</td><td>15,400원</td></tr></tbody></table><p>SK브로드밴드의 기본가가 가장 저렴하므로 결합 후에도 SK가 최저가입니다.</p>")], "faq": [("SKT 알뜰폰도 SK 인터넷 결합이 되나요?", "SKT 망을 사용하는 알뜰폰은 <strong>결합 대상이 아닙니다</strong>. SKT 직접 가입 모바일만 결합할인이 적용됩니다."), ("SK브로드밴드 인터넷 품질은 KT와 차이가 있나요?", "도시 지역에서는 <strong>체감 차이가 거의 없습니다</strong>. SK는 일부 구간에서 KT 회선을 임대하지만, 최종 사용자 체감 속도에 큰 영향은 없습니다."), ("Btv와 올레tv 중 어떤 것이 좋나요?", "콘텐츠 취향에 따라 다릅니다. Btv는 <strong>시즌·푹 독점 콘텐츠</strong>가 강점이고, 올레tv는 <strong>채널 수</strong>가 많습니다. 결합할인 금액은 동일합니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 12. LG U+ 결합할인
    {"title": "LG U+ 결합할인 종류 조건 가족결합 총정리", "cat": CAT_INTERNET, "slug": "lg-bundle-discount", "intro": "LG U+는 인터넷, IPTV, 모바일을 결합하는 <strong>U+ 결합할인</strong>을 운영합니다. 특히 U+tv는 넷플릭스가 기본 포함된 요금제가 있어 OTT 비용까지 절약할 수 있는 것이 차별점입니다. LG U+ 결합할인을 총정리합니다.", "sections": [("LG U+ 결합할인 종류", "<table><thead><tr><th>결합 유형</th><th>구성</th><th>월 할인</th></tr></thead><tbody><tr><td>2중 결합</td><td>인터넷 + LG모바일</td><td>5,500원</td></tr><tr><td>인터넷+TV</td><td>인터넷 + U+tv</td><td>4,400원</td></tr><tr><td>3중 결합</td><td>인터넷 + 모바일 + TV</td><td>11,000원</td></tr><tr><td>가족결합</td><td>LG모바일 추가</td><td>회선당 2,200원</td></tr></tbody></table>"), ("LG U+만의 차별점: 넷플릭스 포함 IPTV", "<p>LG U+tv 프리미엄 이상 요금제에는 <strong>넷플릭스가 기본 포함</strong>되어 있습니다.</p><ul><li>U+tv 프리미엄: 월 14,300원 (넷플릭스 광고형 포함)</li><li>넷플릭스 별도 가입 시 월 5,500원 추가 비용</li><li>U+tv + 인터넷 결합 시 넷플릭스 비용을 절약하면서 결합할인까지 적용</li></ul><p>넷플릭스를 구독 중이라면 LG U+tv 결합이 다른 통신사보다 실질적으로 더 저렴할 수 있습니다.</p>"), ("LG U+ 결합할인 극대화 전략", "<ol><li><strong>U+tv 프리미엄 결합</strong>: 넷플릭스 비용 절약 + 3중 결합 할인으로 월 16,500원 이상 절약 가능</li><li><strong>가족 결합</strong>: LG모바일 사용 가족을 등록하면 회선당 2,200원 추가 할인</li><li><strong>IoT 패키지</strong>: LG U+의 스마트홈 IoT 기기와 결합하면 추가 할인이 적용됩니다.</li></ol>"), ("LG U+가 유리한 사람", "<ul><li>넷플릭스를 이미 구독 중이거나 구독 예정인 분</li><li>LG 모바일 사용자 (결합할인 극대화)</li><li>스마트홈 IoT 기기를 사용하는 분</li><li>U+tv의 다양한 콘텐츠(아이들나라 등)가 필요한 가정</li></ul>")], "faq": [("LG U+tv에 넷플릭스가 정말 무료로 포함되나요?", "U+tv 프리미엄 이상 요금제에 <strong>넷플릭스 광고형이 포함</strong>됩니다. 광고 없는 스탠다드 이상은 추가 요금이 발생합니다."), ("LG 알뜰폰도 결합되나요?", "LG U+ 직접 가입 모바일만 결합 대상입니다. <strong>LG망 알뜰폰은 결합 불가</strong>입니다."), ("LG U+의 10Gbps 인터넷은 어디서 쓸 수 있나요?", "수도권 및 주요 도시 일부 아파트에서 제공됩니다. <strong>LG U+ 홈페이지에서 주소를 입력</strong>하면 제공 여부를 확인할 수 있습니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 13. 가족결합 할인
    {"title": "가족결합 할인 통신사별 비교 4인 가족 최대 할인", "cat": CAT_INTERNET, "slug": "family-bundle-discount", "intro": "가족 구성원의 인터넷과 휴대폰을 같은 통신사로 묶으면 <strong>가족결합 할인</strong>으로 월 수만 원을 절약할 수 있습니다. 가족 수가 많을수록 할인이 커지며, 4인 가족 기준 월 2만 원 이상 절약이 가능합니다.", "sections": [("통신사별 가족결합 할인 비교", "<table><thead><tr><th>가족 수</th><th>KT</th><th>SK</th><th>LG U+</th></tr></thead><tbody><tr><td>2인 (3중결합+1회선)</td><td>월 13,200원</td><td>월 13,200원</td><td>월 13,200원</td></tr><tr><td>3인 (3중결합+2회선)</td><td>월 15,400원</td><td>월 15,400원</td><td>월 15,400원</td></tr><tr><td>4인 (3중결합+3회선)</td><td>월 17,600원</td><td>월 17,600원</td><td>월 17,600원</td></tr><tr><td>5인 (3중결합+4회선)</td><td>월 19,800원</td><td>월 18,700원</td><td>월 19,250원</td></tr></tbody></table>"), ("가족결합 등록 방법", "<ol><li><strong>가족 관계 증빙</strong>: 주민등록등본 또는 가족관계증명서가 필요합니다.</li><li><strong>등록 방법</strong>: 통신사 앱, 홈페이지, 대리점, 고객센터에서 등록 가능</li><li><strong>등록 시점</strong>: 등록 다음 달부터 할인 적용 (일부 통신사 당월 적용)</li><li><strong>해외 거주 가족</strong>: 국내 모바일 회선이 있어야 결합 가능</li></ol>"), ("가족결합 시 통신사 선택 기준", "<ul><li><strong>가족 중 가장 많이 쓰는 통신사</strong>로 통일하면 번호이동 비용을 최소화할 수 있습니다.</li><li><strong>인터넷 기본가가 가장 저렴한 SK</strong>가 결합 후에도 총 비용이 가장 낮습니다.</li><li><strong>넷플릭스를 보는 가정</strong>은 LG U+(넷플릭스 포함 IPTV)가 실질적으로 유리합니다.</li><li><strong>안정성 우선</strong>이면 KT 자체 회선이 가장 안정적입니다.</li></ul>"), ("가족결합 주의사항", "<ul><li><strong>가족 1인 이탈 시</strong>: 번호이동이나 해지하면 결합할인 구조가 변경되어 전체 할인이 줄어듭니다.</li><li><strong>자녀 독립 시</strong>: 자녀가 분가하면 가족결합에서 빠지게 되어 할인이 줄어듭니다.</li><li><strong>약정 기간 불일치</strong>: 가족 각자의 모바일 약정 만료 시점이 다르면 동시 전환이 어렵습니다.</li></ul>")], "faq": [("부모님이 다른 통신사인데 결합이 되나요?", "<strong>안 됩니다.</strong> 가족결합은 같은 통신사 회선끼리만 가능합니다. 부모님의 통신사를 변경(번호이동)해야 합니다."), ("자녀가 알뜰폰을 쓰는데 가족결합이 되나요?", "알뜰폰은 <strong>가족결합 대상이 아닙니다</strong>. 대형 통신사(KT, SKT, LG U+) 직접 가입 회선만 가능합니다."), ("결혼 후 배우자도 가족결합에 추가할 수 있나요?", "<strong>네</strong>, 혼인관계증명서를 제출하면 배우자도 가족결합에 추가할 수 있습니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 14. 2인 가족 결합할인
    {"title": "2인 가족 결합할인 추천 부부 최적 조합 비교", "cat": CAT_INTERNET, "slug": "couple-bundle-discount", "intro": "신혼부부나 2인 가구도 <strong>결합할인</strong>으로 통신비를 크게 줄일 수 있습니다. 2인 가족에게 최적의 인터넷+모바일+TV 결합 조합을 비교하여 추천합니다.", "sections": [("2인 가족 결합할인 시뮬레이션", "<p>부부 2인이 인터넷+TV+모바일 2회선을 결합한 경우:</p><table><thead><tr><th>항목</th><th>결합 전</th><th>결합 후</th><th>절약</th></tr></thead><tbody><tr><td>인터넷 500M</td><td>27,500원</td><td>16,500원</td><td>-11,000원</td></tr><tr><td>TV 기본형</td><td>5,500원</td><td>실질 0원</td><td>-5,500원</td></tr><tr><td>모바일 2회선</td><td>변동 없음</td><td>-2,200원</td><td>-2,200원</td></tr><tr><td><strong>월 합계</strong></td><td></td><td></td><td><strong>-18,700원</strong></td></tr></tbody></table><p>연간 약 <strong>224,400원</strong> 절약 가능합니다.</p>"), ("2인 가족 추천 결합 조합", "<ul><li><strong>가성비 최우선</strong>: SK 500M + Btv 기본 + SKT 모바일 2회선 → 월 약 14,300원 (인터넷)</li><li><strong>넷플릭스 포함</strong>: LG 500M + U+tv 프리미엄 + LG 모바일 2회선 → 넷플릭스 포함으로 OTT 비용 절약</li><li><strong>안정성 + 콘텐츠</strong>: KT 500M + 올레tv + KT 모바일 2회선 → 가장 안정적인 회선</li></ul>"), ("2인 가족 통신비 추가 절약 팁", "<ol><li><strong>모바일 요금제 재검토</strong>: 실제 데이터 사용량을 확인하고 과도한 요금제를 낮추세요.</li><li><strong>부가서비스 정리</strong>: 사용하지 않는 부가서비스(보안, 클라우드 등)를 해지하세요.</li><li><strong>TV 유료채널 정리</strong>: 보지 않는 유료 채널 구독을 해지하세요.</li><li><strong>공유기 성능 확인</strong>: 통신사 기본 공유기 대신 고성능 공유기로 교체하면 속도가 개선됩니다.</li></ol>"), ("맞벌이 부부 vs 외벌이 가정 전략 차이", "<ul><li><strong>맞벌이</strong>: 각자 재택근무 가능성 → 500Mbps 이상 권장, 화상회의 품질 중요</li><li><strong>외벌이</strong>: 집에서 한 명이 주로 사용 → 100~500Mbps 충분, 요금 절약 우선</li></ul>")], "faq": [("부부가 다른 통신사를 쓰는데 어떻게 해야 하나요?", "한 쪽이 <strong>번호이동</strong>하여 같은 통신사로 통일해야 결합할인을 받을 수 있습니다. 번호이동은 무료이며, 기존 번호 그대로 유지됩니다."), ("신혼집 이사 시 인터넷을 새로 가입해야 하나요?", "기존 인터넷이 있으면 <strong>이전 설치</strong>(같은 통신사)가 가능합니다. 새 집에서 통신사를 바꾸고 싶다면 기존 해지 후 신규 가입합니다."), ("2인 가족도 TV가 없이 2중 결합만 해도 되나요?", "<strong>네</strong>, 인터넷+모바일 2중 결합으로도 월 5,500원 할인됩니다. 다만 TV 기본형을 추가하면 3중 결합 할인(11,000원)이 적용되어 오히려 이득입니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 15. 결합 vs 단독 비교
    {"title": "인터넷 결합할인 vs 단독 가입 어떤 것이 저렴할까", "cat": CAT_INTERNET, "slug": "bundle-vs-single-internet", "intro": "인터넷을 가입할 때 <strong>결합할인</strong>을 받는 것이 항상 유리할까요? 결합할인은 조건이 복잡하고, 해지 시 불이익이 있어 단독 가입이 나은 경우도 있습니다. 결합할인과 단독 가입의 장단점을 비교하여 나에게 맞는 방법을 찾아보겠습니다.", "sections": [("결합할인 vs 단독 비교표", "<table><thead><tr><th>항목</th><th>결합할인</th><th>단독 가입</th></tr></thead><tbody><tr><td>월 요금</td><td>저렴 (할인 적용)</td><td>비쌈 (정가)</td></tr><tr><td>유연성</td><td>낮음 (통신사 묶임)</td><td>높음 (자유롭게 변경)</td></tr><tr><td>해지 시</td><td>전체 할인 구조 변동</td><td>해당 상품만 해지</td></tr><tr><td>적합한 사람</td><td>장기 거주, 가족 다수</td><td>자주 이사, 1인 가구</td></tr></tbody></table>"), ("결합할인이 유리한 경우", "<ul><li>가족 2인 이상이 같은 통신사를 사용할 때</li><li>인터넷 + TV를 모두 사용할 때</li><li>3년 이상 같은 곳에 거주할 때</li><li>통신사 변경 계획이 없을 때</li></ul>"), ("단독 가입이 유리한 경우", "<ul><li><strong>알뜰폰 사용자</strong>: 결합 대상이 아니므로 단독 가입이 불가피</li><li><strong>자주 이사하는 1인 가구</strong>: 무약정 알뜰 인터넷이 더 저렴</li><li><strong>TV를 보지 않는 경우</strong>: 2중 결합(인터넷+모바일)만으로는 할인이 크지 않아 알뜰 인터넷이 유리할 수 있음</li><li><strong>통신사 변경을 자주 하는 경우</strong>: 결합 시 해지가 복잡해짐</li></ul>"), ("실제 비용 비교 시뮬레이션", "<p><strong>1인 가구, 알뜰폰 사용 시:</strong></p><table><thead><tr><th>방법</th><th>인터넷</th><th>휴대폰</th><th>월 합계</th></tr></thead><tbody><tr><td>SK 결합 (SK인터넷+SKT모바일)</td><td>19,800원</td><td>55,000원</td><td>74,800원</td></tr><tr><td>알뜰인터넷 + 알뜰폰</td><td>16,500원</td><td>20,000원</td><td>36,500원</td></tr></tbody></table><p>알뜰폰+알뜰인터넷 조합이 월 <strong>38,300원 저렴</strong>합니다. 결합할인이 항상 유리한 것은 아닙니다.</p>")], "faq": [("알뜰폰을 쓰면 결합할인을 아예 못 받나요?", "대부분 <strong>불가</strong>합니다. 하지만 알뜰폰 + 알뜰인터넷 조합이 대형 통신사 결합보다 총 비용이 더 저렴한 경우가 많습니다."), ("결합할인 중에 통신사를 바꾸면 위약금이 있나요?", "결합할인 자체에는 위약금이 없지만, <strong>인터넷 약정 위약금</strong>이 발생합니다. 약정 만료 후 변경하면 위약금 없이 가능합니다."), ("1인 가구는 어떤 방법이 좋나요?", "알뜰폰을 쓴다면 <strong>알뜰인터넷 단독 가입</strong>이 가장 저렴합니다. 대형 통신사 모바일을 쓴다면 <strong>2중 결합</strong>(인터넷+모바일)이 유리합니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 16. IPTV 요금제 비교
    {"title": "IPTV 요금제 비교 KT 올레 SK Btv LG U+ 총정리", "cat": CAT_INTERNET, "slug": "iptv-plan-comparison", "intro": "TV를 보려면 <strong>IPTV(올레tv, Btv, U+tv)</strong> 중 하나를 선택해야 합니다. 채널 수, 월 요금, 부가 콘텐츠(넷플릭스, 디즈니+ 등)가 통신사마다 다르기 때문에 비교가 필요합니다. 3대 IPTV의 요금과 혜택을 총정리합니다.", "sections": [("IPTV 요금제 비교표", "<table><thead><tr><th>요금제</th><th>올레tv (KT)</th><th>Btv (SK)</th><th>U+tv (LG)</th></tr></thead><tbody><tr><td>기본형</td><td>월 5,500원 / 90ch</td><td>월 5,500원 / 85ch</td><td>월 5,500원 / 88ch</td></tr><tr><td>스탠다드</td><td>월 9,900원 / 170ch</td><td>월 9,900원 / 155ch</td><td>월 9,900원 / 160ch</td></tr><tr><td>프리미엄</td><td>월 14,300원 / 220ch</td><td>월 14,300원 / 200ch</td><td>월 14,300원 / 210ch + 넷플릭스</td></tr></tbody></table>"), ("IPTV별 차별 포인트", "<ul><li><strong>올레tv</strong>: 채널 수 최다, 시즌2 독점 콘텐츠, KT 결합 시 최적</li><li><strong>Btv</strong>: 푹(Pooq) 연계, 시즌(Seezn) 콘텐츠, SK 결합 시 최적</li><li><strong>U+tv</strong>: 넷플릭스 기본 포함(프리미엄), 아이들나라, LG 결합 시 최적</li></ul>"), ("IPTV + 인터넷 결합 시 실질 요금", "<p>IPTV는 인터넷과 결합하면 큰 할인을 받을 수 있습니다.</p><ul><li>인터넷 500M + IPTV 기본형: 인터넷 단독 대비 <strong>실질 TV 무료</strong> (3중 결합 할인이 TV 요금보다 큼)</li><li>결합 없이 IPTV만 가입: 비추천 (할인이 없어 비쌈)</li></ul>"), ("IPTV 선택 가이드", "<ul><li><strong>채널 많이 보는 분</strong> → 올레tv (채널 최다)</li><li><strong>넷플릭스 구독자</strong> → U+tv (넷플릭스 포함)</li><li><strong>SKT 사용자</strong> → Btv (결합 할인 극대화)</li><li><strong>어린이 있는 가정</strong> → U+tv (아이들나라 콘텐츠)</li></ul>")], "faq": [("IPTV 없이 인터넷만 써도 되나요?", "<strong>네</strong>, IPTV 없이 인터넷만 단독 가입 가능합니다. 다만 결합 시 IPTV 기본형(5,500원)을 추가하면 할인이 더 크므로 손해가 아닙니다."), ("IPTV와 넷플릭스 둘 다 필요한가요?", "IPTV는 실시간 채널(뉴스, 스포츠), 넷플릭스는 VOD(드라마, 영화)로 <strong>용도가 다릅니다</strong>. 둘 다 쓴다면 U+tv 프리미엄(넷플릭스 포함)이 가장 경제적입니다."), ("IPTV 셋톱박스는 무료인가요?", "대부분 <strong>임대(월 3,300~5,500원)</strong> 방식입니다. 기본형 요금에 셋톱박스 임대료가 포함된 경우가 많으니 약관을 확인하세요.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 17. 인터넷 TV 결합 요금 비교
    {"title": "인터넷 TV 결합 요금 비교 채널 수 가격 총정리", "cat": CAT_INTERNET, "slug": "internet-tv-bundle-price", "intro": "인터넷과 TV를 함께 결합하면 할인을 받을 수 있습니다. 하지만 <strong>인터넷 속도, TV 채널 수, 결합 조건</strong>에 따라 요금이 다르므로 꼼꼼한 비교가 필요합니다. 통신사별 인터넷+TV 결합 요금을 비교합니다.", "sections": [("인터넷+TV 결합 요금 비교표 (500M 기준)", "<table><thead><tr><th>통신사</th><th>인터넷 500M + TV 기본</th><th>인터넷 500M + TV 프리미엄</th></tr></thead><tbody><tr><td>KT</td><td>월 28,600원</td><td>월 37,400원</td></tr><tr><td>SK</td><td>월 26,400원</td><td>월 35,200원</td></tr><tr><td>LG U+</td><td>월 27,500원</td><td>월 36,300원 (넷플릭스 포함)</td></tr></tbody></table><p>※ 3년 약정, 인터넷+TV 2중 결합할인 적용 기준</p>"), ("인터넷+TV vs 인터넷만 비교", "<p>인터넷만 가입하는 것과 TV를 추가 결합하는 것의 비용 차이:</p><table><thead><tr><th>방법</th><th>월 요금</th><th>비고</th></tr></thead><tbody><tr><td>인터넷 500M 단독</td><td>25,300~27,500원</td><td>결합할인 없음</td></tr><tr><td>인터넷 500M + TV 기본</td><td>26,400~28,600원</td><td>결합할인 적용</td></tr><tr><td>차이</td><td>+1,100원</td><td>TV 실질 1,100원에 추가</td></tr></tbody></table><p>TV 기본형이 결합할인 덕분에 <strong>실질 월 1,100원</strong>에 추가되는 셈입니다. 결합 구조를 잘 활용하면 TV가 거의 공짜입니다.</p>"), ("채널 수 비교: 기본형 vs 프리미엄", "<ul><li><strong>기본형 (85~90ch)</strong>: 지상파, 종합편성, 주요 케이블 채널. 기본적인 TV 시청에 충분합니다.</li><li><strong>스탠다드 (155~170ch)</strong>: 스포츠, 영화, 어린이 채널 추가. 가족이 다양한 채널을 보는 가정에 적합.</li><li><strong>프리미엄 (200~220ch)</strong>: 해외 채널, 프리미엄 영화, 넷플릭스(LG U+) 포함. 채널을 많이 보는 분에게 추천.</li></ul>"), ("인터넷+TV 결합 추천 조합", "<ul><li><strong>최저가</strong>: SK 500M + Btv 기본 → 월 26,400원</li><li><strong>가성비</strong>: LG 500M + U+tv 프리미엄(넷플릭스 포함) → 월 36,300원</li><li><strong>채널 최다</strong>: KT 500M + 올레tv 프리미엄 → 월 37,400원</li></ul>")], "faq": [("TV를 거의 안 보는데 결합해야 하나요?", "TV를 안 봐도 <strong>기본형(5,500원)을 추가</strong>하면 3중 결합 할인이 적용되어 오히려 이득입니다. TV를 켜지 않아도 할인만 받으세요."), ("IPTV 대신 OTT(넷플릭스, 웨이브)만 보면 안 되나요?", "가능합니다. 실시간 TV를 보지 않으면 IPTV 없이 <strong>인터넷 단독 + OTT 구독</strong>이 더 경제적일 수 있습니다. 다만 3중 결합 할인을 포기해야 합니다."), ("셋톱박스 없이 스마트TV로 볼 수 있나요?", "일부 스마트TV에서 IPTV 앱을 지원하지만, <strong>셋톱박스가 있어야 전체 채널</strong>을 이용할 수 있습니다. 앱으로는 일부 채널만 시청 가능합니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 18. IPTV vs OTT
    {"title": "IPTV vs OTT 비교 TV 꼭 필요할까 해지해도 될까", "cat": CAT_INTERNET, "slug": "iptv-vs-ott", "intro": "넷플릭스, 웨이브, 티빙 등 <strong>OTT 서비스</strong>가 늘면서 IPTV 해지를 고민하는 분이 많습니다. IPTV와 OTT의 장단점을 비교하고, 어떤 경우에 IPTV를 유지하고 어떤 경우에 해지하는 것이 유리한지 안내합니다.", "sections": [("IPTV vs OTT 완벽 비교", "<table><thead><tr><th>항목</th><th>IPTV</th><th>OTT</th></tr></thead><tbody><tr><td>콘텐츠</td><td>실시간 채널 + VOD</td><td>VOD 위주</td></tr><tr><td>실시간 뉴스·스포츠</td><td>가능</td><td>일부만 가능</td></tr><tr><td>월 요금</td><td>5,500~14,300원</td><td>5,500~17,000원</td></tr><tr><td>약정</td><td>인터넷과 묶여 있음</td><td>없음 (월 단위 해지)</td></tr><tr><td>기기</td><td>셋톱박스 + TV</td><td>스마트폰, 태블릿, TV</td></tr><tr><td>결합할인</td><td>가능</td><td>불가</td></tr></tbody></table>"), ("IPTV를 유지해야 하는 경우", "<ul><li>실시간 뉴스, 스포츠 중계를 즐기는 분</li><li>부모님·어르신이 리모컨으로 채널 돌리기를 선호하는 가정</li><li>인터넷+TV 결합으로 실질 TV 무료인 경우</li><li>어린이 전용 채널이 필요한 가정</li></ul>"), ("OTT로 대체해도 되는 경우", "<ul><li>드라마·영화 VOD만 보는 분</li><li>1인 가구로 TV를 거의 보지 않는 분</li><li>이미 넷플릭스·티빙 등 OTT를 구독 중인 분</li><li>결합할인이 없어서 IPTV 유지 비용이 큰 경우</li></ul>"), ("IPTV 해지 시 결합할인 영향", "<p>IPTV를 해지하면 3중 결합이 2중 결합으로 변경되어 할인이 줄어듭니다.</p><ul><li>3중 결합 할인: 월 11,000원</li><li>2중 결합(인터넷+모바일)으로 변경: 월 5,500원</li><li>할인 감소분: 월 5,500원</li><li>IPTV 기본형 요금: 월 5,500원</li></ul><p><strong>결론</strong>: IPTV 기본형(5,500원)을 해지해도 결합 할인이 5,500원 줄어 실질 절약 금액은 0원입니다. 기본형은 해지하지 않는 것이 유리합니다.</p>")], "faq": [("IPTV를 해지하면 인터넷 요금이 올라가나요?", "IPTV 해지 자체로 인터넷 요금이 오르지는 않지만, <strong>결합할인 구조가 변경</strong>되어 전체 할인이 줄어듭니다."), ("OTT만으로 실시간 TV를 볼 수 있나요?", "티빙, 웨이브 등에서 일부 실시간 채널을 제공하지만, <strong>지상파·종편 전체를 보려면 IPTV가 필요</strong>합니다."), ("셋톱박스를 반납해야 하나요?", "IPTV 해지 시 <strong>셋톱박스를 반납</strong>해야 합니다. 미반납 시 기기 비용이 청구될 수 있으니 택배 또는 방문 수거를 요청하세요.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 19. 인터넷만 단독 가입
    {"title": "인터넷만 단독 가입 방법 TV 없이 저렴하게 쓰기", "cat": CAT_INTERNET, "slug": "internet-only-no-tv", "intro": "TV를 보지 않는 분이라면 <strong>인터넷만 단독</strong>으로 가입하여 비용을 절약할 수 있습니다. IPTV 없이 인터넷만 가입하는 방법, 요금, 주의사항을 안내합니다.", "sections": [("인터넷만 단독 가입 요금 비교", "<table><thead><tr><th>요금제</th><th>속도</th><th>월 요금 (3년)</th><th>통신사</th></tr></thead><tbody><tr><td>SK 라이트</td><td>100Mbps</td><td>19,800원</td><td>SK</td></tr><tr><td>LG 베이직</td><td>100Mbps</td><td>20,900원</td><td>LG</td></tr><tr><td>KT 슬림</td><td>100Mbps</td><td>22,000원</td><td>KT</td></tr><tr><td>SK 스탠다드</td><td>500Mbps</td><td>25,300원</td><td>SK</td></tr><tr><td>LG 스탠다드</td><td>500Mbps</td><td>26,400원</td><td>LG</td></tr><tr><td>알뜰 인터넷</td><td>100Mbps</td><td>16,500원</td><td>MVNO</td></tr></tbody></table>"), ("TV 없이 인터넷만 쓸 때 유의사항", "<ul><li><strong>결합할인 포기</strong>: IPTV를 추가하면 3중 결합 할인(11,000원)을 받을 수 있지만, 인터넷만 가입하면 2중 결합(5,500원)이 최대입니다.</li><li><strong>기본형 IPTV 추가 검토</strong>: IPTV 기본형(5,500원)을 추가하면 3중 결합 할인(11,000원)이 적용되어 실질 TV 무료입니다. TV를 보지 않아도 추가하는 것이 유리할 수 있습니다.</li></ul>"), ("TV 대체 방법", "<ol><li><strong>OTT 서비스</strong>: 넷플릭스(5,500~17,000원), 티빙(5,500~13,900원), 웨이브(7,900~13,900원)</li><li><strong>유튜브</strong>: 무료 콘텐츠로 대부분 해결. 프리미엄(14,900원) 가입 시 광고 없이 시청.</li><li><strong>실시간 TV 앱</strong>: 웨이브, 티빙에서 일부 실시간 채널 제공</li></ol>"), ("인터넷만 가입 추천 대상", "<ul><li>1인 가구로 TV를 거의 보지 않는 분</li><li>이미 넷플릭스 등 OTT를 구독 중인 분</li><li>스마트폰이나 태블릿으로 영상을 보는 분</li><li>알뜰폰 사용자로 결합할인이 불가능한 분</li></ul>")], "faq": [("인터넷만 가입하면 TV를 아예 볼 수 없나요?", "IPTV는 볼 수 없지만, <strong>스마트TV로 OTT(넷플릭스, 유튜브 등)</strong>는 인터넷만 있으면 시청 가능합니다."), ("인터넷만 가입해도 공유기는 제공되나요?", "<strong>네</strong>, 대부분의 통신사에서 인터넷 가입 시 공유기를 기본 제공(임대)합니다."), ("나중에 IPTV를 추가할 수 있나요?", "<strong>네</strong>, 인터넷 사용 중 언제든 IPTV를 추가 가입할 수 있습니다. 추가 시 결합할인이 적용됩니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 20. IPTV 셋톱박스 없이
    {"title": "IPTV 셋톱박스 없이 인터넷만 쓰는 방법 총정리", "cat": CAT_INTERNET, "slug": "iptv-without-settopbox", "intro": "IPTV 셋톱박스 없이도 TV 콘텐츠를 즐기는 방법이 있습니다. <strong>스마트TV, 스마트폰, 태블릿</strong>으로 OTT와 실시간 방송을 보는 방법을 총정리합니다.", "sections": [("셋톱박스 없이 TV 보는 방법 5가지", "<ol><li><strong>스마트TV 내장 앱</strong>: 넷플릭스, 유튜브, 티빙, 웨이브 앱이 기본 설치되어 있어 인터넷만 연결하면 바로 시청 가능합니다.</li><li><strong>크롬캐스트</strong>: 구글 크롬캐스트(5만원대)를 TV HDMI에 연결하면 스마트폰 화면을 TV로 미러링할 수 있습니다.</li><li><strong>아마존 파이어TV 스틱</strong>: TV를 스마트TV로 변환하는 기기(5만원대). 넷플릭스, 유튜브 등 앱 설치 가능.</li><li><strong>애플TV</strong>: 애플 기기 사용자에게 최적. 에어플레이로 미러링 + 앱 스토어 이용.</li><li><strong>노트북 HDMI 연결</strong>: 노트북을 TV에 HDMI로 연결하면 모든 콘텐츠를 TV로 볼 수 있습니다.</li></ol>"), ("셋톱박스 없이 실시간 TV 보는 방법", "<ul><li><strong>웨이브</strong>: KBS, MBC, SBS 실시간 방송 제공 (월 7,900원~)</li><li><strong>티빙</strong>: tvN, JTBC 등 CJ ENM 채널 실시간 (월 5,500원~)</li><li><strong>카카오TV</strong>: 일부 채널 무료 실시간 방송</li><li><strong>지상파 앱</strong>: KBS, MBC, SBS 각 앱에서 실시간 무료(일부 제한) 제공</li></ul>"), ("셋톱박스 있을 때 vs 없을 때 비교", "<table><thead><tr><th>항목</th><th>셋톱박스 있음 (IPTV)</th><th>셋톱박스 없음 (OTT)</th></tr></thead><tbody><tr><td>채널 수</td><td>85~220개</td><td>OTT 콘텐츠 위주</td></tr><tr><td>실시간 방송</td><td>전 채널 가능</td><td>일부만 가능</td></tr><tr><td>리모컨</td><td>전용 리모컨</td><td>TV 리모컨/앱</td></tr><tr><td>월 비용</td><td>5,500~14,300원</td><td>OTT 구독료</td></tr><tr><td>결합할인</td><td>가능</td><td>불가</td></tr></tbody></table>"), ("셋톱박스 반납 방법", "<ol><li>통신사 고객센터에 IPTV 해지 신청</li><li>셋톱박스 반납 방법 선택 (택배 수거 또는 대리점 방문)</li><li>반납 확인 후 해지 완료</li><li>미반납 시 기기 비용 청구 (5~15만원) 주의</li></ol>")], "faq": [("스마트TV가 아닌 일반 TV에서도 OTT를 볼 수 있나요?", "<strong>크롬캐스트나 파이어TV 스틱</strong>을 HDMI에 꽂으면 일반 TV도 스마트TV처럼 사용 가능합니다."), ("셋톱박스를 반납하면 인터넷은 그대로 쓸 수 있나요?", "<strong>네</strong>, IPTV만 해지하고 인터넷은 계속 사용 가능합니다. 다만 결합할인 구조가 변경됩니다."), ("OTT만으로 가족 모두 만족할 수 있나요?", "젊은 세대는 OTT로 충분하지만, 부모님 세대는 <strong>리모컨으로 채널 돌리기</strong>를 선호하므로 IPTV가 편할 수 있습니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 21. 인터넷 통신사 변경 방법
    {"title": "인터넷 통신사 변경 방법 위약금 면제 조건 총정리", "cat": CAT_INTERNET, "slug": "internet-provider-switch", "intro": "현재 인터넷 통신사에 불만이 있거나 더 저렴한 곳으로 바꾸고 싶다면 <strong>통신사 변경</strong>을 고려해야 합니다. 위약금, 변경 절차, 면제 조건을 총정리합니다.", "sections": [("인터넷 통신사 변경 절차", "<ol><li><strong>현재 약정 상태 확인</strong>: 통신사 앱 또는 고객센터에서 약정 잔여 기간과 위약금을 확인합니다.</li><li><strong>새 통신사 가입 신청</strong>: 비교 사이트 또는 대리점에서 새 통신사 인터넷을 신청합니다.</li><li><strong>기존 통신사 해지</strong>: 새 인터넷 설치 후 기존 통신사를 해지합니다. 순서가 중요합니다.</li><li><strong>설치 및 개통</strong>: 기사 방문 설치 (보통 3~7일 소요)</li></ol>"), ("위약금 계산 방법", "<p>인터넷 위약금은 <strong>잔여 약정 기간에 비례</strong>합니다.</p><table><thead><tr><th>잔여 기간</th><th>위약금 예상 (3년 약정)</th></tr></thead><tbody><tr><td>2년 이상</td><td>15~20만원</td></tr><tr><td>1~2년</td><td>8~15만원</td></tr><tr><td>6개월~1년</td><td>4~8만원</td></tr><tr><td>6개월 이하</td><td>1~4만원</td></tr><tr><td>만료</td><td>0원</td></tr></tbody></table>"), ("위약금 면제 조건", "<ul><li><strong>약정 만료</strong>: 3년 약정이 끝나면 위약금 없이 해지 가능</li><li><strong>이전 불가 지역</strong>: 이사지에서 해당 통신사 서비스를 제공하지 않으면 위약금 면제</li><li><strong>서비스 장애</strong>: 통신사 귀책 사유로 장기간 서비스 장애 시 면제 가능</li><li><strong>군입대</strong>: 군 복무로 인한 해지 시 위약금 감면 또는 면제</li><li><strong>해외 이주</strong>: 해외 장기 체류 시 증빙 서류 제출로 면제 가능</li></ul>"), ("변경 시 사은품 받는 법", "<ul><li>새 통신사 가입 시 대리점보다 <strong>비교 사이트 경유</strong>가 현금 사은품이 더 큽니다 (5~20만원).</li><li>약정 만료 시점에 기존 통신사에서 <strong>잔류 혜택(사은품)</strong>을 제안하는 경우도 있으니 비교 후 결정하세요.</li><li>이사 시즌(3월, 9월)에 프로모션이 가장 활발합니다.</li></ul>")], "faq": [("해지 먼저 하고 새 통신사를 가입해야 하나요?", "<strong>새 통신사 가입을 먼저</strong> 하세요. 설치까지 3~7일 걸리므로, 기존 인터넷을 쓰면서 새 인터넷이 개통된 후 해지하면 공백이 없습니다."), ("같은 아파트에서 통신사만 바꿀 수 있나요?", "<strong>네</strong>, 같은 주소에서 통신사를 변경할 수 있습니다. 새 통신사 기사가 방문하여 회선을 교체합니다."), ("위약금을 새 통신사에서 대납해주나요?", "일부 대리점이나 비교 사이트에서 <strong>사은품으로 위약금을 보전</strong>해주는 경우가 있습니다. 가입 전 문의하세요.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 22. 약정 만료 후 재가입 vs 연장
    {"title": "인터넷 약정 만료 후 재가입 vs 연장 어떤 것이 유리할까", "cat": CAT_INTERNET, "slug": "internet-contract-renewal", "intro": "인터넷 3년 약정이 만료되면 <strong>같은 통신사 연장</strong>과 <strong>다른 통신사 재가입</strong> 중 선택해야 합니다. 어떤 것이 더 유리한지 비교합니다.", "sections": [("연장 vs 재가입 비교표", "<table><thead><tr><th>항목</th><th>같은 통신사 연장</th><th>다른 통신사 재가입</th></tr></thead><tbody><tr><td>요금</td><td>기존과 동일 또는 소폭 할인</td><td>신규 프로모션 적용 (더 저렴할 수 있음)</td></tr><tr><td>사은품</td><td>적거나 없음</td><td>5~20만원 현금 사은품</td></tr><tr><td>설치</td><td>변경 없음</td><td>기사 방문 재설치 필요</td></tr><tr><td>결합할인</td><td>유지</td><td>재설정 필요</td></tr><tr><td>번거로움</td><td>적음</td><td>있음 (해지+신규 가입)</td></tr></tbody></table>"), ("재가입이 유리한 경우", "<ul><li>타 통신사의 프로모션 요금이 현재보다 월 5,000원 이상 저렴할 때</li><li>사은품(현금 10만원 이상)을 받을 수 있을 때</li><li>현재 통신사의 속도나 품질에 불만이 있을 때</li><li>결합할인 구조를 변경하고 싶을 때</li></ul>"), ("연장이 유리한 경우", "<ul><li>현재 요금과 품질에 만족하는 경우</li><li>결합할인이 복잡하게 얽혀 있어 변경이 번거로운 경우</li><li>기존 통신사에서 연장 시 특별 할인을 제안하는 경우</li><li>설치 기사 방문이 번거로운 경우</li></ul>"), ("약정 만료 후 최적 전략", "<ol><li><strong>만료 3개월 전</strong>: 다른 통신사 요금 비교 시작</li><li><strong>현 통신사에 이탈 의사 표현</strong>: 잔류 혜택(사은품, 할인)을 제안받을 수 있습니다.</li><li><strong>비교 사이트에서 견적 받기</strong>: 2~3개 통신사 견적을 비교</li><li><strong>최종 결정</strong>: 총 비용(요금+사은품) 기준으로 가장 유리한 곳 선택</li></ol>")], "faq": [("약정 만료 후 아무것도 안 하면 어떻게 되나요?", "약정 만료 후에는 <strong>무약정 상태</strong>로 자동 전환됩니다. 월 요금이 약정 할인 없이 정상가로 올라가므로, 재약정 또는 타사 가입을 권합니다."), ("연장 시 약정 기간은 다시 3년인가요?", "<strong>네</strong>, 연장하면 새로 3년 약정이 시작됩니다. 1년 약정을 선택할 수도 있지만 요금이 더 비쌉니다."), ("약정 만료일을 어떻게 확인하나요?", "통신사 앱 → 나의 상품 → <strong>인터넷 약정 정보</strong>에서 확인 가능합니다. 고객센터(114)에 전화해도 확인됩니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 23. 인터넷 가입 사은품
    {"title": "인터넷 가입 사은품 현금 비교 통신사별 혜택 총정리", "cat": CAT_INTERNET, "slug": "internet-signup-cashback", "intro": "인터넷 가입 시 받을 수 있는 <strong>사은품(현금, 상품권, 가전)</strong>은 가입 경로에 따라 크게 달라집니다. 같은 요금제라도 어디서 가입하느냐에 따라 수십만 원 차이가 납니다. 통신사별 사은품 비교와 최대 혜택 받는 방법을 안내합니다.", "sections": [("가입 경로별 사은품 비교", "<table><thead><tr><th>가입 경로</th><th>사은품 수준</th><th>특징</th></tr></thead><tbody><tr><td>통신사 공식 홈페이지</td><td>0~5만원</td><td>가장 적음</td></tr><tr><td>통신사 고객센터</td><td>3~10만원</td><td>전화 상담 필요</td></tr><tr><td>오프라인 대리점</td><td>5~15만원</td><td>협상 가능</td></tr><tr><td>인터넷 비교 사이트</td><td>10~20만원</td><td>가장 많음</td></tr></tbody></table>"), ("사은품 받을 때 주의사항", "<ul><li><strong>현금 지급 시점</strong>: 가입 즉시 vs 3개월 후 vs 6개월 후 등 지급 시점이 다릅니다. 즉시 지급이 가장 확실합니다.</li><li><strong>조건 확인</strong>: 3년 약정, 특정 요금제 이상 등 조건을 충족해야 사은품을 받을 수 있습니다.</li><li><strong>현금 vs 상품권</strong>: 현금이 가장 실속 있습니다. 상품권은 사용처가 제한될 수 있습니다.</li><li><strong>사은품 미지급 시</strong>: 계약서에 사은품 내용을 명시하고 사진을 찍어두세요. 미지급 시 방송통신위원회에 신고할 수 있습니다.</li></ul>"), ("사은품 극대화 전략", "<ol><li><strong>비교 사이트 2~3곳 견적 받기</strong>: 사이트마다 사은품 금액이 다르므로 비교하세요.</li><li><strong>약정 만료 시즌 활용</strong>: 약정 만료 고객은 통신사가 유치 경쟁을 하므로 사은품이 커집니다.</li><li><strong>이사 시즌(3월, 9월) 활용</strong>: 프로모션이 가장 활발한 시기입니다.</li><li><strong>결합 가입 시 추가 사은품</strong>: 인터넷+TV+모바일 동시 가입 시 사은품이 더 큽니다.</li></ol>"), ("불법 사은품 주의", "<p>과도한 사은품은 <strong>불법</strong>일 수 있습니다.</p><ul><li>방송통신위원회 기준 사은품 상한선이 있습니다.</li><li>과도한 사은품을 약속하고 나중에 지급하지 않는 '먹튀' 대리점에 주의하세요.</li><li>계약서에 사은품 내용을 반드시 명시하고 보관하세요.</li></ul>")], "faq": [("사은품은 세금을 내야 하나요?", "개인이 받는 인터넷 가입 사은품은 <strong>세금 대상이 아닙니다</strong>."), ("사은품을 받고 바로 해지하면 되나요?", "약정 기간 내 해지하면 <strong>위약금이 발생</strong>하며, 사은품보다 위약금이 더 큽니다. 최소 약정 기간은 유지해야 합니다."), ("가전(TV, 노트북) 사은품은 믿을 수 있나요?", "일부 대리점에서 가전 사은품을 제공하지만, 사양이 낮거나 중고일 수 있습니다. <strong>현금 사은품이 가장 확실</strong>합니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 24. 인터넷 설치 신청 방법
    {"title": "인터넷 설치 신청 방법 개통까지 걸리는 시간 총정리", "cat": CAT_INTERNET, "slug": "internet-installation-guide", "intro": "인터넷을 신규 가입하거나 이사 후 설치하려면 <strong>신청부터 개통까지의 과정</strong>을 알아야 합니다. 신청 방법, 소요 시간, 설치 당일 준비사항을 총정리합니다.", "sections": [("인터넷 설치 신청 방법 3가지", "<ol><li><strong>온라인 신청</strong>: 통신사 홈페이지 또는 비교 사이트에서 24시간 신청 가능. 상담원이 전화로 일정을 조율합니다.</li><li><strong>전화 신청</strong>: 통신사 고객센터(114)로 전화하여 신청. 상담원이 요금제 추천과 일정을 안내합니다.</li><li><strong>대리점 방문</strong>: 오프라인 대리점에 방문하여 상담 후 신청. 대면 상담과 사은품 협상이 가능합니다.</li></ol>"), ("개통까지 걸리는 시간", "<table><thead><tr><th>상황</th><th>소요 시간</th><th>비고</th></tr></thead><tbody><tr><td>아파트 (FTTH 설비 있음)</td><td>3~5일</td><td>기사 방문 설치</td></tr><tr><td>빌라·오피스텔</td><td>5~7일</td><td>회선 공사 필요할 수 있음</td></tr><tr><td>신축 아파트</td><td>7~14일</td><td>인입 공사 필요</td></tr><tr><td>농어촌</td><td>7~14일</td><td>회선 구축 필요</td></tr></tbody></table>"), ("설치 당일 준비사항", "<ul><li><strong>본인 또는 대리인 재택</strong>: 기사 방문 시 누군가 집에 있어야 합니다.</li><li><strong>공유기 설치 위치 결정</strong>: 집 중앙에 설치하면 와이파이 신호가 고르게 퍼집니다.</li><li><strong>신분증 준비</strong>: 본인 확인을 위해 필요할 수 있습니다.</li><li><strong>속도 테스트</strong>: 설치 직후 fast.com에서 속도를 측정하여 정상인지 확인하세요.</li></ul>"), ("설치 후 확인사항", "<ol><li>유선(랜선) 속도가 가입 속도의 80% 이상인지 확인</li><li>와이파이 속도가 각 방에서 정상인지 확인</li><li>공유기 관리자 비밀번호 변경 (보안 목적)</li><li>IPTV가 있다면 셋톱박스 채널이 정상 수신되는지 확인</li></ol>")], "faq": [("설치 기사가 오기 전에 해야 할 것이 있나요?", "특별히 없습니다. 다만 <strong>공유기 설치 희망 위치</strong>를 미리 정해두면 설치가 빠릅니다."), ("설치비는 별도로 내야 하나요?", "약정 가입 시 <strong>설치비 무료</strong>인 경우가 대부분입니다. 무약정이나 특수 공사가 필요한 경우 3~5만 원이 발생할 수 있습니다."), ("주말에도 설치가 가능한가요?", "통신사에 따라 <strong>토요일 설치가 가능</strong>한 경우가 있습니다. 일요일은 대부분 불가합니다. 신청 시 희망 일정을 알려주세요.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 25. 인터넷 해지 방법
    {"title": "인터넷 해지 방법 위약금 계산 절차 주의사항", "cat": CAT_INTERNET, "slug": "internet-cancellation-guide", "intro": "인터넷을 해지하려면 <strong>위약금, 해지 절차, 장비 반납</strong> 등을 알아야 합니다. 불필요한 비용을 피하고 깔끔하게 해지하는 방법을 총정리합니다.", "sections": [("인터넷 해지 절차", "<ol><li><strong>약정 잔여 기간·위약금 확인</strong>: 통신사 앱 또는 고객센터에서 확인</li><li><strong>해지 신청</strong>: 고객센터 전화(114) 또는 홈페이지에서 신청</li><li><strong>잔류 혜택 제안 거절</strong>: 해지 의사를 밝히면 잔류 혜택을 제안합니다. 확고하면 거절하세요.</li><li><strong>장비 반납</strong>: 공유기, 셋톱박스 등 임대 장비를 택배 또는 대리점에 반납</li><li><strong>최종 요금 정산</strong>: 해지 월 요금 일할 계산 + 위약금이 마지막 청구됩니다.</li></ol>"), ("위약금 계산 방법", "<p>위약금 = <strong>(약정 할인 금액 × 잔여 개월 수) × 40~50%</strong></p><ul><li>3년 약정에서 1년 사용 후 해지: 잔여 24개월 → 약 10~15만원</li><li>3년 약정에서 2년 사용 후 해지: 잔여 12개월 → 약 5~8만원</li><li>약정 만료 후: 위약금 0원</li></ul>"), ("장비 반납 주의사항", "<ul><li><strong>공유기</strong>: 통신사 임대 공유기는 반납 필수. 미반납 시 5~10만원 청구.</li><li><strong>셋톱박스</strong>: IPTV 가입 시 제공된 셋톱박스 반납 필수. 미반납 시 10~15만원 청구.</li><li><strong>반납 방법</strong>: 택배 수거 요청(무료) 또는 가까운 대리점 방문 반납</li><li><strong>반납 확인</strong>: 반납 후 통신사에 확인 전화하여 처리 완료 여부를 꼭 확인하세요.</li></ul>"), ("해지 전 체크리스트", "<ol><li>약정 잔여 기간 및 위약금 확인</li><li>결합할인 구조 확인 (인터넷 해지 시 모바일·TV 할인 변동)</li><li>임대 장비(공유기, 셋톱박스) 목록 확인</li><li>자동이체 해제 확인</li><li>새 인터넷 가입 완료 후 해지 (공백 방지)</li></ol>")], "faq": [("전화하면 해지를 안 시켜주는데 어떻게 하나요?", "해지 의사를 <strong>명확하고 단호하게</strong> 밝히세요. 잔류 혜택 제안은 '필요 없다'고 거절하면 됩니다. 법적으로 해지를 거부할 수 없습니다."), ("해지 당일에 인터넷이 끊기나요?", "해지 신청 후 <strong>해당 월 말일</strong>까지 사용 가능한 경우가 많습니다. 즉시 해지를 원하면 요청하세요."), ("해지 후 같은 통신사에 재가입할 수 있나요?", "<strong>네</strong>, 가능합니다. 해지 후 일정 기간(보통 3~6개월)이 지나면 신규 고객 혜택(사은품)을 받고 재가입할 수 있습니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 26. 인터넷 속도 측정
    {"title": "인터넷 속도 측정 방법 느릴 때 해결법 총정리", "cat": CAT_INTERNET, "slug": "internet-speed-test-fix", "intro": "인터넷이 느리다고 느껴지면 먼저 <strong>실제 속도를 측정</strong>해야 합니다. 측정 방법과 느린 원인별 해결법을 총정리합니다.", "sections": [("인터넷 속도 측정 방법", "<ol><li><strong>fast.com</strong> (넷플릭스 제공): 접속만 하면 자동 측정. 가장 간편합니다.</li><li><strong>speedtest.net</strong> (Ookla): 다운로드·업로드·핑을 상세히 측정합니다.</li><li><strong>통신사 속도 측정</strong>: KT·SK·LG 각 앱에서 공식 속도 측정 기능을 제공합니다.</li></ol><p><strong>정확한 측정 팁</strong>: 공유기에 랜선을 직접 연결한 상태에서 측정해야 와이파이 변수를 제거한 순수 회선 속도를 확인할 수 있습니다.</p>"), ("속도가 느린 원인 5가지", "<ol><li><strong>공유기 문제</strong>: 구형 공유기는 100Mbps까지만 지원합니다. 와이파이 6 공유기로 교체하세요.</li><li><strong>와이파이 거리·장애물</strong>: 공유기와 기기 사이에 벽이 많으면 속도가 떨어집니다. 메시 공유기를 고려하세요.</li><li><strong>랜선 규격</strong>: Cat5 랜선은 100Mbps까지만 지원. Cat5e 이상으로 교체하세요.</li><li><strong>시간대</strong>: 저녁 8~11시는 동네 전체가 인터넷을 쓰므로 속도가 느려질 수 있습니다.</li><li><strong>통신사 회선 문제</strong>: 위 모든 것이 정상인데도 느리면 통신사에 회선 점검을 요청하세요.</li></ol>"), ("속도 개선 방법 단계별 가이드", "<ol><li><strong>1단계: 공유기 재부팅</strong> → 전원을 뽑고 30초 후 다시 연결</li><li><strong>2단계: 유선 속도 측정</strong> → 공유기에 랜선 직접 연결 후 측정</li><li><strong>3단계: 유선 속도 정상이면</strong> → 공유기 또는 와이파이 문제. 공유기 교체 고려.</li><li><strong>4단계: 유선 속도도 느리면</strong> → 통신사 고객센터(114)에 회선 점검 요청</li><li><strong>5단계: 회선 정상인데 느리면</strong> → 요금제 속도 업그레이드 검토</li></ol>"), ("공유기 교체로 속도 개선하기", "<p>통신사 기본 공유기 대신 <strong>고성능 공유기</strong>로 교체하면 체감 속도가 크게 개선됩니다.</p><ul><li><strong>예산 5만원대</strong>: ipTIME AX3000, TP-Link AX3000 (와이파이 6)</li><li><strong>예산 10만원대</strong>: ASUS RT-AX55, 넷기어 RAX50 (와이파이 6)</li><li><strong>넓은 집</strong>: 메시 공유기(ipTIME Mesh, TP-Link Deco) 세트 추천</li></ul>")], "faq": [("fast.com과 speedtest.net 결과가 다른 이유는?", "측정 서버 위치와 프로토콜이 다르기 때문입니다. <strong>여러 사이트에서 측정</strong>하여 평균을 확인하세요."), ("와이파이 속도가 유선의 절반인데 정상인가요?", "와이파이는 유선보다 느린 것이 <strong>정상</strong>입니다. 와이파이 5(802.11ac)는 유선의 30~50%, 와이파이 6(802.11ax)는 50~80% 수준입니다."), ("통신사에 속도 보상을 요청할 수 있나요?", "가입 속도의 70% 이하가 지속되면 <strong>통신사에 회선 점검 및 보상</strong>을 요청할 수 있습니다. 방송통신위원회 기준으로 보상 규정이 있습니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 27. 와이파이 공유기 추천
    {"title": "와이파이 공유기 추천 인터넷 속도 최대로 쓰는 방법", "cat": CAT_INTERNET, "slug": "wifi-router-recommendation", "intro": "비싼 인터넷 요금제에 가입해도 <strong>공유기 성능이 떨어지면</strong> 속도를 제대로 못 씁니다. 인터넷 속도를 최대로 활용하는 공유기 추천과 설치 팁을 안내합니다.", "sections": [("공유기 추천 TOP 5", "<table><thead><tr><th>제품</th><th>규격</th><th>최대 속도</th><th>가격대</th><th>추천 환경</th></tr></thead><tbody><tr><td>ipTIME AX3000</td><td>와이파이 6</td><td>3,000Mbps</td><td>5만원대</td><td>소형 원룸~투룸</td></tr><tr><td>TP-Link Archer AX55</td><td>와이파이 6</td><td>3,000Mbps</td><td>7만원대</td><td>3룸 가정</td></tr><tr><td>ASUS RT-AX55</td><td>와이파이 6</td><td>1,800Mbps</td><td>6만원대</td><td>가성비</td></tr><tr><td>ipTIME Mesh A8004</td><td>메시 와이파이 6</td><td>3,000Mbps</td><td>15만원대(2팩)</td><td>넓은 아파트</td></tr><tr><td>TP-Link Deco X50</td><td>메시 와이파이 6</td><td>3,000Mbps</td><td>18만원대(2팩)</td><td>3층 주택</td></tr></tbody></table>"), ("공유기 선택 기준", "<ul><li><strong>와이파이 6(802.11ax) 이상</strong>: 기가 인터넷을 제대로 쓰려면 필수</li><li><strong>안테나 수</strong>: 외장 안테나가 많을수록 신호 범위가 넓음</li><li><strong>MU-MIMO 지원</strong>: 여러 기기가 동시에 빠르게 연결</li><li><strong>메시 지원</strong>: 넓은 집(30평 이상)은 메시 공유기 추천</li></ul>"), ("공유기 설치 최적 위치", "<ul><li><strong>집 중앙</strong>에 높은 곳(선반 위)에 설치</li><li><strong>바닥이나 구석</strong>은 피하세요 (신호가 사방으로 퍼져야 합니다)</li><li><strong>전자레인지·블루투스 기기 근처</strong>는 피하세요 (주파수 간섭)</li><li><strong>금속 물체</strong> 뒤에 설치하지 마세요 (신호 차단)</li></ul>"), ("통신사 공유기 vs 자체 공유기", "<table><thead><tr><th>항목</th><th>통신사 공유기</th><th>자체 구매 공유기</th></tr></thead><tbody><tr><td>비용</td><td>무료 임대 (해지 시 반납)</td><td>5~18만원 구매</td></tr><tr><td>성능</td><td>보통 (구형인 경우 많음)</td><td>우수 (최신 규격 선택 가능)</td></tr><tr><td>AS</td><td>통신사 AS</td><td>제조사 AS</td></tr><tr><td>설정</td><td>기사가 설정해줌</td><td>본인이 설정</td></tr></tbody></table>")], "faq": [("통신사 공유기를 쓰면서 자체 공유기를 추가할 수 있나요?", "<strong>네</strong>, 통신사 공유기를 브릿지 모드로 전환하고 자체 공유기를 연결하면 됩니다. 또는 통신사 공유기를 반납하고 자체 공유기만 사용할 수도 있습니다."), ("메시 공유기가 꼭 필요한가요?", "30평 이하 아파트는 <strong>일반 공유기로 충분</strong>합니다. 30평 이상이거나 벽이 많은 구조, 2층 이상 주택은 메시 공유기를 추천합니다."), ("공유기를 바꾸면 인터넷 속도가 확실히 빨라지나요?", "구형 공유기(802.11n 이하)에서 와이파이 6 공유기로 교체하면 <strong>와이파이 속도가 2~3배</strong> 빨라질 수 있습니다. 유선 속도에는 영향 없습니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 28. 아파트 인터넷 추천
    {"title": "아파트 인터넷 추천 단지 내 속도 빠른 통신사 확인법", "cat": CAT_INTERNET, "slug": "apartment-internet-recommendation", "intro": "같은 아파트 단지라도 통신사에 따라 <strong>인터넷 속도와 안정성</strong>이 다를 수 있습니다. 아파트에서 가장 빠른 통신사를 확인하는 방법과 추천 전략을 안내합니다.", "sections": [("아파트 인터넷 속도가 달라지는 이유", "<ul><li><strong>FTTH(광케이블) 직접 인입</strong>: 해당 통신사가 아파트까지 직접 광케이블을 깔았으면 속도가 가장 빠르고 안정적입니다.</li><li><strong>VDSL/LAN 방식</strong>: 아파트 통신실까지 광케이블이고, 각 세대까지는 전화선/랜선으로 연결되면 속도가 제한됩니다.</li><li><strong>같은 동 사용자 수</strong>: 한 동에서 같은 통신사 사용자가 많으면 피크 시간대에 속도가 떨어질 수 있습니다.</li></ul>"), ("아파트 최적 통신사 확인 방법", "<ol><li><strong>관리사무소 문의</strong>: 아파트 통신실에 어떤 통신사 설비가 있는지 확인</li><li><strong>이웃 주민에게 물어보기</strong>: 같은 동 주민의 인터넷 속도 체험담이 가장 정확합니다.</li><li><strong>통신사 홈페이지 조회</strong>: 주소를 입력하면 제공 가능한 속도를 확인할 수 있습니다.</li><li><strong>커뮤니티 검색</strong>: 아파트 커뮤니티(네이버 카페 등)에서 인터넷 후기를 검색하세요.</li></ol>"), ("신축 아파트 vs 구축 아파트", "<table><thead><tr><th>항목</th><th>신축 아파트</th><th>구축 아파트 (15년 이상)</th></tr></thead><tbody><tr><td>설비</td><td>FTTH (광케이블 직접 인입)</td><td>VDSL 또는 LAN 방식 가능</td></tr><tr><td>최대 속도</td><td>1~10Gbps</td><td>100Mbps~1Gbps</td></tr><tr><td>통신사 선택</td><td>대부분 3사 가능</td><td>일부 통신사만 가능할 수 있음</td></tr></tbody></table>"), ("아파트 인터넷 속도 개선 팁", "<ol><li><strong>FTTH 지원 통신사 선택</strong>: 관리사무소에서 확인 후 직접 인입한 통신사를 선택하세요.</li><li><strong>고성능 공유기 사용</strong>: 통신사 기본 공유기 대신 와이파이 6 공유기로 교체</li><li><strong>유선 연결 활용</strong>: PC, TV 등 고정 기기는 와이파이 대신 랜선으로 연결하면 속도가 안정적입니다.</li><li><strong>피크 시간대 회피</strong>: 저녁 8~11시에 속도가 느리면 새벽이나 오전에 대용량 다운로드하세요.</li></ol>")], "faq": [("아파트에서 10기가 인터넷을 쓸 수 있나요?", "신축 아파트 중 10Gbps FTTH 설비가 있는 곳에서만 가능합니다. KT와 LG U+가 10G 서비스를 제공하며, <strong>통신사 홈페이지에서 주소로 확인</strong>할 수 있습니다."), ("구축 아파트에서 속도가 100Mbps밖에 안 나오는데 어떻게 하나요?", "건물 내부 배선이 VDSL 방식이면 <strong>100Mbps가 최대</strong>입니다. 통신사에 FTTH 전환 공사를 요청하거나, 관리사무소를 통해 아파트 전체 통신설비 업그레이드를 건의할 수 있습니다."), ("같은 아파트 같은 통신사인데 옆집보다 느린 이유는?", "공유기 성능, 와이파이 채널 간섭, 랜선 규격 등의 차이 때문입니다. <strong>유선 속도 측정</strong>을 해서 회선 자체가 느린 건지, 공유기/와이파이 문제인지 구분하세요.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 29. 인터넷 요금 줄이는 방법
    {"title": "인터넷 요금 줄이는 방법 7가지 숨은 할인 찾기", "cat": CAT_INTERNET, "slug": "internet-save-money-tips", "intro": "매달 나가는 인터넷 요금을 <strong>바로 줄일 수 있는 7가지 방법</strong>을 알려드립니다. 통신사 변경 없이도 월 수천~수만 원을 절약할 수 있습니다.", "sections": [("인터넷 요금 줄이는 7가지 방법", "<ol><li><strong>불필요한 부가서비스 해지</strong>: 통신사 앱에서 가입된 부가서비스(보안, 클라우드, 게임팩 등)를 확인하고 불필요한 것을 해지하세요. 월 2,000~5,000원 절약.</li><li><strong>속도 다운그레이드</strong>: 1Gbps를 쓰지만 실제 500Mbps면 충분하다면 요금제를 낮추세요. 월 5,000~7,000원 절약.</li><li><strong>결합할인 점검</strong>: 인터넷+모바일+TV 결합 여부를 확인하고, 결합이 안 되어 있으면 등록하세요.</li><li><strong>TV 요금제 다운</strong>: IPTV 프리미엄을 기본형으로 변경하면 월 5,000~9,000원 절약.</li><li><strong>약정 만료 시 재협상</strong>: 약정 만료 후 통신사에 요금 인하를 요청하거나 타사 이동을 검토하세요.</li><li><strong>유료 채널 정리</strong>: IPTV 유료 채널(영화, 스포츠 등)을 확인하고 보지 않는 것을 해지하세요.</li><li><strong>알뜰 인터넷 전환</strong>: 약정 만료 후 알뜰 인터넷으로 전환하면 월 5,000~10,000원 절약.</li></ol>"), ("숨은 부가서비스 찾아 해지하기", "<p>많은 분들이 가입 사실도 모르는 부가서비스가 있습니다.</p><ul><li><strong>통신사 앱</strong> → 나의 상품 → 부가서비스 목록 확인</li><li><strong>흔한 부가서비스</strong>: 인터넷 보안(V3), 클라우드 백업, 게임팩, 뮤직팩, 교육 서비스</li><li>사용하지 않는 서비스를 모두 해지하면 월 <strong>2,000~10,000원</strong> 절약 가능</li></ul>"), ("요금 줄이기 실전 예시", "<table><thead><tr><th>절약 항목</th><th>변경 전</th><th>변경 후</th><th>월 절약</th></tr></thead><tbody><tr><td>인터넷 속도 변경</td><td>1Gbps 33,000원</td><td>500Mbps 27,500원</td><td>-5,500원</td></tr><tr><td>TV 요금제 변경</td><td>프리미엄 14,300원</td><td>기본형 5,500원</td><td>-8,800원</td></tr><tr><td>부가서비스 해지</td><td>3건 6,600원</td><td>0원</td><td>-6,600원</td></tr><tr><td><strong>합계</strong></td><td></td><td></td><td><strong>-20,900원/월</strong></td></tr></tbody></table><p>연간 <strong>약 25만 원</strong> 절약 가능합니다.</p>"), ("통신사에 요금 인하 요청하는 법", "<ol><li>고객센터(114)에 전화</li><li>'요금이 비싸서 타사 이동을 검토 중'이라고 말하기</li><li>잔류 혜택(할인, 사은품)을 제안받으면 비교 후 결정</li><li>만족스럽지 않으면 실제로 타사로 이동</li></ol>")], "faq": [("부가서비스를 해지하면 인터넷에 문제가 생기나요?", "<strong>아닙니다.</strong> 부가서비스는 인터넷 회선과 별개이므로 해지해도 인터넷 속도나 품질에 영향이 없습니다."), ("속도를 낮추면 체감이 크게 달라지나요?", "1Gbps에서 500Mbps로 낮춰도 <strong>일반 사용에서 체감 차이는 거의 없습니다</strong>. 대용량 다운로드 시에만 차이가 느껴집니다."), ("통신사에 전화하면 정말 할인해주나요?", "약정 만료 고객이 이탈 의사를 밝히면 <strong>잔류 혜택을 제안하는 경우가 많습니다</strong>. 월 3,000~5,000원 추가 할인이나 상품권을 받을 수 있습니다.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},

    # 30. 인터넷 요금 미납 시
    {"title": "인터넷 요금 미납 시 불이익 복구 방법 총정리", "cat": CAT_INTERNET, "slug": "internet-unpaid-penalty", "intro": "인터넷 요금을 미납하면 <strong>서비스 중단, 신용점수 하락</strong> 등 불이익이 발생할 수 있습니다. 미납 시 일어나는 일과 복구 방법을 총정리합니다.", "sections": [("인터넷 요금 미납 시 단계별 불이익", "<table><thead><tr><th>미납 기간</th><th>불이익</th></tr></thead><tbody><tr><td>1개월</td><td>연체 안내 문자·전화</td></tr><tr><td>2개월</td><td>서비스 일시 정지 (인터넷 끊김)</td></tr><tr><td>3개월</td><td>서비스 해지 통보</td></tr><tr><td>3개월 이상</td><td>강제 해지 + 미납 요금 + 위약금 + 신용점수 하락</td></tr><tr><td>6개월 이상</td><td>채권추심 (추심 회사에서 연락)</td></tr></tbody></table>"), ("미납 시 신용점수 영향", "<ul><li><strong>통신 요금 연체</strong>는 신용평가 기관에 보고됩니다.</li><li>연체 기간이 길수록 신용점수 하락 폭이 큽니다.</li><li>연체 이력은 완납 후에도 <strong>최대 5년간 기록</strong>이 남습니다.</li><li>신용점수가 하락하면 대출 금리 상승, 카드 발급 거절 등의 불이익이 있습니다.</li></ul>"), ("미납 요금 납부 및 복구 방법", "<ol><li><strong>미납 요금 확인</strong>: 통신사 앱 또는 고객센터에서 미납 금액을 확인합니다.</li><li><strong>즉시 납부</strong>: 앱 내 결제, 계좌이체, 편의점 납부 등으로 즉시 납부합니다.</li><li><strong>분할 납부 요청</strong>: 금액이 큰 경우 고객센터에 분할 납부를 요청할 수 있습니다.</li><li><strong>서비스 복구 요청</strong>: 납부 후 고객센터에 서비스 재개를 요청합니다. 보통 납부 후 <strong>수 시간~1일 내</strong> 복구됩니다.</li></ol>"), ("미납 예방 방법", "<ul><li><strong>자동이체 설정</strong>: 은행 자동이체 또는 카드 자동결제를 설정하면 미납을 예방할 수 있습니다.</li><li><strong>결제일 변경</strong>: 월급일 직후로 결제일을 변경하세요.</li><li><strong>통신사 앱 알림</strong>: 청구서 발행 알림을 설정하면 잊지 않고 납부할 수 있습니다.</li></ul>")], "faq": [("미납 후 바로 납부하면 신용점수에 영향이 없나요?", "1개월 이내 납부하면 <strong>신용점수에 영향이 없는 경우가 대부분</strong>입니다. 2개월 이상 연체부터 신용기관에 보고됩니다."), ("미납으로 해지되면 다시 가입할 수 있나요?", "미납 요금을 전액 납부하면 <strong>재가입 가능</strong>합니다. 다만 같은 통신사에서 신뢰도가 낮아져 약정 조건이 불리해질 수 있습니다."), ("분할 납부는 누구나 가능한가요?", "통신사 재량이지만, 미납 금액이 크고 납부 의사가 확실하면 <strong>대부분 분할 납부를 허용</strong>합니다. 고객센터에 사정을 설명하고 요청하세요.")], "ctas": [CTA_INTERNET_COMPARE, CTA_SPEED_TEST, CTA_INTERNET_SIGNUP]},
]


def publish(post_data):
    data = json.dumps(post_data).encode("utf-8")
    req = urllib.request.Request(API, data=data, headers={
        "Authorization": f"Basic {AUTH}",
        "Content-Type": "application/json",
    }, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("id"), result.get("link", "")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"  HTTP Error {e.code}: {body[:200]}")
        return None, None
    except Exception as e:
        print(f"  Error: {e}")
        return None, None


def main():
    upload_all_images()
    total = len(POSTS)
    print("=" * 60)
    print(f"총 {total}개 포스트 발행 시작")
    print("=" * 60)
    for idx, post in enumerate(POSTS, 1):
        content = build_content(post)
        slug = post["slug"]
        payload = {
            "title": post["title"],
            "content": content,
            "status": "publish",
            "slug": slug,
            "categories": [post["cat"]],
        }
        featured_id = get_featured_image_id(slug)
        if featured_id:
            payload["featured_media"] = featured_id
        post_id, link = publish(payload)
        if post_id:
            print(f"[{idx}/{total}] OK | ID:{post_id} | {post['title']}")
            if link:
                print(f"  -> {link}")
        else:
            print(f"[{idx}/{total}] FAIL | {post['title']}")
        time.sleep(1)
    print("\n완료!")


if __name__ == "__main__":
    main()

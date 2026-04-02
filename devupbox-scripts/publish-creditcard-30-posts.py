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

# Categories: IT정보=5, 금융=8, 대출=6, 수입차=10, 국산차=9, 엑셀=12, 인터넷=3, 지식=13
CAT_FINANCE = 8

UPLOADED_IMAGES = {}

IMAGES = {
    "cashback-credit-card-recommendation": [
        ("photo-1556742049-0cfed4f6a45d", "캐시백 신용카드 비교"),
        ("photo-1579621970563-9ae2e01f6860", "신용카드 결제 모습"),
    ],
    "mileage-credit-card-recommendation": [
        ("photo-1436491865332-7a61a109db05", "마일리지 항공 여행"),
        ("photo-1556742049-0cfed4f6a45d", "마일리지 신용카드"),
    ],
    "gas-discount-credit-card": [
        ("photo-1545262810-a9a689880a3f", "주유소 주유 모습"),
        ("photo-1556742049-0cfed4f6a45d", "주유 할인 카드"),
    ],
    "telecom-discount-credit-card": [
        ("photo-1556742049-0cfed4f6a45d", "통신비 할인 카드"),
        ("photo-1512941937669-90a1b58e7e9c", "스마트폰 통신비 절약"),
    ],
    "delivery-app-discount-credit-card": [
        ("photo-1556742049-0cfed4f6a45d", "배달앱 할인 카드"),
        ("photo-1526367790999-0150786686a2", "배달 음식 주문"),
    ],
    "mart-discount-credit-card": [
        ("photo-1556742049-0cfed4f6a45d", "마트 할인 카드"),
        ("photo-1604719312566-8912e9227c6a", "대형마트 장보기"),
    ],
    "transportation-credit-card": [
        ("photo-1556742049-0cfed4f6a45d", "교통카드 신용카드"),
        ("photo-1544620347-c4fd4a3d5957", "대중교통 이용"),
    ],
    "online-shopping-credit-card": [
        ("photo-1556742049-0cfed4f6a45d", "온라인 쇼핑 카드"),
        ("photo-1563013544-824ae1b704d3", "온라인 쇼핑 결제"),
    ],
    "office-worker-credit-card": [
        ("photo-1556742049-0cfed4f6a45d", "직장인 신용카드"),
        ("photo-1454165804606-c3d57bc86b40", "직장인 업무 모습"),
    ],
    "first-credit-card-recommendation": [
        ("photo-1556742049-0cfed4f6a45d", "사회초년생 첫 카드"),
        ("photo-1521791136064-7986c2920216", "첫 카드 발급"),
    ],
    "business-credit-card-recommendation": [
        ("photo-1556742049-0cfed4f6a45d", "자영업자 사업용 카드"),
        ("photo-1450101499163-c8848c66ca85", "사업 경비 관리"),
    ],
    "student-credit-card-recommendation": [
        ("photo-1556742049-0cfed4f6a45d", "대학생 카드 추천"),
        ("photo-1523050854058-8df90110c9f1", "대학생 캠퍼스 생활"),
    ],
    "housewife-credit-card-recommendation": [
        ("photo-1556742049-0cfed4f6a45d", "주부 생활비 절약 카드"),
        ("photo-1604719312566-8912e9227c6a", "생활비 절약 장보기"),
    ],
    "freelancer-credit-card-recommendation": [
        ("photo-1556742049-0cfed4f6a45d", "프리랜서 신용카드"),
        ("photo-1488590528505-98d2b5aba04b", "프리랜서 업무 환경"),
    ],
    "samsung-card-recommendation": [
        ("photo-1556742049-0cfed4f6a45d", "삼성카드 추천"),
        ("photo-1579621970563-9ae2e01f6860", "삼성카드 혜택 비교"),
    ],
    "hyundai-card-recommendation": [
        ("photo-1556742049-0cfed4f6a45d", "현대카드 추천"),
        ("photo-1579621970563-9ae2e01f6860", "현대카드 혜택 비교"),
    ],
    "shinhan-card-recommendation": [
        ("photo-1556742049-0cfed4f6a45d", "신한카드 추천"),
        ("photo-1579621970563-9ae2e01f6860", "신한카드 혜택 비교"),
    ],
    "kb-card-recommendation": [
        ("photo-1556742049-0cfed4f6a45d", "KB국민카드 추천"),
        ("photo-1579621970563-9ae2e01f6860", "KB카드 혜택 비교"),
    ],
    "lotte-card-recommendation": [
        ("photo-1556742049-0cfed4f6a45d", "롯데카드 추천"),
        ("photo-1579621970563-9ae2e01f6860", "롯데카드 혜택 비교"),
    ],
    "woori-card-recommendation": [
        ("photo-1556742049-0cfed4f6a45d", "우리카드 추천"),
        ("photo-1579621970563-9ae2e01f6860", "우리카드 혜택 비교"),
    ],
    "no-annual-fee-credit-card": [
        ("photo-1556742049-0cfed4f6a45d", "연회비 무료 카드"),
        ("photo-1554224155-6726b3ff858f", "연회비 무료 혜택"),
    ],
    "premium-credit-card-comparison": [
        ("photo-1556742049-0cfed4f6a45d", "프리미엄 카드 비교"),
        ("photo-1559526324-4b87b5e36e44", "프리미엄 신용카드"),
    ],
    "check-card-recommendation": [
        ("photo-1556742049-0cfed4f6a45d", "체크카드 추천"),
        ("photo-1579621970563-9ae2e01f6860", "체크카드 혜택 비교"),
    ],
    "plcc-card-recommendation": [
        ("photo-1556742049-0cfed4f6a45d", "PLCC 카드 추천"),
        ("photo-1472851294608-062f824d29cc", "브랜드 제휴카드"),
    ],
    "postpaid-transportation-check-card": [
        ("photo-1556742049-0cfed4f6a45d", "후불교통 체크카드"),
        ("photo-1544620347-c4fd4a3d5957", "교통카드 체크카드"),
    ],
    "credit-card-approval-requirements": [
        ("photo-1556742049-0cfed4f6a45d", "신용카드 발급 조건"),
        ("photo-1450101499163-c8848c66ca85", "카드 심사 서류"),
    ],
    "credit-card-limit-increase": [
        ("photo-1556742049-0cfed4f6a45d", "카드 한도 올리기"),
        ("photo-1579621970563-9ae2e01f6860", "신용카드 한도 상향"),
    ],
    "credit-card-cancellation-guide": [
        ("photo-1556742049-0cfed4f6a45d", "신용카드 해지 방법"),
        ("photo-1554224155-6726b3ff858f", "카드 해지 신용점수"),
    ],
    "credit-card-point-cash-conversion": [
        ("photo-1556742049-0cfed4f6a45d", "카드 포인트 현금 전환"),
        ("photo-1579621970563-9ae2e01f6860", "포인트 활용법"),
    ],
    "credit-card-vs-check-card": [
        ("photo-1556742049-0cfed4f6a45d", "신용카드 vs 체크카드"),
        ("photo-1554224155-6726b3ff858f", "카드 비교 선택"),
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
    except urllib.error.HTTPError as e:
        print(f"  WP 업로드 실패: HTTP {e.code} - {e.read().decode()[:200]}")
        return None, None
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
            filename = f"{slug}-{idx+1}"
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
                print(f"  [{uploaded+failed}/{total}] OK | {filename} -> {wp_url}")
            else:
                UPLOADED_IMAGES[slug].append(("", "", alt_text))
                failed += 1
                print(f"  [{uploaded+failed}/{total}] FAIL | {filename}")
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


CTA_CARD_GORILLA = {"text": "카드고릴라에서 내게 맞는 카드 찾기", "desc": "조건별 신용카드 비교·추천 서비스", "url": "https://www.card-gorilla.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"}
CTA_NAVER_CARD = {"text": "네이버페이 카드 혜택 비교", "desc": "네이버페이에서 카드 혜택을 한눈에 비교하세요", "url": "https://new-m.pay.naver.com/cards", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"}
CTA_CREDIT_SCORE = {"text": "내 신용점수 무료 조회", "desc": "올크레딧에서 신용점수를 무료로 확인하세요", "url": "https://www.allcredit.co.kr/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"}


# ============================================================
# 포스트 데이터 (1~10): 혜택별 + 대상별 앞부분
# ============================================================
POSTS = [
    # 1. 캐시백 신용카드 추천
    {
        "title": "캐시백 신용카드 추천 비교 실속파를 위한 TOP 7",
        "cat": CAT_FINANCE,
        "slug": "cashback-credit-card-recommendation",
        "intro": "카드 혜택 중 가장 직관적인 것이 바로 <strong>캐시백</strong>입니다. 포인트처럼 복잡한 전환 과정 없이, 사용한 금액의 일정 비율이 현금처럼 돌아오기 때문입니다. 하지만 캐시백 카드마다 적립률, 월 한도, 전월 실적 조건이 천차만별이라 꼼꼼한 비교가 필수입니다. 이 글에서는 실속 있는 캐시백 신용카드 7장을 조건별로 비교하고, 나에게 맞는 카드를 고르는 기준을 안내합니다.",
        "sections": [
            ("캐시백 신용카드란 무엇인가", "<p>캐시백 신용카드는 결제 금액의 일정 비율을 <strong>현금성 혜택</strong>으로 돌려주는 카드입니다. 할인형 카드가 특정 가맹점에서만 혜택을 주는 것과 달리, 캐시백 카드는 어디서 결제하든 일정 비율이 적립됩니다.</p><p>캐시백 방식은 크게 세 가지입니다. <strong>①</strong> 결제일에 청구 금액에서 차감하는 <strong>청구할인형</strong>, <strong>②</strong> 별도 캐시백 계좌로 입금되는 <strong>현금 입금형</strong>, <strong>③</strong> 포인트로 적립 후 현금 전환하는 <strong>포인트 전환형</strong>입니다. 가장 체감이 좋은 것은 청구할인형이며, 대부분의 인기 캐시백 카드가 이 방식을 사용합니다.</p>"),
            ("캐시백 신용카드 TOP 7 비교표", "<table><thead><tr><th>카드명</th><th>캐시백률</th><th>월 한도</th><th>전월 실적</th><th>연회비</th></tr></thead><tbody><tr><td>신한 Mr.Life</td><td>0.8%</td><td>1만원</td><td>30만원</td><td>1만원</td></tr><tr><td>KB국민 탄탄대로</td><td>0.7%</td><td>1만원</td><td>30만원</td><td>1만원</td></tr><tr><td>현대 제로 에디션2(캐시백)</td><td>건별 할인</td><td>무제한</td><td>없음</td><td>없음</td></tr><tr><td>삼성 iD SIMPLE</td><td>0.8%</td><td>8천원</td><td>30만원</td><td>1만원</td></tr><tr><td>우리 카드의정석 COOKIE CHECK</td><td>0.5%</td><td>5천원</td><td>없음</td><td>없음</td></tr><tr><td>NH올원 파이카드</td><td>0.7%</td><td>7천원</td><td>30만원</td><td>8천원</td></tr><tr><td>하나 원큐 카드</td><td>0.6%</td><td>6천원</td><td>20만원</td><td>5천원</td></tr></tbody></table>"),
            ("전월 실적 조건 꼼꼼히 따져보기", "<p>캐시백 카드의 핵심은 <strong>전월 실적 조건</strong>입니다. 아무리 캐시백률이 높아도 전월 실적을 채우지 못하면 혜택이 0원이 됩니다.</p><ul><li><strong>30만원 이상</strong>: 대부분의 캐시백 카드 기준. 월 고정지출(통신비, 보험료, 구독료)만으로 충분히 채울 수 있습니다.</li><li><strong>실적 없음</strong>: 현대 제로 에디션2, 우리 COOKIE CHECK 등. 소비가 적은 분에게 유리합니다.</li><li><strong>실적 제외 항목 주의</strong>: 국세, 지방세, 아파트 관리비, 상품권 구매 등은 대부분 실적에서 제외됩니다. 자동이체 항목이 실적에 포함되는지 반드시 확인하세요.</li></ul>"),
            ("캐시백 극대화 전략 4가지", "<ol><li><strong>고정비를 캐시백 카드에 집중</strong>: 통신비, 보험료, 구독료(넷플릭스, 유튜브 등)를 한 카드로 결제하면 전월 실적 + 캐시백을 동시에 확보할 수 있습니다.</li><li><strong>연회비 대비 캐시백 계산</strong>: 연회비 1만원 카드라면, 월 캐시백이 최소 834원 이상이어야 본전입니다. 월 100만원 이상 결제 시 캐시백률 0.8% 기준 8,000원 적립으로 충분히 이득입니다.</li><li><strong>캐시백 한도 도달 시 서브 카드 활용</strong>: 메인 카드의 월 캐시백 한도를 채웠다면, 서브 카드로 전환하여 추가 혜택을 받으세요.</li><li><strong>이벤트 캐시백 챙기기</strong>: 카드사 앱에서 수시로 진행하는 5~10% 이벤트 캐시백을 응모하면 기본 캐시백에 추가 적립됩니다.</li></ol>"),
            ("캐시백 vs 할인 vs 포인트 어떤 카드가 유리할까", "<p>카드 혜택을 비교할 때 가장 흔한 고민입니다.</p><table><thead><tr><th>구분</th><th>캐시백</th><th>할인</th><th>포인트</th></tr></thead><tbody><tr><td>혜택 방식</td><td>현금 환급</td><td>즉시 차감</td><td>적립 후 전환</td></tr><tr><td>체감 만족도</td><td>높음</td><td>가장 높음</td><td>낮음</td></tr><tr><td>사용 편의성</td><td>자동 적용</td><td>자동 적용</td><td>전환 필요</td></tr><tr><td>적합한 사람</td><td>다양한 곳에서 결제</td><td>특정 가맹점 집중</td><td>대량 적립 후 사용</td></tr></tbody></table><p><strong>결론</strong>: 특정 가맹점(마트, 주유소 등)에서 집중 소비하면 할인 카드, 다양한 곳에서 고르게 소비하면 캐시백 카드가 유리합니다. 포인트 카드는 항공 마일리지 등 대량 적립이 목적일 때 선택하세요.</p>"),
        ],
        "faq": [
            ("캐시백 신용카드와 체크카드 중 어떤 것이 유리한가요?", "월 결제액이 30만원 이상이라면 <strong>신용카드</strong>가 유리합니다. 캐시백률이 체크카드보다 높고, 무이자할부·해외결제 등 부가 혜택도 많습니다. 반대로 월 소비가 적거나 소비 통제가 필요하다면 체크카드가 적합합니다."),
            ("캐시백은 세금 신고 시 소득에 포함되나요?", "개인 소비자의 신용카드 캐시백은 <strong>소득으로 보지 않습니다</strong>. 단, 사업자가 사업용 카드로 받는 캐시백은 매입세액 조정 대상이 될 수 있으니 세무사와 확인하세요."),
            ("여러 캐시백 카드를 동시에 쓰면 불이익이 있나요?", "불이익은 없지만, 카드별 전월 실적을 분산 관리해야 하는 번거로움이 있습니다. <strong>메인 카드 1장 + 서브 카드 1장</strong> 구성이 가장 효율적입니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 2. 마일리지 신용카드 추천
    {
        "title": "마일리지 신용카드 추천 항공 적립 카드 비교 총정리",
        "cat": CAT_FINANCE,
        "slug": "mileage-credit-card-recommendation",
        "intro": "해외여행을 자주 가거나 항공 마일리지를 모으고 싶다면 <strong>마일리지 신용카드</strong>가 필수입니다. 같은 소비를 해도 마일리지 카드를 사용하면 연 1~2회 항공권을 무료로 받을 수 있습니다. 하지만 카드마다 적립 항공사, 적립률, 연회비가 크게 다르기 때문에 본인의 여행 패턴에 맞는 카드를 골라야 합니다. 대한항공, 아시아나, 해외 항공사별 최적의 마일리지 카드를 비교해 드립니다.",
        "sections": [
            ("마일리지 신용카드 기본 원리", "<p>마일리지 카드는 결제 금액에 비례하여 <strong>항공 마일리지</strong>가 적립되는 구조입니다. 보통 1,000원~1,500원당 1마일이 적립되며, 국내선 왕복에 약 15,000마일, 동남아 왕복에 약 35,000~50,000마일이 필요합니다.</p><p>마일리지 적립 방식은 <strong>직접 적립</strong>(카드 결제 시 바로 항공사 마일리지에 합산)과 <strong>전환 적립</strong>(카드 포인트를 마일리지로 전환)으로 나뉩니다. 직접 적립이 전환 손실 없이 유리합니다.</p>"),
            ("항공사별 마일리지 카드 TOP 비교", "<table><thead><tr><th>카드명</th><th>항공사</th><th>적립률</th><th>연회비</th><th>부가혜택</th></tr></thead><tbody><tr><td>신한 대한항공 아시아나클럽</td><td>대한항공</td><td>1,000원=1마일</td><td>1.5만원</td><td>공항라운지</td></tr><tr><td>삼성 iD MILEAGE</td><td>대한항공</td><td>1,500원=1마일</td><td>1.2만원</td><td>해외결제 수수료 면제</td></tr><tr><td>현대 아시아나 CLUB</td><td>아시아나</td><td>1,000원=1마일</td><td>1.5만원</td><td>보너스 마일리지</td></tr><tr><td>KB국민 스카이패스</td><td>대한항공</td><td>1,000원=1마일</td><td>1.5만원</td><td>연간 보너스 2,000마일</td></tr><tr><td>하나 대한항공 1Q</td><td>대한항공</td><td>1,500원=1마일</td><td>1만원</td><td>해외 1.5배 적립</td></tr></tbody></table>"),
            ("마일리지 카드 연회비 본전 뽑는 계산법", "<p>마일리지 카드를 쓸 때 가장 중요한 것은 <strong>연회비 대비 적립 마일리지의 가치</strong>입니다.</p><ul><li>마일리지 1마일의 가치: 대한항공 기준 약 <strong>15~25원</strong>(특전 항공권 기준)</li><li>연회비 1.5만원 카드에서 본전을 뽑으려면: 1.5만원 ÷ 20원 = <strong>750마일</strong> 이상 적립 필요</li><li>1,000원당 1마일 카드 기준: 월 약 <strong>63만원</strong> 이상 결제 시 연회비 본전</li></ul><p>월 100만원 이상 결제한다면 연간 12,000마일 적립으로 <strong>국내선 왕복 항공권</strong>(15,000마일)에 근접합니다. 카드사 이벤트와 보너스 마일리지를 합하면 충분히 달성 가능한 수치입니다.</p>"),
            ("마일리지 빠르게 모으는 꿀팁 5가지", "<ol><li><strong>모든 고정비를 마일리지 카드로</strong>: 통신비, 보험료, 구독료, 공과금을 한 카드에 집중하세요.</li><li><strong>해외 결제 시 2배 적립 이벤트 활용</strong>: 해외여행 시 해외가맹점 2배 적립 카드를 사용하면 적립 속도가 2배입니다.</li><li><strong>항공사 제휴 쇼핑몰 경유</strong>: 대한항공 스카이패스몰, 아시아나 스타얼라이언스 쇼핑 등 경유 구매 시 추가 마일리지 적립됩니다.</li><li><strong>카드사 보너스 마일리지</strong>: 전년도 사용 실적에 따라 연간 1,000~5,000 보너스 마일리지를 제공하는 카드가 있습니다.</li><li><strong>가족 합산 적립</strong>: 가족 카드를 발급받아 마일리지를 한 계정에 합산하면 더 빨리 목표에 도달합니다.</li></ol>"),
            ("마일리지 유효기간과 소멸 방지법", "<p>대한항공 마일리지는 적립일로부터 <strong>10년</strong>, 아시아나는 <strong>12년</strong>이 유효기간입니다. 유효기간 내에 사용하지 않으면 소멸됩니다.</p><ul><li><strong>소멸 예정 마일리지 확인</strong>: 각 항공사 앱에서 연도별 소멸 예정 마일리지를 확인할 수 있습니다.</li><li><strong>좌석 승급</strong>: 보너스 항공권이 부족하면 좌석 승급(이코노미→비즈니스)에 사용하세요.</li><li><strong>제휴사 전환</strong>: 호텔, 렌터카, 쿠폰 등으로 전환하여 소멸을 방지할 수 있습니다.</li></ul>"),
        ],
        "faq": [
            ("마일리지 카드는 해외에서도 적립되나요?", "<strong>네, 해외 가맹점에서도 적립됩니다.</strong> 일부 카드는 해외 결제 시 1.5~2배 적립 혜택을 제공합니다. 단, 해외 결제 수수료(보통 1~1.8%)가 있으므로 수수료 면제 카드를 선택하는 것이 유리합니다."),
            ("마일리지 카드와 캐시백 카드를 함께 쓰는 것이 좋은가요?", "좋은 전략입니다. <strong>고정비는 마일리지 카드</strong>로 꾸준히 적립하고, <strong>변동 소비는 캐시백 카드</strong>로 즉시 환급받는 투카드 전략이 효율적입니다."),
            ("가족 간 마일리지 합산이 가능한가요?", "대한항공은 가족 합산 프로그램을 통해 <strong>최대 5인까지</strong> 마일리지를 합산할 수 있습니다. 아시아나도 가족 마일리지 서비스를 제공합니다. 각 항공사 홈페이지에서 가족 등록 후 이용 가능합니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 3. 주유 할인 신용카드
    {
        "title": "주유 할인 신용카드 추천 리터당 최대 할인 비교",
        "cat": CAT_FINANCE,
        "slug": "gas-discount-credit-card",
        "intro": "자동차를 운전하는 분이라면 매달 주유비가 상당한 지출입니다. <strong>주유 할인 신용카드</strong>를 잘 활용하면 리터당 최대 100~300원까지 할인받을 수 있어 연간 수십만 원을 절약할 수 있습니다. SK에너지, GS칼텍스, S-OIL, HD현대오일뱅크 등 정유사별 제휴 카드와 전 주유소 할인 카드를 비교하여 최적의 카드를 찾아보겠습니다.",
        "sections": [
            ("주유 할인 카드 선택 기준 3가지", "<p>주유 카드를 고를 때 반드시 확인해야 할 3가지 기준입니다.</p><ol><li><strong>자주 가는 주유소 브랜드</strong>: 특정 정유사 제휴 카드는 해당 주유소에서만 할인됩니다. 집·회사 근처 주유소 브랜드를 먼저 확인하세요.</li><li><strong>리터당 할인 금액 vs 월 한도</strong>: 리터당 할인이 높아도 월 할인 한도가 낮으면 실익이 적습니다. 월 주유량 기준으로 계산하세요.</li><li><strong>전월 실적 조건</strong>: 주유 할인을 받으려면 전월 30~50만원 이상 사용해야 하는 카드가 대부분입니다.</li></ol>"),
            ("주유 할인 카드 TOP 7 비교표", "<table><thead><tr><th>카드명</th><th>할인</th><th>대상 주유소</th><th>월 한도</th><th>전월 실적</th><th>연회비</th></tr></thead><tbody><tr><td>현대 오일뱅크 카드</td><td>L당 80원</td><td>HD현대오일뱅크</td><td>200L</td><td>30만원</td><td>1만원</td></tr><tr><td>신한 S-OIL</td><td>L당 60원</td><td>S-OIL</td><td>200L</td><td>30만원</td><td>1만원</td></tr><tr><td>삼성 iD SK에너지</td><td>L당 주유 할인</td><td>SK에너지</td><td>200L</td><td>30만원</td><td>1만원</td></tr><tr><td>KB국민 GS칼텍스</td><td>L당 60원</td><td>GS칼텍스</td><td>200L</td><td>30만원</td><td>1만원</td></tr><tr><td>롯데 오토모빌</td><td>L당 80원</td><td>전 주유소</td><td>150L</td><td>40만원</td><td>1.5만원</td></tr><tr><td>하나 주유 플러스</td><td>L당 60원</td><td>전 주유소</td><td>200L</td><td>30만원</td><td>1만원</td></tr><tr><td>NH 주유 올원</td><td>L당 50원</td><td>전 주유소</td><td>300L</td><td>30만원</td><td>8천원</td></tr></tbody></table>"),
            ("월 주유량별 예상 절약 금액", "<p>내 주유 패턴에 따른 연간 절약 금액을 계산해봅시다.</p><table><thead><tr><th>월 주유량</th><th>리터당 60원 할인</th><th>리터당 80원 할인</th><th>연간 절약</th></tr></thead><tbody><tr><td>100L (약 15만원)</td><td>6,000원/월</td><td>8,000원/월</td><td>7.2~9.6만원</td></tr><tr><td>150L (약 23만원)</td><td>9,000원/월</td><td>12,000원/월</td><td>10.8~14.4만원</td></tr><tr><td>200L (약 30만원)</td><td>12,000원/월</td><td>16,000원/월</td><td>14.4~19.2만원</td></tr></tbody></table><p>월 150L 이상 주유하는 분이라면 연간 <strong>10만원 이상</strong> 절약이 가능합니다. 연회비를 감안해도 확실한 이득입니다.</p>"),
            ("주유 할인 극대화 팁", "<ul><li><strong>셀프 주유소 + 주유 카드</strong>: 셀프 주유소는 리터당 50~100원 저렴합니다. 여기에 카드 할인까지 더하면 이중 절약됩니다.</li><li><strong>주유 앱 활용</strong>: 오피넷(opinet.co.kr)에서 근처 최저가 주유소를 검색하세요.</li><li><strong>주유 쿠폰 병행</strong>: 정유사 앱(SK에너지 엔크린, GS칼텍스 등)의 추가 할인 쿠폰과 카드 할인은 중복 적용됩니다.</li><li><strong>하이패스 카드 겸용</strong>: 하이패스 할인 + 주유 할인이 함께 되는 카드를 선택하면 자동차 관련 비용을 한 카드로 관리할 수 있습니다.</li></ul>"),
        ],
        "faq": [
            ("전 주유소 할인 카드와 특정 정유사 카드 중 어떤 것이 좋나요?", "항상 같은 주유소를 이용한다면 <strong>특정 정유사 카드</strong>가 리터당 할인이 더 큽니다. 여러 주유소를 번갈아 이용한다면 <strong>전 주유소 할인 카드</strong>가 편리합니다."),
            ("주유 카드의 전월 실적에 주유비가 포함되나요?", "대부분의 카드에서 <strong>주유비는 전월 실적에 포함</strong>됩니다. 단, 일부 카드는 주유비를 실적에서 제외하는 경우가 있으니 약관을 반드시 확인하세요."),
            ("전기차도 주유 카드 혜택을 받을 수 있나요?", "기존 주유 할인 카드는 전기차 충전에 적용되지 않습니다. 전기차 사용자는 <strong>전기차 충전 할인 전용 카드</strong>(현대 EV카드, 삼성 EV카드 등)를 별도로 알아보시는 것이 좋습니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 4. 통신비 할인 신용카드
    {
        "title": "통신비 할인 신용카드 추천 매달 자동 절약하는 방법",
        "cat": CAT_FINANCE,
        "slug": "telecom-discount-credit-card",
        "intro": "통신비는 매달 고정으로 나가는 지출입니다. <strong>통신비 할인 신용카드</strong>를 사용하면 월 5,000원~15,000원까지 자동 할인받을 수 있어 연간 6만~18만원을 절약할 수 있습니다. SKT, KT, LG U+ 등 통신사별 제휴 카드와 전 통신사 할인 카드를 비교하여 최적의 선택을 안내합니다.",
        "sections": [
            ("통신비 할인 카드의 할인 방식", "<p>통신비 할인 카드는 크게 두 가지 방식으로 작동합니다.</p><ul><li><strong>자동납부 할인</strong>: 카드로 통신비를 자동납부하면 매월 일정 금액이 청구서에서 차감됩니다. 가장 일반적인 방식입니다.</li><li><strong>포인트 차감</strong>: 카드 사용 포인트를 통신비에서 차감하는 방식입니다. 자동 할인보다 체감이 덜하지만 유연하게 사용 가능합니다.</li></ul><p>대부분의 통신비 할인 카드는 <strong>전월 실적 30~50만원</strong> 이상 사용 시 할인이 적용됩니다. 단, 실적 조건 없이 할인하는 카드도 있으니 소비 패턴에 따라 선택하세요.</p>"),
            ("통신사별 제휴 카드 비교", "<table><thead><tr><th>카드명</th><th>통신사</th><th>할인 금액</th><th>전월 실적</th><th>연회비</th></tr></thead><tbody><tr><td>신한 SKT T 카드</td><td>SKT</td><td>월 최대 1.2만원</td><td>40만원</td><td>1만원</td></tr><tr><td>KB국민 KT 멤버십</td><td>KT</td><td>월 최대 1만원</td><td>30만원</td><td>1만원</td></tr><tr><td>현대 LG U+ 카드</td><td>LG U+</td><td>월 최대 1.1만원</td><td>30만원</td><td>1만원</td></tr><tr><td>삼성 통신할인 카드</td><td>전 통신사</td><td>월 최대 8천원</td><td>30만원</td><td>1만원</td></tr><tr><td>우리 카드의정석 통신</td><td>전 통신사</td><td>월 최대 7천원</td><td>30만원</td><td>5천원</td></tr></tbody></table>"),
            ("통신비 할인 vs 알뜰폰 요금제 어떤 것이 더 절약될까", "<p>통신비를 줄이는 방법은 카드 할인 외에 <strong>알뜰폰(MVNO)</strong>으로 전환하는 것도 있습니다.</p><table><thead><tr><th>구분</th><th>대형 통신사 + 카드할인</th><th>알뜰폰 요금제</th></tr></thead><tbody><tr><td>월 요금 (데이터 10GB)</td><td>55,000원 - 10,000원 = 45,000원</td><td>15,000~25,000원</td></tr><tr><td>통화품질</td><td>동일 (같은 망 사용)</td><td>동일</td></tr><tr><td>부가서비스</td><td>멤버십, 로밍 등</td><td>최소한</td></tr></tbody></table><p>순수 절약 목적이라면 알뜰폰이 더 유리하지만, 멤버십·로밍·가족 결합 등이 필요하면 대형 통신사 + 카드 할인 조합이 적합합니다.</p>"),
            ("통신비 할인 극대화 전략", "<ol><li><strong>가족 결합 + 카드 할인</strong>: 가족 결합 할인과 카드 할인은 중복 적용됩니다. 4인 가족이면 월 4~5만원 절약도 가능합니다.</li><li><strong>인터넷·TV 결합</strong>: 인터넷, TV, 모바일을 한 통신사로 결합하면 추가 할인 + 카드 할인 중복 적용됩니다.</li><li><strong>자동납부 설정 필수</strong>: 대부분의 통신비 할인 카드는 자동납부 등록 시에만 할인이 적용됩니다.</li><li><strong>요금제 재설계</strong>: 실제 데이터 사용량을 확인하고 과도한 요금제를 낮추면 카드 할인과 함께 이중 절약됩니다.</li></ol>"),
        ],
        "faq": [
            ("통신비 할인 카드의 할인은 바로 적용되나요?", "카드 발급 후 자동납부를 등록하면 <strong>다음 달 청구분부터</strong> 할인이 적용됩니다. 카드사마다 다를 수 있으니 발급 시 고객센터에 확인하세요."),
            ("가족 모두 같은 카드를 써야 하나요?", "아닙니다. <strong>본인 카드로 가족 회선의 통신비를 자동납부</strong>하면 됩니다. 가족 각자 다른 카드를 쓰되, 통신비 결제만 한 카드에 모으는 전략이 효율적입니다."),
            ("알뜰폰도 카드 할인이 되나요?", "일부 카드에서 가능합니다. <strong>전 통신사 할인 카드</strong>의 경우 알뜰폰(MVNO) 요금에도 할인이 적용되는 경우가 있으니 카드 약관의 '할인 대상 통신사' 항목을 확인하세요."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 5. 배달앱 할인 신용카드
    {
        "title": "배달앱 할인 신용카드 추천 배민 쿠팡이츠 요기요 비교",
        "cat": CAT_FINANCE,
        "slug": "delivery-app-discount-credit-card",
        "intro": "배달 음식 주문이 일상이 된 시대, 매달 배달앱에 쓰는 비용이 만만치 않습니다. <strong>배달앱 할인 신용카드</strong>를 활용하면 주문 건당 5~10% 할인 또는 월 최대 만원 이상의 청구할인을 받을 수 있습니다. 배달의민족, 쿠팡이츠, 요기요 등 주요 배달앱별 최적의 할인 카드를 비교해 드립니다.",
        "sections": [
            ("배달앱 할인 카드의 종류", "<p>배달앱 할인 카드는 크게 세 가지 유형으로 나뉩니다.</p><ul><li><strong>특정 배달앱 제휴 카드</strong>: 배달의민족 현대카드, 쿠팡이츠 전용 할인 등 특정 앱에서 높은 할인율을 제공합니다.</li><li><strong>간편결제 할인 카드</strong>: 네이버페이, 카카오페이 등 간편결제 시 추가 할인되는 카드로, 배달앱 결제에도 적용됩니다.</li><li><strong>생활 할인 카드</strong>: 온라인 결제, 모바일 결제 등 포괄적으로 할인하는 카드로, 배달앱도 할인 대상에 포함됩니다.</li></ul>"),
            ("배달앱별 할인 카드 비교표", "<table><thead><tr><th>카드명</th><th>배달앱</th><th>할인율</th><th>월 한도</th><th>전월 실적</th><th>연회비</th></tr></thead><tbody><tr><td>현대 배민 현대카드</td><td>배달의민족</td><td>5%</td><td>5천원</td><td>30만원</td><td>없음</td></tr><tr><td>KB국민 오하쳌</td><td>전 배달앱</td><td>10%</td><td>5천원</td><td>30만원</td><td>1만원</td></tr><tr><td>신한 MR.LIFE</td><td>전 배달앱</td><td>5%</td><td>5천원</td><td>30만원</td><td>1만원</td></tr><tr><td>삼성 iD SIMPLE</td><td>전 온라인</td><td>0.8% 캐시백</td><td>8천원</td><td>30만원</td><td>1만원</td></tr><tr><td>롯데 LOCA 생활비</td><td>전 배달앱</td><td>7%</td><td>3천원</td><td>30만원</td><td>없음</td></tr></tbody></table>"),
            ("배달비까지 절약하는 구독 서비스 + 카드 할인 조합", "<p>배달앱 구독 서비스와 카드 할인을 결합하면 절약 효과가 극대화됩니다.</p><ul><li><strong>배민클럽</strong>(월 3,900원): 배달비 무료 + 카드 5% 할인 = 건당 최대 15~20% 절약</li><li><strong>쿠팡 로켓와우</strong>(월 4,990원): 쿠팡이츠 무료배달 + 카드 할인 중복</li><li><strong>요기요 슈퍼클럽</strong>: 배달비 할인 + 카드 할인 중복 적용</li></ul><p>월 8회 이상 배달 주문하는 분이라면 구독료를 감안해도 <strong>월 1~2만원</strong> 이상 절약 가능합니다.</p>"),
            ("배달앱 지출 관리 팁", "<ol><li><strong>월 배달비 예산 설정</strong>: 카드사 앱에서 배달앱 카테고리 알림을 설정하여 지출을 통제하세요.</li><li><strong>포장 주문 할인 활용</strong>: 포장 시 10~15% 추가 할인하는 가게가 많습니다. 카드 할인과 중복 적용됩니다.</li><li><strong>카드사 이벤트 상시 확인</strong>: 배달앱 결제 시 추가 5~10% 할인 이벤트가 수시로 진행됩니다.</li></ol>"),
        ],
        "faq": [
            ("배달앱 할인 카드와 배달앱 자체 쿠폰은 중복 사용 가능한가요?", "<strong>대부분 중복 적용됩니다.</strong> 배달앱 쿠폰 할인 + 카드 청구 할인은 별개의 할인이므로 동시에 받을 수 있습니다."),
            ("배달의민족과 쿠팡이츠 중 어떤 앱이 카드 할인에 유리한가요?", "카드에 따라 다릅니다. <strong>현대 배민카드</strong>는 배민에서, <strong>KB 오하쳌</strong>은 전 배달앱에서 높은 할인율을 제공합니다. 한 앱만 쓰면 전용 카드, 여러 앱을 쓰면 전체 할인 카드가 유리합니다."),
            ("1인 가구인데 배달 카드가 필요할까요?", "월 배달 주문이 4회 이상이면 카드 할인 효과가 있습니다. 연회비 무료 카드를 선택하면 부담 없이 할인 혜택만 받을 수 있습니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 6. 대형마트 할인 신용카드
    {
        "title": "대형마트 할인 신용카드 추천 이마트 코스트코 홈플러스 비교",
        "cat": CAT_FINANCE,
        "slug": "mart-discount-credit-card",
        "intro": "장보기는 매달 피할 수 없는 지출입니다. <strong>대형마트 할인 신용카드</strong>를 사용하면 결제 금액의 5~10%를 절약할 수 있어 연간 수십만 원의 차이가 납니다. 이마트, 코스트코, 홈플러스, 롯데마트 등 마트별 최적의 카드를 비교하고 장보기 비용을 줄이는 전략을 안내합니다.",
        "sections": [
            ("마트별 제휴 카드 비교", "<table><thead><tr><th>카드명</th><th>대상 마트</th><th>할인율</th><th>월 한도</th><th>전월 실적</th><th>연회비</th></tr></thead><tbody><tr><td>신한 이마트 카드</td><td>이마트</td><td>5~7%</td><td>1만원</td><td>30만원</td><td>1만원</td></tr><tr><td>삼성 코스트코 리워드</td><td>코스트코</td><td>1~3% 적립</td><td>무제한</td><td>없음</td><td>없음</td></tr><tr><td>KB국민 홈플러스</td><td>홈플러스</td><td>5%</td><td>7천원</td><td>30만원</td><td>1만원</td></tr><tr><td>롯데 롯데마트 카드</td><td>롯데마트</td><td>5~10%</td><td>1만원</td><td>30만원</td><td>1만원</td></tr><tr><td>현대 M포인트 카드</td><td>전 마트</td><td>M포인트 적립</td><td>월 1만P</td><td>30만원</td><td>1만원</td></tr></tbody></table>"),
            ("코스트코 결제 카드 선택 가이드", "<p>코스트코는 <strong>삼성카드·현대카드만 결제 가능</strong>한 특수한 환경입니다. 코스트코에서 최대 혜택을 받으려면 다음을 확인하세요.</p><ul><li><strong>삼성 코스트코 리워드 카드</strong>: 코스트코 1~3% 적립 + 전월 실적 없음 + 연회비 무료. 코스트코 전용 카드로 가장 인기가 많습니다.</li><li><strong>현대카드 M</strong>: M포인트 적립 후 현대백화점·마트에서 사용 가능. 코스트코 외 현대 계열 혜택도 원한다면 추천합니다.</li><li><strong>체크카드</strong>: 코스트코에서 모든 체크카드가 결제 가능합니다. 신용카드 없이도 이용 가능합니다.</li></ul>"),
            ("온라인 장보기 할인 카드 활용법", "<p>이마트몰, 쿠팡, 마켓컬리 등 <strong>온라인 장보기</strong>에서도 카드 할인이 적용됩니다.</p><ul><li><strong>이마트몰·SSG닷컴</strong>: 신한 이마트 카드 5% 할인 + SSG머니 적립 중복</li><li><strong>쿠팡</strong>: 로켓와우 회원 + 캐시백 카드 조합으로 실질 5~8% 절약</li><li><strong>마켓컬리</strong>: 특정 카드사 상시 5% 할인 이벤트 활용</li></ul><p>오프라인 마트와 온라인 장보기 카드를 분리하면 각각의 할인 한도를 최대로 활용할 수 있습니다.</p>"),
            ("장보기 비용 절약 종합 전략", "<ol><li><strong>전단지 특가 + 카드 할인</strong>: 마트 전단지 할인 상품에 카드 할인을 더하면 최대 20~30% 절약됩니다.</li><li><strong>마트 자체 앱 쿠폰</strong>: 이마트앱, 홈플러스앱 등에서 추가 할인 쿠폰을 다운받아 카드 할인과 중복 적용하세요.</li><li><strong>대량 구매는 코스트코</strong>: 단가가 저렴한 생필품은 코스트코에서 대량 구매 + 코스트코 카드 적립이 가장 경제적입니다.</li><li><strong>PB상품 활용</strong>: 노브랜드, 홈플러스 시그니처 등 PB상품은 NB 대비 20~40% 저렴합니다.</li></ol>"),
        ],
        "faq": [
            ("마트 카드를 여러 장 만들어야 하나요?", "자주 가는 마트 1~2곳에 맞는 카드만 있으면 충분합니다. 카드를 너무 많이 만들면 전월 실적이 분산되어 오히려 할인을 못 받을 수 있습니다."),
            ("코스트코에서 삼성·현대 외 다른 카드는 정말 안 되나요?", "<strong>신용카드는 삼성·현대만 가능</strong>합니다. 단, 체크카드(직불카드)는 모든 은행 카드가 사용 가능하고, 현금·삼성페이도 결제 가능합니다."),
            ("마트 할인 카드와 온라인 쇼핑 할인 카드를 따로 써야 하나요?", "이상적으로는 분리하는 것이 좋습니다. 각 카드의 월 할인 한도를 최대로 활용할 수 있기 때문입니다. 하지만 카드 관리가 번거롭다면 <strong>전 가맹점 캐시백 카드</strong> 1장으로 통합하는 것도 방법입니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 7. 교통카드 기능 신용카드
    {
        "title": "교통카드 신용카드 추천 대중교통 할인 혜택 비교",
        "cat": CAT_FINANCE,
        "slug": "transportation-credit-card",
        "intro": "매일 대중교통을 이용하는 분이라면 <strong>교통 할인 신용카드</strong>로 교통비를 절약할 수 있습니다. 버스·지하철 10~20% 할인부터, 택시·KTX 할인까지 교통 관련 혜택을 제공하는 카드를 비교해 드립니다. 후불교통 기능이 포함된 카드를 선택하면 별도의 교통카드 충전 없이 편리하게 이용할 수 있습니다.",
        "sections": [
            ("교통카드 신용카드의 핵심 혜택", "<p>교통 신용카드는 다음과 같은 혜택을 제공합니다.</p><ul><li><strong>대중교통 할인</strong>: 버스·지하철 결제 시 10~20% 청구 할인</li><li><strong>후불교통 기능</strong>: 별도 충전 없이 신용카드로 버스·지하철 탑승</li><li><strong>택시 할인</strong>: 택시 결제 시 5~10% 할인</li><li><strong>KTX·SRT 할인</strong>: 기차 예매 시 5~10% 할인</li><li><strong>주차장 할인</strong>: 제휴 주차장 50% 할인</li></ul>"),
            ("교통 할인 카드 TOP 5 비교표", "<table><thead><tr><th>카드명</th><th>대중교통 할인</th><th>택시</th><th>전월 실적</th><th>연회비</th></tr></thead><tbody><tr><td>신한 교통 플러스</td><td>10%</td><td>5%</td><td>30만원</td><td>1만원</td></tr><tr><td>KB국민 위시 교통</td><td>10%</td><td>10%</td><td>30만원</td><td>1만원</td></tr><tr><td>우리 카드의정석 교통</td><td>10%</td><td>5%</td><td>20만원</td><td>5천원</td></tr><tr><td>현대 제로 에디션2</td><td>건별 할인</td><td>건별</td><td>없음</td><td>없음</td></tr><tr><td>하나 교통 원큐</td><td>10%</td><td>5%</td><td>20만원</td><td>5천원</td></tr></tbody></table>"),
            ("월 교통비별 예상 절약 금액", "<table><thead><tr><th>월 교통비</th><th>10% 할인 시</th><th>연간 절약</th></tr></thead><tbody><tr><td>5만원</td><td>5,000원/월</td><td>6만원</td></tr><tr><td>10만원</td><td>10,000원/월</td><td>12만원</td></tr><tr><td>15만원</td><td>15,000원/월</td><td>18만원</td></tr></tbody></table><p>월 교통비가 10만원 이상이라면 연간 <strong>12만원 이상</strong> 절약이 가능합니다. 연회비 1만원을 감안해도 11만원 순이익입니다.</p>"),
            ("교통비 절약 추가 팁", "<ol><li><strong>정기권 + 카드 할인</strong>: 서울시 기후동행카드 등 정기권과 교통 카드 할인을 비교하여 더 유리한 쪽을 선택하세요.</li><li><strong>환승 할인 최대 활용</strong>: 30분 이내 환승 시 기본요금이 면제됩니다. 교통 카드 할인과 환승 할인이 중복 적용됩니다.</li><li><strong>카카오택시 할인</strong>: 카카오페이 연동 카드를 등록하면 택시 결제 시 추가 할인을 받을 수 있습니다.</li></ol>"),
        ],
        "faq": [
            ("후불교통 기능이 모든 신용카드에 있나요?", "아닙니다. <strong>후불교통 기능은 카드 발급 시 별도로 신청</strong>해야 합니다. 대부분의 신용카드에서 옵션으로 추가 가능하지만, 일부 카드는 지원하지 않으니 발급 전 확인하세요."),
            ("체크카드도 교통 할인이 되나요?", "네, 교통 할인 혜택이 있는 <strong>체크카드</strong>도 있습니다. 다만 할인율이 신용카드보다 낮거나 월 할인 한도가 적은 경우가 많습니다."),
            ("교통비 소득공제율은 어떻게 되나요?", "대중교통 이용분은 <strong>소득공제율 80%</strong>가 적용됩니다(일반 카드 15~30% 대비 매우 높음). 교통 카드 할인 + 높은 소득공제율로 이중 혜택을 받을 수 있습니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 8. 온라인 쇼핑 할인 신용카드
    {
        "title": "온라인 쇼핑 할인 신용카드 추천 쿠팡 네이버 비교",
        "cat": CAT_FINANCE,
        "slug": "online-shopping-credit-card",
        "intro": "쿠팡, 네이버쇼핑, 11번가 등 <strong>온라인 쇼핑</strong> 비중이 높은 분이라면 전용 할인 카드로 매달 수만 원을 절약할 수 있습니다. 온라인 결제 시 5~10% 할인되는 카드부터 간편결제(네이버페이, 카카오페이) 연동 할인 카드까지 비교하여 최적의 선택을 안내합니다.",
        "sections": [
            ("온라인 쇼핑 할인 카드 유형", "<ul><li><strong>특정 쇼핑몰 제휴 카드</strong>: 쿠팡 현대카드, 11번가 SK카드 등 특정 플랫폼 전용 할인</li><li><strong>간편결제 할인 카드</strong>: 네이버페이, 카카오페이 결제 시 추가 포인트 적립</li><li><strong>온라인 전 가맹점 할인 카드</strong>: 온라인 결제 건에 대해 일괄 할인 적용</li></ul>"),
            ("온라인 쇼핑 할인 카드 TOP 비교", "<table><thead><tr><th>카드명</th><th>대상</th><th>할인율</th><th>월 한도</th><th>전월 실적</th><th>연회비</th></tr></thead><tbody><tr><td>현대 쿠팡 카드</td><td>쿠팡</td><td>로켓배송 2~4%</td><td>1만원</td><td>30만원</td><td>없음</td></tr><tr><td>신한 네이버페이 카드</td><td>네이버페이</td><td>최대 3% 적립</td><td>무제한</td><td>없음</td><td>없음</td></tr><tr><td>삼성 iD ONLINE</td><td>전 온라인</td><td>5%</td><td>5천원</td><td>30만원</td><td>1만원</td></tr><tr><td>KB국민 톡톡O</td><td>전 온라인</td><td>5%</td><td>5천원</td><td>30만원</td><td>1만원</td></tr><tr><td>카카오페이 신한카드</td><td>카카오페이</td><td>최대 3% 적립</td><td>무제한</td><td>없음</td><td>없음</td></tr></tbody></table>"),
            ("쿠팡 로켓와우 + 카드 할인 조합", "<p>쿠팡 헤비유저라면 <strong>로켓와우</strong>(월 4,990원) + <strong>현대 쿠팡카드</strong> 조합이 최적입니다.</p><ul><li>로켓배송 무료 + 와우할인가 적용</li><li>쿠팡카드 추가 2~4% 적립</li><li>쿠팡이츠 무료배달</li><li>쿠팡플레이 무료 스트리밍</li></ul><p>월 쿠팡 결제액 20만원 기준, 와우할인가 + 카드 적립으로 <strong>월 1~2만원</strong> 이상 절약됩니다.</p>"),
            ("네이버페이 포인트 극대화 전략", "<p>네이버쇼핑을 자주 이용한다면 <strong>네이버페이 충전 + 신한 네이버페이 카드</strong> 조합이 유리합니다.</p><ol><li>네이버페이 머니 충전 시 기본 적립</li><li>네이버페이 카드 결제 시 추가 적립</li><li>네이버 멤버십(월 4,900원) 가입 시 4% 추가 적립</li><li>네이버쇼핑 리뷰 작성 시 추가 포인트</li></ol><p>이 모든 적립을 합하면 실질 할인율이 <strong>7~10%</strong>에 달합니다.</p>"),
        ],
        "faq": [
            ("온라인 쇼핑 할인 카드는 오프라인에서는 혜택이 없나요?", "온라인 전용 할인 카드라도 오프라인에서 <strong>기본 캐시백이나 포인트 적립</strong>은 됩니다. 단, 온라인 전용 추가 할인은 오프라인에서 적용되지 않습니다."),
            ("해외 직구도 할인 대상인가요?", "카드에 따라 다릅니다. <strong>해외 온라인 결제</strong>가 할인 대상에 포함되는 카드가 있고, 국내 온라인만 해당하는 카드도 있습니다. 해외 직구가 많다면 약관의 '할인 대상 가맹점' 항목을 확인하세요."),
            ("간편결제 카드와 일반 카드 중 어떤 것이 유리한가요?", "간편결제(네이버페이, 카카오페이)를 자주 쓴다면 전용 카드가 유리합니다. <strong>실적 조건 없이 상시 적립</strong>되는 것이 장점입니다. 다양한 곳에서 결제한다면 일반 온라인 할인 카드가 범용성이 좋습니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 9. 직장인 신용카드 추천
    {
        "title": "직장인 신용카드 추천 연봉별 혜택 비교 가이드",
        "cat": CAT_FINANCE,
        "slug": "office-worker-credit-card",
        "intro": "직장인에게 신용카드는 단순한 결제 수단이 아니라 <strong>연말정산 소득공제, 생활비 절약, 포인트 적립</strong>을 위한 필수 재테크 도구입니다. 하지만 수백 장의 카드 중 나에게 맞는 카드를 고르기 어렵습니다. 연봉 구간별, 소비 패턴별 최적의 신용카드를 비교하고 직장인이 알아야 할 카드 활용 전략을 안내합니다.",
        "sections": [
            ("연봉 구간별 추천 카드 전략", "<table><thead><tr><th>연봉 구간</th><th>추천 카드 유형</th><th>핵심 전략</th></tr></thead><tbody><tr><td>3,000만원 이하</td><td>연회비 무료 + 캐시백</td><td>소비 통제, 실질 할인 위주</td></tr><tr><td>3,000~5,000만원</td><td>생활할인 + 포인트 카드</td><td>고정지출 할인, 소득공제 최적화</td></tr><tr><td>5,000~7,000만원</td><td>프리미엄 일반 카드</td><td>공항라운지, 해외결제 혜택</td></tr><tr><td>7,000만원 이상</td><td>프리미엄 + 마일리지</td><td>여행, 골프, 프리미엄 서비스</td></tr></tbody></table>"),
            ("직장인 필수 카드 TOP 5", "<table><thead><tr><th>카드명</th><th>핵심 혜택</th><th>전월 실적</th><th>연회비</th><th>추천 대상</th></tr></thead><tbody><tr><td>현대 제로 에디션2</td><td>전 가맹점 할인, 실적 없음</td><td>없음</td><td>없음</td><td>사회초년생</td></tr><tr><td>신한 Mr.Life</td><td>생활 전 영역 5% 할인</td><td>30만원</td><td>1만원</td><td>3040 직장인</td></tr><tr><td>KB국민 탄탄대로</td><td>캐시백 + 교통 할인</td><td>30만원</td><td>1만원</td><td>대중교통 출퇴근</td></tr><tr><td>삼성 iD MILES</td><td>마일리지 적립</td><td>30만원</td><td>1.5만원</td><td>해외출장/여행</td></tr><tr><td>롯데 LOCA LIKIT</td><td>생활비 5~7% 할인</td><td>30만원</td><td>1만원</td><td>생활비 절약형</td></tr></tbody></table>"),
            ("직장인 연말정산 카드 전략", "<p>연말정산 시 신용카드·체크카드 소득공제는 <strong>연봉의 25%를 초과한 사용분</strong>부터 적용됩니다.</p><ul><li><strong>신용카드</strong>: 소득공제율 15%</li><li><strong>체크카드·현금</strong>: 소득공제율 30%</li><li><strong>대중교통·전통시장</strong>: 소득공제율 40~80%</li></ul><p><strong>최적 전략</strong>: 연봉 25%까지는 혜택이 좋은 신용카드로 결제하고, 25%를 넘기면 체크카드로 전환하여 소득공제율을 높이세요. 카드사 앱에서 연간 사용 누적액을 확인할 수 있습니다.</p>"),
            ("직장인 카드 관리 2장 전략", "<p>카드는 많을수록 관리가 어렵고 실적이 분산됩니다. <strong>메인 카드 1장 + 서브 카드 1장</strong>이 최적입니다.</p><ol><li><strong>메인 카드</strong>: 고정지출(통신비, 보험, 구독료) + 일상 소비 → 전월 실적 확보 + 최대 할인</li><li><strong>서브 카드</strong>: 메인 카드 할인 한도 초과 시 사용 또는 특수 혜택(주유, 마트 등)</li></ol><p>연말정산 시즌에는 체크카드를 서브 카드로 활용하여 소득공제를 극대화하세요.</p>"),
        ],
        "faq": [
            ("사회초년생은 어떤 카드부터 만들어야 하나요?", "<strong>연회비 무료 + 전월 실적 없는 카드</strong>부터 시작하세요. 현대 제로 에디션2가 대표적입니다. 소비 패턴이 안정된 후 혜택이 더 좋은 카드로 갈아타면 됩니다."),
            ("카드를 너무 많이 만들면 신용점수에 불이익이 있나요?", "카드 발급 자체는 신용점수에 큰 영향을 주지 않지만, <strong>단기간에 여러 장</strong>을 발급하면 일시적으로 점수가 하락할 수 있습니다. 6개월 이상 간격을 두고 필요한 카드만 발급하세요."),
            ("법인카드와 개인카드 중 어떤 것으로 결제해야 하나요?", "업무 경비는 <strong>법인카드</strong>, 개인 소비는 <strong>개인카드</strong>로 분리하세요. 법인카드 사용분은 개인 소득공제 대상이 아니며, 혼용 시 세무 문제가 생길 수 있습니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 10. 사회초년생 첫 신용카드 추천
    {
        "title": "사회초년생 첫 신용카드 추천 발급 조건 선택 가이드",
        "cat": CAT_FINANCE,
        "slug": "first-credit-card-recommendation",
        "intro": "취업 후 처음으로 <strong>신용카드</strong>를 만들려고 하면 어디서부터 시작해야 할지 막막합니다. 어떤 카드사가 좋은지, 연회비는 얼마가 적당한지, 혜택은 어떻게 비교하는지 모든 것이 생소합니다. 이 글에서는 사회초년생이 첫 신용카드를 고를 때 반드시 알아야 할 기준과 추천 카드를 안내합니다.",
        "sections": [
            ("첫 신용카드 선택 기준 5가지", "<ol><li><strong>연회비 무료 또는 1만원 이하</strong>: 소비 패턴이 안정되기 전이므로 부담 없는 카드를 선택하세요.</li><li><strong>전월 실적 조건 낮은 카드</strong>: 30만원 이하 또는 실적 없는 카드가 초년생에게 유리합니다.</li><li><strong>자주 쓰는 곳 할인</strong>: 편의점, 카페, 배달앱, 대중교통 등 본인이 가장 많이 쓰는 곳에서 할인되는 카드를 고르세요.</li><li><strong>후불교통 기능</strong>: 별도 교통카드 없이 신용카드로 버스·지하철을 탈 수 있어 편리합니다.</li><li><strong>해외결제 수수료</strong>: 해외여행이나 해외 직구를 자주 한다면 해외결제 수수료 면제 카드를 선택하세요.</li></ol>"),
            ("사회초년생 추천 카드 TOP 5", "<table><thead><tr><th>카드명</th><th>핵심 혜택</th><th>전월 실적</th><th>연회비</th><th>추천 포인트</th></tr></thead><tbody><tr><td>현대 제로 에디션2</td><td>전 가맹점 건별 할인</td><td>없음</td><td>없음</td><td>가장 부담 없는 첫 카드</td></tr><tr><td>신한 Deep On</td><td>온라인 3% 적립</td><td>없음</td><td>없음</td><td>온라인 소비 많은 2030</td></tr><tr><td>KB국민 노리2</td><td>편의점·카페 할인</td><td>20만원</td><td>없음</td><td>편의점·카페 헤비유저</td></tr><tr><td>삼성 iD SIMPLE</td><td>전 가맹점 0.8% 캐시백</td><td>30만원</td><td>1만원</td><td>심플한 캐시백 원하는 분</td></tr><tr><td>카카오뱅크 카카오페이 카드</td><td>카카오페이 3% 적립</td><td>없음</td><td>없음</td><td>카카오페이 자주 쓰는 분</td></tr></tbody></table>"),
            ("신용카드 발급 조건과 과정", "<p>사회초년생이 신용카드를 발급받으려면 다음 조건을 충족해야 합니다.</p><ul><li><strong>연소득 기준</strong>: 연소득 1,200만원 이상(카드사마다 다름). 재직증명서 또는 원천징수영수증으로 증빙합니다.</li><li><strong>신용점수</strong>: NICE 기준 600점 이상이면 대부분 발급 가능합니다. 신용 이력이 없는 사회초년생은 체크카드를 3~6개월 사용한 후 신용카드를 발급받으면 승인율이 높아집니다.</li><li><strong>발급 방법</strong>: 카드사 앱, 홈페이지, 은행 방문, 카드고릴라 등 비교사이트에서 신청 가능합니다.</li></ul>"),
            ("첫 카드 발급 후 꼭 해야 할 것", "<ol><li><strong>카드사 앱 설치</strong>: 실시간 사용 내역 확인, 이벤트 응모, 월 사용 금액 관리에 필수입니다.</li><li><strong>자동납부 등록</strong>: 통신비, 구독료 등을 자동납부로 설정하면 전월 실적을 자연스럽게 채울 수 있습니다.</li><li><strong>결제일 설정</strong>: 월급일 직후로 결제일을 설정하면 연체 위험이 줄어듭니다.</li><li><strong>할부·리볼빙 주의</strong>: 할부는 꼭 필요한 경우만, 리볼빙(최소결제)은 절대 사용하지 마세요. 연 15~20% 이자가 붙습니다.</li></ol>"),
            ("신용점수 관리 기본 원칙", "<p>첫 카드를 잘 관리하면 <strong>신용점수</strong>가 꾸준히 올라갑니다.</p><ul><li><strong>연체 금지</strong>: 단 1회 연체도 신용점수에 큰 타격을 줍니다. 자동이체를 꼭 설정하세요.</li><li><strong>한도의 30% 이내 사용</strong>: 카드 한도의 30% 이상을 매달 사용하면 '과도한 카드 사용'으로 점수가 하락할 수 있습니다.</li><li><strong>꾸준한 사용</strong>: 카드를 발급받고 사용하지 않는 것보다, 소액이라도 꾸준히 사용하는 것이 신용 이력에 긍정적입니다.</li></ul>"),
        ],
        "faq": [
            ("체크카드와 신용카드 중 먼저 만들어야 할 것은?", "신용 이력이 전혀 없다면 <strong>체크카드를 3~6개월 먼저</strong> 사용하세요. 이후 신용카드를 발급받으면 승인율이 높고, 더 좋은 조건의 카드를 받을 수 있습니다."),
            ("카드 한도가 너무 낮게 나왔는데 어떻게 하나요?", "사회초년생은 보통 한도 100~300만원으로 시작합니다. <strong>6개월~1년</strong> 성실하게 사용하면 카드사에서 자동으로 한도 상향을 제안하거나, 앱에서 한도 상향을 신청할 수 있습니다."),
            ("카드 발급이 거절되었는데 어떻게 해야 하나요?", "거절 사유를 카드사 고객센터에 문의하세요. 흔한 사유는 <strong>소득 부족, 신용 이력 없음, 단기간 다수 발급 신청</strong>입니다. 체크카드로 3~6개월 이력을 쌓은 후 재신청하면 승인 가능성이 높아집니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 11. 자영업자 사업용 신용카드
    {
        "title": "자영업자 사업용 신용카드 추천 경비처리 세금 절약 가이드",
        "cat": CAT_FINANCE,
        "slug": "business-credit-card-recommendation",
        "intro": "자영업자에게 <strong>사업용 신용카드</strong>는 경비처리와 세금 절약의 핵심 도구입니다. 사업 관련 지출을 개인 카드로 결제하면 경비 증빙이 복잡해지고, 세무조사 시 불이익을 받을 수 있습니다. 사업자 전용 카드의 세금 혜택, 추천 카드, 경비처리 팁을 총정리합니다.",
        "sections": [
            ("사업용 신용카드를 써야 하는 이유", "<p>사업용 카드를 사용하면 다음과 같은 혜택이 있습니다.</p><ul><li><strong>부가세 매입세액 공제</strong>: 사업용 카드로 결제한 비용은 부가가치세 신고 시 매입세액 공제를 받을 수 있습니다. 개인 카드로 결제하면 공제가 안 되거나 증빙이 복잡합니다.</li><li><strong>경비 자동 분류</strong>: 카드사 앱에서 사업 관련 지출을 자동 분류하여 장부 정리가 간편합니다.</li><li><strong>세무조사 대비</strong>: 개인·사업 지출이 혼재되면 세무조사 시 소명이 어렵습니다. 카드를 분리하면 깔끔합니다.</li><li><strong>사업자 전용 혜택</strong>: 사업자 카드는 세금 납부 할인, 사무용품 할인, 주유 할인 등 사업자 맞춤 혜택을 제공합니다.</li></ul>"),
            ("자영업자 추천 카드 TOP 5", "<table><thead><tr><th>카드명</th><th>핵심 혜택</th><th>전월 실적</th><th>연회비</th><th>추천 업종</th></tr></thead><tbody><tr><td>KB국민 비즈 올림</td><td>세금 0.5% 할인, 주유 60원/L</td><td>50만원</td><td>1만원</td><td>전 업종</td></tr><tr><td>신한 비즈 플러스</td><td>사무용품 5%, 택배 3%</td><td>50만원</td><td>1만원</td><td>온라인 사업자</td></tr><tr><td>현대 비즈 에센셜</td><td>전 가맹점 0.7% 캐시백</td><td>30만원</td><td>없음</td><td>소규모 사업자</td></tr><tr><td>삼성 비즈보드 카드</td><td>경비 관리 + 세금 할인</td><td>50만원</td><td>1만원</td><td>법인 전환 예정</td></tr><tr><td>우리 비즈 카드</td><td>국세 할인 + 주유 할인</td><td>30만원</td><td>5천원</td><td>운수업/영업직</td></tr></tbody></table>"),
            ("사업용 카드 경비처리 핵심 정리", "<ul><li><strong>홈택스 사업용 카드 등록</strong>: 국세청 홈택스에 사업용 카드를 등록하면 부가세 매입세액 공제가 자동 반영됩니다. 등록은 무료이며 카드 여러 장 등록 가능합니다.</li><li><strong>경비 인정 항목</strong>: 사무용품, 접대비, 교통비, 통신비, 광고비, 임차료 등 사업과 관련된 모든 지출이 경비로 인정됩니다.</li><li><strong>접대비 한도</strong>: 1회 접대비 한도는 법인 아닌 개인사업자 기준 연 2,400만원(기본) + 수입금액 비례 추가 한도입니다.</li><li><strong>개인 지출 혼용 금지</strong>: 사업용 카드로 개인 지출을 하면 세무상 불이익이 발생합니다. 반드시 분리하세요.</li></ul>"),
            ("세금 납부 시 카드 할인 활용", "<p>국세·지방세를 카드로 납부하면 할인을 받을 수 있습니다.</p><ul><li><strong>국세 카드 납부</strong>: 부가세, 종합소득세 등을 카드로 납부하면 수수료 0.8%가 발생하지만, 카드 할인(0.5~1%)과 무이자할부를 활용하면 실질 이득입니다.</li><li><strong>지방세 카드 납부</strong>: 재산세, 자동차세 등 지방세는 카드 수수료가 없어 카드 혜택을 그대로 받을 수 있습니다.</li><li><strong>무이자할부</strong>: 세금 납부 시 2~6개월 무이자할부를 지원하는 카드사가 많아 현금흐름 관리에 유리합니다.</li></ul>"),
        ],
        "faq": [
            ("개인사업자도 법인카드를 만들 수 있나요?", "개인사업자는 <strong>법인카드가 아닌 사업자 카드</strong>를 발급받습니다. 사업자등록증과 소득증빙으로 신청 가능합니다. 법인카드는 법인 등기가 완료된 법인만 발급 가능합니다."),
            ("사업용 카드와 개인 카드를 하나로 쓰면 안 되나요?", "가능하지만 <strong>권장하지 않습니다</strong>. 세무 신고 시 개인·사업 지출을 일일이 분류해야 하고, 세무조사 시 소명이 어렵습니다. 카드를 분리하면 이런 번거로움이 사라집니다."),
            ("배달·택배 라이더도 사업용 카드가 필요한가요?", "네, 배달·택배 라이더는 <strong>프리랜서(사업소득자)</strong>로 분류됩니다. 오토바이 주유비, 수리비, 통신비 등을 사업용 카드로 결제하면 경비처리가 가능하여 종합소득세를 줄일 수 있습니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 12. 대학생 카드 추천
    {
        "title": "대학생 신용카드 체크카드 추천 혜택 비교 총정리",
        "cat": CAT_FINANCE,
        "slug": "student-credit-card-recommendation",
        "intro": "대학생 시절부터 <strong>카드 혜택</strong>을 잘 활용하면 월 수만 원을 절약할 수 있습니다. 편의점, 카페, 대중교통 등 대학생이 자주 쓰는 곳에서 할인이 큰 카드를 비교하고, 신용카드와 체크카드 중 어떤 것이 유리한지 안내합니다.",
        "sections": [
            ("대학생은 신용카드 vs 체크카드 어떤 것이 좋을까", "<table><thead><tr><th>구분</th><th>신용카드</th><th>체크카드</th></tr></thead><tbody><tr><td>발급 조건</td><td>소득 증빙 필요</td><td>통장만 있으면 가능</td></tr><tr><td>소비 통제</td><td>한도까지 사용 가능(과소비 위험)</td><td>잔액 내에서만 결제(통제 쉬움)</td></tr><tr><td>혜택 수준</td><td>높음</td><td>보통</td></tr><tr><td>신용 이력</td><td>쌓임(향후 유리)</td><td>쌓이지 않음</td></tr><tr><td>연말정산 공제율</td><td>15%</td><td>30%</td></tr></tbody></table><p><strong>추천</strong>: 아르바이트 소득이 있으면 신용카드(한도 소액)로 신용 이력을 쌓고, 소득이 없으면 체크카드로 시작하세요.</p>"),
            ("대학생 추천 체크카드 TOP 5", "<table><thead><tr><th>카드명</th><th>핵심 혜택</th><th>연회비</th><th>추천 포인트</th></tr></thead><tbody><tr><td>카카오뱅크 체크카드</td><td>카페·편의점 5% 할인</td><td>없음</td><td>카카오페이 연동</td></tr><tr><td>토스뱅크 체크카드</td><td>전 가맹점 0.4% 캐시백</td><td>없음</td><td>조건 없이 캐시백</td></tr><tr><td>KB국민 노리2 체크</td><td>편의점·카페·배달 10%</td><td>없음</td><td>학생 혜택 최강</td></tr><tr><td>신한 체크 SOL</td><td>편의점 5%, 교통 5%</td><td>없음</td><td>교통 할인 겸용</td></tr><tr><td>우리 카드의정석 CHECK</td><td>캐시백 0.5%</td><td>없음</td><td>실적 없이 캐시백</td></tr></tbody></table>"),
            ("대학생 할인 극대화 꿀팁", "<ol><li><strong>편의점 할인 카드 활용</strong>: CU, GS25, 세븐일레븐 등 편의점 할인 카드를 사용하면 매일 500~1,000원 절약 가능합니다.</li><li><strong>카페 구독 + 카드 할인</strong>: 메가커피, 컴포즈 등 저가 카페에서 카드 할인을 받으면 한 잔당 200~500원 추가 절약됩니다.</li><li><strong>교통비 소득공제</strong>: 대학생도 아르바이트 소득이 있으면 연말정산 가능합니다. 대중교통 공제율 80%를 활용하세요.</li><li><strong>카드사 20대 전용 이벤트</strong>: 카드사마다 20대 전용 캐시백, 쿠폰 이벤트를 수시로 진행합니다. 카드사 앱을 꼭 설치하세요.</li></ol>"),
            ("대학생 카드 사용 주의사항", "<ul><li><strong>할부 사용 금지</strong>: 아르바이트 소득으로 할부금을 감당하기 어렵습니다. 일시불 결제를 원칙으로 하세요.</li><li><strong>리볼빙 절대 금지</strong>: 최소결제(리볼빙)는 연 15~20% 이자가 붙는 사실상의 고금리 대출입니다.</li><li><strong>카드 한도 최소 설정</strong>: 신용카드 발급 시 한도를 최소(100~200만원)로 설정하여 과소비를 방지하세요.</li><li><strong>연체 절대 금지</strong>: 학생 때 연체 기록이 생기면 졸업 후 주담대, 신용대출 등에서 불이익을 받습니다.</li></ul>"),
        ],
        "faq": [
            ("대학생도 신용카드를 만들 수 있나요?", "아르바이트 등 <strong>소득이 있으면 가능</strong>합니다. 4대보험에 가입된 아르바이트, 프리랜서 소득 등으로 증빙하면 됩니다. 소득이 없으면 체크카드부터 시작하세요."),
            ("부모님 가족카드를 쓰는 것과 본인 카드 중 어떤 것이 좋나요?", "소비 통제 목적이면 가족카드가 유리하고, <strong>본인 신용 이력</strong>을 쌓으려면 본인 명의 카드가 필요합니다. 졸업 후 신용카드·대출 발급에 유리하므로, 가능하면 본인 카드를 1장 이상 만드는 것을 권합니다."),
            ("체크카드도 신용점수에 영향을 주나요?", "체크카드는 신용점수에 <strong>직접적 영향을 주지 않습니다</strong>. 신용 이력을 쌓으려면 신용카드를 사용해야 합니다. 다만 체크카드 사용 이력이 있으면 신용카드 발급 심사 시 긍정적으로 반영될 수 있습니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 13. 주부 생활비 절약 신용카드
    {
        "title": "주부 생활비 절약 신용카드 추천 마트 육아 할인 비교",
        "cat": CAT_FINANCE,
        "slug": "housewife-credit-card-recommendation",
        "intro": "가정의 <strong>생활비 관리</strong>를 담당하는 주부에게 신용카드는 강력한 절약 도구입니다. 마트 장보기, 교육비, 의료비, 온라인 쇼핑 등 가정 지출의 대부분에서 할인을 받을 수 있습니다. 생활비 항목별 최적의 카드를 비교하고 월 수만 원을 절약하는 전략을 안내합니다.",
        "sections": [
            ("생활비 항목별 추천 카드", "<table><thead><tr><th>지출 항목</th><th>추천 카드</th><th>할인율</th><th>월 절약 예상</th></tr></thead><tbody><tr><td>대형마트</td><td>신한 이마트 / 롯데마트 카드</td><td>5~10%</td><td>1~2만원</td></tr><tr><td>온라인 장보기</td><td>현대 쿠팡카드</td><td>2~4%</td><td>5천~1만원</td></tr><tr><td>교육비(학원)</td><td>KB국민 교육비 카드</td><td>5%</td><td>1~3만원</td></tr><tr><td>의료비</td><td>삼성 의료비 할인 카드</td><td>5%</td><td>5천~1만원</td></tr><tr><td>통신비</td><td>통신사 제휴 카드</td><td>월 1만원</td><td>1만원</td></tr></tbody></table><p>이 카드들을 조합하면 월 <strong>4~8만원</strong>, 연간 <strong>48~96만원</strong>을 절약할 수 있습니다.</p>"),
            ("전업주부 카드 발급 가능 여부", "<p>소득이 없는 전업주부도 신용카드를 발급받을 수 있습니다.</p><ul><li><strong>배우자 소득 증빙</strong>: 배우자의 재직증명서·소득증명서로 발급 가능합니다.</li><li><strong>재산 증빙</strong>: 부동산, 예금 등 재산으로 발급 가능합니다.</li><li><strong>가족카드</strong>: 배우자의 본인 카드에 가족카드를 추가 발급하는 방법도 있습니다.</li><li><strong>체크카드</strong>: 소득 증빙 없이 발급 가능하며, 생활비 할인 혜택도 충분합니다.</li></ul>"),
            ("생활비 카드 2장 전략", "<p>생활비 관리를 위한 최적의 카드 조합입니다.</p><ol><li><strong>메인 카드 (생활 할인형)</strong>: 마트, 온라인 쇼핑, 교육비 등 주요 지출에 사용. 전월 실적을 이 카드에 집중하세요.</li><li><strong>서브 카드 (캐시백/포인트형)</strong>: 메인 카드 할인 한도 초과 시 또는 기타 지출에 사용.</li></ol><p>카드를 3장 이상 쓰면 실적이 분산되어 오히려 손해입니다. <strong>2장 이내</strong>로 관리하세요.</p>"),
            ("가계부 앱 + 카드 연동 활용법", "<ul><li><strong>뱅크샐러드</strong>: 모든 카드 사용 내역을 한곳에서 확인. 카테고리별 지출 분석 가능.</li><li><strong>카카오페이 가계부</strong>: 카카오페이 연동 카드의 지출을 자동 분류.</li><li><strong>네이버 가계부</strong>: 영수증 촬영으로 현금 지출도 기록 가능.</li></ul><p>카드 사용 내역이 자동으로 가계부에 반영되므로 별도로 기록할 필요가 없습니다. 월말에 카테고리별 지출을 확인하고 다음 달 예산을 조정하세요.</p>"),
        ],
        "faq": [
            ("전업주부도 연말정산 혜택을 받을 수 있나요?", "전업주부 본인은 소득이 없으므로 연말정산 대상이 아닙니다. 하지만 <strong>배우자의 연말정산</strong>에서 가족카드 사용분이 소득공제 대상이 됩니다. 배우자 명의 가족카드를 쓰는 것이 소득공제에 유리합니다."),
            ("아이 교육비도 카드 할인이 되나요?", "학원비, 교재비 등은 카드 결제가 가능한 곳이면 <strong>카드 할인 적용</strong>됩니다. 교육비 전용 할인 카드나, 생활 할인 카드의 교육 카테고리 할인을 활용하세요."),
            ("생활비를 현금으로 쓰는 것과 카드로 쓰는 것 중 어떤 것이 유리한가요?", "카드가 유리합니다. 카드 할인 혜택 + 소득공제(배우자 연말정산) + 지출 관리 편의성 모두 카드가 앞섭니다. 단, <strong>과소비 방지</strong>를 위해 체크카드를 사용하거나 카드 한도를 낮게 설정하세요."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 14. 프리랜서 신용카드
    {
        "title": "프리랜서 신용카드 추천 소득 증빙 경비처리 가이드",
        "cat": CAT_FINANCE,
        "slug": "freelancer-credit-card-recommendation",
        "intro": "프리랜서는 고정 소득이 없어 카드 발급이 어렵고, 경비처리와 세금 관리도 복잡합니다. 하지만 <strong>프리랜서에게 맞는 신용카드</strong>를 선택하면 경비 증빙이 간편해지고, 종합소득세 절세에도 도움이 됩니다. 프리랜서 카드 발급 팁, 추천 카드, 경비처리 방법을 총정리합니다.",
        "sections": [
            ("프리랜서 카드 발급이 어려운 이유와 해결법", "<p>프리랜서는 직장인 대비 카드 발급 승인율이 낮습니다. 그 이유와 해결 방법입니다.</p><ul><li><strong>소득 불안정</strong>: 월 소득이 일정하지 않아 카드사가 리스크로 판단합니다. → <strong>해결</strong>: 최근 3~6개월 입금 내역서(통장 거래내역)를 증빙으로 제출하세요.</li><li><strong>4대보험 미가입</strong>: 직장인과 달리 건강보험 지역가입자이므로 소득 증빙이 어렵습니다. → <strong>해결</strong>: 종합소득세 신고서, 사업소득 원천징수영수증을 제출하세요.</li><li><strong>사업자등록 여부</strong>: 사업자등록을 하면 사업자 카드 발급이 가능해져 선택지가 넓어집니다.</li></ul>"),
            ("프리랜서 추천 카드 TOP 5", "<table><thead><tr><th>카드명</th><th>핵심 혜택</th><th>전월 실적</th><th>연회비</th><th>발급 난이도</th></tr></thead><tbody><tr><td>현대 제로 에디션2</td><td>실적 없이 건별 할인</td><td>없음</td><td>없음</td><td>쉬움</td></tr><tr><td>카카오뱅크 신용카드</td><td>간편 발급, 캐시백</td><td>없음</td><td>없음</td><td>쉬움</td></tr><tr><td>토스뱅크 신용카드</td><td>전 가맹점 캐시백</td><td>없음</td><td>없음</td><td>쉬움</td></tr><tr><td>신한 비즈 플러스</td><td>사업 경비 할인</td><td>50만원</td><td>1만원</td><td>사업자등록 필요</td></tr><tr><td>KB국민 비즈 올림</td><td>세금 납부 할인</td><td>50만원</td><td>1만원</td><td>사업자등록 필요</td></tr></tbody></table>"),
            ("프리랜서 경비처리와 카드 활용", "<p>프리랜서가 카드로 경비처리할 수 있는 항목입니다.</p><ul><li><strong>업무용 장비</strong>: 노트북, 모니터, 카메라, 소프트웨어 구독료 등</li><li><strong>통신비</strong>: 휴대폰, 인터넷 요금 (업무 사용 비율만큼)</li><li><strong>교통비</strong>: 미팅·출장 시 택시비, KTX, 주유비</li><li><strong>식비</strong>: 클라이언트 미팅 시 식대 (접대비)</li><li><strong>교육비</strong>: 업무 관련 강의, 세미나, 도서 구매비</li><li><strong>사무실 비용</strong>: 공유오피스 이용료, 사무용품</li></ul><p>이 항목들을 사업용 카드로 결제하면 <strong>종합소득세 신고 시 경비로 인정</strong>받아 세금을 줄일 수 있습니다.</p>"),
            ("프리랜서 세금 절약 카드 전략", "<ol><li><strong>사업용 카드 홈택스 등록</strong>: 등록하면 부가세 매입세액 공제가 자동 반영됩니다.</li><li><strong>개인·사업 카드 분리</strong>: 경비처리 카드와 생활비 카드를 분리하여 세무 관리를 간편하게 하세요.</li><li><strong>국세 카드 납부</strong>: 종합소득세를 카드로 납부하면 무이자할부 혜택 + 카드 할인을 받을 수 있습니다.</li><li><strong>영수증 관리</strong>: 카드 사용 내역이 자동 기록되므로 별도 영수증 보관이 불필요합니다.</li></ol>"),
        ],
        "faq": [
            ("프리랜서도 사업자등록을 해야 하나요?", "의무는 아니지만 <strong>연 수입이 2,400만원 이상</strong>이면 사업자등록을 하는 것이 유리합니다. 사업자 카드 발급, 매입세액 공제, 경비 인정 범위가 넓어집니다."),
            ("카드사에서 프리랜서 소득을 어떻게 확인하나요?", "<strong>종합소득세 신고서, 소득금액증명원, 통장 거래내역</strong> 등으로 확인합니다. 인터넷 뱅킹 카드사는 계좌 연동으로 소득을 자동 추정하여 발급하기도 합니다."),
            ("유튜버·블로거도 사업용 카드가 필요한가요?", "네, 유튜버·블로거도 <strong>사업소득자</strong>입니다. 촬영 장비, 소프트웨어, 소품 구매 등을 사업용 카드로 결제하면 경비처리가 가능합니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 15. 삼성카드 추천
    {
        "title": "삼성카드 추천 인기 순위 혜택 비교 총정리",
        "cat": CAT_FINANCE,
        "slug": "samsung-card-recommendation",
        "intro": "<strong>삼성카드</strong>는 국내 5대 카드사 중 하나로, 코스트코 결제, 삼성페이 연동, iD 시리즈 등 독자적인 혜택이 강점입니다. 하지만 삼성카드 내에서도 수십 장의 카드가 있어 선택이 어렵습니다. 삼성카드의 인기 카드를 혜택별로 비교하고 나에게 맞는 카드를 찾아보겠습니다.",
        "sections": [
            ("삼성카드 인기 TOP 7 비교표", "<table><thead><tr><th>카드명</th><th>핵심 혜택</th><th>전월 실적</th><th>연회비</th><th>추천 대상</th></tr></thead><tbody><tr><td>iD SIMPLE</td><td>전 가맹점 0.8% 캐시백</td><td>30만원</td><td>1만원</td><td>심플한 캐시백</td></tr><tr><td>iD MILES</td><td>대한항공 마일리지</td><td>30만원</td><td>1.5만원</td><td>마일리지 적립</td></tr><tr><td>iD ONLINE</td><td>온라인 5% 할인</td><td>30만원</td><td>1만원</td><td>온라인 쇼핑</td></tr><tr><td>코스트코 리워드</td><td>코스트코 1~3% 적립</td><td>없음</td><td>없음</td><td>코스트코 회원</td></tr><tr><td>taptap O</td><td>탭탭 결제 할인</td><td>30만원</td><td>1만원</td><td>삼성페이 유저</td></tr><tr><td>삼성 iD SK에너지</td><td>주유 리터당 할인</td><td>30만원</td><td>1만원</td><td>차량 보유자</td></tr><tr><td>삼성 비즈보드</td><td>사업 경비 관리</td><td>50만원</td><td>1만원</td><td>자영업자</td></tr></tbody></table>"),
            ("삼성카드만의 독점 혜택", "<ul><li><strong>코스트코 결제</strong>: 코스트코에서 결제 가능한 신용카드는 삼성카드와 현대카드뿐입니다. 코스트코 이용자에게는 필수입니다.</li><li><strong>삼성페이 최적화</strong>: 삼성 갤럭시 스마트폰의 삼성페이에 등록하면 추가 혜택을 받을 수 있습니다.</li><li><strong>LINK 서비스</strong>: 삼성카드 앱에서 다양한 할인 쿠폰을 LINK하면 결제 시 자동 할인됩니다.</li><li><strong>삼성 계열사 혜택</strong>: 삼성전자, 삼성물산 등 삼성 계열사 쇼핑몰에서 추가 할인·적립이 됩니다.</li></ul>"),
            ("삼성카드 선택 가이드", "<p>본인의 소비 패턴에 따라 다음과 같이 선택하세요.</p><ul><li><strong>다양한 곳에서 고르게 소비</strong> → iD SIMPLE (전 가맹점 캐시백)</li><li><strong>온라인 쇼핑 위주</strong> → iD ONLINE (온라인 5% 할인)</li><li><strong>코스트코 자주 이용</strong> → 코스트코 리워드 카드</li><li><strong>해외여행·출장 잦음</strong> → iD MILES (마일리지 적립)</li><li><strong>차량 보유, 주유 위주</strong> → iD SK에너지</li></ul>"),
            ("삼성카드 앱 활용 팁", "<ol><li><strong>LINK 쿠폰 매일 체크</strong>: 앱에서 매일 새로운 LINK 할인이 제공됩니다. 결제 전 꼭 LINK하세요.</li><li><strong>월 사용 내역 분석</strong>: 카테고리별 지출 분석으로 소비 패턴을 파악하세요.</li><li><strong>이벤트 응모</strong>: 카드사 이벤트에 응모하면 추가 캐시백·상품권을 받을 수 있습니다.</li><li><strong>해외 결제 알림</strong>: 해외 결제 시 실시간 환율과 수수료를 확인할 수 있습니다.</li></ol>"),
        ],
        "faq": [
            ("삼성카드 iD 시리즈 중 가장 인기 있는 카드는?", "<strong>iD SIMPLE</strong>이 가장 인기입니다. 복잡한 조건 없이 전 가맹점에서 0.8% 캐시백을 제공하여 누구에게나 실속 있습니다."),
            ("삼성페이가 없는 아이폰에서도 삼성카드를 쓸 수 있나요?", "물론입니다. 삼성카드 자체는 모든 가맹점에서 사용 가능합니다. 삼성페이는 갤럭시 전용 부가 기능일 뿐, <strong>아이폰에서는 애플페이에 등록</strong>하여 사용할 수 있습니다."),
            ("삼성카드 포인트는 어디에 쓸 수 있나요?", "삼성카드 포인트는 <strong>카드 대금 차감, 삼성전자 제품 구매, 제휴사 포인트 전환</strong> 등에 사용 가능합니다. 가장 가치가 높은 것은 카드 대금 차감(1포인트 = 1원)입니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 16. 현대카드 추천
    {
        "title": "현대카드 추천 인기 순위 혜택 비교 총정리",
        "cat": CAT_FINANCE,
        "slug": "hyundai-card-recommendation",
        "intro": "<strong>현대카드</strong>는 디자인, 프리미엄 서비스, 코스트코 결제로 유명한 카드사입니다. 제로 에디션 시리즈의 실적 조건 없는 혜택이 큰 인기를 끌고 있으며, M포인트·배민 제휴 등 독자적 혜택도 풍부합니다. 현대카드의 인기 카드를 비교하여 나에게 맞는 카드를 찾아보겠습니다.",
        "sections": [
            ("현대카드 인기 TOP 7 비교표", "<table><thead><tr><th>카드명</th><th>핵심 혜택</th><th>전월 실적</th><th>연회비</th><th>추천 대상</th></tr></thead><tbody><tr><td>제로 에디션2 (할인형)</td><td>건별 할인, 모든 가맹점</td><td>없음</td><td>없음</td><td>사회초년생, 서브카드</td></tr><tr><td>제로 에디션2 (포인트형)</td><td>건별 포인트 적립</td><td>없음</td><td>없음</td><td>포인트 모으는 분</td></tr><tr><td>배민 현대카드</td><td>배달의민족 5% 할인</td><td>30만원</td><td>없음</td><td>배달 자주 시키는 분</td></tr><tr><td>현대카드 M</td><td>M포인트 적립</td><td>30만원</td><td>1.5만원</td><td>현대백화점·마트 이용자</td></tr><tr><td>현대카드 X</td><td>프리미엄 라운지·여행</td><td>80만원</td><td>3만원</td><td>고소득 프리미엄</td></tr><tr><td>쿠팡 현대카드</td><td>쿠팡 2~4% 적립</td><td>30만원</td><td>없음</td><td>쿠팡 헤비유저</td></tr><tr><td>현대 오일뱅크 카드</td><td>리터당 80원 할인</td><td>30만원</td><td>1만원</td><td>HD현대오일뱅크 이용자</td></tr></tbody></table>"),
            ("현대카드 제로 에디션2 심층 분석", "<p><strong>제로 에디션2</strong>는 현대카드에서 가장 인기 있는 카드입니다. 전월 실적 조건 없이, 연회비 없이 혜택을 제공합니다.</p><ul><li><strong>할인형</strong>: 건별 결제 금액에서 즉시 할인 (가맹점마다 다름, 보통 200~3,000원)</li><li><strong>포인트형</strong>: 건별 결제 금액에 비례하여 M포인트 적립</li><li><strong>할인형이 유리한 경우</strong>: 소액 결제가 많은 분 (편의점, 카페 등)</li><li><strong>포인트형이 유리한 경우</strong>: 대금 결제가 많은 분 (포인트를 모아 사용)</li></ul>"),
            ("M포인트 활용 가이드", "<p>현대카드의 M포인트는 다양한 곳에서 사용할 수 있습니다.</p><ul><li><strong>현대백화점·한화갤러리아</strong>: M포인트로 백화점 쇼핑 결제</li><li><strong>현대 계열사</strong>: 현대홈쇼핑, 현대리바트 등에서 사용</li><li><strong>카드 대금 차감</strong>: 포인트를 청구 금액에서 차감 (1포인트 = 1원)</li><li><strong>항공 마일리지 전환</strong>: M포인트를 대한항공·아시아나 마일리지로 전환 가능</li></ul>"),
            ("현대카드 앱 프리미엄 기능", "<ol><li><strong>현대카드 라이브러리</strong>: 여행, 쿠킹, 뮤직 라이브러리 등 현대카드 회원 전용 문화 공간</li><li><strong>DIVE</strong>: 소비 데이터 분석 서비스. 본인의 소비 패턴을 시각화하여 보여줍니다.</li><li><strong>할인 알림</strong>: 방문한 가맹점에서 사용 가능한 할인이 있으면 자동 알림</li></ol>"),
        ],
        "faq": [
            ("현대카드 제로 에디션2 할인형과 포인트형 중 어떤 것이 좋나요?", "소액 결제가 많으면 <strong>할인형</strong>(즉시 할인 체감), 대금 결제 위주면 <strong>포인트형</strong>(적립 후 활용)이 유리합니다. 확실하지 않다면 할인형이 체감이 좋아 더 인기가 많습니다."),
            ("현대카드도 코스트코에서 결제 가능한가요?", "<strong>네, 가능합니다.</strong> 코스트코에서 결제 가능한 카드는 삼성카드와 현대카드뿐입니다. 코스트코 이용이 잦다면 현대카드를 고려하세요."),
            ("M포인트의 유효기간은 얼마인가요?", "M포인트는 적립일로부터 <strong>5년</strong>이 유효기간입니다. 유효기간 내에 사용하지 않으면 소멸됩니다. 앱에서 소멸 예정 포인트를 확인할 수 있습니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 17. 신한카드 추천
    {
        "title": "신한카드 추천 인기 순위 혜택 비교 총정리",
        "cat": CAT_FINANCE,
        "slug": "shinhan-card-recommendation",
        "intro": "<strong>신한카드</strong>는 국내 카드 발급 점유율 1위 카드사로, Mr.Life, Deep On 등 생활 밀착형 카드가 강점입니다. 네이버페이 제휴, 항공 마일리지, SKT 통신 할인 등 다양한 영역에서 강력한 혜택을 제공합니다. 신한카드의 인기 카드를 비교하여 최적의 선택을 안내합니다.",
        "sections": [
            ("신한카드 인기 TOP 7 비교표", "<table><thead><tr><th>카드명</th><th>핵심 혜택</th><th>전월 실적</th><th>연회비</th><th>추천 대상</th></tr></thead><tbody><tr><td>Mr.Life</td><td>생활 전 영역 5% 할인</td><td>30만원</td><td>1만원</td><td>3040 직장인</td></tr><tr><td>Deep On</td><td>온라인 3% 적립</td><td>없음</td><td>없음</td><td>온라인 쇼핑</td></tr><tr><td>네이버페이 신한카드</td><td>네이버페이 최대 3%</td><td>없음</td><td>없음</td><td>네이버 헤비유저</td></tr><tr><td>대한항공 신한카드</td><td>마일리지 1,000원=1마일</td><td>30만원</td><td>1.5만원</td><td>항공 마일리지</td></tr><tr><td>SKT T 신한카드</td><td>통신비 월 최대 1.2만원</td><td>40만원</td><td>1만원</td><td>SKT 사용자</td></tr><tr><td>S-OIL 신한카드</td><td>주유 리터당 60원 할인</td><td>30만원</td><td>1만원</td><td>S-OIL 주유</td></tr><tr><td>신한 비즈 플러스</td><td>사업 경비 할인</td><td>50만원</td><td>1만원</td><td>자영업자</td></tr></tbody></table>"),
            ("신한카드 Mr.Life 심층 분석", "<p><strong>Mr.Life</strong>는 신한카드의 대표 생활 할인 카드입니다.</p><ul><li>쇼핑, 외식, 카페, 편의점, 대중교통 등 <strong>12개 생활 영역</strong>에서 5% 할인</li><li>월 최대 할인 금액: <strong>1만원</strong> (전월 실적 구간에 따라 상이)</li><li>전월 실적 30만원 이상 시 혜택 적용</li><li>직장인이 가장 많이 보유한 카드 중 하나</li></ul><p>월 50만원 이상 결제하면 월 할인 한도 1만원을 꽉 채울 수 있어 <strong>연간 12만원 절약</strong>이 가능합니다.</p>"),
            ("신한 SOL페이 연동 혜택", "<ul><li><strong>SOL페이</strong>: 신한카드 전용 간편결제. 등록 카드로 결제 시 추가 적립 이벤트가 수시로 진행됩니다.</li><li><strong>마이신한포인트</strong>: 신한카드 사용 시 적립되는 포인트. 카드 대금 차감, 쇼핑, 기프티콘 구매 등에 사용 가능합니다.</li><li><strong>자동 할인 LINK</strong>: 앱에서 할인 쿠폰을 LINK하면 해당 가맹점 결제 시 자동 할인 적용됩니다.</li></ul>"),
            ("신한카드 선택 가이드", "<ul><li><strong>생활비 절약 우선</strong> → Mr.Life</li><li><strong>온라인 쇼핑 위주</strong> → Deep On 또는 네이버페이 카드</li><li><strong>항공 마일리지</strong> → 대한항공 신한카드</li><li><strong>SKT 통신비 절약</strong> → SKT T 신한카드</li><li><strong>주유비 절약</strong> → S-OIL 신한카드</li></ul>"),
        ],
        "faq": [
            ("신한카드 Mr.Life와 Deep On 중 어떤 것이 좋나요?", "오프라인 소비가 많으면 <strong>Mr.Life</strong>(12개 영역 5% 할인), 온라인 소비가 많으면 <strong>Deep On</strong>(온라인 3% 적립)이 유리합니다. 두 카드를 함께 사용하면 온·오프라인 모두 커버됩니다."),
            ("신한카드 포인트는 어디에 쓰는 것이 가장 좋나요?", "가장 가치가 높은 것은 <strong>카드 대금 차감</strong>(1포인트 = 1원)입니다. 기프티콘이나 제휴사 전환은 교환 비율이 불리할 수 있으니 대금 차감을 추천합니다."),
            ("신한카드 앱에서 할인 쿠폰은 어떻게 받나요?", "신한 SOL페이 앱 → <strong>'혜택' 탭</strong>에서 다양한 LINK 할인 쿠폰을 확인할 수 있습니다. 결제 전 꼭 LINK를 누르세요. LINK하지 않으면 할인이 적용되지 않습니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 18. KB국민카드 추천
    {
        "title": "KB국민카드 추천 인기 순위 혜택 비교 총정리",
        "cat": CAT_FINANCE,
        "slug": "kb-card-recommendation",
        "intro": "<strong>KB국민카드</strong>는 KB금융그룹의 카드사로, 탄탄대로·노리2 등 실속형 카드와 KB Pay 간편결제가 강점입니다. 국민은행 연동 혜택, 적금 연계, 마일리지 등 금융 그룹 시너지가 풍부합니다. KB국민카드의 인기 카드를 비교하여 최적의 선택을 안내합니다.",
        "sections": [
            ("KB국민카드 인기 TOP 7 비교표", "<table><thead><tr><th>카드명</th><th>핵심 혜택</th><th>전월 실적</th><th>연회비</th><th>추천 대상</th></tr></thead><tbody><tr><td>탄탄대로 티타늄</td><td>캐시백 0.7% + 교통 할인</td><td>30만원</td><td>1만원</td><td>직장인 캐시백</td></tr><tr><td>노리2 체크</td><td>편의점·카페·배달 10%</td><td>20만원</td><td>없음</td><td>2030 대학생</td></tr><tr><td>KB Pay 카드</td><td>KB Pay 결제 5% 할인</td><td>30만원</td><td>1만원</td><td>KB Pay 유저</td></tr><tr><td>스카이패스 국민카드</td><td>대한항공 1,000원=1마일</td><td>30만원</td><td>1.5만원</td><td>마일리지</td></tr><tr><td>홈플러스 국민카드</td><td>홈플러스 5% 할인</td><td>30만원</td><td>1만원</td><td>홈플러스 이용자</td></tr><tr><td>오하쳌 카드</td><td>배달·OTT·카페 10%</td><td>30만원</td><td>1만원</td><td>MZ세대 생활</td></tr><tr><td>비즈 올림 카드</td><td>세금·주유 할인</td><td>50만원</td><td>1만원</td><td>자영업자</td></tr></tbody></table>"),
            ("KB Pay 간편결제 혜택", "<p><strong>KB Pay</strong>는 KB국민카드의 간편결제 서비스입니다.</p><ul><li>KB Pay로 결제 시 <strong>추가 할인</strong>이 적용되는 카드가 많습니다.</li><li>오프라인 매장에서 QR코드 결제로 편리하게 사용 가능합니다.</li><li>KB Pay 전용 이벤트: 매월 특정 가맹점 추가 할인 이벤트가 진행됩니다.</li><li>KB국민은행 계좌 연동: 계좌 잔액 확인, 이체 등 뱅킹 기능도 통합되어 있습니다.</li></ul>"),
            ("국민은행 연동 시너지", "<ul><li><strong>급여통장 연동</strong>: KB국민은행 급여통장에 KB카드 자동납부를 설정하면 추가 할인이나 포인트가 적립됩니다.</li><li><strong>적금 연계</strong>: 카드 사용 실적에 따라 적금 우대금리를 받을 수 있습니다.</li><li><strong>대출 우대</strong>: KB카드 우수 고객은 KB국민은행 대출 금리 우대를 받을 수 있습니다.</li></ul>"),
            ("KB국민카드 선택 가이드", "<ul><li><strong>캐시백 + 교통</strong> → 탄탄대로 티타늄</li><li><strong>편의점·카페 할인</strong> → 노리2 체크</li><li><strong>KB Pay 자주 사용</strong> → KB Pay 카드</li><li><strong>항공 마일리지</strong> → 스카이패스 국민카드</li><li><strong>MZ세대 라이프스타일</strong> → 오하쳌 카드</li></ul>"),
        ],
        "faq": [
            ("KB국민카드와 국민은행은 같은 곳인가요?", "KB국민카드는 <strong>KB금융그룹 계열의 카드사</strong>이고, 국민은행은 같은 그룹의 은행입니다. 같은 그룹이므로 앱 연동, 포인트 통합 등 시너지가 좋습니다."),
            ("탄탄대로 카드와 오하쳌 카드 중 어떤 것이 좋나요?", "30~40대 직장인이라면 <strong>탄탄대로</strong>(캐시백 + 교통), 20~30대 MZ세대라면 <strong>오하쳌</strong>(배달·OTT·카페)이 소비 패턴에 맞습니다."),
            ("KB 포인트리는 어디에 쓸 수 있나요?", "KB 포인트리는 <strong>카드 대금 차감, KB국민은행 적금 이체, 제휴사 포인트 전환, 기프티콘 구매</strong> 등에 사용 가능합니다. 1포인트 = 1원으로 카드 대금 차감이 가장 효율적입니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 19. 롯데카드 추천
    {
        "title": "롯데카드 추천 인기 순위 혜택 비교 총정리",
        "cat": CAT_FINANCE,
        "slug": "lotte-card-recommendation",
        "intro": "<strong>롯데카드</strong>는 롯데백화점, 롯데마트, 롯데면세점 등 롯데 계열사 혜택이 강점인 카드사입니다. LOCA 시리즈의 생활 할인 카드, 롯데 멤버스 포인트 적립 등 독자적 혜택이 풍부합니다. 롯데카드의 인기 카드를 비교하여 최적의 선택을 안내합니다.",
        "sections": [
            ("롯데카드 인기 TOP 5 비교표", "<table><thead><tr><th>카드명</th><th>핵심 혜택</th><th>전월 실적</th><th>연회비</th><th>추천 대상</th></tr></thead><tbody><tr><td>LOCA LIKIT</td><td>생활 5~7% 할인</td><td>30만원</td><td>1만원</td><td>생활비 절약</td></tr><tr><td>LOCA 365</td><td>전 가맹점 0.5% 캐시백</td><td>없음</td><td>없음</td><td>실적 부담 없는 분</td></tr><tr><td>롯데 오토모빌</td><td>전 주유소 L당 80원 할인</td><td>40만원</td><td>1.5만원</td><td>차량 보유자</td></tr><tr><td>롯데백화점 카드</td><td>백화점 5% 적립</td><td>30만원</td><td>1만원</td><td>백화점 쇼핑</td></tr><tr><td>롯데면세점 카드</td><td>면세점 추가 할인</td><td>30만원</td><td>1만원</td><td>해외여행·면세</td></tr></tbody></table>"),
            ("롯데 계열사 연동 혜택", "<ul><li><strong>롯데백화점</strong>: L.Point 적립 + 카드 추가 할인으로 실질 할인율 7~10%</li><li><strong>롯데마트</strong>: 롯데마트 전용 카드 사용 시 5~10% 할인</li><li><strong>롯데면세점</strong>: 해외여행 전 면세품 구매 시 추가 할인 + L.Point 적립</li><li><strong>롯데시네마</strong>: L.Point로 영화 예매 가능, 특정 카드는 영화 할인</li><li><strong>세븐일레븐</strong>: 롯데카드 결제 시 편의점 할인 이벤트</li></ul>"),
            ("L.Point 활용 가이드", "<p>롯데카드의 핵심 포인트인 <strong>L.Point</strong>는 롯데 계열 전체에서 사용 가능합니다.</p><ul><li>롯데백화점, 롯데마트, 롯데면세점, 롯데시네마, 세븐일레븐 등</li><li>1포인트 = 1원으로 현금처럼 사용</li><li>롯데 계열을 자주 이용하면 포인트가 빠르게 쌓여 체감 혜택이 큽니다</li></ul>"),
            ("롯데카드 선택 가이드", "<ul><li><strong>생활비 절약</strong> → LOCA LIKIT</li><li><strong>부담 없는 캐시백</strong> → LOCA 365</li><li><strong>주유비 절약</strong> → 오토모빌 카드</li><li><strong>롯데백화점 쇼핑</strong> → 롯데백화점 카드</li><li><strong>해외여행·면세점</strong> → 롯데면세점 카드</li></ul>"),
        ],
        "faq": [
            ("롯데카드는 롯데 계열에서만 혜택이 좋은가요?", "아닙니다. <strong>LOCA 시리즈</strong>는 전 가맹점에서 할인·캐시백을 제공합니다. 롯데 계열 혜택은 추가 보너스입니다."),
            ("L.Point는 다른 포인트로 전환할 수 있나요?", "L.Point는 <strong>항공 마일리지(대한항공, 아시아나)</strong>로 전환 가능합니다. 전환 비율은 시기에 따라 다르니 L.Point 앱에서 확인하세요."),
            ("롯데카드 앱에서 할인 쿠폰을 받을 수 있나요?", "네, 롯데카드 앱의 <strong>'혜택' 탭</strong>에서 다양한 할인 쿠폰을 다운받을 수 있습니다. 롯데마트, 롯데백화점 전용 쿠폰도 수시로 제공됩니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 20. 우리카드 추천
    {
        "title": "우리카드 추천 인기 순위 혜택 비교 총정리",
        "cat": CAT_FINANCE,
        "slug": "woori-card-recommendation",
        "intro": "<strong>우리카드</strong>는 우리금융그룹의 카드사로, 카드의정석 시리즈의 합리적인 혜택과 낮은 연회비가 강점입니다. 우리은행 연동 혜택, 생활비 절약 카드 등 실속 있는 카드가 많습니다. 우리카드의 인기 카드를 비교하여 최적의 선택을 안내합니다.",
        "sections": [
            ("우리카드 인기 TOP 5 비교표", "<table><thead><tr><th>카드명</th><th>핵심 혜택</th><th>전월 실적</th><th>연회비</th><th>추천 대상</th></tr></thead><tbody><tr><td>카드의정석 COOKIE CHECK</td><td>전 가맹점 0.5% 캐시백</td><td>없음</td><td>없음</td><td>실적 부담 없는 분</td></tr><tr><td>카드의정석 위비온플러스</td><td>온라인 쇼핑 5% 할인</td><td>30만원</td><td>1만원</td><td>온라인 쇼핑</td></tr><tr><td>카드의정석 다이노스</td><td>생활 전 영역 5% 할인</td><td>30만원</td><td>1만원</td><td>3040 직장인</td></tr><tr><td>카드의정석 교통</td><td>대중교통 10% 할인</td><td>20만원</td><td>5천원</td><td>대중교통 출퇴근</td></tr><tr><td>우리 비즈 카드</td><td>국세 할인 + 주유 할인</td><td>30만원</td><td>5천원</td><td>자영업자</td></tr></tbody></table>"),
            ("우리카드의 강점: 낮은 연회비와 실속 혜택", "<p>우리카드는 다른 카드사 대비 <strong>연회비가 낮고 실적 조건이 유연</strong>합니다.</p><ul><li>카드의정석 COOKIE CHECK: 연회비 없음 + 전월 실적 없음 + 0.5% 캐시백</li><li>교통카드: 연회비 5천원 + 전월 실적 20만원 → 진입 장벽이 낮음</li><li>다이노스: 연회비 1만원에 생활 전 영역 5% 할인 → 신한 Mr.Life와 대등한 혜택</li></ul><p>카드 혜택을 처음 접하는 분이나 연회비 부담이 있는 분에게 우리카드는 좋은 출발점입니다.</p>"),
            ("우리은행 연동 혜택", "<ul><li><strong>급여통장 연동</strong>: 우리은행 급여통장에 우리카드 자동납부 등록 시 추가 혜택</li><li><strong>적금 우대금리</strong>: 우리카드 사용 실적에 따라 우리은행 적금 우대금리 제공</li><li><strong>대출 금리 우대</strong>: 우리카드 우수 고객은 우리은행 신용대출·주담대 금리 우대</li><li><strong>우리WON뱅킹 연동</strong>: 우리카드 앱과 우리WON뱅킹이 통합되어 카드·은행을 한 앱에서 관리</li></ul>"),
            ("우리카드 선택 가이드", "<ul><li><strong>부담 없이 시작</strong> → 카드의정석 COOKIE CHECK</li><li><strong>온라인 쇼핑</strong> → 위비온플러스</li><li><strong>생활비 절약</strong> → 다이노스</li><li><strong>교통비 절약</strong> → 카드의정석 교통</li><li><strong>사업용</strong> → 우리 비즈 카드</li></ul>"),
        ],
        "faq": [
            ("우리카드는 다른 카드사보다 혜택이 적지 않나요?", "우리카드는 화려한 프리미엄 혜택보다 <strong>실속 있는 할인과 낮은 진입 장벽</strong>이 강점입니다. COOKIE CHECK처럼 조건 없이 캐시백을 주는 카드는 다른 카드사에서 찾기 어렵습니다."),
            ("우리은행 고객이 아니어도 우리카드를 쓸 수 있나요?", "<strong>네, 가능합니다.</strong> 결제 계좌를 다른 은행으로 설정할 수 있습니다. 다만 우리은행 연동 혜택은 받지 못합니다."),
            ("카드의정석 시리즈 중 가장 인기 있는 카드는?", "<strong>COOKIE CHECK</strong>가 가장 인기입니다. 연회비·전월 실적 없이 0.5% 캐시백을 제공하여, 서브 카드나 첫 카드로 부담 없이 사용할 수 있습니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 21. 연회비 무료 신용카드
    {
        "title": "연회비 무료 신용카드 추천 비교 혜택 총정리",
        "cat": CAT_FINANCE,
        "slug": "no-annual-fee-credit-card",
        "intro": "연회비 부담 없이 카드 혜택을 누리고 싶다면 <strong>연회비 무료 신용카드</strong>가 정답입니다. 최근에는 연회비 없이도 캐시백, 할인, 포인트 적립 등 실속 있는 혜택을 제공하는 카드가 늘고 있습니다. 연회비 무료 카드 중 혜택이 가장 좋은 카드를 비교하여 추천합니다.",
        "sections": [
            ("연회비 무료 카드 TOP 7 비교표", "<table><thead><tr><th>카드명</th><th>핵심 혜택</th><th>전월 실적</th><th>카드사</th></tr></thead><tbody><tr><td>현대 제로 에디션2</td><td>건별 할인/포인트</td><td>없음</td><td>현대</td></tr><tr><td>신한 Deep On</td><td>온라인 3% 적립</td><td>없음</td><td>신한</td></tr><tr><td>카카오뱅크 신용카드</td><td>간편결제 캐시백</td><td>없음</td><td>카카오뱅크</td></tr><tr><td>토스뱅크 신용카드</td><td>전 가맹점 캐시백</td><td>없음</td><td>토스뱅크</td></tr><tr><td>우리 COOKIE CHECK</td><td>전 가맹점 0.5% 캐시백</td><td>없음</td><td>우리</td></tr><tr><td>현대 배민 카드</td><td>배달의민족 5% 할인</td><td>30만원</td><td>현대</td></tr><tr><td>롯데 LOCA 365</td><td>전 가맹점 0.5% 캐시백</td><td>없음</td><td>롯데</td></tr></tbody></table>"),
            ("연회비 무료 카드가 수익을 내는 구조", "<p>연회비가 무료인데 어떻게 혜택을 줄 수 있을까요?</p><ul><li><strong>가맹점 수수료</strong>: 카드사는 결제 시 가맹점으로부터 1~2% 수수료를 받습니다. 이 수수료의 일부를 회원에게 돌려주는 것이 캐시백·할인입니다.</li><li><strong>리볼빙·할부 이자</strong>: 할부·리볼빙 사용자의 이자 수익이 카드사의 주요 수입원입니다.</li><li><strong>제휴 수수료</strong>: 제휴 가맹점에서 추가 수수료를 받고, 회원에게는 할인을 제공합니다.</li></ul><p>따라서 연회비 무료 카드를 일시불로만 사용하면 회원이 일방적으로 유리한 구조입니다.</p>"),
            ("연회비 무료 vs 유료 카드 실질 비교", "<table><thead><tr><th>항목</th><th>연회비 무료</th><th>연회비 1만원</th></tr></thead><tbody><tr><td>캐시백률</td><td>0.3~0.5%</td><td>0.7~1.0%</td></tr><tr><td>월 50만원 결제 시 연간 혜택</td><td>1.8~3만원</td><td>4.2~6만원</td></tr><tr><td>연회비 차감 후 순혜택</td><td>1.8~3만원</td><td>3.2~5만원</td></tr><tr><td>전월 실적 조건</td><td>없는 경우 많음</td><td>30만원 이상</td></tr></tbody></table><p>월 결제액이 30만원 이하라면 연회비 무료 카드가, 30만원 이상이면 유료 카드가 순혜택이 더 큽니다.</p>"),
            ("연회비 무료 카드 활용 전략", "<ol><li><strong>서브 카드로 활용</strong>: 메인 카드의 월 할인 한도를 채운 후, 나머지 결제에 연회비 무료 카드를 사용하세요.</li><li><strong>실적 없는 카드 선택</strong>: 전월 실적 조건이 없는 카드를 선택하면 사용 금액에 관계없이 혜택을 받을 수 있습니다.</li><li><strong>인터넷 뱅킹 카드 활용</strong>: 카카오뱅크, 토스뱅크 등 인터넷 뱅킹 카드는 연회비 무료 + 실적 없음 + 간편 발급이 장점입니다.</li></ol>"),
        ],
        "faq": [
            ("연회비 무료 카드는 혜택이 없는 것 아닌가요?", "과거에는 그랬지만, 최근에는 <strong>연회비 무료로도 0.3~0.5% 캐시백, 특정 가맹점 5% 할인</strong> 등 실속 있는 카드가 많습니다. 특히 인터넷 전문은행 카드의 혜택이 좋습니다."),
            ("연회비 무료 카드를 여러 장 만들어도 되나요?", "가능합니다. 연회비 부담이 없으므로 <strong>용도별로 2~3장</strong> 만들어 활용하는 것도 전략입니다. 단, 카드 개수가 너무 많으면 관리가 어려우니 3장 이내를 권합니다."),
            ("연회비 무료 카드도 신용점수에 영향을 주나요?", "<strong>네, 동일하게 영향을 줍니다.</strong> 연회비 유무와 관계없이 카드 사용·결제 이력은 신용점수에 반영됩니다. 성실하게 사용하면 점수가 올라갑니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 22. 프리미엄 신용카드 비교
    {
        "title": "프리미엄 신용카드 비교 연회비 혜택 공항라운지 총정리",
        "cat": CAT_FINANCE,
        "slug": "premium-credit-card-comparison",
        "intro": "연회비 3만원 이상의 <strong>프리미엄 신용카드</strong>는 공항라운지 무료 이용, 발레파킹, 골프 예약, 해외 호텔 업그레이드 등 일반 카드에는 없는 고급 혜택을 제공합니다. 프리미엄 카드의 혜택과 연회비 대비 가성비를 비교하여 나에게 맞는 카드를 찾아보겠습니다.",
        "sections": [
            ("프리미엄 카드 TOP 5 비교표", "<table><thead><tr><th>카드명</th><th>연회비</th><th>공항라운지</th><th>핵심 혜택</th><th>전월 실적</th></tr></thead><tbody><tr><td>현대카드 X</td><td>3만원</td><td>연 2회</td><td>여행·다이닝·골프</td><td>80만원</td></tr><tr><td>삼성 iD PLATINUM</td><td>5만원</td><td>연 4회</td><td>공항라운지·호텔</td><td>100만원</td></tr><tr><td>신한 프리미어</td><td>3만원</td><td>연 2회</td><td>항공·호텔·발레파킹</td><td>80만원</td></tr><tr><td>KB 플래티넘</td><td>3만원</td><td>연 2회</td><td>공항·골프·여행</td><td>80만원</td></tr><tr><td>아멕스 골드</td><td>15만원</td><td>무제한</td><td>글로벌 라운지·여행</td><td>없음</td></tr></tbody></table>"),
            ("프리미엄 카드 연회비 본전 뽑기", "<p>프리미엄 카드의 연회비가 아깝지 않으려면 다음 혜택을 꼭 활용하세요.</p><ul><li><strong>공항라운지</strong>: 1회 이용 시 약 3~5만원 가치. 연 2회만 이용해도 연회비 본전입니다.</li><li><strong>발레파킹</strong>: 백화점·호텔 발레파킹 1회 약 1~2만원 가치.</li><li><strong>여행 보험</strong>: 프리미엄 카드에 포함된 해외여행 보험은 별도 가입 시 5~10만원 수준입니다.</li><li><strong>호텔 업그레이드</strong>: 제휴 호텔 객실 업그레이드 시 1박당 5~20만원 가치.</li></ul>"),
            ("프리미엄 카드가 필요한 사람", "<ul><li>연 2회 이상 해외여행하는 분</li><li>공항 이용이 잦은 출장족</li><li>골프·다이닝 등 프리미엄 라이프스타일을 즐기는 분</li><li>월 결제액 100만원 이상으로 마일리지 적립 효과가 큰 분</li></ul><p>반대로, 해외여행이 거의 없고 월 결제액이 50만원 이하라면 연회비 1만원 이하 카드가 더 효율적입니다.</p>"),
            ("블랙카드·VVIP 카드 간략 비교", "<p>연회비 30~100만원 이상의 초프리미엄 카드는 초청제로 운영됩니다.</p><ul><li><strong>현대카드 the Black</strong>: 연회비 100만원, 무제한 라운지, 전담 컨시어지</li><li><strong>삼성 RAUME</strong>: 연회비 30만원, 프리미엄 라운지, 호텔 VIP</li><li><strong>롯데 L7</strong>: 연회비 30만원, 롯데 계열 최고 혜택</li></ul><p>이 카드들은 카드사의 초청을 받아야 발급 가능하며, 연간 수천만원 이상 결제하는 고객이 대상입니다.</p>"),
        ],
        "faq": [
            ("프리미엄 카드는 아무나 발급받을 수 있나요?", "일반 프리미엄 카드(연회비 3~15만원)는 <strong>소득 조건만 충족하면 누구나 신청</strong> 가능합니다. 블랙카드 등 초프리미엄 카드는 초청제입니다."),
            ("공항라운지는 동반자도 이용 가능한가요?", "카드에 따라 다릅니다. 일부 카드는 <strong>동반 1인 무료</strong>이고, 일부는 본인만 무료입니다. 가족 여행이 잦다면 동반자 혜택이 있는 카드를 선택하세요."),
            ("연회비 3만원 카드와 15만원 카드의 차이는?", "3만원 카드는 연 2~4회 라운지 + 기본 프리미엄 서비스, 15만원 카드는 <strong>무제한 라운지 + 글로벌 제휴 + 전담 컨시어지</strong>가 추가됩니다. 해외 출장 빈도에 따라 선택하세요."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 23. 체크카드 추천
    {
        "title": "체크카드 추천 혜택 비교 순위 총정리",
        "cat": CAT_FINANCE,
        "slug": "check-card-recommendation",
        "intro": "<strong>체크카드</strong>는 통장 잔액 내에서만 결제되어 과소비를 방지하면서도, 캐시백·할인 혜택과 연말정산 30% 소득공제를 받을 수 있는 현명한 결제 수단입니다. 신용카드보다 발급이 쉽고 연회비 부담도 없어 누구에게나 추천합니다. 체크카드 인기 순위와 혜택을 비교합니다.",
        "sections": [
            ("체크카드 인기 TOP 7 비교표", "<table><thead><tr><th>카드명</th><th>핵심 혜택</th><th>실적 조건</th><th>카드사</th></tr></thead><tbody><tr><td>카카오뱅크 체크카드</td><td>카페·편의점 5% 할인</td><td>없음</td><td>카카오뱅크</td></tr><tr><td>토스뱅크 체크카드</td><td>전 가맹점 0.4% 캐시백</td><td>없음</td><td>토스뱅크</td></tr><tr><td>KB국민 노리2 체크</td><td>편의점·카페·배달 10%</td><td>20만원</td><td>KB국민</td></tr><tr><td>신한 체크 SOL</td><td>편의점 5%, 교통 5%</td><td>없음</td><td>신한</td></tr><tr><td>우리 COOKIE CHECK</td><td>전 가맹점 0.5% 캐시백</td><td>없음</td><td>우리</td></tr><tr><td>하나 1Q 체크카드</td><td>교통 10%, 카페 5%</td><td>20만원</td><td>하나</td></tr><tr><td>NH 올원 체크</td><td>전 가맹점 0.3% 캐시백</td><td>없음</td><td>NH농협</td></tr></tbody></table>"),
            ("체크카드 vs 신용카드 완벽 비교", "<table><thead><tr><th>항목</th><th>체크카드</th><th>신용카드</th></tr></thead><tbody><tr><td>결제 방식</td><td>즉시 출금</td><td>후불 결제</td></tr><tr><td>과소비 위험</td><td>낮음</td><td>높음</td></tr><tr><td>혜택 수준</td><td>보통</td><td>높음</td></tr><tr><td>연말정산 공제율</td><td>30%</td><td>15%</td></tr><tr><td>신용 이력</td><td>안 쌓임</td><td>쌓임</td></tr><tr><td>해외 결제</td><td>가능 (환율 적용)</td><td>가능</td></tr></tbody></table>"),
            ("체크카드 연말정산 공제 극대화", "<p>체크카드는 소득공제율이 <strong>30%</strong>로 신용카드(15%)의 2배입니다.</p><ul><li>연봉의 25%까지는 신용카드로 결제 (혜택이 더 좋으므로)</li><li>25% 초과분부터 체크카드로 전환 (공제율 30% 적용)</li><li>대중교통은 체크카드로 결제 시 공제율 80% 적용</li></ul><p>이 전략으로 카드 혜택 + 소득공제를 모두 극대화할 수 있습니다.</p>"),
            ("체크카드 선택 가이드", "<ul><li><strong>편의점·카페 자주 이용</strong> → 카카오뱅크 또는 KB 노리2</li><li><strong>조건 없이 캐시백</strong> → 토스뱅크 또는 우리 COOKIE CHECK</li><li><strong>교통비 할인</strong> → 하나 1Q 체크 또는 신한 SOL 체크</li><li><strong>첫 카드 발급</strong> → 인터넷 은행 체크카드 (발급 쉬움)</li></ul>"),
        ],
        "faq": [
            ("체크카드도 해외에서 사용 가능한가요?", "<strong>네, 가능합니다.</strong> VISA, Mastercard 브랜드가 붙은 체크카드는 해외 가맹점에서 결제 가능합니다. 단, 해외 결제 수수료(1~2%)가 발생합니다."),
            ("체크카드로 자동납부를 설정할 수 있나요?", "네, 통신비, 공과금, 구독료 등 <strong>자동납부 설정이 가능</strong>합니다. 단, 결제일에 통장 잔액이 부족하면 결제가 실패하므로 잔액을 확인하세요."),
            ("인터넷 은행 체크카드와 시중은행 체크카드의 차이는?", "인터넷 은행(카카오뱅크, 토스뱅크)은 <strong>앱에서 간편 발급 + 전월 실적 없음</strong>이 장점입니다. 시중은행은 창구 방문이 필요하지만 은행 연동 혜택(적금 우대 등)이 있습니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 24. PLCC 카드 추천
    {
        "title": "PLCC 카드 추천 총정리 브랜드 제휴카드 비교",
        "cat": CAT_FINANCE,
        "slug": "plcc-card-recommendation",
        "intro": "<strong>PLCC(Private Label Credit Card)</strong>란 특정 브랜드와 카드사가 공동으로 만든 제휴 카드입니다. 배민 현대카드, 쿠팡 현대카드, 스타벅스 현대카드 등이 대표적입니다. 해당 브랜드에서 높은 할인·적립을 받을 수 있어, 특정 브랜드를 자주 이용하는 분에게 최적의 카드입니다.",
        "sections": [
            ("인기 PLCC 카드 비교표", "<table><thead><tr><th>카드명</th><th>제휴 브랜드</th><th>핵심 혜택</th><th>연회비</th><th>전월 실적</th></tr></thead><tbody><tr><td>배민 현대카드</td><td>배달의민족</td><td>배민 5% 할인</td><td>없음</td><td>30만원</td></tr><tr><td>쿠팡 현대카드</td><td>쿠팡</td><td>로켓배송 2~4%</td><td>없음</td><td>30만원</td></tr><tr><td>스타벅스 현대카드</td><td>스타벅스</td><td>스타벅스 10% 적립</td><td>없음</td><td>30만원</td></tr><tr><td>네이버페이 신한카드</td><td>네이버</td><td>네이버페이 3% 적립</td><td>없음</td><td>없음</td></tr><tr><td>카카오페이 신한카드</td><td>카카오</td><td>카카오페이 3% 적립</td><td>없음</td><td>없음</td></tr><tr><td>SSG.COM 삼성카드</td><td>SSG</td><td>SSG 5% 할인</td><td>없음</td><td>30만원</td></tr></tbody></table>"),
            ("PLCC 카드의 장단점", "<p><strong>장점:</strong></p><ul><li>해당 브랜드에서 일반 카드보다 2~3배 높은 혜택</li><li>대부분 연회비 무료</li><li>브랜드 전용 쿠폰·이벤트 추가 제공</li></ul><p><strong>단점:</strong></p><ul><li>해당 브랜드 외에서는 혜택이 약함</li><li>전월 실적 조건이 있는 경우 소비를 강제함</li><li>브랜드 이용을 중단하면 카드 가치가 급락</li></ul>"),
            ("PLCC 카드 현명하게 활용하는 법", "<ol><li><strong>자주 쓰는 브랜드 1~2개만 선택</strong>: PLCC 카드를 너무 많이 만들면 전월 실적이 분산됩니다.</li><li><strong>일반 카드와 병행</strong>: PLCC 카드는 해당 브랜드 전용으로, 나머지 결제는 일반 할인/캐시백 카드로 분리하세요.</li><li><strong>연회비 무료 + 실적 없는 PLCC 우선</strong>: 네이버페이, 카카오페이 카드는 조건 없이 혜택을 주므로 부담이 없습니다.</li></ol>"),
            ("PLCC vs 일반 제휴카드 차이", "<table><thead><tr><th>항목</th><th>PLCC</th><th>일반 제휴카드</th></tr></thead><tbody><tr><td>카드 디자인</td><td>브랜드 고유 디자인</td><td>카드사 디자인</td></tr><tr><td>혜택 수준</td><td>브랜드 특화 높은 혜택</td><td>보통 수준</td></tr><tr><td>앱 연동</td><td>브랜드 앱과 깊은 연동</td><td>카드사 앱 중심</td></tr><tr><td>브랜드 이벤트</td><td>전용 이벤트 많음</td><td>일반 이벤트</td></tr></tbody></table>"),
        ],
        "faq": [
            ("PLCC 카드는 해당 브랜드에서만 쓸 수 있나요?", "아닙니다. <strong>모든 가맹점에서 결제 가능</strong>합니다. 단, 특별 할인은 해당 브랜드에서만 적용됩니다."),
            ("PLCC 카드를 여러 장 만들 수 있나요?", "네, 가능합니다. 하지만 전월 실적이 분산되므로 <strong>자주 쓰는 브랜드 2장 이내</strong>로 제한하는 것이 효율적입니다."),
            ("PLCC 카드도 소득공제 대상인가요?", "<strong>네, 일반 신용카드와 동일하게</strong> 소득공제 대상입니다. 소득공제율 15%가 적용됩니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 25. 후불교통 체크카드
    {
        "title": "후불교통 체크카드 추천 비교 발급 방법 총정리",
        "cat": CAT_FINANCE,
        "slug": "postpaid-transportation-check-card",
        "intro": "<strong>후불교통 체크카드</strong>는 교통카드 기능이 내장된 체크카드로, 별도 충전 없이 버스·지하철을 이용할 수 있습니다. 교통비가 통장에서 자동 출금되어 편리하고, 교통 할인 혜택까지 받을 수 있습니다. 후불교통 기능이 있는 체크카드를 비교하여 추천합니다.",
        "sections": [
            ("후불교통 체크카드 TOP 5 비교", "<table><thead><tr><th>카드명</th><th>교통 할인</th><th>추가 혜택</th><th>카드사</th></tr></thead><tbody><tr><td>카카오뱅크 체크카드</td><td>교통 5%</td><td>카페·편의점 5%</td><td>카카오뱅크</td></tr><tr><td>KB국민 노리2 체크</td><td>교통 10%</td><td>편의점·배달 10%</td><td>KB국민</td></tr><tr><td>신한 SOL 체크</td><td>교통 5%</td><td>편의점 5%</td><td>신한</td></tr><tr><td>하나 1Q 체크</td><td>교통 10%</td><td>카페 5%</td><td>하나</td></tr><tr><td>우리 카드의정석 교통체크</td><td>교통 10%</td><td>통신비 5%</td><td>우리</td></tr></tbody></table>"),
            ("후불교통 vs 선불교통 비교", "<table><thead><tr><th>항목</th><th>후불교통</th><th>선불교통</th></tr></thead><tbody><tr><td>충전</td><td>불필요 (자동 출금)</td><td>사전 충전 필요</td></tr><tr><td>잔액 걱정</td><td>없음</td><td>잔액 부족 시 탑승 불가</td></tr><tr><td>할인</td><td>카드 할인 적용</td><td>할인 없음</td></tr><tr><td>소득공제</td><td>체크카드 30% 공제</td><td>현금영수증 30% 공제</td></tr><tr><td>사용 가능 교통</td><td>버스, 지하철, 택시</td><td>버스, 지하철</td></tr></tbody></table>"),
            ("후불교통 체크카드 발급 방법", "<ol><li><strong>인터넷 은행</strong>: 카카오뱅크, 토스뱅크 앱에서 체크카드 발급 시 '후불교통' 옵션을 선택하면 됩니다.</li><li><strong>시중은행</strong>: 은행 앱 또는 영업점에서 체크카드 발급 시 후불교통 기능 추가를 요청하세요.</li><li><strong>카드사 앱</strong>: 일부 카드사는 기존 체크카드에 후불교통 기능을 사후 추가할 수 있습니다.</li></ol><p>후불교통 기능은 <strong>만 12세 이상</strong>이면 신청 가능합니다.</p>"),
            ("교통비 절약 종합 전략", "<ul><li><strong>후불교통 체크카드 + 교통 할인</strong>: 카드 교통 할인 10%를 기본으로 받으세요.</li><li><strong>환승 할인</strong>: 30분 이내 환승 시 추가 요금 없이 이동 가능합니다.</li><li><strong>정기권 비교</strong>: 기후동행카드, 알뜰교통카드 등 정기권과 후불교통 할인을 비교하여 더 저렴한 쪽을 선택하세요.</li><li><strong>소득공제 활용</strong>: 대중교통 소득공제율 80%를 활용하면 연말정산에서 추가 환급됩니다.</li></ul>"),
        ],
        "faq": [
            ("후불교통 체크카드는 잔액이 없어도 교통 이용이 가능한가요?", "카드사에 따라 다릅니다. 대부분 <strong>통장 잔액이 부족해도 일정 한도 내</strong>에서 교통 이용이 가능합니다. 단, 나중에 출금되므로 잔액을 채워두는 것이 좋습니다."),
            ("후불교통 체크카드로 택시도 탈 수 있나요?", "<strong>네, 가능합니다.</strong> 후불교통 기능은 버스, 지하철뿐만 아니라 택시에서도 사용 가능합니다."),
            ("아이(초등학생)도 후불교통 체크카드를 만들 수 있나요?", "만 12세 이상이면 가능합니다. 미성년자는 <strong>보호자 동의</strong> 하에 은행에서 체크카드를 발급받을 수 있습니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 26. 신용카드 발급 조건
    {
        "title": "신용카드 발급 조건 심사 기준 총정리 거절 시 대처법",
        "cat": CAT_FINANCE,
        "slug": "credit-card-approval-requirements",
        "intro": "신용카드를 신청했는데 <strong>발급 거절</strong>을 당한 경험이 있으신가요? 카드사마다 발급 조건과 심사 기준이 다르고, 어떤 항목을 중점적으로 보는지 알면 승인 확률을 높일 수 있습니다. 신용카드 발급 조건, 심사 기준, 거절 사유, 승인율을 높이는 방법을 총정리합니다.",
        "sections": [
            ("신용카드 발급 기본 조건", "<ul><li><strong>나이</strong>: 만 19세 이상 (일부 카드사 만 18세 가능)</li><li><strong>소득</strong>: 연소득 1,200만원 이상 (카드사마다 다름). 직장인은 재직증명서, 프리랜서는 소득금액증명원으로 증빙.</li><li><strong>신용점수</strong>: NICE 기준 600점 이상이면 대부분 발급 가능. 700점 이상이면 프리미엄 카드도 가능.</li><li><strong>기존 카드 보유 수</strong>: 이미 5장 이상 보유 시 추가 발급이 어려울 수 있습니다.</li></ul>"),
            ("카드사 심사에서 보는 핵심 항목", "<ol><li><strong>신용점수</strong>: 가장 중요한 기준. NICE, KCB 점수를 모두 확인합니다.</li><li><strong>연체 이력</strong>: 과거 연체 기록이 있으면 심사에 불리합니다. 연체 이력은 최대 5년간 기록됩니다.</li><li><strong>소득 대비 부채</strong>: 기존 대출, 카드 한도 대비 소득 비율(DSR)을 확인합니다.</li><li><strong>카드 발급 이력</strong>: 최근 3개월 내 여러 카드사에 동시 신청하면 '카드 쇼핑'으로 판단하여 거절될 수 있습니다.</li><li><strong>직업 안정성</strong>: 정규직 > 계약직 > 프리랜서 > 무직 순으로 승인율이 다릅니다.</li></ol>"),
            ("발급 거절 시 대처법", "<ul><li><strong>거절 사유 확인</strong>: 카드사 고객센터(1588-xxxx)에 전화하여 거절 사유를 물어보세요. 대부분 알려줍니다.</li><li><strong>신용점수 개선</strong>: 체크카드를 3~6개월 꾸준히 사용하면 신용 이력이 쌓여 점수가 올라갑니다.</li><li><strong>다른 카드사 신청</strong>: 카드사마다 심사 기준이 다르므로, 한 곳에서 거절되어도 다른 곳에서 승인될 수 있습니다.</li><li><strong>3개월 후 재신청</strong>: 단기간 다수 신청은 점수에 불리합니다. 3개월 이상 간격을 두고 재신청하세요.</li><li><strong>인터넷 은행 카드 시도</strong>: 카카오뱅크, 토스뱅크는 상대적으로 발급 기준이 유연합니다.</li></ul>"),
            ("카드 발급 전 체크리스트", "<ol><li>NICE 또는 KCB 신용점수 무료 조회 (올크레딧, 토스)</li><li>연체 기록 유무 확인</li><li>최근 3개월 내 카드 발급 이력 확인</li><li>소득 증빙 서류 준비 (재직증명서, 원천징수영수증)</li><li>희망 카드의 발급 조건 사전 확인</li></ol>"),
        ],
        "faq": [
            ("신용점수가 없는 '씬파일러'도 카드를 만들 수 있나요?", "신용 이력이 없는 씬파일러(thin filer)는 발급이 어려울 수 있습니다. <strong>체크카드를 3~6개월 사용</strong>하여 신용 이력을 만든 후 신용카드를 신청하면 승인율이 높아집니다."),
            ("카드 발급 조회만 해도 신용점수가 떨어지나요?", "카드 발급 시 카드사가 하는 <strong>신용조회(경성조회)</strong>는 소폭 점수가 하락할 수 있습니다. 단, 본인이 하는 신용점수 확인(연성조회)은 점수에 영향이 없습니다."),
            ("주부나 학생도 카드를 발급받을 수 있나요?", "배우자 소득이나 재산으로 증빙하면 <strong>주부도 발급 가능</strong>합니다. 학생은 아르바이트 등 소득이 있으면 가능하고, 없으면 체크카드나 가족카드를 이용하세요."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 27. 카드 한도 올리기
    {
        "title": "신용카드 한도 올리는 방법 상향 신청 조건 총정리",
        "cat": CAT_FINANCE,
        "slug": "credit-card-limit-increase",
        "intro": "신용카드 한도가 부족하면 결제가 거절되는 난감한 상황이 발생합니다. <strong>카드 한도를 올리는 방법</strong>은 여러 가지가 있으며, 올바른 방법을 사용하면 신용점수에 부정적 영향 없이 한도를 높일 수 있습니다. 한도 상향 방법, 조건, 주의사항을 총정리합니다.",
        "sections": [
            ("카드 한도가 정해지는 기준", "<ul><li><strong>연소득</strong>: 소득이 높을수록 한도가 높게 설정됩니다.</li><li><strong>신용점수</strong>: 점수가 높으면 카드사가 더 높은 한도를 부여합니다.</li><li><strong>기존 카드 사용 이력</strong>: 6개월 이상 성실하게 사용하면 한도 상향에 유리합니다.</li><li><strong>기존 대출·카드 한도 합계</strong>: 다른 카드사 한도와 대출 합계가 소득 대비 과도하면 한도가 제한됩니다.</li></ul>"),
            ("한도 올리는 5가지 방법", "<ol><li><strong>카드사 앱에서 한도 상향 신청</strong>: 가장 간편한 방법. 카드사 앱 → 카드 관리 → 한도 상향 신청. 심사 후 1~3일 내 결과 통보.</li><li><strong>소득 증빙 서류 제출</strong>: 연봉이 올랐거나 추가 소득이 생겼다면 소득 증빙(원천징수영수증, 급여명세서)을 제출하면 한도가 올라갑니다.</li><li><strong>일시적 한도 상향</strong>: 고가 물품 구매, 해외여행 등 일시적으로 한도가 필요한 경우 기간 한정 한도 상향을 요청할 수 있습니다.</li><li><strong>사용 실적 쌓기</strong>: 6개월 이상 꾸준히 사용하고 연체 없이 결제하면 카드사에서 자동으로 한도 상향을 제안합니다.</li><li><strong>고객센터 전화 요청</strong>: 앱 신청이 안 되면 고객센터에 직접 전화하여 한도 상향을 요청하세요. 상담원이 조건을 안내해 줍니다.</li></ol>"),
            ("한도 상향 시 주의사항", "<ul><li><strong>무리한 한도 상향은 금물</strong>: 소득 대비 과도한 한도는 신용점수에 부정적 영향을 줄 수 있습니다.</li><li><strong>한도 = 내 돈이 아님</strong>: 한도가 높다고 그만큼 쓰면 안 됩니다. 한도의 30% 이내 사용이 신용 관리에 좋습니다.</li><li><strong>여러 카드사에 동시 신청 금지</strong>: 여러 곳에 동시에 한도 상향 신청하면 신용조회가 중복되어 점수가 하락할 수 있습니다.</li></ul>"),
            ("카드 한도와 신용점수의 관계", "<p>카드 한도 자체는 신용점수에 직접적 영향을 주지 않습니다. 중요한 것은 <strong>한도 대비 사용 비율(이용률)</strong>입니다.</p><ul><li>이용률 30% 이하: 신용점수에 긍정적</li><li>이용률 50% 이상: 중립~부정적</li><li>이용률 80% 이상: 부정적 (과도한 카드 사용으로 판단)</li></ul><p>따라서 한도를 올리되, <strong>실제 사용은 30% 이내</strong>로 유지하는 것이 가장 좋습니다.</p>"),
        ],
        "faq": [
            ("카드 한도 상향 신청 시 신용점수가 떨어지나요?", "한도 상향 심사 시 <strong>신용조회(경성조회)</strong>가 발생하여 소폭 하락할 수 있습니다. 하지만 한도가 올라가면 이용률이 낮아져 장기적으로는 점수에 긍정적입니다."),
            ("카드사에서 자동 한도 상향을 제안하면 받는 것이 좋나요?", "<strong>받는 것이 좋습니다.</strong> 자동 한도 상향은 추가 신용조회 없이 진행되므로 점수 하락이 없고, 이용률도 낮아져 점수에 긍정적입니다."),
            ("한도를 줄일 수도 있나요?", "네, 카드사 앱이나 고객센터에서 <strong>한도 축소</strong>를 요청할 수 있습니다. 과소비 방지를 위해 불필요하게 높은 한도를 줄이는 것도 좋은 방법입니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 28. 신용카드 해지 방법
    {
        "title": "신용카드 해지 방법 주의사항 신용점수 영향 총정리",
        "cat": CAT_FINANCE,
        "slug": "credit-card-cancellation-guide",
        "intro": "사용하지 않는 신용카드를 정리하고 싶지만, <strong>해지하면 신용점수가 떨어지지 않을까</strong> 걱정되시나요? 카드 해지가 신용점수에 미치는 영향, 올바른 해지 방법, 해지 전 확인해야 할 사항을 총정리합니다.",
        "sections": [
            ("신용카드 해지 방법 3가지", "<ol><li><strong>카드사 앱에서 해지</strong>: 가장 간편한 방법. 카드사 앱 → 카드 관리 → 해지 신청. 즉시 처리됩니다.</li><li><strong>고객센터 전화</strong>: 카드사 대표번호로 전화하여 해지 요청. 본인 확인 후 즉시 처리.</li><li><strong>영업점 방문</strong>: 신분증 지참하여 카드사 또는 발급 은행 방문. 대면 처리.</li></ol><p>해지 전 <strong>미결제 잔액, 할부금, 자동납부 등록 여부</strong>를 반드시 확인하세요. 미결제 금액이 있으면 해지가 안 되거나, 해지 후에도 청구됩니다.</p>"),
            ("카드 해지가 신용점수에 미치는 영향", "<ul><li><strong>단기적</strong>: 카드를 해지하면 총 신용한도가 줄어들어 <strong>이용률이 높아지며</strong> 점수가 소폭 하락할 수 있습니다.</li><li><strong>장기적</strong>: 오래된 카드를 해지하면 <strong>신용 이력 기간</strong>이 짧아져 점수에 부정적일 수 있습니다.</li><li><strong>사용하지 않는 카드</strong>: 6개월 이상 미사용 카드는 이미 점수에 기여하지 않으므로 해지해도 영향이 작습니다.</li></ul><p><strong>결론</strong>: 가장 오래된 카드 1장은 유지하고, 나머지 미사용 카드를 정리하는 것이 좋습니다.</p>"),
            ("해지 전 체크리스트", "<ol><li>미결제 잔액·할부금 완납 확인</li><li>자동납부(통신비, 구독료 등) 다른 카드로 이전</li><li>포인트·마일리지 잔여분 사용 또는 전환</li><li>연회비 환불 가능 여부 확인 (미사용 기간에 대한 환불)</li><li>가족카드 유무 확인 (본 카드 해지 시 가족카드도 해지됨)</li></ol>"),
            ("카드 정리 가이드: 몇 장이 적당할까", "<ul><li><strong>최적 보유 수</strong>: 메인 1장 + 서브 1장 = 총 2장</li><li><strong>최대 보유 수</strong>: 3장 이내 (실적 분산 방지)</li><li><strong>해지 우선순위</strong>: ① 1년 이상 미사용 카드 → ② 연회비 있는데 혜택 안 쓰는 카드 → ③ 중복 혜택 카드</li><li><strong>유지할 카드</strong>: 가장 오래된 카드 (신용 이력), 주거래 은행 연동 카드</li></ul>"),
        ],
        "faq": [
            ("카드를 해지하면 연회비를 환불받을 수 있나요?", "<strong>네, 가능합니다.</strong> 카드를 해지하면 미사용 기간에 해당하는 연회비를 일할 계산하여 환불받을 수 있습니다. 해지 시 고객센터에 환불을 요청하세요."),
            ("오래된 카드를 해지하면 신용점수가 크게 떨어지나요?", "가장 오래된 카드를 해지하면 <strong>소폭 하락</strong>할 수 있습니다. 신용 이력 기간이 짧아지기 때문입니다. 가능하면 가장 오래된 카드 1장은 유지하세요."),
            ("해지한 카드를 다시 사용할 수 있나요?", "해지된 카드는 <strong>재사용이 불가</strong>합니다. 같은 카드를 원한다면 새로 발급받아야 하며, 신규 심사가 진행됩니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 29. 카드 포인트 현금 전환
    {
        "title": "신용카드 포인트 현금 전환 방법 카드사별 총정리",
        "cat": CAT_FINANCE,
        "slug": "credit-card-point-cash-conversion",
        "intro": "신용카드를 쓰다 보면 자신도 모르게 <strong>수만~수십만 포인트</strong>가 쌓여 있습니다. 이 포인트를 그냥 두면 유효기간이 지나 소멸됩니다. 카드사별 포인트를 현금으로 전환하거나 활용하는 방법을 총정리합니다.",
        "sections": [
            ("카드사별 포인트 현금 전환 방법", "<table><thead><tr><th>카드사</th><th>포인트명</th><th>현금 전환</th><th>전환 방법</th></tr></thead><tbody><tr><td>삼성</td><td>삼성카드 포인트</td><td>1P = 1원</td><td>앱 → 포인트 → 캐시백 전환</td></tr><tr><td>현대</td><td>M포인트</td><td>1P = 1원</td><td>앱 → M포인트 → 카드대금 차감</td></tr><tr><td>신한</td><td>마이신한포인트</td><td>1P = 1원</td><td>앱 → 포인트 → 현금 입금</td></tr><tr><td>KB국민</td><td>포인트리</td><td>1P = 1원</td><td>앱 → 포인트리 → 계좌 입금</td></tr><tr><td>롯데</td><td>L.Point</td><td>현금 전환 불가</td><td>롯데 계열사에서 사용</td></tr><tr><td>우리</td><td>우리 포인트</td><td>1P = 1원</td><td>앱 → 포인트 → 카드대금 차감</td></tr><tr><td>하나</td><td>하나머니</td><td>1P = 1원</td><td>앱 → 하나머니 → 계좌 입금</td></tr></tbody></table>"),
            ("포인트 활용처 비교", "<p>현금 전환 외에도 다양한 활용 방법이 있습니다.</p><ul><li><strong>카드 대금 차감</strong>: 가장 효율적. 1포인트 = 1원으로 청구 금액에서 차감.</li><li><strong>온라인 쇼핑 결제</strong>: 카드사 쇼핑몰에서 포인트로 결제 가능. 교환비가 불리할 수 있음.</li><li><strong>기프티콘 구매</strong>: 카페, 편의점 기프티콘으로 교환. 1,000~5,000P 단위.</li><li><strong>항공 마일리지 전환</strong>: 포인트를 마일리지로 전환 가능. 전환 비율은 카드사마다 다름.</li><li><strong>기부</strong>: 포인트를 자선단체에 기부할 수 있습니다.</li></ul>"),
            ("숨은 포인트 찾는 방법", "<ol><li><strong>여신금융협회 카드포인트 통합조회</strong>: card.or.kr에서 모든 카드사의 숨은 포인트를 한번에 조회할 수 있습니다.</li><li><strong>카드사 앱 확인</strong>: 각 카드사 앱에 로그인하면 현재 적립 포인트와 유효기간을 확인할 수 있습니다.</li><li><strong>소멸 예정 포인트 확인</strong>: 대부분의 포인트는 5년 유효기간이며, 소멸 예정 알림을 설정하세요.</li></ol>"),
            ("포인트 극대화 팁", "<ul><li><strong>소액이라도 즉시 사용</strong>: 포인트를 모아두다 소멸되는 것보다 즉시 카드 대금 차감에 사용하는 것이 효율적입니다.</li><li><strong>이벤트 적립 활용</strong>: 카드사 앱에서 포인트 2배, 3배 적립 이벤트에 응모하세요.</li><li><strong>기프티콘 교환 시 주의</strong>: 기프티콘은 교환 비율이 불리할 수 있으니, 카드 대금 차감이 가장 유리합니다.</li></ul>"),
        ],
        "faq": [
            ("카드 포인트에 세금이 부과되나요?", "개인 소비자의 카드 포인트·캐시백은 <strong>소득세 대상이 아닙니다</strong>. 단, 사업자가 대량의 포인트를 현금화하는 경우 세무 확인이 필요할 수 있습니다."),
            ("카드를 해지하면 포인트는 어떻게 되나요?", "카드 해지 시 <strong>적립된 포인트는 소멸</strong>됩니다. 해지 전 반드시 포인트를 사용하거나 전환하세요."),
            ("여러 카드사 포인트를 하나로 합칠 수 있나요?", "카드사가 다르면 <strong>직접 합산은 불가</strong>합니다. 단, 여신금융협회 사이트에서 각 카드사 포인트를 한눈에 확인하고 개별적으로 사용할 수 있습니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },

    # 30. 신용카드 vs 체크카드 비교
    {
        "title": "신용카드 vs 체크카드 장단점 비교 어떤 것이 유리할까",
        "cat": CAT_FINANCE,
        "slug": "credit-card-vs-check-card",
        "intro": "카드를 처음 만들거나 기존 카드를 재정비할 때 가장 먼저 고민되는 것이 <strong>신용카드와 체크카드 중 어떤 것이 유리한가</strong>입니다. 두 카드는 결제 방식, 혜택, 소득공제율, 신용점수 영향 등 여러 면에서 차이가 큽니다. 완벽하게 비교하여 나에게 맞는 카드를 결정할 수 있도록 안내합니다.",
        "sections": [
            ("신용카드 vs 체크카드 완벽 비교표", "<table><thead><tr><th>항목</th><th>신용카드</th><th>체크카드</th></tr></thead><tbody><tr><td>결제 방식</td><td>후불 (다음 달 결제)</td><td>즉시 출금</td></tr><tr><td>발급 조건</td><td>소득 증빙 필요</td><td>통장만 있으면 가능</td></tr><tr><td>혜택 수준</td><td>높음 (할인, 캐시백, 마일리지)</td><td>보통 (할인, 소액 캐시백)</td></tr><tr><td>연말정산 공제율</td><td>15%</td><td>30%</td></tr><tr><td>연회비</td><td>0~15만원</td><td>없음</td></tr><tr><td>신용 이력</td><td>쌓임 (대출 시 유리)</td><td>안 쌓임</td></tr><tr><td>무이자할부</td><td>가능</td><td>불가</td></tr><tr><td>해외 결제</td><td>편리</td><td>가능 (일부 제한)</td></tr><tr><td>과소비 위험</td><td>높음</td><td>낮음 (잔액 내 결제)</td></tr></tbody></table>"),
            ("상황별 추천: 신용카드가 유리한 경우", "<ul><li><strong>월 결제액 50만원 이상</strong>: 카드 혜택(할인, 캐시백)의 절대 금액이 커집니다.</li><li><strong>해외여행·해외 직구가 잦은 경우</strong>: 해외 결제 편의성과 여행 보험 혜택.</li><li><strong>고가 물품 구매 시</strong>: 무이자할부 활용 가능.</li><li><strong>신용 이력을 쌓아야 하는 경우</strong>: 향후 주담대, 전세대출 등에 유리.</li><li><strong>마일리지·포인트를 적극 활용하는 경우</strong>.</li></ul>"),
            ("상황별 추천: 체크카드가 유리한 경우", "<ul><li><strong>과소비가 걱정되는 경우</strong>: 잔액 내에서만 결제되어 자연스러운 소비 통제.</li><li><strong>소득이 없거나 적은 경우</strong>: 학생, 무직자도 발급 가능.</li><li><strong>연말정산 공제 극대화</strong>: 소득공제율 30%로 신용카드의 2배.</li><li><strong>카드 관리를 간편하게 하고 싶은 경우</strong>: 즉시 출금으로 별도 결제일 관리 불필요.</li></ul>"),
            ("최적의 투카드 전략", "<p>신용카드와 체크카드를 함께 사용하면 두 카드의 장점을 모두 누릴 수 있습니다.</p><ol><li><strong>연봉의 25%까지</strong>: 혜택이 좋은 <strong>신용카드</strong>로 결제 (할인·캐시백 극대화)</li><li><strong>25% 초과분</strong>: <strong>체크카드</strong>로 전환 (소득공제율 30% 적용)</li><li><strong>대중교통</strong>: 체크카드로 결제 (소득공제율 80%)</li></ol><p>이 전략으로 카드 혜택 + 소득공제를 모두 극대화하여 연간 수십만 원을 절약할 수 있습니다.</p>"),
        ],
        "faq": [
            ("둘 다 쓰면 카드가 너무 많아지지 않나요?", "신용카드 1장 + 체크카드 1장 = <strong>총 2장</strong>이면 충분합니다. 이 조합이 혜택, 소득공제, 관리 편의성 모두 최적입니다."),
            ("체크카드만 쓰면 신용점수에 불이익이 있나요?", "불이익은 없지만, <strong>신용 이력이 쌓이지 않습니다</strong>. 향후 대출(주담대, 전세대출) 시 신용 이력이 있으면 유리하므로, 소액이라도 신용카드를 사용하는 것을 권합니다."),
            ("연말정산 시 어떤 카드를 더 많이 써야 하나요?", "연봉의 25%까지는 어떤 카드로 결제해도 공제 대상이 아닙니다. <strong>25% 초과분부터 체크카드</strong>(30%)가 신용카드(15%)보다 공제율이 2배이므로 체크카드를 더 쓰는 것이 유리합니다."),
        ],
        "ctas": [CTA_CARD_GORILLA, CTA_NAVER_CARD, CTA_CREDIT_SCORE],
    },
]


# ============================================================
# 메인 실행 함수
# ============================================================
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
    # 1단계: 이미지 업로드
    upload_all_images()

    # 2단계: 포스트 발행
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

        # 썸네일(featured image) 설정
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

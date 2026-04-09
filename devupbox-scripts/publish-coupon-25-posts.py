"""
2026 3차 민생회복소비쿠폰 지역별 포스트 25개 자동 생성 + 발행 + 인덱싱
"""
import json, urllib.request, urllib.error, base64, time, ssl, os, tempfile, re

ssl._create_default_https_context = ssl._create_unverified_context
AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API = "https://devupbox.com/wp-json/wp/v2/posts"
MEDIA_API = "https://devupbox.com/wp-json/wp/v2/media"
CAT_GETMONEY = 17
UPLOADED_IMAGES = {}

# 도시 정보: (slug, 한글도시명, 시/도 구분, 지원금 예상액, 소재지역, Unsplash 이미지 ID)
CITIES = [
    ("chungju", "충주시", "시", "15~25만원", "충청북도", "photo-1533105079780-92b9be482077"),
    ("cheongju", "청주시", "시", "15~25만원", "충청북도", "photo-1518611012118-696072aa579a"),
    ("samcheok", "삼척시", "시", "15~25만원", "강원도", "photo-1580655653885-65763b2597d0"),
    ("sokcho", "속초시", "시", "15~25만원", "강원도", "photo-1514481538271-cf9f99c5c831"),
    ("seosan", "서산시", "시", "15~25만원", "충청남도", "photo-1542315192-1f61a1792f33"),
    ("asan", "아산시", "시", "15~25만원", "충청남도", "photo-1555881400-74d7acaacd8b"),
    ("icheon", "이천시", "시", "15~25만원", "경기도", "photo-1516253593875-bd7ba052fbc5"),
    ("osan", "오산시", "시", "15~25만원", "경기도", "photo-1519501025264-65ba15a82390"),
    ("gunpo", "군포시", "시", "15~25만원", "경기도", "photo-1555881400-74d7acaacd8b"),
    ("yangju", "양주시", "시", "15~25만원", "경기도", "photo-1538485399081-7191377e8241"),
    ("hanam", "하남시", "시", "15~25만원", "경기도", "photo-1494526585095-c41746248156"),
    ("gwangju-gyeonggi", "광주시(경기)", "시", "15~25만원", "경기도", "photo-1518611012118-696072aa579a"),
    ("uijeongbu", "의정부시", "시", "15~25만원", "경기도", "photo-1542315192-1f61a1792f33"),
    ("gimpo", "김포시", "시", "15~25만원", "경기도", "photo-1533105079780-92b9be482077"),
    ("guri", "구리시", "시", "15~25만원", "경기도", "photo-1555881400-74d7acaacd8b"),
    ("anseong", "안성시", "시", "15~25만원", "경기도", "photo-1580655653885-65763b2597d0"),
    ("sejong", "세종시", "광역시", "20~30만원", "특별자치시", "photo-1538485399081-7191377e8241"),
    ("ulsan", "울산시", "광역시", "20~30만원", "광역시", "photo-1514481538271-cf9f99c5c831"),
    ("gwangju", "광주시", "광역시", "20~30만원", "광역시", "photo-1494526585095-c41746248156"),
    ("daejeon", "대전시", "광역시", "20~30만원", "광역시", "photo-1533105079780-92b9be482077"),
    ("daegu", "대구시", "광역시", "20~30만원", "광역시", "photo-1542315192-1f61a1792f33"),
    ("incheon", "인천시", "광역시", "20~30만원", "광역시", "photo-1519501025264-65ba15a82390"),
    ("busan", "부산시", "광역시", "20~30만원", "광역시", "photo-1546874177-9e664107314e"),
    ("seoul", "서울시", "특별시", "25~35만원", "특별시", "photo-1517154421773-0529f29ea451"),
    ("yongin", "용인시", "시", "15~25만원", "경기도", "photo-1516253593875-bd7ba052fbc5"),
    ("suwon", "수원시", "시", "15~25만원", "경기도", "photo-1555881400-74d7acaacd8b"),
]


def download_image(photo_id):
    url = f"https://images.unsplash.com/{photo_id}?w=800&h=450&fit=crop&auto=format&q=80"
    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    try:
        req = urllib.request.Request(url); req.add_header("User-Agent", "Mozilla/5.0")
        with urllib.request.urlopen(req, timeout=30) as resp: tmp.write(resp.read())
        tmp.close(); return tmp.name
    except Exception as e:
        tmp.close(); os.unlink(tmp.name); return None

def upload_image(fp, fn, alt):
    with open(fp, "rb") as f: d = f.read()
    req = urllib.request.Request(MEDIA_API, data=d, method="POST")
    req.add_header("Authorization", f"Basic {AUTH}"); req.add_header("Content-Type", "image/jpeg")
    req.add_header("Content-Disposition", f'attachment; filename="{fn}.jpg"')
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            r = json.loads(resp.read().decode())
            mid, murl = r.get("id"), r.get("source_url", "")
            if mid and alt:
                ur = urllib.request.Request(f"{MEDIA_API}/{mid}", data=json.dumps({"alt_text": alt}).encode(), method="POST")
                ur.add_header("Authorization", f"Basic {AUTH}"); ur.add_header("Content-Type", "application/json")
                try: urllib.request.urlopen(ur, timeout=15)
                except: pass
            return mid, murl
    except Exception as e: return None, None


# CTA 버튼
C1 = {"text": "정부24 민생회복소비쿠폰 신청", "desc": "온라인 신청은 정부24에서 가능합니다", "url": "https://www.gov.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"}
C2 = {"text": "행정안전부 공식 안내", "desc": "민생회복소비쿠폰 공식 발표를 확인하세요", "url": "https://www.mois.go.kr/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"}
C3 = {"text": "내 지역 주민센터 찾기", "desc": "가까운 주민센터에서 오프라인 신청 가능", "url": "https://www.gov.kr/portal/locgovFind", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"}


def make_cta(c):
    b = f"border:{c['border']};" if c.get("border") else ""
    return f'<div style="background:{c["bg"]};{b}border-radius:12px;padding:28px 32px;margin:32px 0;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;"><div><p style="margin:0 0 6px;font-size:18px;font-weight:700;color:{c["text_color"]};">{c["text"]}</p><p style="margin:0;font-size:14px;color:{c["desc_color"]};">{c["desc"]}</p></div><a href="{c["url"]}" target="_blank" rel="noopener noreferrer" style="background:{c["btn_bg"]};color:{c["btn_color"]};padding:12px 24px;border-radius:8px;font-weight:700;text-decoration:none;white-space:nowrap;font-size:15px;">바로가기 &rarr;</a></div>'


def make_post_content(city_name, city_type, amount, region, img_url, img_alt):
    """도시별 5000자 이상 컨텐츠 생성"""
    intro = f"2026년 <strong>{city_name} 3차 민생회복소비쿠폰</strong>이 곧 지급될 예정입니다. {region}에 거주하는 {city_name} 주민이라면 누구나 신청할 수 있는 이번 3차 지원금은 1인당 약 {amount} 규모로, 지역 경제 활성화와 가계 부담 경감을 목표로 합니다. 이 글에서는 {city_name} 3차 민생회복소비쿠폰의 <strong>신청 방법, 지급일, 지급 기간, 신청 대상, 사용처</strong>를 상세히 정리합니다."

    img_html = f'<figure style="margin:32px 0;text-align:center;"><img src="{img_url}" alt="{img_alt}" style="width:100%;max-width:800px;height:auto;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.10);" loading="lazy" /><figcaption style="margin-top:8px;font-size:13px;color:#6b7280;">{img_alt}</figcaption></figure>' if img_url else ''

    h2 = lambda t: f'<h2 style="font-size:22px;font-weight:700;margin:40px 0 16px;border-left:4px solid #2563eb;padding-left:12px;">{t}</h2>'
    h3 = lambda t: f'<h3 style="font-size:17px;font-weight:600;color:#1e40af;margin:20px 0 8px;">Q. {t}</h3>'

    body = f'<p style="font-size:17px;line-height:1.8;margin-bottom:24px;">{intro}</p>\n{img_html}\n'

    # 섹션 1: 개요
    body += h2(f"{city_name} 3차 민생회복소비쿠폰 개요")
    body += f'<p>2026년 {city_name} 3차 민생회복소비쿠폰은 <strong>정부와 {region} 지자체가 공동 재원</strong>으로 추진하는 지역 소비 진작 정책입니다. 1차, 2차에 이어 3차로 지급되며, 이번에는 지급 대상이 확대되고 금액도 상향 조정될 가능성이 있습니다.</p>'
    body += '<table><thead><tr><th>항목</th><th>내용</th></tr></thead><tbody>'
    body += f'<tr><td>지급 대상</td><td>{city_name} 거주 주민등록자 전원</td></tr>'
    body += f'<tr><td>지급 금액</td><td>1인당 {amount} (가구 인원별 차등)</td></tr>'
    body += '<tr><td>지급 형태</td><td>지역화폐, 선불카드, 신용카드 포인트 중 선택</td></tr>'
    body += '<tr><td>신청 방법</td><td>온라인(정부24) / 오프라인(주민센터)</td></tr>'
    body += '<tr><td>사용 기한</td><td>지급일로부터 약 3~6개월</td></tr>'
    body += '<tr><td>사용처</td><td>전통시장, 동네 소상공인, 음식점 등</td></tr></tbody></table>'

    body += make_cta(C1)

    # 섹션 2: 신청 대상
    body += h2(f"{city_name} 3차 민생회복소비쿠폰 신청 대상")
    body += f'<p>{city_name} 3차 민생회복소비쿠폰의 <strong>신청 대상</strong>은 다음과 같습니다.</p>'
    body += '<ul>'
    body += f'<li><strong>기본 대상</strong>: 2026년 기준 {city_name}에 주민등록이 되어 있는 모든 국민</li>'
    body += f'<li><strong>외국인</strong>: 영주권자(F-5), 결혼이민자(F-6) 등 일부 체류자격 소지자</li>'
    body += '<li><strong>제외 대상</strong>: 주민등록 말소자, 해외 장기 체류자(90일 이상)</li>'
    body += '<li><strong>신생아</strong>: 기준일 이후 출생한 신생아도 소급 신청 가능</li>'
    body += '</ul>'
    body += f'<p>지급 기준일은 일반적으로 <strong>지급 공고일 기준</strong>으로 {city_name}에 주민등록이 되어 있어야 하며, 세대주 또는 세대원 중 한 명이 가구 단위로 신청할 수 있습니다.</p>'

    # 섹션 3: 신청 방법
    body += h2(f"{city_name} 민생회복소비쿠폰 신청 방법")
    body += '<p>신청 방법은 <strong>온라인 신청</strong>과 <strong>오프라인 신청</strong> 두 가지로 나뉩니다.</p>'
    body += '<ol>'
    body += '<li><strong>온라인 신청 (정부24)</strong>: 정부24 홈페이지 또는 앱 접속 → 공동인증서/간편인증 로그인 → 민생회복소비쿠폰 신청 → 수령 방법 선택 (지역화폐/카드)</li>'
    body += '<li><strong>카드사 앱 신청</strong>: 본인 명의의 신용카드/체크카드를 통해 카드사 홈페이지·앱에서 신청 → 카드 포인트로 충전</li>'
    body += f'<li><strong>주민센터 방문</strong>: 신분증 지참 후 {city_name} 내 주민센터 방문 → 신청서 작성 → 지역화폐/선불카드 현장 수령</li>'
    body += '</ol>'
    body += '<p><strong>온라인 신청 순서</strong>:</p>'
    body += '<ol>'
    body += '<li>정부24 접속 (https://www.gov.kr)</li>'
    body += '<li>"민생회복소비쿠폰" 검색</li>'
    body += '<li>공동인증서 또는 간편인증으로 로그인</li>'
    body += '<li>신청서 작성 (수령 방법 선택)</li>'
    body += '<li>접수 완료 → 문자 안내 수신</li>'
    body += '</ol>'

    body += make_cta(C2)

    # 섹션 4: 지급일 / 기간
    body += h2(f"{city_name} 3차 민생회복소비쿠폰 지급일 및 기간")
    body += f'<p>2026년 {city_name} 3차 민생회복소비쿠폰의 <strong>지급일과 기간</strong>은 다음과 같이 진행될 예정입니다.</p>'
    body += '<table><thead><tr><th>단계</th><th>예상 일정</th><th>비고</th></tr></thead><tbody>'
    body += '<tr><td>신청 시작일</td><td>2026년 상반기 예정</td><td>정부 공고 후</td></tr>'
    body += '<tr><td>신청 마감일</td><td>신청 시작일로부터 약 4주</td><td>마감일 엄수</td></tr>'
    body += '<tr><td>1차 지급일</td><td>신청 후 약 1주일 이내</td><td>온라인 신청 기준</td></tr>'
    body += '<tr><td>사용 기한</td><td>지급일로부터 3~6개월</td><td>기한 경과 시 소멸</td></tr></tbody></table>'
    body += '<p><strong>주의사항</strong>: 신청 마감일을 넘기면 지급이 불가하므로 반드시 기한 내에 신청해야 합니다. 지급된 쿠폰도 사용 기한을 넘기면 자동 소멸되므로 지급 직후 적극적으로 사용하는 것이 좋습니다.</p>'

    # 섹션 5: 사용처
    body += h2(f"{city_name} 민생회복소비쿠폰 사용처")
    body += f'<p>{city_name}에서 지급되는 소비쿠폰은 <strong>지역 내 소상공인 매장</strong>에서만 사용할 수 있습니다. 대형마트, 백화점, 온라인몰 등에서는 사용이 제한됩니다.</p>'
    body += '<p><strong>사용 가능한 곳:</strong></p>'
    body += '<ul>'
    body += '<li>전통시장 및 상점가</li>'
    body += '<li>동네 슈퍼마켓, 편의점</li>'
    body += '<li>음식점, 카페, 베이커리</li>'
    body += '<li>미용실, 세탁소, 학원 등 서비스업</li>'
    body += '<li>병원(비급여 진료), 약국</li>'
    body += '<li>주유소, 세차장</li>'
    body += '</ul>'
    body += '<p><strong>사용 불가한 곳:</strong></p>'
    body += '<ul>'
    body += '<li>대형마트(이마트, 홈플러스, 롯데마트)</li>'
    body += '<li>백화점, 면세점, 아울렛</li>'
    body += '<li>기업형 슈퍼마켓(SSM), 기업형 프랜차이즈 본사 직영점</li>'
    body += '<li>유흥업소, 사행업</li>'
    body += '<li>온라인 쇼핑몰</li>'
    body += '</ul>'

    body += make_cta(C3)

    # 섹션 6: 지급 금액 세부
    body += h2(f"{city_name} 지급 금액 세부 안내")
    body += f'<p>2026년 3차 민생회복소비쿠폰의 지급 금액은 <strong>가구 인원수에 따라 차등 지급</strong>될 가능성이 높습니다. 일반적으로 1인 가구보다 다인 가구에게 더 많은 금액이 지급됩니다.</p>'
    body += '<table><thead><tr><th>가구 구성</th><th>1차 지급액(참고)</th><th>3차 예상 금액</th></tr></thead><tbody>'
    body += '<tr><td>1인 가구</td><td>15만원</td><td>15~20만원</td></tr>'
    body += '<tr><td>2인 가구</td><td>25만원</td><td>25~35만원</td></tr>'
    body += '<tr><td>3인 가구</td><td>35만원</td><td>35~50만원</td></tr>'
    body += '<tr><td>4인 이상 가구</td><td>40만원</td><td>40~60만원</td></tr></tbody></table>'
    body += '<p><strong>취약계층 추가 지급</strong>: 기초생활수급자, 차상위계층, 한부모가정은 일반 지급액에 추가로 10~20만원이 지원될 수 있습니다.</p>'

    # 섹션 7: 주의사항
    body += h2(f"{city_name} 민생회복소비쿠폰 신청 시 주의사항")
    body += '<ol>'
    body += '<li><strong>본인 명의 계정/카드 사용</strong>: 타인 명의로 신청하면 부정수급으로 간주됩니다.</li>'
    body += '<li><strong>중복 신청 불가</strong>: 같은 가구에서 중복으로 신청할 수 없습니다.</li>'
    body += '<li><strong>사용 기한 엄수</strong>: 지급된 쿠폰은 사용 기한 내에 전액 사용해야 하며, 잔액은 소멸됩니다.</li>'
    body += '<li><strong>환불 제한</strong>: 쿠폰으로 결제한 상품은 환불 시 쿠폰으로만 환불됩니다.</li>'
    body += '<li><strong>가맹점 확인</strong>: 사용 전 해당 매장이 소비쿠폰 가맹점인지 확인하세요.</li>'
    body += '</ol>'

    # 섹션 8: 문의 안내
    body += h2(f"{city_name} 소비쿠폰 문의 및 민원 접수")
    body += '<ul>'
    body += '<li><strong>정부24 콜센터</strong>: 1588-2188</li>'
    body += '<li><strong>행정안전부</strong>: 044-205-5000</li>'
    body += f'<li><strong>{city_name} 시청</strong>: 시청 대표번호 또는 주민생활지원과</li>'
    body += '<li><strong>주민센터</strong>: 거주지 읍면동 주민센터</li>'
    body += '</ul>'
    body += f'<p>민원 발생 시에는 먼저 {city_name} 시청 또는 주민센터에 문의하고, 해결이 어려울 경우 정부24 콜센터를 이용하세요.</p>'

    # FAQ
    body += h2("자주 묻는 질문 (FAQ)")
    body += h3(f"{city_name} 3차 민생회복소비쿠폰은 누구나 받을 수 있나요?")
    body += f'<p>A. <strong>{city_name}에 주민등록이 되어 있는 모든 국민</strong>이 대상입니다. 외국인은 영주권자(F-5), 결혼이민자(F-6) 등 일부만 해당됩니다. 해외 장기 체류자(90일 이상)나 주민등록 말소자는 제외됩니다.</p>'
    body += h3("1차, 2차에 이미 받았는데 3차도 받을 수 있나요?")
    body += '<p>A. <strong>네, 1차/2차와 별개로 3차를 받을 수 있습니다.</strong> 각 차수는 독립적으로 지급되며, 이전에 받았다고 해서 3차에서 제외되지 않습니다.</p>'
    body += h3(f"{city_name} 소비쿠폰을 다른 지역에서 사용할 수 있나요?")
    body += f'<p>A. <strong>아니요, {city_name} 내 가맹점에서만 사용 가능</strong>합니다. 지역화폐 형태로 지급되는 쿠폰은 해당 지자체 내에서만 사용할 수 있습니다.</p>'
    body += h3("쿠폰 사용 기한이 지나면 어떻게 되나요?")
    body += '<p>A. <strong>사용 기한이 지나면 자동 소멸</strong>되며 환급되지 않습니다. 지급 후 3~6개월 이내에 반드시 사용해야 합니다.</p>'
    body += h3("온라인 신청이 어려운 어르신은 어떻게 신청하나요?")
    body += f'<p>A. <strong>주민센터 방문 신청</strong>이 가능합니다. 신분증을 지참하고 거주지 주민센터에 방문하면 직원이 신청을 도와드립니다. {city_name} 내 모든 주민센터에서 신청 가능합니다.</p>'
    body += h3("신용카드 포인트로 받으면 어떻게 사용하나요?")
    body += '<p>A. 카드사 앱에서 소비쿠폰을 신청하면 <strong>해당 카드의 포인트로 자동 충전</strong>됩니다. 가맹점에서 카드로 결제할 때 포인트가 먼저 차감되는 방식입니다. 별도의 조작이 필요 없어 가장 편리합니다.</p>'

    return body


def get_wp_media(photo_id, slug, alt):
    """이미지 다운로드 + 업로드 → (media_id, url)"""
    tmp = download_image(photo_id)
    if not tmp: return None, None
    mid, murl = upload_image(tmp, f"coupon-{slug}", alt)
    os.unlink(tmp)
    return mid, murl


def main():
    print(f"{'='*60}\n지원금 25개 포스트 발행 시작\n{'='*60}")
    published_urls = []
    success = fail = 0

    for i, (slug_en, city_name, city_type, amount, region, photo_id) in enumerate(CITIES, 1):
        full_slug = f"2026-{slug_en}-3rd-livelihood-coupon"
        title = f"2026 {city_name} 3차 민생회복소비쿠폰 지원금 신청방법 지급일 기간 대상 총정리"

        # 이미지 업로드
        alt = f"{city_name} 3차 민생회복소비쿠폰 지원금 안내"
        media_id, media_url = get_wp_media(photo_id, full_slug, alt)

        # 콘텐츠 생성
        content = make_post_content(city_name, city_type, amount, region, media_url, alt)

        # 발행
        payload = {
            "title": title,
            "content": content,
            "status": "publish",
            "slug": full_slug,
            "categories": [CAT_GETMONEY],
        }
        if media_id: payload["featured_media"] = media_id

        data = json.dumps(payload).encode()
        req = urllib.request.Request(API, data=data, headers={"Authorization": f"Basic {AUTH}", "Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req) as resp:
                r = json.loads(resp.read().decode())
                pid = r.get("id"); link = r.get("link", "")
                print(f"[{i}/{len(CITIES)}] OK | ID:{pid} | {title[:50]}")
                if link: print(f"  -> {link}"); published_urls.append(link)
                success += 1
        except urllib.error.HTTPError as e:
            print(f"[{i}/{len(CITIES)}] FAIL | {e.code}: {e.read().decode()[:150]}")
            fail += 1
        except Exception as e:
            print(f"[{i}/{len(CITIES)}] FAIL | {e}")
            fail += 1
        time.sleep(1)

    print(f"\n발행 완료! 성공: {success} / 실패: {fail}\n")

    # 인덱싱
    if published_urls:
        print(f"{'='*60}\nIndexNow\n{'='*60}")
        payload = {"host":"devupbox.com","key":"8dbbd7d6729b4a65b7dce4b9083c65e3","keyLocation":"https://devupbox.com/8dbbd7d6729b4a65b7dce4b9083c65e3.txt","urlList":published_urls}
        data = json.dumps(payload).encode()
        for n, ep in [("Naver","https://searchadvisor.naver.com/indexnow"),("Bing","https://www.bing.com/indexnow"),("Yandex","https://yandex.com/indexnow")]:
            req = urllib.request.Request(ep, data=data, method="POST"); req.add_header("Content-Type","application/json; charset=utf-8")
            try:
                with urllib.request.urlopen(req, timeout=30) as r: print(f"  {n}: HTTP {r.status}")
            except urllib.error.HTTPError as e: print(f"  {n}: HTTP {e.code}")

        print(f"\n{'='*60}\nGoogle Indexing API\n{'='*60}")
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            creds = service_account.Credentials.from_service_account_file("devupbox.json", scopes=["https://www.googleapis.com/auth/indexing"])
            svc = build("indexing","v3",credentials=creds); ok=0
            for idx,u in enumerate(published_urls,1):
                try: svc.urlNotifications().publish(body={"url":u,"type":"URL_UPDATED"}).execute(); print(f"  [{idx}/{len(published_urls)}] OK"); ok+=1
                except Exception as e: print(f"  [{idx}] FAIL | {str(e)[:50]}")
                time.sleep(3)
            print(f"\n  Google: {ok}/{len(published_urls)}")
        except Exception as e: print(f"  Google 실패: {e}")
    print("\n완료!")


if __name__ == "__main__":
    main()

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
    req = urllib.request.Request(MEDIA_API, data=data, method="POST")
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
                ur = urllib.request.Request(f"{MEDIA_API}/{mid}", data=ud, method="POST")
                ur.add_header("Authorization", f"Basic {AUTH}")
                ur.add_header("Content-Type", "application/json")
                try: urllib.request.urlopen(ur, timeout=15)
                except: pass
            return mid, murl
    except Exception as e:
        print(f"  업로드 실패: {e}")
        return None, None

def img_block(url, alt):
    return f'<!-- wp:image {{"sizeSlug":"large"}} -->\n<figure class="wp-block-image size-large"><img src="{url}" alt="{alt}"/><figcaption class="wp-element-caption">{alt}</figcaption></figure>\n<!-- /wp:image -->'

def cta(text, desc, url, style="blue"):
    s = {"blue":{"bg":"linear-gradient(135deg,#1e3a5f 0%,#2d5a8e 100%)","bb":"#fff","bc":"#1e3a5f","tc":"#fff","dc":"#cde0f5","bd":"none"},"yellow":{"bg":"#fffbeb","bb":"#f59e0b","bc":"#fff","tc":"#92400e","dc":"#78716c","bd":"2px solid #f59e0b"},"green":{"bg":"linear-gradient(135deg,#0f766e 0%,#14b8a6 100%)","bb":"#fff","bc":"#0f766e","tc":"#fff","dc":"#ccfbf1","bd":"none"}}[style]
    return f'<div style="background:{s["bg"]};border:{s["bd"]};border-radius:12px;padding:28px 32px;margin:32px 0;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;"><div><p style="margin:0 0 6px;font-size:18px;font-weight:700;color:{s["tc"]};">{text}</p><p style="margin:0;font-size:14px;color:{s["dc"]};">{desc}</p></div><a href="{url}" target="_blank" rel="noopener noreferrer" style="background:{s["bb"]};color:{s["bc"]};padding:12px 24px;border-radius:8px;font-weight:700;text-decoration:none;white-space:nowrap;font-size:15px;">바로가기 →</a></div>'

def post_content(title, intro, sections, faqs, ctas_list, imgs):
    """범용 콘텐츠 빌더"""
    html = f'<p style="font-size:17px;line-height:1.8;">{intro}</p>\n'
    if len(imgs) > 0 and imgs[0]: html += imgs[0] + "\n"
    cta_idx = 0
    for i, (stitle, sbody) in enumerate(sections):
        html += f'<h2>{stitle}</h2>\n{sbody}\n'
        if i == 1 and cta_idx < len(ctas_list):
            html += ctas_list[cta_idx] + "\n"; cta_idx += 1
        if i == len(sections)//2 and len(imgs) > 1 and imgs[1]:
            html += imgs[1] + "\n"
        if i == len(sections)-1 and cta_idx < len(ctas_list):
            html += ctas_list[cta_idx] + "\n"; cta_idx += 1
    html += '<h2>자주 묻는 질문 (FAQ)</h2>\n'
    for q, a in faqs:
        html += f'<h3>Q. {q}</h3>\n<p>A. {a}</p>\n'
    if cta_idx < len(ctas_list):
        html += ctas_list[cta_idx] + "\n"
    html += '<h2>마무리</h2>\n<p>이 글이 도움이 되셨다면 주변에도 공유해주세요. 궁금한 점은 댓글로 남겨주시기 바랍니다.</p>'
    return html

POSTS = [
    {
        "title": "데스크톱 조립 PC 추천 2026 용도별 견적 가이드",
        "cat": 5, "slug": "desktop-pc-build-guide-2026",
        "images": [("photo-1518770660439-4636190af475","조립PC 부품"),("photo-1593062096033-9a26b09da705","데스크톱 모니터 셋업")],
        "content": lambda imgs: post_content("조립PC", "2026년 데스크톱 PC를 직접 조립하면 같은 가격에 <strong>20~30% 더 높은 성능</strong>을 얻을 수 있습니다. 사무용부터 게이밍, 영상편집까지 용도별 최적 견적과 부품 선택법을 총정리합니다.", [
            ("2026년 CPU 추천 비교", "<table><thead><tr><th>용도</th><th>AMD</th><th>Intel</th><th>가격대</th></tr></thead><tbody><tr><td>사무용</td><td>Ryzen 5 7600</td><td>Core i5-14400F</td><td>15~20만원</td></tr><tr><td>게이밍</td><td>Ryzen 7 7800X3D</td><td>Core i7-14700K</td><td>30~45만원</td></tr><tr><td>영상편집</td><td>Ryzen 9 7950X</td><td>Core i9-14900K</td><td>50~70만원</td></tr></tbody></table><p>게이밍에는 <strong>Ryzen 7 7800X3D</strong>가 가성비 최강이며, 멀티코어 작업은 Intel이 유리합니다.</p>"),
            ("그래픽카드 추천", "<table><thead><tr><th>용도</th><th>모델</th><th>VRAM</th><th>가격</th></tr></thead><tbody><tr><td>사무용</td><td>내장그래픽(iGPU)</td><td>-</td><td>0원</td></tr><tr><td>FHD 게이밍</td><td>RTX 4060</td><td>8GB</td><td>35~40만원</td></tr><tr><td>QHD 게이밍</td><td>RTX 4070 Super</td><td>12GB</td><td>60~70만원</td></tr><tr><td>4K 게이밍/편집</td><td>RTX 4080 Super</td><td>16GB</td><td>100~120만원</td></tr></tbody></table>"),
            ("용도별 견적표", "<h3>사무용 PC (50만원)</h3><ul><li>CPU: Ryzen 5 7600 (20만원)</li><li>메인보드: B650M (10만원)</li><li>RAM: DDR5 16GB (5만원)</li><li>SSD: 500GB NVMe (5만원)</li><li>케이스+파워: (10만원)</li></ul><h3>게이밍 PC (120만원)</h3><ul><li>CPU: Ryzen 7 7800X3D (40만원)</li><li>GPU: RTX 4060 Ti (40만원)</li><li>메인보드: B650 (12만원)</li><li>RAM: DDR5 32GB (10만원)</li><li>SSD: 1TB NVMe (8만원)</li><li>케이스+파워 650W (10만원)</li></ul><h3>영상편집 PC (250만원)</h3><ul><li>CPU: Ryzen 9 7950X (60만원)</li><li>GPU: RTX 4070 Ti Super (80만원)</li><li>메인보드: X670E (25만원)</li><li>RAM: DDR5 64GB (20만원)</li><li>SSD: 2TB NVMe (15만원)</li><li>케이스+파워 850W (20만원)+쿨러(10만원)</li></ul>"),
            ("조립 순서 가이드", "<ol><li><strong>메인보드에 CPU 장착</strong>: 방향 맞춰 소켓에 올리고 레버 고정</li><li><strong>CPU 쿨러 장착</strong>: 서멀구리스 도포 후 쿨러 고정</li><li><strong>RAM 장착</strong>: 듀얼채널(2,4번 슬롯)에 딸깍 소리날 때까지</li><li><strong>M.2 SSD 장착</strong>: 메인보드 M.2 슬롯에 나사 고정</li><li><strong>메인보드를 케이스에 장착</strong>: 스탠드오프 확인 후 나사 고정</li><li><strong>파워서플라이 장착</strong>: 케이블 연결(24핀, 8핀 CPU, GPU 보조전원)</li><li><strong>그래픽카드 장착</strong>: PCIe 슬롯에 삽입, 보조전원 연결</li><li><strong>케이블 정리 후 부팅 테스트</strong></li></ol>"),
            ("호환성 체크 필수 사항", "<ul><li><strong>소켓 호환</strong>: AMD AM5 → 600시리즈 보드 / Intel LGA1700 → 600·700시리즈</li><li><strong>RAM 규격</strong>: DDR4와 DDR5는 호환 불가. 메인보드 지원 규격 확인</li><li><strong>파워 용량</strong>: GPU TDP + CPU TDP + 여유 200W 이상</li><li><strong>케이스 크기</strong>: ATX/mATX/ITX 메인보드 규격에 맞는 케이스 선택</li><li><strong>GPU 길이</strong>: 케이스 내부 GPU 클리어런스 확인 (보통 300~350mm)</li></ul>"),
        ], [
            ("조립PC와 완제품 PC 중 뭐가 나은가요?", "성능 대비 가격은 <strong>조립PC가 20~30% 저렴</strong>합니다. 다만 AS가 부품별로 따로이므로, 컴퓨터에 익숙하지 않다면 조립 대행 서비스(다나와 조립PC)를 이용하세요."),
            ("RAM은 16GB면 충분한가요?", "사무용·일반 게이밍은 16GB로 충분합니다. 영상편집, 3D 작업, 동시에 많은 프로그램을 사용한다면 <strong>32GB 이상</strong>을 추천합니다."),
            ("SSD와 HDD 중 뭘 선택해야 하나요?", "2026년 기준 <strong>NVMe SSD가 필수</strong>입니다. 부팅과 프로그램 실행 속도가 HDD 대비 5~10배 빠릅니다. 대용량 저장은 HDD를 추가로 사용하세요."),
        ], [cta("다나와에서 부품 최저가 비교","실시간 부품별 최저가와 호환성을 확인하세요","https://www.danawa.com/","blue"), cta("컴퓨존 조립PC 견적 받기","전문가가 호환성 검증한 조립PC 견적을 받아보세요","https://www.compuzone.co.kr/","yellow"), cta("쿠팡에서 PC 부품 로켓배송","오늘 주문하면 내일 도착! 부품을 빠르게 받아보세요","https://www.coupang.com/","green")], imgs)
    },
    {
        "title": "마우스 추천 2026 사무용 게이밍 버티컬 비교 TOP 10",
        "cat": 5, "slug": "mouse-recommendation-2026",
        "images": [("photo-1587829741301-dc798b83add3","마우스 키보드 셋업"),("photo-1486312338219-ce68d2c6f44d","사무용 마우스 작업")],
        "content": lambda imgs: post_content("마우스", "하루 8시간 이상 사용하는 마우스, 잘못 고르면 손목 통증의 원인이 됩니다. 2026년 사무용, 게이밍, 버티컬 마우스를 <strong>DPI, 무게, 연결 방식, 인체공학</strong> 기준으로 비교합니다.", [
            ("사무용 마우스 TOP 5 비교", "<table><thead><tr><th>모델</th><th>가격</th><th>DPI</th><th>무게</th><th>연결</th><th>배터리</th><th>특징</th></tr></thead><tbody><tr><td>로지텍 MX Master 3S</td><td>11만원</td><td>8,000</td><td>141g</td><td>BT+USB</td><td>70일</td><td>사무용 최고, 3대 동시연결</td></tr><tr><td>로지텍 M750</td><td>5만원</td><td>4,000</td><td>101g</td><td>BT+USB</td><td>24개월</td><td>가성비 최강</td></tr><tr><td>MS 에르고 마우스</td><td>8만원</td><td>2,400</td><td>133g</td><td>BT</td><td>15개월</td><td>인체공학 디자인</td></tr><tr><td>애플 매직마우스</td><td>11만원</td><td>1,300</td><td>99g</td><td>BT</td><td>1개월</td><td>맥 최적화, 제스처</td></tr><tr><td>라포 MT760</td><td>3만원</td><td>4,000</td><td>105g</td><td>BT+USB</td><td>12개월</td><td>초가성비</td></tr></tbody></table>"),
            ("게이밍 마우스 TOP 5 비교", "<table><thead><tr><th>모델</th><th>가격</th><th>DPI</th><th>무게</th><th>센서</th><th>특징</th></tr></thead><tbody><tr><td>로지텍 G Pro X Superlight 2</td><td>16만원</td><td>32,000</td><td>60g</td><td>HERO 2</td><td>초경량 무선, e스포츠 표준</td></tr><tr><td>레이저 DeathAdder V3</td><td>14만원</td><td>30,000</td><td>59g</td><td>Focus Pro 36K</td><td>인체공학, 대형 손</td></tr><tr><td>레이저 Viper V3 Pro</td><td>17만원</td><td>35,000</td><td>54g</td><td>Focus Pro 36K</td><td>최경량 무선</td></tr><tr><td>풀스타 X2V2</td><td>7만원</td><td>26,000</td><td>58g</td><td>PAW3395</td><td>가성비 무선 게이밍</td></tr><tr><td>로지텍 G502 X Plus</td><td>15만원</td><td>25,600</td><td>106g</td><td>HERO 25K</td><td>다버튼, 무한 스크롤</td></tr></tbody></table>"),
            ("버티컬 마우스 추천", "<p>손목터널증후군 예방을 위한 <strong>버티컬 마우스</strong>는 손목을 자연스러운 악수 자세로 유지합니다.</p><table><thead><tr><th>모델</th><th>가격</th><th>각도</th><th>연결</th><th>특징</th></tr></thead><tbody><tr><td>로지텍 Lift</td><td>7만원</td><td>57°</td><td>BT+USB</td><td>소형 손 최적, 조용한 클릭</td></tr><tr><td>로지텍 MX Vertical</td><td>10만원</td><td>57°</td><td>BT+USB</td><td>대형 손, 4000DPI</td></tr><tr><td>앱코 EM30</td><td>2만원</td><td>60°</td><td>유선</td><td>초가성비 입문용</td></tr></tbody></table>"),
            ("마우스 선택 기준 5가지", "<ol><li><strong>용도</strong>: 사무용은 인체공학+멀티페어링, 게이밍은 센서+무게</li><li><strong>손 크기</strong>: 소형(17cm 이하) → 소형 마우스, 대형(19cm+) → 대형 마우스</li><li><strong>그립 스타일</strong>: 팜그립(손바닥)/클로그립(손가락)/핑거팁(끝)</li><li><strong>유무선</strong>: 게이밍도 2026년 무선이 유선과 동일 지연 (1ms)</li><li><strong>배터리</strong>: 사무용은 6개월+, 게이밍은 70시간+ 권장</li></ol>"),
        ], [
            ("무선 마우스가 유선보다 입력 지연이 있나요?", "2026년 최신 무선 마우스는 <strong>1ms 이하 지연</strong>으로 유선과 체감 차이가 없습니다. 프로 게이머들도 무선을 사용합니다."),
            ("손목이 아프면 어떤 마우스가 좋나요?", "<strong>버티컬 마우스</strong>(로지텍 Lift, MX Vertical)를 추천합니다. 57도 각도가 손목 부담을 크게 줄여줍니다."),
            ("마우스 DPI가 높으면 좋은 건가요?", "DPI가 높다고 무조건 좋은 건 아닙니다. 사무용은 <strong>800~1600 DPI</strong>, 게이밍은 <strong>400~1600 DPI</strong>가 일반적입니다. 센서 정확도가 더 중요합니다."),
        ], [cta("다나와 마우스 최저가 비교","전 모델 실시간 최저가를 확인하세요","https://www.danawa.com/","blue"), cta("쿠팡 마우스 특가 확인","로켓배송 마우스 오늘의 특가를 확인하세요","https://www.coupang.com/","yellow"), cta("네이버 쇼핑에서 비교하기","네이버 가격비교로 최저가 판매처를 찾아보세요","https://search.shopping.naver.com/","green")], imgs)
    },
]

# 나머지 23개 포스트를 간결하게 생성하는 함수
def make_post(title, slug, imgs_ids, intro, sections, faqs, cta1, cta2, cta3):
    return {
        "title": title, "cat": 5, "slug": slug,
        "images": imgs_ids,
        "content": lambda imgs, intro=intro, sections=sections, faqs=faqs, cta1=cta1, cta2=cta2, cta3=cta3: post_content(title, intro, sections, faqs, [cta1, cta2, cta3], imgs)
    }

POSTS += [
    make_post("USB 허브 독 추천 2026 맥북 노트북 필수 액세서리", "usb-hub-dock-recommendation-2026",
        [("photo-1496181133206-80ce9b88a853","USB 허브 노트북 연결"),("photo-1460925895917-afdab827c52f","USB-C 독 셋업")],
        "맥북이나 최신 노트북에는 USB-C 포트만 있어서 <strong>USB 허브나 도킹스테이션</strong>이 필수입니다. 벨킨, 앤커, 칼디짓 등 주요 브랜드를 포트 구성, 전력 공급, 가격 기준으로 비교합니다.",
        [("USB-C 허브 vs 도킹스테이션 차이", "<table><thead><tr><th>구분</th><th>USB-C 허브</th><th>도킹스테이션</th></tr></thead><tbody><tr><td>가격</td><td>3~8만원</td><td>10~30만원</td></tr><tr><td>포트 수</td><td>5~8개</td><td>10~15개</td></tr><tr><td>전원</td><td>노트북 전원 사용</td><td>별도 전원 어댑터</td></tr><tr><td>모니터 출력</td><td>1대(대부분)</td><td>2~3대</td></tr><tr><td>휴대성</td><td>우수</td><td>고정 사용</td></tr><tr><td>추천 대상</td><td>이동 잦은 사용자</td><td>데스크 고정 사용자</td></tr></tbody></table>"),
        ("USB-C 허브 추천 TOP 5", "<table><thead><tr><th>모델</th><th>가격</th><th>포트</th><th>PD충전</th><th>특징</th></tr></thead><tbody><tr><td>앤커 PowerExpand 8-in-1</td><td>6만원</td><td>8개</td><td>100W</td><td>가성비 최강</td></tr><tr><td>벨킨 Connect 7-in-1</td><td>7만원</td><td>7개</td><td>100W</td><td>애플 공식 추천</td></tr><tr><td>사테치 V2 멀티포트</td><td>8만원</td><td>8개</td><td>87W</td><td>알루미늄 맥북 매칭</td></tr><tr><td>유그린 9-in-1</td><td>4만원</td><td>9개</td><td>100W</td><td>초가성비</td></tr><tr><td>하이퍼 HyperDrive 6-in-1</td><td>5만원</td><td>6개</td><td>60W</td><td>초소형 휴대용</td></tr></tbody></table>"),
        ("도킹스테이션 추천 TOP 3", "<table><thead><tr><th>모델</th><th>가격</th><th>포트</th><th>모니터</th><th>특징</th></tr></thead><tbody><tr><td>칼디짓 TS4</td><td>35만원</td><td>18개</td><td>듀얼 4K</td><td>최고급 썬더볼트4</td></tr><tr><td>벨킨 썬더볼트4 독</td><td>30만원</td><td>12개</td><td>듀얼 4K</td><td>애플 공식 추천</td></tr><tr><td>앤커 PowerExpand 13-in-1</td><td>15만원</td><td>13개</td><td>듀얼 QHD</td><td>가성비 독</td></tr></tbody></table>"),
        ("구매 시 체크포인트 5가지", "<ol><li><strong>PD 충전 와트</strong>: 노트북 충전기 와트 이상 지원 확인 (맥북 프로 96W)</li><li><strong>HDMI/DP 출력</strong>: 외부 모니터 사용 시 해상도·주사율 확인</li><li><strong>USB-A 포트</strong>: 기존 USB 기기 연결용 (최소 2개 추천)</li><li><strong>SD카드 슬롯</strong>: 사진/영상 작업자 필수</li><li><strong>발열</strong>: 장시간 사용 시 발열 적은 제품 선택</li></ol>"),
        ], [
            ("허브를 사용하면 속도가 느려지나요?", "USB 3.0 이상 허브는 <strong>5~10Gbps</strong>로 충분합니다. 다만 여러 기기를 동시에 사용하면 대역폭이 나눠질 수 있습니다."),
            ("맥북에 아무 허브나 써도 되나요?", "맥북은 <strong>USB-C/Thunderbolt</strong> 규격입니다. 맥북 호환 명시된 제품을 사용하세요. 일부 저가 허브는 macOS에서 인식 문제가 있습니다."),
            ("썬더볼트4와 USB4의 차이는?", "둘 다 40Gbps 속도이지만, <strong>썬더볼트4</strong>는 듀얼 4K 모니터, PCIe 터널링 등 추가 기능을 보장합니다."),
        ], cta("다나와에서 USB 허브 비교","전 모델 가격과 스펙을 비교하세요","https://www.danawa.com/","blue"), cta("쿠팡 USB허브 특가","로켓배송으로 빠르게 받아보세요","https://www.coupang.com/","yellow"), cta("앤커 공식몰 방문","앤커 공식몰에서 정품 구매 혜택을 확인하세요","https://www.anker.com/","green")),

    make_post("프린터 추천 2026 가정용 레이저 vs 잉크젯 비교", "printer-recommendation-2026",
        [("photo-1556742049-0cfed4f6a45d","프린터 문서 출력"),("photo-1460925895917-afdab827c52f","가정용 프린터")],
        "프린터는 <strong>잉크젯과 레이저</strong>, 두 종류 중 본인 용도에 맞는 것을 선택해야 합니다. 잘못 사면 유지비가 본체 가격을 넘길 수 있습니다. 삼성, HP, 엡손, 브라더 주요 모델을 비교합니다.",
        [("잉크젯 vs 레이저 비교", "<table><thead><tr><th>구분</th><th>잉크젯</th><th>레이저</th></tr></thead><tbody><tr><td>본체 가격</td><td>5~20만원</td><td>15~40만원</td></tr><tr><td>장당 인쇄비</td><td>50~150원</td><td>20~50원</td></tr><tr><td>인쇄 속도</td><td>보통 (분당 10~15장)</td><td>빠름 (분당 20~30장)</td></tr><tr><td>컬러 품질</td><td>우수 (사진 적합)</td><td>보통 (문서 적합)</td></tr><tr><td>유지비</td><td>잉크 교체 비용 높음</td><td>토너 수명 길어 저렴</td></tr><tr><td>추천 용도</td><td>사진, 소량 인쇄</td><td>문서, 대량 인쇄</td></tr></tbody></table>"),
        ("가정용 프린터 추천 TOP 5", "<table><thead><tr><th>모델</th><th>유형</th><th>가격</th><th>장당비용</th><th>특징</th></tr></thead><tbody><tr><td>HP 스마트탱크 580</td><td>잉크젯(무한잉크)</td><td>20만원</td><td>약 10원</td><td>가성비 최강, 무한잉크</td></tr><tr><td>엡손 L3250</td><td>잉크젯(무한잉크)</td><td>18만원</td><td>약 8원</td><td>잉크 비용 초저가</td></tr><tr><td>삼성 SL-M2030</td><td>흑백 레이저</td><td>12만원</td><td>약 25원</td><td>문서 전용, 빠른 출력</td></tr><tr><td>브라더 HL-L2350DW</td><td>흑백 레이저</td><td>15만원</td><td>약 20원</td><td>자동양면, 와이파이</td></tr><tr><td>HP 컬러레이저 150nw</td><td>컬러 레이저</td><td>25만원</td><td>약 40원</td><td>컬러 문서 출력</td></tr></tbody></table>"),
        ("프린터 유지비 비교", "<p>프린터 구매 시 본체 가격보다 <strong>유지비(잉크/토너)</strong>가 더 중요합니다.</p><ul><li><strong>일반 잉크젯</strong>: 카트리지 1세트 3~5만원, 약 200~500장 출력</li><li><strong>무한잉크 잉크젯</strong>: 잉크 1병 1만원, 약 4,000~7,000장 출력</li><li><strong>흑백 레이저</strong>: 토너 1개 5~8만원, 약 2,000~3,000장 출력</li><li><strong>결론</strong>: 월 50장 이상 인쇄 → 무한잉크 or 레이저 추천</li></ul>"),
        ("프린터 선택 기준", "<ol><li><strong>인쇄량</strong>: 월 50장 이하 → 잉크젯, 이상 → 레이저/무한잉크</li><li><strong>컬러 필요</strong>: 사진 출력 → 잉크젯, 문서만 → 흑백 레이저</li><li><strong>복합기 여부</strong>: 스캔/복사 필요 시 복합기 선택</li><li><strong>무선 지원</strong>: 와이파이/모바일 인쇄 지원 확인</li><li><strong>자동 양면</strong>: 용지 절약을 위해 자동양면 인쇄 추천</li></ol>"),
        ], [
            ("무한잉크 프린터가 정말 경제적인가요?", "네, 월 100장 이상 인쇄하면 <strong>1년에 잉크 비용이 1~2만원</strong> 수준입니다. 일반 카트리지 잉크젯 대비 10배 이상 저렴합니다."),
            ("레이저 프린터는 인체에 해롭나요?", "레이저 프린터는 미세먼지(토너 분진)를 발생시킬 수 있습니다. <strong>환기가 되는 곳</strong>에 설치하고, 토너 교체 시 마스크 착용을 권장합니다."),
            ("프린터 없이 출력하는 방법은?", "편의점(CU, GS25) <strong>무인 출력 서비스</strong>를 이용하면 장당 50~100원에 출력 가능합니다. 네이버 프린팅, 프린토 앱을 활용하세요."),
        ], cta("다나와 프린터 비교","전 모델 가격과 유지비를 비교하세요","https://www.danawa.com/","blue"), cta("쿠팡 프린터 특가","무한잉크 프린터 특가를 확인하세요","https://www.coupang.com/","yellow"), cta("네이버 쇼핑 프린터 비교","최저가 판매처를 한눈에 비교하세요","https://search.shopping.naver.com/","green")),
]

# 5~25번 간략 정의 - generate_post로 대량 생성
TOPICS = [
    ("빔프로젝터 추천 2026 가정용 캠핑용 가성비 TOP 7", "projector-recommendation-2026", [("photo-1593062096033-9a26b09da705","빔프로젝터 영상"),("photo-1611162617213-7d7a39e9b1d7","프로젝터 시청")],
     "빔프로젝터는 100인치 이상 대화면을 <strong>TV의 절반 가격</strong>에 즐길 수 있습니다. LG시네빔, 삼성 프리스타일, XGIMI, 엡손 등 가정용·캠핑용 프로젝터를 루멘, 해상도, 가격 기준으로 비교합니다.",
     [("가정용 프로젝터 TOP 5","<table><thead><tr><th>모델</th><th>가격</th><th>해상도</th><th>밝기</th><th>특징</th></tr></thead><tbody><tr><td>LG 시네빔 PU700R</td><td>130만원</td><td>4K</td><td>2,700안시</td><td>웹OS, 넷플릭스 내장</td></tr><tr><td>삼성 더 프리스타일 2</td><td>100만원</td><td>FHD</td><td>550안시</td><td>휴대용, 360도 회전</td></tr><tr><td>XGIMI Horizon Ultra</td><td>180만원</td><td>4K</td><td>2,300안시</td><td>돌비비전, 자동보정</td></tr><tr><td>엡손 EF-21</td><td>80만원</td><td>FHD</td><td>1,200안시</td><td>레이저 광원, 고수명</td></tr><tr><td>뷰소닉 PX701-4K</td><td>90만원</td><td>4K</td><td>3,200안시</td><td>고밝기 가성비</td></tr></tbody></table>"),
     ("프로젝터 선택 기준","<ul><li><strong>밝기(안시루멘)</strong>: 거실용 1,500+ / 암막 환경 800+</li><li><strong>해상도</strong>: FHD(1080p) 최소, 4K 추천</li><li><strong>투사 거리</strong>: 단초점(벽 가까이) vs 일반(3m 이상)</li><li><strong>광원</strong>: LED(수명 3만시간) vs 램프(수명 5천시간)</li><li><strong>스마트 기능</strong>: OS 내장 여부(별도 스틱 불필요)</li></ul>"),
     ("캠핑용 미니 프로젝터 추천","<table><thead><tr><th>모델</th><th>가격</th><th>무게</th><th>배터리</th><th>밝기</th></tr></thead><tbody><tr><td>삼성 프리스타일 2</td><td>100만원</td><td>830g</td><td>별도</td><td>550안시</td></tr><tr><td>XGIMI MoGo 2 Pro</td><td>60만원</td><td>1.1kg</td><td>내장(2시간)</td><td>400안시</td></tr><tr><td>앤커 네뷸라 캡슐3</td><td>55만원</td><td>850g</td><td>내장(2.5시간)</td><td>300안시</td></tr></tbody></table>")],
     [("프로젝터로 넷플릭스를 볼 수 있나요?","LG 시네빔(webOS), XGIMI(Android TV) 등 <strong>스마트OS 내장 모델</strong>은 넷플릭스를 바로 볼 수 있습니다. 미지원 모델은 크롬캐스트를 연결하세요."),
      ("프로젝터 수명은 얼마나 되나요?","LED/레이저 광원은 <strong>약 25,000~30,000시간</strong>으로, 하루 4시간 사용 시 17년 이상 사용 가능합니다."),
      ("스크린이 꼭 필요한가요?","흰 벽이면 스크린 없이도 감상 가능합니다. 하지만 <strong>전용 스크린</strong>을 사용하면 화질과 색감이 크게 향상됩니다. 3만원대 풀다운 스크린도 충분합니다.")]),

    ("블루투스 스피커 추천 2026 실내용 야외용 비교 TOP 10", "bluetooth-speaker-recommendation-2026", [("photo-1505740420928-5e560c06d30e","블루투스 스피커"),("photo-1484154218962-a197022b5858","실내 스피커")],
     "블루투스 스피커는 실내용과 야외용의 선택 기준이 다릅니다. <strong>음질, 방수, 배터리, 크기</strong>를 기준으로 JBL, 소니, 보스, 마샬, 하만카돈을 비교합니다.",
     [("실내용 스피커 TOP 5","<table><thead><tr><th>모델</th><th>가격</th><th>출력</th><th>배터리</th><th>특징</th></tr></thead><tbody><tr><td>소니 SRS-RA5000</td><td>45만원</td><td>50W</td><td>AC전원</td><td>360도 사운드, 하이레졸</td></tr><tr><td>마샬 스탠모어 III</td><td>40만원</td><td>80W</td><td>AC전원</td><td>빈티지 디자인, 강력한 저음</td></tr><tr><td>하만카돈 Aura Studio 4</td><td>35만원</td><td>40W</td><td>AC전원</td><td>LED 조명, 인테리어</td></tr><tr><td>보스 Home Speaker 500</td><td>35만원</td><td>30W</td><td>AC전원</td><td>알렉사 내장, 스테레오</td></tr><tr><td>소노스 Era 100</td><td>30만원</td><td>25W</td><td>AC전원</td><td>멀티룸 지원</td></tr></tbody></table>"),
     ("야외용 스피커 TOP 5","<table><thead><tr><th>모델</th><th>가격</th><th>방수</th><th>배터리</th><th>무게</th><th>특징</th></tr></thead><tbody><tr><td>JBL Charge 5</td><td>18만원</td><td>IP67</td><td>20시간</td><td>960g</td><td>보조배터리 기능</td></tr><tr><td>JBL Flip 6</td><td>13만원</td><td>IP67</td><td>12시간</td><td>550g</td><td>휴대성 최강</td></tr><tr><td>소니 SRS-XB33</td><td>15만원</td><td>IP67</td><td>24시간</td><td>1.1kg</td><td>Extra Bass</td></tr><tr><td>보스 SoundLink Flex</td><td>15만원</td><td>IP67</td><td>12시간</td><td>590g</td><td>음질 최고</td></tr><tr><td>마샬 윌렌</td><td>8만원</td><td>IP67</td><td>15시간</td><td>310g</td><td>초가성비 초소형</td></tr></tbody></table>"),
     ("스피커 선택 기준","<ol><li><strong>용도</strong>: 실내 고정 → AC전원 대출력 / 야외 휴대 → 배터리+방수</li><li><strong>방수등급</strong>: IP67(완전방수) 이상 추천</li><li><strong>코덱</strong>: aptX, LDAC 지원 시 고음질</li><li><strong>스테레오 페어링</strong>: 2대 연결로 스테레오 가능한지 확인</li></ol>")],
     [("블루투스 스피커 음질이 유선보다 나쁜가요?","LDAC, aptX HD 코덱 지원 제품은 <strong>CD 수준 음질</strong>을 제공합니다. 일반 SBC 코덱은 다소 손실이 있습니다."),
      ("방수 스피커를 물속에 넣어도 되나요?","IP67 등급은 <strong>1m 깊이에서 30분</strong> 방수입니다. 수영장 옆은 OK, 물속 장시간 사용은 피하세요."),
      ("스피커 2개를 연결할 수 있나요?","JBL PartyBoost, 소니 Stereo Pair 등 <strong>같은 브랜드 2대 연결</strong>로 스테레오 재생이 가능합니다.")]),
]

# TOPICS를 POSTS로 변환
for title, slug, imgs_ids, intro, secs, faqs in TOPICS:
    POSTS.append(make_post(title, slug, imgs_ids, intro, secs, faqs,
        cta("다나와에서 최저가 비교","전 모델 실시간 최저가를 확인하세요","https://www.danawa.com/","blue"),
        cta("쿠팡에서 특가 확인","로켓배송으로 빠르게 받아보세요","https://www.coupang.com/","yellow"),
        cta("네이버 쇼핑 비교","가격비교로 최저가 판매처를 찾아보세요","https://search.shopping.naver.com/","green")))

# 7~25번 추가 토픽
MORE_TOPICS = [
    ("게이밍 의자 추천 2026 허리 보호 가성비 비교 TOP 7", "gaming-chair-recommendation-2026", [("photo-1518770660439-4636190af475","게이밍 의자"),("photo-1486312338219-ce68d2c6f44d","사무용 의자")],
     "하루 8시간 이상 앉아있는 직장인과 게이머에게 의자는 <strong>건강 투자</strong>입니다. 시디즈, 듀오백, 허먼밀러, 제닉스 등 인기 의자를 허리 지지력, 소재, 가격 기준으로 비교합니다.",
     [("사무용/게이밍 의자 TOP 7","<table><thead><tr><th>모델</th><th>가격</th><th>유형</th><th>허리지지</th><th>특징</th></tr></thead><tbody><tr><td>시디즈 T80</td><td>60만원</td><td>사무용</td><td>S자 등판</td><td>국산 프리미엄, 틸팅</td></tr><tr><td>듀오백 알파</td><td>40만원</td><td>사무용</td><td>듀얼 등판</td><td>허리 분리 지지</td></tr><tr><td>허먼밀러 에어론</td><td>170만원</td><td>프리미엄</td><td>포스처핏</td><td>12년 보증, 최고급</td></tr><tr><td>제닉스 TITAN</td><td>25만원</td><td>게이밍</td><td>럼바서포트</td><td>가성비 게이밍</td></tr><tr><td>이케아 마르쿠스</td><td>20만원</td><td>사무용</td><td>기본</td><td>입문 가성비</td></tr><tr><td>시디즈 T50</td><td>35만원</td><td>사무용</td><td>럼바서포트</td><td>중급 가성비</td></tr><tr><td>DXRacer 포뮬러</td><td>30만원</td><td>게이밍</td><td>쿠션형</td><td>e스포츠 공식</td></tr></tbody></table>"),
     ("사무용 vs 게이밍 의자 차이","<table><thead><tr><th>구분</th><th>사무용</th><th>게이밍</th></tr></thead><tbody><tr><td>디자인</td><td>깔끔, 사무실 적합</td><td>화려, 레이싱 스타일</td></tr><tr><td>허리 지지</td><td>메쉬/S자 등판</td><td>쿠션+럼바 서포트</td></tr><tr><td>팔걸이</td><td>2D~4D 조절</td><td>1D~4D 조절</td></tr><tr><td>소재</td><td>메쉬(통기성)</td><td>PU가죽/패브릭</td></tr><tr><td>가격대</td><td>20~170만원</td><td>15~50만원</td></tr></tbody></table>"),
     ("의자 선택 체크리스트","<ol><li><strong>럼바 서포트</strong>: 허리 S자 곡선을 받쳐주는 기능 필수</li><li><strong>좌판 깊이 조절</strong>: 허벅지 뒤에 2~3cm 여유</li><li><strong>팔걸이 높이</strong>: 책상 높이와 맞춰야 어깨 통증 방지</li><li><strong>틸팅/리클라이닝</strong>: 등을 뒤로 젖힐 수 있는 기능</li><li><strong>메쉬 vs 가죽</strong>: 여름에 덥다면 메쉬 추천</li></ol>")],
     [("게이밍 의자가 허리에 좋은가요?","가격대에 따라 다릅니다. 15만원 이하 저가 게이밍 의자는 허리 지지가 부족할 수 있습니다. <strong>럼바서포트가 있는 30만원 이상</strong> 제품을 추천합니다."),
      ("의자에 가장 중요한 기능은?","<strong>럼바 서포트(허리 지지)</strong>입니다. 허리 S자 곡선을 유지해주는 기능이 없으면 장시간 착석 시 디스크의 원인이 됩니다."),
      ("허먼밀러가 비싼 값을 하나요?","12년 보증, 인체공학 설계, 내구성 면에서 <strong>장기적으로 가성비가 좋습니다</strong>. 중고 시장에서도 가치가 유지됩니다.")]),

    ("노트북 거치대 추천 2026 자세 교정 쿨링 효과 비교", "laptop-stand-recommendation-2026", [("photo-1496181133206-80ce9b88a853","노트북 거치대"),("photo-1593062096033-9a26b09da705","데스크 셋업")],
     "노트북을 책상에 그대로 놓고 쓰면 <strong>거북목과 어깨 통증</strong>의 원인이 됩니다. 거치대를 사용하면 시선 높이를 올려 자세를 교정하고, 통풍으로 발열도 줄일 수 있습니다.",
     [("노트북 거치대 유형별 비교","<table><thead><tr><th>유형</th><th>가격대</th><th>높이조절</th><th>쿨링</th><th>추천</th></tr></thead><tbody><tr><td>알루미늄 고정형</td><td>3~8만원</td><td>고정</td><td>자연냉각</td><td>데스크 고정 사용자</td></tr><tr><td>접이식 휴대형</td><td>1~3만원</td><td>다단계</td><td>없음</td><td>이동 많은 사용자</td></tr><tr><td>쿨링패드형</td><td>2~5만원</td><td>각도조절</td><td>팬 내장</td><td>발열 심한 게이밍 노트북</td></tr><tr><td>모니터암 겸용</td><td>5~15만원</td><td>자유</td><td>없음</td><td>듀얼 모니터 사용자</td></tr></tbody></table>"),
     ("추천 거치대 TOP 5","<table><thead><tr><th>모델</th><th>가격</th><th>유형</th><th>재질</th><th>특징</th></tr></thead><tbody><tr><td>레인디자인 mStand</td><td>6만원</td><td>고정형</td><td>알루미늄</td><td>맥북 매칭, 프리미엄</td></tr><tr><td>넥스트 NEXT-NBS5605</td><td>2만원</td><td>접이식</td><td>알루미늄</td><td>가성비 최강</td></tr><tr><td>쿨러마스터 U3 Plus</td><td>4만원</td><td>쿨링패드</td><td>알루미늄</td><td>3팬 쿨링</td></tr><tr><td>카멜마운트 CA2</td><td>8만원</td><td>모니터암</td><td>스틸</td><td>듀얼 사용 가능</td></tr><tr><td>MOFT 노트북스탠드</td><td>3만원</td><td>부착형</td><td>PU</td><td>초슬림 휴대</td></tr></tbody></table>"),
     ("거치대 효과","<ul><li><strong>자세 교정</strong>: 화면을 눈높이로 올려 거북목 예방</li><li><strong>쿨링</strong>: 바닥과 간격이 생겨 자연 통풍 → 온도 5~10°C 감소</li><li><strong>책상 정리</strong>: 거치대 아래 공간 활용 가능</li><li><strong>타이핑</strong>: 외장 키보드+거치대 조합이 가장 이상적</li></ul>")],
     [("거치대를 쓰면 외장 키보드가 필요한가요?","화면이 눈높이로 올라가므로 <strong>외장 키보드를 함께 사용</strong>하는 것이 편합니다. 무선 키보드를 추천합니다."),
      ("쿨링패드가 실제로 효과가 있나요?","게이밍 노트북 등 발열이 심한 기기에서 <strong>5~10°C 정도 온도를 낮추는 효과</strong>가 있습니다. 일반 사무용은 알루미늄 거치대의 자연냉각만으로 충분합니다."),
      ("맥북에 맞는 거치대는?","맥북과 디자인 매칭이 좋은 <strong>레인디자인 mStand</strong>를 추천합니다. 알루미늄 재질로 쿨링 효과도 있습니다.")]),

    ("스마트워치 추천 2026 애플워치 갤럭시워치 가민 비교", "smartwatch-recommendation-2026", [("photo-1563013544-824ae1b704d3","스마트워치 착용"),("photo-1551288049-bebda4e38f71","건강 데이터 차트")],
     "스마트워치는 단순한 시계를 넘어 <strong>건강 관리, 운동 트래킹, 알림</strong>의 핵심 기기입니다. Apple Watch, Galaxy Watch, Garmin 등 2026년 인기 모델을 비교합니다.",
     [("2026년 스마트워치 TOP 5 비교","<table><thead><tr><th>모델</th><th>가격</th><th>OS</th><th>배터리</th><th>건강기능</th><th>추천</th></tr></thead><tbody><tr><td>Apple Watch Ultra 2</td><td>95만원</td><td>watchOS</td><td>36시간</td><td>심전도,혈중산소,체온</td><td>아이폰+아웃도어</td></tr><tr><td>Apple Watch Series 10</td><td>55만원</td><td>watchOS</td><td>18시간</td><td>심전도,혈중산소</td><td>아이폰 일반</td></tr><tr><td>Galaxy Watch 7</td><td>35만원</td><td>Wear OS</td><td>40시간</td><td>심전도,체성분,체온</td><td>갤럭시 사용자</td></tr><tr><td>Garmin Venu 3</td><td>55만원</td><td>자체OS</td><td>14일</td><td>심박,수면,스트레스</td><td>운동 매니아</td></tr><tr><td>Galaxy Watch FE</td><td>20만원</td><td>Wear OS</td><td>30시간</td><td>심박,수면</td><td>입문 가성비</td></tr></tbody></table>"),
     ("건강 기능 비교","<table><thead><tr><th>기능</th><th>Apple Watch</th><th>Galaxy Watch</th><th>Garmin</th></tr></thead><tbody><tr><td>심전도(ECG)</td><td>O</td><td>O</td><td>X</td></tr><tr><td>혈중산소</td><td>O</td><td>O</td><td>O</td></tr><tr><td>체온 측정</td><td>O(Ultra)</td><td>O</td><td>X</td></tr><tr><td>체성분 분석</td><td>X</td><td>O</td><td>X</td></tr><tr><td>수면 분석</td><td>O</td><td>O</td><td>O(최고)</td></tr><tr><td>스트레스</td><td>X</td><td>O</td><td>O</td></tr></tbody></table>"),
     ("용도별 추천","<ul><li><strong>아이폰 사용자</strong>: Apple Watch Series 10 (유일한 선택)</li><li><strong>갤럭시 사용자</strong>: Galaxy Watch 7 (체성분 분석 독보적)</li><li><strong>운동 중심</strong>: Garmin Venu 3 (14일 배터리, GPS 정밀도)</li><li><strong>입문/가성비</strong>: Galaxy Watch FE (20만원대)</li></ul>")],
     [("애플워치를 안드로이드폰에 연결할 수 있나요?","아닙니다. Apple Watch는 <strong>아이폰 전용</strong>입니다. 안드로이드 사용자는 Galaxy Watch나 Garmin을 선택하세요."),
      ("스마트워치로 수영해도 되나요?","Apple Watch, Galaxy Watch 모두 <strong>5ATM 방수</strong>로 수영 가능합니다. 다만 사우나, 온수 사용은 권장하지 않습니다."),
      ("배터리가 가장 오래가는 스마트워치는?","<strong>Garmin Venu 3</strong>가 14일로 압도적입니다. 매일 충전이 부담되면 Garmin을 추천합니다.")]),

    ("액션캠 추천 2026 고프로 인스타360 DJI 비교", "action-camera-recommendation-2026", [("photo-1434030216411-0b793f4b4173","액션캠 촬영"),("photo-1460925895917-afdab827c52f","영상 편집")],
     "여행, 브이로그, 익스트림 스포츠에 필수인 <strong>액션캠</strong>. GoPro Hero 13, Insta360 X4, DJI Osmo Action 5를 화질, 손떨림 보정, 배터리, 가격 기준으로 비교합니다.",
     [("액션캠 TOP 5 비교","<table><thead><tr><th>모델</th><th>가격</th><th>해상도</th><th>손떨림</th><th>방수</th><th>특징</th></tr></thead><tbody><tr><td>GoPro Hero 13</td><td>55만원</td><td>5.3K/60fps</td><td>HyperSmooth 6.0</td><td>10m</td><td>업계 표준, 액세서리 풍부</td></tr><tr><td>DJI Osmo Action 5 Pro</td><td>45만원</td><td>4K/120fps</td><td>RockSteady 3.0+</td><td>20m</td><td>듀얼 터치스크린, 방수 최강</td></tr><tr><td>Insta360 X4</td><td>55만원</td><td>8K/360도</td><td>FlowState</td><td>10m</td><td>360도 촬영, 후편집 리프레임</td></tr><tr><td>Insta360 Ace Pro 2</td><td>45만원</td><td>8K/24fps</td><td>FlowState</td><td>10m</td><td>1/1.3인치 센서, 저조도 우수</td></tr><tr><td>GoPro Hero (보급형)</td><td>30만원</td><td>4K/60fps</td><td>HyperSmooth</td><td>5m</td><td>입문 가성비</td></tr></tbody></table>"),
     ("용도별 추천","<ul><li><strong>올라운드</strong>: GoPro Hero 13 - 가장 무난하고 액세서리가 풍부</li><li><strong>수중 촬영</strong>: DJI Osmo Action 5 Pro - 20m 방수 최강</li><li><strong>여행/브이로그</strong>: Insta360 X4 - 360도 촬영 후 원하는 앵글 편집</li><li><strong>저조도/야간</strong>: Insta360 Ace Pro 2 - 1/1.3인치 대형센서</li></ul>"),
     ("액션캠 필수 액세서리","<ol><li><strong>여분 배터리</strong>: 1개 배터리 약 1~2시간, 최소 3개 권장</li><li><strong>메모리카드</strong>: V30 이상 MicroSD 256GB 추천</li><li><strong>셀카봉/삼각대</strong>: 3-way 마운트 추천</li><li><strong>보호 케이스</strong>: 렌즈 스크래치 방지 필수</li></ol>")],
     [("스마트폰 카메라가 좋은데 액션캠이 필요한가요?","액션캠은 <strong>방수, 내충격, 초광각, 강력한 손떨림 보정</strong>에서 스마트폰을 압도합니다. 수중, 자전거, 스키 등 액티비티에는 필수입니다."),
      ("고프로와 DJI 중 뭘 사야 하나요?","액세서리 호환성은 <strong>고프로</strong>가 압도적, 화질과 방수는 <strong>DJI</strong>가 우수합니다. 이미 고프로 마운트가 있다면 고프로를 추천합니다."),
      ("360도 카메라가 정말 유용한가요?","촬영 후 원하는 앵글을 자유롭게 편집할 수 있어 <strong>혼자 여행하는 분께 강력 추천</strong>합니다. 놓치는 장면 없이 모든 방향을 기록합니다.")]),

    ("무료 PPT 대체 프로그램 추천 캔바 구글슬라이드 비교 2026", "free-ppt-alternative-2026", [("photo-1460925895917-afdab827c52f","프레젠테이션 작업"),("photo-1551288049-bebda4e38f71","슬라이드 디자인")],
     "파워포인트 없이도 <strong>무료로 멋진 프레젠테이션</strong>을 만들 수 있습니다. Canva, Google Slides, Prezi, Gamma 등 무료 PPT 대체 프로그램을 기능과 디자인 퀄리티 기준으로 비교합니다.",
     [("무료 PPT 프로그램 비교","<table><thead><tr><th>프로그램</th><th>가격</th><th>템플릿</th><th>협업</th><th>오프라인</th><th>특징</th></tr></thead><tbody><tr><td>Canva</td><td>무료(Pro $13/월)</td><td>수만 개</td><td>O</td><td>X</td><td>디자인 퀄리티 최고</td></tr><tr><td>Google Slides</td><td>완전 무료</td><td>기본 제공</td><td>O(최고)</td><td>O(확장)</td><td>실시간 협업 최강</td></tr><tr><td>Prezi</td><td>무료(Pro $7/월)</td><td>다수</td><td>O</td><td>X</td><td>줌인/아웃 애니메이션</td></tr><tr><td>Gamma</td><td>무료(Pro $10/월)</td><td>AI 생성</td><td>O</td><td>X</td><td>AI가 슬라이드 자동 생성</td></tr><tr><td>LibreOffice Impress</td><td>완전 무료</td><td>기본</td><td>X</td><td>O</td><td>PPT 파일 호환</td></tr></tbody></table>"),
     ("용도별 추천","<ul><li><strong>디자인 중시</strong>: Canva - 템플릿 퀄리티가 독보적</li><li><strong>팀 협업</strong>: Google Slides - 실시간 동시 편집 최강</li><li><strong>발표 효과</strong>: Prezi - 시각적 임팩트 있는 줌 애니메이션</li><li><strong>빠른 제작</strong>: Gamma - AI가 내용 입력만으로 슬라이드 생성</li><li><strong>PPT 호환</strong>: LibreOffice Impress - .pptx 파일 직접 편집 가능</li></ul>"),
     ("PPT 파일 호환성 비교","<ul><li><strong>Google Slides</strong>: PPT 가져오기/내보내기 지원 (일부 깨짐 가능)</li><li><strong>Canva</strong>: PPT 내보내기 가능, 가져오기 일부 지원</li><li><strong>LibreOffice</strong>: PPT/PPTX 직접 편집 가능 (호환성 가장 높음)</li><li><strong>Prezi/Gamma</strong>: PPT 직접 호환 제한적</li></ul>")],
     [("Canva 무료 버전으로 충분한가요?","대부분의 경우 <strong>무료 버전으로 충분</strong>합니다. Pro 버전은 프리미엄 템플릿, 배경 제거, 브랜드 키트 등이 추가됩니다."),
      ("Google Slides가 파워포인트를 완전히 대체할 수 있나요?","기본 기능은 충분하지만, 복잡한 애니메이션이나 매크로는 <strong>파워포인트가 여전히 우수</strong>합니다."),
      ("AI로 PPT를 자동 생성할 수 있나요?","<strong>Gamma</strong>에서 주제를 입력하면 AI가 슬라이드를 자동 생성합니다. ChatGPT + Canva 조합으로도 가능합니다.")]),

    ("무료 이미지 사이트 추천 저작권 걱정 없는 TOP 10 2026", "free-stock-image-sites-2026", [("photo-1499750310107-5fef28a66643","이미지 검색"),("photo-1547658719-da2b51169166","무료 사진 사이트")],
     "블로그, 유튜브 썸네일, 프레젠테이션에 사용할 <strong>저작권 걱정 없는 무료 이미지</strong>를 찾고 계신가요? 상업적 사용까지 가능한 무료 스톡 이미지 사이트 TOP 10을 소개합니다.",
     [("무료 이미지 사이트 TOP 10","<table><thead><tr><th>사이트</th><th>라이선스</th><th>상업용</th><th>출처표기</th><th>특징</th></tr></thead><tbody><tr><td>Unsplash</td><td>Unsplash License</td><td>O</td><td>불필요</td><td>고화질 사진 400만+</td></tr><tr><td>Pexels</td><td>Pexels License</td><td>O</td><td>불필요</td><td>사진+영상 무료</td></tr><tr><td>Pixabay</td><td>Pixabay License</td><td>O</td><td>불필요</td><td>일러스트+벡터 포함</td></tr><tr><td>Freepik</td><td>Free(제한)/Pro</td><td>O(출처표기)</td><td>무료시 필요</td><td>벡터/PSD/일러스트 풍부</td></tr><tr><td>공유마당(한국)</td><td>공공누리</td><td>O(유형별)</td><td>유형별 다름</td><td>한국 콘텐츠 특화</td></tr><tr><td>Kaboompics</td><td>자체 라이선스</td><td>O</td><td>불필요</td><td>라이프스타일 특화</td></tr><tr><td>StockSnap</td><td>CC0</td><td>O</td><td>불필요</td><td>매일 새 사진 추가</td></tr><tr><td>Burst(Shopify)</td><td>자체 라이선스</td><td>O</td><td>불필요</td><td>비즈니스/쇼핑 특화</td></tr><tr><td>ISO Republic</td><td>CC0</td><td>O</td><td>불필요</td><td>큐레이션된 고품질</td></tr><tr><td>Reshot</td><td>자체 라이선스</td><td>O</td><td>불필요</td><td>아이콘/일러스트 포함</td></tr></tbody></table>"),
     ("라이선스 종류 이해하기","<ul><li><strong>CC0 (퍼블릭 도메인)</strong>: 완전 자유 사용, 수정·상업용 모두 가능</li><li><strong>CC BY</strong>: 상업용 가능하지만 출처 표기 필수</li><li><strong>CC BY-NC</strong>: 비상업적 사용만 가능</li><li><strong>Unsplash/Pexels 자체 라이선스</strong>: 상업용 가능, 출처 불필요, 재판매만 금지</li><li><strong>공공누리</strong>: 1유형(자유이용)~4유형(비상업+변경금지) 확인 필요</li></ul>"),
     ("주의사항","<ul><li><strong>인물 사진</strong>: 초상권 문제가 있을 수 있어 상업 광고에는 모델 릴리스 확인</li><li><strong>로고/상표</strong>: 사진 속 브랜드 로고가 보이면 상업용 사용 시 주의</li><li><strong>AI 생성 이미지</strong>: 일부 사이트에 AI 이미지가 섞여 있으니 확인 필요</li></ul>")],
     [("블로그에 구글 이미지 검색 결과를 써도 되나요?","절대 안 됩니다. 구글 이미지 검색 결과는 <strong>저작권이 있는 이미지</strong>입니다. 반드시 무료 스톡 사이트를 이용하세요."),
      ("유튜브 썸네일에 무료 이미지를 써도 되나요?","Unsplash, Pexels 등의 이미지는 <strong>유튜브 썸네일에 상업적으로 사용 가능</strong>합니다."),
      ("한국 관련 이미지는 어디서 구하나요?","<strong>공유마당(gongu.copyright.or.kr)</strong>에서 한국 풍경, 문화, 음식 등 이미지를 무료로 받을 수 있습니다.")]),

    ("가계부 앱 추천 2026 뱅크샐러드 머니플러스 편한가계부 비교", "budget-app-recommendation-2026", [("photo-1484480974693-6ca0a78fb36b","가계부 앱 화면"),("photo-1551288049-bebda4e38f71","지출 분석 차트")],
     "돈 관리의 시작은 <strong>가계부</strong>입니다. 2026년 인기 가계부 앱 뱅크샐러드, 머니플러스, 편한가계부, 토스 등을 자동 연동, 카테고리 분류, 분석 기능 기준으로 비교합니다.",
     [("가계부 앱 TOP 5 비교","<table><thead><tr><th>앱</th><th>가격</th><th>자동연동</th><th>분석</th><th>특징</th></tr></thead><tbody><tr><td>뱅크샐러드</td><td>무료</td><td>은행+카드+보험</td><td>AI 분석</td><td>자산관리 올인원</td></tr><tr><td>토스</td><td>무료</td><td>은행+카드</td><td>기본</td><td>간편송금+가계부 통합</td></tr><tr><td>편한가계부</td><td>무료(Pro 유료)</td><td>수동+SMS</td><td>상세</td><td>수동 입력 최적화</td></tr><tr><td>머니플러스</td><td>무료</td><td>수동+SMS</td><td>상세</td><td>예산 관리 기능 우수</td></tr><tr><td>위플(Weple)</td><td>무료</td><td>수동</td><td>캘린더형</td><td>깔끔한 UI, 커플공유</td></tr></tbody></table>"),
     ("자동 연동 vs 수동 입력","<table><thead><tr><th>구분</th><th>자동 연동</th><th>수동 입력</th></tr></thead><tbody><tr><td>편리성</td><td>매우 편함</td><td>번거로움</td></tr><tr><td>정확도</td><td>높음</td><td>입력 누락 가능</td></tr><tr><td>소비 인식</td><td>낮음</td><td>높음(직접 입력으로 체감)</td></tr><tr><td>보안</td><td>금융정보 제공 필요</td><td>개인정보 불필요</td></tr><tr><td>추천</td><td>바쁜 직장인</td><td>절약 의지 강한 분</td></tr></tbody></table>"),
     ("가계부 작성 팁","<ol><li><strong>고정비 먼저 등록</strong>: 월세, 보험, 구독료 등 자동 입력</li><li><strong>카테고리 단순화</strong>: 식비, 교통, 문화, 쇼핑, 기타 5개면 충분</li><li><strong>주 1회 점검</strong>: 매주 일요일 지출 리뷰</li><li><strong>예산 설정</strong>: 카테고리별 월 예산을 설정하고 초과 알림 받기</li></ol>")],
     [("뱅크샐러드에 금융정보를 연동해도 안전한가요?","뱅크샐러드는 <strong>마이데이터 사업자</strong>로 금융위원회 인가를 받았습니다. 데이터는 암호화되어 저장됩니다."),
      ("가계부 앱 중 가장 추천하는 것은?","자동 연동을 원하면 <strong>뱅크샐러드</strong>, 직접 입력으로 소비 습관을 고치고 싶다면 <strong>편한가계부</strong>를 추천합니다."),
      ("커플이 함께 쓸 수 있는 가계부 앱은?","<strong>위플(Weple)</strong>이 커플 공유 기능을 지원합니다. 공동 지출을 함께 관리할 수 있습니다.")]),

    ("번역 앱 추천 2026 파파고 구글번역 딥엘 정확도 비교", "translation-app-comparison-2026", [("photo-1434030216411-0b793f4b4173","번역 앱 사용"),("photo-1517842645767-c639042777db","번역 작업")],
     "번역 앱의 정확도는 <strong>2026년 AI 기술</strong>로 비약적으로 향상되었습니다. 파파고, 구글번역, DeepL, ChatGPT까지 주요 번역 도구의 정확도, 속도, 지원 언어를 비교합니다.",
     [("번역 앱 비교표","<table><thead><tr><th>앱</th><th>가격</th><th>한→영</th><th>영→한</th><th>일→한</th><th>특징</th></tr></thead><tbody><tr><td>파파고</td><td>무료</td><td>우수</td><td>최고</td><td>최고</td><td>한/중/일 최강, 이미지번역</td></tr><tr><td>구글번역</td><td>무료</td><td>우수</td><td>우수</td><td>우수</td><td>133개 언어, 오프라인</td></tr><tr><td>DeepL</td><td>무료(Pro $9/월)</td><td>최고</td><td>우수</td><td>보통</td><td>유럽어 최강, 자연스러운 문체</td></tr><tr><td>ChatGPT</td><td>무료(Plus $20)</td><td>최고</td><td>최고</td><td>우수</td><td>맥락 이해, 문체 지정 가능</td></tr><tr><td>카카오i번역</td><td>무료</td><td>보통</td><td>보통</td><td>우수</td><td>카카오톡 내 바로 번역</td></tr></tbody></table>"),
     ("용도별 추천","<ul><li><strong>일상 번역(한중일)</strong>: 파파고 - 한/중/일 번역 정확도 최고</li><li><strong>영어 문서 번역</strong>: DeepL - 자연스러운 영어 번역 최강</li><li><strong>여행 중 즉석 번역</strong>: 구글번역 - 카메라/음성/오프라인 지원</li><li><strong>전문 번역/교정</strong>: ChatGPT - 문체, 톤, 전문 용어 지정 가능</li></ul>"),
     ("번역 정확도 높이는 팁","<ol><li><strong>짧은 문장으로 나누기</strong>: 긴 문장보다 2~3문장씩 나눠 번역</li><li><strong>주어 명시</strong>: 한국어는 주어 생략이 많으므로 주어를 넣어주면 정확도 향상</li><li><strong>2가지 이상 비교</strong>: 파파고+DeepL 결과를 교차 확인</li><li><strong>역번역 확인</strong>: 번역 결과를 다시 원문 언어로 번역해 의미 확인</li></ol>")],
     [("파파고와 구글번역 중 뭐가 더 정확한가요?","한국어↔일본어/중국어는 <strong>파파고</strong>, 한국어↔유럽어는 <strong>구글번역</strong>이 더 정확합니다. 영어는 비슷하지만 파파고가 약간 자연스럽습니다."),
      ("DeepL이 정말 좋은가요?","영어↔유럽어 번역은 <strong>DeepL이 독보적</strong>입니다. 한국어 번역도 계속 개선 중이지만, 한국어는 아직 파파고가 우세합니다."),
      ("ChatGPT로 번역하면 정확한가요?","문맥을 이해하고 톤을 지정할 수 있어 <strong>전문 문서나 마케팅 번역에 매우 유용</strong>합니다. 단순 번역은 파파고/DeepL이 빠릅니다.")]),

    ("일정 관리 앱 추천 2026 구글캘린더 타임트리 비교", "calendar-app-recommendation-2026", [("photo-1484480974693-6ca0a78fb36b","일정 관리 앱"),("photo-1517842645767-c639042777db","캘린더 메모")],
     "일정 관리는 생산성의 핵심입니다. Google Calendar, TimeTree, Notion Calendar 등 <strong>2026년 인기 캘린더 앱</strong>을 공유 기능, 연동성, UI 기준으로 비교합니다.",
     [("캘린더 앱 비교","<table><thead><tr><th>앱</th><th>가격</th><th>공유</th><th>연동</th><th>특징</th></tr></thead><tbody><tr><td>Google Calendar</td><td>무료</td><td>O</td><td>Gmail/Meet</td><td>업무용 표준, 일정 자동 추가</td></tr><tr><td>TimeTree</td><td>무료</td><td>O(최고)</td><td>기본</td><td>가족/커플 공유 최강</td></tr><tr><td>Notion Calendar</td><td>무료</td><td>O</td><td>Notion DB</td><td>할일+일정 통합</td></tr><tr><td>네이버 캘린더</td><td>무료</td><td>O</td><td>네이버 서비스</td><td>음력/공휴일 자동</td></tr><tr><td>Fantastical</td><td>유료($5/월)</td><td>O</td><td>Apple/Google</td><td>자연어 입력, 맥/iOS 최고</td></tr></tbody></table>"),
     ("용도별 추천","<ul><li><strong>직장인 업무</strong>: Google Calendar (Gmail 연동 필수)</li><li><strong>가족/커플</strong>: TimeTree (공유 캘린더 특화)</li><li><strong>프로젝트 관리</strong>: Notion Calendar (DB 연동)</li><li><strong>애플 유저</strong>: Fantastical (자연어 입력 편리)</li></ul>"),
     ("캘린더 활용 팁","<ol><li><strong>타임블로킹</strong>: 할 일을 시간 단위로 캘린더에 배치</li><li><strong>반복 일정</strong>: 정기 회의, 운동 등 반복 설정으로 자동화</li><li><strong>알림 설정</strong>: 중요 일정은 10분 전 + 1일 전 이중 알림</li><li><strong>색상 코딩</strong>: 업무(파랑), 개인(초록), 중요(빨강) 등 색상으로 구분</li></ol>")],
     [("구글캘린더와 애플캘린더를 동기화할 수 있나요?","네, 아이폰 설정 > 캘린더 > 계정 추가에서 <strong>Google 계정을 연동</strong>하면 양쪽에서 동기화됩니다."),
      ("커플이 일정을 공유하기 좋은 앱은?","<strong>TimeTree</strong>가 커플 공유에 최적화되어 있습니다. 상대방 일정을 한눈에 볼 수 있고 메모/사진 공유도 가능합니다."),
      ("캘린더에 할 일 관리도 할 수 있나요?","Google Calendar에 Task 기능이 있고, <strong>Notion Calendar</strong>는 할 일 DB와 연동되어 가장 강력합니다.")]),
]

for title, slug, imgs_ids, intro, secs, faqs in MORE_TOPICS:
    POSTS.append(make_post(title, slug, imgs_ids, intro, secs, faqs,
        cta("다나와에서 최저가 비교","전 모델 실시간 최저가를 확인하세요","https://www.danawa.com/","blue"),
        cta("쿠팡에서 특가 확인","로켓배송으로 빠르게 받아보세요","https://www.coupang.com/","yellow"),
        cta("네이버 쇼핑 비교","가격비교로 최저가 판매처를 찾아보세요","https://search.shopping.naver.com/","green")))

# 15~25번: 나머지 주제 간략 생성
REMAINING = [
    ("무료 다이어그램 도구 추천 Figma 미로 Draw.io 비교 2026", "free-diagram-tool-comparison-2026",
     "업무 플로우차트, 마인드맵, 와이어프레임을 만들 때 <strong>무료 다이어그램 도구</strong>가 필수입니다. Draw.io, Miro, Figma, Lucidchart를 기능과 가격 기준으로 비교합니다.",
     [("다이어그램 도구 비교","<table><thead><tr><th>도구</th><th>가격</th><th>용도</th><th>협업</th><th>특징</th></tr></thead><tbody><tr><td>Draw.io</td><td>완전 무료</td><td>플로우차트/다이어그램</td><td>O</td><td>설치 불필요, 구글 연동</td></tr><tr><td>Miro</td><td>무료(Pro $8/월)</td><td>화이트보드/브레인스토밍</td><td>O(최고)</td><td>무한 캔버스, 팀 협업</td></tr><tr><td>Figma</td><td>무료(Pro $15/월)</td><td>UI/UX 디자인</td><td>O</td><td>와이어프레임, 프로토타입</td></tr><tr><td>Lucidchart</td><td>무료(Pro $8/월)</td><td>플로우차트/ERD</td><td>O</td><td>비즈니스 다이어그램 특화</td></tr><tr><td>Whimsical</td><td>무료(Pro $10/월)</td><td>마인드맵/플로우</td><td>O</td><td>깔끔한 UI, 마인드맵 우수</td></tr></tbody></table>"),
     ("용도별 추천","<ul><li><strong>플로우차트</strong>: Draw.io (무료+간편)</li><li><strong>팀 브레인스토밍</strong>: Miro (무한 캔버스)</li><li><strong>UI 설계</strong>: Figma (업계 표준)</li><li><strong>마인드맵</strong>: Whimsical (깔끔한 UI)</li></ul>")]),

    ("무료 글꼴 폰트 사이트 추천 상업용 무료 한글 폰트 모음 2026", "free-korean-font-sites-2026",
     "디자인, 영상, 문서 작업에 <strong>예쁜 한글 폰트</strong>를 찾고 계신가요? 상업적 사용까지 가능한 무료 한글 폰트 사이트와 인기 폰트를 소개합니다.",
     [("무료 폰트 사이트 TOP 5","<table><thead><tr><th>사이트</th><th>폰트 수</th><th>상업용</th><th>특징</th></tr></thead><tbody><tr><td>눈누(noonnu.cc)</td><td>1,000+</td><td>O(개별 확인)</td><td>한글 폰트 통합 검색</td></tr><tr><td>네이버 나눔폰트</td><td>15+</td><td>O</td><td>나눔고딕/바른체 등</td></tr><tr><td>카카오 브랜딩체</td><td>5+</td><td>O</td><td>카카오 빅체/작은체</td></tr><tr><td>Google Fonts</td><td>50+(한글)</td><td>O</td><td>노토산스 등 웹폰트</td></tr><tr><td>공공기관 폰트</td><td>20+</td><td>O</td><td>서울체, 부산체, 제주체 등</td></tr></tbody></table>"),
     ("인기 무료 한글 폰트 TOP 10","<ol><li><strong>Pretendard</strong> - 애플 산돌고딕 대체, 웹/앱 최적</li><li><strong>나눔스퀘어</strong> - 깔끔한 고딕, PPT 필수</li><li><strong>마루부리</strong> - 세련된 명조체</li><li><strong>카카오 빅체</strong> - 임팩트 있는 제목용</li><li><strong>노토산스 KR</strong> - 구글 공식, 다국어 지원</li><li><strong>IBM Plex Sans KR</strong> - 코딩+문서 겸용</li><li><strong>Gmarket Sans</strong> - 쇼핑몰 디자인 인기</li><li><strong>배달의민족 폰트</strong> - 주아체, 한나체 등</li><li><strong>서울 한강체/남산체</strong> - 서울시 공식 폰트</li><li><strong>KoPub World</strong> - 출판/인쇄 최적화</li></ol>")]),

    ("클라우드 백업 프로그램 추천 자동 백업 설정 방법 2026", "cloud-backup-program-2026",
     "컴퓨터 고장, 랜섬웨어, 실수로 삭제... <strong>백업이 없으면 복구 불가능</strong>합니다. Backblaze, Google Drive, OneDrive 등 자동 백업 프로그램을 비교하고 설정 방법을 안내합니다.",
     [("백업 프로그램 비교","<table><thead><tr><th>프로그램</th><th>가격</th><th>용량</th><th>자동백업</th><th>특징</th></tr></thead><tbody><tr><td>Backblaze</td><td>$7/월</td><td>무제한</td><td>O</td><td>무제한 PC 백업 최강</td></tr><tr><td>Google Drive</td><td>무료 15GB(100GB $2/월)</td><td>15GB~2TB</td><td>O</td><td>구글 생태계 연동</td></tr><tr><td>OneDrive</td><td>무료 5GB(1TB $7/월)</td><td>5GB~1TB</td><td>O</td><td>윈도우 기본 내장</td></tr><tr><td>iCloud</td><td>무료 5GB(50GB $1/월)</td><td>5GB~12TB</td><td>O</td><td>애플 기기 자동</td></tr><tr><td>Synology NAS</td><td>하드웨어 30만원+</td><td>무제한(HDD)</td><td>O</td><td>로컬+원격 이중백업</td></tr></tbody></table>"),
     ("3-2-1 백업 규칙","<ul><li><strong>3</strong>: 중요 데이터를 3개 복사본으로 보관</li><li><strong>2</strong>: 2종류 이상의 저장매체 사용 (SSD + 클라우드)</li><li><strong>1</strong>: 1개는 원격지(클라우드)에 보관</li></ul>")]),

    ("엑셀 대체 무료 프로그램 구글시트 리브레오피스 비교 2026", "free-excel-alternative-2026",
     "엑셀 없이도 스프레드시트 작업이 가능합니다. <strong>Google Sheets, LibreOffice Calc, WPS</strong> 등 무료 대안을 기능, 호환성, 속도 기준으로 비교합니다.",
     [("무료 스프레드시트 비교","<table><thead><tr><th>프로그램</th><th>가격</th><th>엑셀 호환</th><th>협업</th><th>매크로</th><th>특징</th></tr></thead><tbody><tr><td>Google Sheets</td><td>무료</td><td>높음</td><td>O(최고)</td><td>Apps Script</td><td>실시간 협업, 어디서나 접속</td></tr><tr><td>LibreOffice Calc</td><td>무료</td><td>매우 높음</td><td>X</td><td>O(VBA 일부)</td><td>오프라인 사용, 엑셀과 가장 유사</td></tr><tr><td>WPS Spreadsheets</td><td>무료(Pro 유료)</td><td>높음</td><td>O</td><td>O</td><td>엑셀 UI와 거의 동일</td></tr><tr><td>Zoho Sheet</td><td>무료</td><td>보통</td><td>O</td><td>기본</td><td>비즈니스 용도 적합</td></tr></tbody></table>"),
     ("용도별 추천","<ul><li><strong>팀 협업</strong>: Google Sheets (실시간 편집 최강)</li><li><strong>엑셀 호환</strong>: LibreOffice Calc (수식, 서식 호환 최고)</li><li><strong>엑셀과 동일 UI</strong>: WPS Spreadsheets (적응 시간 0)</li></ul>")]),

    ("IPTV 비교 SK KT LG 요금 채널 셋톱박스 총정리 2026", "iptv-comparison-2026",
     "IPTV 3사(SK Btv, KT 올레tv, LG U+tv)의 <strong>요금, 채널, 화질, 셋톱박스</strong>를 비교합니다. 인터넷과 결합 시 할인까지 고려한 최적의 선택을 안내합니다.",
     [("IPTV 3사 비교","<table><thead><tr><th>구분</th><th>SK Btv</th><th>KT 올레tv</th><th>LG U+tv</th></tr></thead><tbody><tr><td>기본 요금</td><td>월 13,200원~</td><td>월 13,200원~</td><td>월 12,100원~</td></tr><tr><td>채널 수</td><td>약 230개</td><td>약 240개</td><td>약 220개</td></tr><tr><td>4K 지원</td><td>O</td><td>O</td><td>O</td></tr><tr><td>AI 추천</td><td>O</td><td>O(기가지니)</td><td>O</td></tr><tr><td>OTT 결합</td><td>wavve 포함</td><td>시즌 포함</td><td>자체 콘텐츠</td></tr><tr><td>인터넷 결합할인</td><td>최대 1.1만원</td><td>최대 1.1만원</td><td>최대 1.1만원</td></tr></tbody></table>"),
     ("인터넷+IPTV 결합 추천","<ul><li><strong>SK 사용자</strong>: Btv + wavve 결합 → OTT 무료</li><li><strong>KT 사용자</strong>: 올레tv + 기가지니 → AI 스피커 겸용</li><li><strong>LG 사용자</strong>: U+tv + 아이들나라 → 키즈 콘텐츠 최강</li></ul>")]),

    ("전자도서관 무료 이북 서비스 추천 총정리 2026", "free-ebook-library-service-2026",
     "도서관에 가지 않아도 <strong>전자책을 무료</strong>로 빌릴 수 있습니다. 국립중앙도서관, 지역 전자도서관, 밀리의서재 무료체험까지 총정리합니다.",
     [("무료 전자도서관 비교","<table><thead><tr><th>서비스</th><th>가격</th><th>도서 수</th><th>대출 권수</th><th>특징</th></tr></thead><tbody><tr><td>국립중앙도서관</td><td>무료</td><td>20만+</td><td>5권/14일</td><td>전국민 이용 가능</td></tr><tr><td>서울도서관(서울시)</td><td>무료</td><td>15만+</td><td>5권/14일</td><td>서울시민 대상</td></tr><tr><td>YES24 도서관</td><td>무료</td><td>10만+</td><td>3권/14일</td><td>지역 도서관 연계</td></tr><tr><td>교보문고 SAM</td><td>월 7,900원</td><td>15만+</td><td>무제한</td><td>구독형, 최신간 포함</td></tr><tr><td>밀리의서재</td><td>월 9,900원(첫달무료)</td><td>12만+</td><td>무제한</td><td>오디오북 포함</td></tr></tbody></table>"),
     ("전자도서관 이용 방법","<ol><li>도서관 홈페이지에서 <strong>회원가입</strong> (거주지 인증)</li><li>전자책 앱 설치 (교보문고, 리디, 예스24 등)</li><li>원하는 도서 검색 → <strong>대출 신청</strong></li><li>앱에서 다운로드 후 오프라인 읽기 가능</li><li>대출 기간(보통 14일) 만료 시 자동 반납</li></ol>")]),

    ("AI 이미지 생성 도구 추천 미드저니 달리 스테이블디퓨전 비교 2026", "ai-image-generator-comparison-2026",
     "텍스트 한 줄로 <strong>전문가 수준의 이미지</strong>를 만들 수 있는 시대입니다. Midjourney, DALL-E 3, Stable Diffusion, Adobe Firefly를 품질, 가격, 사용법 기준으로 비교합니다.",
     [("AI 이미지 생성 도구 비교","<table><thead><tr><th>도구</th><th>가격</th><th>품질</th><th>속도</th><th>상업용</th><th>특징</th></tr></thead><tbody><tr><td>Midjourney</td><td>$10/월~</td><td>최고</td><td>빠름</td><td>O</td><td>예술적 퀄리티 최강</td></tr><tr><td>DALL-E 3(ChatGPT)</td><td>ChatGPT Plus $20/월</td><td>상</td><td>빠름</td><td>O</td><td>텍스트 이해력 최고</td></tr><tr><td>Stable Diffusion</td><td>무료(로컬설치)</td><td>상</td><td>GPU 필요</td><td>O</td><td>완전 무료, 커스터마이징</td></tr><tr><td>Adobe Firefly</td><td>무료(제한)/CC포함</td><td>상</td><td>빠름</td><td>O(안전)</td><td>저작권 안전, 포토샵 통합</td></tr><tr><td>Canva AI</td><td>무료(제한)</td><td>중상</td><td>빠름</td><td>O</td><td>디자인 작업에 바로 적용</td></tr></tbody></table>"),
     ("용도별 추천","<ul><li><strong>고품질 예술 이미지</strong>: Midjourney</li><li><strong>간편한 이미지 생성</strong>: DALL-E 3 (ChatGPT 채팅으로 생성)</li><li><strong>무료+완전 제어</strong>: Stable Diffusion (GPU 필요)</li><li><strong>상업용 안전</strong>: Adobe Firefly (저작권 학습 데이터)</li></ul>")]),

    ("공인인증서 폐지 후 전자서명 간편인증 총정리 2026", "digital-certificate-simple-auth-2026",
     "공인인증서가 폐지된 후 <strong>간편인증</strong>이 대세가 되었습니다. 카카오, 네이버, PASS, 토스 등 간편인증 서비스를 보안, 편의성, 사용처 기준으로 비교합니다.",
     [("간편인증 서비스 비교","<table><thead><tr><th>서비스</th><th>인증 방식</th><th>사용처</th><th>보안등급</th><th>특징</th></tr></thead><tbody><tr><td>카카오 인증서</td><td>지문/PIN</td><td>은행, 공공기관, 보험</td><td>높음</td><td>카카오톡 내 바로 인증</td></tr><tr><td>네이버 인증서</td><td>지문/PIN</td><td>은행, 공공기관</td><td>높음</td><td>네이버앱에서 바로 인증</td></tr><tr><td>PASS 인증서</td><td>지문/PIN</td><td>통신3사, 은행, 공공</td><td>높음</td><td>통신사 기반, 본인확인 강점</td></tr><tr><td>토스 인증서</td><td>지문/PIN</td><td>은행, 증권, 보험</td><td>높음</td><td>금융 특화, 간편 사용</td></tr><tr><td>KB모바일 인증서</td><td>지문/PIN</td><td>KB금융그룹</td><td>높음</td><td>KB 서비스 최적화</td></tr></tbody></table>"),
     ("간편인증 발급 방법","<ol><li>해당 앱(카카오톡/네이버/토스 등) 설치</li><li>본인인증 (휴대폰 인증 또는 신분증 촬영)</li><li>인증서 발급 요청 → 지문/PIN 등록</li><li>발급 완료 (보통 1~3분 소요)</li></ol>")]),
]

for title, slug, intro, secs in REMAINING:
    POSTS.append(make_post(title, slug,
        [("photo-1460925895917-afdab827c52f", title.split()[0]),("photo-1551288049-bebda4e38f71", title.split()[0]+" 비교")],
        intro, secs,
        [(f"{title.split()[0]} 관련 비용은?","상품과 조건에 따라 다릅니다. 위 비교표를 참고하여 본인에게 맞는 것을 선택하세요."),
         (f"초보자에게 가장 추천하는 것은?","입문자에게는 <strong>무료 버전</strong>부터 시작하는 것을 추천합니다. 익숙해진 후 유료 업그레이드를 고려하세요."),
         (f"모바일에서도 사용 가능한가요?","대부분의 서비스가 <strong>모바일 앱</strong>을 지원합니다. iOS와 Android 모두 사용 가능합니다.")],
        cta("더 자세한 정보 확인","관련 최신 정보를 확인하세요","https://www.google.com/","blue"),
        cta("네이버에서 검색","네이버에서 관련 정보를 검색하세요","https://search.naver.com/","yellow"),
        cta("관련 커뮤니티 방문","사용자 리뷰와 팁을 확인하세요","https://www.clien.net/","green")))

def main():
    published = []
    for idx, post in enumerate(POSTS, 1):
        print(f"\n{'='*60}")
        print(f"[{idx}/{len(POSTS)}] {post['title']}")
        print(f"{'='*60}")
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
        content = post["content"](img_htmls)
        payload = {"title": post["title"], "content": content, "status": "publish", "slug": post["slug"], "categories": [post["cat"]]}
        if first_media_id:
            payload["featured_media"] = first_media_id
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(API, data=data, method="POST")
        req.add_header("Authorization", f"Basic {AUTH}")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                r = json.loads(resp.read().decode())
                print(f"  발행 OK | ID:{r.get('id')} | {r.get('link','')}")
                published.append(r.get("link",""))
        except Exception as e:
            print(f"  발행 FAIL | {e}")
        time.sleep(1)
    if published:
        print(f"\n{'='*60}\nIndexNow 제출\n{'='*60}")
        np_data = {"host":"devupbox.com","key":"8dbbd7d6729b4a65b7dce4b9083c65e3","keyLocation":"https://devupbox.com/8dbbd7d6729b4a65b7dce4b9083c65e3.txt","urlList":published}
        nd = json.dumps(np_data).encode("utf-8")
        for name, eu in [("Naver","https://searchadvisor.naver.com/indexnow"),("Bing","https://www.bing.com/indexnow"),("Yandex","https://yandex.com/indexnow")]:
            req = urllib.request.Request(eu, data=nd, method="POST")
            req.add_header("Content-Type", "application/json; charset=utf-8")
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    print(f"  {name}: HTTP {resp.status}")
            except urllib.error.HTTPError as e:
                print(f"  {name}: HTTP {e.code}")
            except Exception as e:
                print(f"  {name}: {e}")
    print(f"\n완료! {len(published)}개 발행")

if __name__ == "__main__":
    main()

import json
import urllib.request
import urllib.error
import base64
import time
import ssl
import os
import tempfile
import re

ssl._create_default_https_context = ssl._create_unverified_context
AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API = "https://devupbox.com/wp-json/wp/v2/posts"
MEDIA_API = "https://devupbox.com/wp-json/wp/v2/media"

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

# ========== 5개 포스트 정의 ==========
POSTS = [
    # 1. 종량제닷컴
    {
        "title": "종량제닷컴 종량제봉투 온라인 주문 가격 배달 방법 2026 총정리",
        "cat": 13,
        "slug": "jongryangjae-dotcom-waste-bag-order-2026",
        "images": [
            ("photo-1558618666-fcd25c85f82e", "종량제봉투 온라인 주문"),
            ("photo-1532996122724-e3c354a0b15b", "재활용 쓰레기봉투 종류"),
            ("photo-1604187351574-c75ca79f5807", "종량제봉투 배달 수령"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">바쁜 일상 속에서 <strong>종량제봉투</strong>를 사러 편의점이나 슈퍼마켓까지 직접 가는 번거로움을 해결해 주는 서비스가 있습니다. 바로 <strong>종량제닷컴(jongryangjae.com)</strong>입니다. 주민센터나 마트에 가지 않고도 클릭 몇 번으로 내 집 앞까지 종량제봉투를 배달받을 수 있어, 특히 거동이 불편한 어르신이나 바쁜 직장인에게 큰 인기를 끌고 있습니다. 이 글에서는 종량제닷컴 이용 방법, 지역별 가격, 배달 방법, 오프라인 구매와의 비교까지 완벽하게 정리합니다.</p>

{imgs[0]}

<h2>종량제닷컴이란?</h2>
<p><strong>종량제닷컴</strong>은 전국 각 지자체 공식 규격 종량제봉투를 온라인으로 주문하고 택배로 받을 수 있는 쇼핑몰입니다. 지자체별로 규격이 다른 종량제봉투의 특성상, 종량제닷컴은 배송 주소 기반으로 해당 지역 규격봉투를 자동 매칭하여 발송합니다.</p>
<table><thead><tr><th>구분</th><th>내용</th></tr></thead><tbody>
<tr><td>서비스명</td><td>종량제닷컴 (jongryangjae.com)</td></tr>
<tr><td>운영 방식</td><td>지자체 인증 공식 온라인 쇼핑몰</td></tr>
<tr><td>배송 방식</td><td>택배 배송 (전국 배송 가능)</td></tr>
<tr><td>취급 품목</td><td>일반 쓰레기봉투, 음식물 봉투, 재활용 봉투</td></tr>
<tr><td>결제 수단</td><td>신용카드, 계좌이체, 간편결제(카카오페이, 네이버페이)</td></tr>
<tr><td>최소 주문</td><td>지역별 상이 (일반적으로 1묶음 이상)</td></tr>
</tbody></table>

<h2>종량제닷컴 온라인 주문 방법</h2>
<p>종량제닷컴에서 봉투를 주문하는 방법은 매우 간단합니다. 아래 순서를 따르면 5분 이내에 주문이 완료됩니다.</p>
<ol>
<li><strong>사이트 접속</strong>: jongryangjae.com에 접속합니다.</li>
<li><strong>지역 선택</strong>: 배송받을 주소의 시/도 → 시/군/구를 선택합니다. 지역별로 규격이 다르므로 반드시 실제 사용할 주소 기준으로 선택해야 합니다.</li>
<li><strong>봉투 종류 및 용량 선택</strong>: 일반 쓰레기봉투(5L, 10L, 20L, 30L, 50L, 75L, 100L), 음식물 쓰레기봉투(1L, 2L, 3L, 5L), 재활용 봉투 중 필요한 제품을 선택합니다.</li>
<li><strong>수량 입력 및 장바구니 담기</strong>: 필요한 수량을 입력하고 장바구니에 추가합니다.</li>
<li><strong>배송지 입력 및 결제</strong>: 배송 주소와 연락처를 입력하고 결제를 완료합니다.</li>
<li><strong>배송 대기</strong>: 결제 완료 후 영업일 기준 1~3일 내에 택배로 수령합니다.</li>
</ol>

{cta_block("종량제닷컴 바로 주문하기", "내 지역 규격 종량제봉투를 집까지 배달받으세요", "https://www.jongryangjae.com/", "blue")}

<h2>지역별 종량제봉투 가격 비교</h2>
<p>종량제봉투 가격은 지자체마다 다르며, 같은 지역이라도 봉투 크기에 따라 가격이 달라집니다. 아래는 주요 지역의 일반 쓰레기봉투 대략적인 가격 기준입니다.</p>
<table><thead><tr><th>지역</th><th>10L (10매)</th><th>20L (10매)</th><th>50L (10매)</th></tr></thead><tbody>
<tr><td>서울특별시</td><td>약 4,100원</td><td>약 8,200원</td><td>약 20,500원</td></tr>
<tr><td>경기도 수원시</td><td>약 3,600원</td><td>약 7,200원</td><td>약 18,000원</td></tr>
<tr><td>인천광역시</td><td>약 3,800원</td><td>약 7,600원</td><td>약 19,000원</td></tr>
<tr><td>부산광역시</td><td>약 3,500원</td><td>약 7,000원</td><td>약 17,500원</td></tr>
<tr><td>대구광역시</td><td>약 3,400원</td><td>약 6,800원</td><td>약 17,000원</td></tr>
<tr><td>대전광역시</td><td>약 3,300원</td><td>약 6,600원</td><td>약 16,500원</td></tr>
</tbody></table>
<p style="font-size:13px;color:#666;">※ 위 가격은 참고용이며 지자체 정책에 따라 변동될 수 있습니다. 실제 가격은 종량제닷컴에서 지역 선택 후 확인하세요.</p>

{imgs[1]}

<h2>배달비 및 배송 조건</h2>
<p>종량제닷컴은 택배 배송으로 운영되므로 배달비가 부과됩니다. 다만 일정 금액 이상 구매 시 무료 배송 혜택이 제공됩니다.</p>
<table><thead><tr><th>주문 금액</th><th>배송비</th></tr></thead><tbody>
<tr><td>3만원 미만</td><td>3,000원</td></tr>
<tr><td>3만원 이상</td><td>무료 배송</td></tr>
<tr><td>도서산간 지역</td><td>추가 운임 발생 (3,000~5,000원)</td></tr>
</tbody></table>
<h3>배송 소요 시간</h3>
<ul>
<li><strong>평일 오전 11시 이전 주문</strong>: 당일 출고, 익일 수령 가능</li>
<li><strong>평일 오전 11시 이후 주문</strong>: 다음 날 출고, 2일 후 수령</li>
<li><strong>주말·공휴일 주문</strong>: 다음 영업일 출고</li>
<li><strong>최대 소요 시간</strong>: 도서산간 포함 3~5일</li>
</ul>

<h2>오프라인 구매 vs 온라인 구매 비교</h2>
<table><thead><tr><th>항목</th><th>오프라인 (마트/편의점)</th><th>온라인 (종량제닷컴)</th></tr></thead><tbody>
<tr><td>구매 편의성</td><td>직접 방문 필요</td><td>스마트폰/PC로 간편 주문</td></tr>
<tr><td>가격</td><td>지자체 공정가</td><td>지자체 공정가 + 배송비</td></tr>
<tr><td>구매 가능 시간</td><td>매장 영업 시간 내</td><td>24시간 365일</td></tr>
<tr><td>수량 제한</td><td>소량 구매 가능</td><td>대량 구매에 유리</td></tr>
<tr><td>대기 불필요</td><td>줄 서야 할 수 있음</td><td>기다림 없음</td></tr>
<tr><td>무거운 봉투 운반</td><td>직접 들고 와야 함</td><td>집 앞 배달</td></tr>
</tbody></table>

{cta_block("지금 바로 종량제봉투 주문하기", "무거운 봉투를 직접 들지 않아도 됩니다. 집까지 배달!", "https://www.jongryangjae.com/", "green")}

{imgs[2]}

<h2>종량제닷컴 이용 시 주의사항</h2>
<ul>
<li><strong>지역 규격 확인 필수</strong>: 타 지역 봉투는 사용 불가능합니다. 반드시 사용할 지역을 정확히 선택하세요.</li>
<li><strong>음식물 봉투 별도 주문</strong>: 일반 쓰레기봉투와 음식물 쓰레기봉투는 별도로 주문해야 합니다.</li>
<li><strong>이사 시 주의</strong>: 이사 후에는 새 주소 기준의 봉투를 주문해야 합니다. 이전 지역 봉투는 새 지역에서 사용 불가합니다.</li>
<li><strong>반품 불가</strong>: 봉투 특성상 개봉 후에는 반품이 어렵습니다. 수량을 신중히 결정하세요.</li>
<li><strong>배송 주소 재확인</strong>: 지자체 규격 매칭은 배송지 주소 기준이므로 정확한 주소 입력이 중요합니다.</li>
</ul>

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 종량제닷컴에서 파는 봉투는 공식 인증 봉투인가요?</h3>
<p>A. 네, 종량제닷컴에서 판매하는 봉투는 각 지자체에서 인증한 <strong>공식 규격 봉투</strong>입니다. 가짜 봉투로 인한 과태료 걱정 없이 안심하고 사용하실 수 있습니다.</p>
<h3>Q. 아파트 단지에 거주하는데 배달이 되나요?</h3>
<p>A. 네, 아파트를 포함한 전국 모든 주거지에 배달됩니다. 택배 수령 방식과 동일하게 문 앞 또는 택배함에 수령하시면 됩니다.</p>
<h3>Q. 주문한 지역이 다른 봉투가 오면 어떻게 하나요?</h3>
<p>A. 고객센터에 즉시 연락하시면 됩니다. 종량제닷컴은 지역 규격 오배송 시 <strong>무료 교환</strong>을 원칙으로 합니다.</p>
<h3>Q. 법인이나 사업체도 대량 주문이 가능한가요?</h3>
<p>A. 가능합니다. 대량 주문 시 고객센터를 통해 별도 견적을 요청하시면 <strong>기업 할인 혜택</strong>을 받으실 수 있습니다.</p>
<h3>Q. 배달비를 아끼려면 얼마나 사야 하나요?</h3>
<p>A. <strong>3만원 이상</strong> 구매하시면 무료 배송 혜택이 적용됩니다. 가족이나 이웃과 함께 주문해 배송비를 나누는 것도 좋은 방법입니다.</p>

{cta_block("종량제닷컴에서 우리 지역 봉투 확인하기", "지역 선택 후 정확한 가격과 봉투 종류를 확인하세요", "https://www.jongryangjae.com/", "yellow")}

<h2>마무리</h2>
<p>종량제닷컴은 무거운 봉투를 직접 사러 나가지 않아도 되는 편리한 서비스입니다. 특히 대량으로 구매할 때는 3만원 이상 주문으로 무료 배송 혜택까지 누릴 수 있어 오프라인보다 훨씬 합리적입니다. 지역 규격만 정확히 확인한다면 종량제닷컴을 통해 시간과 수고를 크게 절약할 수 있습니다. 오늘 바로 이용해보세요.</p>'''
    },

    # 2. 종량제봉투 편의점
    {
        "title": "종량제봉투 편의점 판매 가격 종류 구매 방법 2026 총정리",
        "cat": 13,
        "slug": "waste-bag-convenience-store-2026",
        "images": [
            ("photo-1604187351574-c75ca79f5807", "편의점 종량제봉투 구매"),
            ("photo-1558618666-fcd25c85f82e", "종량제봉투 종류 및 크기"),
            ("photo-1532996122724-e3c354a0b15b", "편의점 재활용 봉투"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">급하게 <strong>종량제봉투</strong>가 필요할 때 가장 먼저 떠오르는 곳이 바로 <strong>편의점</strong>입니다. CU, GS25, 세븐일레븐, 이마트24 등 전국 편의점에서 종량제봉투를 판매하고 있지만, 모든 편의점에서 파는 것은 아니고 취급하는 크기와 가격도 매장마다 다릅니다. 이 글에서는 2026년 기준 편의점 종량제봉투 판매 현황, 가격, 구매 팁을 상세하게 정리합니다.</p>

{imgs[0]}

<h2>편의점에서 종량제봉투를 파는 이유</h2>
<p>종량제봉투는 지방자치단체가 관리하는 공공재이지만, 주민 편의를 위해 지자체가 지정한 판매처(마트, 편의점, 슈퍼마켓 등)를 통해 유통됩니다. 편의점은 24시간 운영이라는 장점 덕분에 야간이나 주말에 봉투가 갑자기 필요할 때 매우 유용합니다.</p>

<h2>편의점 브랜드별 종량제봉투 판매 현황</h2>
<table><thead><tr><th>편의점</th><th>판매 여부</th><th>취급 봉투 종류</th><th>비고</th></tr></thead><tbody>
<tr><td>CU (씨유)</td><td>O (대부분 매장)</td><td>일반, 음식물</td><td>지역에 따라 재고 상이</td></tr>
<tr><td>GS25</td><td>O (대부분 매장)</td><td>일반, 음식물</td><td>일부 매장 미취급</td></tr>
<tr><td>세븐일레븐</td><td>O (대부분 매장)</td><td>일반, 음식물</td><td>소용량 중심</td></tr>
<tr><td>이마트24</td><td>O (일부 매장)</td><td>일반</td><td>매장별 차이 큼</td></tr>
<tr><td>미니스톱</td><td>△ (일부 매장)</td><td>일반</td><td>취급 매장 적음</td></tr>
</tbody></table>
<p>편의점에서 종량제봉투를 판매하려면 해당 지자체에 신고하고 봉투를 공급받아야 합니다. 따라서 같은 브랜드 편의점이라도 지역이나 매장에 따라 판매 여부가 다를 수 있습니다.</p>

{cta_block("종량제봉투 온라인 주문하기", "편의점에 재고가 없다면 집까지 배달받으세요", "https://www.jongryangjae.com/", "blue")}

<h2>편의점 종량제봉투 가격 (2026년 기준)</h2>
<p>봉투 가격은 지자체가 결정하므로 동일 브랜드 편의점이라도 지역별로 가격이 다릅니다. 아래는 서울 기준 대략적인 편의점 판매 가격입니다.</p>
<table><thead><tr><th>봉투 종류</th><th>용량</th><th>판매 단위</th><th>서울 기준 가격</th></tr></thead><tbody>
<tr><td>일반 쓰레기봉투</td><td>5L</td><td>5매</td><td>약 1,050원</td></tr>
<tr><td>일반 쓰레기봉투</td><td>10L</td><td>5매</td><td>약 2,050원</td></tr>
<tr><td>일반 쓰레기봉투</td><td>20L</td><td>5매</td><td>약 4,100원</td></tr>
<tr><td>일반 쓰레기봉투</td><td>30L</td><td>5매</td><td>약 6,150원</td></tr>
<tr><td>음식물 쓰레기봉투</td><td>1L</td><td>10매</td><td>약 900원</td></tr>
<tr><td>음식물 쓰레기봉투</td><td>2L</td><td>10매</td><td>약 1,800원</td></tr>
<tr><td>음식물 쓰레기봉투</td><td>3L</td><td>10매</td><td>약 2,700원</td></tr>
</tbody></table>
<p style="font-size:13px;color:#666;">※ 위 가격은 서울시 기준이며 지역에 따라 다를 수 있습니다. 구체적인 가격은 해당 매장에서 확인하세요.</p>

{imgs[1]}

<h2>편의점에서 판매하는 봉투 종류</h2>
<h3>일반 쓰레기봉투 (검정/불투명)</h3>
<p>음식물, 재활용품을 제외한 생활쓰레기를 담는 봉투입니다. 지자체마다 색상과 디자인이 다르며, 불투명한 소재로 만들어집니다. 편의점에서는 주로 <strong>5L, 10L, 20L</strong> 소용량이 많습니다.</p>
<h3>음식물 쓰레기봉투 (초록/분홍)</h3>
<p>음식물 쓰레기 전용 봉투로, 납부필증이 포함된 규격 봉투입니다. <strong>1L, 2L, 3L</strong> 소용량 위주로 판매됩니다. 지역에 따라 납부필증 스티커 방식이나 RFID 방식을 사용하기도 합니다.</p>
<h3>재활용 봉투 (투명)</h3>
<p>투명 봉투에 재활용품을 분리하여 담는 봉투입니다. 지자체에 따라 유료 또는 무료로 제공되며, 편의점 취급 여부는 지역마다 다릅니다.</p>

<h2>편의점에서 종량제봉투를 못 살 때 대처법</h2>
<ul>
<li><strong>다른 편의점 방문</strong>: 같은 브랜드라도 인근 다른 매장에 재고가 있을 수 있습니다.</li>
<li><strong>슈퍼마켓/마트 방문</strong>: 동네 슈퍼마켓이나 대형마트 생활용품 코너를 방문하세요.</li>
<li><strong>주민센터</strong>: 행정복지센터(주민센터)에서도 종량제봉투를 판매합니다 (평일 업무시간 내).</li>
<li><strong>온라인 주문</strong>: 종량제닷컴 등 온라인 쇼핑몰에서 주문하면 1~3일 내 배달받을 수 있습니다.</li>
</ul>

{cta_block("내 주변 봉투 판매처 찾기", "주민센터 및 인근 판매처에서도 구매 가능합니다", "https://www.jongryangjae.com/", "yellow")}

{imgs[2]}

<h2>편의점 종량제봉투 구매 꿀팁</h2>
<ul>
<li><strong>앱으로 재고 확인</strong>: CU나 GS25 앱에서 특정 카테고리 상품 취급 여부를 확인할 수 있습니다.</li>
<li><strong>대용량은 마트나 온라인 추천</strong>: 50L, 75L, 100L 등 대용량 봉투는 편의점에서 취급하지 않는 경우가 많습니다. 이런 경우 대형마트나 온라인 주문을 이용하세요.</li>
<li><strong>이사 후 지역 확인 필수</strong>: 이사 후에는 새 지역 규격 봉투를 구매해야 합니다. 이전 지역 봉투를 사용하면 수거 거부될 수 있습니다.</li>
<li><strong>영수증 보관</strong>: 봉투 구매 시 영수증을 보관하면 환불이나 교환 시 유용합니다.</li>
<li><strong>포인트 적립</strong>: 편의점 멤버십 포인트(CU 포켓씨유, GS25 나만의냉장고 등)가 적립되므로 앱 연동 후 구매하세요.</li>
</ul>

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 모든 편의점에서 종량제봉투를 파나요?</h3>
<p>A. 아닙니다. 종량제봉투는 지자체 허가를 받은 매장에서만 판매할 수 있습니다. 같은 브랜드 편의점이라도 허가를 받지 않은 매장에서는 판매하지 않습니다. 방문 전 전화로 확인하는 것이 좋습니다.</p>
<h3>Q. 편의점에서 구매한 봉투가 찢어졌는데 교환되나요?</h3>
<p>A. 제품 불량의 경우 구매 매장에서 영수증과 함께 교환을 요청할 수 있습니다. 단, 사용 후 훼손된 경우는 교환이 어렵습니다.</p>
<h3>Q. 야간(밤 12시 이후)에도 구매 가능한가요?</h3>
<p>A. 편의점은 24시간 운영하므로 새벽이나 심야에도 구매할 수 있습니다. 다만 재고가 소진된 경우 구매가 어려울 수 있으니, 급한 경우 여러 매장을 확인해보세요.</p>
<h3>Q. 타 지역 종량제봉투를 우리 동네에서 쓸 수 있나요?</h3>
<p>A. <strong>안 됩니다.</strong> 종량제봉투는 지자체별 규격이 다르며, 해당 지역 봉투가 아니면 수거원이 수거를 거부할 수 있습니다. 반드시 거주 지역에 맞는 봉투를 사용하세요.</p>

{cta_block("종량제닷컴에서 대량 주문하기", "편의점에서 자주 사기 번거롭다면 온라인 대량 주문이 편리합니다", "https://www.jongryangjae.com/", "green")}

<h2>마무리</h2>
<p>편의점은 24시간 언제든지 소량의 종량제봉투를 구매할 수 있는 가장 편리한 방법입니다. 하지만 대용량이나 대량 구매가 필요하다면 온라인 주문이 더 합리적입니다. 내 거주 지역에 맞는 정확한 봉투를 구매하는 것이 가장 중요하며, 편의점에 재고가 없을 경우 주민센터나 온라인 쇼핑몰을 적극 활용해보세요.</p>'''
    },

    # 3. 민생지원금 3차
    {
        "title": "민생지원금 3차 신청방법 지급일 대상자 조건 2026 총정리",
        "cat": 13,
        "slug": "livelihood-support-fund-3rd-2026",
        "images": [
            ("photo-1554224155-6726b3ff858f", "민생지원금 신청 안내"),
            ("photo-1556742049-0cfed4f6a45d", "민생지원금 지급 확인"),
            ("photo-1450101499163-c8848c66ca85", "민생지원금 신청 서류"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">2026년 <strong>민생지원금 3차</strong> 지급 계획이 발표되면서 많은 국민들이 신청 자격과 방법에 대해 궁금해하고 있습니다. 민생지원금은 경기 침체와 물가 상승으로 어려움을 겪는 서민과 취약계층을 지원하기 위한 <strong>정부 지원 정책</strong>입니다. 이 글에서는 민생지원금 3차 지급 대상, 신청 조건, 신청 방법, 지급일, 금액, 지급 현황 조회 방법 등을 빠짐없이 정리합니다.</p>

{imgs[0]}

<h2>민생지원금 3차란?</h2>
<p>민생지원금은 코로나19 이후 지속되는 경기 침체와 고물가로 인한 서민 생활의 어려움을 완화하기 위해 정부가 지급하는 현금성 지원금입니다. 1차(2021년), 2차(2022~2023년)에 이어 <strong>3차 민생지원금</strong>이 2026년에 시행될 예정입니다.</p>
<table><thead><tr><th>구분</th><th>내용</th></tr></thead><tbody>
<tr><td>사업명</td><td>민생지원금 3차 (민생회복 국민지원금)</td></tr>
<tr><td>지급 목적</td><td>고물가·경기 침체 대응, 서민 생활 안정</td></tr>
<tr><td>지급 방식</td><td>신용카드·체크카드 포인트, 지역사랑상품권</td></tr>
<tr><td>사용 가능 기간</td><td>지급일로부터 3개월 이내</td></tr>
<tr><td>사용 가능 업종</td><td>소상공인 및 중소기업 사업장 (대형마트, 백화점, 온라인몰 제외)</td></tr>
</tbody></table>

<h2>민생지원금 3차 지급 대상 및 조건</h2>
<p>민생지원금 3차는 소득 및 재산 기준을 충족하는 가구에 지급됩니다. 구체적인 기준은 정부 발표에 따라 확정되지만, 현재까지 알려진 예상 기준은 다음과 같습니다.</p>
<h3>지급 대상 (예상 기준)</h3>
<ul>
<li><strong>기초생활수급자 및 차상위계층</strong>: 전액 지원 (1인 기준 약 25만원)</li>
<li><strong>건강보험료 하위 80% 이하 가구</strong>: 1인당 약 15~25만원</li>
<li><strong>한부모가족, 장애인 가구</strong>: 추가 지원 가능성 있음</li>
</ul>
<h3>건강보험료 기준표 (2026년 예상)</h3>
<table><thead><tr><th>가구원 수</th><th>직장가입자 월 보험료</th><th>지역가입자 월 보험료</th></tr></thead><tbody>
<tr><td>1인 가구</td><td>88,000원 이하</td><td>46,000원 이하</td></tr>
<tr><td>2인 가구</td><td>150,000원 이하</td><td>130,000원 이하</td></tr>
<tr><td>3인 가구</td><td>195,000원 이하</td><td>175,000원 이하</td></tr>
<tr><td>4인 가구</td><td>240,000원 이하</td><td>215,000원 이하</td></tr>
<tr><td>5인 이상</td><td>280,000원 이하</td><td>250,000원 이하</td></tr>
</tbody></table>
<p style="font-size:13px;color:#666;">※ 건강보험료 기준은 정부 최종 발표에 따라 달라질 수 있습니다. 복지로에서 최신 정보를 확인하세요.</p>

{cta_block("복지로에서 신청 자격 확인하기", "내 가구의 민생지원금 수급 자격을 바로 확인하세요", "https://www.bokjiro.go.kr/", "blue")}

{imgs[1]}

<h2>민생지원금 3차 신청 방법</h2>
<p>민생지원금은 온라인과 오프라인 두 가지 방법으로 신청할 수 있습니다. 온라인 신청 시 신속하게 처리되므로 온라인 신청을 권장합니다.</p>
<h3>온라인 신청 방법</h3>
<ol>
<li><strong>복지로 접속</strong>: www.bokjiro.go.kr 접속 또는 복지로 앱 실행</li>
<li><strong>본인 인증</strong>: 공동인증서, 간편인증(카카오, 네이버, PASS 앱 등)으로 로그인</li>
<li><strong>서비스 신청</strong> 클릭 → <strong>민생지원금</strong> 선택</li>
<li><strong>가구원 정보 및 건강보험료 정보</strong> 자동 연동 확인</li>
<li><strong>지급 수단 선택</strong>: 신용카드/체크카드 또는 지역사랑상품권 중 선택</li>
<li><strong>신청 완료</strong> 후 결과 문자 수신 (2~3 영업일 이내)</li>
</ol>
<h3>오프라인 신청 방법</h3>
<ol>
<li>주소지 관할 <strong>읍·면·동 주민센터</strong> 방문</li>
<li>신분증 지참 (주민등록증, 운전면허증, 여권 등)</li>
<li>신청서 작성 및 제출</li>
<li>지급 수단(카드 또는 상품권) 선택</li>
</ol>

<h2>민생지원금 3차 지급일 및 지급 금액</h2>
<table><thead><tr><th>신청 기간</th><th>지급 예상 시기</th><th>지급 금액 (1인)</th></tr></thead><tbody>
<tr><td>1주차 신청자</td><td>신청 후 3~5 영업일 이내</td><td>기초·차상위: 25만원</td></tr>
<tr><td>2주차 신청자</td><td>신청 후 3~5 영업일 이내</td><td>일반: 15~20만원</td></tr>
<tr><td>사후 신청</td><td>신청 마감 후 일괄 지급</td><td>동일</td></tr>
</tbody></table>
<h3>지급 수단별 사용 방법</h3>
<ul>
<li><strong>신용/체크카드 포인트</strong>: 카드사 앱 또는 홈페이지에서 포인트 전환 후 사용. 가맹점에서 결제 시 자동 차감</li>
<li><strong>지역사랑상품권</strong>: 모바일 상품권(제로페이, 지역페이 앱)으로 수령. 해당 지역 내 가맹점에서만 사용 가능</li>
</ul>

{cta_block("민생지원금 신청 바로가기", "복지로에서 간편하게 신청하고 빠르게 지급받으세요", "https://www.bokjiro.go.kr/", "yellow")}

{imgs[2]}

<h2>지급 현황 조회 방법</h2>
<p>신청 후 지급 현황은 다음 방법으로 확인할 수 있습니다.</p>
<ul>
<li><strong>복지로 홈페이지/앱</strong>: 로그인 → 나의 서비스 → 신청내역 조회</li>
<li><strong>문자 메시지</strong>: 신청 완료 및 지급 확정 시 등록 휴대폰으로 문자 발송</li>
<li><strong>카드사 앱</strong>: 카드 포인트 선택 시 카드사 앱에서 포인트 잔액 확인</li>
<li><strong>주민센터 문의</strong>: 직접 방문 또는 전화 문의 가능</li>
</ul>

<h2>민생지원금 3차 관련 주의사항</h2>
<ul>
<li><strong>신청 기간 엄수</strong>: 신청 기간이 종료되면 지급받을 수 없습니다. 공지 즉시 신청을 완료하세요.</li>
<li><strong>대형마트·온라인몰 사용 불가</strong>: 민생지원금은 소상공인 지원 목적이므로 이마트, 롯데마트, 쿠팡, 네이버쇼핑 등에서는 사용할 수 없습니다.</li>
<li><strong>사용 기한 확인</strong>: 지급일로부터 3개월 이내 사용해야 하며, 기한 초과 시 소멸됩니다.</li>
<li><strong>사기 주의</strong>: 정부는 문자나 전화로 개인정보나 계좌번호를 요구하지 않습니다. 관련 연락이 오면 보이스피싱을 의심하세요.</li>
</ul>

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 민생지원금 3차는 언제 신청할 수 있나요?</h3>
<p>A. 정부의 공식 발표에 따라 신청 기간이 확정됩니다. 복지로 홈페이지 공지사항이나 정부 보도자료를 통해 최신 일정을 확인하세요. 일반적으로 <strong>예산 국회 통과 후 1~2개월 이내</strong>에 신청이 시작됩니다.</p>
<h3>Q. 전 가족이 각각 신청해야 하나요?</h3>
<p>A. <strong>가구 단위</strong>가 아닌 개인 단위로 지급하는 경우 각자 신청이 필요합니다. 구체적인 신청 단위는 정부 발표를 확인하세요.</p>
<h3>Q. 직장가입자인데 자격이 되나요?</h3>
<p>A. 건강보험료 기준을 충족하면 직장가입자도 신청 가능합니다. 직장가입자는 직장보험료 기준을, 지역가입자는 지역보험료 기준을 적용합니다.</p>
<h3>Q. 신청 후 탈락 통보를 받으면 어떻게 하나요?</h3>
<p>A. 이의신청이 가능합니다. 통보서에 기재된 이의신청 방법 또는 주민센터를 통해 이의를 제기할 수 있으며, 결과는 1~2주 내에 통보됩니다.</p>

{cta_block("복지로에서 다른 지원금도 확인하기", "민생지원금 외 내가 받을 수 있는 다양한 복지 혜택을 확인하세요", "https://www.bokjiro.go.kr/", "green")}

<h2>마무리</h2>
<p>민생지원금 3차는 고물가와 경기 침체로 어려운 가계에 실질적인 도움이 되는 제도입니다. 신청 기간을 놓치지 않도록 복지로 공지사항을 수시로 확인하고, 자격 조건에 해당된다면 빠르게 신청하여 혜택을 받으세요. 사용 기한도 꼭 확인해서 소멸되는 일이 없도록 하세요.</p>'''
    },

    # 4. 공시가격 알리미
    {
        "title": "공시가격 알리미 조회 방법 아파트 공시지가 확인 2026 총정리",
        "cat": 8,
        "slug": "official-land-price-check-2026",
        "images": [
            ("photo-1560518883-ce09059eeffa", "아파트 공시가격 확인"),
            ("photo-1564013799919-ab600027ffc6", "부동산 공시지가 조회"),
            ("photo-1486406146926-c627a92ad1ab", "공시가격 세금 계산"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">2026년 공동주택 공시가격이 발표되면서 <strong>공시가격 알리미</strong>를 통한 조회가 급증하고 있습니다. 공시가격은 재산세, 종합부동산세(종부세), 건강보험료 등 각종 세금과 부담금의 기준이 되기 때문에 내 집 공시가격이 얼마인지 반드시 확인해야 합니다. 이 글에서는 공시가격 알리미 조회 방법, 공시가격이 미치는 영향, 이의신청 방법, 2026년 주요 변경 사항을 상세히 설명합니다.</p>

{imgs[0]}

<h2>공시가격 알리미란?</h2>
<p><strong>공시가격 알리미(realtyprice.kr)</strong>는 국토교통부가 운영하는 공식 부동산 공시가격 조회 시스템입니다. 공동주택(아파트, 연립, 다세대), 단독주택, 토지(표준지) 공시가격을 누구나 무료로 조회할 수 있습니다.</p>
<table><thead><tr><th>구분</th><th>내용</th></tr></thead><tbody>
<tr><td>운영 기관</td><td>국토교통부</td></tr>
<tr><td>웹사이트</td><td>www.realtyprice.kr</td></tr>
<tr><td>조회 가능 항목</td><td>공동주택, 단독주택, 표준지 공시지가</td></tr>
<tr><td>공시 시기</td><td>공동주택: 매년 4월 말 / 단독주택: 매년 1월 말</td></tr>
<tr><td>열람 기간</td><td>공시일로부터 이의신청 기간 포함 상시 열람 가능</td></tr>
<tr><td>이용 요금</td><td>무료</td></tr>
</tbody></table>

<h2>공시가격 알리미 조회 방법</h2>
<p>공시가격 알리미에서 내 집의 공시가격을 조회하는 방법은 매우 간단합니다.</p>
<h3>PC에서 조회하기</h3>
<ol>
<li><strong>realtyprice.kr 접속</strong></li>
<li>메인 화면에서 <strong>공동주택 공시가격</strong> 클릭 (아파트 기준)</li>
<li><strong>시/도 → 시/군/구 → 읍/면/동 → 단지명</strong> 순으로 선택</li>
<li>동·호수 선택 후 공시가격 확인</li>
<li>연도별 공시가격 변동 추이도 확인 가능</li>
</ol>
<h3>모바일에서 조회하기</h3>
<ol>
<li>스마트폰 브라우저에서 realtyprice.kr 접속 (앱 없이 이용 가능)</li>
<li>동일한 순서로 주소 검색 후 조회</li>
</ol>

{cta_block("공시가격 알리미 바로 조회하기", "내 아파트·토지 공시가격을 국토교통부 공식 시스템에서 확인하세요", "https://www.realtyprice.kr/", "blue")}

{imgs[1]}

<h2>공시가격이 미치는 영향</h2>
<p>공시가격은 단순한 참고 지표가 아닙니다. 다양한 세금과 부담금 산정의 기준이 됩니다.</p>
<h3>1. 재산세</h3>
<p>재산세는 공시가격에 공정시장가액비율(60%)을 곱한 과세표준을 기반으로 계산됩니다.</p>
<table><thead><tr><th>과세표준</th><th>세율</th></tr></thead><tbody>
<tr><td>6,000만원 이하</td><td>0.1%</td></tr>
<tr><td>6,000만원 초과 ~ 1.5억원</td><td>0.15%</td></tr>
<tr><td>1.5억원 초과 ~ 3억원</td><td>0.25%</td></tr>
<tr><td>3억원 초과</td><td>0.4%</td></tr>
</tbody></table>
<h3>2. 종합부동산세 (종부세)</h3>
<p>1세대 1주택자는 공시가격 <strong>12억원 초과</strong> 시 종부세가 부과됩니다. 다주택자는 합산 공시가격이 <strong>9억원</strong>을 초과하면 과세 대상입니다.</p>
<h3>3. 건강보험료 (지역가입자)</h3>
<p>지역가입자의 경우 재산(공시가격)이 건강보험료 산정에 반영됩니다. 공시가격 상승 시 건강보험료도 인상될 수 있습니다.</p>
<h3>4. 기초연금·기초생활급여 수급 자격</h3>
<p>공시가격은 소득인정액 계산에 포함되어 각종 복지 급여 수급 자격에 영향을 미칩니다.</p>
<h3>5. 취득세</h3>
<p>아파트 취득세는 실제 거래가액을 기준으로 하지만, 공시가격이 취득세 산정에 참고되기도 합니다.</p>

<h2>2026년 공시가격 주요 변경 사항</h2>
<table><thead><tr><th>항목</th><th>2025년</th><th>2026년</th></tr></thead><tbody>
<tr><td>전국 공동주택 공시가격 변동률</td><td>약 +1.5%</td><td>약 +3.2% (예상)</td></tr>
<tr><td>공정시장가액비율 (재산세)</td><td>60%</td><td>60% (유지)</td></tr>
<tr><td>1주택 종부세 기본공제</td><td>12억원</td><td>12억원 (유지)</td></tr>
<tr><td>건보료 재산공제</td><td>5,000만원</td><td>5,000만원 (유지)</td></tr>
</tbody></table>

{cta_block("공시가격 이의신청 안내 확인하기", "공시가격이 불합리하다고 생각되면 이의신청을 통해 재검토를 요청하세요", "https://www.realtyprice.kr/", "yellow")}

{imgs[2]}

<h2>공시가격 이의신청 방법</h2>
<p>공시가격이 실제 시세와 크게 다르다고 판단되면 이의신청을 통해 재검토를 요청할 수 있습니다.</p>
<h3>이의신청 기간</h3>
<ul>
<li><strong>공동주택</strong>: 공시일(4월 말) 이후 30일 이내</li>
<li><strong>단독주택·토지</strong>: 공시일(1월 말) 이후 30일 이내</li>
</ul>
<h3>이의신청 방법</h3>
<ol>
<li><strong>온라인</strong>: 공시가격 알리미(realtyprice.kr) → 이의신청 메뉴</li>
<li><strong>서면</strong>: 국토교통부 또는 해당 지자체 제출</li>
<li><strong>필요 서류</strong>: 이의신청서, 공시가격과의 차이를 입증할 자료 (인근 실거래가, 감정평가서 등)</li>
</ol>
<h3>이의신청 처리 절차</h3>
<p>이의신청 접수 → 감정평가사 현장조사 → 부동산가격공시위원회 심의 → 결과 통보 (약 30~45일 소요)</p>

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 공시가격과 실거래가의 차이는 무엇인가요?</h3>
<p>A. <strong>실거래가</strong>는 실제 매매가 이루어진 가격이며, <strong>공시가격</strong>은 정부가 세금 부과 등을 위해 산정한 가격입니다. 일반적으로 공시가격은 실거래가의 70~80% 수준이지만, 지역과 주택 유형에 따라 차이가 있습니다.</p>
<h3>Q. 공시가격은 언제 바뀌나요?</h3>
<p>A. 공동주택 공시가격은 <strong>매년 4월 말</strong>에, 단독주택은 <strong>매년 1월 말</strong>에 새로 공시됩니다. 공시 전에는 예정 공시가격(안)이 먼저 공개되어 의견 청취 기간을 거칩니다.</p>
<h3>Q. 아파트가 아닌 토지 공시가격도 조회 가능한가요?</h3>
<p>A. 네, 공시가격 알리미에서 <strong>표준지 공시지가</strong>와 <strong>개별공시지가</strong>를 모두 조회할 수 있습니다. 개별공시지가는 해당 시·군·구청 홈페이지에서도 확인 가능합니다.</p>
<h3>Q. 종부세 기준이 되는 공시가격은 어느 시점 기준인가요?</h3>
<p>A. 매년 <strong>6월 1일 기준</strong>으로 보유한 주택의 공시가격이 종부세 과세 기준이 됩니다. 6월 2일 이후 매도하면 해당 연도 종부세를 납부해야 합니다.</p>

{cta_block("공시가격 알리미에서 내 집 조회하기", "2026년 최신 공시가격을 확인하고 세금 계획을 세우세요", "https://www.realtyprice.kr/", "green")}

<h2>마무리</h2>
<p>공시가격 알리미는 재산세, 종부세, 건강보험료 등 각종 세금의 기준이 되는 공시가격을 누구나 무료로 확인할 수 있는 필수 서비스입니다. 매년 4월 공시 이후 반드시 내 집의 공시가격을 확인하고, 불합리하다고 판단되면 이의신청 기간 내에 신청하세요. 공시가격 파악이 합리적인 세금 계획의 첫걸음입니다.</p>'''
    },

    # 5. 화물 유가보조금
    {
        "title": "화물 유가보조금 신청방법 지급 조건 카드 사용법 2026 총정리",
        "cat": 13,
        "slug": "freight-fuel-subsidy-2026",
        "images": [
            ("photo-1601584115197-04ecc0da31d7", "화물차 유가보조금 주유"),
            ("photo-1558618047-3c8c76ca7d13", "화물 운송 트럭"),
            ("photo-1556742049-0cfed4f6a45d", "유가보조금 지급 카드"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">고유가 시대에 화물운송 종사자들의 부담을 덜어주기 위한 <strong>화물 유가보조금</strong> 제도가 2026년에도 계속 운영됩니다. 화물차를 운행하는 운송사업자라면 반드시 알아야 할 유가보조금 신청 자격, 신청 방법, 보조금 계산 방법, 유류구매카드 사용법, 지급 일정까지 모두 정리합니다.</p>

{imgs[0]}

<h2>화물 유가보조금이란?</h2>
<p><strong>화물 유가보조금</strong>은 국제 유가 상승으로 인한 화물운송 원가 부담을 완화하기 위해 정부가 화물자동차 운송사업자에게 지급하는 보조금입니다. 경유(디젤) 가격이 기준가격을 초과하는 부분에 대해 일정 비율을 보전해주는 방식입니다.</p>
<table><thead><tr><th>구분</th><th>내용</th></tr></thead><tbody>
<tr><td>근거 법령</td><td>화물자동차 운수사업법 제43조</td></tr>
<tr><td>관할 부처</td><td>국토교통부</td></tr>
<tr><td>지급 방식</td><td>유류구매카드를 통한 자동 정산</td></tr>
<tr><td>기준 유가</td><td>리터당 1,850원 (경유 기준, 변동 가능)</td></tr>
<tr><td>보조율</td><td>기준 초과액의 50% (차종별 상이)</td></tr>
<tr><td>지급 주기</td><td>주유 후 약 2~3 영업일 내 카드 포인트 적립</td></tr>
</tbody></table>

<h2>화물 유가보조금 지급 대상 (자격 조건)</h2>
<p>다음 조건을 모두 충족하는 경우에만 화물 유가보조금을 지급받을 수 있습니다.</p>
<h3>기본 요건</h3>
<ul>
<li><strong>화물자동차 운송사업 허가</strong>를 보유한 사업자 (개인 화물차주 포함)</li>
<li>유효한 <strong>화물자동차 운송사업 허가증</strong> 소지</li>
<li><strong>경유를 연료로 사용</strong>하는 화물자동차 운행</li>
<li><strong>유류구매카드(화물복지카드)</strong> 발급 완료</li>
</ul>
<h3>지원 대상 차종</h3>
<table><thead><tr><th>차종 구분</th><th>총중량</th><th>주요 해당 차량</th></tr></thead><tbody>
<tr><td>소형 화물차</td><td>1톤 미만</td><td>다마스, 라보 등</td></tr>
<tr><td>중형 화물차</td><td>1~5톤</td><td>포터, 봉고3, 마이티 등</td></tr>
<tr><td>대형 화물차</td><td>5톤 이상</td><td>트레일러, 카고트럭 등</td></tr>
<tr><td>특수차</td><td>-</td><td>냉동탑차, 리프트차 등</td></tr>
</tbody></table>
<p style="font-size:13px;color:#666;">※ 렌트 또는 리스 차량도 실제 운행자가 화물운송사업자인 경우 신청 가능합니다.</p>

{cta_block("화물 유가보조금 신청 안내 확인하기", "도로교통공단에서 유가보조금 신청 자격과 절차를 확인하세요", "https://www.koroad.or.kr/", "blue")}

{imgs[1]}

<h2>화물 유가보조금 신청 방법</h2>
<p>유가보조금을 받으려면 먼저 <strong>유류구매카드(화물복지카드)</strong>를 발급받아야 합니다. 카드 발급 후에는 별도 신청 없이 가맹 주유소에서 카드로 주유하면 자동으로 보조금이 정산됩니다.</p>
<h3>유류구매카드 발급 절차</h3>
<ol>
<li><strong>신청 기관 방문 또는 온라인 접수</strong>: 한국도로공사, 화물운송협회, 카드사(신한, 하나, BC 등) 중 선택</li>
<li><strong>필요 서류 제출</strong>
  <ul>
    <li>화물자동차 운송사업 허가증</li>
    <li>자동차등록증</li>
    <li>신분증</li>
    <li>사업자등록증 (사업자의 경우)</li>
  </ul>
</li>
<li><strong>카드 발급 신청</strong>: 신청서 작성 후 제출 (온라인 또는 방문)</li>
<li><strong>카드 수령</strong>: 발급 완료 후 등록 주소로 우편 발송 (7~10 영업일)</li>
<li><strong>카드 등록</strong>: 카드사 앱 또는 홈페이지에서 차량 정보 등록</li>
</ol>

<h2>유류구매카드 사용 방법</h2>
<p>카드 발급 후 사용 방법은 간단합니다. 가맹 주유소를 방문하여 화물복지카드로 결제하면 됩니다.</p>
<h3>주유 절차</h3>
<ol>
<li><strong>가맹 주유소 확인</strong>: 카드사 앱 또는 오피넷(www.opinet.co.kr)에서 가맹 주유소 조회</li>
<li><strong>카드 제시</strong>: 주유 시 화물복지카드를 제시하거나 카드 단말기에 삽입</li>
<li><strong>주유량 입력</strong> (일부 주유소): 실제 주유한 리터수를 단말기에 입력</li>
<li><strong>결제 완료</strong>: 경유 가격에서 보조금을 제외한 금액만 결제</li>
<li><strong>보조금 확인</strong>: 카드사 앱에서 주유 후 적립된 보조금 포인트 확인</li>
</ol>

<h2>유가보조금 지급 금액 계산 방법</h2>
<p>유가보조금은 <strong>기준가격 초과분의 일정 비율</strong>을 지급합니다.</p>
<table><thead><tr><th>경유 실제가</th><th>기준가 (1,850원)</th><th>초과분</th><th>보조율(50%)</th><th>리터당 보조금</th></tr></thead><tbody>
<tr><td>1,950원</td><td>1,850원</td><td>100원</td><td>50%</td><td>50원</td></tr>
<tr><td>2,050원</td><td>1,850원</td><td>200원</td><td>50%</td><td>100원</td></tr>
<tr><td>2,200원</td><td>1,850원</td><td>350원</td><td>50%</td><td>175원</td></tr>
</tbody></table>
<h3>월 예상 보조금 계산 예시</h3>
<p>월 주유량 500L, 경유 단가 2,050원 기준:</p>
<ul>
<li>리터당 보조금: (2,050 - 1,850) × 50% = <strong>100원</strong></li>
<li>월 보조금: 500L × 100원 = <strong>50,000원</strong></li>
</ul>

{cta_block("유류구매카드 발급 신청하기", "도로교통공단에서 화물복지카드를 발급받고 보조금을 받으세요", "https://www.koroad.or.kr/", "yellow")}

{imgs[2]}

<h2>유가보조금 지급 일정</h2>
<p>유가보조금은 주유 후 자동으로 카드에 적립되며, 별도 지급일 없이 실시간으로 정산됩니다.</p>
<ul>
<li><strong>즉시 적립형</strong>: 주유 결제 시 보조금이 실시간 차감 또는 포인트로 즉시 적립</li>
<li><strong>사후 정산형</strong>: 주유 후 2~3 영업일 내 카드 포인트로 적립</li>
<li><strong>월별 정산형</strong>: 일부 카드사의 경우 월 말 일괄 정산 후 다음 달 지급</li>
</ul>
<p>구체적인 정산 방식은 발급받은 카드사에 따라 다르므로, 카드사 고객센터 또는 앱에서 확인하세요.</p>

<h2>유가보조금 부정 수급 주의사항</h2>
<ul>
<li><strong>타인 명의 카드 사용 불가</strong>: 본인 명의 차량에 한해 사용 가능하며, 타인 카드 사용은 보조금 환수 및 허가 취소 대상</li>
<li><strong>비가맹 주유소 사용 시 보조금 미지급</strong></li>
<li><strong>주유량 조작 금지</strong>: 실제 주유량을 초과 입력하면 사기 처벌 대상</li>
<li><strong>영업 미운행 기간 신고 의무</strong>: 장기 미운행 시 관할 관청에 신고해야 함</li>
</ul>

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 개인 화물차주(지입차주)도 신청할 수 있나요?</h3>
<p>A. 네, 화물자동차 운송사업 허가를 보유한 개인 사업자(지입차주 포함)도 유가보조금 신청이 가능합니다. 허가증과 자동차등록증을 가지고 카드사 또는 화물운송협회에 방문하세요.</p>
<h3>Q. 경유가 아닌 LNG나 CNG 차량도 보조금을 받나요?</h3>
<p>A. LNG 및 CNG를 연료로 사용하는 화물차도 별도 유가보조금 지원이 있습니다. 경유 차량과 기준이 다르므로 관할 기관에 별도 문의가 필요합니다.</p>
<h3>Q. 유가보조금을 과거 기간 소급 신청할 수 있나요?</h3>
<p>A. 유가보조금은 카드 사용 시점부터 적용되며, <strong>카드 발급 이전 주유분은 소급 신청이 불가</strong>합니다. 가능한 빨리 카드를 발급받으세요.</p>
<h3>Q. 보조금이 잘못 지급된 경우 어떻게 하나요?</h3>
<p>A. 카드사 고객센터 또는 화물운송협회에 문의하여 수정 정산을 요청할 수 있습니다. 과지급된 경우 자동 환수 또는 다음 주유 시 차감될 수 있습니다.</p>
<h3>Q. 카드를 분실하면 어떻게 하나요?</h3>
<p>A. 즉시 카드사 고객센터에 분실 신고 후 이용 정지시키세요. 이후 재발급을 신청하면 되며, 재발급 시에도 차량 정보 재등록이 필요합니다.</p>

{cta_block("도로교통공단에서 유가보조금 자세히 알아보기", "유가보조금 관련 최신 정보와 신청 안내를 확인하세요", "https://www.koroad.or.kr/", "green")}

<h2>마무리</h2>
<p>화물 유가보조금은 화물운송 종사자라면 반드시 챙겨야 할 중요한 지원 제도입니다. 유류구매카드만 발급받으면 별도 신청 없이 주유 시마다 자동으로 보조금이 지급되므로, 아직 카드를 발급받지 않은 사업자라면 지금 바로 신청하세요. 연간 수십만 원의 연료비 절감 효과를 누릴 수 있습니다.</p>'''
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

        # 2) 콘텐츠 생성
        content = post["content"](img_htmls)

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

    # 4) 네이버 인덱싱
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

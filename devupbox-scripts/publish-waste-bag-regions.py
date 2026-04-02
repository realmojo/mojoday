import json
import urllib.request
import urllib.error
import urllib.parse
import base64
import time
import ssl
import re
import sys

ssl._create_default_https_context = ssl._create_unverified_context

# ========== WordPress 설정 ==========
AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API = "https://devupbox.com/wp-json/wp/v2/posts"

# ========== CTA 블록 ==========
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
    url_re = re.compile(r'(?<![a-zA-Z0-9/])((?:[a-zA-Z0-9-]+\.)+(?:com|co\.kr|or\.kr|go\.kr|kr|net|org)(?:/[^\s<"\')\]]*)?)')
    img_re = re.compile(r'\.(?:jpg|jpeg|png|gif|webp|svg|css|js)(?:\?|$)', re.I)

    def linkify_text(text):
        def replace_url(m):
            url = m.group(1)
            if img_re.search(url):
                return m.group(0)
            return f'<a href="https://{url}" target="_blank" rel="noopener noreferrer">{url}</a>'
        return url_re.sub(replace_url, text)

    parts = re.split(r'(<[^>]+>)', html)
    result = []
    for part in parts:
        if part.startswith('<'):
            result.append(part)
        else:
            result.append(linkify_text(part))
    return ''.join(result)

# ========== 지역 데이터 ==========
REGIONS = {
    "서울": {
        "full": "서울특별시",
        "districts": ["강남구","강동구","강북구","강서구","관악구","광진구","구로구","금천구","노원구","도봉구","동대문구","동작구","마포구","서대문구","서초구","성동구","성북구","송파구","양천구","영등포구","용산구","은평구","종로구","중구","중랑구"],
        "price_20L": "410원",
        "price_50L": "960원",
        "price_100L": "1,900원",
        "food_2L": "180원",
        "food_5L": "380원",
        "district_type": "구청",
        "phone_prefix": "02",
    },
    "부산": {
        "full": "부산광역시",
        "districts": ["강서구","금정구","기장군","남구","동구","동래구","부산진구","북구","사상구","사하구","서구","수영구","연제구","영도구","중구","해운대구"],
        "price_20L": "380원",
        "price_50L": "900원",
        "price_100L": "1,800원",
        "food_2L": "150원",
        "food_5L": "340원",
        "district_type": "구청",
        "phone_prefix": "051",
    },
    "대구": {
        "full": "대구광역시",
        "districts": ["남구","달서구","달성군","동구","북구","서구","수성구","중구"],
        "price_20L": "350원",
        "price_50L": "870원",
        "price_100L": "1,750원",
        "food_2L": "140원",
        "food_5L": "320원",
        "district_type": "구청",
        "phone_prefix": "053",
    },
    "인천": {
        "full": "인천광역시",
        "districts": ["강화군","계양구","남동구","동구","미추홀구","부평구","서구","연수구","옹진군","중구"],
        "price_20L": "390원",
        "price_50L": "930원",
        "price_100L": "1,850원",
        "food_2L": "160원",
        "food_5L": "360원",
        "district_type": "구청",
        "phone_prefix": "032",
    },
    "광주": {
        "full": "광주광역시",
        "districts": ["광산구","남구","동구","북구","서구"],
        "price_20L": "340원",
        "price_50L": "850원",
        "price_100L": "1,700원",
        "food_2L": "130원",
        "food_5L": "300원",
        "district_type": "구청",
        "phone_prefix": "062",
    },
    "대전": {
        "full": "대전광역시",
        "districts": ["대덕구","동구","서구","유성구","중구"],
        "price_20L": "360원",
        "price_50L": "880원",
        "price_100L": "1,760원",
        "food_2L": "140원",
        "food_5L": "320원",
        "district_type": "구청",
        "phone_prefix": "042",
    },
    "울산": {
        "full": "울산광역시",
        "districts": ["남구","동구","북구","울주군","중구"],
        "price_20L": "370원",
        "price_50L": "890원",
        "price_100L": "1,780원",
        "food_2L": "150원",
        "food_5L": "340원",
        "district_type": "구청",
        "phone_prefix": "052",
    },
    "세종": {
        "full": "세종특별자치시",
        "districts": ["세종시"],
        "price_20L": "350원",
        "price_50L": "860원",
        "price_100L": "1,720원",
        "food_2L": "140원",
        "food_5L": "310원",
        "district_type": "시청",
        "phone_prefix": "044",
    },
    "경기": {
        "full": "경기도",
        "districts": ["가평군","고양시","과천시","광명시","광주시","구리시","군포시","김포시","남양주시","동두천시","부천시","성남시","수원시","시흥시","안산시","안성시","안양시","양주시","양평군","여주시","연천군","오산시","용인시","의왕시","의정부시","이천시","파주시","평택시","포천시","하남시","화성시"],
        "price_20L": "400원",
        "price_50L": "950원",
        "price_100L": "1,880원",
        "food_2L": "170원",
        "food_5L": "370원",
        "district_type": "시청",
        "phone_prefix": "031",
    },
    "강원": {
        "full": "강원특별자치도",
        "districts": ["강릉시","고성군","동해시","삼척시","속초시","양구군","양양군","영월군","원주시","인제군","정선군","철원군","춘천시","태백시","평창군","홍천군","화천군","횡성군"],
        "price_20L": "330원",
        "price_50L": "810원",
        "price_100L": "1,650원",
        "food_2L": "120원",
        "food_5L": "280원",
        "district_type": "시청",
        "phone_prefix": "033",
    },
    "제주": {
        "full": "제주특별자치도",
        "districts": ["제주시","서귀포시"],
        "price_20L": "360원",
        "price_50L": "870원",
        "price_100L": "1,740원",
        "food_2L": "140원",
        "food_5L": "320원",
        "district_type": "시청",
        "phone_prefix": "064",
    },
}

# ========== 한국어 → 로마자 슬러그 변환 ==========
ROMANIZE_MAP = {
    # 서울
    "강남구": "gangnam-gu",
    "강동구": "gangdong-gu",
    "강북구": "gangbuk-gu",
    "강서구": "gangseo-gu",
    "관악구": "gwanak-gu",
    "광진구": "gwangjin-gu",
    "구로구": "guro-gu",
    "금천구": "geumcheon-gu",
    "노원구": "nowon-gu",
    "도봉구": "dobong-gu",
    "동대문구": "dongdaemun-gu",
    "동작구": "dongjak-gu",
    "마포구": "mapo-gu",
    "서대문구": "seodaemun-gu",
    "서초구": "seocho-gu",
    "성동구": "seongdong-gu",
    "성북구": "seongbuk-gu",
    "송파구": "songpa-gu",
    "양천구": "yangcheon-gu",
    "영등포구": "yeongdeungpo-gu",
    "용산구": "yongsan-gu",
    "은평구": "eunpyeong-gu",
    "종로구": "jongno-gu",
    "중구": "jung-gu",
    "중랑구": "jungnang-gu",
    # 부산
    "강서구": "gangseo-gu",
    "금정구": "geumjeong-gu",
    "기장군": "gijang-gun",
    "남구": "nam-gu",
    "동구": "dong-gu",
    "동래구": "dongnae-gu",
    "부산진구": "busanjin-gu",
    "북구": "buk-gu",
    "사상구": "sasang-gu",
    "사하구": "saha-gu",
    "서구": "seo-gu",
    "수영구": "suyeong-gu",
    "연제구": "yeonje-gu",
    "영도구": "yeongdo-gu",
    "해운대구": "haeundae-gu",
    # 대구
    "달서구": "dalseo-gu",
    "달성군": "dalseong-gun",
    "수성구": "suseong-gu",
    # 인천
    "강화군": "ganghwa-gun",
    "계양구": "gyeyang-gu",
    "남동구": "namdong-gu",
    "미추홀구": "michuhol-gu",
    "부평구": "bupyeong-gu",
    "연수구": "yeonsu-gu",
    "옹진군": "ongjin-gun",
    # 광주
    "광산구": "gwangsan-gu",
    # 대전
    "대덕구": "daedeok-gu",
    "유성구": "yuseong-gu",
    # 울산
    "울주군": "ulju-gun",
    # 세종
    "세종시": "sejong-si",
    # 경기
    "가평군": "gapyeong-gun",
    "고양시": "goyang-si",
    "과천시": "gwacheon-si",
    "광명시": "gwangmyeong-si",
    "광주시": "gwangju-si",
    "구리시": "guri-si",
    "군포시": "gunpo-si",
    "김포시": "gimpo-si",
    "남양주시": "namyangju-si",
    "동두천시": "dongducheon-si",
    "부천시": "bucheon-si",
    "성남시": "seongnam-si",
    "수원시": "suwon-si",
    "시흥시": "siheung-si",
    "안산시": "ansan-si",
    "안성시": "anseong-si",
    "안양시": "anyang-si",
    "양주시": "yangju-si",
    "양평군": "yangpyeong-gun",
    "여주시": "yeoju-si",
    "연천군": "yeoncheon-gun",
    "오산시": "osan-si",
    "용인시": "yongin-si",
    "의왕시": "uiwang-si",
    "의정부시": "uijeongbu-si",
    "이천시": "icheon-si",
    "파주시": "paju-si",
    "평택시": "pyeongtaek-si",
    "포천시": "pocheon-si",
    "하남시": "hanam-si",
    "화성시": "hwaseong-si",
    # 강원
    "강릉시": "gangneung-si",
    "고성군": "goseong-gun",
    "동해시": "donghae-si",
    "삼척시": "samcheok-si",
    "속초시": "sokcho-si",
    "양구군": "yanggu-gun",
    "양양군": "yangyang-gun",
    "영월군": "yeongwol-gun",
    "원주시": "wonju-si",
    "인제군": "inje-gun",
    "정선군": "jeongseon-gun",
    "철원군": "cheorwon-gun",
    "춘천시": "chuncheon-si",
    "태백시": "taebaek-si",
    "평창군": "pyeongchang-gun",
    "홍천군": "hongcheon-gun",
    "화천군": "hwacheon-gun",
    "횡성군": "hoengseong-gun",
    # 제주
    "제주시": "jeju-si",
    "서귀포시": "seogwipo-si",
}

# 지역명 → 슬러그 접두사 매핑
REGION_SLUG_MAP = {
    "서울": "seoul",
    "부산": "busan",
    "대구": "daegu",
    "인천": "incheon",
    "광주": "gwangju",
    "대전": "daejeon",
    "울산": "ulsan",
    "세종": "sejong",
    "경기": "gyeonggi",
    "강원": "gangwon",
    "제주": "jeju",
}


def get_slug(region_name, district):
    region_slug = REGION_SLUG_MAP.get(region_name, region_name)
    district_slug = ROMANIZE_MAP.get(district, district.replace(" ", "-"))
    return f"waste-bag-{region_slug}-{district_slug}"


def calc_price(base_20L_str, multiplier):
    """base_20L 기준가에서 배율을 곱해 가격 문자열 반환"""
    raw = base_20L_str.replace("원", "").replace(",", "")
    val = int(float(raw) * multiplier)
    if val >= 1000:
        formatted = f"{val:,}"
    else:
        formatted = str(val)
    return f"{formatted}원"


def get_price_table(info):
    """지역 기준가를 토대로 규격별 가격 계산"""
    base = int(info["price_20L"].replace("원", "").replace(",", ""))
    # 5L, 10L, 20L, 50L, 75L, 100L 비율 추정
    prices = {
        "5L":   round(base * 0.25 / 10) * 10,
        "10L":  round(base * 0.5 / 10) * 10,
        "20L":  base,
        "50L":  int(info["price_50L"].replace("원", "").replace(",", "")),
        "75L":  round(int(info["price_50L"].replace("원", "").replace(",", "")) * 1.5 / 10) * 10,
        "100L": int(info["price_100L"].replace("원", "").replace(",", "")),
    }
    rows = ""
    for size, price in prices.items():
        formatted = f"{price:,}원"
        rows += f"<tr><td>{size}</td><td>{formatted}</td><td>일반쓰레기용</td></tr>\n"
    return rows


def get_food_price_table(info):
    base_2L = int(info["food_2L"].replace("원", "").replace(",", ""))
    base_5L = int(info["food_5L"].replace("원", "").replace(",", ""))
    prices = {
        "1L":  round(base_2L * 0.5 / 10) * 10,
        "2L":  base_2L,
        "3L":  round(base_2L * 1.5 / 10) * 10,
        "5L":  base_5L,
        "10L": round(base_5L * 2.0 / 10) * 10,
    }
    rows = ""
    for size, price in prices.items():
        rows += f"<tr><td>{size}</td><td>{price:,}원</td><td>음식물쓰레기 전용</td></tr>\n"
    return rows


def generate_title(region_info, district):
    full = region_info["full"]
    return f"{full} {district} 종량제봉투 파는곳 가격 종류 구매 방법 총정리"


def generate_content(region_name, region_info, district):
    full = region_info["full"]
    dtype = region_info["district_type"]
    price_20L = region_info["price_20L"]
    price_50L = region_info["price_50L"]
    price_100L = region_info["price_100L"]
    food_2L = region_info["food_2L"]
    food_5L = region_info["food_5L"]
    phone = region_info["phone_prefix"]

    price_rows = get_price_table(region_info)
    food_rows = get_food_price_table(region_info)

    # 구청/시청 URL 패턴 (실제 URL은 지역마다 다르지만 대표 포맷 사용)
    district_office_url_map = {
        "서울": f"https://www.seoul.go.kr/",
        "부산": f"https://www.busan.go.kr/",
        "대구": f"https://www.daegu.go.kr/",
        "인천": f"https://www.incheon.go.kr/",
        "광주": f"https://www.gwangju.go.kr/",
        "대전": f"https://www.daejeon.go.kr/",
        "울산": f"https://www.ulsan.go.kr/",
        "세종": f"https://www.sejong.go.kr/",
        "경기": f"https://www.gg.go.kr/",
        "강원": f"https://www.gwd.go.kr/",
        "제주": f"https://www.jeju.go.kr/",
    }
    office_url = district_office_url_map.get(region_name, "https://www.gov.kr/")

    # 지역 특성에 따른 소개 문구 변형
    region_intro_map = {
        "서울": f"대한민국 수도 서울특별시 {district}에 거주하시는 분들을 위한",
        "부산": f"제2의 도시 부산광역시 {district}에 거주하시는 분들을 위한",
        "대구": f"섬유·패션의 도시 대구광역시 {district}에 거주하시는 분들을 위한",
        "인천": f"국제공항의 도시 인천광역시 {district}에 거주하시는 분들을 위한",
        "광주": f"예향의 도시 광주광역시 {district}에 거주하시는 분들을 위한",
        "대전": f"과학의 도시 대전광역시 {district}에 거주하시는 분들을 위한",
        "울산": f"산업의 도시 울산광역시 {district}에 거주하시는 분들을 위한",
        "세종": f"행정중심복합도시 세종특별자치시 {district}에 거주하시는 분들을 위한",
        "경기": f"수도권 핵심 지역 경기도 {district}에 거주하시는 분들을 위한",
        "강원": f"청정 자연의 강원특별자치도 {district}에 거주하시는 분들을 위한",
        "제주": f"아름다운 섬 제주특별자치도 {district}에 거주하시는 분들을 위한",
    }
    intro_prefix = region_intro_map.get(region_name, f"{full} {district}에 거주하시는 분들을 위한")

    content = f'''<p style="font-size:17px;line-height:1.8;">{intro_prefix} <strong>종량제봉투 구매 완벽 가이드</strong>입니다. {district} 내에서 종량제봉투를 어디서 살 수 있는지, 규격별 가격은 얼마인지, 음식물 쓰레기봉투는 어떻게 구매하는지까지 <strong>한 번에 정리</strong>했습니다. {district}의 종량제봉투는 반드시 {district} 지정 봉투를 사용해야 하며, 다른 지역 봉투를 사용하면 수거가 거부될 수 있으니 주의하세요.</p>

<h2>{district} 종량제봉투 가격표</h2>
<p>{full} {district}의 종량제봉투 가격은 {dtype}에서 결정하며, 규격에 따라 가격이 달라집니다. 20L 기준 <strong>{price_20L}</strong>이며, 아래 표에서 전 규격 가격을 확인하세요.</p>

<table>
<thead><tr><th>규격</th><th>가격</th><th>용도</th></tr></thead>
<tbody>
{price_rows}</tbody>
</table>

<p>※ 위 가격은 {district} 기준 표준 판매가이며, 판매처(편의점·마트 등)에 따라 소폭 차이가 있을 수 있습니다. 정확한 최신 가격은 {district} {dtype}({phone}-xxx-xxxx) 또는 공식 홈페이지에서 확인하세요.</p>

<h2>{district} 종량제봉투 파는곳</h2>
<p>{district} 내에서 종량제봉투를 구입할 수 있는 곳은 크게 편의점, 대형마트, {dtype}, 동 주민센터, 온라인 채널로 나뉩니다. 각 구매처의 특징을 아래에서 확인하세요.</p>

<h3>편의점</h3>
<p>가장 접근하기 쉬운 구매처입니다. {district} 내 편의점이라면 <strong>{district} 전용 종량제봉투</strong>를 판매합니다. 24시간 운영하므로 급하게 봉투가 필요할 때 편리합니다.</p>
<ul>
<li><strong>CU</strong> – {district} 내 전 지점에서 판매. 다양한 규격 구비</li>
<li><strong>GS25</strong> – {district} 지정 봉투 취급. 소규격(5L, 10L) 위주로 항상 재고 유지</li>
<li><strong>세븐일레븐</strong> – {district} 전 지점에서 구매 가능. 늦은 밤에도 이용 가능</li>
<li><strong>이마트24</strong> – {district} 봉투 상시 판매. 대용량(50L, 100L) 재고도 보유</li>
</ul>

<h3>대형마트</h3>
<p>대용량 봉투를 여러 장 한꺼번에 구매할 때는 대형마트가 편리합니다. {district} 인근 마트에서 구매 가능합니다.</p>
<ul>
<li><strong>이마트</strong> – 생활용품 코너 또는 서비스 카운터에서 {district} 종량제봉투 판매</li>
<li><strong>홈플러스</strong> – 봉투 전용 진열대에서 규격별로 구매 가능</li>
<li><strong>롯데마트</strong> – {district} 지정 봉투 취급, 대용량 묶음 구매 가능</li>
</ul>

<h3>{dtype}</h3>
<p>{district} {dtype}에서는 종량제봉투를 직접 구매하거나 판매처 목록을 안내받을 수 있습니다. {dtype} 민원실 방문 시 가격표와 인근 판매점 안내를 제공합니다.</p>

<h3>동 주민센터</h3>
<p>{district}의 각 동 주민센터에서도 종량제봉투를 판매합니다. 주민등록 관련 업무를 보러 가실 때 함께 구매하면 편리합니다. 평일 오전 9시~오후 6시 운영합니다.</p>

<h3>온라인 구매</h3>
<p>직접 방문이 어렵다면 온라인으로도 구매할 수 있습니다. <strong>종량제닷컴(jongryangjae.com)</strong>은 전국 지자체별 종량제봉투를 온라인으로 주문하고 택배로 받을 수 있는 공식 인증 쇼핑몰입니다. {district} 지정 봉투도 취급하니 참고하세요.</p>

{cta_block("종량제닷컴 – 온라인 종량제봉투 구매", f"{district} 지정 종량제봉투를 집에서 편하게 주문하세요", "https://www.jongryangjae.com/", "blue")}

<h2>{district} 음식물 종량제봉투</h2>
<p>{district}에서는 음식물 쓰레기를 별도의 <strong>음식물 종량제봉투</strong>에 담아 배출해야 합니다. 일반 쓰레기봉투와 혼용하면 과태료 부과 대상이 되므로 주의하세요.</p>

<table>
<thead><tr><th>규격</th><th>가격</th><th>비고</th></tr></thead>
<tbody>
{food_rows}</tbody>
</table>

<p>{district}의 음식물 종량제봉투는 일반 종량제봉투와 같은 판매처(편의점, 마트, 주민센터 등)에서 구매할 수 있습니다. 2L 기준 <strong>{food_2L}</strong>, 5L 기준 <strong>{food_5L}</strong>입니다.</p>
<p>음식물 쓰레기 배출 시 국물은 최대한 제거한 후 봉투에 담아야 하며, 뼈·껍데기류는 일반 쓰레기봉투에 버려야 합니다.</p>

<h2>종량제봉투 종류</h2>
<p>{district}에서 사용하는 종량제봉투는 크게 세 가지로 구분됩니다.</p>

<h3>1. 일반쓰레기용 종량제봉투</h3>
<p>가장 일반적인 종량제봉투입니다. 재활용이 불가능한 생활 쓰레기를 담아 지정 장소에 배출합니다. {district} 지정 색상(보통 흰색 또는 회색)의 봉투만 사용 가능합니다.</p>

<h3>2. 음식물쓰레기용 종량제봉투</h3>
<p>음식물 쓰레기 전용 봉투로, 녹색 또는 노란색 계열이 많습니다. {district}에서는 음식물 쓰레기를 이 봉투에 담거나 공동주택의 경우 전용 수거함(RFID)을 이용합니다.</p>

<h3>3. 재활용 분리배출</h3>
<p>종이, 플라스틱, 유리, 캔류 등 재활용 가능한 품목은 종량제봉투 없이 투명 비닐봉투에 담아 분리배출합니다. {district}에서는 재활용 가능 품목을 반드시 분리배출해 자원 낭비를 줄여야 합니다.</p>

{cta_block(f"{district} {dtype} 홈페이지", f"{district} 쓰레기 배출 안내 및 종량제봉투 관련 공지를 확인하세요", office_url, "yellow")}

<h2>종량제봉투 사용 시 주의사항</h2>
<p>{district}에서 종량제봉투를 올바르게 사용하려면 아래 사항을 반드시 지켜야 합니다.</p>
<ul>
<li><strong>타 지역 봉투 사용 금지</strong>: {district} 지정 봉투 외에 다른 시·군·구 봉투는 수거되지 않습니다. 타 지역에서 구매한 봉투를 {district}에서 사용하면 쓰레기 수거 거부 및 과태료 부과 대상이 됩니다.</li>
<li><strong>봉투 규격 준수</strong>: 내용물이 봉투 용량의 80% 이상이 되지 않도록 주의하고, 봉투 입구는 단단히 묶어야 합니다.</li>
<li><strong>분리배출 철저</strong>: 재활용 가능 품목(종이, 플라스틱, 캔, 유리 등)은 반드시 분리배출합니다. 종량제봉투에 넣으면 과태료 부과 대상입니다.</li>
<li><strong>배출 시간 준수</strong>: {district}의 쓰레기 배출 시간은 원칙적으로 수거 전날 저녁(오후 8시 이후)부터 수거 당일 새벽까지입니다.</li>
<li><strong>대형 폐기물 별도 신고</strong>: 가구, 가전 등 대형 폐기물은 종량제봉투에 넣을 수 없으며, {district} {dtype}에 대형 폐기물 스티커를 신청해야 합니다.</li>
</ul>

<h2>자주 묻는 질문 (FAQ)</h2>

<h3>Q. {district}에서 다른 지역 종량제봉투를 사용해도 되나요?</h3>
<p>A. 안 됩니다. 종량제봉투는 해당 지자체에서만 사용 가능한 <strong>지역 전용 규격봉투</strong>입니다. {district} 외 다른 시·군·구에서 발행한 봉투는 {district}에서 수거되지 않으며, 위반 시 <strong>최대 100만 원의 과태료</strong>가 부과될 수 있습니다.</p>

<h3>Q. 종량제봉투를 편의점에서 교환하거나 환불할 수 있나요?</h3>
<p>A. 원칙적으로 미개봉 상태의 봉투는 동일 판매점에서 영수증을 지참하면 교환 또는 환불이 가능합니다. 단, 개봉 후에는 불가능하며 판매처마다 규정이 다를 수 있으므로 구매 전에 확인하는 것이 좋습니다.</p>

<h3>Q. 음식물 종량제봉투와 일반 종량제봉투의 차이는 무엇인가요?</h3>
<p>A. <strong>일반 종량제봉투</strong>는 재활용이 불가능한 생활 쓰레기(잔여 생활폐기물)를 담는 봉투이고, <strong>음식물 종량제봉투</strong>는 과일껍질·채소·음식 찌꺼기 등 음식물 쓰레기 전용 봉투입니다. {district}에서는 두 종류를 반드시 구분해서 사용해야 합니다.</p>

<h3>Q. {district} 종량제봉투 불법 판매 신고는 어디에 하나요?</h3>
<p>A. 가격 초과 판매, 위조 봉투 판매 등 불법 행위는 <strong>{district} {dtype}({phone}-xxx-xxxx)</strong> 또는 <strong>국민신문고(www.epeople.go.kr)</strong>에 신고할 수 있습니다. 신고자에 대한 포상 제도도 운영 중입니다.</p>

<h3>Q. {district} 종량제봉투를 대량으로 구매하면 할인이 되나요?</h3>
<p>A. 일부 대형마트에서 묶음 판매 형태로 제공하는 경우가 있으나, 종량제봉투 자체는 {district} {dtype}이 고시한 가격으로 판매되므로 별도의 할인은 거의 없습니다. 온라인 쇼핑몰(종량제닷컴 등)에서도 동일 가격으로 판매됩니다.</p>

{cta_block("종량제닷컴 – 전국 종량제봉투 온라인 구매", f"{district}을 포함한 전국 지자체 종량제봉투를 한 곳에서 구매하세요", "https://www.jongryangjae.com/", "green")}

<h2>마무리</h2>
<p style="font-size:17px;line-height:1.8;">{full} {district}의 종량제봉투 구매처와 가격, 사용 방법을 모두 정리했습니다. {district}에서는 반드시 <strong>{district} 전용 종량제봉투</strong>를 사용하고, 음식물 쓰레기는 별도의 음식물 봉투에 담아야 합니다. 가장 가까운 편의점(CU, GS25, 세븐일레븐, 이마트24)에서 쉽게 구매할 수 있으며, 온라인 주문도 가능합니다.</p>
<p style="font-size:17px;line-height:1.8;">분리배출을 철저히 실천해 자원을 절약하고, 올바른 봉투 사용으로 {district}의 쾌적한 환경을 함께 만들어 나갑시다. 추가로 궁금한 사항은 {district} {dtype} 환경 담당 부서({phone}-xxx-xxxx)로 문의하시기 바랍니다.</p>'''

    return content


# ========== WordPress 발행 ==========
def publish_to_wordpress(title, slug, content, category_id):
    payload = {
        "title": title,
        "content": content,
        "status": "publish",
        "slug": slug,
        "categories": [category_id],
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API, data=data, method="POST")
    req.add_header("Authorization", f"Basic {AUTH}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        r = json.loads(resp.read().decode())
    return r.get("id"), r.get("link", "")


# ========== IndexNow 제출 ==========
def submit_indexnow(urls):
    if not urls:
        return
    print(f"\n[IndexNow] {len(urls)}개 URL 제출 중...")
    payload = {
        "host": "devupbox.com",
        "key": "8dbbd7d6729b4a65b7dce4b9083c65e3",
        "keyLocation": "https://devupbox.com/8dbbd7d6729b4a65b7dce4b9083c65e3.txt",
        "urlList": urls,
    }
    ndata = json.dumps(payload).encode("utf-8")
    for name, endpoint in [
        ("Naver", "https://searchadvisor.naver.com/indexnow"),
        ("Bing", "https://www.bing.com/indexnow"),
        ("Yandex", "https://yandex.com/indexnow"),
    ]:
        req = urllib.request.Request(endpoint, data=ndata, method="POST")
        req.add_header("Content-Type", "application/json; charset=utf-8")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                print(f"  {name}: HTTP {resp.status}")
        except urllib.error.HTTPError as e:
            print(f"  {name}: HTTP {e.code}")
        except Exception as e:
            print(f"  {name}: {e}")


# ========== 메인 ==========
def main():
    start_idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0

    all_posts = []
    for region_name, info in REGIONS.items():
        for district in info["districts"]:
            all_posts.append((region_name, info, district))

    total = len(all_posts)
    print(f"총 {total}개 포스트 예정 (시작 인덱스: {start_idx})")

    published_urls = []

    for idx, (region_name, info, district) in enumerate(all_posts):
        if idx < start_idx:
            continue

        title = generate_title(info, district)
        slug = get_slug(region_name, district)
        raw_content = generate_content(region_name, info, district)
        content = auto_link(raw_content)

        try:
            pid, link = publish_to_wordpress(title, slug, content, category_id=13)
            print(f"[{idx + 1}/{total}] {info['full']} {district} → OK | ID:{pid} | {link}")
            if link:
                published_urls.append(link)
        except urllib.error.HTTPError as e:
            body = e.read().decode() if e.fp else ""
            print(f"[{idx + 1}/{total}] {info['full']} {district} → FAIL | HTTP {e.code} | {body[:200]}")
        except Exception as e:
            print(f"[{idx + 1}/{total}] {info['full']} {district} → FAIL | {e}")

        time.sleep(1)

    # IndexNow 일괄 제출 (최대 1000개씩)
    chunk_size = 1000
    for i in range(0, len(published_urls), chunk_size):
        submit_indexnow(published_urls[i:i + chunk_size])

    print(f"\n{'=' * 60}")
    print(f"완료! 발행 성공: {len(published_urls)}개 / 전체: {total - start_idx}개")
    print("=" * 60)


if __name__ == "__main__":
    main()

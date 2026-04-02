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
    # 1. 봄소풍/벚꽃축제/꽃놀이
    {
        "title": "2026 벚꽃축제 일정 봄소풍 꽃놀이 명소 BEST 10 총정리",
        "cat": 13,
        "slug": "cherry-blossom-festival-spring-picnic-2026",
        "images": [
            ("photo-1462275646964-a0e3c11f18a6", "2026 벚꽃축제 봄소풍 명소"),
            ("photo-1522383225653-ed111181a951", "벚꽃 꽃놀이 풍경"),
            ("photo-1490750967868-88aa4f44baee", "봄소풍 피크닉 준비"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">매년 봄이 오면 전국이 분홍빛으로 물드는 <strong>벚꽃 시즌</strong>이 찾아옵니다. 2026년에도 여의도, 경주, 진해, 석촌호수 등 전국 각지에서 화려한 벚꽃축제가 펼쳐질 예정입니다. 짧게는 일주일, 길게는 보름 남짓인 벚꽃 시즌을 제대로 즐기려면 미리 개화 시기와 명소를 파악하는 것이 중요합니다. 이 글에서는 <strong>2026 벚꽃 개화 예상 시기</strong>부터 <strong>전국 벚꽃축제 BEST 10</strong>, 봄소풍 준비물, 인생 사진 팁까지 빠짐없이 정리해 드립니다.</p>

{imgs[0]}

<h2>2026 벚꽃 개화 예상 시기 (지역별)</h2>
<p>기상청 장기 예보와 최근 기후 트렌드를 종합하면, 2026년 벚꽃은 평년보다 2~3일 빠르게 개화할 것으로 예상됩니다. 아래 표에서 주요 지역별 개화 시기를 확인하세요.</p>
<table><thead><tr><th>지역</th><th>개화 예상일</th><th>만개 예상일</th><th>대표 명소</th></tr></thead><tbody>
<tr><td>제주</td><td>3월 21일</td><td>3월 27일</td><td>제주 왕벚꽃길</td></tr>
<tr><td>부산</td><td>3월 27일</td><td>4월 2일</td><td>해운대, 범어사</td></tr>
<tr><td>광주</td><td>3월 29일</td><td>4월 4일</td><td>충장로, 사직공원</td></tr>
<tr><td>진해(창원)</td><td>3월 30일</td><td>4월 5일</td><td>경화역, 여좌천</td></tr>
<tr><td>서울</td><td>4월 3일</td><td>4월 9일</td><td>여의도, 석촌호수</td></tr>
<tr><td>경주</td><td>4월 4일</td><td>4월 10일</td><td>보문호수, 불국사</td></tr>
<tr><td>강릉</td><td>4월 7일</td><td>4월 13일</td><td>경포대, 오죽헌길</td></tr>
<tr><td>춘천</td><td>4월 9일</td><td>4월 15일</td><td>의암호, 남이섬</td></tr>
</tbody></table>
<p><strong>TIP:</strong> 개화 후 만개까지 보통 5~7일이 소요됩니다. 만개 이후 2~3일이 가장 아름다운 절정기이므로, 만개 예상일 기준 ±3일을 방문 목표일로 잡으세요.</p>

{cta_block("한국관광공사 공식 축제 정보", "전국 벚꽃축제 일정과 행사 정보를 한눈에 확인하세요", "https://korean.visitkorea.or.kr/", "blue")}

<h2>전국 벚꽃축제 BEST 10</h2>

<h3>1. 서울 여의도 봄꽃축제</h3>
<p>국회의사당 뒷길과 여의도공원을 중심으로 약 1,500그루의 벚꽃이 터널을 이룹니다. 2026년 축제는 4월 4일~13일 예정이며, 야간 조명 행사와 버스킹 공연이 함께 열립니다.</p>

<h3>2. 진해 군항제</h3>
<p>국내 최대 규모의 벚꽃 행사로, 약 36만 그루의 벚나무가 진해 전역을 뒤덮습니다. 경화역 철길 벚꽃길과 여좌천 로망스다리가 하이라이트입니다. 2026년 개최 기간은 3월 28일~4월 6일.</p>

<h3>3. 경주 벚꽃 마라톤 & 봄 축제</h3>
<p>보문호수 일대와 불국사 진입로는 경주 벚꽃의 양대 산맥입니다. 4월 첫째 주에는 벚꽃 마라톤 대회가 열려 달리기와 꽃구경을 동시에 즐길 수 있습니다.</p>

<h3>4. 서울 석촌호수 벚꽃축제</h3>
<p>롯데월드타워를 배경으로 펼쳐지는 석촌호수 벚꽃은 도심 속 이색 풍경을 선사합니다. 산책로 2km를 따라 빼곡한 벚꽃길이 이어지며, 야간 조명으로 밤 벚꽃도 즐길 수 있습니다.</p>

<h3>5. 하동 십리벚꽃길</h3>
<p>경남 하동의 섬진강변을 따라 4km에 걸쳐 이어지는 벚꽃 터널은 국내에서 가장 긴 벚꽃 도로 중 하나입니다. 드라이브 코스로도 제격입니다.</p>

<h3>6. 전주 완산칠봉 꽃동산</h3>
<p>벚꽃과 개나리, 진달래가 어우러진 복합 꽃 명소입니다. 한옥마을과 연계해 방문하면 더욱 알찬 봄나들이가 됩니다.</p>

<h3>7. 수원 팔달산 벚꽃길</h3>
<p>수원화성과 어우러진 벚꽃 풍경이 독특한 분위기를 자아냅니다. 수원천변 벚꽃길도 함께 걷기 좋습니다.</p>

<h3>8. 대구 달성공원·수성못</h3>
<p>대구의 도심 속 벚꽃 명소로, 수성못 유원지의 야경 벚꽃이 특히 유명합니다. 오리배를 타며 벚꽃을 감상할 수 있습니다.</p>

<h3>9. 경포대 벚꽃길 (강릉)</h3>
<p>경포호 주변과 경포대 해수욕장 인근의 벚꽃길은 바다와 꽃을 동시에 즐길 수 있는 이색 코스입니다.</p>

<h3>10. 제주 왕벚꽃길 (전농로)</h3>
<p>제주 왕벚나무는 국내 자생종으로, 일반 벚꽃보다 꽃잎이 더 크고 화려합니다. 전농로 1km 구간이 핵심 명소입니다.</p>

{imgs[1]}

<h2>봄소풍 필수 준비물 체크리스트</h2>
<table><thead><tr><th>카테고리</th><th>준비물</th><th>비고</th></tr></thead><tbody>
<tr><td>돗자리/텐트</td><td>방수 돗자리, 미니 그늘막</td><td>바람막이 겸용 추천</td></tr>
<tr><td>먹거리</td><td>김밥, 샌드위치, 과일, 음료</td><td>쓰레기봉투 필수</td></tr>
<tr><td>방한/방풍</td><td>얇은 겉옷, 바람막이</td><td>봄바람 쌀쌀할 수 있음</td></tr>
<tr><td>자외선 차단</td><td>선크림, 선글라스, 모자</td><td>봄 자외선 강함</td></tr>
<tr><td>알레르기</td><td>항히스타민제, 마스크</td><td>꽃가루 대비</td></tr>
<tr><td>카메라</td><td>스마트폰, 삼각대, 보조배터리</td><td>인생샷 필수템</td></tr>
<tr><td>기타</td><td>물티슈, 핫팩, 쓰레기봉투</td><td>미세먼지 대비 마스크</td></tr>
</tbody></table>

{cta_block("한국관광공사 봄 여행 정보", "봄소풍 명소와 여행 코스를 지금 바로 검색하세요", "https://korean.visitkorea.or.kr/", "green")}

<h2>꽃놀이 인생 사진 팁</h2>
<h3>구도 & 촬영 시간</h3>
<ul>
<li><strong>골든아워 활용</strong>: 일출 후 1시간, 일몰 전 1시간이 가장 부드러운 빛을 제공합니다.</li>
<li><strong>역광 촬영</strong>: 벚꽃을 역광으로 찍으면 꽃잎이 반투명하게 빛나 몽환적인 사진을 얻을 수 있습니다.</li>
<li><strong>낮은 앵글</strong>: 카메라를 낮춰 벚꽃을 배경으로 인물을 담으면 꽃이 더욱 풍성하게 표현됩니다.</li>
<li><strong>흔들림 활용</strong>: 꽃잎이 흩날리는 순간을 느린 셔터속도로 담으면 시적인 감성 사진이 완성됩니다.</li>
</ul>
<h3>스마트폰 촬영 꿀팁</h3>
<ul>
<li>인물 모드(Portrait Mode)로 배경을 흐릿하게 처리해 벚꽃을 돋보이게 합니다.</li>
<li>HDR 기능을 켜면 밝은 하늘과 어두운 꽃잎 모두 살아있는 사진을 얻을 수 있습니다.</li>
<li>광각 렌즈를 활용해 벚꽃 터널 전체를 한 프레임에 담으세요.</li>
</ul>

{imgs[2]}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 벚꽃 개화 예측이 빗나가는 경우가 있나요?</h3>
<p>A. 네, 기온 변화에 따라 1~2주까지 차이가 날 수 있습니다. 방문 1주일 전 기상청 개화 모니터링 페이지나 한국관광공사 SNS를 확인하세요.</p>
<h3>Q. 벚꽃 명소 주차는 어떻게 하나요?</h3>
<p>A. 진해, 여의도 등 대형 축제 기간에는 대중교통 이용을 강력 권장합니다. 셔틀버스나 임시 주차장이 운영되니 미리 공식 축제 홈페이지를 확인하세요.</p>
<h3>Q. 비 오는 날 벚꽃 구경도 괜찮나요?</h3>
<p>A. 빗속 벚꽃은 운치 있는 풍경을 연출합니다. 다만 강풍을 동반한 비는 꽃잎이 빨리 떨어지게 하니, 약한 봄비라면 오히려 특별한 사진을 건질 수 있습니다.</p>
<h3>Q. 꽃가루 알레르기가 있는데 벚꽃축제를 즐길 수 있나요?</h3>
<p>A. 벚꽃 자체는 꽃가루 알레르기 유발이 낮은 편입니다. 다만 봄철 소나무 등 다른 식물의 꽃가루가 함께 날리므로 항히스타민제와 마스크를 준비하세요.</p>

{cta_block("한국관광공사에서 축제 일정 확인", "2026 봄 축제 전체 일정을 공식 채널에서 확인하세요", "https://korean.visitkorea.or.kr/", "yellow")}

<h2>마무리</h2>
<p>2026년 벚꽃 시즌은 3월 하순부터 4월 중순까지 이어집니다. 지역별 개화 시기를 미리 파악하고, 준비물 체크리스트를 활용해 완벽한 봄소풍을 계획해 보세요. 짧은 벚꽃 시즌인 만큼, 올해는 더 적극적으로 나서서 소중한 봄의 기억을 만들어 보시길 바랍니다. 꽃 지기 전에 서두르세요!</p>''',
    },

    # 2. 캠핑/차박/글램핑
    {
        "title": "2026 봄 캠핑 차박 글램핑 추천 명소 준비물 총정리",
        "cat": 13,
        "slug": "spring-camping-car-camping-glamping-2026",
        "images": [
            ("photo-1504280390367-361c6d9f38f4", "2026 봄 캠핑 추천 명소"),
            ("photo-1478131143081-80f7f84ca84d", "차박 캠핑 풍경"),
            ("photo-1537905569824-f89f14cceb68", "글램핑 감성 캠핑"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">날씨가 따뜻해지는 봄은 캠핑 애호가들이 가장 기다리는 계절입니다. 미세먼지 걱정이 줄어들고, 숲과 강변이 초록빛으로 물드는 4월~5월은 <strong>캠핑, 차박, 글램핑</strong> 모두에 최적의 시즌입니다. 2026년 봄 캠핑을 계획하는 분들을 위해 세 가지 캠핑 스타일 비교부터 전국 추천 캠핑장 10곳, 필수 준비물 체크리스트, 초보자 꿀팁까지 한 번에 정리했습니다.</p>

{imgs[0]}

<h2>캠핑 vs 차박 vs 글램핑 비교</h2>
<p>캠핑 스타일은 크게 세 가지로 나눌 수 있습니다. 각각의 특징과 장단점을 비교해 나에게 맞는 스타일을 선택해 보세요.</p>
<table><thead><tr><th>구분</th><th>일반 캠핑</th><th>차박</th><th>글램핑</th></tr></thead><tbody>
<tr><td>숙박 방식</td><td>텐트</td><td>차량 내부</td><td>상설 텐트/카라반</td></tr>
<tr><td>준비 난이도</td><td>높음</td><td>중간</td><td>낮음</td></tr>
<tr><td>비용</td><td>저~중</td><td>저</td><td>높음</td></tr>
<tr><td>이동 편의성</td><td>낮음</td><td>높음</td><td>낮음(예약 필요)</td></tr>
<tr><td>자연 친밀도</td><td>매우 높음</td><td>높음</td><td>중간</td></tr>
<tr><td>편의시설</td><td>직접 구성</td><td>차량 의존</td><td>제공됨</td></tr>
<tr><td>추천 대상</td><td>캠핑 마니아</td><td>솔로·커플</td><td>가족·초보자</td></tr>
</tbody></table>

{cta_block("고캠핑 공식 예약 사이트", "전국 캠핑장 검색 및 예약을 지금 바로 시작하세요", "https://www.gocamping.or.kr/", "blue")}

<h2>2026 봄 추천 캠핑장 10곳</h2>

<h3>1. 남양주 수동국민여가캠핑장 (경기)</h3>
<p>서울에서 1시간 거리, 수동계곡 옆에 위치한 국공립 캠핑장입니다. 봄철 연두빛 숲 속에서 텐트를 치고 계곡 소리를 들으며 하룻밤을 보낼 수 있습니다. 사이트당 전기 공급이 되어 편리합니다.</p>

<h3>2. 인제 원대리 자작나무숲 캠핑장 (강원)</h3>
<p>국내 유일의 자작나무 인공림을 배경으로 한 감성 캠핑 성지입니다. 봄에는 연초록 자작나무 잎과 흰 수피의 조화가 압도적입니다.</p>

<h3>3. 고창 선운산도립공원 캠핑장 (전북)</h3>
<p>4월 중순 꽃무릇과 동백이 피는 선운산 기슭에 위치합니다. 등산과 캠핑을 함께 즐기기에 최적입니다.</p>

<h3>4. 가평 자라섬 캠핑장 (경기)</h3>
<p>북한강 위의 섬에서 캠핑하는 특별한 경험을 제공합니다. 봄철 재즈 페스티벌 시즌과 겹치면 더욱 특별한 여행이 됩니다.</p>

<h3>5. 경주 보문관광단지 오토캠핑장 (경북)</h3>
<p>벚꽃 명소인 보문호수 바로 옆에 위치해 봄 캠핑과 꽃구경을 동시에 즐길 수 있습니다.</p>

<h3>6. 강릉 정동진 솔향기캠핑장 (강원)</h3>
<p>소나무 숲과 동해 바다가 어우러진 캠핑장입니다. 새벽에 정동진 일출을 캠핑장에서 바로 감상할 수 있습니다.</p>

<h3>7. 남해 독일마을 차박 명소 (경남)</h3>
<p>독일풍 건물과 남해 바다를 배경으로 한 이색 차박 성지입니다. 봄철 유채꽃과 함께라면 더욱 아름다운 풍경을 즐길 수 있습니다.</p>

<h3>8. 춘천 남이섬 캠핑장 (강원)</h3>
<p>국제적으로 유명한 남이섬 내 공식 캠핑장으로, 섬 특유의 자연환경이 봄철 분위기를 더욱 살려줍니다.</p>

<h3>9. 제주 비자림 캠핑장 (제주)</h3>
<p>수백 년 된 비자나무 숲 인근의 캠핑장으로, 제주의 봄 바람과 함께 힐링 캠핑을 즐길 수 있습니다.</p>

<h3>10. 대관령 삼양목장 오토캠핑장 (강원)</h3>
<p>해발 1,100m의 고원에 위치해 봄에도 서늘한 기온이 유지됩니다. 탁 트인 초원 뷰가 일품인 글램핑·캠핑 명소입니다.</p>

{imgs[1]}

<h2>봄 캠핑 필수 준비물 체크리스트</h2>
<table><thead><tr><th>카테고리</th><th>아이템</th><th>비고</th></tr></thead><tbody>
<tr><td>잠자리</td><td>텐트, 타프, 슬리핑백(3계절용)</td><td>봄밤 기온 급강하 대비</td></tr>
<tr><td>취사</td><td>버너, 코펠, 식기류, 점화기</td><td>캠핑장 화기 규정 확인</td></tr>
<tr><td>전기</td><td>멀티탭, 랜턴, 보조배터리</td><td>전기 사이트 여부 확인</td></tr>
<tr><td>방충</td><td>모기향/매트, 방충 스프레이</td><td>봄 모기·벌레 활동 시작</td></tr>
<tr><td>방한</td><td>핫팩, 두꺼운 방한복, 방풍 재킷</td><td>새벽 기온 10도 이하</td></tr>
<tr><td>세면</td><td>수건, 세면도구, 슬리퍼</td><td>공용 샤워시설 확인</td></tr>
<tr><td>응급</td><td>구급함, 벌레 물림 약, 소독제</td><td>기본 상비약 필수</td></tr>
</tbody></table>

{cta_block("고캠핑에서 캠핑장 예약하기", "한국관광공사 운영 공식 캠핑장 예약 플랫폼", "https://www.gocamping.or.kr/", "green")}

<h2>초보자를 위한 봄 캠핑 꿀팁</h2>
<h3>날씨 & 기온</h3>
<ul>
<li>봄 캠핑의 최대 변수는 <strong>일교차</strong>입니다. 낮 기온이 20도여도 새벽에는 5~7도까지 떨어질 수 있으니 방한 준비를 철저히 하세요.</li>
<li>갑작스러운 봄비에 대비해 방수 타프는 필수입니다.</li>
</ul>
<h3>예약 & 사이트 선택</h3>
<ul>
<li>봄 성수기에는 인기 캠핑장이 2~3개월 전에 마감됩니다. 고캠핑(gocamping.or.kr) 사이트를 즐겨찾기 해두고 오픈 날짜를 놓치지 마세요.</li>
<li>초보자는 전기 사이트 + 화장실 인접 사이트를 선택하면 편리합니다.</li>
</ul>
<h3>쓰레기 처리</h3>
<ul>
<li>캠핑장 규정에 따라 쓰레기를 분리배출하세요. 종량제봉투를 챙겨가면 편리합니다.</li>
</ul>

{imgs[2]}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 차박용 매트는 어떤 것을 사야 하나요?</h3>
<p>A. 차종에 맞는 맞춤형 매트를 구매하는 것이 가장 좋습니다. SUV라면 2열 시트를 접고 트렁크와 연결되는 평탄화 매트를 추천합니다. 두께는 최소 7cm 이상이어야 편안하게 잠들 수 있습니다.</p>
<h3>Q. 글램핑과 일반 캠핑 비용 차이가 얼마나 나나요?</h3>
<p>A. 글램핑은 1박 기준 10~20만원, 일반 캠핑은 1~5만원 수준입니다. 글램핑은 침대, 에어컨, 조리도구 등이 제공되어 편의성이 높습니다.</p>
<h3>Q. 반려동물 동반 캠핑이 가능한 곳이 있나요?</h3>
<p>A. 고캠핑 검색 시 '반려동물 동반 가능' 필터로 조회할 수 있습니다. 대부분 목줄 착용 의무이며, 일부 캠핑장은 반려동물 전용 구역을 별도 운영합니다.</p>

{cta_block("캠핑 장비 준비부터 예약까지", "고캠핑 공식 사이트에서 전국 캠핑장을 비교하고 예약하세요", "https://www.gocamping.or.kr/", "yellow")}

<h2>마무리</h2>
<p>2026년 봄 캠핑 시즌이 성큼 다가왔습니다. 차박, 글램핑, 일반 캠핑 중 나의 취향과 준비 상황에 맞는 스타일을 선택하고, 위에서 소개한 명소들을 참고해 잊지 못할 봄 추억을 만들어 보세요. 무엇보다 예약은 빠를수록 좋습니다. 지금 바로 예약 캘린더를 확인해 보세요!</p>''',
    },

    # 3. 대학생활/캠퍼스룩/MT
    {
        "title": "2026 새학기 대학생활 캠퍼스룩 MT 준비 총정리",
        "cat": 13,
        "slug": "college-life-campus-look-mt-2026",
        "images": [
            ("photo-1523050854058-8df90110c5f6", "2026 새학기 대학생활"),
            ("photo-1517486808906-6ca8b3f04846", "캠퍼스룩 트렌드 2026"),
            ("photo-1571019614242-c5c5dee9f50b", "MT 준비물 체크리스트"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">새학기가 시작되는 3~4월은 설렘과 긴장이 교차하는 시기입니다. 새로운 친구들을 만나고, MT를 계획하고, 캠퍼스를 활보하는 즐거움이 가득한 계절이죠. <strong>2026 새학기</strong>를 맞이해 대학생활 꿀팁, 올봄 캠퍼스룩 트렌드, MT 준비물과 추천 게임까지 한 번에 정리했습니다. 대학 새내기부터 복학생까지 모두에게 도움이 되는 정보를 담았습니다.</p>

{imgs[0]}

<h2>대학생활 꿀팁 TOP 7</h2>

<h3>1. 수강신청 전략</h3>
<p>인기 강의는 수강신청 오픈과 동시에 마감됩니다. 미리 예비 수강신청 목록을 5~6개 만들어두고, 오픈 시간 1분 전부터 대기하세요. 분반이 여러 개라면 가장 빈 시간대부터 공략합니다.</p>

<h3>2. 교내 장학금 놓치지 않기</h3>
<p>성적 장학금 외에도 교내에는 다양한 종류의 장학금이 있습니다. 학생처 공지사항을 주기적으로 확인하고, 봉사활동·어학·창업 관련 장학금도 적극 지원하세요.</p>

<h3>3. 동아리·학회 활동</h3>
<p>대학의 핵심은 다양한 인연입니다. 전공 관련 학회나 관심 있는 동아리에 1~2개 가입해 네트워크를 넓히세요. 취업 시 큰 도움이 됩니다.</p>

<h3>4. 도서관 활용</h3>
<p>대학 도서관은 학술 데이터베이스, 전자책, 열람실 등 강력한 자원을 무료로 제공합니다. 스터디룸 예약 시스템을 익혀두면 그룹 스터디에 유용합니다.</p>

<h3>5. 시간 관리 앱 활용</h3>
<p>Notion, 구글 캘린더, 포레스트 등을 활용해 강의 스케줄과 과제 마감일을 한눈에 관리하세요.</p>

<h3>6. 교수님과의 소통</h3>
<p>오피스아워를 활용해 교수님과 대화하면 학점 관리뿐 아니라 진로 상담, 인턴십 추천서 등 다양한 기회가 열립니다.</p>

<h3>7. 건강 관리</h3>
<p>불규칙한 생활 패턴에 빠지기 쉬운 대학생활. 교내 헬스장이나 수영장을 활용해 규칙적인 운동 습관을 만들어두면 학업 효율도 높아집니다.</p>

{cta_block("내일배움카드로 자격증 준비하기", "대학생도 신청 가능한 국비지원 교육 정보를 확인하세요", "https://www.naeilshot.co.kr/", "blue")}

<h2>2026 봄 캠퍼스룩 트렌드</h2>
<p>2026년 봄 캠퍼스 패션은 <strong>Y2K 리바이벌</strong>과 <strong>미니멀 캐주얼</strong>의 두 가지 방향으로 나뉩니다.</p>
<table><thead><tr><th>트렌드</th><th>핵심 아이템</th><th>코디 팁</th></tr></thead><tbody>
<tr><td>Y2K 리바이벌</td><td>로우라이즈 데님, 크롭 후드, 컬러 선글라스</td><td>과감한 색상 조합 도전</td></tr>
<tr><td>미니멀 캐주얼</td><td>오버핏 화이트 셔츠, 슬랙스, 로퍼</td><td>뉴트럴 컬러로 단정하게</td></tr>
<tr><td>스포츠 믹스</td><td>트랙재킷, 와이드 팬츠, 스니커즈</td><td>상하 색상 통일감 주기</td></tr>
<tr><td>레이어드룩</td><td>얇은 가디건 + 슬립 원피스</td><td>일교차 대비 + 감성룩</td></tr>
<tr><td>아카데믹 룩</td><td>체크 블레이저, 옥스퍼드 셔츠</td><td>강의실과 카페 모두 OK</td></tr>
</tbody></table>

<h3>봄 캠퍼스룩 필수 아이템</h3>
<ul>
<li><strong>얇은 아우터</strong>: 봄바람에 대비한 가디건이나 후드 집업</li>
<li><strong>흰 스니커즈</strong>: 어떤 코디에도 잘 어울리는 만능 아이템</li>
<li><strong>미니 크로스백</strong>: 교재+필기도구+스마트폰을 담기 딱 좋은 사이즈</li>
<li><strong>선글라스</strong>: 봄 자외선 차단 + 패션 포인트</li>
</ul>

{imgs[1]}

<h2>MT 준비 완벽 가이드</h2>
<h3>MT 준비물 체크리스트</h3>
<table><thead><tr><th>카테고리</th><th>준비물</th><th>비고</th></tr></thead><tbody>
<tr><td>개인 위생</td><td>세면도구, 수건, 슬리퍼</td><td>공용 화장실 고려</td></tr>
<tr><td>의복</td><td>여벌 옷 2세트, 방한복, 운동복</td><td>야외 활동 대비</td></tr>
<tr><td>전자기기</td><td>보조배터리, 충전기, 이어폰</td><td>멀티탭 1개 챙기면 인기</td></tr>
<tr><td>먹거리</td><td>간식, 음료, 개인 컵</td><td>단체 식사와 별도 준비</td></tr>
<tr><td>약품</td><td>소화제, 두통약, 밴드</td><td>모두를 위해 챙기면 좋음</td></tr>
<tr><td>오락</td><td>폰 충전기, 보드게임, 간단한 소품</td><td>게임 아이디어 미리 준비</td></tr>
<tr><td>기타</td><td>슬리핑백 or 두꺼운 양말</td><td>바닥 냉기 대비</td></tr>
</tbody></table>

<h3>MT 게임 추천 BEST 5</h3>
<ul>
<li><strong>1. 빌런 게임</strong>: 랜덤으로 빌런 역할을 받아 자연스럽게 연기하는 사람을 찾는 관찰력 게임. 어색한 분위기를 단번에 깨줍니다.</li>
<li><strong>2. 노래방 배틀</strong>: 팀을 나눠 노래 점수를 합산하는 방식. 점수가 낮은 팀이 벌칙을 받습니다.</li>
<li><strong>3. 007 게임</strong>: 007, 빵, 총소리를 조합한 빠른 반응 게임. 단체 놀이의 고전이자 명작입니다.</li>
<li><strong>4. 인간 빙고</strong>: 빙고판의 칸을 채울 특징을 가진 사람을 찾아다니는 아이스브레이킹 게임. 서로를 빠르게 알아가는 데 효과적입니다.</li>
<li><strong>5. 탕! 게임</strong>: 원형으로 앉아 왼쪽·오른쪽을 외치며 손가락 총으로 지목하는 순발력 게임. 간단하지만 폭발적인 재미를 선사합니다.</li>
</ul>

{cta_block("내일배움카드 신청 안내", "대학생을 위한 국가기술자격 취득 지원 프로그램을 확인하세요", "https://www.naeilshot.co.kr/", "green")}

{imgs[2]}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 새내기인데 MT에 꼭 가야 하나요?</h3>
<p>A. 의무는 아니지만, MT는 새로운 인연을 빠르게 만들 수 있는 좋은 기회입니다. 처음에는 어색해도 게임을 몇 번 하면 금세 친해집니다. 가능하다면 참여를 추천합니다.</p>
<h3>Q. MT 비용은 보통 얼마인가요?</h3>
<p>A. 학교와 동아리마다 다르지만, 1박 2일 기준 1인당 3~7만원 수준이 일반적입니다. 음식비, 숙소비가 포함된 금액으로, 학생회가 지원하는 경우 더 저렴할 수 있습니다.</p>
<h3>Q. 캠퍼스룩을 저렴하게 구성하려면?</h3>
<p>A. 에이블리, 지그재그, 무신사 같은 패션 앱에서 시즌 세일을 노리거나, 중고 거래 앱(당근마켓, 번개장터)을 활용하면 합리적으로 구성할 수 있습니다.</p>

{cta_block("취업 준비도 미리미리!", "대학생부터 준비하는 내일배움카드 혜택을 확인하세요", "https://www.naeilshot.co.kr/", "yellow")}

<h2>마무리</h2>
<p>2026 새학기는 새로운 시작입니다. 수강신청부터 동아리, MT, 캠퍼스룩까지 철저히 준비해서 대학생활을 가장 알차게 보내보세요. 지금 이 순간이 나중에 가장 그리운 시절이 될 것입니다. 설레는 봄 학기, 마음껏 즐기세요!</p>''',
    },

    # 4. 체중감량/다이어트/식단관리
    {
        "title": "2026 봄 다이어트 체중감량 식단관리 방법 총정리",
        "cat": 13,
        "slug": "spring-diet-weight-loss-meal-plan-2026",
        "images": [
            ("photo-1490645935967-10de6ba17061", "봄 다이어트 식단관리"),
            ("photo-1512621776951-a57141f2eefd", "체중감량 건강 식단"),
            ("photo-1476224203421-9ac39bcb3327", "홈트레이닝 운동"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">봄이 오면 가장 먼저 떠오르는 것 중 하나가 바로 <strong>다이어트</strong>입니다. 겨울 동안 두꺼운 옷 속에 숨겨뒀던 몸을 가볍게 만들 수 있는 최적의 시즌이기도 합니다. 하지만 무작정 굶거나 과한 운동을 강행하면 오히려 요요 현상과 건강 악화로 이어질 수 있습니다. 이 글에서는 <strong>2026년 봄에 효과적으로 체중을 감량하는 방법</strong>을 목표 설정부터 주간 식단표, 칼로리 계산법, 홈트레이닝, 간헐적 단식까지 과학적 근거를 바탕으로 정리합니다.</p>

{imgs[0]}

<h2>체중감량 목표 설정 방법</h2>
<p>효과적인 다이어트의 첫 번째 단계는 <strong>현실적인 목표 설정</strong>입니다. 한 달에 1~2kg 감량이 건강하고 지속 가능한 목표입니다.</p>
<h3>SMART 목표 설정법</h3>
<ul>
<li><strong>S (Specific)</strong>: "살 빼기"가 아닌 "8주 안에 4kg 감량"처럼 구체적으로</li>
<li><strong>M (Measurable)</strong>: 체중계, 줄자, 체지방 측정기로 수치화</li>
<li><strong>A (Achievable)</strong>: 주당 0.5~1kg 감량 — 과도한 목표는 포기로 이어짐</li>
<li><strong>R (Relevant)</strong>: 건강 개선, 체력 향상 등 자신의 동기와 연결</li>
<li><strong>T (Time-bound)</strong>: 봄 시즌 종료인 6월 말을 최종 목표일로 설정</li>
</ul>
<h3>기초 대사량(BMR) 계산</h3>
<table><thead><tr><th>성별</th><th>계산식</th></tr></thead><tbody>
<tr><td>남성</td><td>BMR = 88.36 + (13.4 × 체중kg) + (4.8 × 키cm) − (5.7 × 나이)</td></tr>
<tr><td>여성</td><td>BMR = 447.6 + (9.2 × 체중kg) + (3.1 × 키cm) − (4.3 × 나이)</td></tr>
</tbody></table>
<p>계산된 BMR에 활동 계수(좌식: ×1.2, 가벼운 운동: ×1.375, 중등도 운동: ×1.55)를 곱하면 <strong>일일 유지 칼로리</strong>가 나옵니다. 여기서 하루 300~500kcal를 줄이면 건강한 감량이 시작됩니다.</p>

{cta_block("식품안전나라에서 영양 정보 확인", "칼로리·영양소 데이터를 무료로 조회하고 식단을 설계하세요", "https://www.foodsafetykorea.go.kr/", "blue")}

<h2>2026 봄 추천 주간 식단표</h2>
<p>아래는 1,600~1,800kcal 기준의 봄철 다이어트 식단 예시입니다. 개인 BMR에 따라 칼로리를 조절하세요.</p>
<table><thead><tr><th>요일</th><th>아침</th><th>점심</th><th>저녁</th></tr></thead><tbody>
<tr><td>월</td><td>귀리오트밀+바나나</td><td>닭가슴살 샐러드+통밀빵</td><td>두부미역국+현미밥 1/2공기</td></tr>
<tr><td>화</td><td>달걀 2개+방울토마토</td><td>비빔밥(고기 제외)+된장국</td><td>연어구이+샐러드</td></tr>
<tr><td>수</td><td>그릭요거트+블루베리</td><td>잡채(당면 줄이기)+나물 반찬</td><td>닭가슴살 볶음+브로콜리</td></tr>
<tr><td>목</td><td>통밀토스트+아보카도</td><td>현미밥+생선구이+나물</td><td>달걀찜+시금치나물+미소국</td></tr>
<tr><td>금</td><td>귀리오트밀+견과류</td><td>닭가슴살 덮밥(소스 줄이기)</td><td>두부조림+현미밥 1/2공기</td></tr>
<tr><td>토</td><td>달걀 오믈렛+채소</td><td>자유식 (과식 주의)</td><td>채소 듬뿍 된장찌개</td></tr>
<tr><td>일</td><td>스무디(시금치+바나나+단백질파우더)</td><td>현미 주먹밥+미역국</td><td>닭가슴살 샤브샤브</td></tr>
</tbody></table>

{imgs[1]}

<h2>칼로리 계산 실전 팁</h2>
<h3>추천 칼로리 추적 앱</h3>
<ul>
<li><strong>눔(Noom)</strong>: 심리 코칭 방식으로 식습관 개선에 초점</li>
<li><strong>다이어트 신(Diet Shin)</strong>: 한국 음식 데이터가 풍부한 국내 앱</li>
<li><strong>마이피트니스팔(MyFitnessPal)</strong>: 전 세계 1,400만 개 이상 식품 데이터 보유</li>
</ul>
<h3>외식 시 칼로리 줄이는 법</h3>
<ul>
<li>소스는 따로 받아 찍어 먹기</li>
<li>밥 대신 샐러드 or 밥 절반으로 줄이기</li>
<li>음료는 무조건 물 또는 무당 아이스티</li>
<li>튀김보다 구이, 볶음보다 찜 선택</li>
</ul>

<h2>봄 홈트레이닝 루틴</h2>
<h3>주 4회 기본 루틴 (각 30분)</h3>
<table><thead><tr><th>요일</th><th>운동</th><th>세트×횟수</th></tr></thead><tbody>
<tr><td>월·목</td><td>스쿼트, 런지, 플랭크, 버피</td><td>3세트×15회</td></tr>
<tr><td>화·금</td><td>푸시업, 마운틴 클라이머, 점프스쿼트</td><td>3세트×12회</td></tr>
</tbody></table>
<p>운동 전후 스트레칭 5분은 필수입니다. 봄철 야외 러닝도 적극 추천하며, 30분 이상 걷기만 해도 유산소 효과를 볼 수 있습니다.</p>

<h2>간헐적 단식 실전 가이드</h2>
<p>가장 인기 있는 방식은 <strong>16:8 단식</strong>(16시간 공복, 8시간 식사 허용)입니다.</p>
<ul>
<li><strong>시작 시간 예시</strong>: 오전 12시에 첫 식사 → 오후 8시 마지막 식사 → 이후 공복 유지</li>
<li><strong>공복 중 허용</strong>: 물, 블랙커피(무당), 허브티</li>
<li><strong>주의사항</strong>: 당뇨, 저혈압, 임산부는 반드시 의사 상담 후 시행</li>
</ul>

{cta_block("식품영양성분 데이터베이스 활용하기", "식품안전나라에서 정확한 칼로리와 영양 정보를 확인하세요", "https://www.foodsafetykorea.go.kr/", "green")}

{imgs[2]}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 유산소 운동과 근력 운동 중 어느 것이 더 효과적인가요?</h3>
<p>A. 체중 감량만 목표라면 유산소가 효율적이지만, 장기적으로는 근력 운동으로 기초 대사량을 높이는 것이 더 지속 가능한 방법입니다. 두 가지를 병행하는 것이 가장 이상적입니다.</p>
<h3>Q. 다이어트 중 단백질 섭취는 어떻게 해야 하나요?</h3>
<p>A. 체중 1kg당 1.2~1.5g의 단백질을 섭취하는 것이 근손실 방지에 효과적입니다. 닭가슴살, 달걀, 두부, 그릭요거트, 단백질 쉐이크가 좋은 선택입니다.</p>
<h3>Q. 다이어트 중 치팅데이가 필요한가요?</h3>
<p>A. 완전한 치팅데이보다 주 1회 '여유 식사'를 허용하는 방식이 심리적 지속력을 높입니다. 과식으로 이어지지 않도록 식사량 기준을 미리 정해두세요.</p>

{cta_block("올바른 식품 정보 확인하기", "식품안전나라에서 다이어트 식품의 영양 성분을 꼼꼼히 체크하세요", "https://www.foodsafetykorea.go.kr/", "yellow")}

<h2>마무리</h2>
<p>봄 다이어트의 핵심은 <strong>급격한 변화가 아닌 지속 가능한 습관 만들기</strong>입니다. 목표 칼로리를 설정하고, 균형 잡힌 식단과 규칙적인 운동을 병행하면 8~12주 안에 눈에 띄는 변화를 경험할 수 있습니다. 오늘부터 작은 한 걸음을 내딛어 보세요. 여름이 오기 전에 분명 후회 없는 결과를 만들 수 있습니다.</p>''',
    },

    # 5. 황사/미세먼지/산불예방
    {
        "title": "2026 봄 황사 미세먼지 대처법 산불예방 행동수칙 총정리",
        "cat": 13,
        "slug": "yellow-dust-fine-dust-forest-fire-prevention-2026",
        "images": [
            ("photo-1527482797697-8795b05a13fe", "2026 봄 황사 미세먼지 대처법"),
            ("photo-1534088568595-a066f410bcda", "미세먼지 등급 확인 방법"),
            ("photo-1558618666-fcd25c85f82e", "산불예방 행동수칙"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">봄은 따뜻하고 아름다운 계절이지만, 동시에 <strong>황사와 미세먼지, 산불</strong>이 집중되는 위험한 시기이기도 합니다. 중국 북부와 몽골의 건조한 토양이 강한 바람에 실려 한반도로 날아오는 황사, 그리고 건조한 날씨에 급격히 확산되는 산불은 매년 봄철 우리의 건강과 안전을 위협합니다. 2026년 봄, 미세먼지 등급표와 대처법, 실시간 확인 방법, 산불 예방 수칙과 신고 절차까지 완벽하게 정리했습니다.</p>

{imgs[0]}

<h2>미세먼지·초미세먼지 등급표</h2>
<p>미세먼지(PM10)와 초미세먼지(PM2.5)는 농도에 따라 4단계로 구분합니다.</p>
<table><thead><tr><th>등급</th><th>PM10 (㎍/㎥)</th><th>PM2.5 (㎍/㎥)</th><th>건강 영향</th><th>행동 요령</th></tr></thead><tbody>
<tr><td style="color:#4ade80;font-weight:bold;">좋음</td><td>0~30</td><td>0~15</td><td>영향 없음</td><td>야외 활동 자유롭게</td></tr>
<tr><td style="color:#facc15;font-weight:bold;">보통</td><td>31~80</td><td>16~35</td><td>민감군 약한 영향</td><td>민감군 장시간 야외 자제</td></tr>
<tr><td style="color:#fb923c;font-weight:bold;">나쁨</td><td>81~150</td><td>36~75</td><td>호흡기·심혈관 자극</td><td>마스크 착용, 외출 자제</td></tr>
<tr><td style="color:#ef4444;font-weight:bold;">매우나쁨</td><td>151 이상</td><td>76 이상</td><td>심각한 건강 피해</td><td>외출 금지, 창문 닫기</td></tr>
</tbody></table>
<p><strong>민감군</strong>: 어린이, 노인, 임산부, 호흡기·심혈관 질환자는 '보통' 등급부터 주의가 필요합니다.</p>

{cta_block("에어코리아에서 실시간 미세먼지 확인", "전국 대기질 지수를 실시간으로 확인하고 건강을 지키세요", "https://www.airkorea.or.kr/", "blue")}

<h2>황사·미세먼지 대처법</h2>
<h3>야외에서</h3>
<ul>
<li><strong>KF94 마스크 착용</strong>: KF80 이상 인증 마스크를 착용하되, 얼굴에 밀착되도록 착용하는 것이 중요합니다.</li>
<li><strong>눈 보호</strong>: 황사가 심한 날은 렌즈 대신 안경을 착용하고, 눈에 이물감이 있으면 깨끗한 물로 씻어내세요.</li>
<li><strong>피부 노출 최소화</strong>: 긴팔 옷을 입고 귀가 후 즉시 샤워하세요.</li>
<li><strong>외출 후 손씻기</strong>: 비누로 20초 이상 손을 씻는 것이 기본입니다.</li>
</ul>
<h3>실내에서</h3>
<ul>
<li><strong>창문 닫기</strong>: 미세먼지 나쁨 이상이면 창문을 닫고 공기청정기를 가동하세요.</li>
<li><strong>환기</strong>: 미세먼지가 '좋음'이나 '보통'인 시간대(보통 오전 6~8시, 오후 6~8시)에 짧게 환기하세요.</li>
<li><strong>물 자주 마시기</strong>: 수분 섭취를 늘려 호흡기 점막을 보호합니다.</li>
</ul>

{imgs[1]}

<h2>실시간 미세먼지 확인 앱 추천</h2>
<table><thead><tr><th>앱 이름</th><th>특징</th><th>플랫폼</th></tr></thead><tbody>
<tr><td>에어코리아</td><td>환경부 공식 데이터, 가장 정확</td><td>iOS/Android</td></tr>
<tr><td>미세미세</td><td>직관적 UI, 내일 예보 제공</td><td>iOS/Android</td></tr>
<tr><td>케어러(Carer)</td><td>건강 취약계층 맞춤 알림</td><td>iOS/Android</td></tr>
<tr><td>위즈날씨</td><td>날씨+미세먼지 통합 제공</td><td>iOS/Android</td></tr>
<tr><td>Plume Labs</td><td>글로벌 데이터, 이동 경로별 오염도 제공</td><td>iOS/Android</td></tr>
</tbody></table>

<h2>봄철 산불 예방 수칙</h2>
<p>봄은 강수량이 적고 바람이 강해 산불이 가장 많이 발생하는 계절입니다. 산림청 통계에 따르면 전체 산불의 약 40%가 3~5월에 집중됩니다.</p>
<h3>산불 예방 10대 수칙</h3>
<ol>
<li>입산 통제 구역에는 절대 들어가지 않기</li>
<li>산 속 야영, 취사 시 지정된 장소에서만</li>
<li>산에서 담배 피우지 않기 (등산로 포함)</li>
<li>논·밭두렁, 쓰레기 소각 절대 금지</li>
<li>산행 전 입산 가능 여부 확인 (산림청 앱)</li>
<li>건조주의보 발령 시 입산 자제</li>
<li>캠프파이어 및 모닥불 금지</li>
<li>산 인근 주차 시 촉매 과열로 인한 화재 주의</li>
<li>등산 중 라이터, 성냥 소지 자제</li>
<li>어린이가 불을 가지고 놀지 않도록 교육</li>
</ol>

<h3>산불 신고 방법</h3>
<table><thead><tr><th>신고 수단</th><th>번호/방법</th><th>비고</th></tr></thead><tbody>
<tr><td>산불신고 전화</td><td>119 또는 산림청 1588-3119</td><td>24시간 운영</td></tr>
<tr><td>산림청 앱</td><td>스마트 산림재해</td><td>GPS 위치 자동 전송</td></tr>
<tr><td>경찰</td><td>112</td><td>야간·긴급 상황 시</td></tr>
</tbody></table>
<p>산불 발견 시 <strong>신속 대피가 최우선</strong>입니다. 연기가 있는 방향의 반대쪽으로 이동하고, 연기를 마셨을 경우 낮은 자세로 이동하세요.</p>

{cta_block("에어코리아 대기질 정보 확인", "오늘의 미세먼지 등급과 황사 예보를 지금 바로 확인하세요", "https://www.airkorea.or.kr/", "green")}

{imgs[2]}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 황사와 미세먼지는 다른가요?</h3>
<p>A. 황사는 중국·몽골 사막의 모래 먼지가 바람을 타고 날아오는 자연현상으로 주로 굵은 입자(PM10)로 구성됩니다. 미세먼지는 공장·자동차 등 인위적 오염원에서 발생하는 PM2.5 이하의 극미세 입자입니다. 봄철에는 두 가지가 복합적으로 나타나는 경우가 많습니다.</p>
<h3>Q. KF94와 KF80 마스크의 차이는?</h3>
<p>A. KF94는 0.4㎛ 입자를 94% 이상 차단, KF80은 0.6㎛ 입자를 80% 이상 차단합니다. 초미세먼지(PM2.5)가 심한 날은 KF94 이상을 착용하는 것이 안전합니다.</p>
<h3>Q. 산불이 가까이 오면 어떻게 해야 하나요?</h3>
<p>A. 즉시 119에 신고하고 안전한 방향으로 대피하세요. 불길보다 연기가 더 위험할 수 있으니 수건으로 코와 입을 막고 낮은 자세를 유지하며 이동합니다. 차량으로 이동 시 헤드라이트를 켜고 천천히 운전하세요.</p>

{cta_block("실시간 대기질 모니터링", "에어코리아 공식 앱으로 황사·미세먼지를 미리 체크하세요", "https://www.airkorea.or.kr/", "yellow")}

<h2>마무리</h2>
<p>2026년 봄도 황사와 미세먼지, 산불의 위협은 계속될 것입니다. 에어코리아 앱을 즐겨찾기에 추가하고, 미세먼지 나쁨 이상인 날에는 KF94 마스크를 반드시 착용하세요. 산에 오를 때는 산불 예방 수칙을 철저히 지켜 소중한 자연과 우리 모두의 안전을 함께 지킵시다.</p>''',
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

    # 4) 네이버/Bing/Yandex IndexNow 제출
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

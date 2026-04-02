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

# ========== 4개 포스트 정의 ==========
POSTS = [
    # 1. 환절기/춘곤증/알레르기
    {
        "title": "2026 봄 환절기 춘곤증 극복법 알레르기 예방 총정리",
        "cat": 13,
        "slug": "spring-fatigue-allergy-prevention-2026",
        "images": [
            ("photo-1544367567-0f2fcb009e0b", "봄 환절기 춘곤증 극복법"),
            ("photo-1556909114-f6e7ad7d3136", "봄철 알레르기 예방"),
            ("photo-1507003211169-0a1dd7228f2d", "환절기 건강 관리"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">3월이 되면 어김없이 찾아오는 <strong>춘곤증</strong>과 <strong>봄철 알레르기</strong>. 낮에는 따뜻하고 아침저녁으로는 쌀쌀한 환절기 날씨가 우리 몸을 혼란스럽게 합니다. 쉽게 피로해지고, 눈이 간지럽고, 코가 막히는 증상이 반복된다면 이미 환절기의 영향을 받고 있는 것입니다. 2026년 봄, 춘곤증의 원인부터 극복법, 알레르기 예방까지 한 번에 정리했습니다.</p>

{imgs[0]}

<h2>춘곤증이란? 원인과 주요 증상</h2>
<p><strong>춘곤증(春困症)</strong>은 봄철 계절 변화에 적응하는 과정에서 나타나는 일시적인 피로 증후군입니다. 질병이 아닌 생리적 반응이지만, 일상생활에 큰 지장을 주는 경우도 많습니다.</p>
<h3>춘곤증의 주요 원인</h3>
<ul>
<li><strong>일조시간 증가</strong>: 낮이 길어지면서 생체리듬이 변화하고 수면 패턴이 흔들립니다.</li>
<li><strong>기온 상승</strong>: 따뜻해진 날씨에 신진대사가 활발해지면서 에너지 소비가 증가합니다.</li>
<li><strong>비타민·미네랄 부족</strong>: 겨울 동안 쌓인 영양소 부족이 봄에 증상으로 표면화됩니다.</li>
<li><strong>호르몬 변화</strong>: 계절 전환기에 멜라토닌과 세로토닌 분비량이 변화합니다.</li>
</ul>
<h3>춘곤증 주요 증상</h3>
<table><thead><tr><th>증상</th><th>설명</th><th>지속 기간</th></tr></thead><tbody>
<tr><td>낮 졸음</td><td>식후 특히 심한 졸음, 집중력 저하</td><td>2~4주</td></tr>
<tr><td>만성 피로</td><td>충분히 자도 피곤한 느낌 지속</td><td>2~6주</td></tr>
<tr><td>소화 불량</td><td>식욕 감소, 더부룩함</td><td>1~3주</td></tr>
<tr><td>두통·어지럼증</td><td>기온차로 인한 혈압 변동</td><td>불규칙</td></tr>
<tr><td>무기력·의욕 저하</td><td>신체 활동 감소, 집중 어려움</td><td>2~4주</td></tr>
</tbody></table>

<h2>춘곤증 극복법 7가지</h2>
<p>춘곤증은 생활 습관 개선으로 충분히 완화할 수 있습니다. 아래 7가지 방법을 꾸준히 실천해 보세요.</p>
<ol>
<li><strong>규칙적인 수면 습관 유지</strong>: 매일 같은 시간에 자고 일어나세요. 성인은 7~8시간 수면이 적절합니다.</li>
<li><strong>가벼운 스트레칭과 운동</strong>: 아침에 10~15분 스트레칭만으로도 혈액순환을 개선할 수 있습니다. 점심 후 짧은 산책도 효과적입니다.</li>
<li><strong>비타민 B군 섭취</strong>: 피로 회복의 핵심인 비타민 B1(티아민)이 풍부한 현미, 돼지고기, 콩류를 챙겨 드세요.</li>
<li><strong>수분 보충 철저히</strong>: 봄에는 건조한 날씨로 수분이 부족해지기 쉽습니다. 하루 1.5~2L 물을 마시세요.</li>
<li><strong>점심 식사 후 낮잠 10~20분</strong>: 짧은 낮잠은 오후 업무 효율을 크게 높여줍니다. 30분 이상은 오히려 역효과.</li>
<li><strong>카페인 의존 줄이기</strong>: 커피로 잠을 쫓으면 밤 수면의 질이 떨어지는 악순환이 생깁니다.</li>
<li><strong>햇볕 쬐기</strong>: 세로토닌 분비를 촉진하는 자연광에 하루 30분 이상 노출되는 것이 좋습니다.</li>
</ol>

{cta_block("질병관리청 건강 정보 확인하기", "춘곤증과 환절기 건강 관리에 대한 공식 정보를 확인하세요", "https://www.kdca.go.kr/", "blue")}

{imgs[1]}

<h2>봄철 알레르기 종류와 원인</h2>
<p>봄철 알레르기는 꽃가루, 황사, 미세먼지 등 다양한 원인으로 발생합니다. 알레르기 종류에 따라 대처법도 달라지므로 정확히 파악하는 것이 중요합니다.</p>
<h3>1. 꽃가루 알레르기</h3>
<p>3~5월은 오리나무, 자작나무, 소나무, 참나무 등의 꽃가루가 절정에 달하는 시기입니다. 2026년 기상청 예보에 따르면 3월 하순부터 꽃가루 농도가 높아져 알레르기 환자들의 각별한 주의가 필요합니다.</p>
<h3>2. 알레르기 비염</h3>
<p>콧물, 재채기, 코막힘이 주요 증상입니다. 꽃가루 외에도 집먼지진드기, 곰팡이 포자도 비염을 악화시킵니다.</p>
<h3>3. 봄철 피부 트러블</h3>
<p>건조한 공기와 갑작스런 기온 변화로 피부 장벽이 약해지며 아토피, 접촉성 피부염이 악화될 수 있습니다.</p>
<table><thead><tr><th>알레르기 종류</th><th>주요 원인</th><th>주요 증상</th><th>피크 시기</th></tr></thead><tbody>
<tr><td>꽃가루 알레르기</td><td>오리나무·자작나무 꽃가루</td><td>눈 가려움, 재채기</td><td>3~4월</td></tr>
<tr><td>알레르기 비염</td><td>꽃가루, 집먼지진드기</td><td>콧물, 코막힘, 두통</td><td>3~5월</td></tr>
<tr><td>피부 알레르기</td><td>황사, 미세먼지, 꽃가루</td><td>두드러기, 가려움</td><td>4~5월</td></tr>
<tr><td>결막염</td><td>꽃가루, 미세먼지</td><td>눈 충혈, 눈물</td><td>3~5월</td></tr>
</tbody></table>

<h2>봄철 알레르기 예방법</h2>
<ul>
<li><strong>외출 시 마스크 착용</strong>: KF80 이상의 보건용 마스크가 꽃가루 차단에 효과적입니다.</li>
<li><strong>꽃가루 지수 확인</strong>: 기상청 생활기상지수(www.weather.go.kr)에서 꽃가루 농도를 미리 확인하세요.</li>
<li><strong>귀가 후 즉시 샤워</strong>: 외출 후에는 눈, 코, 피부에 묻은 꽃가루를 씻어내야 합니다.</li>
<li><strong>환기 시간대 선택</strong>: 꽃가루는 오전 6~10시에 가장 많이 날립니다. 환기는 오후로 미루세요.</li>
<li><strong>항히스타민제 상비</strong>: 알레르기 증상이 심한 분은 의사 처방 항히스타민제를 미리 준비하세요.</li>
<li><strong>실내 공기청정기 가동</strong>: HEPA 필터가 장착된 공기청정기가 꽃가루 제거에 효과적입니다.</li>
</ul>

<h2>환절기 건강 관리에 좋은 식품</h2>
<p>음식으로 면역력을 높이고 알레르기 반응을 줄일 수 있습니다.</p>
<table><thead><tr><th>식품</th><th>효능</th><th>섭취 방법</th></tr></thead><tbody>
<tr><td>냉이·달래·쑥갓</td><td>비타민·미네랄 풍부, 면역 강화</td><td>나물, 국, 된장국</td></tr>
<tr><td>생강</td><td>항염·항히스타민 효과</td><td>생강차, 요리 양념</td></tr>
<tr><td>꿀</td><td>항균·항산화, 면역 조절</td><td>하루 1스푼, 차에 넣기</td></tr>
<tr><td>연어·고등어</td><td>오메가3로 알레르기 반응 완화</td><td>주 2~3회 섭취</td></tr>
<tr><td>블루베리·딸기</td><td>항산화 플라보노이드</td><td>아침 식사 또는 간식</td></tr>
</tbody></table>

{imgs[2]}

<h2>병원 진료가 필요한 시기</h2>
<p>대부분의 춘곤증과 경미한 알레르기는 생활 습관 개선으로 나아지지만, 다음과 같은 경우에는 반드시 전문의 진료를 받으세요.</p>
<ul>
<li>피로감이 <strong>6주 이상</strong> 지속될 때</li>
<li>알레르기 증상이 <strong>시중 약으로 개선되지 않을 때</strong></li>
<li>호흡 곤란이나 <strong>천명음(쌕쌕거림)</strong>이 동반될 때</li>
<li>눈 충혈이 <strong>1주일 이상 호전되지 않을 때</strong></li>
<li>피부 두드러기가 <strong>전신으로 퍼질 때</strong></li>
</ul>

{cta_block("질병관리청에서 알레르기 예방 정보 확인", "봄철 알레르기 예방 수칙과 병원 정보를 공식 사이트에서 확인하세요", "https://www.kdca.go.kr/", "green")}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 춘곤증과 만성피로증후군은 다른가요?</h3>
<p>A. 춘곤증은 봄 환절기에 일시적으로 나타나는 피로감으로, 보통 4~6주 이내에 호전됩니다. 반면 만성피로증후군은 6개월 이상 지속되며 일상생활에 심각한 지장을 줍니다. 피로가 장기화된다면 전문의 상담을 받아보세요.</p>
<h3>Q. 꽃가루 알레르기가 있는데 봄에 외출을 완전히 피해야 하나요?</h3>
<p>A. 완전한 회피는 현실적으로 어렵습니다. KF80 이상 마스크 착용, 선글라스 착용, 꽃가루 지수가 낮은 오후 시간대 외출, 귀가 후 즉시 씻기 등 방어 전략을 세우면 일상생활이 충분히 가능합니다.</p>
<h3>Q. 알레르기 비염과 감기를 어떻게 구별하나요?</h3>
<p>A. 감기는 발열, 인후통, 근육통을 동반하며 1~2주 내 회전되지만, 알레르기 비염은 발열 없이 맑은 콧물·재채기·코막힘이 반복되고 수주~수개월 지속됩니다. 특히 특정 장소나 물질에 노출될 때 증상이 악화되면 알레르기를 의심하세요.</p>
<h3>Q. 춘곤증에 좋은 영양제가 있나요?</h3>
<p>A. 비타민 B 복합체, 비타민 C, 마그네슘이 에너지 대사와 피로 회복에 도움을 줍니다. 단, 영양제는 보조 수단이며 균형 잡힌 식사가 우선입니다.</p>

<h2>마무리</h2>
<p>봄은 새 출발의 계절이지만 우리 몸에는 적응의 시간이 필요합니다. 춘곤증과 알레르기는 누구에게나 찾아올 수 있지만, 규칙적인 생활, 충분한 영양 섭취, 그리고 적절한 예방 조치로 충분히 건강한 봄을 보낼 수 있습니다. 올봄엔 미리 준비해서 활기차고 건강한 하루하루를 만들어가세요!</p>''',
    },

    # 2. 봄맞이 대청소/봄 옷 정리
    {
        "title": "2026 봄맞이 대청소 체크리스트 옷 정리 수납 꿀팁 총정리",
        "cat": 13,
        "slug": "spring-cleaning-closet-organization-2026",
        "images": [
            ("photo-1584622650111-993a426fbf0a", "봄맞이 대청소 체크리스트"),
            ("photo-1558317374-067fb5f30001", "봄 옷 정리 수납 꿀팁"),
            ("photo-1527515637462-cee1cc710a97", "겨울옷 정리 보관 방법"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">겨울이 지나고 봄이 찾아오면 자연스럽게 <strong>봄맞이 대청소</strong>를 해야겠다는 마음이 생깁니다. 오랫동안 닫혀 있던 창문을 열고 묵은 먼지를 털어내는 일, 두꺼운 겨울옷을 정리하고 봄 옷장을 새롭게 꾸미는 일은 단순한 청소를 넘어 마음의 환기이기도 합니다. 2026년 봄, 방별 체크리스트와 옷 정리 꿀팁으로 더 빠르고 깔끔하게 봄맞이를 완성하세요.</p>

{imgs[0]}

<h2>봄맞이 대청소 순서</h2>
<p>무작정 시작하면 중간에 지치기 쉽습니다. 다음 3단계 순서로 진행하면 효율적으로 대청소를 마칠 수 있습니다.</p>
<ol>
<li><strong>1단계 - 버리기</strong>: 모든 공간에서 필요 없는 물건을 먼저 분류합니다. 비워야 닦을 수 있습니다.</li>
<li><strong>2단계 - 위에서 아래로 청소</strong>: 천장 → 벽 → 가구 → 바닥 순서로 먼지가 아래로 내려오는 방향을 따릅니다.</li>
<li><strong>3단계 - 수납 및 정리</strong>: 청소 후 물건을 제자리에 돌려놓고 수납 도구를 활용해 정돈합니다.</li>
</ol>

<h2>방별 청소 체크리스트</h2>
<table><thead><tr><th>공간</th><th>청소 항목</th><th>주기</th></tr></thead><tbody>
<tr><td>거실</td><td>소파 쿠션 세탁, 커튼 세탁, 에어컨 필터 청소, TV 뒤·아래 먼지 제거</td><td>연 1~2회</td></tr>
<tr><td>주방</td><td>냉장고 내부 정리, 환풍기 필터 세척, 가스레인지 그리스 청소, 찬장 내부 닦기</td><td>연 2회</td></tr>
<tr><td>욕실</td><td>줄눈 곰팡이 제거, 샤워헤드 스케일 제거, 배수구 청소, 수납장 정리</td><td>연 2~4회</td></tr>
<tr><td>침실</td><td>매트리스 진드기 제거, 이불·베개 커버 세탁, 옷장 정리, 창틀 닦기</td><td>연 1~2회</td></tr>
<tr><td>베란다</td><td>바닥 물청소, 화분 정리, 창문 프레임 청소, 방충망 세척</td><td>연 2회</td></tr>
</tbody></table>

<h3>에어컨 필터 청소 꿀팁</h3>
<p>에어컨 필터는 여름 시즌 전인 봄에 반드시 청소해야 합니다. 필터를 꺼내 물에 담갔다가 부드러운 솔로 먼지를 제거하고 그늘에서 완전 건조 후 다시 장착하세요. 2주에 한 번 가볍게 청소하면 냉방 효율이 최대 15% 향상됩니다.</p>

{cta_block("중고거래로 안 쓰는 물건 정리하기", "당근마켓에서 안 쓰는 겨울 물건과 옷을 이웃과 나눠보세요", "https://www.daangn.com/", "yellow")}

{imgs[1]}

<h2>겨울옷 정리와 보관법</h2>
<p>봄이 오면 두꺼운 겨울옷을 어떻게 정리하느냐에 따라 내년 겨울 옷의 상태가 달라집니다.</p>
<h3>겨울옷 보관 전 필수 체크</h3>
<ul>
<li><strong>세탁 먼저</strong>: 눈에 보이지 않는 땀, 피지, 음식 얼룩이 있으면 보관 중 변색·충해가 생깁니다. 반드시 세탁 후 보관하세요.</li>
<li><strong>완전 건조 확인</strong>: 습기가 남아 있으면 곰팡이가 생깁니다. 햇볕에 충분히 말린 후 보관하세요.</li>
<li><strong>방충제 함께 보관</strong>: 울, 캐시미어 소재는 좀벌레에 취약합니다. 방충제를 넣어 보관하세요.</li>
</ul>
<h3>소재별 보관 방법</h3>
<table><thead><tr><th>소재</th><th>보관 방법</th><th>주의사항</th></tr></thead><tbody>
<tr><td>패딩·다운</td><td>전용 압축팩보다 통기성 있는 의류 커버</td><td>압축 보관 시 솜털 복원력 저하</td></tr>
<tr><td>울·캐시미어</td><td>접어서 수납, 방충제 필수</td><td>세탁 후 뉘어 건조</td></tr>
<tr><td>니트류</td><td>접어서 수납, 행거 금지</td><td>걸면 늘어남</td></tr>
<tr><td>청바지·면류</td><td>접거나 행거 모두 가능</td><td>세탁 후 뒤집어 건조</td></tr>
</tbody></table>

<h2>옷장 정리 꿀팁 5가지</h2>
<ol>
<li><strong>색상별·계절별 분류</strong>: 봄/여름 옷은 꺼내기 쉬운 앞쪽에, 가을/겨울 옷은 안쪽이나 상단에 수납합니다.</li>
<li><strong>1년 법칙 적용</strong>: 지난 1년 동안 한 번도 입지 않은 옷은 과감히 버리거나 중고거래에 내놓으세요.</li>
<li><strong>수납 박스 활용</strong>: 티셔츠는 세워서 수납하면 한눈에 보이고 공간도 절약됩니다.</li>
<li><strong>행거 통일</strong>: 얇은 벨벳 행거로 통일하면 수납 공간이 30~40% 늘어납니다.</li>
<li><strong>문등 수납 활용</strong>: 옷장 문 안쪽에 걸이를 달면 스카프, 벨트 등 잡화 수납에 유용합니다.</li>
</ol>

{imgs[2]}

<h2>중고거래로 겨울옷 처분하기</h2>
<p>정리하다 보면 처분해야 할 옷들이 생깁니다. 버리기 아깝다면 중고거래를 활용해 보세요.</p>
<table><thead><tr><th>플랫폼</th><th>특징</th><th>추천 품목</th></tr></thead><tbody>
<tr><td>당근마켓</td><td>동네 주민 거래, 직거래 중심</td><td>일상복, 생활용품</td></tr>
<tr><td>번개장터</td><td>전국 택배 거래, 브랜드 제품</td><td>패딩, 코트, 스포츠웨어</td></tr>
<tr><td>중고나라</td><td>다양한 카테고리, 대량 거래</td><td>시즌 아웃 의류 묶음</td></tr>
</tbody></table>
<p>옷 사진은 <strong>밝은 자연광 아래</strong>에서 촬영하고, 소재·사이즈·세탁 횟수·브랜드 정보를 상세히 적으면 빠르게 판매됩니다.</p>

<h2>추천 청소 도구 리스트</h2>
<ul>
<li><strong>고압 물걸레 청소기</strong>: 욕실 바닥, 베란다 타일 청소에 효과적</li>
<li><strong>강력 다목적 세정제</strong>: 주방 기름때, 욕실 물때 제거</li>
<li><strong>마이크로파이버 걸레</strong>: 가구 표면, 창틀 먼지 제거</li>
<li><strong>창틀 청소 솔</strong>: 홈이 있는 창틀 틈새 청소 전용</li>
<li><strong>스팀 청소기</strong>: 매트리스, 소파의 진드기와 살균</li>
</ul>

{cta_block("당근마켓에서 안 쓰는 물건 정리하기", "동네 이웃과 중고거래로 새 출발을 준비해 보세요", "https://www.daangn.com/", "green")}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 봄 대청소는 며칠에 걸쳐 하는 게 좋을까요?</h3>
<p>A. 30평대 아파트 기준으로 방별로 나눠 3~4일에 걸쳐 진행하는 것이 무리 없이 완성할 수 있는 방법입니다. 하루에 한두 공간씩 집중하면 지치지 않습니다.</p>
<h3>Q. 겨울옷 보관 시 진공 압축팩을 써도 되나요?</h3>
<p>A. 일반 면류나 합성섬유 의류는 괜찮지만, 패딩·다운·울 소재는 섬유가 눌려 복원력이 떨어질 수 있어 권장하지 않습니다. 통기성이 있는 의류 커버나 수납 박스를 활용하는 것이 좋습니다.</p>
<h3>Q. 곰팡이가 생긴 옷은 어떻게 처리하나요?</h3>
<p>A. 가벼운 곰팡이는 과탄산소다 물에 30분 담갔다가 세탁하면 제거됩니다. 심한 경우 전문 세탁소에 맡기세요. 보관 장소는 제습제를 두고 주기적으로 환기하는 것이 예방책입니다.</p>

<h2>마무리</h2>
<p>봄맞이 대청소는 단순히 집을 깨끗하게 하는 것이 아니라, 새 계절을 맞이하는 마음의 준비 과정입니다. 방별 체크리스트로 빠짐없이 청소하고, 겨울옷을 깔끔하게 정리하면 훨씬 가볍고 쾌적한 일상을 보낼 수 있습니다. 올봄에는 묵은 것들을 털어내고 새롭게 시작해 보세요!</p>''',
    },

    # 3. 프로야구 개막/야구 경기
    {
        "title": "2026 KBO 프로야구 개막일 일정 구단별 전력분석 총정리",
        "cat": 13,
        "slug": "kbo-baseball-opening-day-2026",
        "images": [
            ("photo-1508514177221-188b1cf16e9d", "KBO 프로야구 개막 2026"),
            ("photo-1566577739112-5180d4bf9390", "야구장 관람 좌석 정보"),
            ("photo-1529156069898-49953e39b3ac", "야구 경기 관람 준비물"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">봄이 오면 함께 시작되는 것이 있습니다. 바로 <strong>KBO 프로야구</strong>입니다. 2026년에도 10개 구단이 치열한 페넌트레이스를 펼치며 전국 야구팬들의 가슴을 설레게 합니다. 개막일 일정, 구단별 전력 분석, 티켓 예매 방법, 야구장별 꿀팁까지 야구 시즌을 100% 즐기기 위한 모든 것을 정리했습니다.</p>

{imgs[0]}

<h2>2026 KBO 리그 개막 일정</h2>
<p>2026 KBO 리그는 <strong>3월 28일(토)</strong> 전국 5개 구장에서 동시 개막합니다. 총 144경기의 정규 시즌을 치르며, 포스트시즌은 10월에 진행될 예정입니다.</p>
<table><thead><tr><th>일정</th><th>내용</th></tr></thead><tbody>
<tr><td>2026년 3월 28일</td><td>정규 시즌 개막 (전국 5경기 동시)</td></tr>
<tr><td>2026년 9월 말</td><td>정규 시즌 종료 (예정)</td></tr>
<tr><td>2026년 10월 초</td><td>와일드카드 결정전</td></tr>
<tr><td>2026년 10월 중</td><td>준플레이오프 / 플레이오프</td></tr>
<tr><td>2026년 10월 말~11월 초</td><td>한국시리즈</td></tr>
</tbody></table>

<h2>10개 구단 2026 전력 분석표</h2>
<table><thead><tr><th>구단</th><th>홈구장</th><th>2025 순위</th><th>2026 전망</th><th>주목 선수</th></tr></thead><tbody>
<tr><td>LG 트윈스</td><td>잠실구장</td><td>2위</td><td>우승 후보</td><td>오스틴 딘, 문보경</td></tr>
<tr><td>KT 위즈</td><td>수원KT위즈파크</td><td>4위</td><td>상위권 유력</td><td>강백호, 박영현</td></tr>
<tr><td>SSG 랜더스</td><td>인천SSG랜더스필드</td><td>6위</td><td>중위권</td><td>최정, 김광현</td></tr>
<tr><td>NC 다이노스</td><td>창원NC파크</td><td>7위</td><td>중위권</td><td>손아섭, 박민우</td></tr>
<tr><td>두산 베어스</td><td>잠실구장</td><td>3위</td><td>상위권 경쟁</td><td>양석환, 김택연</td></tr>
<tr><td>KIA 타이거즈</td><td>광주-기아챔피언스필드</td><td>1위</td><td>디펜딩 챔피언</td><td>이의리, 나성범</td></tr>
<tr><td>롯데 자이언츠</td><td>사직구장</td><td>9위</td><td>재건 시즌</td><td>전준우, 윤동희</td></tr>
<tr><td>삼성 라이온즈</td><td>대구삼성라이온즈파크</td><td>5위</td><td>상위권 도전</td><td>구자욱, 원태인</td></tr>
<tr><td>한화 이글스</td><td>한화생명이글스파크</td><td>10위</td><td>플레이오프 도전</td><td>노시환, 류현진</td></tr>
<tr><td>키움 히어로즈</td><td>고척스카이돔</td><td>8위</td><td>중위권 목표</td><td>이정후(복귀), 안우진</td></tr>
</tbody></table>

<h3>2026 시즌 주요 이슈</h3>
<ul>
<li><strong>KIA 타이거즈</strong>: 2025 한국시리즈 우승팀으로 디펜딩 챔피언의 지위를 지키기 위해 전력을 보강했습니다.</li>
<li><strong>한화 이글스</strong>: 류현진의 국내 복귀 시즌 연속으로 팬들의 관심이 집중됩니다.</li>
<li><strong>키움 히어로즈</strong>: 이정후의 MLB 경험을 마치고 국내 복귀 가능성이 제기되며 팬들의 기대감이 높습니다.</li>
</ul>

{cta_block("KBO 공식 홈페이지에서 일정·순위 확인", "2026 KBO 리그 전체 경기 일정과 티켓 예매를 확인하세요", "https://www.koreabaseball.com/", "blue")}

{imgs[1]}

<h2>야구 티켓 예매 방법</h2>
<p>야구 인기가 높아지면서 주말 경기는 빠르게 매진됩니다. 미리 예매하는 것이 필수입니다.</p>
<table><thead><tr><th>예매 채널</th><th>특징</th><th>수수료</th></tr></thead><tbody>
<tr><td>티켓링크</td><td>KBO 공식 파트너, 전 구단 통합</td><td>장당 1,000~1,500원</td></tr>
<tr><td>인터파크 티켓</td><td>다양한 좌석 선택, 멤버십 할인</td><td>장당 1,000원</td></tr>
<tr><td>구단 공식 앱</td><td>구단별 멤버십 혜택, 이벤트 우선 참여</td><td>무료 또는 저렴</td></tr>
<tr><td>카카오톡 선물하기</td><td>지인 선물, 티켓 공유 편리</td><td>장당 1,000원</td></tr>
</tbody></table>
<p><strong>예매 꿀팁</strong>: 개막 경기와 더비 매치(LG vs 두산 잠실, KIA vs 삼성 등)는 오픈 즉시 매진되는 경우가 많습니다. 원하는 구단 공식 앱의 알림을 설정해 두세요.</p>

<h2>야구장별 좌석 추천</h2>
<table><thead><tr><th>구장</th><th>추천 좌석</th><th>특징</th></tr></thead><tbody>
<tr><td>잠실구장</td><td>1루/3루 외야 지정석</td><td>응원 열기 최고, 그늘 확보 중요</td></tr>
<tr><td>수원KT위즈파크</td><td>블루존 내야</td><td>넓은 좌석, 가족 관람에 최적</td></tr>
<tr><td>인천SSG랜더스필드</td><td>테이블석, 파티룸</td><td>단체 관람, 식음료 반입 가능</td></tr>
<tr><td>광주기아챔피언스필드</td><td>1루 내야 지정석</td><td>KIA 홈 응원 분위기 최고</td></tr>
<tr><td>고척스카이돔</td><td>3층 중앙 내야</td><td>날씨 무관, 실내 돔 구장</td></tr>
</tbody></table>

{imgs[2]}

<h2>야구장 관람 준비물 체크리스트</h2>
<ul>
<li><strong>응원 도구</strong>: 응원봉, 구단 모자, 유니폼 (현장 구매 가능하나 비쌈)</li>
<li><strong>자외선 차단</strong>: 선크림, 선글라스, 모자 (오후 경기는 햇빛이 강함)</li>
<li><strong>간식</strong>: 외부 음식 반입 가능 구장도 있으니 사전 확인 필수</li>
<li><strong>방한용품</strong>: 개막 초기 4월까지는 저녁에 쌀쌀합니다. 얇은 점퍼 필수</li>
<li><strong>보조 배터리</strong>: 응원 영상, 선수 검색으로 배터리 소모가 빠릅니다</li>
</ul>

<h2>야구 초보를 위한 용어 사전</h2>
<table><thead><tr><th>용어</th><th>설명</th></tr></thead><tbody>
<tr><td>이닝(Inning)</td><td>야구의 기본 단위, 9이닝이 1경기</td></tr>
<tr><td>삼진(Strike Out)</td><td>타자가 3번의 스트라이크를 당해 아웃</td></tr>
<tr><td>볼넷(Walk)</td><td>4개의 볼로 타자가 1루 진출</td></tr>
<tr><td>홈런(Home Run)</td><td>외야 펜스 너머로 공을 쳐 전 루 진루</td></tr>
<tr><td>방어율(ERA)</td><td>투수의 9이닝 당 평균 실점 (낮을수록 우수)</td></tr>
<tr><td>타율(Batting Average)</td><td>타수 대비 안타 비율 (0.300 이상이면 우수)</td></tr>
</tbody></table>

{cta_block("KBO 공식 사이트에서 티켓 예매하기", "구단별 경기 일정과 좌석 선택, 티켓 예매까지 한 번에", "https://www.koreabaseball.com/", "green")}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 야구장에 음식 반입이 가능한가요?</h3>
<p>A. 구장마다 다릅니다. 대부분 외부 음식 반입이 허용되지만, 알코올 음료는 반입 금지입니다. 잠실구장은 외부 음식 반입이 가능하며 캔 음료도 허용됩니다. 방문 전 해당 구장 공지를 확인하세요.</p>
<h3>Q. 경기 시작 시간은 보통 몇 시인가요?</h3>
<p>A. 평일 경기는 오후 6시 30분, 주말·공휴일 경기는 오후 2시 또는 5시 시작이 일반적입니다. 구단 및 구장별로 다를 수 있으니 티켓 정보를 반드시 확인하세요.</p>
<h3>Q. 어린 아이와 함께 야구장에 가도 괜찮을까요?</h3>
<p>A. 36개월 미만 영유아는 무릎 관람 시 무료입니다. 가족석이나 테이블석을 예매하면 더욱 편안하게 관람할 수 있습니다. 귀마개를 챙기면 응원 소음으로부터 아이를 보호할 수 있습니다.</p>

<h2>마무리</h2>
<p>2026 KBO 프로야구 시즌은 디펜딩 챔피언 KIA의 연속 우승 도전, 류현진의 완전 복귀, 각 구단의 치열한 경쟁으로 역대 가장 흥미로운 시즌이 될 것으로 기대됩니다. 미리 티켓을 예매하고 응원 도구를 준비해서 올봄 야구장의 뜨거운 열기를 직접 느껴보세요!</p>''',
    },

    # 4. 인생샷 명소/드라이브 코스/서울 근교
    {
        "title": "2026 봄 인생샷 명소 드라이브 코스 서울 근교 여행지 BEST 10",
        "cat": 13,
        "slug": "instagram-spot-drive-course-seoul-2026",
        "images": [
            ("photo-1471295253337-3ceaaedca402", "서울 근교 봄 인생샷 명소"),
            ("photo-1506905925346-21bda4d32df4", "봄 드라이브 코스 추천"),
            ("photo-1494548162494-384bba4ab999", "SNS 핫플 인생샷 스팟"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">봄꽃이 피는 계절, <strong>서울 근교 인생샷 명소</strong>를 찾아 떠나는 당일치기 여행만큼 설레는 것도 없습니다. 벚꽃, 유채꽃, 튤립이 한데 어우러지는 2026년 봄, SNS를 가득 채울 인생샷을 건지고 싶다면 이 글 하나로 완벽하게 준비하세요. 드라이브 코스 5곳, 인생샷 명소 10곳, 사진 팁까지 총정리했습니다.</p>

{imgs[0]}

<h2>서울 근교 인생샷 명소 BEST 10</h2>
<table><thead><tr><th>순위</th><th>장소명</th><th>위치</th><th>특징</th><th>입장료</th></tr></thead><tbody>
<tr><td>1</td><td>에버랜드 튤립축제</td><td>경기 용인</td><td>국내 최대 튤립 정원, 100만 송이 튤립</td><td>입장료 별도</td></tr>
<tr><td>2</td><td>경의선 숲길 벚꽃터널</td><td>서울 마포구</td><td>도심 속 벚꽃터널, 감성 카페 밀집</td><td>무료</td></tr>
<tr><td>3</td><td>남이섬</td><td>강원 춘천</td><td>메타세쿼이아길, 호수 뷰, 사계절 꽃밭</td><td>성인 16,000원</td></tr>
<tr><td>4</td><td>제부도 노을 해변</td><td>경기 화성</td><td>바닷길이 열리는 신비의 섬, 석양 명소</td><td>무료 (주차료)</td></tr>
<tr><td>5</td><td>양평 들꽃수목원</td><td>경기 양평</td><td>유채꽃·수선화·벚꽃 동시 감상</td><td>성인 5,000원</td></tr>
<tr><td>6</td><td>일산 호수공원 벚꽃길</td><td>경기 고양</td><td>호수+벚꽃 조화, 주말 피크닉 최적</td><td>무료</td></tr>
<tr><td>7</td><td>가평 아침고요수목원</td><td>경기 가평</td><td>정원식 조경, 계절 꽃 변화 아름다움</td><td>성인 11,000원</td></tr>
<tr><td>8</td><td>파주 헤이리 예술마을</td><td>경기 파주</td><td>갤러리·카페·특색 건축물 포토존</td><td>무료</td></tr>
<tr><td>9</td><td>강화도 조양방직 카페</td><td>인천 강화</td><td>레트로 공장 개조 카페, 감성 소품</td><td>음료 구매</td></tr>
<tr><td>10</td><td>서울식물원 봄 정원</td><td>서울 강서구</td><td>온실 정원, 야외 꽃밭, 한강뷰</td><td>성인 5,000원</td></tr>
</tbody></table>

<h3>2026년 봄꽃 개화 예상 시기</h3>
<table><thead><tr><th>꽃 종류</th><th>서울 기준 개화</th><th>절정</th></tr></thead><tbody>
<tr><td>벚꽃</td><td>3월 말~4월 초</td><td>4월 첫째~둘째 주</td></tr>
<tr><td>개나리·진달래</td><td>3월 중순~말</td><td>3월 말~4월 초</td></tr>
<tr><td>튤립</td><td>4월 초</td><td>4월 중순</td></tr>
<tr><td>유채꽃</td><td>4월 초</td><td>4월 중~하순</td></tr>
<tr><td>철쭉</td><td>4월 말</td><td>5월 초</td></tr>
</tbody></table>

{cta_block("한국관광공사에서 봄 여행지 검색하기", "공식 여행 정보와 숙박·교통 할인 혜택을 확인하세요", "https://korean.visitkorea.or.kr/", "blue")}

{imgs[1]}

<h2>봄 드라이브 코스 BEST 5</h2>
<p>따뜻한 봄날, 차창 밖으로 펼쳐지는 꽃길을 달리는 드라이브는 봄의 백미입니다.</p>

<h3>1. 올림픽대로 → 한강공원 → 양평 벚꽃길</h3>
<p>서울에서 양평 북한강로를 따라 달리는 코스입니다. 특히 수동에서 양평까지 이어지는 벚꽃 가로수길은 터널처럼 펼쳐져 환상적인 드라이브 경험을 선사합니다. <strong>총 거리 약 80km, 소요 1시간 30분</strong></p>

<h3>2. 강화도 해안 일주 코스</h3>
<p>초지진에서 시작해 강화도 외포리, 동막 해변, 광성보를 거치는 해안 순환 코스입니다. 갯벌과 봄 바다 뷰가 일품이며 중간에 조양방직 카페에서 휴식을 취하기 좋습니다. <strong>총 거리 약 60km, 소요 2시간</strong></p>

<h3>3. 춘천 소양강 → 남이섬 → 가평 코스</h3>
<p>경춘고속도로를 타고 춘천까지 간 뒤, 소양강 댐 뷰를 즐기고 가평 남이섬으로 이동하는 코스입니다. 청평 호반길의 봄 경치가 특히 아름답습니다. <strong>총 거리 약 120km, 소요 2시간 30분</strong></p>

<h3>4. 파주 헤이리 → 임진각 → 통일전망대</h3>
<p>파주 출판단지와 헤이리 마을을 구경한 후 임진각까지 이어지는 감성 코스입니다. 유채꽃이 피는 4월 중순에 방문하면 노란 꽃밭과 함께 인생사진을 찍을 수 있습니다. <strong>총 거리 약 50km, 소요 1시간 30분</strong></p>

<h3>5. 용인 에버랜드 → 양지 → 이천 도자기 마을</h3>
<p>에버랜드 튤립 축제를 즐긴 후 이천 설봉공원의 벚꽃, 이천 도자기 마을을 둘러보는 코스입니다. 가족 단위 당일치기에 최적화되어 있습니다. <strong>총 거리 약 70km, 소요 2시간</strong></p>

{imgs[2]}

<h2>인생샷 잘 찍는 사진 팁</h2>
<ul>
<li><strong>황금 시간대(Golden Hour) 활용</strong>: 일출 직후 1시간, 일몰 전 1시간의 빛은 사진을 따뜻하고 몽환적으로 만들어 줍니다.</li>
<li><strong>역광 촬영</strong>: 꽃을 배경으로 역광으로 찍으면 꽃잎이 빛을 투과해 아름다운 실루엣 사진이 나옵니다.</li>
<li><strong>로우앵글(낮은 각도)</strong>: 카메라를 낮게 들고 꽃을 올려다보는 구도로 촬영하면 꽃밭이 더 풍성해 보입니다.</li>
<li><strong>인물+배경 비율</strong>: 인물은 프레임의 1/3 정도, 배경이 2/3 이상 나오면 장소감이 살아납니다.</li>
<li><strong>스마트폰 포트레이트 모드</strong>: 아이폰·갤럭시의 인물 사진 모드로 자연스러운 배경 흐림 효과를 활용하세요.</li>
</ul>

<h2>SNS 인기 해시태그 & 핫플 정보</h2>
<table><thead><tr><th>해시태그</th><th>관련 명소</th><th>인스타 게시물 수</th></tr></thead><tbody>
<tr><td>#서울근교봄나들이</td><td>한강공원, 남이섬, 양평</td><td>320만+</td></tr>
<tr><td>#벚꽃드라이브</td><td>북한강로, 경의선숲길</td><td>180만+</td></tr>
<tr><td>#튤립축제</td><td>에버랜드, 태안세계튤립축제</td><td>140만+</td></tr>
<tr><td>#파주헤이리</td><td>헤이리 예술마을</td><td>90만+</td></tr>
<tr><td>#강화도카페</td><td>조양방직, 뷰 카페들</td><td>75만+</td></tr>
</tbody></table>

<h2>주요 명소 주차 정보</h2>
<table><thead><tr><th>명소</th><th>주차 가능 여부</th><th>주차 요금</th><th>주차 팁</th></tr></thead><tbody>
<tr><td>경의선 숲길</td><td>인근 유료 주차장</td><td>시간당 3,000~5,000원</td><td>대중교통 권장 (홍대입구역)</td></tr>
<tr><td>일산 호수공원</td><td>대형 무료 주차장</td><td>무료</td><td>주말 오전 일찍 도착 권장</td></tr>
<tr><td>남이섬</td><td>남이섬 주차장</td><td>소형 3,000원/일</td><td>가평 선착장에서 배 이용</td></tr>
<tr><td>아침고요수목원</td><td>전용 주차장</td><td>무료</td><td>개장 30분 전 도착 권장</td></tr>
<tr><td>서울식물원</td><td>지하 유료 주차장</td><td>10분당 600원</td><td>지하철 9호선 마곡나루역 도보 5분</td></tr>
</tbody></table>

{cta_block("한국관광공사 공식 여행 정보", "숙박, 맛집, 관광지 정보와 봄 여행 특가 상품을 확인하세요", "https://korean.visitkorea.or.kr/", "green")}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 벚꽃 절정 시기를 미리 알 수 있나요?</h3>
<p>A. 기상청 봄꽃 개화 예보 서비스(www.weather.go.kr)에서 지역별 벚꽃 개화일과 절정 예상일을 확인할 수 있습니다. 2026년 서울 기준 벚꽃 절정은 4월 첫째~둘째 주로 예상됩니다.</p>
<h3>Q. 서울 근교 당일치기 여행 시 교통수단은 차가 편한가요?</h3>
<p>A. 양평, 가평, 강화도 등 대중교통이 불편한 곳은 차가 편리합니다. 단, 벚꽃 절정 주말에는 극심한 정체가 예상되므로 주차 예약과 우회로를 미리 파악해 두는 것이 좋습니다. 남이섬은 경춘선 열차+선박 조합이 오히려 빠를 수 있습니다.</p>
<h3>Q. 인생샷 명소가 사람이 너무 많으면 어떻게 하나요?</h3>
<p>A. 주말 피크 시간(오전 11시~오후 3시)을 피하고 이른 아침이나 평일을 이용하면 한산하게 촬영할 수 있습니다. 일부 명소는 사전 예약제를 운영하므로 공식 홈페이지를 확인하세요.</p>

<h2>마무리</h2>
<p>2026년 봄, 서울 근교에는 인생사진을 남길 수 있는 아름다운 명소들이 가득합니다. 벚꽃이 바람에 날리는 드라이브 코스를 달리거나, 튤립 가득한 정원에서 소중한 사람과 사진을 찍으며 봄의 기억을 만들어 보세요. 미리 개화 예보를 확인하고, 주차 계획을 세워서 여유롭고 즐거운 봄 여행을 즐기시길 바랍니다!</p>''',
    },
]


# ========== 실행 ==========
def main():
    published = []

    for idx, post in enumerate(POSTS, 1):
        print(f"\n{'='*60}")
        print(f"[{idx}/4] {post['title']}")
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

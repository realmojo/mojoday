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
    # 1. 기초연금 모의계산
    {
        "title": "기초연금 모의계산 수급자격 조건 신청방법 2026 총정리",
        "cat": 13,
        "slug": "basic-pension-calculator-2026",
        "images": [
            ("photo-1556742049-0cfed4f6a45d", "기초연금 모의계산 신청"),
            ("photo-1554224155-6726b3ff858f", "기초연금 수급 조건 확인"),
            ("photo-1450101499163-c8848c66ca85", "기초연금 서류 준비"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">2026년 기초연금은 만 65세 이상 어르신 중 소득인정액이 일정 기준 이하인 분께 매달 지급되는 <strong>국가 복지 제도</strong>입니다. 올해 기준 단독가구 최대 <strong>월 334,810원</strong>, 부부가구 최대 <strong>월 535,680원</strong>까지 받을 수 있습니다. 하지만 소득인정액 계산이 복잡해서 본인이 대상자인지 모르는 경우가 많습니다. 이 글에서는 기초연금 모의계산 방법, 수급 자격, 신청 절차를 완벽하게 정리합니다.</p>

{imgs[0]}

<h2>기초연금이란?</h2>
<p>기초연금은 노인빈곤 문제를 해소하기 위해 2014년 7월부터 시행된 제도입니다. 국민연금과는 별도로 지급되며, 국민연금을 받고 있더라도 소득인정액 기준을 충족하면 기초연금을 추가로 받을 수 있습니다.</p>
<table><thead><tr><th>구분</th><th>2026년 기준</th></tr></thead><tbody>
<tr><td>지급 대상</td><td>만 65세 이상, 소득 하위 70%</td></tr>
<tr><td>단독가구 선정기준액</td><td>월 2,130,000원</td></tr>
<tr><td>부부가구 선정기준액</td><td>월 3,408,000원</td></tr>
<tr><td>단독가구 최대 지급액</td><td>월 334,810원</td></tr>
<tr><td>부부가구 최대 지급액</td><td>월 535,680원 (20% 감액)</td></tr>
<tr><td>지급일</td><td>매월 25일</td></tr>
</tbody></table>

<h2>기초연금 모의계산 방법</h2>
<p>기초연금 수급 여부는 <strong>소득인정액</strong>으로 판단합니다. 소득인정액 = 소득평가액 + 재산의 소득환산액입니다.</p>
<h3>소득평가액 계산</h3>
<p>소득평가액은 근로소득, 사업소득, 재산소득, 공적이전소득 등을 합산한 금액입니다.</p>
<ul>
<li><strong>근로소득</strong>: (월 근로소득 - 110만원) × 0.7 (110만원 기본공제 + 30% 추가공제)</li>
<li><strong>사업소득</strong>: 기타사업소득은 전액 반영</li>
<li><strong>재산소득</strong>: 이자, 배당, 연금소득 등</li>
<li><strong>공적이전소득</strong>: 국민연금, 공무원연금 등 (국민연금은 일부만 반영)</li>
</ul>
<h3>재산의 소득환산액 계산</h3>
<p>재산은 일반재산, 금융재산, 부채를 고려합니다.</p>
<ul>
<li><strong>일반재산</strong>: (부동산 + 전월세 보증금 - 기본재산액) × 소득환산율(연 4%)</li>
<li><strong>금융재산</strong>: (예금 + 주식 + 보험 - 2,000만원 공제) × 소득환산율(연 4%)</li>
<li><strong>기본재산액 공제</strong>: 대도시 1억 3,500만원 / 중소도시 8,500만원 / 농어촌 7,250만원</li>
<li><strong>고급 자동차</strong>: 3,000cc 이상 또는 4,000만원 이상 차량은 전액 반영</li>
</ul>

{cta_block("기초연금 모의계산 바로하기", "복지로에서 내 소득인정액과 예상 수급액을 확인하세요", "https://www.bokjiro.go.kr/", "blue")}

<h3>모의계산 예시</h3>
<p>서울 거주, 단독가구, 만 68세 기준:</p>
<table><thead><tr><th>항목</th><th>금액</th><th>계산</th></tr></thead><tbody>
<tr><td>국민연금</td><td>월 40만원</td><td>40만원 반영</td></tr>
<tr><td>근로소득</td><td>월 150만원</td><td>(150만-110만) × 0.7 = 28만원</td></tr>
<tr><td>아파트 시가</td><td>3억원</td><td>(3억-1.35억) × 4% ÷ 12 = 55만원</td></tr>
<tr><td>예금</td><td>3,000만원</td><td>(3,000만-2,000만) × 4% ÷ 12 = 3.3만원</td></tr>
<tr><td><strong>소득인정액 합계</strong></td><td colspan="2"><strong>약 126.3만원 → 수급 가능 (기준 213만원 이하)</strong></td></tr>
</tbody></table>

{imgs[1]}

<h2>기초연금 신청 방법</h2>
<ol>
<li><strong>방문 신청</strong>: 주소지 관할 읍·면·동 주민센터 또는 국민연금공단 지사 방문</li>
<li><strong>온라인 신청</strong>: 복지로(www.bokjiro.go.kr) 접속 → 서비스 신청 → 기초연금</li>
<li><strong>전화 신청</strong>: 국민연금공단 콜센터 1355</li>
</ol>
<h3>필요 서류</h3>
<ul>
<li>신분증 (주민등록증, 운전면허증 등)</li>
<li>기초연금 신청서 (현장 작성 가능)</li>
<li>통장 사본 (본인 명의)</li>
<li>금융정보등 제공동의서</li>
<li>소득·재산 관련 서류 (필요 시)</li>
</ul>

<h2>기초연금 감액 사유 3가지</h2>
<ol>
<li><strong>부부 감액</strong>: 부부 모두 수급 시 각각 20% 감액 (단독 334,810원 → 부부 각 267,850원)</li>
<li><strong>국민연금 연계 감액</strong>: 국민연금 수령액이 기초연금의 150%(약 50만원)를 초과하면 기초연금이 최대 50%까지 감액</li>
<li><strong>소득역전 방지 감액</strong>: 소득인정액이 선정기준액에 근접하면 초과분만큼 감액</li>
</ol>

{cta_block("국민연금공단에서 상담받기", "1355 전화 또는 가까운 지사 방문으로 상세 상담 가능합니다", "https://www.nps.or.kr/", "yellow")}

{imgs[2]}

<h2>기초연금 자주 묻는 질문 (FAQ)</h2>
<h3>Q. 국민연금을 받고 있어도 기초연금을 받을 수 있나요?</h3>
<p>A. 네, 받을 수 있습니다. 다만 국민연금 수령액이 기초연금의 150%(약 50만원)를 넘으면 <strong>기초연금이 일부 감액</strong>될 수 있습니다. 국민연금을 월 40만원 이하로 받는 분은 기초연금 전액을 받을 수 있습니다.</p>
<h3>Q. 자녀 명의 집에 살고 있으면 재산에 포함되나요?</h3>
<p>A. <strong>본인 명의 재산만 반영</strong>됩니다. 자녀 소유 주택에 거주하는 경우 본인 재산에 포함되지 않습니다. 단, 자녀로부터 정기적으로 생활비를 받는 경우 사적이전소득으로 반영될 수 있습니다.</p>
<h3>Q. 기초연금과 기초생활수급은 중복으로 받을 수 있나요?</h3>
<p>A. 기초연금과 기초생활보장 수급은 <strong>중복 수급이 가능</strong>합니다. 다만 기초연금 수급액이 소득에 포함되어 기초생활보장 급여가 조정될 수 있습니다.</p>
<h3>Q. 기초연금은 매년 인상되나요?</h3>
<p>A. 네, 전국소비자물가변동률을 반영하여 <strong>매년 1월 인상</strong>됩니다. 2026년에는 전년 대비 약 3.3% 인상되었습니다.</p>

{cta_block("복지로에서 다른 복지 혜택도 확인하기", "기초연금 외에도 받을 수 있는 복지 혜택을 한눈에 확인하세요", "https://www.bokjiro.go.kr/", "green")}

<h2>마무리</h2>
<p>기초연금은 만 65세 이상이라면 반드시 확인해봐야 할 복지 제도입니다. 소득인정액 계산이 복잡하지만, 복지로 모의계산이나 국민연금공단(1355)을 통해 쉽게 확인할 수 있습니다. 본인뿐 아니라 부모님의 수급 자격도 꼭 확인해보세요.</p>'''
    },

    # 2. 지방선거 알바
    {
        "title": "지방선거 알바 종류 급여 신청방법 2026 총정리",
        "cat": 13,
        "slug": "local-election-part-time-job-2026",
        "images": [
            ("photo-1540910419892-4a36d2c3266c", "지방선거 투표소 모습"),
            ("photo-1434030216411-0b793f4b4173", "선거 관련 업무"),
            ("photo-1554224155-6726b3ff858f", "선거 알바 급여"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">2026년 6월 지방선거가 다가오면서 <strong>선거 관련 단기 알바</strong>에 대한 관심이 높아지고 있습니다. 선거 알바는 짧은 기간에 비교적 높은 급여를 받을 수 있어 대학생, 취준생, 주부 등에게 인기입니다. 투표사무원부터 여론조사원까지 다양한 종류의 선거 알바 종류, 급여, 신청 방법을 총정리합니다.</p>

{imgs[0]}

<h2>2026 지방선거 알바 종류 및 급여</h2>
<table><thead><tr><th>알바 종류</th><th>일급/시급</th><th>근무 시간</th><th>근무 기간</th><th>채용 주체</th></tr></thead><tbody>
<tr><td>투표사무원</td><td>일급 10~12만원</td><td>06:00~18:00 (약 12시간)</td><td>선거 당일 1일</td><td>선거관리위원회</td></tr>
<tr><td>개표사무원</td><td>일급 8~10만원</td><td>18:00~익일 새벽</td><td>선거 당일 1일</td><td>선거관리위원회</td></tr>
<tr><td>사전투표사무원</td><td>일급 10만원</td><td>06:00~18:00</td><td>2일 (금·토)</td><td>선거관리위원회</td></tr>
<tr><td>여론조사원</td><td>시급 1.2~2만원</td><td>4~8시간</td><td>선거 전 2~4주</td><td>여론조사 업체</td></tr>
<tr><td>선거유세 도우미</td><td>일급 8~15만원</td><td>4~10시간</td><td>선거운동기간</td><td>후보 선거사무소</td></tr>
<tr><td>선거벽보 부착</td><td>건당 1,000~3,000원</td><td>자유</td><td>선거운동기간</td><td>후보 선거사무소</td></tr>
<tr><td>참관인</td><td>일급 8~10만원</td><td>투표 시작~개표 종료</td><td>1일</td><td>정당/후보</td></tr>
</tbody></table>

<h2>가장 인기 있는 선거 알바 TOP 3</h2>
<h3>1위. 투표사무원 (일급 10~12만원)</h3>
<p>가장 인기 있고 경쟁률이 높은 선거 알바입니다. 투표소에서 신분 확인, 투표용지 교부, 투표 안내 등의 업무를 합니다.</p>
<ul>
<li><strong>근무 시간</strong>: 선거 당일 오전 6시~오후 6시 (약 12시간)</li>
<li><strong>급여</strong>: 일급 약 10~12만원 + 식비 별도</li>
<li><strong>자격</strong>: 만 18세 이상, 해당 선거 선거권 있는 자</li>
<li><strong>제한</strong>: 공무원, 정당원, 후보자 관계인 불가</li>
<li><strong>신청 방법</strong>: 관할 구·시·군 선거관리위원회 홈페이지 또는 방문 신청</li>
</ul>

{cta_block("선거관리위원회 투표사무원 신청", "중앙선거관리위원회 홈페이지에서 투표사무원을 신청하세요", "https://www.nec.go.kr/", "blue")}

<h3>2위. 사전투표사무원 (2일간 약 20만원)</h3>
<p>사전투표 기간(선거일 전 금·토요일) 2일간 근무합니다. 투표사무원과 업무가 동일하며, 2일 근무이므로 총 약 20만원을 받을 수 있습니다.</p>
<ul>
<li><strong>근무 기간</strong>: 선거일 전 금·토 2일간</li>
<li><strong>급여</strong>: 일 10만원 × 2일 = 약 20만원</li>
<li><strong>장점</strong>: 선거 당일보다 경쟁률이 낮은 편</li>
</ul>

<h3>3위. 여론조사원 (시급 1.2~2만원)</h3>
<p>전화 또는 현장에서 유권자 대상 여론조사를 진행합니다. 선거 전 2~4주 동안 지속적으로 일할 수 있어 총 수입이 높습니다.</p>
<ul>
<li><strong>근무 형태</strong>: 전화 여론조사(콜센터) 또는 현장 면접 조사</li>
<li><strong>시급</strong>: 1.2~2만원 (경력에 따라 상이)</li>
<li><strong>장점</strong>: 선거 전 여러 주 동안 장기 근무 가능</li>
<li><strong>신청</strong>: 알바몬, 알바천국 등 구인 사이트에서 "여론조사" 검색</li>
</ul>

{imgs[1]}

<h2>선거 알바 신청 방법</h2>
<h3>투표사무원 / 개표사무원 / 사전투표사무원</h3>
<ol>
<li><strong>중앙선거관리위원회</strong>(nec.go.kr) 접속</li>
<li>선거 정보 → 투표사무원 모집 공고 확인</li>
<li>거주지 관할 구·시·군 선거관리위원회에 신청</li>
<li>보통 선거일 1~2개월 전부터 모집 시작</li>
<li>선착순 또는 추첨 방식으로 선발</li>
</ol>
<h3>여론조사원 / 선거유세 도우미</h3>
<ol>
<li><strong>알바몬</strong>, <strong>알바천국</strong>, <strong>사람인</strong> 등 구인 사이트 접속</li>
<li>"선거", "여론조사", "선거유세" 등으로 검색</li>
<li>해당 업체에 직접 지원</li>
</ol>

{cta_block("알바몬에서 선거 알바 찾기", "알바몬에서 '선거' 검색으로 최신 선거 알바를 확인하세요", "https://www.albamon.com/", "yellow")}

<h2>선거 알바 시 주의사항</h2>
<ul>
<li><strong>정치적 중립 의무</strong>: 투표사무원은 근무 중 특정 후보·정당 지지 표현이 절대 금지됩니다</li>
<li><strong>비밀 유지</strong>: 투표 및 개표 과정에서 알게 된 정보를 외부에 유출하면 처벌받습니다</li>
<li><strong>복장 규정</strong>: 특정 정당 색상의 옷, 선거 관련 문구가 있는 옷 착용 금지</li>
<li><strong>휴대폰 제한</strong>: 투표소 내에서는 휴대폰 사진 촬영 금지</li>
<li><strong>선거법 위반 주의</strong>: 선거유세 도우미의 경우 선거법 범위 내에서만 활동해야 합니다</li>
</ul>

{imgs[2]}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 대학생도 투표사무원 신청이 가능한가요?</h3>
<p>A. 네, <strong>만 18세 이상</strong>이면 누구나 가능합니다. 단, 해당 선거의 선거권이 있어야 하고 공무원·정당원은 불가합니다.</p>
<h3>Q. 투표사무원 경쟁률이 높은가요?</h3>
<p>A. 지역에 따라 다르지만 보통 <strong>2~5:1</strong> 수준입니다. 조기 마감되는 경우가 많으므로 모집 공고가 나오면 바로 신청하세요.</p>
<h3>Q. 선거 알바 급여에 세금이 붙나요?</h3>
<p>A. 투표·개표사무원 급여는 <strong>기타소득</strong>으로 분류되며, 8.8%의 원천징수가 발생합니다. 다만 금액이 크지 않아 종합소득세 신고 시 환급받을 수 있습니다.</p>
<h3>Q. 개표사무원은 밤새 근무하나요?</h3>
<p>A. 투표 종료(오후 6시) 후 개표가 시작되며, 보통 <strong>자정~새벽 2시경</strong>에 종료됩니다. 접전 지역은 더 늦어질 수 있습니다.</p>

{cta_block("중앙선거관리위원회에서 모집 공고 확인", "2026 지방선거 투표사무원 모집 일정과 신청 방법을 확인하세요", "https://www.nec.go.kr/", "green")}

<h2>마무리</h2>
<p>2026년 지방선거는 6월에 실시될 예정이며, 선거 알바 모집은 보통 선거일 1~2개월 전부터 시작됩니다. 인기 있는 투표사무원은 조기 마감되므로 선거관리위원회 공지를 수시로 확인하세요.</p>'''
    },

    # 3. 청년월세지원
    {
        "title": "청년월세 한시 특별지원 조건 신청방법 지급액 2026 총정리",
        "cat": 13,
        "slug": "youth-rent-support-2026",
        "images": [
            ("photo-1560448204-e02f11c3d0e2", "청년 원룸 월세 지원"),
            ("photo-1484154218962-a197022b5858", "청년 주거 공간"),
            ("photo-1554224155-6726b3ff858f", "월세 지원금 신청"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">높은 월세 부담에 시달리는 청년들을 위해 정부에서 <strong>월 최대 20만원</strong>의 월세를 지원하는 '청년월세 한시 특별지원' 사업이 2026년에도 계속됩니다. 소득과 재산 기준을 충족하는 만 19~34세 청년이면 최대 12개월간 지원받을 수 있습니다. 자격 조건, 신청 방법, 필요 서류까지 총정리합니다.</p>

{imgs[0]}

<h2>청년월세 한시 특별지원이란?</h2>
<p>청년월세 한시 특별지원은 주거비 부담이 큰 청년 1인 가구를 대상으로 <strong>월 최대 20만원, 최대 12개월</strong>간 월세를 지원하는 제도입니다.</p>
<table><thead><tr><th>구분</th><th>내용</th></tr></thead><tbody>
<tr><td>지원 대상</td><td>만 19~34세 독립거주 무주택 청년</td></tr>
<tr><td>지원 금액</td><td>월 최대 20만원 (실제 월세 한도 내)</td></tr>
<tr><td>지원 기간</td><td>최대 12개월</td></tr>
<tr><td>소득 기준</td><td>청년 본인 소득 중위 60% 이하</td></tr>
<tr><td>재산 기준</td><td>청년 본인 1.22억원 이하</td></tr>
<tr><td>원가구 소득</td><td>중위소득 100% 이하 (부모님 가구)</td></tr>
</tbody></table>

<h2>자격 조건 상세</h2>
<h3>나이 조건</h3>
<p>신청일 기준 <strong>만 19세~34세</strong> (1991년~2007년생). 병역 이행 기간은 나이에서 차감됩니다. 예: 군복무 2년 → 만 36세까지 신청 가능.</p>
<h3>소득 조건 (2026년 기준)</h3>
<table><thead><tr><th>가구 규모</th><th>청년 본인 (중위 60%)</th><th>원가구 (중위 100%)</th></tr></thead><tbody>
<tr><td>1인 가구</td><td>월 1,337,067원</td><td>월 2,228,445원</td></tr>
<tr><td>2인 가구</td><td>-</td><td>월 3,682,609원</td></tr>
<tr><td>3인 가구</td><td>-</td><td>월 4,714,657원</td></tr>
<tr><td>4인 가구</td><td>-</td><td>월 5,729,913원</td></tr>
</tbody></table>
<p>※ 청년 본인은 1인 가구 기준 적용, 원가구(부모님)는 가구원 수에 따라 적용</p>
<h3>재산 조건</h3>
<ul>
<li>청년 본인: 총 재산 <strong>1.22억원 이하</strong></li>
<li>원가구(부모님): 총 재산 <strong>4.7억원 이하</strong></li>
<li>자동차 가액 3,708만원 이하</li>
</ul>
<h3>주거 조건</h3>
<ul>
<li><strong>무주택자</strong>여야 함</li>
<li>부모와 별도 거주 (독립 세대)</li>
<li>보증금 5,000만원 이하 & 월세 70만원 이하인 주택</li>
<li>임대차계약서상 본인 명의</li>
</ul>

{cta_block("청년월세지원 자격 확인하기", "복지로에서 내 소득·재산 기준 충족 여부를 확인하세요", "https://www.bokjiro.go.kr/", "blue")}

{imgs[1]}

<h2>신청 방법 (단계별)</h2>
<ol>
<li><strong>복지로(bokjiro.go.kr) 온라인 신청</strong>
<ul><li>복지로 접속 → 로그인 → 서비스 신청 → 복지서비스 → '청년월세' 검색</li><li>공동인증서 또는 간편인증 필요</li></ul></li>
<li><strong>주민센터 방문 신청</strong>
<ul><li>주소지 관할 읍·면·동 주민센터 방문</li><li>신분증, 임대차계약서, 통장사본 지참</li></ul></li>
</ol>
<h3>필요 서류</h3>
<ul>
<li>사회보장급여 신청서 (현장 작성)</li>
<li>소득·재산 신고서</li>
<li>임대차계약서 사본</li>
<li>월세 이체 확인서 (통장 거래내역)</li>
<li>가족관계증명서</li>
<li>통장 사본 (본인 명의)</li>
</ul>

<h2>지급 방식 및 일정</h2>
<ul>
<li><strong>지급 방식</strong>: 청년 본인 계좌로 매월 입금</li>
<li><strong>지급일</strong>: 매월 25일경 (자치단체별 상이)</li>
<li><strong>지급액</strong>: 실제 월세와 20만원 중 적은 금액 (월세 15만원이면 15만원 지급)</li>
<li><strong>심사 기간</strong>: 신청 후 약 1~2개월 소요</li>
</ul>

{cta_block("청년월세지원 온라인 신청하기", "복지로에서 바로 온라인 신청이 가능합니다", "https://www.bokjiro.go.kr/", "yellow")}

{imgs[2]}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 전세에 살고 있으면 신청이 안 되나요?</h3>
<p>A. <strong>월세가 있어야 신청 가능</strong>합니다. 순수 전세는 불가하지만, 보증금 + 월세 형태(반전세)는 신청 가능합니다.</p>
<h3>Q. 부모님과 같은 시에 살아도 되나요?</h3>
<p>A. 같은 시에 살아도 됩니다. 중요한 것은 <strong>주민등록상 부모와 별도 세대 분리</strong>가 되어 있어야 한다는 것입니다.</p>
<h3>Q. 기존 청년 주거급여와 중복 수급이 가능한가요?</h3>
<p>A. <strong>주거급여 수급자는 신청 불가</strong>합니다. 다만 주거급여를 받지 않는 경우, 다른 청년 지원 사업과 일부 중복 수급이 가능합니다.</p>
<h3>Q. 고시원이나 기숙사도 신청 가능한가요?</h3>
<p>A. <strong>고시원은 가능</strong>합니다 (임대차계약서 필요). 기숙사, 사택 등은 불가합니다.</p>

{cta_block("다른 청년 지원 사업도 확인하기", "청년도약계좌, 청년내일채움공제 등 다른 혜택도 확인하세요", "https://www.youthcenter.go.kr/", "green")}

<h2>마무리</h2>
<p>청년월세 한시 특별지원은 자격만 되면 반드시 신청해야 하는 혜택입니다. 월 최대 20만원 × 12개월 = 최대 240만원을 받을 수 있으니, 조건이 되는 분은 빠르게 신청하세요.</p>'''
    },

    # 4. 자동차세 환급
    {
        "title": "자동차세 환급 조건 신청방법 조회 2026 총정리",
        "cat": 8,
        "slug": "car-tax-refund-guide-2026",
        "images": [
            ("photo-1449965408869-eaa3f722e40d", "자동차세 환급 신청"),
            ("photo-1560179707-f14e90ef3623", "자동차 세금 계산"),
            ("photo-1554224155-6726b3ff858f", "자동차세 환급금 조회"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">자동차를 <strong>중고로 팔거나 폐차</strong>했는데 이미 연납한 자동차세가 있다면? 남은 기간만큼 <strong>환급</strong>받을 수 있습니다. 매년 수십만 원의 환급금을 모르고 놓치는 분들이 많습니다. 2026년 자동차세 환급 조건, 금액 계산, 신청 방법을 총정리합니다.</p>

{imgs[0]}

<h2>자동차세 환급이란?</h2>
<p>자동차세를 연초에 <strong>연납(일괄납부)</strong>하면 약 5% 할인을 받습니다. 하지만 연중에 차량을 매도, 폐차, 말소하면 이미 낸 세금 중 <strong>남은 기간에 해당하는 금액을 돌려받을 수 있습니다</strong>.</p>
<table><thead><tr><th>환급 사유</th><th>설명</th></tr></thead><tbody>
<tr><td>차량 매도(이전)</td><td>중고차 판매 후 소유권 이전 시</td></tr>
<tr><td>차량 폐차</td><td>폐차장에서 말소 처리 완료 시</td></tr>
<tr><td>차량 수출</td><td>해외 수출로 국내 등록 말소 시</td></tr>
<tr><td>주소 이전</td><td>다른 지자체로 전입 시 (지자체 간 정산)</td></tr>
<tr><td>이중 납부</td><td>같은 기간 세금을 중복 납부한 경우</td></tr>
</tbody></table>

<h2>자동차세 환급금 계산 방법</h2>
<p>환급금은 <strong>연납 금액 ÷ 365일 × 남은 일수</strong>로 계산됩니다.</p>
<h3>계산 예시</h3>
<table><thead><tr><th>항목</th><th>금액</th></tr></thead><tbody>
<tr><td>연납 자동차세 (2000cc 승용차)</td><td>520,000원</td></tr>
<tr><td>매도일</td><td>2026년 7월 1일</td></tr>
<tr><td>남은 일수</td><td>184일 (7/1~12/31)</td></tr>
<tr><td><strong>환급금</strong></td><td><strong>520,000 ÷ 365 × 184 = 약 262,000원</strong></td></tr>
</tbody></table>

<h3>배기량별 연간 자동차세 참고</h3>
<table><thead><tr><th>배기량</th><th>연간 자동차세 (비영업)</th><th>7월 매도 시 환급 예상</th></tr></thead><tbody>
<tr><td>1,000cc 이하</td><td>약 104,000원</td><td>약 52,000원</td></tr>
<tr><td>1,600cc</td><td>약 291,200원</td><td>약 147,000원</td></tr>
<tr><td>2,000cc</td><td>약 520,000원</td><td>약 262,000원</td></tr>
<tr><td>3,000cc</td><td>약 780,000원</td><td>약 393,000원</td></tr>
<tr><td>전기차</td><td>130,000원 (정액)</td><td>약 65,000원</td></tr>
</tbody></table>

{cta_block("위택스에서 자동차세 환급 조회하기", "위택스에서 내 자동차세 납부 내역과 환급 가능 금액을 확인하세요", "https://www.wetax.go.kr/", "blue")}

{imgs[1]}

<h2>자동차세 환급 신청 방법</h2>
<h3>방법 1. 자동 환급 (가장 일반적)</h3>
<p>차량을 매도하거나 폐차하면 <strong>관할 시·군·구청에서 자동으로 환급 처리</strong>합니다. 보통 소유권 이전/말소 후 1~3개월 이내에 기존 납부 계좌 또는 등록된 계좌로 입금됩니다.</p>
<h3>방법 2. 위택스(Wetax) 온라인 신청</h3>
<ol>
<li><strong>위택스</strong>(wetax.go.kr) 접속 후 로그인</li>
<li>환급금 조회/신청 메뉴 클릭</li>
<li>환급 대상 확인 후 환급 계좌 등록</li>
<li>환급 신청 완료</li>
</ol>
<h3>방법 3. 정부24 환급금 조회</h3>
<ol>
<li><strong>정부24</strong>(gov.kr) 접속</li>
<li>'미환급금 조회' 서비스 이용</li>
<li>자동차세 환급금 포함 각종 미환급금 일괄 조회 가능</li>
</ol>
<h3>방법 4. ARS 전화 신청</h3>
<p>관할 시·군·구청 세무과에 전화하여 환급 신청 가능합니다.</p>

{cta_block("정부24에서 미환급금 통합 조회", "자동차세 외에도 놓치고 있는 환급금이 있는지 한번에 확인하세요", "https://www.gov.kr/", "yellow")}

<h2>환급 시 주의사항</h2>
<ul>
<li><strong>환급 청구 기한</strong>: 환급 사유 발생일로부터 <strong>5년 이내</strong> 청구해야 합니다. 5년이 지나면 소멸됩니다.</li>
<li><strong>계좌 미등록</strong>: 환급 계좌가 등록되어 있지 않으면 우편 환급 통지서가 발송됩니다. 위택스에서 미리 계좌를 등록해두세요.</li>
<li><strong>체납 세금</strong>: 다른 지방세 체납이 있으면 환급금에서 <strong>자동 충당</strong>됩니다.</li>
<li><strong>연납 할인분</strong>: 환급 시 연납 할인을 받은 부분은 제외하고 계산됩니다.</li>
</ul>

{imgs[2]}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 차를 팔았는데 환급금이 안 들어와요</h3>
<p>A. 보통 소유권 이전 후 <strong>1~3개월</strong> 소요됩니다. 3개월 이상 미입금 시 위택스에서 환급금 조회를 하거나, 관할 구청 세무과에 문의하세요.</p>
<h3>Q. 자동차세 연납을 안 했으면 환급이 없나요?</h3>
<p>A. <strong>기납부한 금액 기준으로 환급</strong>됩니다. 1기분(6월)만 납부한 상태에서 8월에 매도했다면 9~12월분은 매수자가 납부하므로 환급은 발생하지 않습니다.</p>
<h3>Q. 전기차도 환급 대상인가요?</h3>
<p>A. 네, 전기차도 동일하게 적용됩니다. 전기차 자동차세는 <strong>연 13만원(정액)</strong>이므로 환급금은 크지 않습니다.</p>

{cta_block("위택스에서 자동차세 연납 신청하기", "1월에 연납하면 약 5% 할인! 아직 연납 안 했다면 지금 신청하세요", "https://www.wetax.go.kr/", "green")}

<h2>마무리</h2>
<p>자동차를 매도하거나 폐차한 후에는 반드시 자동차세 환급금을 확인하세요. 위택스 또는 정부24에서 간편하게 조회할 수 있으며, 5년 이내에 청구하지 않으면 소멸되니 서둘러 확인하시기 바랍니다.</p>'''
    },

    # 5. 양도세 중과 유예
    {
        "title": "양도세 중과 유예 기간 조건 다주택자 절세 전략 2026 총정리",
        "cat": 8,
        "slug": "capital-gains-tax-suspension-2026",
        "images": [
            ("photo-1560518883-ce09059eeffa", "부동산 양도소득세"),
            ("photo-1450101499163-c8848c66ca85", "양도세 계산 서류"),
            ("photo-1554224155-6726b3ff858f", "다주택자 절세 전략"),
        ],
        "content": lambda imgs: f'''<p style="font-size:17px;line-height:1.8;">다주택자에게 적용되는 <strong>양도소득세 중과세율</strong>이 2026년에도 유예 상태입니다. 정부는 부동산 시장 안정화를 위해 다주택자 양도세 중과를 한시적으로 유예하고 있으며, 이 기간에 매도하면 <strong>기본세율(6~45%)</strong>만 적용받아 수천만 원의 세금을 절약할 수 있습니다. 양도세 중과 유예 조건, 기간, 절세 전략을 총정리합니다.</p>

{imgs[0]}

<h2>양도세 중과란?</h2>
<p>양도소득세 중과란 <strong>조정대상지역 내 다주택자</strong>가 주택을 매도할 때 기본세율에 추가로 세금을 부과하는 제도입니다.</p>
<table><thead><tr><th>구분</th><th>기본세율</th><th>중과세율 (유예 전)</th></tr></thead><tbody>
<tr><td>2주택자</td><td>6~45%</td><td>기본세율 + 20%p (최대 65%)</td></tr>
<tr><td>3주택 이상</td><td>6~45%</td><td>기본세율 + 30%p (최대 75%)</td></tr>
</tbody></table>
<p>예를 들어 양도차익 3억원인 2주택자의 경우:</p>
<table><thead><tr><th>구분</th><th>세율</th><th>예상 세금</th><th>차이</th></tr></thead><tbody>
<tr><td>중과 적용 시</td><td>약 55~65%</td><td>약 1.6~1.9억원</td><td>-</td></tr>
<tr><td>유예(기본세율) 시</td><td>약 35~38%</td><td>약 1.0~1.1억원</td><td><strong>약 6,000만~8,000만원 절약</strong></td></tr>
</tbody></table>

<h2>2026년 양도세 중과 유예 현황</h2>
<p>정부는 2022년 5월부터 <strong>다주택자 양도세 중과를 한시적으로 유예</strong>하고 있습니다.</p>
<table><thead><tr><th>항목</th><th>내용</th></tr></thead><tbody>
<tr><td>유예 시작일</td><td>2022년 5월 10일</td></tr>
<tr><td>현재 유예 기한</td><td>2026년 5월 9일까지 (연장 가능성 있음)</td></tr>
<tr><td>적용 대상</td><td>조정대상지역 내 2주택 이상 보유자</td></tr>
<tr><td>유예 효과</td><td>중과세율 대신 기본세율(6~45%) 적용</td></tr>
<tr><td>장기보유특별공제</td><td>유예 기간 중 적용 가능 (최대 30%)</td></tr>
</tbody></table>

{cta_block("국세청 홈택스에서 양도세 모의계산", "홈택스에서 내 양도소득세를 직접 계산해보세요", "https://www.hometax.go.kr/", "blue")}

{imgs[1]}

<h2>양도세 기본세율 구간 (2026년)</h2>
<table><thead><tr><th>과세표준</th><th>세율</th><th>누진공제</th></tr></thead><tbody>
<tr><td>1,400만원 이하</td><td>6%</td><td>-</td></tr>
<tr><td>1,400만~5,000만원</td><td>15%</td><td>126만원</td></tr>
<tr><td>5,000만~8,800만원</td><td>24%</td><td>576만원</td></tr>
<tr><td>8,800만~1.5억원</td><td>35%</td><td>1,544만원</td></tr>
<tr><td>1.5억~3억원</td><td>38%</td><td>1,994만원</td></tr>
<tr><td>3억~5억원</td><td>40%</td><td>2,594만원</td></tr>
<tr><td>5억~10억원</td><td>42%</td><td>3,594만원</td></tr>
<tr><td>10억원 초과</td><td>45%</td><td>6,594만원</td></tr>
</tbody></table>

<h2>다주택자 절세 전략 5가지</h2>
<h3>1. 중과 유예 기간 내 매도</h3>
<p>가장 확실한 절세 방법입니다. <strong>2026년 5월 9일 이전</strong>에 잔금일(또는 등기이전일)을 맞추세요. 양도일 기준은 잔금 수령일과 등기이전일 중 빠른 날입니다.</p>
<h3>2. 장기보유특별공제 활용</h3>
<p>중과 유예 기간에는 장기보유특별공제도 적용됩니다. <strong>보유 기간 3년 이상</strong>이면 연 2%씩 최대 30%까지 공제됩니다.</p>
<table><thead><tr><th>보유 기간</th><th>공제율</th></tr></thead><tbody>
<tr><td>3년</td><td>6%</td></tr>
<tr><td>5년</td><td>10%</td></tr>
<tr><td>10년</td><td>20%</td></tr>
<tr><td>15년 이상</td><td>30%</td></tr>
</tbody></table>
<h3>3. 1세대 1주택 비과세 만들기</h3>
<p>다주택 중 1채를 매도하여 <strong>1주택자가 되면</strong>, 남은 주택은 2년 보유(조정지역은 2년 거주 추가) 후 비과세(양도차익 12억원까지)를 받을 수 있습니다.</p>
<h3>4. 부부 공동명의 활용</h3>
<p>부부 공동명의로 전환하면 양도차익이 나눠져 <strong>낮은 세율 구간</strong>이 적용됩니다. 다만 증여세(6억원 배우자 공제)와 취득세를 감안해야 합니다.</p>
<h3>5. 필요경비 최대한 확보</h3>
<p>양도차익을 줄이는 가장 기본적인 방법입니다. <strong>취득세, 중개수수료, 인테리어 비용, 법무사 비용</strong> 등의 영수증을 반드시 보관하세요.</p>

{cta_block("세무사 상담으로 절세 전략 확인", "다주택자 양도세는 세무사 상담이 필수입니다", "https://www.nts.go.kr/", "yellow")}

{imgs[2]}

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 중과 유예가 2026년 5월 이후에도 연장될까요?</h3>
<p>A. 정부 정책에 따라 달라지지만, 부동산 시장 상황에 따라 <strong>추가 연장 가능성</strong>이 있습니다. 다만 확정되지 않았으므로 유예 기간 내 매도를 계획하는 것이 안전합니다.</p>
<h3>Q. 양도일 기준이 계약일인가요, 잔금일인가요?</h3>
<p>A. <strong>잔금 수령일과 등기이전일 중 빠른 날</strong>이 양도일입니다. 유예 기간 내 매도하려면 잔금일을 기준으로 계획하세요.</p>
<h3>Q. 비조정대상지역은 중과 유예와 관계없나요?</h3>
<p>A. 맞습니다. 비조정대상지역은 원래부터 <strong>중과가 적용되지 않으므로</strong> 기본세율이 적용됩니다. 유예와 관계없이 동일합니다.</p>
<h3>Q. 분양권이나 입주권도 중과 유예 대상인가요?</h3>
<p>A. 분양권은 주택 수에 포함되며, <strong>조정지역 내 분양권 양도 시에도 중과 유예가 적용</strong>됩니다.</p>

{cta_block("홈택스에서 양도세 신고하기", "양도소득세 예정신고는 양도일이 속하는 달의 말일부터 2개월 이내입니다", "https://www.hometax.go.kr/", "green")}

<h2>마무리</h2>
<p>양도세 중과 유예는 다주택자에게 수천만 원의 절세 기회를 제공합니다. 유예 기간이 종료되기 전에 매도 계획이 있다면 서둘러 진행하고, 반드시 세무사 상담을 받아 최적의 절세 전략을 세우세요.</p>'''
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

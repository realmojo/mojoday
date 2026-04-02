import json
import urllib.request
import urllib.error
import base64
import time
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API = "https://devupbox.com/wp-json/wp/v2/posts"

# Categories: IT정보=5, 금융=8, 대출=6, 수입차=10, 국산차=9, 엑셀=12, 인터넷=3, 지식=13

def make_cta(cta):
    border = cta.get("border", "none")
    return f'''<div style="background: {cta['bg']}; border: {border}; border-radius: 12px; padding: 28px 24px; margin: 32px 0; text-align: center; color: {cta['text_color']};">
<p style="font-size: 20px; font-weight: 700; margin: 0 0 8px 0; color: {cta['text_color']};">{cta['text']}</p>
<p style="font-size: 15px; margin: 0 0 18px 0; color: {cta['desc_color']};">{cta['desc']}</p>
<a href="{cta['url']}" target="_blank" rel="noopener noreferrer" style="display: inline-block; background: {cta['btn_bg']}; color: {cta['btn_color']}; font-weight: 700; font-size: 16px; padding: 14px 36px; border-radius: 8px; text-decoration: none;">자세히 알아보기 →</a>
</div>'''


def build_content(post):
    html = f"<p>{post['intro']}</p>\n\n"
    sections = post['sections']
    ctas = post['ctas']

    cta_positions = []
    n = len(sections)
    if n >= 3:
        cta_positions = [n // 3, 2 * n // 3]
    elif n >= 2:
        cta_positions = [1]

    for i, (title, content) in enumerate(sections):
        html += f"<h2>{title}</h2>\n{content}\n\n"
        if i in cta_positions and ctas:
            html += make_cta(ctas.pop(0)) + "\n\n"

    if post.get('faq'):
        if ctas:
            html += make_cta(ctas.pop(0)) + "\n\n"
        html += "<h2>자주 묻는 질문 (FAQ)</h2>\n\n"
        for q, a in post['faq']:
            html += f"<h3>Q. {q}</h3>\n<p>{a}</p>\n\n"

    html += "<h2>마무리</h2>\n"
    html += f"<p>이 글이 도움이 되셨다면 주변에도 공유해주세요. 더 궁금한 점이 있다면 댓글로 남겨주시기 바랍니다.</p>"
    return html


def publish_post(post):
    content = build_content(post)
    data = json.dumps({
        "title": post["title"],
        "content": content,
        "status": "publish",
        "categories": [post["cat"]],
        "slug": post["slug"],
    }).encode()
    req = urllib.request.Request(API, data=data, headers={
        "Authorization": f"Basic {AUTH}",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            print(f"✅ Published: {post['title']} → {result.get('link','')}")
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"❌ Error {e.code}: {post['title']} → {body[:200]}")
        return False


POSTS = [
    # ===== POST 1 =====
    {
        "title": "생애최초 주택구입 대출 조건 한도 금리 2026 총정리",
        "cat": 6,
        "slug": "first-home-loan-guide-2026",
        "intro": "<strong>생애최초 주택구입 대출</strong>은 처음으로 내 집을 마련하는 분들을 위한 정부 지원 대출입니다. 일반 주택담보대출보다 금리가 낮고 LTV 한도가 높아 내 집 마련 첫걸음으로 가장 인기 있는 상품입니다. 2026년 기준 조건, 한도, 금리, 신청 방법까지 이 글 하나로 완벽하게 정리했습니다. 생애최초 주택구입자라면 반드시 확인하세요.",
        "sections": [
            ("생애최초 주택구입 대출이란?", "<p><strong>생애최초 주택구입 대출</strong>은 생애 처음으로 주택을 구입하는 무주택자를 위해 정부(주택도시기금)가 지원하는 저금리 정책 대출입니다. 일반 주택담보대출 대비 <strong>LTV 우대(최대 80%)</strong>와 <strong>낮은 금리</strong>가 핵심 혜택입니다.</p><ul><li>취급 기관: 우리은행, 기업은행, 국민은행, 농협, 신한은행, 하나은행 등 주요 시중은행</li><li>재원: 주택도시기금</li><li>대출 목적: 주거용 주택 구입</li></ul><p>생애최초 특별공급과는 별개 개념으로, 아파트 외에도 연립·다세대·단독주택 구입에도 활용할 수 있습니다.</p>"),
            ("2026년 생애최초 대출 자격 조건", "<h3>기본 자격 요건</h3><ul><li><strong>무주택 세대주</strong>: 본인 및 세대원 모두 무주택이어야 함</li><li><strong>생애최초</strong>: 과거 주택 소유 이력이 없어야 함 (매매·상속·증여 모두 포함)</li><li><strong>소득 기준</strong>: 부부 합산 연소득 <strong>1억원 이하</strong> (2026년 기준)</li><li><strong>순자산 기준</strong>: 부부 합산 순자산 <strong>4억 6,900만원 이하</strong></li><li><strong>주택 가격</strong>: 수도권 <strong>9억원 이하</strong>, 비수도권 <strong>5억원 이하</strong></li><li><strong>전용면적</strong>: 전용 <strong>85㎡ 이하</strong> (읍·면 지역 100㎡ 이하)</li></ul><h3>우대 조건 (금리 추가 인하)</h3><ul><li>신혼부부(혼인 7년 이내): 연 0.2% 우대</li><li>다자녀 가구: 자녀 수에 따라 연 0.3~0.5% 우대</li><li>전자계약 체결: 연 0.1% 우대</li><li>청약저축 가입 기간별 우대: 최대 연 0.3% 우대</li></ul>"),
            ("생애최초 주택구입 대출 한도 및 금리 비교", "<table><thead><tr><th>구분</th><th>디딤돌 대출(생애최초)</th><th>보금자리론</th><th>은행 자체 생애최초 대출</th></tr></thead><tbody><tr><td>취급 기관</td><td>주택도시기금 협약 은행</td><td>주택금융공사</td><td>각 시중은행</td></tr><tr><td>LTV 한도</td><td>최대 80%</td><td>최대 70%</td><td>최대 70~80%</td></tr><tr><td>DTI 한도</td><td>60%</td><td>60%</td><td>50~60%</td></tr><tr><td>DSR 적용</td><td>스트레스 DSR 적용</td><td>스트레스 DSR 적용</td><td>스트레스 DSR 적용</td></tr><tr><td>대출 한도</td><td>최대 3억원</td><td>최대 3.6억원</td><td>LTV 범위 내</td></tr><tr><td>금리(2026)</td><td>연 2.45~3.55%</td><td>연 3.65~4.55%</td><td>연 3.5~5.5%</td></tr><tr><td>상환 방식</td><td>원리금균등/원금균등</td><td>원리금균등</td><td>다양</td></tr></tbody></table><p><strong>생애최초 디딤돌 대출</strong>이 금리 측면에서 가장 유리합니다. 단, 소득 요건이 맞아야 신청 가능합니다.</p>"),
            ("신청 방법 단계별 가이드", "<ol><li><strong>사전 자격 확인</strong>: 주택도시기금 홈페이지(nhuf.molit.go.kr)에서 자격 조건 사전 점검</li><li><strong>주택 매매 계약 체결</strong>: 대출 신청 전 주택 매매계약서 작성 필수</li><li><strong>은행 방문 or 온라인 신청</strong>: 협약 은행(우리·국민·기업·농협·신한·하나) 방문 또는 인터넷뱅킹 신청</li><li><strong>서류 제출</strong>: 주민등록등본, 가족관계증명서, 매매계약서, 소득 증빙서류(근로소득원천징수영수증 or 사업소득 확인서), 무주택 확인서</li><li><strong>심사 및 승인</strong>: 통상 7~14일 소요</li><li><strong>잔금 지급일 대출 실행</strong>: 잔금일에 맞춰 대출금 지급</li></ol><p><strong>Tip:</strong> 잔금일 최소 2~3주 전에 신청하는 것이 안전합니다.</p>"),
            ("주의사항 및 실전 꿀팁", "<h3>놓치기 쉬운 주의사항</h3><ul><li><strong>상속·증여도 주택 소유 이력에 포함</strong>됩니다. 과거 짧은 기간이라도 소유 이력이 있으면 생애최초 요건 미충족입니다.</li><li>대출 실행 후 <strong>1개월 이내 전입신고</strong>를 해야 합니다. 미이행 시 대출금 즉시 상환 요구를 받을 수 있습니다.</li><li>대출 실행 후 <strong>5년간 주거 의무</strong>가 있어 임대 목적으로 활용 불가합니다.</li><li>DSR(총부채원리금상환비율) 규제로 소득 대비 대출 한도가 제한될 수 있습니다.</li></ul><h3>꿀팁</h3><ul><li>부부라면 <strong>청약저축 가입 기간이 긴 배우자</strong> 명의로 대출 신청 시 우대금리 최대화 가능</li><li>전자계약으로 매매계약 시 금리 0.1% 추가 인하 혜택 있음</li><li>생애최초 LTV 80% 적용 시 취득세 50% 감면(수도권 1.5억 이하)도 함께 챙기세요</li></ul>"),
            ("생애최초 주택 취득세 감면 혜택", "<p>생애최초 주택 구입 시 <strong>취득세 감면 혜택</strong>도 함께 챙길 수 있습니다.</p><table><thead><tr><th>주택 가격</th><th>원래 취득세율</th><th>생애최초 감면 후</th></tr></thead><tbody><tr><td>1억 5천만원 이하</td><td>1%</td><td>전액 면제(0%)</td></tr><tr><td>1억 5천~3억원</td><td>1%</td><td>50% 감면</td></tr><tr><td>3억~9억원(수도권)</td><td>1~3%</td><td>50% 감면 (최대 200만원)</td></tr></tbody></table><p>취득세 감면은 주소지 관할 시군구청에 <strong>잔금일로부터 60일 이내</strong>에 신청해야 합니다.</p>"),
        ],
        "faq": [
            ("배우자가 과거에 주택을 소유했다면 생애최초 요건이 안 되나요?", "네, <strong>세대원 중 한 명이라도 과거 주택 소유 이력이 있으면 생애최초 요건을 충족하지 못합니다.</strong> 배우자의 이력도 포함됩니다. 단, 혼인 전 배우자가 주택을 소유했다가 처분한 경우도 해당됩니다."),
            ("부부 합산 소득 1억원이 넘으면 아예 신청 불가인가요?", "<strong>디딤돌 대출(생애최초 포함)은 소득 제한이 있어 1억원 초과 시 신청 불가</strong>입니다. 이 경우 보금자리론이나 은행 자체 생애최초 우대 상품을 검토하세요."),
            ("전세로 거주 중인데 생애최초 대출 신청 가능한가요?", "전세 거주는 무주택으로 인정됩니다. <strong>주택을 소유하지 않은 상태에서 매매계약을 체결하면 신청 가능</strong>합니다."),
            ("대출 한도가 부족하면 어떻게 해야 하나요?", "디딤돌 대출 한도(최대 3억원)가 부족한 경우 <strong>은행의 일반 주택담보대출과 병행</strong>하거나 보금자리론을 검토하세요. 단, 기금 대출과 일반 대출 병행 시 규정에 따라 제한이 있을 수 있습니다."),
            ("아파트 외 빌라, 단독주택도 생애최초 대출 가능한가요?", "네, <strong>아파트뿐 아니라 연립·다세대·단독주택도 대상</strong>입니다. 다만 주택 가격 기준(수도권 9억 이하)과 전용면적 기준(85㎡ 이하)은 동일하게 적용됩니다."),
        ],
        "ctas": [
            {"text": "생애최초 대출 자격 지금 바로 확인하기", "desc": "주택도시기금 공식 홈페이지에서 나의 대출 가능 여부를 확인하세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "은행별 생애최초 대출 금리 한눈에 비교", "desc": "핀크에서 내 조건에 맞는 생애최초 대출 상품을 비교해보세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "무료 대출 상담 받아보기", "desc": "토스에서 내 조건에 맞는 주택 대출을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 2 =====
    {
        "title": "주택담보대출 LTV DTI DSR 계산법 쉽게 이해하기 2026",
        "cat": 6,
        "slug": "mortgage-ltv-dti-dsr-calculation-2026",
        "intro": "주택담보대출을 알아보다 보면 반드시 마주치는 세 가지 용어가 있습니다. 바로 <strong>LTV, DTI, DSR</strong>입니다. 이 세 가지 지표가 대출 한도를 결정하는 핵심이지만, 처음 접하는 분들에게는 매우 낯설고 복잡하게 느껴집니다. 2026년 최신 규제 기준에 맞춰 LTV·DTI·DSR의 개념과 실제 계산 방법을 쉽고 명확하게 설명합니다.",
        "sections": [
            ("LTV(주택담보인정비율)란?", "<p><strong>LTV(Loan to Value ratio)</strong>는 주택 가격 대비 대출 가능 금액의 비율입니다. 예를 들어 LTV 70%라면 10억짜리 아파트에 최대 7억원까지 대출 가능합니다.</p><p><strong>계산식:</strong> LTV = 대출금액 ÷ 주택 가격 × 100</p><table><thead><tr><th>지역/구분</th><th>무주택자</th><th>1주택자</th><th>2주택 이상</th></tr></thead><tbody><tr><td>투기과열지구</td><td>최대 50%</td><td>대출 불가(일부 예외)</td><td>대출 불가</td></tr><tr><td>조정대상지역</td><td>최대 50%</td><td>대출 불가(일부 예외)</td><td>대출 불가</td></tr><tr><td>기타 지역</td><td>최대 70%</td><td>최대 60%</td><td>최대 50%</td></tr><tr><td>생애최초(전국)</td><td>최대 80%</td><td>해당없음</td><td>해당없음</td></tr></tbody></table><p><strong>2026년 기준:</strong> 서울 일부 지역은 투기과열지구로 지정되어 LTV 50% 제한이 적용됩니다. 지역별 규제는 수시로 바뀌므로 반드시 최신 정보를 확인하세요.</p>"),
            ("DTI(총부채상환비율)란?", "<p><strong>DTI(Debt to Income ratio)</strong>는 연간 소득 대비 연간 원리금 상환액의 비율입니다. 소득을 기준으로 대출 부담 능력을 측정합니다.</p><p><strong>계산식:</strong> DTI = (주택담보대출 연간 원리금 상환액 + 기타 부채 연간 이자 상환액) ÷ 연간 소득 × 100</p><h3>DTI 계산 예시</h3><ul><li>연소득: 6,000만원</li><li>DTI 한도: 60%</li><li>최대 연간 원리금: 3,600만원</li><li>월 최대 상환액: 300만원</li></ul><p>기존 자동차 할부, 신용대출 이자도 DTI 계산에 포함되므로 <strong>기존 부채가 많으면 주담대 한도가 줄어듭니다.</strong></p>"),
            ("DSR(총부채원리금상환비율)란?", "<p><strong>DSR(Debt Service Ratio)</strong>은 DTI보다 더 강화된 규제로, 모든 금융 부채(주담대·신용대출·카드론·자동차 할부 등)의 원금과 이자를 모두 합산합니다.</p><p><strong>계산식:</strong> DSR = 모든 부채의 연간 원리금 상환액 합계 ÷ 연간 소득 × 100</p><table><thead><tr><th>대출 종류</th><th>DSR 한도</th><th>비고</th></tr></thead><tbody><tr><td>은행권 대출</td><td>40%</td><td>2022년 7월부터 전면 적용</td></tr><tr><td>2금융권 대출</td><td>50%</td><td>카드사·저축은행·보험사 등</td></tr><tr><td>정책 모기지</td><td>별도 적용</td><td>디딤돌·보금자리론 별도</td></tr></tbody></table><p><strong>2026년 스트레스 DSR</strong>: 변동금리 대출에 스트레스 금리(약 1.5%)를 가산하여 DSR을 계산합니다. 이 때문에 실제 대출 가능 금액이 더 줄어들 수 있습니다.</p>"),
            ("LTV·DTI·DSR 실제 적용 예시", "<h3>사례: 서울 아파트 구입 (기타 지역 기준, 무주택자)</h3><ul><li>아파트 시세: 8억원</li><li>연소득: 8,000만원</li><li>기존 대출: 자동차 할부 월 50만원</li></ul><p><strong>LTV 계산</strong>: 8억 × 70% = 5억 6,000만원 (LTV 한도)</p><p><strong>DSR 계산</strong>: 연소득 8,000만원 × 40% = 3,200만원 (연간 최대 원리금)<br>자동차 할부 연간: 600만원 → 주담대 허용 원리금: 2,600만원<br>금리 4%, 30년 원리금균등 기준 → 약 <strong>5억 4,500만원</strong> 대출 가능</p><p><strong>최종 대출 가능액: LTV와 DSR 중 낮은 값 적용 → 약 5억 4,500만원</strong></p>"),
            ("대출 한도 높이는 실전 전략", "<ul><li><strong>기존 소액 대출 정리</strong>: 마이너스통장, 소액 신용대출 해지 → DSR 계산에서 제외</li><li><strong>소득 증빙 최대화</strong>: 부업 소득, 임대 소득, 배우자 소득 합산 신청</li><li><strong>고정금리 선택</strong>: 스트레스 DSR 적용 시 고정금리가 변동금리보다 한도 유리</li><li><strong>상환 기간 늘리기</strong>: 30년 → 40년 상환으로 월 원리금 낮춰 DSR 여유 확보</li><li><strong>부부 공동 명의</strong>: 배우자 소득이 있다면 공동 대출로 합산 소득 적용 가능</li></ul>"),
            ("2026년 주요 규제 변경 사항", "<table><thead><tr><th>규제</th><th>2025년</th><th>2026년</th><th>변경 내용</th></tr></thead><tbody><tr><td>스트레스 DSR</td><td>1.5% 가산</td><td>1.5% 유지</td><td>변동금리 대출에 적용</td></tr><tr><td>생애최초 LTV</td><td>80%</td><td>80%</td><td>유지</td></tr><tr><td>투기과열지구 LTV</td><td>50%</td><td>50%</td><td>유지</td></tr><tr><td>은행 DSR</td><td>40%</td><td>40%</td><td>전면 적용 유지</td></tr></tbody></table><p>규제는 정부 정책에 따라 수시로 변경될 수 있으므로, 대출 신청 전 <strong>금융감독원 금융소비자정보포털</strong>에서 최신 규제를 확인하는 것을 권장합니다.</p>"),
        ],
        "faq": [
            ("DSR 40%가 적용된다면 실제로 얼마나 빌릴 수 있나요?", "연소득 6,000만원 기준 DSR 40% 적용 시 연간 원리금 최대 2,400만원(월 200만원)입니다. 금리 4%, 30년 상환 시 약 <strong>4억 1,000만원</strong> 수준입니다. 기존 부채가 없을 때 기준이며, 기존 대출이 있다면 그만큼 한도가 줄어듭니다."),
            ("전세자금대출도 DSR에 포함되나요?", "원칙적으로 전세자금대출은 DSR 산정에서 제외됩니다. 다만 <strong>일부 상품에 따라 다를 수 있으므로</strong> 은행에 직접 확인하세요."),
            ("LTV가 70%인데 집값의 70%를 전부 빌릴 수 있나요?", "LTV는 최대 한도이고, <strong>DSR 규제가 동시에 적용</strong>됩니다. 둘 중 낮은 한도가 실제 대출 가능액이 됩니다. 또한 기존 선순위 대출·임차 보증금도 LTV 계산에서 차감됩니다."),
            ("스트레스 DSR이 뭔가요?", "변동금리 대출의 경우 금리가 오를 경우를 대비해 <strong>현재 금리에 스트레스 금리(약 1.5%)를 더해</strong> DSR을 계산하는 방식입니다. 예를 들어 현재 금리 4%라면 5.5%로 계산해 한도를 산정합니다."),
        ],
        "ctas": [
            {"text": "나의 주담대 한도 지금 계산해보기", "desc": "금융감독원 금융소비자정보포털에서 대출 가능 금액을 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "은행별 주택담보대출 금리 비교", "desc": "핀크에서 내 조건에 맞는 주담대 금리를 한눈에 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "주담대 전문 상담 받아보기", "desc": "토스에서 나의 대출 한도와 최적 상품을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 3 =====
    {
        "title": "디딤돌 대출 조건 금리 한도 신청 방법 2026 최신",
        "cat": 6,
        "slug": "diditmdol-loan-conditions-2026",
        "intro": "<strong>디딤돌 대출</strong>은 주택도시기금이 지원하는 대표적인 정책형 주택구입 대출로, 시중 은행보다 훨씬 낮은 금리와 높은 LTV 한도가 특징입니다. 무주택 서민·중산층의 내 집 마련을 위해 2026년에도 꾸준히 인기 있는 상품입니다. 이 글에서 디딤돌 대출의 자격 조건, 금리, 한도, 신청 방법을 2026년 최신 기준으로 완벽 정리했습니다.",
        "sections": [
            ("디딤돌 대출이란?", "<p><strong>디딤돌 대출</strong>은 주택도시기금에서 운영하는 주택구입 자금 대출로, 소득 기준을 충족하는 무주택 세대주에게 시중 금리보다 낮은 우대 금리를 제공합니다. 협약 은행(국민·우리·기업·농협·신한·하나 등)을 통해 신청합니다.</p><ul><li>재원: 주택도시기금</li><li>목적: 주거용 주택 구입(아파트·연립·다세대·단독주택)</li><li>특징: 저금리 + 높은 LTV + 장기 분할 상환</li></ul>"),
            ("2026년 디딤돌 대출 자격 조건", "<table><thead><tr><th>구분</th><th>일반 디딤돌</th><th>생애최초 디딤돌</th><th>신혼가구 디딤돌</th></tr></thead><tbody><tr><td>세대주 요건</td><td>무주택 세대주</td><td>무주택 세대주(생애최초)</td><td>무주택 세대주</td></tr><tr><td>소득 기준</td><td>부부합산 6,000만원 이하</td><td>부부합산 7,000만원 이하</td><td>부부합산 7,500만원 이하</td></tr><tr><td>순자산 기준</td><td>4.69억원 이하</td><td>4.69억원 이하</td><td>4.69억원 이하</td></tr><tr><td>주택 가격</td><td>5억원 이하</td><td>수도권 9억, 비수도권 5억</td><td>수도권 9억, 비수도권 5억</td></tr><tr><td>전용면적</td><td>85㎡ 이하</td><td>85㎡ 이하</td><td>85㎡ 이하</td></tr><tr><td>LTV 한도</td><td>최대 70%</td><td>최대 80%</td><td>최대 80%</td></tr></tbody></table>"),
            ("2026년 디딤돌 대출 금리 상세", "<h3>소득 구간별 기준 금리</h3><table><thead><tr><th>연소득</th><th>만기 10년</th><th>만기 15년</th><th>만기 20년</th><th>만기 30년</th></tr></thead><tbody><tr><td>2,000만원 이하</td><td>연 2.45%</td><td>연 2.55%</td><td>연 2.65%</td><td>연 2.75%</td></tr><tr><td>2,000~4,000만원</td><td>연 2.70%</td><td>연 2.80%</td><td>연 2.90%</td><td>연 3.00%</td></tr><tr><td>4,000~6,000만원</td><td>연 3.00%</td><td>연 3.10%</td><td>연 3.20%</td><td>연 3.30%</td></tr><tr><td>6,000~7,000만원</td><td>연 3.25%</td><td>연 3.35%</td><td>연 3.45%</td><td>연 3.55%</td></tr></tbody></table><h3>우대 금리 항목 (중복 적용 가능)</h3><ul><li>청약저축 가입 1년 이상: -0.1%</li><li>청약저축 가입 3년 이상: -0.2%</li><li>청약저축 가입 5년 이상 + 96회 납입: -0.3%</li><li>전자계약 체결: -0.1%</li><li>부동산 안심거래: -0.1%</li><li>신혼가구(7년 이내): -0.2%</li><li>2자녀: -0.3%, 3자녀 이상: -0.5%</li></ul>"),
            ("대출 한도 및 상환 방식", "<ul><li><strong>대출 한도</strong>: 최대 3억원(생애최초·신혼 최대 3억원, 일반 최대 2억 5,000만원)</li><li><strong>상환 방식</strong>: 원리금균등상환, 원금균등상환, 체증식 상환(소득이 늘 것으로 예상되는 경우)</li><li><strong>대출 기간</strong>: 10·15·20·30년 선택 가능</li><li><strong>중도상환수수료</strong>: 대출일로부터 3년 이내 중도상환 시 수수료 부과(1.2%→0.6%→0% 단계적 감소)</li></ul><h3>체증식 상환 예시</h3><p>초기에 원리금 부담을 줄이고 이후 점점 늘려가는 방식으로, <strong>신혼부부나 사회초년생</strong>에게 적합합니다.</p>"),
            ("신청 서류 및 절차", "<ol><li><strong>주택 매매계약 체결</strong></li><li><strong>협약 은행 방문 또는 온라인 신청</strong></li><li><strong>필요 서류 제출</strong></li></ol><h3>필수 서류 목록</h3><ul><li>주민등록등본 및 가족관계증명서 (3개월 이내)</li><li>무주택 확인서 (협약 은행 제공 양식)</li><li>주택 매매계약서 사본</li><li>소득 증빙 서류: 근로소득자→근로소득원천징수영수증, 자영업자→사업소득 확인서·세금계산서</li><li>청약저축 납입 확인서 (우대금리 적용 시)</li><li>등기부등본 (잔금 지급 후)</li></ul>"),
            ("디딤돌 vs 보금자리론 비교", "<table><thead><tr><th>구분</th><th>디딤돌 대출</th><th>보금자리론</th></tr></thead><tbody><tr><td>운영 기관</td><td>주택도시기금</td><td>주택금융공사(HF)</td></tr><tr><td>소득 제한</td><td>부부합산 6,000~7,500만원</td><td>없음(단, 9억 초과 주택 시 제한)</td></tr><tr><td>주택 가격</td><td>5~9억원 이하</td><td>9억원 이하</td></tr><tr><td>금리 수준</td><td>연 2.45~3.55%</td><td>연 3.65~4.55%</td></tr><tr><td>대출 한도</td><td>최대 3억원</td><td>최대 3.6억원</td></tr><tr><td>LTV</td><td>최대 70~80%</td><td>최대 70%</td></tr><tr><td>적합 대상</td><td>소득 낮은 무주택자</td><td>소득 높거나 한도 더 필요한 경우</td></tr></tbody></table>"),
        ],
        "faq": [
            ("디딤돌 대출 소득 기준 6,000만원은 어떻게 산정하나요?", "부부 합산 <strong>전년도 소득을 기준</strong>으로 합니다. 근로소득은 근로소득원천징수영수증, 자영업 소득은 종합소득세 신고 기준입니다. 소득이 없는 배우자는 0원으로 합산합니다."),
            ("아파트 분양권도 디딤돌 대출 가능한가요?", "분양권은 <strong>잔금일에 가까운 시점에 신청</strong>할 수 있습니다. 입주 시점의 주택 가격이 기준이므로 분양 계약서와 분양가 확인이 필요합니다."),
            ("디딤돌 대출 중도상환하면 불이익이 있나요?", "대출 실행 후 <strong>3년 이내 중도상환 시 수수료(최대 1.2%)</strong>가 부과됩니다. 3년이 지나면 수수료 없이 자유롭게 상환 가능합니다."),
            ("배우자 명의로도 신청 가능한가요?", "세대주 명의로 신청하는 것이 원칙입니다. 단, <strong>배우자도 공동 채무자로 신청</strong>하여 소득 합산으로 대출 한도를 높일 수 있습니다."),
        ],
        "ctas": [
            {"text": "디딤돌 대출 자격 조건 지금 확인", "desc": "주택도시기금 공식 홈페이지에서 나의 자격 여부를 확인하세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "디딤돌 대출 금리 상세 비교", "desc": "핀크에서 나의 소득 조건에 맞는 디딤돌 금리를 확인하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "디딤돌 대출 무료 상담 신청", "desc": "토스에서 디딤돌 대출 한도와 월 상환액을 계산해보세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 4 =====
    {
        "title": "버팀목 전세자금대출 조건 한도 금리 총정리 2026",
        "cat": 6,
        "slug": "butimok-jeonse-loan-2026",
        "intro": "<strong>버팀목 전세자금대출</strong>은 주택도시기금에서 지원하는 대표적인 전세 자금 지원 상품으로, 시중 전세대출보다 금리가 크게 낮아 무주택 서민들에게 큰 인기를 얻고 있습니다. 2026년 기준 버팀목 전세대출의 자격 조건, 금리, 한도, 신청 방법을 상세하게 정리했습니다. 전세 계약을 앞두고 있다면 반드시 읽어보세요.",
        "sections": [
            ("버팀목 전세자금대출이란?", "<p><strong>버팀목 전세자금대출</strong>은 주택도시기금이 재원을 공급하고 협약 은행(국민·우리·기업·농협·신한·하나 등)이 취급하는 정책 대출입니다. 보증금의 상당 부분을 저금리로 조달할 수 있어 전세 시장에서 필수적인 상품입니다.</p><ul><li>지원 목적: 무주택 세대주의 전세 보증금 마련 지원</li><li>금리: 연 1.8~2.9% (소득·조건에 따라 상이)</li><li>한도: 최대 1억 2,000만원(수도권), 8,000만원(비수도권)</li></ul>"),
            ("2026년 버팀목 전세대출 자격 조건", "<table><thead><tr><th>구분</th><th>일반 버팀목</th><th>청년 버팀목</th><th>신혼부부 버팀목</th></tr></thead><tbody><tr><td>연령</td><td>무주택 세대주</td><td>만 19~34세 무주택</td><td>혼인 7년 이내</td></tr><tr><td>소득 기준</td><td>부부합산 5,000만원 이하</td><td>단독 5,000만원 이하</td><td>부부합산 6,000만원 이하</td></tr><tr><td>순자산</td><td>3.61억원 이하</td><td>3.61억원 이하</td><td>3.61억원 이하</td></tr><tr><td>전세 보증금</td><td>수도권 3억, 비수도권 2억</td><td>수도권 3억, 비수도권 2억</td><td>수도권 4억, 비수도권 3억</td></tr><tr><td>전용면적</td><td>85㎡ 이하</td><td>60㎡ 이하</td><td>85㎡ 이하</td></tr></tbody></table>"),
            ("버팀목 전세대출 금리 상세 (2026년 기준)", "<table><thead><tr><th>소득 구간</th><th>일반</th><th>청년 우대</th><th>신혼부부 우대</th></tr></thead><tbody><tr><td>2,000만원 이하</td><td>연 1.8%</td><td>연 1.5%</td><td>연 1.5%</td></tr><tr><td>2,000~4,000만원</td><td>연 2.1%</td><td>연 1.8%</td><td>연 1.8%</td></tr><tr><td>4,000~5,000만원</td><td>연 2.4%</td><td>연 2.1%</td><td>연 2.1%</td></tr><tr><td>5,000~6,000만원</td><td>-</td><td>-</td><td>연 2.4%</td></tr></tbody></table><h3>우대 금리 적용 항목</h3><ul><li>부동산 전자계약 체결: -0.1%</li><li>주거안정 월세대출 성실 납부자: -0.2%</li><li>다자녀(2명 이상): -0.5%</li><li>장애인 가구: -0.2%</li></ul>"),
            ("한도 및 신청 방법", "<h3>대출 한도</h3><ul><li>일반·청년: 수도권 최대 <strong>1억 2,000만원</strong>, 비수도권 최대 <strong>8,000만원</strong></li><li>신혼부부: 수도권 최대 <strong>2억 2,000만원</strong>, 비수도권 최대 <strong>1억 6,000만원</strong></li><li>LTV 기준: 전세 보증금의 최대 80%</li></ul><h3>신청 절차</h3><ol><li>전세 계약 체결 (보증금·계약 기간 확인)</li><li>협약 은행 방문 또는 인터넷뱅킹 신청</li><li>서류 제출 및 심사</li><li>보증 기관(HUG or HF) 보증서 발급</li><li>잔금일 대출 실행</li></ol>"),
            ("필요 서류 목록", "<ul><li>주민등록등본, 가족관계증명서</li><li>전세 계약서 사본</li><li>확정일자 부여 확인서</li><li>건물 등기부등본</li><li>소득 증빙: 근로소득원천징수영수증 or 사업소득 확인서</li><li>무주택 확인서 (은행 제공 양식)</li><li>보증금 납입 영수증 (계약금)</li></ul>"),
            ("버팀목 대출 주의사항 및 꿀팁", "<h3>주의사항</h3><ul><li><strong>전입신고 필수</strong>: 대출 실행 후 즉시 전입신고 및 확정일자 취득해야 보증 효력 발생</li><li><strong>갱신 시 재신청 필요</strong>: 계약 갱신 시 대출도 갱신 신청이 필요합니다</li><li><strong>임대인 동의 필요 없음</strong>: 임차인 단독으로 신청 가능</li><li><strong>근저당 확인</strong>: 대상 주택의 선순위 근저당이 보증금의 60% 초과 시 대출 제한</li></ul><h3>꿀팁</h3><ul><li>전자계약서 작성 시 금리 0.1% 인하 혜택 + 서류 제출 간소화</li><li>부부 합산 소득이 높다면 청년 버팀목(개인 소득 기준)으로 신청하는 것이 유리할 수 있음</li></ul>"),
        ],
        "faq": [
            ("버팀목 전세대출은 오피스텔도 가능한가요?", "주거용 오피스텔은 가능합니다. 단, <strong>건축물 대장에 주거용으로 등재</strong>되어야 하며 전용면적 기준을 충족해야 합니다."),
            ("전세 계약 중간에 버팀목 대출을 신청할 수 있나요?", "원칙적으로 <strong>잔금일 또는 전세 계약일로부터 3개월 이내</strong>에 신청해야 합니다. 계약 중간에는 원칙적으로 불가하나, 갱신 계약의 경우 갱신 시점에 신청 가능합니다."),
            ("버팀목 대출과 시중 전세대출을 동시에 받을 수 있나요?", "원칙적으로 <strong>중복 수혜 불가</strong>입니다. 버팀목 대출을 받으면 시중 전세대출은 불가하며, 한도 초과분은 개인 자금으로 충당해야 합니다."),
            ("소득이 없는 주부도 신청 가능한가요?", "소득이 없는 경우에도 <strong>세대 합산 소득 기준을 충족</strong>하면 신청 가능합니다. 소득이 전혀 없는 경우 0원으로 산정합니다."),
        ],
        "ctas": [
            {"text": "버팀목 전세대출 자격 확인하기", "desc": "주택도시기금 홈페이지에서 나의 자격 요건을 바로 확인하세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "전세대출 금리 비교 한눈에 보기", "desc": "핀크에서 버팀목 대출과 시중 전세대출 금리를 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "전세 계약 전 무료 대출 상담", "desc": "토스에서 전세 보증금 마련 방법을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 5 =====
    {
        "title": "전세 보증금 반환 대출 신청 방법 조건 완벽 가이드",
        "cat": 6,
        "slug": "jeonse-deposit-return-loan-guide",
        "intro": "전세 계약이 끝났는데 집주인이 보증금을 돌려주지 못하는 상황, 이른바 <strong>전세사기·깡통전세</strong> 피해가 증가하면서 전세 보증금 반환 대출의 중요성이 높아졌습니다. 임대인이 보증금을 반환하기 위해 받는 대출과, 임차인이 보호받을 수 있는 보증보험 상품까지 이 글에서 완벽하게 정리합니다.",
        "sections": [
            ("전세 보증금 반환 대출이란?", "<p><strong>전세 보증금 반환 대출</strong>은 전세 계약 만료 시 집주인(임대인)이 새로운 세입자를 구하지 못했거나 자금이 부족한 경우, 기존 임차인에게 보증금을 돌려주기 위해 받는 대출입니다.</p><ul><li>대출 주체: 임대인(집주인)이 차주</li><li>상환 재원: 새 임차인의 보증금 or 주택 매각 대금</li><li>유사 상품: HUG 전세보증금반환보증(임차인 보호)</li></ul>"),
            ("보증금 반환 대출 자격 및 조건", "<h3>임대인 대출 자격</h3><ul><li>주택 소유자(1주택 이상)</li><li>신용등급 및 소득 요건 충족</li><li>담보 주택의 시세 및 선순위 대출 확인</li></ul><h3>은행별 주요 조건 (2026년 기준)</h3><table><thead><tr><th>은행</th><th>금리</th><th>한도</th><th>기간</th><th>특징</th></tr></thead><tbody><tr><td>국민은행</td><td>연 4.5~6.5%</td><td>LTV 60% 이내</td><td>1년(연장 가능)</td><td>전세 반환 목적 명시</td></tr><tr><td>신한은행</td><td>연 4.3~6.3%</td><td>LTV 60% 이내</td><td>1년</td><td>신속 실행 가능</td></tr><tr><td>하나은행</td><td>연 4.4~6.4%</td><td>LTV 60% 이내</td><td>1년</td><td>비대면 신청</td></tr><tr><td>우리은행</td><td>연 4.5~6.5%</td><td>LTV 60% 이내</td><td>1년</td><td>우리WON뱅킹</td></tr><tr><td>농협</td><td>연 4.6~6.6%</td><td>LTV 60% 이내</td><td>1년</td><td>NH앱 신청</td></tr></tbody></table>"),
            ("HUG 전세보증금반환보증 가입법 (임차인 보호)", "<p>임차인이 직접 보호받을 수 있는 가장 확실한 방법은 <strong>HUG(주택도시보증공사) 전세보증금반환보증</strong>에 가입하는 것입니다.</p><h3>HUG 전세보증보험 조건</h3><ul><li>보증 대상: 전세 보증금 수도권 7억원 이하, 비수도권 5억원 이하</li><li>가입 시기: 전세 계약일로부터 계약 기간의 1/2이 지나기 전</li><li>연 보증료: 보증금의 약 0.128~0.154%</li><li>혜택: 집주인이 보증금을 못 돌려주면 HUG가 먼저 대신 반환 후 집주인에게 구상</li></ul>"),
            ("전세사기 피해 시 대처 방법", "<ol><li><strong>임차권 등기 명령 신청</strong>: 계약 만료 후 보증금을 못 받은 경우 법원에 신청. 이사 후에도 대항력·우선변제권 유지</li><li><strong>내용증명 발송</strong>: 집주인에게 보증금 반환 공식 요청</li><li><strong>전세보증보험 청구</strong>: HUG or HF에 가입되어 있다면 즉시 보험금 청구</li><li><strong>경매 참여</strong>: 집주인이 반환 못 할 경우 강제경매 신청 검토</li><li><strong>전세사기 피해자 지원센터</strong>: 국토교통부 운영, 법률·금융 지원 무료 제공</li></ol>"),
            ("보증금 반환 대출 신청 서류", "<ul><li>임대인 신분증 사본</li><li>임대차 계약서 (만료 확인)</li><li>부동산 등기부등본 (발급 3개월 이내)</li><li>임차인 주민등록등본</li><li>소득 증빙 서류 (근로소득원천징수영수증 등)</li><li>은행 제공 전세 반환 목적 확인서</li></ul>"),
            ("전세 보증금 지키는 5가지 체크리스트", "<ol><li><strong>등기부등본 선순위 확인</strong>: 근저당+전세 보증금이 시세의 70% 초과 시 위험</li><li><strong>전세보증보험 가입</strong>: 계약 직후 가입 (반드시 계약 기간 절반 전)</li><li><strong>전입신고 + 확정일자</strong>: 이사 당일 즉시 완료</li><li><strong>임대인 세금 체납 확인</strong>: 국세·지방세 체납 여부 확인 후 계약</li><li><strong>공인중개사 확인</strong>: 중개사 등록 여부 및 책임보험 가입 확인</li></ol>"),
        ],
        "faq": [
            ("집주인이 보증금을 못 주겠다고 하면 어떻게 해야 하나요?", "우선 <strong>임차권 등기 명령을 법원에 신청</strong>하세요. 이후 HUG 전세보증보험이 있다면 보험금 청구, 없다면 법률 지원을 통해 강제경매를 검토해야 합니다. 국토교통부 전세사기 피해 지원센터(1670-1004)에 문의하세요."),
            ("전세보증보험 가입을 계약 후 늦게 하면 안 되나요?", "<strong>계약 기간의 절반이 지나면 가입이 불가</strong>합니다. 예를 들어 2년 계약이라면 1년이 지나기 전까지만 가입 가능합니다. 계약 직후 바로 가입하는 것이 안전합니다."),
            ("전세 계약 시 깡통전세를 어떻게 피할 수 있나요?", "(선순위 근저당 + 전세 보증금) ÷ 시세 비율이 <strong>70% 이하인 매물</strong>을 선택하세요. 이 비율이 80% 이상이면 경매 시 보증금을 돌려받지 못할 위험이 높습니다."),
        ],
        "ctas": [
            {"text": "전세보증보험 가입 조건 확인하기", "desc": "HUG 공식 홈페이지에서 전세보증보험 가입 가능 여부를 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "전세 대출 금리 한눈에 비교", "desc": "핀크에서 전세 관련 대출 상품을 한눈에 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "전세 계약 전 무료 상담 받기", "desc": "토스에서 전세 계약 전 꼭 확인해야 할 사항을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 6 =====
    {
        "title": "아파트 담보대출 은행별 금리 비교 TOP 5 2026",
        "cat": 6,
        "slug": "apartment-mortgage-bank-rate-comparison-2026",
        "intro": "아파트 담보대출은 주택 구입이나 생활자금 마련을 위해 가장 많이 활용되는 금융 상품입니다. 그러나 은행마다 금리, 한도, 조건이 크게 다르기 때문에 <strong>꼼꼼한 비교가 필수</strong>입니다. 2026년 기준 주요 5대 은행의 아파트 담보대출 금리와 조건을 한눈에 비교하고, 유리한 상품을 선택하는 방법을 완벽 정리했습니다.",
        "sections": [
            ("아파트 담보대출 기본 개념", "<p><strong>아파트 담보대출</strong>은 본인 소유 아파트를 담보로 금융기관에서 자금을 빌리는 대출입니다. 구입 자금 외에도 생활자금, 사업자금, 기존 대출 상환 등 다양한 목적으로 활용됩니다.</p><ul><li><strong>LTV</strong>: 아파트 시세 대비 대출 비율 (지역·규제에 따라 50~80%)</li><li><strong>금리 유형</strong>: 변동금리(COFIX 연동), 혼합형(5년 고정+변동), 고정금리</li><li><strong>상환 방식</strong>: 원리금균등, 원금균등, 만기일시상환</li></ul>"),
            ("2026년 5대 은행 아파트 담보대출 금리 비교", "<table><thead><tr><th>은행</th><th>변동금리</th><th>혼합형(5년)</th><th>고정금리</th><th>최대 한도</th><th>특징</th></tr></thead><tbody><tr><td>국민은행</td><td>연 3.8~5.2%</td><td>연 3.9~5.3%</td><td>연 4.1~5.5%</td><td>LTV 이내</td><td>KB스타뱅킹 비대면 0.1% 우대</td></tr><tr><td>신한은행</td><td>연 3.7~5.1%</td><td>연 3.85~5.2%</td><td>연 4.0~5.4%</td><td>LTV 이내</td><td>쏠편한 주담대 우대</td></tr><tr><td>하나은행</td><td>연 3.75~5.15%</td><td>연 3.9~5.25%</td><td>연 4.05~5.45%</td><td>LTV 이내</td><td>하나원큐 앱 0.1% 우대</td></tr><tr><td>우리은행</td><td>연 3.8~5.2%</td><td>연 3.95~5.35%</td><td>연 4.1~5.5%</td><td>LTV 이내</td><td>WON주택대출 특화</td></tr><tr><td>농협은행</td><td>연 3.85~5.3%</td><td>연 4.0~5.4%</td><td>연 4.15~5.6%</td><td>LTV 이내</td><td>NH농협 조합원 우대</td></tr></tbody></table><p><strong>※ 2026년 3월 기준 금리이며, 개인 신용도·담보 조건에 따라 달라집니다.</strong></p>"),
            ("인터넷은행 담보대출 비교", "<table><thead><tr><th>은행</th><th>변동금리</th><th>최대 한도</th><th>특징</th></tr></thead><tbody><tr><td>카카오뱅크</td><td>연 3.6~5.0%</td><td>LTV 이내</td><td>100% 비대면, 신속 심사</td></tr><tr><td>케이뱅크</td><td>연 3.65~5.05%</td><td>LTV 이내</td><td>아파트 담보 특화</td></tr></tbody></table><p>인터넷은행은 <strong>지점 방문 없이 100% 비대면</strong>으로 신청 가능하며, 금리도 시중은행 대비 소폭 유리한 경우가 많습니다.</p>"),
            ("금리 우대 조건 총정리", "<h3>은행별 공통 우대 조건</h3><ul><li><strong>급여 이체 지정</strong>: 해당 은행 계좌로 급여 이체 시 0.1~0.3% 인하</li><li><strong>신용카드 사용실적</strong>: 월 30만원 이상 시 0.1% 인하</li><li><strong>자동납부 등록</strong>: 이자 자동이체 시 0.05~0.1% 인하</li><li><strong>비대면 신청</strong>: 앱/인터넷뱅킹 신청 시 0.1% 인하</li><li><strong>우수 고객 등급</strong>: 은행별 우수/VIP 고객 인정 시 추가 우대</li></ul><p>우대 조건을 모두 충족하면 기준 금리 대비 최대 <strong>0.5~0.8%까지 인하</strong> 가능합니다.</p>"),
            ("대출 신청 전 체크리스트", "<ol><li><strong>지역별 LTV 규제 확인</strong>: 투기과열지구·조정지역 여부에 따라 한도가 크게 다름</li><li><strong>DSR 계산</strong>: 기존 대출 포함 DSR 40% 이내 여부 사전 확인</li><li><strong>신용점수 점검</strong>: 최소 700점 이상이면 우대 금리 적용 가능</li><li><strong>다수 은행 사전 심사</strong>: 최소 3개 은행 사전 심사 후 가장 낮은 금리 선택</li><li><strong>중도상환수수료 확인</strong>: 3년 이내 상환 계획 있다면 수수료 낮은 상품 선택</li></ol>"),
            ("변동금리 vs 고정금리 선택 기준", "<table><thead><tr><th>구분</th><th>변동금리</th><th>혼합형</th><th>고정금리</th></tr></thead><tbody><tr><td>초기 금리</td><td>낮음</td><td>중간</td><td>높음</td></tr><tr><td>금리 인하 수혜</td><td>즉시 적용</td><td>5년 후 적용</td><td>없음</td></tr><tr><td>금리 인상 위험</td><td>높음</td><td>5년간 없음</td><td>없음</td></tr><tr><td>추천 상황</td><td>금리 하락 예상 or 단기 보유</td><td>중장기 안정 원하는 경우</td><td>장기 보유 + 금리 인상 우려</td></tr></tbody></table>"),
        ],
        "faq": [
            ("아파트 담보대출 금리가 가장 낮은 은행은 어디인가요?", "개인 신용도와 조건에 따라 다르지만, 일반적으로 <strong>카카오뱅크·케이뱅크 등 인터넷은행이 시중은행보다 0.1~0.3% 낮은 경향</strong>이 있습니다. 다만 조건에 따라 다를 수 있으므로 반드시 여러 은행에서 사전 심사를 받아보세요."),
            ("담보대출 사전 심사가 신용점수에 영향을 주나요?", "은행의 <strong>사전 심사(가심사)는 신용점수에 거의 영향을 주지 않습니다.</strong> 실제 대출 신청(정식 심사) 시에는 소폭 영향이 있을 수 있으나, 단기간에 여러 곳에 동시 신청하지 않는 한 크게 걱정하지 않아도 됩니다."),
            ("주택담보대출 갈아타기(대환)가 유리한가요?", "현재 금리보다 <strong>0.5~1% 이상 낮은 상품</strong>으로 갈아탈 수 있고 중도상환수수료보다 이자 절감액이 크다면 갈아타기를 고려할 수 있습니다. 최근에는 대환 대출 플랫폼을 통해 쉽게 비교할 수 있습니다."),
        ],
        "ctas": [
            {"text": "아파트 담보대출 금리 지금 비교하기", "desc": "금융감독원 금융소비자포털에서 은행별 담보대출 금리를 비교하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "내 조건 맞는 담보대출 한눈에 비교", "desc": "핀크에서 나의 아파트와 소득에 맞는 최저 금리를 찾아보세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "담보대출 무료 상담 받기", "desc": "토스에서 아파트 담보대출 한도와 금리를 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 7 =====
    {
        "title": "주택담보대출 중도상환수수료 면제 조건 총정리",
        "cat": 6,
        "slug": "mortgage-early-repayment-fee-guide",
        "intro": "주택담보대출을 중간에 갚으면 <strong>중도상환수수료</strong>가 발생합니다. 대출 잔액의 최대 1.5%에 달하는 이 수수료는 수백만 원에 이를 수 있습니다. 하지만 특정 조건에서는 수수료가 면제되거나 감면됩니다. 2026년 기준 중도상환수수료 계산 방법과 면제·감면 조건을 완벽하게 정리했습니다.",
        "sections": [
            ("중도상환수수료란?", "<p><strong>중도상환수수료</strong>는 대출 만기 이전에 대출금을 일부 또는 전부 상환할 때 금융기관이 부과하는 수수료입니다. 금융기관 입장에서는 예상보다 일찍 상환되면 자금 운용 계획이 틀어지기 때문에 이를 보전하는 목적입니다.</p><p><strong>계산식:</strong> 중도상환수수료 = 중도상환금액 × 수수료율 × (잔여 기간 ÷ 의무 기간)</p><p><strong>예시:</strong> 1억원 대출, 수수료율 1.2%, 잔여 기간 18개월, 의무 기간 36개월<br>→ 1억 × 1.2% × (18/36) = <strong>60만원</strong></p>"),
            ("은행별 주담대 중도상환수수료율 비교 (2026년)", "<table><thead><tr><th>은행</th><th>변동금리</th><th>혼합형</th><th>고정금리</th><th>의무 기간</th></tr></thead><tbody><tr><td>국민은행</td><td>0.6%</td><td>1.2%</td><td>1.4%</td><td>3년</td></tr><tr><td>신한은행</td><td>0.6%</td><td>1.2%</td><td>1.4%</td><td>3년</td></tr><tr><td>하나은행</td><td>0.7%</td><td>1.2%</td><td>1.5%</td><td>3년</td></tr><tr><td>우리은행</td><td>0.6%</td><td>1.2%</td><td>1.4%</td><td>3년</td></tr><tr><td>농협은행</td><td>0.7%</td><td>1.2%</td><td>1.5%</td><td>3년</td></tr><tr><td>카카오뱅크</td><td>0.5%</td><td>1.0%</td><td>1.2%</td><td>3년</td></tr><tr><td>케이뱅크</td><td>0.5%</td><td>1.0%</td><td>1.2%</td><td>3년</td></tr></tbody></table>"),
            ("중도상환수수료 면제 조건 6가지", "<ol><li><strong>의무 기간(3년) 경과 후 상환</strong>: 대출 실행일로부터 3년이 지나면 수수료 없이 자유 상환 가능</li><li><strong>연간 10% 이내 부분 상환</strong>: 많은 은행이 매년 대출 잔액의 10% 이내 부분 상환에 대해 수수료 면제 (은행별 상이)</li><li><strong>금리 인상 시 상환</strong>: 변동금리 대출에서 금리가 오르면 30일 이내 수수료 없이 해지 가능 (은행별 상이)</li><li><strong>사망·실직 등 불가피한 사유</strong>: 차주 사망, 실직, 폐업 등 불가피한 사유 시 면제 (증빙 필요)</li><li><strong>대환 대출 인프라 이용</strong>: 금융위원회 대환 플랫폼을 통한 갈아타기 시 수수료 면제 (2025년부터 확대)</li><li><strong>정책 대출(디딤돌·버팀목)</strong>: 수수료율 적용 방식이 다름 (3년 경과 후 무료)</li></ol>"),
            ("중도상환수수료 절약 전략", "<ul><li><strong>연간 면제 한도 활용</strong>: 매년 대출 잔액의 10% 범위 내에서 수수료 없이 상환</li><li><strong>3년 이후 집중 상환</strong>: 여유 자금이 생겼다면 3년 의무 기간이 지난 후 한 번에 상환</li><li><strong>갈아타기 전 수수료 계산</strong>: 대환 시 수수료 금액보다 금리 절감 효과가 큰지 꼭 계산</li><li><strong>여유 자금 파킹</strong>: 마이너스통장이나 CMA에 예치하면서 3년을 기다리는 방법도 있음</li></ul>"),
            ("대환 대출 시 중도상환수수료 절감법", "<p>2024년부터 확대된 <strong>대환 대출 인프라(플랫폼 대환)</strong>를 활용하면 기존 주담대를 낮은 금리 상품으로 쉽게 갈아탈 수 있습니다.</p><ul><li>참여 기관: 시중은행, 인터넷은행, 저축은행 등</li><li>중도상환수수료: 플랫폼 경유 시 면제 or 감면 혜택 (기관별 상이)</li><li>신청 방법: 각 은행 앱 또는 대환 대출 전용 플랫폼 이용</li></ul><p><strong>주의:</strong> 면제 혜택은 상품·시기에 따라 달라질 수 있으므로 신청 전 반드시 확인하세요.</p>"),
        ],
        "faq": [
            ("중도상환수수료는 언제부터 없어지나요?", "대부분의 은행에서 <strong>대출 실행일로부터 3년이 지나면 중도상환수수료가 없습니다.</strong> 3년 미만이라도 연간 10% 이내 부분 상환은 면제되는 경우가 많습니다."),
            ("일부 상환도 수수료가 발생하나요?", "네, 일부 상환도 수수료 부과 대상입니다. 다만 <strong>연간 10% 이내의 부분 상환은 수수료 면제</strong>하는 은행이 많으므로 약관을 확인하세요."),
            ("대환 대출로 갈아타면 수수료 면제인가요?", "금융당국 대환 대출 플랫폼을 이용하면 수수료 면제 혜택이 있는 경우가 있습니다. 단, <strong>상품마다 다르므로 신청 전 반드시 해당 은행에 확인</strong>하세요."),
        ],
        "ctas": [
            {"text": "중도상환수수료 계산 바로 해보기", "desc": "금융감독원 포털에서 수수료 계산기를 활용해보세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "낮은 금리로 담보대출 갈아타기", "desc": "핀크에서 대환 대출 상품을 비교하고 이자를 아껴보세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "대환 대출 무료 상담 받기", "desc": "토스에서 현재 대출보다 유리한 상품으로 갈아타는 방법을 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 8 =====
    {
        "title": "보금자리론 조건 한도 신청 방법 2026 완벽 가이드",
        "cat": 6,
        "slug": "bogeumjari-loan-guide-2026",
        "intro": "<strong>보금자리론</strong>은 한국주택금융공사(HF)에서 운영하는 대표적인 장기 고정금리 주택담보대출입니다. 소득 제한이 없고(일부 예외), 장기 고정금리로 이자 부담을 안정적으로 관리할 수 있어 내 집 마련에 나선 많은 분들이 선택합니다. 2026년 최신 조건, 금리, 한도를 완벽하게 정리했습니다.",
        "sections": [
            ("보금자리론이란?", "<p><strong>보금자리론</strong>은 한국주택금융공사(HF)가 공급하는 <strong>장기 고정금리 분할상환 주택담보대출</strong>입니다. 시중은행의 변동금리 주담대와 달리 금리 변동 위험 없이 대출 기간 내내 동일한 금리를 적용받습니다.</p><ul><li>운영 기관: 한국주택금융공사(HF)</li><li>취급 은행: 국민·우리·기업·농협·신한·하나·부산·대구 등</li><li>특징: 장기 고정금리, 중도상환수수료 없음(유동화형)</li></ul>"),
            ("2026년 보금자리론 자격 조건", "<table><thead><tr><th>구분</th><th>일반 보금자리론</th><th>우대형(특례보금자리)</th></tr></thead><tbody><tr><td>무주택 여부</td><td>무주택 or 1주택(처분 조건)</td><td>무주택자</td></tr><tr><td>소득 기준</td><td>9억원 초과 주택 시 연 7,000만원 이하</td><td>부부합산 6,000만원 이하</td></tr><tr><td>주택 가격</td><td>9억원 이하</td><td>6억원 이하</td></tr><tr><td>전용면적</td><td>제한 없음</td><td>85㎡ 이하</td></tr><tr><td>LTV 한도</td><td>최대 70%</td><td>최대 70~80%</td></tr></tbody></table>"),
            ("2026년 보금자리론 금리 (고정금리)", "<table><thead><tr><th>상환 기간</th><th>일반</th><th>신혼가구 우대</th><th>다자녀 우대</th></tr></thead><tbody><tr><td>10년</td><td>연 3.65%</td><td>연 3.35%</td><td>연 3.05%</td></tr><tr><td>15년</td><td>연 3.75%</td><td>연 3.45%</td><td>연 3.15%</td></tr><tr><td>20년</td><td>연 3.85%</td><td>연 3.55%</td><td>연 3.25%</td></tr><tr><td>30년</td><td>연 3.95%</td><td>연 3.65%</td><td>연 3.35%</td></tr><tr><td>40년</td><td>연 4.05%</td><td>연 3.75%</td><td>연 3.45%</td></tr><tr><td>50년</td><td>연 4.15%</td><td>연 3.85%</td><td>연 3.55%</td></tr></tbody></table><p>신혼가구(혼인 7년 이내) 0.3%, 2자녀 이상 가구 최대 0.6% 우대 금리 적용</p>"),
            ("대출 한도 및 상환 방식", "<ul><li><strong>대출 한도</strong>: 최대 3억 6,000만원 (주택 가격의 70% 이내)</li><li><strong>상환 방식</strong>: 원리금균등상환, 원금균등상환, 체증식 상환</li><li><strong>대출 기간</strong>: 10·15·20·30·40·50년 (최장 50년)</li><li><strong>중도상환수수료</strong>: 없음 (유동화 MBS 형 기준)</li></ul><h3>월 상환액 예시 (3억원 대출, 30년 원리금균등, 금리 3.95%)</h3><p>월 상환액: 약 <strong>142만원</strong> (원리금 합산)</p>"),
            ("신청 방법 및 서류", "<ol><li><strong>온라인 사전 상담</strong>: HF 홈페이지(hf.go.kr) 또는 협약 은행 앱</li><li><strong>주택 매매계약 체결</strong></li><li><strong>협약 은행 방문 or 비대면 신청</strong></li><li><strong>서류 제출</strong>: 주민등록등본, 소득 증빙, 매매계약서, 등기부등본</li><li><strong>HF 보증서 발급</strong></li><li><strong>잔금일 대출 실행</strong></li></ol>"),
            ("보금자리론 vs 시중은행 주담대 선택 기준", "<table><thead><tr><th>구분</th><th>보금자리론</th><th>시중은행 주담대</th></tr></thead><tbody><tr><td>금리 유형</td><td>완전 고정</td><td>변동·혼합·고정 선택</td></tr><tr><td>초기 금리</td><td>다소 높을 수 있음</td><td>변동 기준 초기 낮음</td></tr><tr><td>금리 안정성</td><td>매우 높음</td><td>변동 시 불안정</td></tr><tr><td>중도상환수수료</td><td>없음</td><td>3년간 0.6~1.5%</td></tr><tr><td>소득 제한</td><td>일부 있음</td><td>없음</td></tr><tr><td>추천 대상</td><td>장기 거주 + 안정 원하는 경우</td><td>단기 거주 or 금리 하락 예상 시</td></tr></tbody></table>"),
        ],
        "faq": [
            ("보금자리론과 디딤돌 대출 중 어느 것이 유리한가요?", "소득 요건이 맞다면 <strong>디딤돌 대출의 금리가 더 낮습니다.</strong> 디딤돌은 소득 기준(부부 합산 6,000~7,000만원)이 있고 한도도 낮으므로, 소득이 높거나 대출 한도가 더 필요하면 보금자리론을 선택하세요."),
            ("보금자리론은 소득 제한이 없나요?", "주택 가격 9억원 이하 주택은 소득 제한이 없습니다. 다만 <strong>9억원 초과 주택은 부부 합산 연소득 7,000만원 이하</strong> 조건이 있습니다."),
            ("보금자리론으로 신축 아파트 분양도 가능한가요?", "네, 분양권 취득 후 <strong>잔금 지급 시점에 보금자리론 신청</strong>이 가능합니다. 다만 분양가가 9억원을 넘으면 조건이 달라집니다."),
            ("50년 만기 보금자리론을 선택하면 이자 총액이 너무 많지 않나요?", "네, 만기가 길수록 이자 총액은 늘어납니다. 3억원 대출, 30년 vs 50년 비교 시 이자 총액 차이가 약 5,000만원 이상 납니다. 단, <strong>월 상환 부담을 줄이고 싶은 경우</strong> 50년을 선택한 뒤 중도상환(수수료 없음)을 적극 활용하는 전략이 유효합니다."),
        ],
        "ctas": [
            {"text": "보금자리론 자격 지금 확인하기", "desc": "한국주택금융공사 홈페이지에서 보금자리론 가능 여부를 확인하세요", "url": "https://www.hf.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "보금자리론 vs 시중은행 금리 비교", "desc": "핀크에서 보금자리론과 은행 주담대 금리를 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "보금자리론 무료 상담 신청", "desc": "토스에서 나의 상황에 맞는 주택 대출 방법을 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 9 =====
    {
        "title": "전세자금대출 연장 조건 절차 주의사항 완벽 정리",
        "cat": 6,
        "slug": "jeonse-loan-renewal-guide",
        "intro": "전세 계약 만료가 다가오면 전세자금대출도 함께 연장해야 합니다. 그냥 두면 대출이 자동 연장될 것 같지만, <strong>대출 연장은 별도 신청이 필요</strong>하고 조건이 변경될 수도 있습니다. 전세 계약 만료 시점에 꼭 알아야 할 대출 연장 절차, 조건 변경 사항, 주의사항을 완벽하게 정리했습니다.",
        "sections": [
            ("전세자금대출 연장이란?", "<p>전세자금대출은 대개 <strong>2년 만기</strong>로 설정되며, 전세 계약 기간과 연동됩니다. 계약이 갱신되면 대출도 갱신(연장)해야 하는데, 이 과정에서 금리, 한도, 보증 조건 등이 변경될 수 있습니다.</p><ul><li>연장 신청 시기: 만기 <strong>1~3개월 전</strong> (은행별 상이)</li><li>연장 방식: 계약 연장형 or 신규 대출 재실행</li><li>금리 재산정: 연장 시점 기준 금리로 재적용</li></ul>"),
            ("전세대출 연장 절차 단계별 정리", "<ol><li><strong>전세 계약 갱신 결정</strong>: 임대인과 협의 후 계약 갱신 확정</li><li><strong>은행 연장 신청</strong>: 만기 1개월 전까지 해당 은행에 연장 신청</li><li><strong>갱신 계약서 제출</strong>: 갱신 전세 계약서 사본 제출 (공인중개사 확인 권장)</li><li><strong>보증 갱신</strong>: HUG·HF 보증 갱신 신청 (보증서 기간도 함께 연장)</li><li><strong>연장 심사 및 승인</strong>: 소득·신용·보증 조건 재심사</li><li><strong>연장 완료</strong>: 새로운 금리 및 조건 확인 후 대출 연장 완료</li></ol>"),
            ("연장 시 주요 변경 사항", "<table><thead><tr><th>항목</th><th>최초 대출 시</th><th>연장 시</th></tr></thead><tbody><tr><td>금리</td><td>가입 당시 시장 금리</td><td>연장 시점 금리로 재산정</td></tr><tr><td>한도</td><td>보증금 기준 산정</td><td>보증금 변동 시 한도 조정 가능</td></tr><tr><td>보증 기간</td><td>2년</td><td>2년 재연장 (조건 재확인)</td></tr><tr><td>소득 심사</td><td>있음</td><td>있음 (변경 없어도 재확인)</td></tr><tr><td>주택 조건</td><td>확인</td><td>보증금 80% 초과 시 문제 가능</td></tr></tbody></table>"),
            ("연장 거절 사유 및 대처법", "<h3>연장 거절 주요 사유</h3><ul><li>신용점수 하락</li><li>소득 감소 또는 직장 변경</li><li>대상 주택 담보 가치 하락 (깡통 우려)</li><li>보증 기관 조건 미충족</li></ul><h3>대처 방법</h3><ul><li>타 은행으로 전세대출 이전 신청</li><li>보증금 일부 반환 협의 후 재계약</li><li>버팀목 전세대출로 전환 검토 (조건 충족 시)</li></ul>"),
            ("전세대출 연장 시 보증금 인상 처리", "<p>전세 갱신 시 보증금이 오른 경우 <strong>증액분에 대해 추가 대출이 필요</strong>합니다.</p><ul><li>기존 대출 연장 + 증액분 추가 대출: 동일 은행에서 처리 가능한 경우</li><li>한도 초과 시: 타 은행 상품 검토 or 보증금 인상 거절 협의</li><li>증액 한도: 전세 보증금의 80% 이내 (버팀목 기준)</li></ul><p><strong>주의:</strong> 임대차 3법(계약갱신요구권)에 따라 2년 추가 갱신 시 임대인은 보증금을 5% 이상 올릴 수 없습니다.</p>"),
            ("전세대출 연장 시 꿀팁", "<ul><li><strong>만기 2개월 전에 미리 움직이기</strong>: 심사·보증 발급에 시간이 걸리므로 여유 있게 준비</li><li><strong>금리 비교 후 은행 변경 검토</strong>: 연장 시점에 타 은행 금리가 낮다면 이전도 고려</li><li><strong>전자계약 활용</strong>: 갱신 계약도 전자계약 시 금리 우대 적용 가능</li><li><strong>보증 보험 갱신 누락 주의</strong>: 대출만 연장하고 보증보험 갱신을 잊으면 보호받지 못함</li></ul>"),
        ],
        "faq": [
            ("전세대출 연장 신청을 안 하면 어떻게 되나요?", "만기일에 대출이 자동으로 상환 처리되어 <strong>보증금 반환에 차질이 생길 수 있습니다.</strong> 반드시 만기 1개월 전에 연장 신청을 하세요."),
            ("전세 계약 갱신을 안 하고 이사하면 대출은?", "<strong>이사 예정일 전에 새 주소지 전세대출을 신청</strong>하고, 기존 대출은 이사 당일 보증금으로 상환합니다. 새 전세지에서 다시 대출을 받는 구조입니다."),
            ("버팀목 전세대출도 연장이 가능한가요?", "네, 버팀목 전세대출도 최초 2년 + <strong>최대 4회(총 10년) 연장</strong>이 가능합니다. 단, 연장 시마다 소득·자격 조건 재확인이 필요합니다."),
            ("연장 시 금리가 올랐다면 어떻게 해야 하나요?", "연장 시 금리는 시장 금리를 반영합니다. 금리가 많이 올랐다면 <strong>버팀목·청년 버팀목 등 정책 대출로 전환</strong>하거나, 대출 비교 플랫폼으로 더 낮은 금리 상품을 찾아보세요."),
        ],
        "ctas": [
            {"text": "전세대출 연장 조건 미리 확인하기", "desc": "주택도시기금 홈페이지에서 전세대출 연장 자격을 확인하세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "더 낮은 금리로 전세대출 갈아타기", "desc": "핀크에서 전세대출 금리를 비교하고 유리한 상품으로 이전하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "전세 연장 무료 대출 상담", "desc": "토스에서 전세 갱신 시 대출 연장 방법을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 10 =====
    {
        "title": "신혼부부 전세자금대출 조건 금리 한도 2026",
        "cat": 6,
        "slug": "newlywed-jeonse-loan-2026",
        "intro": "결혼 후 첫 보금자리를 마련할 때 가장 먼저 알아봐야 하는 것이 <strong>신혼부부 전세자금대출</strong>입니다. 일반 전세대출보다 낮은 금리와 높은 한도를 제공하는 정책 상품들이 있습니다. 2026년 기준 신혼부부가 이용할 수 있는 전세자금대출 종류, 조건, 금리, 한도를 한눈에 비교 정리했습니다.",
        "sections": [
            ("신혼부부 전세대출 종류 한눈에 비교", "<table><thead><tr><th>상품명</th><th>운영 기관</th><th>금리</th><th>최대 한도</th><th>소득 기준</th></tr></thead><tbody><tr><td>신혼부부 버팀목</td><td>주택도시기금</td><td>연 1.5~2.4%</td><td>수도권 2.2억</td><td>합산 6,000만원</td></tr><tr><td>청년 버팀목</td><td>주택도시기금</td><td>연 1.5~2.1%</td><td>수도권 1.2억</td><td>단독 5,000만원</td></tr><tr><td>신혼부부 전용 시중대출</td><td>각 은행</td><td>연 3.5~5.0%</td><td>LTV 이내</td><td>심사 기준</td></tr><tr><td>카카오뱅크 전세대출</td><td>카카오뱅크</td><td>연 3.4~4.8%</td><td>5억원</td><td>심사 기준</td></tr></tbody></table>"),
            ("신혼부부 버팀목 전세대출 상세 조건", "<h3>자격 요건</h3><ul><li>혼인 신고일로부터 <strong>7년 이내</strong> (예비 신혼부부 포함)</li><li>부부 합산 <strong>연소득 6,000만원 이하</strong></li><li>순자산 <strong>3.61억원 이하</strong></li><li>무주택 세대주</li><li>대상 주택: 전용 <strong>85㎡ 이하</strong>, 보증금 수도권 4억/비수도권 3억 이하</li></ul><h3>우대 금리 조건</h3><ul><li>자녀 1명: 연 0.3% 추가 인하</li><li>자녀 2명 이상: 연 0.5% 추가 인하</li><li>다문화 가구: 연 0.2% 추가 인하</li><li>전자계약: 연 0.1% 추가 인하</li></ul>"),
            ("신혼부부 전세대출 소득 구간별 금리", "<table><thead><tr><th>합산 연소득</th><th>기본 금리</th><th>자녀 1명</th><th>자녀 2명 이상</th></tr></thead><tbody><tr><td>2,000만원 이하</td><td>연 1.5%</td><td>연 1.2%</td><td>연 1.0%</td></tr><tr><td>2,000~4,000만원</td><td>연 1.8%</td><td>연 1.5%</td><td>연 1.3%</td></tr><tr><td>4,000~6,000만원</td><td>연 2.4%</td><td>연 2.1%</td><td>연 1.9%</td></tr></tbody></table>"),
            ("신혼부부 주택구입 대출과 병행 전략", "<p>신혼부부는 전세 대신 바로 주택 구입을 선택할 수도 있습니다. 이 경우 <strong>신혼가구 디딤돌 대출</strong>이 가장 유리합니다.</p><ul><li>소득 기준: 부부 합산 <strong>7,500만원 이하</strong></li><li>금리: 연 2.15~3.00% (자녀 수에 따라 우대)</li><li>LTV: 최대 <strong>80%</strong></li><li>한도: 최대 <strong>3억원</strong></li><li>특징: 2자녀 이상 시 최저 금리 + 한도 우대</li></ul>"),
            ("신혼부부 주거 지원 제도 총정리", "<table><thead><tr><th>제도</th><th>지원 내용</th><th>신청 기관</th></tr></thead><tbody><tr><td>신혼부부 버팀목</td><td>저금리 전세대출</td><td>주택도시기금</td></tr><tr><td>신혼가구 디딤돌</td><td>저금리 구입대출</td><td>주택도시기금</td></tr><tr><td>신혼부부 특별공급</td><td>청약 우선 배정</td><td>한국부동산원</td></tr><tr><td>신생아 특례대출</td><td>출산 후 저금리 구입·전세</td><td>주택도시기금</td></tr><tr><td>주거급여</td><td>임차료 일부 지원</td><td>한국토지주택공사</td></tr></tbody></table>"),
            ("신혼부부 전세대출 신청 시 주의사항", "<ul><li><strong>예비 신혼부부 신청</strong>: 결혼 전이라도 계약일로부터 <strong>3개월 이내 혼인 예정</strong>이면 신청 가능. 실행 전까지 혼인신고 완료 필요</li><li><strong>만 34세 이하라면 청년 버팀목</strong>이 신혼 버팀목보다 조건이 유리할 수 있음 (소득 기준: 개인 5,000만원)</li><li><strong>신생아 특례대출</strong>: 2023년 1월 이후 출생아 부모라면 전세 최대 3억원, 연 1.1~3.0% 특례 금리 이용 가능</li></ul>"),
        ],
        "faq": [
            ("결혼 전에 신혼부부 전세대출 신청이 가능한가요?", "네, <strong>예비 신혼부부도 신청 가능</strong>합니다. 단, 대출 실행 전까지 혼인신고를 완료해야 하며, 계약일로부터 3개월 이내에 혼인 예정이어야 합니다."),
            ("신혼부부 버팀목과 청년 버팀목을 동시에 받을 수 없나요?", "<strong>중복 수혜는 불가</strong>합니다. 두 상품 중 조건과 혜택을 비교해 더 유리한 것을 선택하세요. 일반적으로 만 34세 이하이고 단독 소득 5,000만원 이하라면 청년 버팀목이 유리할 수 있습니다."),
            ("신생아 특례대출 요건은 어떻게 되나요?", "2023년 1월 1일 이후 출생아가 있고, <strong>부부 합산 연소득 1억 3,000만원 이하</strong>이면 전세 최대 3억원(연 1.1~3.0%), 구입 최대 5억원(연 1.6~3.3%) 대출이 가능합니다."),
            ("신혼부부 버팀목 대출로 오피스텔도 가능한가요?", "주거용 오피스텔도 가능합니다. 단, <strong>건축물대장상 주거용으로 등재</strong>된 경우에 한하며, 전용면적과 보증금 기준을 충족해야 합니다."),
        ],
        "ctas": [
            {"text": "신혼부부 전세대출 자격 확인하기", "desc": "주택도시기금 공식 홈페이지에서 신혼부부 대출 자격을 확인하세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "신혼부부 대출 금리 한눈에 비교", "desc": "핀크에서 신혼부부에게 유리한 전세·구입 대출을 비교해보세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "신혼부부 주거 지원 무료 상담", "desc": "토스에서 신혼부부 맞춤 대출 상품을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 11 =====
    {
        "title": "임차보증금 반환 보증 가입 방법 HUG vs HF 비교",
        "cat": 6,
        "slug": "jeonse-deposit-guarantee-hug-hf-compare",
        "intro": "전세 보증금을 지키는 가장 확실한 방법은 <strong>전세보증보험(임차보증금 반환 보증)</strong>에 가입하는 것입니다. 집주인이 보증금을 돌려주지 못할 경우 보증 기관이 대신 지급해주는 상품으로, HUG와 HF 두 기관에서 운영합니다. 두 상품의 차이를 정확히 이해하고 본인에게 맞는 상품을 선택하세요.",
        "sections": [
            ("전세보증보험이란?", "<p><strong>전세보증보험(임차보증금 반환 보증)</strong>은 전세 계약 만료 시 집주인이 보증금을 반환하지 못할 경우, 보증 기관이 임차인에게 보증금을 대신 지급하고 이후 집주인에게 구상권을 행사하는 상품입니다.</p><ul><li>보증 기관: HUG(주택도시보증공사), HF(한국주택금융공사)</li><li>보험료: 보증금의 연 0.1~0.4% 수준</li><li>혜택: 집주인이 돌려주지 못해도 100% 보장</li></ul>"),
            ("HUG vs HF 전세보증보험 비교", "<table><thead><tr><th>구분</th><th>HUG 전세보증보험</th><th>HF 전세금안심대출보증</th></tr></thead><tbody><tr><td>운영 기관</td><td>주택도시보증공사(HUG)</td><td>한국주택금융공사(HF)</td></tr><tr><td>보증 대상</td><td>전세 보증금 반환 보증</td><td>전세자금대출 연계 보증</td></tr><tr><td>보증금 한도</td><td>수도권 7억, 비수도권 5억</td><td>수도권 5억, 비수도권 4억</td></tr><tr><td>연 보증료</td><td>약 0.128~0.154%</td><td>약 0.102%</td></tr><tr><td>가입 가능 시기</td><td>계약 기간 1/2 이전</td><td>전세대출 실행 시</td></tr><tr><td>단독 가입</td><td>가능</td><td>전세대출 연계만 가능</td></tr><tr><td>적용 대상</td><td>전세 임차인 누구나</td><td>전세자금대출 이용자</td></tr></tbody></table>"),
            ("HUG 전세보증보험 가입 방법", "<ol><li><strong>자격 확인</strong>: HUG 홈페이지(khug.or.kr) 또는 은행 앱에서 가입 가능 여부 확인</li><li><strong>신청 경로</strong>: HUG 직접 신청 or 카카오뱅크·국민은행·우리은행 등 협약 은행 앱</li><li><strong>필요 서류</strong>: 전세 계약서, 주민등록등본, 확정일자 부여 확인</li><li><strong>보증료 납부</strong>: 보증금 × 보증료율 = 납부액 (예: 3억 × 0.128% = 38.4만원/년)</li><li><strong>보증서 수령</strong></li></ol>"),
            ("전세보증보험 거절 사유 및 대처법", "<h3>가입 거절되는 주요 경우</h3><ul><li>선순위 근저당 + 보증금 합계가 시세의 100% 초과 (깡통전세)</li><li>집주인의 세금 체납 사실 확인</li><li>다세대·빌라 등 일부 주택 유형 제한</li><li>공시가격의 150% 초과 보증금</li></ul><h3>대처 방법</h3><ul><li>보증금을 낮춰 재계약 협의</li><li>임대인의 근저당 일부 상환 요청</li><li>SGI서울보증 전세금보장신용보험 검토</li></ul>"),
            ("전세보증보험 보증료 계산 예시", "<table><thead><tr><th>보증금</th><th>HUG 보증료(년)</th><th>HF 보증료(년)</th><th>2년 총 비용</th></tr></thead><tbody><tr><td>1억원</td><td>약 12.8만원</td><td>약 10.2만원</td><td>HUG 25.6 / HF 20.4만원</td></tr><tr><td>2억원</td><td>약 25.6만원</td><td>약 20.4만원</td><td>HUG 51.2 / HF 40.8만원</td></tr><tr><td>3억원</td><td>약 38.4만원</td><td>약 30.6만원</td><td>HUG 76.8 / HF 61.2만원</td></tr><tr><td>5억원</td><td>약 64만원</td><td>약 51만원</td><td>HUG 128 / HF 102만원</td></tr></tbody></table>"),
            ("전세 보증금 지키는 체크리스트", "<ol><li><strong>계약 전</strong>: 등기부등본 선순위 근저당 확인 + 집주인 세금 체납 조회</li><li><strong>계약 당일</strong>: 전입신고 + 확정일자 즉시 취득</li><li><strong>계약 후 1달 이내</strong>: 전세보증보험 가입 (기간의 절반 전)</li><li><strong>만기 3개월 전</strong>: 갱신 or 이사 결정 + 보증 갱신 준비</li></ol>"),
        ],
        "faq": [
            ("빌라·다세대도 전세보증보험 가입이 되나요?", "가능합니다. 단, <strong>선순위 근저당과 보증금 합계가 시세의 100% 이내</strong>여야 하며, 주택 가격 산정 기준에 따라 가입이 거절될 수 있습니다. 아파트보다 제한이 많습니다."),
            ("HUG 보증보험을 이미 가입했는데 집주인이 바뀌면 어떻게 되나요?", "집주인이 변경(양도)되면 새 집주인에게 의무가 이전됩니다. <strong>HUG 보증은 임차인 보호 목적이므로 집주인 변경과 무관하게 유지</strong>됩니다. 단, 새 계약서 작성 시 보증 갱신이 필요합니다."),
            ("전세보증보험 가입 후 이사하면 보증은 어떻게 되나요?", "계약 기간 내 이사하는 경우 <strong>보증 해지 및 잔여 보증료 일부 환급</strong>이 가능합니다. 이사 전 HUG 또는 HF에 해지 신청을 하세요."),
        ],
        "ctas": [
            {"text": "전세보증보험 가입 자격 지금 확인", "desc": "금융감독원 포털에서 전세보증보험 조건을 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "HUG 전세보증보험 바로 가입하기", "desc": "핀크에서 간편하게 전세보증보험 가입을 신청해보세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "전세 계약 전 무료 보증 상담", "desc": "토스에서 전세 보증금 보호 방법을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 12 =====
    {
        "title": "오피스텔 담보대출 조건 LTV 은행별 비교 2026",
        "cat": 6,
        "slug": "officetel-mortgage-loan-2026",
        "intro": "오피스텔은 주택과 업무시설의 성격을 동시에 가지고 있어 담보대출 조건이 아파트와 다릅니다. <strong>LTV 제한, 용도 구분, 금리</strong> 등이 복잡하게 얽혀 있어 제대로 알지 못하면 불이익을 받기 쉽습니다. 2026년 기준 오피스텔 담보대출의 모든 것을 정리했습니다.",
        "sections": [
            ("오피스텔 담보대출 vs 아파트 담보대출 차이", "<table><thead><tr><th>구분</th><th>아파트 담보대출</th><th>오피스텔 담보대출</th></tr></thead><tbody><tr><td>LTV 한도</td><td>최대 60~80%</td><td>최대 50~70%</td></tr><tr><td>담보 인정 방식</td><td>실거래가·KB시세</td><td>감정가 기준</td></tr><tr><td>금리</td><td>상대적으로 낮음</td><td>0.3~0.5% 높은 경우 多</td></tr><tr><td>DTI/DSR 적용</td><td>동일 적용</td><td>동일 적용</td></tr><tr><td>주거용/업무용</td><td>주거용</td><td>용도에 따라 조건 상이</td></tr></tbody></table>"),
            ("주거용 vs 업무용 오피스텔 대출 차이", "<h3>주거용 오피스텔</h3><ul><li>전입신고 및 실거주 목적</li><li>LTV: 최대 <strong>60~70%</strong> 적용 가능 (지역별 상이)</li><li>주택 수 포함: 양도세·종부세 산정 시 주택 수에 포함될 수 있음</li></ul><h3>업무용 오피스텔</h3><ul><li>사업자 또는 임대 목적</li><li>LTV: 최대 <strong>50~60%</strong></li><li>주택 수 미포함: 주택담보대출 규제에서 제외되는 경우</li></ul>"),
            ("2026년 은행별 오피스텔 담보대출 조건", "<table><thead><tr><th>은행</th><th>금리</th><th>LTV 한도</th><th>최소 면적</th><th>특징</th></tr></thead><tbody><tr><td>국민은행</td><td>연 4.2~6.0%</td><td>최대 60%</td><td>없음</td><td>주거용 우선</td></tr><tr><td>신한은행</td><td>연 4.1~5.9%</td><td>최대 60%</td><td>없음</td><td>비대면 신청</td></tr><tr><td>하나은행</td><td>연 4.2~6.0%</td><td>최대 60%</td><td>없음</td><td>감정가 기준</td></tr><tr><td>우리은행</td><td>연 4.3~6.1%</td><td>최대 60%</td><td>없음</td><td>WON뱅킹</td></tr><tr><td>농협은행</td><td>연 4.4~6.2%</td><td>최대 55%</td><td>없음</td><td>농촌 지역 취약</td></tr><tr><td>카카오뱅크</td><td>연 4.0~5.8%</td><td>최대 70%</td><td>없음</td><td>100% 비대면</td></tr></tbody></table>"),
            ("오피스텔 담보대출 주의사항", "<ul><li><strong>소형 오피스텔(10~20㎡ 미만)</strong>: 담보 인정 거부 또는 LTV 대폭 축소하는 은행 있음</li><li><strong>분양 오피스텔 담보대출</strong>: 준공 전 분양권은 담보 인정 어려움. 잔금 시 대출 신청</li><li><strong>임대 중 오피스텔</strong>: 임차인 보증금이 선순위로 차감되어 실제 대출 한도 감소</li><li><strong>감정가 이슈</strong>: 실거래가보다 낮은 감정가가 나올 경우 대출 한도 예상보다 작을 수 있음</li></ul>"),
            ("오피스텔 담보대출 절차", "<ol><li>오피스텔 소유 확인 (등기부등본)</li><li>은행 방문 또는 온라인 신청</li><li>감정평가 의뢰 (은행 지정 감정사)</li><li>LTV·DSR 심사</li><li>대출 승인 및 근저당 설정</li><li>대출금 지급</li></ol><p><strong>감정 비용</strong>은 차주가 부담하며, 보통 <strong>20~50만원</strong> 수준입니다.</p>"),
            ("오피스텔 투자 시 활용 전략", "<ul><li><strong>매매 후 임대 수익</strong>: 임대 수익으로 이자 충당이 가능한지 계산 필수 (연 수익률 > 대출 금리)</li><li><strong>공실 위험 고려</strong>: 공실 시에도 이자를 납부해야 하므로 유동 자금 확보 필수</li><li><strong>주택 수 영향</strong>: 주거용 오피스텔은 주택 수에 포함될 수 있어 다주택자 취득세·종부세 부담 확인</li></ul>"),
        ],
        "faq": [
            ("오피스텔도 전세자금대출 가능한가요?", "주거용으로 등재된 오피스텔은 버팀목 등 전세자금대출 가능합니다. 단, <strong>건축물대장 용도 확인</strong>이 필수입니다."),
            ("소형 오피스텔(12㎡)도 담보대출이 가능한가요?", "일부 은행은 소형 오피스텔에 대해 담보 인정을 거부하거나 LTV를 크게 낮춥니다. <strong>최소 20㎡ 이상</strong>이어야 대부분의 은행에서 담보 인정이 됩니다."),
            ("오피스텔 대출과 아파트 대출 한도가 합산되나요?", "DSR 규제는 모든 대출을 합산하여 적용합니다. 따라서 <strong>오피스텔 대출도 DSR 계산에 포함</strong>되므로 기존 주택담보대출이 있다면 추가 한도가 제한됩니다."),
        ],
        "ctas": [
            {"text": "오피스텔 담보대출 한도 계산해보기", "desc": "금융감독원 포털에서 오피스텔 담보대출 가능 금액을 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "오피스텔 대출 금리 비교하기", "desc": "핀크에서 오피스텔 담보대출 금리를 한눈에 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "오피스텔 대출 무료 상담 신청", "desc": "토스에서 오피스텔 담보대출 조건을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 13 =====
    {
        "title": "마이너스 통장 개설 조건 금리 한도 은행별 비교 2026",
        "cat": 6,
        "slug": "minus-account-conditions-2026",
        "intro": "<strong>마이너스 통장(한도대출)</strong>은 한도 내에서 자유롭게 빌리고 갚을 수 있는 가장 유연한 신용대출 상품입니다. 급여 이체 은행에서 한도를 설정해두고 필요할 때만 쓰면 되므로 직장인 비상 자금 관리에 최적입니다. 2026년 기준 은행별 금리, 한도, 개설 조건을 상세히 비교했습니다.",
        "sections": [
            ("마이너스 통장이란?", "<p><strong>마이너스 통장(한도대출)</strong>은 은행이 승인한 한도 범위 내에서 잔액이 마이너스가 되어도 출금이 가능한 구조의 신용대출입니다. 실제로 사용한 금액에 대해서만 이자가 발생하므로, 한도를 설정해두고 필요할 때 사용하는 방식이 일반적입니다.</p><ul><li>이자: 실제 사용 금액에 대해서만 발생 (일할 계산)</li><li>상환: 언제든 자유롭게 상환 가능</li><li>만기: 보통 1년 (매년 갱신 심사)</li></ul>"),
            ("마이너스 통장 자격 조건", "<h3>일반적인 개설 조건</h3><ul><li><strong>재직 기간</strong>: 현 직장 3개월~1년 이상 (은행별 상이)</li><li><strong>소득</strong>: 연소득 2,000만원 이상 (근로·사업 소득)</li><li><strong>신용점수</strong>: NICE 기준 700점 이상 (은행별 최저 기준 상이)</li><li><strong>통장 실적</strong>: 급여 이체 통장으로 3개월 이상 사용 시 우대</li></ul><h3>우대 조건</h3><ul><li>급여 이체 6개월 이상: 한도·금리 우대</li><li>공과금·카드 자동납부: 추가 우대</li><li>예·적금 보유: 추가 한도</li></ul>"),
            ("2026년 은행별 마이너스 통장 비교", "<table><thead><tr><th>은행</th><th>금리</th><th>최대 한도</th><th>특징</th></tr></thead><tbody><tr><td>국민은행</td><td>연 4.5~7.5%</td><td>3억원</td><td>KB스타뱅킹 비대면</td></tr><tr><td>신한은행</td><td>연 4.3~7.3%</td><td>2억원</td><td>쏠편한 마이너스</td></tr><tr><td>하나은행</td><td>연 4.4~7.4%</td><td>2억원</td><td>하나원큐 앱</td></tr><tr><td>우리은행</td><td>연 4.5~7.5%</td><td>2억원</td><td>WON통장대출</td></tr><tr><td>농협은행</td><td>연 4.6~7.6%</td><td>1억원</td><td>NH올원뱅크</td></tr><tr><td>카카오뱅크</td><td>연 4.1~7.0%</td><td>1억 5,000만원</td><td>완전 비대면·즉시 개설</td></tr><tr><td>토스뱅크</td><td>연 3.9~6.5%</td><td>3,000만원</td><td>신용대출 기반 비교 우위</td></tr><tr><td>케이뱅크</td><td>연 4.0~6.8%</td><td>2억원</td><td>비대면 간편 개설</td></tr></tbody></table>"),
            ("마이너스 통장 활용법 및 주의사항", "<h3>현명한 활용법</h3><ul><li><strong>비상금 용도</strong>: 한도만 설정하고 쓰지 않으면 이자가 없음. 예비 자금으로 활용</li><li><strong>단기 자금 조달</strong>: 급여 지급 전 일시적 자금 필요 시 단기 활용 후 즉시 상환</li><li><strong>이자 최소화</strong>: 사용 후 여유 자금 생기면 즉시 상환 → 일할 계산으로 이자 절감</li></ul><h3>주의사항</h3><ul><li><strong>DSR 포함</strong>: 마이너스 통장 한도 전체(사용 여부 무관)가 DSR 계산에 포함될 수 있음</li><li><strong>매년 갱신 필요</strong>: 만기 1년마다 갱신 심사 → 직장 변경·소득 감소 시 한도 축소 가능</li><li><strong>한도 방치 위험</strong>: 사용하지 않더라도 DSR 한도를 잡아먹으므로 불필요하면 해지</li></ul>"),
            ("마이너스 통장 이자 계산 방법", "<p><strong>계산식:</strong> 이자 = 사용 금액 × (연이율 ÷ 365) × 사용 일수</p><p><strong>예시:</strong> 1,000만원을 금리 5%로 30일 사용 시<br>1,000만원 × (5% ÷ 365) × 30 = 약 <strong>41,096원</strong></p><p>일반 신용대출과 달리 <strong>원금 상환 시 즉시 이자가 줄어드는 구조</strong>이므로, 여유 자금은 즉시 상환하는 습관이 중요합니다.</p>"),
        ],
        "faq": [
            ("마이너스 통장 한도를 설정해두면 이자가 계속 나가나요?", "아니요, <strong>실제로 사용한 금액에 대해서만 이자가 발생</strong>합니다. 한도를 설정해두고 사용하지 않으면 이자는 0원입니다."),
            ("마이너스 통장이 DSR 계산에 포함되면 주담대 한도가 줄어드나요?", "네, <strong>마이너스 통장 한도 일부(또는 전부)가 DSR에 포함</strong>될 수 있습니다. 주담대 신청 전에 마이너스 통장 한도를 축소하거나 해지하면 주담대 한도를 늘릴 수 있습니다."),
            ("직장이 없어도 마이너스 통장을 개설할 수 있나요?", "직장인이 아닌 경우 개설이 어렵습니다. 사업자라면 <strong>사업소득 증빙 후 개설 가능</strong>하지만, 조건이 더 까다롭고 한도가 낮을 수 있습니다."),
        ],
        "ctas": [
            {"text": "마이너스 통장 금리 한눈에 비교", "desc": "금융감독원 포털에서 은행별 한도대출 금리를 비교하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "내 조건에 맞는 마이너스 통장 찾기", "desc": "핀크에서 내 신용점수와 소득에 맞는 한도대출을 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "마이너스 통장 무료 한도 조회", "desc": "토스에서 지금 바로 마이너스 통장 한도를 조회해보세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 14 =====
    {
        "title": "비상금 대출 한도 금리 조건 앱별 비교 2026",
        "cat": 6,
        "slug": "emergency-loan-app-comparison-2026",
        "intro": "갑작스러운 지출이 생겼을 때 은행 방문 없이 스마트폰 하나로 <strong>당일 소액 대출</strong>을 받을 수 있는 비상금 대출이 인기입니다. 카카오뱅크, 토스, 케이뱅크 등 주요 앱의 비상금 대출 한도, 금리, 조건을 2026년 기준으로 꼼꼼히 비교했습니다.",
        "sections": [
            ("비상금 대출이란?", "<p><strong>비상금 대출</strong>은 소액(50~300만원)을 별도 서류 없이 앱 하나로 즉시 받을 수 있는 초단기 신용대출입니다. 심사가 간단하고 실행 속도가 빠른 것이 특징입니다.</p><ul><li>한도: 50만원 ~ 300만원 (앱별 상이)</li><li>금리: 연 2~8% 수준</li><li>심사 방식: 신용점수 기반 자동 심사</li><li>실행 시간: 신청 후 수분 내 즉시 지급</li></ul>"),
            ("2026년 주요 앱 비상금 대출 비교", "<table><thead><tr><th>앱</th><th>최대 한도</th><th>금리</th><th>상환 기간</th><th>특징</th></tr></thead><tbody><tr><td>카카오뱅크 비상금대출</td><td>300만원</td><td>연 2.04~15%</td><td>만기일시(1년)</td><td>신용점수 낮아도 가능, 24시간</td></tr><tr><td>토스 비상금대출</td><td>300만원</td><td>연 연 4~15%</td><td>만기일시(1년)</td><td>토스 신용점수 연동</td></tr><tr><td>케이뱅크 소액대출</td><td>200만원</td><td>연 3~12%</td><td>만기일시(6개월)</td><td>업비트 연동 시 우대</td></tr><tr><td>네이버페이 비상금</td><td>200만원</td><td>연 4~15%</td><td>만기일시</td><td>네이버 활동 점수 반영</td></tr><tr><td>페이코 소액대출</td><td>100만원</td><td>연 5~20%</td><td>만기일시</td><td>페이코 사용 실적 반영</td></tr></tbody></table>"),
            ("카카오뱅크 비상금대출 상세", "<ul><li><strong>한도</strong>: 최대 300만원</li><li><strong>금리</strong>: 신용점수에 따라 연 2.04~15% (평균 약 4~6%)</li><li><strong>조건</strong>: 만 19세 이상, 별도 재직 증명 불필요</li><li><strong>상환</strong>: 1년 만기 일시상환 (중도상환 자유)</li><li><strong>특징</strong>: 신용점수 낮은 분도 일부 이용 가능, 24시간 신청 가능</li></ul>"),
            ("비상금 대출 이용 시 주의사항", "<ul><li><strong>고금리 주의</strong>: 신용점수가 낮으면 최고 20% 가까운 금리 적용 가능 → 단기 이용 후 즉시 상환 필수</li><li><strong>DSR 포함</strong>: 비상금 대출도 DSR에 포함될 수 있어 주담대 등 큰 대출 전 해지 권장</li><li><strong>중복 대출 지양</strong>: 여러 앱에서 동시에 받으면 신용점수 하락 + 이자 부담 가중</li><li><strong>1금융권 우선</strong>: 카카오뱅크·케이뱅크 등 은행권 상품이 저축은행·캐피탈 상품보다 금리가 낮음</li></ul>"),
            ("비상금 마련 현명한 방법 5가지", "<ol><li><strong>CMA 통장 활용</strong>: 50~100만원을 CMA에 예치해두면 즉시 출금 가능한 비상금 역할</li><li><strong>마이너스 통장 한도만 설정</strong>: 사용하지 않으면 이자 0, 비상시만 활용</li><li><strong>청년희망적금·청년도약계좌</strong>: 만기 수령 후 비상금 재원으로 활용</li><li><strong>비상금 전용 자동이체</strong>: 매달 5~10만원씩 별도 계좌에 자동저축</li><li><strong>주거래 은행 한도 조회</strong>: 급여 이체 은행에서 미리 한도대출 신청 (이자 0, 비상시 사용)</li></ol>"),
        ],
        "faq": [
            ("신용점수가 낮아도 비상금 대출이 가능한가요?", "카카오뱅크 비상금대출은 신용점수가 낮더라도 일부 승인되는 경우가 있습니다. 단, <strong>신용점수가 낮을수록 금리가 높아지므로</strong> 단기 사용 후 빨리 상환하는 것이 중요합니다."),
            ("비상금 대출과 카드론 중 어느 것이 유리한가요?", "금리 측면에서는 <strong>비상금 대출(은행권)이 카드론보다 낮은 경우가 많습니다.</strong> 카드론은 편리하지만 신용점수에 부정적 영향이 더 클 수 있으므로, 은행 비상금 대출을 먼저 시도하세요."),
            ("비상금 대출을 여러 앱에서 동시에 받아도 되나요?", "가능은 하지만 <strong>동시에 여러 곳에서 대출을 받으면 신용점수가 하락</strong>하고 DSR 부담도 늘어납니다. 꼭 필요한 금액만 한 곳에서 받는 것을 권장합니다."),
        ],
        "ctas": [
            {"text": "비상금 대출 금리 지금 비교하기", "desc": "금융감독원 포털에서 소액 신용대출 금리를 비교해보세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "비상금 대출 한도 조회하기", "desc": "핀크에서 내 신용점수로 받을 수 있는 비상금 대출 한도를 확인하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "토스 비상금 대출 지금 신청하기", "desc": "토스에서 24시간 즉시 비상금 대출을 받아보세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 15 =====
    {
        "title": "직장인 신용대출 한도 높이는 방법 7가지 실전 가이드",
        "cat": 6,
        "slug": "employee-credit-loan-limit-tips",
        "intro": "같은 직장인이라도 신용대출 한도가 사람마다 크게 다릅니다. <strong>신용점수, 소득, 직장 조건, 거래 이력</strong>에 따라 한도가 수천만 원까지 차이가 납니다. 대출 신청 전 한도를 최대한 높일 수 있는 실전 방법 7가지를 구체적으로 정리했습니다.",
        "sections": [
            ("신용대출 한도를 결정하는 요소들", "<p>은행은 신용대출 한도를 결정할 때 여러 요소를 종합적으로 평가합니다.</p><table><thead><tr><th>평가 요소</th><th>영향도</th><th>개선 가능 여부</th></tr></thead><tbody><tr><td>신용점수</td><td>매우 높음</td><td>가능</td></tr><tr><td>연소득</td><td>매우 높음</td><td>제한적</td></tr><tr><td>재직 기간</td><td>높음</td><td>시간 필요</td></tr><tr><td>직장 규모·안정성</td><td>높음</td><td>제한적</td></tr><tr><td>금융 거래 이력</td><td>중간</td><td>가능</td></tr><tr><td>기존 대출 현황</td><td>높음</td><td>가능</td></tr><tr><td>DSR 여유</td><td>높음</td><td>가능</td></tr></tbody></table>"),
            ("한도 높이는 방법 7가지", "<h3>1. 신용점수 올리기</h3><p>신용점수가 50~100점 오르면 한도가 크게 달라집니다. 체크카드 꾸준히 사용, 연체 없는 신용카드 관리, 공과금 자동이체 등으로 점수를 높이세요.</p><h3>2. 급여 이체 은행에 신청</h3><p>급여가 들어오는 주거래 은행에 신청 시 <strong>소득 증빙이 자동으로 이루어지고 우대 금리·한도</strong>를 받을 수 있습니다.</p><h3>3. 불필요한 대출 정리</h3><p>마이너스 통장, 소액 신용대출 등을 정리하면 DSR 여유가 생겨 신용대출 한도가 늘어납니다. 특히 마이너스 통장 한도(미사용 포함)가 DSR에 반영됩니다.</p><h3>4. 소득 증빙 극대화</h3><p>기본급 외에 상여금, 부업 소득, 배우자 소득 합산 신청이 가능한지 확인하세요. <strong>소득이 높을수록 DSR 여유가 늘어</strong> 한도가 증가합니다.</p><h3>5. 재직 증명서 최신화</h3><p>재직 기간이 길수록, 직장 규모가 클수록 한도가 높습니다. 중소기업보다 <strong>대기업·공기업·공무원</strong>이 같은 소득에서도 한도가 높은 경향이 있습니다.</p><h3>6. 여러 은행 동시 조회 (사전 심사)</h3><p>최소 3~5개 은행에서 사전 심사(가심사)를 받아 한도를 비교하세요. 사전 심사는 신용점수에 거의 영향을 주지 않습니다.</p><h3>7. 대출 신청 타이밍</h3><p>연말정산 후 소득이 확인되는 <strong>2~3월, 성과급 수령 후</strong>에 신청하면 소득 증빙이 유리합니다.</p>"),
            ("은행별 직장인 신용대출 한도 비교 (2026년)", "<table><thead><tr><th>은행</th><th>최대 한도</th><th>금리</th><th>우대 조건</th></tr></thead><tbody><tr><td>국민은행</td><td>연소득 × 200~300%</td><td>연 4.5~8%</td><td>KB급여이체 우대</td></tr><tr><td>신한은행</td><td>연소득 × 200~300%</td><td>연 4.3~7.8%</td><td>신한 급여이체</td></tr><tr><td>하나은행</td><td>연소득 × 200~300%</td><td>연 4.4~7.9%</td><td>하나원큐 비대면</td></tr><tr><td>카카오뱅크</td><td>최대 1억 5,000만원</td><td>연 4.0~8%</td><td>비대면 0.1% 우대</td></tr><tr><td>토스뱅크</td><td>최대 1억원</td><td>연 3.9~9%</td><td>토스 신용점수 연동</td></tr></tbody></table>"),
            ("신용대출 한도 계산 예시", "<p><strong>사례: 연소득 4,000만원, 신용점수 800점, 기존 대출 없음</strong></p><ul><li>DSR 40% 적용 시 연간 원리금 최대: 1,600만원</li><li>금리 5%, 5년 분할상환 기준 → 약 6,900만원</li><li>신용점수 800점 기준 한도 승인: 약 7,000~8,000만원 수준</li></ul><p><strong>사례: 동일 조건, 마이너스 통장 3,000만원 기존 보유</strong></p><ul><li>마이너스 통장 연간 원리금(추정치) 반영 후 DSR 여유 감소</li><li>신용대출 한도: 약 5,000~6,000만원으로 축소</li></ul>"),
            ("신용대출 신청 전 체크리스트", "<ol><li>신용점수 최근 확인 (NICE·KCB 모두)</li><li>기존 대출 현황 파악 및 정리 가능 여부 검토</li><li>연소득 증빙 자료 준비 (원천징수영수증, 건강보험료 납부 확인서)</li><li>주거래 은행 우대 조건 충족 여부 확인</li><li>3개 이상 은행 사전 심사 후 최저 금리·최고 한도 선택</li></ol>"),
        ],
        "faq": [
            ("신용대출 여러 곳에 동시에 신청하면 신용점수가 떨어지나요?", "단기간에 여러 곳에 대출 신청(정식 심사)을 하면 조회 이력이 쌓여 신용점수에 영향을 줄 수 있습니다. 다만 <strong>사전 심사(가심사)는 영향이 매우 미미</strong>하므로 사전 심사로 비교 후 1~2곳에만 정식 신청하세요."),
            ("재직 기간이 짧으면 신용대출이 안 되나요?", "일부 은행은 재직 3개월 이상이면 신청 가능하지만, 재직 기간이 짧을수록 한도가 낮아집니다. <strong>인터넷은행(카카오뱅크·케이뱅크)이 재직 기간 요건이 더 유연</strong>한 편입니다."),
            ("공무원·교사는 신용대출 한도가 더 높나요?", "네, <strong>직업 안정성이 높은 공무원·교사·공기업 직원</strong>은 같은 소득이라도 은행에서 한도를 높게 책정하는 경향이 있습니다."),
        ],
        "ctas": [
            {"text": "내 신용대출 한도 지금 조회하기", "desc": "금융감독원 포털에서 나의 대출 가능 금액을 확인해보세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "신용대출 금리 한눈에 비교하기", "desc": "핀크에서 내 조건에 맞는 최저 금리 신용대출을 찾아보세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "신용대출 무료 한도 조회 및 상담", "desc": "토스에서 신용대출 한도와 금리를 즉시 확인해보세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 16 =====
    {
        "title": "카카오뱅크 신용대출 조건 금리 한도 2026 총정리",
        "cat": 6,
        "slug": "kakaobank-credit-loan-2026",
        "intro": "<strong>카카오뱅크 신용대출</strong>은 100% 비대면으로 신청 가능하고, 당일 심사·당일 지급이 가능하여 직장인들에게 큰 인기를 얻고 있습니다. 2026년 기준 카카오뱅크 신용대출의 종류, 조건, 금리, 한도, 신청 방법을 완벽하게 정리했습니다.",
        "sections": [
            ("카카오뱅크 신용대출 종류", "<table><thead><tr><th>상품</th><th>대상</th><th>최대 한도</th><th>금리</th></tr></thead><tbody><tr><td>직장인 신용대출</td><td>직장인(재직 3개월+)</td><td>1억 5,000만원</td><td>연 3.8~9%</td></tr><tr><td>비상금 대출</td><td>만 19세 이상 누구나</td><td>300만원</td><td>연 2.04~15%</td></tr><tr><td>마이너스통장</td><td>직장인</td><td>1억 5,000만원</td><td>연 4.1~7%</td></tr><tr><td>주택담보대출</td><td>아파트 소유자</td><td>LTV 이내</td><td>연 3.6~5%</td></tr></tbody></table>"),
            ("카카오뱅크 직장인 신용대출 조건", "<h3>자격 요건</h3><ul><li>현 직장 재직 <strong>3개월 이상</strong></li><li>연소득 <strong>2,000만원 이상</strong></li><li>신용점수 NICE <strong>700점 이상</strong> (또는 KCB 기준)</li><li>만 19세 이상 내국인</li></ul><h3>유리한 조건</h3><ul><li>공무원·대기업·금융권 재직 시 한도 우대</li><li>카카오뱅크 급여이체 설정 시 금리 우대</li><li>카카오뱅크 체크카드 3개월 이상 사용 시 우대</li></ul>"),
            ("2026년 카카오뱅크 신용대출 금리 상세", "<table><thead><tr><th>신용점수 구간</th><th>금리 범위</th><th>비고</th></tr></thead><tbody><tr><td>950점 이상</td><td>연 3.8~4.5%</td><td>최우대 금리</td></tr><tr><td>900~950점</td><td>연 4.5~5.5%</td><td>우대 금리</td></tr><tr><td>850~900점</td><td>연 5.5~6.5%</td><td>일반 금리</td></tr><tr><td>800~850점</td><td>연 6.5~7.5%</td><td>일반 금리</td></tr><tr><td>700~800점</td><td>연 7.5~9%</td><td>심사 후 결정</td></tr></tbody></table><p>실제 적용 금리는 소득·재직 기간·직장 종류에 따라 달라집니다.</p>"),
            ("카카오뱅크 신용대출 신청 방법", "<ol><li>카카오뱅크 앱 실행</li><li>'대출' 메뉴 → '직장인 신용대출' 선택</li><li>금리·한도 사전 조회 (신용점수 영향 없음)</li><li>신청 버튼 클릭 후 본인 인증</li><li>소득 증빙: 건강보험료 납부 확인서 or 원천징수영수증 자동 조회</li><li>심사 후 한도·금리 확정 (보통 수 분~수 시간)</li><li>대출 약정 후 즉시 지급</li></ol>"),
            ("카카오뱅크 신용대출 장단점", "<h3>장점</h3><ul><li>100% 비대면 신청, 24시간 가능</li><li>건강보험료 자동 조회로 서류 간소화</li><li>사전 조회 시 신용점수 불변</li><li>중도상환수수료 없음 (일부 상품)</li></ul><h3>단점</h3><ul><li>신용점수·소득이 낮으면 한도 제한</li><li>대면 상담 불가 (복잡한 상황 처리 어려움)</li><li>신규 사업자·프리랜서 조건 까다로움</li></ul>"),
            ("카카오뱅크 vs 시중은행 신용대출 비교", "<table><thead><tr><th>구분</th><th>카카오뱅크</th><th>국민은행</th><th>신한은행</th></tr></thead><tbody><tr><td>신청 방식</td><td>100% 앱</td><td>앱+방문</td><td>앱+방문</td></tr><tr><td>금리</td><td>연 3.8~9%</td><td>연 4.5~8%</td><td>연 4.3~7.8%</td></tr><tr><td>최대 한도</td><td>1.5억원</td><td>연소득 300%</td><td>연소득 300%</td></tr><tr><td>심사 속도</td><td>수 분~수 시간</td><td>1~3일</td><td>1~3일</td></tr><tr><td>우대 조건</td><td>카카오 거래</td><td>KB 주거래</td><td>신한 주거래</td></tr></tbody></table>"),
        ],
        "faq": [
            ("카카오뱅크 신용대출 한도 1억 5,000만원을 모두 받을 수 있나요?", "최대 한도는 1억 5,000만원이지만, <strong>실제 한도는 신용점수·소득·DSR 조건</strong>에 따라 달라집니다. DSR 40% 규제로 소득 대비 적정 한도가 정해집니다."),
            ("카카오뱅크 신용대출 중도상환이 자유롭나요?", "네, <strong>카카오뱅크 신용대출은 중도상환수수료가 없어</strong> 언제든 자유롭게 상환 가능합니다. 여유 자금 생기면 바로 상환하여 이자를 절감하세요."),
            ("카카오뱅크 신용대출과 마이너스 통장 중 어느 것이 유리한가요?", "일정 금액을 한 번에 사용하고 분할 상환할 계획이라면 <strong>신용대출</strong>이 유리합니다. 필요할 때만 소액씩 사용하고 바로 갚을 계획이라면 <strong>마이너스 통장</strong>이 이자를 절감할 수 있습니다."),
        ],
        "ctas": [
            {"text": "카카오뱅크 대출 한도 지금 조회", "desc": "금융소비자포털에서 카카오뱅크 신용대출 조건을 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "인터넷은행 신용대출 금리 비교", "desc": "핀크에서 카카오·토스·케이뱅크 대출 금리를 한눈에 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "내 조건 최저 금리 대출 찾기", "desc": "토스에서 내 신용점수에 맞는 최저 금리 대출을 조회하세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 17 =====
    {
        "title": "토스뱅크 대출 종류 금리 조건 한도 비교 2026",
        "cat": 6,
        "slug": "tossbank-loan-comparison-2026",
        "intro": "<strong>토스뱅크</strong>는 직관적인 UI와 빠른 심사로 MZ세대에게 특히 인기 있는 인터넷은행입니다. 신용대출부터 주택담보대출까지 다양한 대출 상품을 운영하고 있습니다. 2026년 기준 토스뱅크 대출 상품별 조건, 금리, 한도를 완벽히 정리했습니다.",
        "sections": [
            ("토스뱅크 대출 상품 전체 라인업", "<table><thead><tr><th>상품</th><th>대상</th><th>최대 한도</th><th>금리</th></tr></thead><tbody><tr><td>토스뱅크 신용대출</td><td>직장인·사업자</td><td>1억원</td><td>연 3.9~15%</td></tr><tr><td>비상금대출</td><td>만 19세 이상</td><td>300만원</td><td>연 4~15%</td></tr><tr><td>마이너스통장</td><td>직장인</td><td>3,000만원</td><td>연 3.9~6.5%</td></tr><tr><td>토스뱅크 주담대</td><td>아파트 소유자</td><td>LTV 이내</td><td>연 3.7~5.5%</td></tr><tr><td>사업자 대출</td><td>개인사업자</td><td>2,000만원</td><td>연 5~15%</td></tr></tbody></table>"),
            ("토스뱅크 신용대출 자격 조건", "<ul><li>만 19세 이상 대한민국 국민</li><li>재직 중 직장인 (재직 기간 3개월 이상 권장)</li><li>연소득 2,000만원 이상</li><li>신용점수 NICE 650점 이상 (타 은행보다 낮은 기준 적용)</li></ul><p>토스뱅크는 <strong>신용점수 외에 토스 앱 내 금융 활동 데이터를 추가 평가</strong>에 반영하여, 전통 은행에서 거절된 경우에도 승인되는 사례가 있습니다.</p>"),
            ("토스뱅크 대출 금리 상세 (2026년)", "<table><thead><tr><th>신용점수</th><th>신용대출 금리</th><th>마이너스통장</th></tr></thead><tbody><tr><td>900점 이상</td><td>연 3.9~5.0%</td><td>연 3.9~4.5%</td></tr><tr><td>800~900점</td><td>연 5.0~7.0%</td><td>연 4.5~5.5%</td></tr><tr><td>700~800점</td><td>연 7.0~10%</td><td>연 5.5~6.5%</td></tr><tr><td>650~700점</td><td>연 10~15%</td><td>불가</td></tr></tbody></table>"),
            ("토스뱅크 대출 신청 방법", "<ol><li>토스 앱 → '대출' 메뉴 진입</li><li>'신용대출' 또는 원하는 상품 선택</li><li>한도 조회 (신용점수 영향 없음)</li><li>조건 확인 후 신청</li><li>소득 자동 조회 (건강보험료 연동)</li><li>심사 완료 → 실시간 대출 지급</li></ol>"),
            ("토스뱅크만의 차별화 특징", "<ul><li><strong>대안 신용평가</strong>: 토스 앱 내 소비·저축 패턴을 평가에 반영하여 신용점수가 낮아도 승인 가능성 높음</li><li><strong>금리 인하 요구권</strong>: 대출 후 신용점수가 오르면 금리 인하를 직접 요청 가능</li><li><strong>선착순 금리 혜택</strong>: 특정 기간 이벤트 금리 적용</li><li><strong>실시간 분석</strong>: 내 대출 상환 패턴을 앱에서 실시간 확인 가능</li></ul>"),
            ("토스뱅크 vs 카카오뱅크 vs 케이뱅크 비교", "<table><thead><tr><th>구분</th><th>토스뱅크</th><th>카카오뱅크</th><th>케이뱅크</th></tr></thead><tbody><tr><td>신용대출 최대 한도</td><td>1억원</td><td>1.5억원</td><td>2억원</td></tr><tr><td>신용점수 최저 기준</td><td>650점</td><td>700점</td><td>700점</td></tr><tr><td>대안 신용평가</td><td>있음</td><td>제한적</td><td>없음</td></tr><tr><td>최저 금리</td><td>연 3.9%</td><td>연 3.8%</td><td>연 4.0%</td></tr><tr><td>주담대 여부</td><td>있음</td><td>있음</td><td>있음</td></tr></tbody></table>"),
        ],
        "faq": [
            ("토스뱅크에서 거절당하면 어디서 받을 수 있나요?", "토스뱅크 거절 후에는 <strong>카카오뱅크, 케이뱅크 순</strong>으로 시도해보세요. 그래도 거절된다면 저신용자 전용 정부 대출(햇살론, 사잇돌 등)을 검토하세요."),
            ("토스뱅크 대출 금리 인하 요구는 어떻게 하나요?", "토스 앱 → 대출 → '금리 인하 요구' 메뉴에서 신청 가능합니다. <strong>신용점수 50점 이상 상승, 소득 증가, 직장 변경</strong> 등 사유가 있을 때 신청하면 금리를 낮출 수 있습니다."),
            ("토스뱅크 비상금 대출과 신용대출을 동시에 보유할 수 있나요?", "원칙적으로 가능하지만, <strong>DSR 합산 적용</strong>으로 총 한도가 제한됩니다. 비상금 대출 상환 후 신용대출을 받거나 신용대출을 먼저 받는 것을 추천합니다."),
        ],
        "ctas": [
            {"text": "토스뱅크 대출 한도 즉시 조회", "desc": "금융소비자포털에서 토스뱅크 대출 조건을 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "3개 인터넷은행 대출 금리 한눈에 비교", "desc": "핀크에서 토스·카카오·케이뱅크 대출 금리를 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "토스에서 바로 대출 한도 조회하기", "desc": "토스 앱에서 내 조건의 최저 금리와 최대 한도를 확인하세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 18 =====
    {
        "title": "케이뱅크 신용대출 조건 금리 특징 2026 완벽 분석",
        "cat": 6,
        "slug": "kbank-credit-loan-analysis-2026",
        "intro": "<strong>케이뱅크</strong>는 국내 최초 인터넷전문은행으로, 업비트 연동 혜택과 높은 신용대출 한도(최대 2억원)로 차별화된 경쟁력을 갖추고 있습니다. 2026년 기준 케이뱅크 신용대출의 모든 조건, 금리, 한도, 특징을 분석했습니다.",
        "sections": [
            ("케이뱅크 대출 상품 라인업", "<table><thead><tr><th>상품</th><th>대상</th><th>최대 한도</th><th>금리</th></tr></thead><tbody><tr><td>아파트담보대출</td><td>아파트 소유자</td><td>LTV 이내</td><td>연 3.65~5.05%</td></tr><tr><td>직장인신용대출(플러스)</td><td>직장인</td><td>2억원</td><td>연 4.0~8%</td></tr><tr><td>소액신용대출</td><td>누구나</td><td>200만원</td><td>연 3~12%</td></tr><tr><td>마이너스통장</td><td>직장인</td><td>2억원</td><td>연 4.0~6.8%</td></tr><tr><td>파킹통장 연계대출</td><td>케이뱅크 파킹통장 보유자</td><td>잔액 120%</td><td>연 낮음</td></tr></tbody></table>"),
            ("케이뱅크 신용대출 조건 및 금리", "<h3>자격 요건</h3><ul><li>만 19세 이상 국내 거주자</li><li>현 직장 재직 3개월 이상</li><li>연소득 2,000만원 이상</li><li>신용점수 700점 이상 (NICE 기준)</li></ul><h3>금리 구간 (2026년 기준)</h3><table><thead><tr><th>신용점수</th><th>금리 범위</th></tr></thead><tbody><tr><td>950점 이상</td><td>연 4.0~4.8%</td></tr><tr><td>900~950점</td><td>연 4.8~5.8%</td></tr><tr><td>800~900점</td><td>연 5.8~7.0%</td></tr><tr><td>700~800점</td><td>연 7.0~8.0%</td></tr></tbody></table>"),
            ("케이뱅크 업비트 연동 혜택", "<p>케이뱅크는 암호화폐 거래소 <strong>업비트(Upbit)와 공식 파트너십</strong>을 맺고 있어, 업비트 계정 연동 시 추가 혜택을 제공합니다.</p><ul><li>업비트 잔고 연계: 신용도 추가 반영 (심사 가점)</li><li>케이뱅크 파킹통장: 업비트 입출금 계좌로 활용, 연 2.3% 이자 (2026 기준)</li><li>업비트 원화 예치금 이자: 케이뱅크 연동 시 수익</li></ul>"),
            ("케이뱅크 아파트 담보대출 특징", "<ul><li><strong>100% 비대면 신청</strong>: 방문 없이 앱으로 완결</li><li><strong>감정평가 비용</strong>: 케이뱅크 부담 (고객 부담 없음)</li><li><strong>LTV</strong>: 최대 70% (지역별 상이)</li><li><strong>금리</strong>: 연 3.65~5.05% (시중은행 대비 경쟁력)</li><li><strong>중도상환수수료</strong>: 3년 이내 0.5~1.2%</li></ul>"),
            ("케이뱅크 대출 신청 방법", "<ol><li>케이뱅크 앱 설치 및 계좌 개설</li><li>'대출' 탭 → 원하는 상품 선택</li><li>한도·금리 사전 조회</li><li>신청 후 소득 자동 조회</li><li>심사 완료 → 즉시 지급</li></ol>"),
            ("케이뱅크 장단점 분석", "<h3>장점</h3><ul><li>신용대출 한도 최대 2억원 (인터넷은행 중 최대)</li><li>아파트 담보대출 비대면 + 감정 비용 없음</li><li>업비트 연동으로 추가 혜택</li><li>파킹통장 고금리</li></ul><h3>단점</h3><ul><li>카카오뱅크·토스뱅크 대비 브랜드 인지도 낮음</li><li>신용점수 기준 700점으로 다소 높음</li><li>사업자 대출 상품 제한적</li></ul>"),
        ],
        "faq": [
            ("케이뱅크 신용대출 2억원은 누구나 받을 수 있나요?", "2억원은 최대 한도이며, <strong>실제로는 DSR 40% 규제와 신용점수·소득에 따라 한도가 결정</strong>됩니다. 연소득이 높고 신용점수가 900점 이상이어야 근접한 한도를 받을 수 있습니다."),
            ("케이뱅크 파킹통장 잔고로 대출이 가능한가요?", "직접 담보 대출은 아니지만 <strong>파킹통장 잔고가 신용 심사에 긍정적 영향</strong>을 줄 수 있습니다."),
            ("케이뱅크와 카카오뱅크 중 어느 쪽이 대출 한도가 높나요?", "최대 한도 기준으로는 <strong>케이뱅크(2억원)가 카카오뱅크(1.5억원)보다 높습니다.</strong> 단, 실제 승인 한도는 개인 조건에 따라 다르므로 두 곳 모두에서 사전 조회해보는 것을 권장합니다."),
        ],
        "ctas": [
            {"text": "케이뱅크 대출 한도 사전 조회하기", "desc": "금융소비자포털에서 케이뱅크 대출 상품을 비교하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "인터넷은행 대출 최저 금리 찾기", "desc": "핀크에서 케이뱅크·카카오·토스 대출 금리를 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "내 최저 금리 대출 바로 찾기", "desc": "토스에서 나의 조건에 맞는 가장 유리한 대출을 찾아보세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 19 =====
    {
        "title": "신용점수 올리는 방법 10가지 대출 전 필수 체크",
        "cat": 6,
        "slug": "credit-score-improvement-tips",
        "intro": "대출 금리와 한도를 결정짓는 가장 중요한 요소가 바로 <strong>신용점수</strong>입니다. 신용점수 50점 차이가 대출 금리를 1% 이상 바꿀 수 있으며, 수천만 원의 이자 차이로 이어집니다. 대출 신청 전 신용점수를 높이는 실전적인 방법 10가지를 정리했습니다.",
        "sections": [
            ("신용점수 구조 이해하기", "<p>한국의 신용점수는 <strong>NICE평가정보</strong>와 <strong>KCB(코리아크레딧뷰로)</strong> 두 기관이 산정합니다.</p><table><thead><tr><th>평가 항목</th><th>NICE 비중</th><th>KCB 비중</th></tr></thead><tbody><tr><td>상환 이력</td><td>37%</td><td>35%</td></tr><tr><td>부채 수준</td><td>27%</td><td>25%</td></tr><tr><td>신용 거래 기간</td><td>15%</td><td>20%</td></tr><tr><td>신용 형태</td><td>13%</td><td>10%</td></tr><tr><td>신규 신용 조회</td><td>8%</td><td>10%</td></tr></tbody></table>"),
            ("신용점수 올리는 방법 10가지", "<h3>1. 연체 이력 해소</h3><p>가장 큰 영향: 연체된 금액이 있다면 즉시 납부하세요. 완납 후 신용점수가 빠르게 회복됩니다.</p><h3>2. 체크카드 꾸준히 사용</h3><p>월 30만원 이상 6개월 이상 사용 → 금융 거래 이력 형성</p><h3>3. 신용카드 연체 없이 관리</h3><p>매월 전액 결제 or 최소 결제 기한 내 납부 필수</p><h3>4. 통신요금·공과금 자동이체</h3><p>본인 명의 계좌에서 납부 시 성실 납부 이력으로 반영</p><h3>5. 국민연금·건강보험 납부 이력 등록</h3><p>납부 확인서를 신용평가사에 직접 제출하면 가점 적용</p><h3>6. 불필요한 마이너스통장·소액대출 정리</h3><p>미사용 한도도 부채 수준에 반영 → 해지 시 점수 상승</p><h3>7. 카드론·현금서비스 지양</h3><p>신용점수에 부정적 영향 큰 항목</p><h3>8. 오래된 신용카드 유지</h3><p>신용 거래 기간이 길수록 점수에 유리 → 오래된 카드 해지 주의</p><h3>9. 단기간 다수 신규 대출 조회 피하기</h3><p>단기에 여러 곳 정식 심사 신청 시 점수 하락</p><h3>10. 신용점수 무료 관리 앱 활용</h3><p>카카오뱅크·토스·나이스지키미 등에서 정기 조회 + 개선 팁 확인</p>"),
            ("신용점수 등급별 대출 금리 차이", "<table><thead><tr><th>NICE 점수</th><th>시중은행 신용대출 금리</th><th>월 이자(1억 기준)</th></tr></thead><tbody><tr><td>950점 이상</td><td>연 4.0~4.5%</td><td>약 33~37.5만원</td></tr><tr><td>900~950점</td><td>연 4.5~5.5%</td><td>약 37.5~45.8만원</td></tr><tr><td>850~900점</td><td>연 5.5~6.5%</td><td>약 45.8~54.2만원</td></tr><tr><td>800~850점</td><td>연 6.5~8.0%</td><td>약 54.2~66.7만원</td></tr><tr><td>700~800점</td><td>연 8.0~12%</td><td>약 66.7~100만원</td></tr></tbody></table><p>점수 100점 차이가 월 이자를 <strong>수십만 원</strong> 차이나게 만들 수 있습니다.</p>"),
            ("신용점수 올리는 기간 예상", "<table><thead><tr><th>방법</th><th>효과 발생 시기</th><th>점수 상승 예상</th></tr></thead><tbody><tr><td>연체금 완납</td><td>완납 후 1~3개월</td><td>20~100점</td></tr><tr><td>체크카드 6개월 사용</td><td>3~6개월</td><td>10~30점</td></tr><tr><td>마이너스통장 해지</td><td>즉시~1개월</td><td>5~20점</td></tr><tr><td>공과금 납부 이력 등록</td><td>즉시~2개월</td><td>5~15점</td></tr></tbody></table>"),
            ("신용점수 무료 조회 방법", "<ul><li><strong>카카오뱅크</strong>: 앱 → 내 신용점수 (NICE, KCB 무료)</li><li><strong>토스</strong>: 앱 → 신용점수 (KCB 무료)</li><li><strong>뱅크샐러드</strong>: NICE·KCB 모두 무료 조회</li><li><strong>나이스지키미</strong>(www.nicecheckup.com): NICE 공식 무료 조회</li><li><strong>올크레딧</strong>(www.allcredit.co.kr): KCB 공식 무료 조회</li></ul>"),
        ],
        "faq": [
            ("신용점수를 올리는 데 가장 빠른 방법은 무엇인가요?", "가장 빠른 방법은 <strong>연체 금액을 즉시 완납하는 것</strong>입니다. 완납 후 1~3개월 내에 점수가 크게 올라갑니다. 연체가 없다면 마이너스통장·소액대출 해지, 공과금 납부 이력 등록이 다음으로 빠릅니다."),
            ("신용점수 조회하면 점수가 떨어지나요?", "<strong>본인이 직접 조회하는 것은 점수에 전혀 영향을 주지 않습니다.</strong> 금융기관이 대출 심사를 위해 조회하는 '하드 인콰이어리'만 영향이 있습니다."),
            ("신용카드를 아예 안 쓰면 신용점수가 올라가나요?", "아니요, 신용카드를 전혀 사용하지 않으면 신용 거래 이력이 없어 점수가 오히려 낮아집니다. <strong>연체 없이 꾸준히 사용하고 제때 갚는 것</strong>이 점수를 높이는 방법입니다."),
        ],
        "ctas": [
            {"text": "내 신용점수 지금 무료 조회하기", "desc": "금융감독원 포털에서 NICE·KCB 신용점수를 무료로 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "신용점수 높이고 낮은 금리 대출받기", "desc": "핀크에서 내 신용점수에 맞는 최저 금리 대출을 찾아보세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "토스에서 신용점수 관리 시작하기", "desc": "토스 앱에서 신용점수 무료 조회 및 개선 팁을 확인하세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 20 =====
    {
        "title": "대출 거절 사유 7가지와 해결 방법 총정리",
        "cat": 6,
        "slug": "loan-rejection-reasons-solutions",
        "intro": "대출을 신청했는데 거절 통보를 받으셨나요? <strong>대출 거절에는 반드시 이유가 있습니다.</strong> 거절 사유를 정확히 파악하고 해결하면 재신청 성공 가능성을 크게 높일 수 있습니다. 가장 흔한 7가지 대출 거절 사유와 각각의 해결 방법을 상세히 정리했습니다.",
        "sections": [
            ("대출 거절 사유 7가지", "<h3>1. 낮은 신용점수</h3><p>은행권 신용대출 기준 일반적으로 NICE 700점 이상이 필요합니다. 700점 미만이면 거절되거나 금리가 크게 높아집니다.</p><h3>2. DSR 초과</h3><p>기존 대출 원리금이 이미 소득의 40%를 넘으면 추가 대출이 제한됩니다.</p><h3>3. 연체 이력</h3><p>최근 1~3년 이내 연체 기록이 있으면 대출 심사에 크게 불리합니다.</p><h3>4. 재직 기간 부족</h3><p>대부분의 은행이 현 직장 3개월~1년 이상 재직을 요구합니다.</p><h3>5. 소득 증빙 불가</h3><p>프리랜서·무직자·단기 일용직은 소득 증빙이 어려워 거절되기 쉽습니다.</p><h3>6. 과다 채무</h3><p>여러 금융사에 다수 대출이 있거나 총 대출 잔액이 과도한 경우 거절됩니다.</p><h3>7. 허위 정보 제출</h3><p>소득·재직·주소 등 허위 정보 제출 시 즉시 거절 및 블랙리스트 등록 위험이 있습니다.</p>"),
            ("거절 사유별 해결 방법", "<table><thead><tr><th>거절 사유</th><th>해결 방법</th><th>소요 기간</th></tr></thead><tbody><tr><td>낮은 신용점수</td><td>연체 해소, 체크카드 사용, 공과금 납부 이력 등록</td><td>3~6개월</td></tr><tr><td>DSR 초과</td><td>기존 대출 상환·정리, 마이너스통장 해지</td><td>즉시~3개월</td></tr><tr><td>연체 이력</td><td>미납금 즉시 완납, 시간 경과 대기</td><td>6개월~2년</td></tr><tr><td>재직 기간 부족</td><td>현 직장 최소 3개월 이상 근무 후 재신청</td><td>3개월</td></tr><tr><td>소득 증빙 불가</td><td>부가세신고서, 매출 증빙, 사업자 등록증 준비</td><td>다음 신고 기간</td></tr><tr><td>과다 채무</td><td>소액 대출부터 순차 상환, 대환 대출 통해 정리</td><td>1~12개월</td></tr></tbody></table>"),
            ("대출 거절 후 재신청 전략", "<ol><li><strong>거절 사유 정확히 파악</strong>: 금융사에 거절 사유 서면 통보 요청 (금융소비자 권리)</li><li><strong>신용조회 보고서 확인</strong>: 나이스지키미·올크레딧에서 상세 조회</li><li><strong>단기간 재신청 지양</strong>: 1~3개월 이내 동일 금융사 재신청은 심사에 불리</li><li><strong>정책 대출 검토</strong>: 은행 거절 시 햇살론·사잇돌 등 정부 보증 대출 신청</li><li><strong>소득 증빙 보완</strong>: 건강보험료·국민연금 납부 확인서 추가 제출</li></ol>"),
            ("대출 거절 후 대안 상품 비교", "<table><thead><tr><th>상품</th><th>대상</th><th>금리</th><th>한도</th></tr></thead><tbody><tr><td>햇살론 15</td><td>저신용·저소득자</td><td>연 15.9% 이하</td><td>700만원</td></tr><tr><td>햇살론 뱅크</td><td>저신용·저소득자</td><td>연 6.5~10.5%</td><td>2,000만원</td></tr><tr><td>사잇돌 대출</td><td>중신용자</td><td>연 5.9~14.9%</td><td>2,000만원</td></tr><tr><td>미소금융</td><td>기초생활수급자 등</td><td>연 4.5% 이하</td><td>2,000만원</td></tr></tbody></table>"),
            ("대출 거절 방지 사전 체크리스트", "<ul><li>신용점수 700점 이상 확인</li><li>DSR 계산: 기존 원리금 합계가 소득의 40% 이내 여부</li><li>연체 이력 없음 확인</li><li>재직 3개월 이상 확인</li><li>소득 증빙 서류 준비 완료</li><li>금융 정보 정확하게 기재</li></ul>"),
        ],
        "faq": [
            ("대출 거절 사유를 금융사에서 알려주지 않아도 되나요?", "금융소비자보호법에 따라 <strong>금융사는 대출 거절 사유를 서면으로 통보할 의무</strong>가 있습니다. 거절 통보를 받으면 사유 공개를 요청하세요."),
            ("대출 거절 후 바로 다른 은행에 신청해도 되나요?", "가능하지만, <strong>단기간에 여러 곳에 신청하면 조회 이력이 쌓여 신용점수에 불리</strong>합니다. 사전 심사(가심사)로 한도를 확인한 후 유리한 1~2곳만 정식 신청하세요."),
            ("연체를 다 갚았는데도 대출이 안 되는 이유는?", "연체를 완납해도 <strong>연체 이력은 일정 기간(최대 5년) 신용정보에 남아</strong> 있습니다. 미납 완납 후에도 6개월~2년은 이력이 남아 영향을 줍니다."),
        ],
        "ctas": [
            {"text": "내 대출 가능 여부 미리 확인하기", "desc": "금융감독원 포털에서 대출 자격을 사전에 체크해보세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "저신용자도 받을 수 있는 대출 찾기", "desc": "핀크에서 내 신용점수에 맞는 대출 상품을 비교해보세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "대출 거절 후 대안 무료 상담", "desc": "토스에서 내 상황에 맞는 대출 대안을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 21 =====
    {
        "title": "100만원 급전 대출 당일 받는 방법 비교 가이드",
        "cat": 6,
        "slug": "1million-emergency-loan-same-day",
        "intro": "갑작스러운 의료비, 차량 수리비, 경조사비 등으로 <strong>100만원 급전</strong>이 필요할 때, 빠르게 받을 수 있는 방법이 무엇인지 많은 분들이 고민합니다. 당일 실행 가능한 소액 급전 대출 방법을 안전한 순서대로 비교 정리했습니다.",
        "sections": [
            ("급전 대출 안전 순위 (1금융권 우선)", "<p>급전이 필요할 때는 <strong>금리가 낮은 상품부터 순서대로 시도</strong>하는 것이 중요합니다. 성급하게 고금리 상품을 이용하면 이자 부담이 눈덩이처럼 커질 수 있습니다.</p><table><thead><tr><th>우선순위</th><th>상품</th><th>금리</th><th>한도</th><th>속도</th></tr></thead><tbody><tr><td>1순위</td><td>마이너스통장(기보유)</td><td>연 4~7%</td><td>설정 한도</td><td>즉시</td></tr><tr><td>2순위</td><td>카카오/토스 비상금 대출</td><td>연 2~15%</td><td>300만원</td><td>수 분</td></tr><tr><td>3순위</td><td>신용카드 할부</td><td>연 5~20%</td><td>카드 한도</td><td>즉시</td></tr><tr><td>4순위</td><td>저축은행 소액대출</td><td>연 10~20%</td><td>100~500만원</td><td>당일</td></tr><tr><td>5순위</td><td>카드론</td><td>연 10~20%</td><td>카드 한도 이내</td><td>당일</td></tr><tr><td>6순위</td><td>캐피탈 소액대출</td><td>연 15~25%</td><td>500만원 이내</td><td>당일</td></tr></tbody></table>"),
            ("당일 100만원 받는 방법 단계별", "<h3>STEP 1: 기존 마이너스 통장 확인</h3><p>이미 마이너스 통장이 있다면 <strong>즉시 출금</strong>이 가능합니다. 가장 빠르고 금리도 낮습니다.</p><h3>STEP 2: 카카오뱅크 비상금 대출</h3><p>앱 → 비상금 대출 → 3분 이내 심사 → 즉시 지급. 최대 300만원, 연 2~15% 금리.</p><h3>STEP 3: 토스 비상금 대출</h3><p>토스 앱 → 비상금 → 신청 → 즉시 지급. 최대 300만원.</p><h3>STEP 4: 저축은행 앱 대출</h3><p>OK저축은행, SBI저축은행 앱 → 소액 신용대출 → 당일 심사·지급.</p>"),
            ("주요 급전 대출 앱 비교 (2026년)", "<table><thead><tr><th>앱</th><th>최대 한도</th><th>금리</th><th>속도</th><th>신용점수 기준</th></tr></thead><tbody><tr><td>카카오뱅크 비상금</td><td>300만원</td><td>연 2.04~15%</td><td>수 분</td><td>낮아도 가능</td></tr><tr><td>토스 비상금</td><td>300만원</td><td>연 4~15%</td><td>수 분</td><td>650점 이상</td></tr><tr><td>케이뱅크 소액</td><td>200만원</td><td>연 3~12%</td><td>수 분</td><td>700점 이상</td></tr><tr><td>OK저축은행 앱</td><td>500만원</td><td>연 10~20%</td><td>당일</td><td>600점 이상</td></tr><tr><td>SBI저축은행</td><td>300만원</td><td>연 10~19.9%</td><td>당일</td><td>600점 이상</td></tr></tbody></table>"),
            ("급전 대출 시 절대 하지 말아야 할 것", "<ul><li><strong>불법 사금융 이용 금지</strong>: '당일 100만원 즉시 대출' 등 문자 광고는 대부분 불법 대부업 또는 사기입니다.</li><li><strong>개인정보 제공 금지</strong>: 신분증, 통장, 비밀번호 요구 시 100% 사기입니다.</li><li><strong>고금리 중복 대출 금지</strong>: 연 20% 이상 대출을 여러 개 사용하면 이자만으로 원금을 갚기 어렵습니다.</li></ul>"),
            ("저신용자도 받을 수 있는 정부 지원 소액 대출", "<ul><li><strong>미소금융</strong>: 기초생활수급자·차상위계층 대상, 연 4.5% 이하, 최대 2,000만원</li><li><strong>햇살론 15</strong>: 저소득·저신용자 대상, 연 15.9% 이하, 최대 700만원</li><li><strong>복지 긴급복지 지원</strong>: 실직·재난 등 긴급 상황 시 정부 생계비 지원 (대출 아님)</li></ul>"),
        ],
        "faq": [
            ("신용점수 없어도 100만원 당일 받을 수 있나요?", "카카오뱅크 비상금 대출은 신용점수가 낮아도 일부 승인되는 경우가 있습니다. 그 외에는 <strong>정부 지원 미소금융이나 복지 긴급 지원</strong>을 검토하세요. 불법 사금융은 절대 이용하지 마세요."),
            ("카드론과 비상금 대출 중 어느 것이 나은가요?", "일반적으로 <strong>비상금 대출(은행권)이 카드론보다 금리가 낮습니다.</strong> 카드론은 신용점수에 더 부정적인 영향을 줄 수 있으므로, 비상금 대출을 먼저 시도하세요."),
            ("급전 문자 광고를 믿어도 되나요?", "<strong>절대 믿으면 안 됩니다.</strong> '무직자 당일 대출', '신용불량자 즉시 대출' 등의 문자는 불법 대부업 광고이거나 사기일 가능성이 매우 높습니다. 금융감독원 불법금융 신고센터(1332)에 신고하세요."),
        ],
        "ctas": [
            {"text": "안전한 소액 대출 상품 비교하기", "desc": "금융감독원 포털에서 검증된 소액 대출 상품을 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "내 신용점수로 받을 수 있는 대출 찾기", "desc": "핀크에서 나의 조건에 맞는 소액 대출 상품을 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "비상금 대출 지금 신청하기", "desc": "토스에서 안전하게 비상금 대출을 신청하세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 22 =====
    {
        "title": "무직자 대출 가능한 곳 조건 주의사항 2026",
        "cat": 6,
        "slug": "unemployed-loan-options-2026",
        "intro": "직장이 없거나 일시적으로 실직 상태에 있어도 <strong>일정 조건을 충족하면 대출이 가능</strong>합니다. 다만 은행권 대출은 어렵고, 정부 지원 상품이나 특수 조건 상품을 통해야 합니다. 2026년 기준 무직자가 이용할 수 있는 합법적인 대출 방법과 주의사항을 정리했습니다.",
        "sections": [
            ("무직자 대출이 어려운 이유", "<p>대출 심사의 핵심은 <strong>상환 능력(소득) 확인</strong>입니다. 무직 상태에서는 소득 증빙이 어려워 대부분의 은행권 대출이 거절됩니다.</p><ul><li>소득 증빙 불가 → DSR 계산 불가 → 대출 한도 산정 불가</li><li>직업 안정성 낮음 → 대출 리스크 높음</li><li>단, 담보 대출이나 정부 지원 상품은 예외 가능</li></ul>"),
            ("무직자도 가능한 대출 상품 5가지", "<table><thead><tr><th>상품</th><th>조건</th><th>금리</th><th>한도</th></tr></thead><tbody><tr><td>부동산 담보대출</td><td>본인 소유 부동산 있을 경우</td><td>연 4~7%</td><td>LTV 이내</td></tr><tr><td>예금·적금 담보대출</td><td>예금·적금 보유자</td><td>예금금리+0.5~1.5%</td><td>예금액 95%</td></tr><tr><td>햇살론 15</td><td>저소득·저신용자</td><td>연 15.9% 이하</td><td>700만원</td></tr><tr><td>미소금융</td><td>기초생활수급자·실직자</td><td>연 4.5%</td><td>2,000만원</td></tr><tr><td>근로복지공단 실직자 대출</td><td>고용보험 실직급여 수급자</td><td>연 1~2%</td><td>1,000만원</td></tr></tbody></table>"),
            ("근로복지공단 생활안정자금 대출", "<p>고용보험 피보험자 또는 <strong>실직 후 구직급여 수급자</strong>라면 근로복지공단에서 매우 낮은 금리로 생활안정자금을 빌릴 수 있습니다.</p><ul><li>대상: 실직자, 고용보험 가입 근로자</li><li>금리: 연 1.5~2.0%</li><li>한도: 최대 1,000만원</li><li>신청: 근로복지공단 지사 방문 or 복지로(bokjiro.go.kr)</li></ul>"),
            ("예금·적금 담보대출 활용법", "<p>예금이나 적금이 있다면 <strong>만기 전에도 담보로 대출</strong>을 받을 수 있습니다. 소득 증빙이 필요 없고 금리도 매우 낮습니다.</p><ul><li>한도: 예금액의 90~95%</li><li>금리: 예금 금리 + 0.5~1.5% (예: 예금 3.5% → 대출 금리 4~5%)</li><li>신청: 해당 은행 앱 또는 방문</li></ul>"),
            ("무직자 대출 주의사항", "<ul><li><strong>불법 사금융 절대 금지</strong>: '무직자 즉시 대출' 광고는 불법 대부업·사기 가능성 99%</li><li><strong>법정 최고 금리 확인</strong>: 2026년 기준 대부업 최고 금리는 연 20%</li><li><strong>합법 대부업 이용 시</strong>: 금융감독원 등록 여부 반드시 확인 (파인 - fine.fss.or.kr)</li><li><strong>생계급여·주거급여</strong>: 대출 전 국가 복지 지원 수급 가능 여부를 먼저 확인</li></ul>"),
        ],
        "faq": [
            ("실직 후 생활비가 급한데 방법이 없나요?", "고용보험 실직급여 수급자라면 <strong>근로복지공단 생활안정자금(연 1.5~2%)</strong>을 우선 신청하세요. 기초생활수급자라면 미소금융, 긴급복지 지원을 받을 수 있습니다."),
            ("무직 주부는 대출이 전혀 불가능한가요?", "소득이 없는 주부도 <strong>배우자 소득 합산 or 부동산·예금 담보</strong>가 있다면 대출 가능합니다. 또는 카카오뱅크 비상금 대출(최대 300만원, 소액)을 시도해볼 수 있습니다."),
            ("프리랜서는 무직자로 분류되나요?", "프리랜서는 무직이 아니라 <strong>사업소득자</strong>로 분류됩니다. 소득세 신고서, 사업자 통장 거래 내역 등으로 소득 증빙이 가능하면 대출 신청 가능합니다."),
        ],
        "ctas": [
            {"text": "정부 지원 대출 상품 확인하기", "desc": "금융감독원 포털에서 정부 지원 저금리 대출 상품을 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "내 상황에 맞는 대출 상품 찾기", "desc": "핀크에서 무직자도 가능한 합법 대출 상품을 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "무료 대출 상담 받아보기", "desc": "토스에서 내 상황에 맞는 대출 방법을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 23 =====
    {
        "title": "햇살론 15 조건 금리 신청 방법 2026 총정리",
        "cat": 6,
        "slug": "hatsallon15-loan-guide-2026",
        "intro": "<strong>햇살론 15</strong>는 저소득·저신용 서민이 불법 사금융 대신 이용할 수 있는 정부 보증 대출입니다. 연 15.9% 이하의 금리가 적용되며, 저축은행·신협 등에서 신청할 수 있습니다. 2026년 기준 햇살론 15의 자격 조건, 금리, 한도, 신청 방법을 완벽하게 정리했습니다.",
        "sections": [
            ("햇살론 15란?", "<p><strong>햇살론 15</strong>는 서민금융진흥원이 보증하고 저축은행·신협·새마을금고 등에서 취급하는 서민 전용 정책 대출입니다. 최고 금리를 연 15.9%로 제한하여 고금리 불법 사금융 이용을 방지하는 것이 목적입니다.</p><ul><li>보증 기관: 서민금융진흥원</li><li>취급 기관: 저축은행·신협·새마을금고·수협 등</li><li>최고 금리: 연 15.9%</li><li>최대 한도: 700만원</li></ul>"),
            ("2026년 햇살론 15 자격 조건", "<table><thead><tr><th>구분</th><th>소득 기준</th><th>신용점수</th><th>비고</th></tr></thead><tbody><tr><td>저소득자</td><td>연소득 3,500만원 이하</td><td>제한 없음</td><td>소득만 충족하면 OK</td></tr><tr><td>저신용자</td><td>연소득 4,500만원 이하</td><td>NICE 620점 이하</td><td>신용점수 낮아도 가능</td></tr></tbody></table><p><strong>둘 중 하나의 조건만 충족</strong>하면 신청 가능합니다. 무직자·프리랜서도 소득 증빙만 되면 신청 가능합니다.</p>"),
            ("햇살론 15 금리·한도·기간", "<ul><li><strong>금리</strong>: 연 15.9% 이하 (실제 적용 금리는 기관·조건에 따라 상이)</li><li><strong>최대 한도</strong>: 700만원 (기존 햇살론 잔액 합산)</li><li><strong>대출 기간</strong>: 3년 이내 (원리금균등상환)</li><li><strong>보증료</strong>: 연 1.0% (서민금융진흥원 보증료)</li><li><strong>실제 이자 부담</strong>: 금리 + 보증료 = 최대 연 16.9%</li></ul>"),
            ("신청 방법 및 필요 서류", "<ol><li><strong>서민금융진흥원 콜센터(1397) 또는 홈페이지</strong> 사전 상담</li><li>가까운 저축은행·신협·새마을금고 방문 또는 앱 신청</li><li>서류 제출 및 심사</li><li>승인 후 대출 실행</li></ol><h3>필요 서류</h3><ul><li>신분증</li><li>소득 증빙: 원천징수영수증, 급여명세서, 사업소득 확인서, 수급확인서 등</li><li>가족관계증명서 (필요 시)</li></ul>"),
            ("햇살론 15 주의사항 및 활용 팁", "<ul><li><strong>한도 제한</strong>: 햇살론 전체 잔액이 700만원을 초과할 수 없습니다. 기존 햇살론이 있다면 차감된 금액만 추가 신청 가능</li><li><strong>성실 상환의 중요성</strong>: 성실하게 상환하면 신용점수가 오르고, 이후 더 좋은 조건의 대출로 갈아탈 수 있습니다</li><li><strong>보증료 추가</strong>: 금리 외 보증료(연 1%)가 추가로 부과됩니다</li><li><strong>사전 상담 필수</strong>: 조건 충족 여부를 1397로 사전 확인 후 방문하세요</li></ul>"),
            ("햇살론 관련 상품 비교", "<table><thead><tr><th>상품</th><th>대상</th><th>금리</th><th>한도</th><th>취급처</th></tr></thead><tbody><tr><td>햇살론 15</td><td>저소득·저신용</td><td>연 15.9%</td><td>700만원</td><td>저축은행·신협</td></tr><tr><td>햇살론 뱅크</td><td>저소득·저신용</td><td>연 6.5~10.5%</td><td>2,000만원</td><td>시중은행</td></tr><tr><td>사잇돌 대출</td><td>중신용자</td><td>연 5.9~14.9%</td><td>2,000만원</td><td>시중은행·저축은행</td></tr><tr><td>미소금융</td><td>기초생활수급자</td><td>연 4.5%</td><td>2,000만원</td><td>미소금융재단</td></tr></tbody></table>"),
        ],
        "faq": [
            ("햇살론 15를 받으면 신용점수가 더 내려가나요?", "대출 자체가 신용점수를 크게 낮추지는 않습니다. <strong>성실하게 상환하면 오히려 신용점수가 상승</strong>합니다. 연체 없이 꾸준히 납부하세요."),
            ("실직 중에도 햇살론 15 신청이 가능한가요?", "<strong>실업급여 수급 중이거나 소득 증빙이 가능하다면 신청 가능</strong>합니다. 소득이 전혀 없다면 서민금융진흥원(1397)에 전화해 상담을 먼저 받으세요."),
            ("햇살론 15 상환 중에 조기 상환이 가능한가요?", "네, 가능합니다. <strong>중도상환수수료가 부과될 수 있으므로</strong> 취급 기관에 확인 후 상환하세요."),
        ],
        "ctas": [
            {"text": "햇살론 15 자격 확인 및 상담", "desc": "서민금융진흥원(1397) 또는 금융소비자포털에서 자격을 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "저신용자 맞춤 대출 상품 비교", "desc": "핀크에서 내 신용점수에 맞는 정책 대출 상품을 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "서민 대출 무료 상담 받기", "desc": "토스에서 내 상황에 맞는 서민 금융 상품을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 24 =====
    {
        "title": "햇살론 뱅크 조건 한도 금리 신청 완벽 가이드 2026",
        "cat": 6,
        "slug": "hatsallon-bank-guide-2026",
        "intro": "<strong>햇살론 뱅크</strong>는 저소득·저신용 서민이 시중은행에서 낮은 금리로 대출을 받을 수 있도록 정부가 보증하는 상품입니다. 햇살론 15보다 낮은 금리(연 6.5~10.5%)와 높은 한도(최대 2,000만원)가 특징입니다. 2026년 최신 조건을 완벽 정리했습니다.",
        "sections": [
            ("햇살론 뱅크란?", "<p><strong>햇살론 뱅크</strong>는 서민금융진흥원이 보증하고 시중은행(국민·신한·하나·우리·농협 등)이 취급하는 정책 서민 대출입니다. 기존 햇살론(저축은행)보다 낮은 금리로 시중은행 창구에서 이용할 수 있습니다.</p><ul><li>보증 기관: 서민금융진흥원</li><li>취급 기관: 시중은행(국민·신한·우리·하나·농협 등)</li><li>금리: 연 6.5~10.5%</li><li>최대 한도: 2,000만원</li></ul>"),
            ("2026년 햇살론 뱅크 자격 조건", "<table><thead><tr><th>구분</th><th>연소득</th><th>신용점수</th></tr></thead><tbody><tr><td>저소득자</td><td>3,500만원 이하</td><td>제한 없음</td></tr><tr><td>저신용자</td><td>4,500만원 이하</td><td>NICE 620점 이하</td></tr></tbody></table><p>햇살론 15와 동일한 소득·신용 기준이 적용됩니다. 단, 현재 연체 중이거나 금융채무불이행자(신용불량자) 등록 상태면 신청이 어렵습니다.</p>"),
            ("햇살론 뱅크 금리·한도·기간 상세", "<ul><li><strong>금리</strong>: 연 6.5~10.5% (취급 은행·신용 조건에 따라 다름)</li><li><strong>최대 한도</strong>: 2,000만원</li><li><strong>대출 기간</strong>: 3년 이내</li><li><strong>상환 방식</strong>: 원리금균등상환</li><li><strong>보증료</strong>: 연 0.5~0.9% (서민금융진흥원)</li></ul><h3>월 상환액 예시</h3><p>1,000만원, 금리 8%, 3년 원리금균등 → 월 약 <strong>31.3만원</strong></p>"),
            ("신청 방법 및 필요 서류", "<ol><li>서민금융진흥원(1397) 또는 은행 앱에서 사전 자격 확인</li><li>협약 은행 방문 또는 비대면 신청 (일부 은행)</li><li>서류 제출 및 심사</li><li>보증서 발급</li><li>대출 실행</li></ol><h3>필요 서류</h3><ul><li>신분증</li><li>소득 증빙: 원천징수영수증, 건강보험료 납부 확인서</li><li>재직 증명서 (직장인)</li></ul>"),
            ("햇살론 뱅크 vs 햇살론 15 비교", "<table><thead><tr><th>구분</th><th>햇살론 뱅크</th><th>햇살론 15</th></tr></thead><tbody><tr><td>취급 기관</td><td>시중은행</td><td>저축은행·신협 등</td></tr><tr><td>금리</td><td>연 6.5~10.5%</td><td>연 15.9%</td></tr><tr><td>최대 한도</td><td>2,000만원</td><td>700만원</td></tr><tr><td>자격 조건</td><td>동일</td><td>동일</td></tr><tr><td>심사 난이도</td><td>다소 까다로움</td><td>상대적으로 쉬움</td></tr></tbody></table><p>조건이 맞는다면 <strong>햇살론 뱅크가 훨씬 유리</strong>합니다. 거절 시 햇살론 15를 차선책으로 검토하세요.</p>"),
        ],
        "faq": [
            ("햇살론 뱅크를 받으면 다른 대출과 중복 이용이 가능한가요?", "다른 대출과 동시에 보유할 수는 있지만, <strong>DSR 규제가 적용</strong>되므로 기존 대출이 많으면 한도가 줄어듭니다."),
            ("햇살론 뱅크 성실 상환 후 일반 신용대출로 갈아탈 수 있나요?", "네, 성실 상환 시 신용점수가 올라 이후 <strong>일반 신용대출이나 마이너스통장으로 갈아타기</strong>가 가능합니다."),
            ("햇살론 뱅크 신청 은행이 정해져 있나요?", "취급 은행은 <strong>국민·신한·우리·하나·농협·기업은행 등 주요 시중은행</strong>에서 이용 가능합니다. 일부 은행은 비대면 신청도 지원합니다."),
        ],
        "ctas": [
            {"text": "햇살론 뱅크 자격 확인하기", "desc": "서민금융진흥원 또는 금융소비자포털에서 자격을 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "서민 금융 상품 한눈에 비교", "desc": "핀크에서 햇살론 뱅크를 포함한 서민 대출 상품을 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "서민 대출 무료 상담 신청", "desc": "토스에서 내 조건에 맞는 서민 금융 상품을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 25 =====
    {
        "title": "새희망홀씨 대출 조건 금리 한도 신청 방법 2026",
        "cat": 6,
        "slug": "new-hope-loan-guide-2026",
        "intro": "<strong>새희망홀씨 대출</strong>은 저소득·저신용 서민을 위해 시중은행이 자체적으로 운영하는 서민 금융 상품입니다. 정부 보증 없이 은행이 직접 대출하는 구조로, 햇살론보다 금리가 낮은 경우도 있습니다. 2026년 기준 새희망홀씨의 조건, 금리, 한도, 신청 방법을 정리했습니다.",
        "sections": [
            ("새희망홀씨 대출이란?", "<p><strong>새희망홀씨 대출</strong>은 정부 지시로 시중은행이 저소득·저신용 서민을 위해 자체 재원으로 공급하는 서민 대출입니다. 은행마다 조건이 다를 수 있으며, 정부 보증 없이 은행이 자체 심사합니다.</p><ul><li>취급 은행: 국민·신한·하나·우리·농협·기업 등 시중은행</li><li>금리: 연 6~10% 수준 (은행별 상이)</li><li>한도: 최대 2,000만원</li></ul>"),
            ("2026년 새희망홀씨 자격 조건", "<table><thead><tr><th>구분</th><th>조건</th></tr></thead><tbody><tr><td>소득</td><td>연소득 3,500만원 이하 (일부 4,500만원)</td></tr><tr><td>신용점수</td><td>NICE 620점 이하 (저신용자) or 소득 기준만 충족</td></tr><tr><td>재직 여부</td><td>직장인·사업자·프리랜서 모두 가능</td></tr><tr><td>배제 조건</td><td>현재 연체 중, 금융채무불이행자</td></tr></tbody></table>"),
            ("은행별 새희망홀씨 금리·한도 비교", "<table><thead><tr><th>은행</th><th>금리</th><th>최대 한도</th><th>특징</th></tr></thead><tbody><tr><td>국민은행</td><td>연 7~10%</td><td>2,000만원</td><td>KB맞춤형</td></tr><tr><td>신한은행</td><td>연 6.5~9.5%</td><td>2,000만원</td><td>신한SHe대출</td></tr><tr><td>하나은행</td><td>연 6.5~9.5%</td><td>2,000만원</td><td>하나희망나눔</td></tr><tr><td>우리은행</td><td>연 7~10%</td><td>2,000만원</td><td>우리새희망홀씨</td></tr><tr><td>농협은행</td><td>연 7~10%</td><td>2,000만원</td><td>NH희망나눔</td></tr></tbody></table>"),
            ("신청 방법 및 서류", "<ol><li>은행 홈페이지 또는 영업점에서 새희망홀씨 대출 문의</li><li>자격 확인 후 신청 서류 제출</li><li>소득·신용 심사</li><li>대출 승인 및 실행</li></ol><h3>필요 서류</h3><ul><li>신분증</li><li>소득 증빙 서류 (근로소득원천징수영수증 or 건강보험 납부 확인서)</li><li>재직 증명서 (직장인)</li></ul>"),
            ("새희망홀씨 vs 햇살론 뱅크 vs 사잇돌 비교", "<table><thead><tr><th>구분</th><th>새희망홀씨</th><th>햇살론 뱅크</th><th>사잇돌</th></tr></thead><tbody><tr><td>보증</td><td>은행 자체</td><td>서민금융진흥원</td><td>신용보증기금</td></tr><tr><td>금리</td><td>연 6~10%</td><td>연 6.5~10.5%</td><td>연 5.9~14.9%</td></tr><tr><td>한도</td><td>2,000만원</td><td>2,000만원</td><td>2,000만원</td></tr><tr><td>신용점수</td><td>620점 이하 or 저소득</td><td>620점 이하 or 저소득</td><td>620~839점</td></tr></tbody></table>"),
        ],
        "faq": [
            ("새희망홀씨를 거절당하면 다른 서민 대출을 받을 수 있나요?", "새희망홀씨 거절 후에는 <strong>햇살론 뱅크 → 사잇돌 대출 → 햇살론 15</strong> 순으로 시도해보세요. 서민금융진흥원(1397)에 전화하면 통합 상담을 받을 수 있습니다."),
            ("새희망홀씨와 햇살론 뱅크를 동시에 받을 수 있나요?", "원칙적으로 가능하지만 <strong>DSR 규제 및 총 한도 제한</strong>이 있습니다. 중복 이용보다 하나를 성실히 상환하고 신용점수를 높이는 것이 장기적으로 유리합니다."),
        ],
        "ctas": [
            {"text": "새희망홀씨 대출 조건 확인하기", "desc": "금융감독원 포털에서 새희망홀씨 취급 은행을 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "서민 금융 상품 한눈에 비교하기", "desc": "핀크에서 서민 대출 상품을 비교하고 최적 상품을 찾으세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "서민 금융 통합 상담 받기", "desc": "토스에서 내 조건에 맞는 서민 대출을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 26 =====
    {
        "title": "사잇돌 대출 중신용자 조건 금리 한도 2026 완벽 가이드",
        "cat": 6,
        "slug": "saitdol-loan-guide-2026",
        "intro": "<strong>사잇돌 대출</strong>은 1금융권 대출은 어렵지만 고금리 대출은 피하고 싶은 중신용자(신용점수 620~839점)를 위한 정책 대출입니다. 신용보증기금이 보증하고 시중은행과 저축은행에서 취급하며, 연 5.9~14.9% 금리로 최대 2,000만원까지 빌릴 수 있습니다. 2026년 기준 사잇돌 대출의 모든 것을 정리했습니다.",
        "sections": [
            ("사잇돌 대출이란?", "<p><strong>사잇돌 대출</strong>은 중신용자의 금융 접근성을 높이기 위해 신용보증기금(KODIT)이 보증하는 정책 대출입니다. 1금융권에서 거절당한 중신용자가 2금융권 고금리 대출로 빠지는 것을 막기 위해 설계되었습니다.</p><ul><li>보증 기관: 신용보증기금(KODIT)</li><li>취급 기관: 시중은행 + 저축은행</li><li>금리: 연 5.9~14.9%</li><li>최대 한도: 2,000만원</li></ul>"),
            ("2026년 사잇돌 대출 자격 조건", "<table><thead><tr><th>구분</th><th>사잇돌 1(은행)</th><th>사잇돌 2(저축은행)</th></tr></thead><tbody><tr><td>신용점수</td><td>NICE 620~839점</td><td>NICE 620점 미만도 가능</td></tr><tr><td>연소득</td><td>제한 없음</td><td>제한 없음</td></tr><tr><td>금리</td><td>연 5.9~10.9%</td><td>연 10.9~14.9%</td></tr><tr><td>최대 한도</td><td>2,000만원</td><td>2,000만원</td></tr><tr><td>취급 은행</td><td>국민·신한·하나·우리·농협 등</td><td>OK저축은행 등</td></tr></tbody></table><p>현재 연체 중이거나 금융채무불이행자로 등록된 경우에는 신청이 불가합니다.</p>"),
            ("사잇돌 대출 금리·한도·기간 상세", "<ul><li><strong>금리</strong>: 연 5.9~14.9% (신용점수·소득에 따라 결정)</li><li><strong>최대 한도</strong>: 2,000만원 (사잇돌 1+2 합산)</li><li><strong>대출 기간</strong>: 1~5년</li><li><strong>상환 방식</strong>: 원리금균등·원금균등·만기일시 중 선택</li><li><strong>보증료</strong>: 연 0.9~2.0% (신용보증기금)</li></ul><h3>월 상환액 예시 (1,000만원, 연 8%, 3년)</h3><p>원리금균등 상환 시 월 약 <strong>31.3만원</strong></p>"),
            ("신청 방법 및 필요 서류", "<ol><li>취급 은행 또는 저축은행 방문·앱 접속</li><li>사잇돌 대출 신청 (신용보증기금 보증 심사 병행)</li><li>소득·신용 심사 후 보증서 발급</li><li>대출 실행</li></ol><h3>필요 서류</h3><ul><li>신분증</li><li>소득 증빙: 원천징수영수증, 건강보험료 납부 확인서, 사업소득 확인서</li><li>재직 증명서 (직장인)</li></ul>"),
            ("사잇돌 대출 활용 전략", "<ul><li><strong>신용점수 620~839점</strong>이라면 사잇돌 1(은행) 먼저 시도, 거절 시 사잇돌 2(저축은행) 신청</li><li>사잇돌 대출로 고금리 기존 대출을 상환하는 <strong>대환 전략</strong>이 유효합니다</li><li>성실 상환 시 신용점수 상승 → 이후 일반 신용대출로 갈아타기 가능</li><li>보증료를 포함한 실질 비용을 꼭 계산하세요</li></ul>"),
        ],
        "faq": [
            ("사잇돌 대출과 햇살론 뱅크 중 어떤 것이 유리한가요?", "신용점수가 620점 이하라면 <strong>햇살론 뱅크</strong>가 더 적합합니다. 620~839점 중신용자라면 <strong>사잇돌 대출 1</strong>을 먼저 시도하세요. 금리는 비슷하지만 사잇돌은 소득 기준 제한이 없습니다."),
            ("사잇돌 대출 거절 시 다음 단계는?", "사잇돌 거절 후에는 <strong>새희망홀씨 → 햇살론 15</strong> 순으로 시도하거나, 서민금융진흥원(1397)에서 통합 상담을 받으세요."),
            ("사잇돌 대출 한도가 낮게 나오는 이유는?", "보증기관의 신용 심사 결과와 DSR 규제에 따라 한도가 결정됩니다. 기존 대출이 많거나 소득 대비 부채 비율이 높으면 한도가 줄어듭니다."),
        ],
        "ctas": [
            {"text": "사잇돌 대출 자격 조건 확인하기", "desc": "금융소비자포털에서 사잇돌 대출 취급 기관을 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "중신용자 맞춤 대출 상품 비교", "desc": "핀크에서 내 신용점수에 맞는 정책 대출 상품을 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "사잇돌 대출 무료 상담 신청", "desc": "토스에서 내 조건에 맞는 중신용 대출 상품을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 27 =====
    {
        "title": "미소금융 대출 조건 신청 방법 2026 총정리",
        "cat": 6,
        "slug": "miso-finance-loan-guide-2026",
        "intro": "<strong>미소금융</strong>은 기초생활수급자·차상위 계층 등 금융 취약 계층이 창업·운영 자금을 연 4.5% 이하의 초저금리로 빌릴 수 있는 정부 지원 서민 금융 프로그램입니다. 신용점수나 담보가 없어도 사업 의지만 있으면 신청 가능합니다. 2026년 기준 미소금융의 조건, 한도, 신청 방법을 완벽 정리했습니다.",
        "sections": [
            ("미소금융이란?", "<p><strong>미소금융</strong>은 저소득·금융 취약 계층의 자립을 지원하기 위해 서민금융진흥원이 운영하는 무담보·무보증 소액 대출 프로그램입니다. 창업 자금, 운영 자금, 긴급 생계 자금 등으로 활용할 수 있습니다.</p><ul><li>운영 기관: 서민금융진흥원 + 미소금융재단</li><li>금리: 연 4.5% 이하</li><li>한도: 용도별 최대 7,000만원</li><li>무담보·무보증 원칙</li></ul>"),
            ("2026년 미소금융 대출 종류 및 한도", "<table><thead><tr><th>대출 종류</th><th>대상</th><th>한도</th><th>금리</th></tr></thead><tbody><tr><td>창업 자금</td><td>창업 예정자 또는 3년 미만 사업자</td><td>7,000만원</td><td>연 4.5%</td></tr><tr><td>운영 자금</td><td>기존 사업자 (운전 자금)</td><td>2,000만원</td><td>연 4.5%</td></tr><tr><td>시설 개선 자금</td><td>기존 사업자 (설비 교체)</td><td>2,000만원</td><td>연 4.5%</td></tr><tr><td>긴급 생계 자금</td><td>기초생활수급자·차상위</td><td>100만원</td><td>연 무이자</td></tr></tbody></table>"),
            ("미소금융 자격 조건", "<ul><li><strong>기초생활수급자</strong>: 생계·의료·주거·교육급여 수급자</li><li><strong>차상위 계층</strong>: 중위소득 50% 이하</li><li><strong>근로 빈곤층</strong>: 연소득 2,400만원 이하이며 금융 소외 계층</li><li><strong>금융 채무불이행자</strong>도 일부 상품은 신청 가능</li></ul><p>신용점수나 담보 없이도 신청 가능하나, <strong>사업 계획서 또는 창업 의지</strong>가 심사의 핵심 기준입니다.</p>"),
            ("신청 방법 및 절차", "<ol><li>가까운 <strong>미소금융 지점</strong> 방문 (전국 300여 개 지점)</li><li>상담 후 대출 신청서 작성</li><li>심사 (사업 계획서, 자립 의지 평가)</li><li>교육 이수 (창업 자금의 경우 의무)</li><li>대출 실행</li></ol><h3>필요 서류</h3><ul><li>신분증</li><li>수급자 증명서 또는 소득 증빙</li><li>사업 계획서 (창업 자금)</li><li>사업자 등록증 (운영·시설 자금)</li></ul>"),
            ("미소금융 활용 팁 및 주의사항", "<ul><li>창업 자금은 <strong>반드시 교육(8~16시간)을 이수</strong>해야 대출 실행됩니다</li><li>긴급 생계 자금(100만원)은 무이자로 빠르게 받을 수 있어 위급 시 유용합니다</li><li>대출 후 담당 매니저의 <strong>경영 지도·멘토링</strong>을 적극 활용하세요</li><li>상환 기간은 보통 5~7년이며, 거치 기간(1~2년) 설정도 가능합니다</li><li>미소금융재단 공식 홈페이지(misof.or.kr)에서 가까운 지점을 찾을 수 있습니다</li></ul>"),
        ],
        "faq": [
            ("미소금융은 신용불량자도 받을 수 있나요?", "네, <strong>금융채무불이행자(신용불량자)도 일부 미소금융 상품을 신청할 수 있습니다.</strong> 신용점수보다 자립 의지와 사업 계획이 더 중요한 심사 기준입니다."),
            ("미소금융 창업 자금과 일반 정책 자금의 차이는?", "미소금융은 <strong>금융 취약 계층 전용</strong>으로 신용·담보 조건이 없습니다. 소상공인진흥공단 정책 자금은 신용 및 사업 실적 조건이 더 요구됩니다."),
            ("미소금융 대출 후 사업에 실패하면 어떻게 되나요?", "일반 대출과 동일하게 상환 의무가 있습니다. 다만 <strong>상환 유예·분할 납부 협의</strong>가 가능하며, 담당 매니저와 적극적으로 소통하는 것이 중요합니다."),
        ],
        "ctas": [
            {"text": "미소금융 지원 자격 확인하기", "desc": "서민금융진흥원에서 미소금융 신청 자격을 확인하고 상담받으세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "서민 금융 상품 한눈에 비교", "desc": "핀크에서 미소금융을 포함한 서민 금융 상품을 한눈에 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "서민 금융 무료 상담 받기", "desc": "토스에서 내 상황에 맞는 서민 금융 방법을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 28 =====
    {
        "title": "전월세 대환대출 저금리 갈아타기 완벽 가이드 2026",
        "cat": 6,
        "slug": "mortgage-refinancing-low-rate-2026",
        "intro": "<strong>전월세 대환대출</strong>은 기존 고금리 전세·월세 대출을 낮은 금리의 정책 대출로 갈아타는 방법입니다. 2024년부터 시행된 주택 대환대출 인프라 덕분에 은행 방문 없이 앱으로 간편하게 갈아탈 수 있습니다. 2026년 기준 전월세 대환대출 조건, 절차, 절약 효과를 상세히 안내합니다.",
        "sections": [
            ("전월세 대환대출이란?", "<p><strong>대환대출(갈아타기)</strong>이란 기존 대출을 더 낮은 금리의 새로운 대출로 교체하는 것입니다. 전월세 대환은 기존 전세·월세 대출을 <strong>버팀목 전세 대출, 청년 전세 대출 등 정책 저금리 상품</strong>으로 전환하는 것이 핵심입니다.</p><ul><li>2024년 1월부터 주택담보대출 대환 인프라 운영</li><li>전세 대출도 비대면 갈아타기 가능</li><li>주요 절약 효과: 연 1~3%p 금리 절감</li></ul>"),
            ("2026년 전월세 대환대출 주요 상품 비교", "<table><thead><tr><th>상품명</th><th>대상</th><th>금리</th><th>한도</th></tr></thead><tbody><tr><td>버팀목 전세 대출</td><td>무주택 세대주</td><td>연 2.1~2.9%</td><td>수도권 3억/지방 2억</td></tr><tr><td>청년 버팀목 전세 대출</td><td>만 19~34세 청년</td><td>연 1.5~2.7%</td><td>3억원</td></tr><tr><td>신혼부부 전세 대출</td><td>혼인 7년 이내</td><td>연 1.2~2.7%</td><td>3억원</td></tr><tr><td>일반 은행 전세 대출</td><td>누구나</td><td>연 3.5~5.5%</td><td>전세가의 80%</td></tr></tbody></table>"),
            ("대환대출 자격 조건 및 절차", "<h3>자격 조건</h3><ul><li>무주택 세대주 (정책 대출 기준)</li><li>소득 기준: 부부 합산 연소득 5,000~7,000만원 이하 (상품별 상이)</li><li>전세 보증금 기준 내 주택</li></ul><h3>대환 절차</h3><ol><li>현재 전세 대출 잔액 및 금리 확인</li><li>갈아탈 상품 선택 (버팀목·청년 버팀목 등)</li><li>새 대출 신청 및 심사</li><li>기존 대출 상환 + 신규 대출 실행</li></ol>"),
            ("중도상환수수료 계산 및 절약 효과", "<p>대환 시 기존 대출의 <strong>중도상환수수료</strong>가 발생할 수 있습니다.</p><ul><li>중도상환수수료율: 보통 0.6~1.2% (잔액 기준)</li><li>대출 실행 후 3년 이후에는 수수료 없는 경우도 있음</li></ul><h3>절약 효과 예시</h3><table><thead><tr><th>구분</th><th>기존 대출</th><th>갈아타기 후</th><th>연간 절감</th></tr></thead><tbody><tr><td>전세 2억, 3년</td><td>연 4.5%</td><td>연 2.5%</td><td>약 400만원</td></tr><tr><td>전세 1억, 2년</td><td>연 5.0%</td><td>연 2.1%</td><td>약 290만원</td></tr></tbody></table>"),
            ("대환대출 주의사항 및 팁", "<ul><li><strong>중도상환수수료</strong>가 이자 절감액보다 클 경우 갈아타기가 불리할 수 있습니다. 반드시 계산하세요</li><li>정책 대출은 소득·자산 기준을 충족해야 하므로 사전 자격 확인 필수</li><li>주택 가격 변동이 없는지 감정가 재확인 필요</li><li>핀다, 토스, 카카오페이 앱에서 <strong>비대면 대환대출 비교</strong>가 가능합니다</li></ul>"),
        ],
        "faq": [
            ("전세 대출 갈아타기 시 임대인 동의가 필요한가요?", "대부분의 경우 임대인 동의가 필요하지 않지만, <strong>HUG·HF 보증 전세 대출은 임대인 동의</strong>가 필요할 수 있습니다. 대출 기관에 사전 확인하세요."),
            ("전세 계약 중간에 갈아타기가 가능한가요?", "네, 계약 기간 중에도 <strong>중도상환수수료 없는 시점</strong>을 노려 갈아타기가 가능합니다. 만기 3개월 전 갱신 시점에 갈아타는 것이 가장 유리합니다."),
            ("버팀목 전세 대출로 갈아탈 때 소득 기준은?", "부부 합산 연소득 <strong>5,000만원 이하(신혼부부 7,000만원 이하)</strong>가 기준입니다. 소득 초과 시 청년·신혼 특례 상품 또는 일반 은행 갈아타기를 검토하세요."),
        ],
        "ctas": [
            {"text": "버팀목 전세 대출 자격 확인하기", "desc": "주택도시기금에서 전세 대환대출 자격 조건을 확인하세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "전세 대출 금리 한눈에 비교하기", "desc": "핀크에서 전세 대환대출 상품을 비교하고 최저 금리를 찾으세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "대환대출 무료 상담 신청하기", "desc": "토스에서 내 전세 대출 갈아타기 조건을 무료로 비교받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 29 =====
    {
        "title": "소상공인 정책 대출 종류 비교 2026 완벽 정리",
        "cat": 6,
        "slug": "small-business-policy-loan-2026",
        "intro": "<strong>소상공인 정책 대출</strong>은 정부와 공공기관이 소상공인·자영업자를 지원하기 위해 저금리로 제공하는 대출입니다. 소진공 정책 자금, 신용보증재단 보증 대출, 지자체 특화 대출 등 종류가 다양하여 어떤 것을 선택해야 할지 헷갈리는 경우가 많습니다. 2026년 기준 소상공인 정책 대출의 종류와 조건을 한눈에 정리했습니다.",
        "sections": [
            ("소상공인 정책 대출 주요 종류", "<table><thead><tr><th>대출 종류</th><th>취급 기관</th><th>금리</th><th>최대 한도</th></tr></thead><tbody><tr><td>소진공 직접 대출</td><td>소상공인진흥공단</td><td>연 2.0~3.5%</td><td>1억원</td></tr><tr><td>소진공 협업 대출</td><td>시중은행+소진공</td><td>연 3.0~5.0%</td><td>7,000만원</td></tr><tr><td>신보 보증 대출</td><td>신용보증재단+은행</td><td>연 3.5~6.0%</td><td>5억원</td></tr><tr><td>기보 보증 대출</td><td>기술보증기금+은행</td><td>연 3.0~5.5%</td><td>30억원</td></tr><tr><td>지자체 특화 대출</td><td>지역별 상이</td><td>연 1.5~4.0%</td><td>5,000만원</td></tr></tbody></table>"),
            ("소진공 직접 대출 조건 및 신청", "<p><strong>소상공인진흥공단 직접 대출</strong>은 가장 저렴한 금리(연 2.0~3.5%)를 제공하지만 신청 경쟁이 치열하고 대기 기간이 길 수 있습니다.</p><ul><li>자격: 소상공인 (5인 미만 사업체, 일부 업종 10인 미만)</li><li>사업 기간: 최소 6개월 이상</li><li>제외 업종: 유흥업, 도박, 일부 금융업</li><li>신청: 소상공인 스마트 포털(www.sbiz.or.kr)</li></ul>"),
            ("신용보증재단 보증 대출 활용법", "<p><strong>신용보증재단(지역 신보)</strong>의 보증서를 발급받아 은행에서 대출받는 방식입니다. 보증 비율은 최대 100%이며, 담보 없는 소상공인도 이용 가능합니다.</p><ul><li>보증료: 연 0.5~2.0%</li><li>한도: 최대 5억원 (업종·신용에 따라 상이)</li><li>신청 방법: 지역 신용보증재단 방문 또는 은행 창구</li><li>활용 팁: 보증서 발급 후 복수 은행에 경쟁 견적 내서 가장 낮은 금리 선택</li></ul>"),
            ("2026년 소상공인 대출 지원 특별 프로그램", "<ul><li><strong>소상공인 긴급 경영 안정 자금</strong>: 매출 급감·재해 피해 시 긴급 지원 (연 2.0%)</li><li><strong>청년 소상공인 창업 자금</strong>: 만 39세 이하 창업자 우대 금리</li><li><strong>혁신형 소상공인 지원</strong>: 스마트 스토어·디지털 전환 업체 우대</li><li><strong>지자체 이차 보전</strong>: 광역 지자체별 금리 추가 인하 (0.5~2.0%p)</li></ul>"),
            ("소상공인 대출 신청 전 체크리스트", "<ul><li>사업자 등록증 유효 여부 확인</li><li>국세·지방세 체납 여부 (체납 시 신청 불가)</li><li>최근 6개월 매출 증빙 준비 (부가세 신고서, 카드 매출 내역)</li><li>신용점수 확인 (550점 미만이면 보증 심사 어려울 수 있음)</li><li>기존 정책 자금 연체 여부 확인</li></ul>"),
        ],
        "faq": [
            ("소진공 직접 대출과 보증 대출 중 어떤 것이 유리한가요?", "<strong>소진공 직접 대출</strong>은 금리가 더 낮지만 대기가 길고 한도가 낮습니다. 빠르게 자금이 필요하거나 한도가 많이 필요하다면 <strong>신보 보증 대출</strong>이 유리합니다."),
            ("소상공인 정책 대출은 법인도 받을 수 있나요?", "소상공인 기준(상시 근로자 5인 미만)을 충족하는 <strong>법인도 신청 가능</strong>합니다. 다만 법인세 신고서 등 추가 서류가 필요합니다."),
            ("세금 체납이 있으면 정책 대출이 불가능한가요?", "국세·지방세 체납 시 대부분의 정책 대출 신청이 제한됩니다. <strong>분납 합의 후 정리 중</strong>이라면 기관에 따라 예외 적용될 수 있으니 사전 상담이 필요합니다."),
        ],
        "ctas": [
            {"text": "소상공인 정책 자금 신청하기", "desc": "소상공인 스마트포털에서 정책 대출 자격 조건을 확인하세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "소상공인 대출 상품 비교하기", "desc": "핀크에서 소상공인 맞춤 대출 상품을 한눈에 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "소상공인 대출 무료 상담 받기", "desc": "토스에서 소상공인 맞춤 금융 솔루션을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 30 =====
    {
        "title": "프리랜서 소득 증빙 대출 방법 2026 완벽 가이드",
        "cat": 6,
        "slug": "freelancer-income-proof-loan-2026",
        "intro": "<strong>프리랜서 대출</strong>에서 가장 큰 장벽은 소득 증빙입니다. 회사에 재직 중인 직장인과 달리 프리랜서는 다양한 방식으로 소득을 증빙해야 합니다. 2026년 기준 프리랜서가 대출받는 방법, 소득 증빙 서류, 유리한 대출 상품을 단계별로 안내합니다.",
        "sections": [
            ("프리랜서 소득 증빙 서류 종류", "<table><thead><tr><th>증빙 방법</th><th>서류</th><th>인정 수준</th></tr></thead><tbody><tr><td>종합소득세 신고</td><td>종합소득세 신고서 + 납부 확인서</td><td>매우 높음</td></tr><tr><td>사업소득 원천징수</td><td>원천징수영수증(3.3% 세율)</td><td>높음</td></tr><tr><td>건강보험료 납부</td><td>건강보험료 납부 확인서</td><td>중간</td></tr><tr><td>통장 거래 내역</td><td>최근 6~12개월 입출금 내역</td><td>중간</td></tr><tr><td>계약서·세금계산서</td><td>용역 계약서, 세금계산서</td><td>보조 자료</td></tr></tbody></table>"),
            ("프리랜서 대출 가능한 금융권별 비교", "<table><thead><tr><th>금융권</th><th>가능 여부</th><th>소득 증빙 요건</th><th>평균 금리</th></tr></thead><tbody><tr><td>1금융권(은행)</td><td>종소세 신고 필수</td><td>2년 이상 신고 이력</td><td>연 4~7%</td></tr><tr><td>2금융권(저축은행·카드)</td><td>원천징수 또는 통장 내역</td><td>최근 6개월 이상</td><td>연 8~18%</td></tr><tr><td>정책 대출(서민금융)</td><td>소득 확인 가능 시</td><td>수급 확인서, 소득 확인서</td><td>연 4.5~10%</td></tr></tbody></table>"),
            ("프리랜서에게 유리한 대출 상품 TOP 5", "<ol><li><strong>인터넷 은행 신용대출</strong>(케이뱅크·카카오뱅크): 사업소득 원천징수 또는 건강보험료로 소득 인정, 비대면 간편 신청</li><li><strong>카드론·리볼빙</strong>: 카드 사용 실적 기반, 별도 소득 증빙 불필요 (고금리 주의)</li><li><strong>사잇돌 대출</strong>: 중신용자도 가능, 소득 확인서 인정</li><li><strong>햇살론 뱅크</strong>: 저소득 프리랜서 가능, 건강보험 납부 확인서로 소득 인정</li><li><strong>P2P·핀테크 대출</strong>: 사업 포트폴리오, 거래 내역 기반 심사</li></ol>"),
            ("종합소득세 신고로 대출력 높이는 방법", "<ul><li>프리랜서라면 <strong>5월 종합소득세 신고</strong>를 반드시 하세요. 신고 이력이 2년 이상이면 1금융권 대출이 훨씬 수월해집니다</li><li>소득을 과소 신고하면 절세는 되지만 대출 한도가 줄어듭니다. 트레이드오프를 고려하세요</li><li>건강보험 지역 가입자로 전환되면 보험료 납부 확인서로도 소득 인정 가능</li><li>사업자 등록(개인사업자)을 하면 더 다양한 대출 상품 이용 가능</li></ul>"),
            ("프리랜서 대출 신청 시 주의사항", "<ul><li><strong>소득 과장 신청은 금융 사기</strong>에 해당합니다. 실제 소득 범위 내에서 신청하세요</li><li>카드론은 금리가 높으므로 단기 자금에만 사용하고 장기 이용은 피하세요</li><li>여러 곳에 동시 신청하면 신용 조회가 집중되어 신용점수가 일시적으로 하락할 수 있습니다</li><li>DSR 규제 적용으로 기존 대출이 많으면 추가 한도가 제한됩니다</li></ul>"),
        ],
        "faq": [
            ("프리랜서 소득이 불규칙해도 대출받을 수 있나요?", "네, 가능합니다. <strong>최근 6~12개월 평균 소득</strong>을 기준으로 심사합니다. 소득이 불규칙하더라도 통장 내역이 꾸준하다면 인정받을 수 있습니다."),
            ("3.3% 원천징수 프리랜서는 어떻게 소득을 증빙하나요?", "발주처에서 발행한 <strong>3.3% 원천징수영수증</strong>이 가장 강력한 증빙 서류입니다. 이것이 없다면 종합소득세 신고서나 건강보험료 납부 내역을 활용하세요."),
            ("사업자 등록을 하면 대출에 더 유리한가요?", "일반적으로 <strong>사업자 등록 후 소득 신고 이력이 있으면 더 유리</strong>합니다. 단, 사업자 전환 시 건강보험료가 올라갈 수 있으니 세무사와 상담 후 결정하세요."),
        ],
        "ctas": [
            {"text": "프리랜서 맞춤 대출 자격 확인하기", "desc": "금융소비자포털에서 프리랜서 전용 대출 상품을 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "프리랜서 대출 상품 비교하기", "desc": "핀크에서 프리랜서 소득 인정 대출 상품을 한눈에 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "프리랜서 대출 무료 상담 받기", "desc": "토스에서 내 소득 증빙 방법으로 받을 수 있는 대출을 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 31 =====
    {
        "title": "신용불량자 대출 가능한 곳 2026 합법 방법 총정리",
        "cat": 6,
        "slug": "bad-credit-loan-options-2026",
        "intro": "<strong>신용불량자(금융채무불이행자)</strong>도 합법적인 방법으로 대출받을 수 있는 기관과 상품이 존재합니다. 불법 사금융에 손대기 전, 정부 지원 서민 금융과 합법 금융 기관을 먼저 확인하세요. 2026년 기준 신용불량자가 이용 가능한 대출 방법을 단계별로 안내합니다.",
        "sections": [
            ("신용불량자란? 기준과 현황", "<p><strong>금융채무불이행자(신용불량자)</strong>는 3개월 이상 채무를 연체하여 신용정보원에 불량 정보가 등록된 사람입니다.</p><ul><li>연체 90일 이상 → 신용정보원 등록</li><li>등록 기간: 채무 해결 후 최대 5년까지 이력 남음</li><li>신용점수: 보통 NICE 300~500점대</li></ul><p>신용불량자가 되면 일반 대출이 전면 차단되지만, 일부 서민 금융 상품은 이용 가능합니다.</p>"),
            ("신용불량자 이용 가능한 합법 대출 상품", "<table><thead><tr><th>상품</th><th>기관</th><th>금리</th><th>조건</th></tr></thead><tbody><tr><td>미소금융</td><td>서민금융진흥원</td><td>연 4.5%</td><td>취약 계층, 창업·생계 자금</td></tr><tr><td>햇살론 15</td><td>저축은행·신협</td><td>연 15.9%</td><td>소득 증빙 가능자</td></tr><tr><td>지역 신협·새마을금고</td><td>상호금융</td><td>연 10~20%</td><td>조합원 가입 후 이용</td></tr><tr><td>법원 회생 중 생계비 대출</td><td>일부 서민 금융</td><td>연 10~15%</td><td>개인회생 인가 후</td></tr></tbody></table>"),
            ("신용 회복 절차와 대출 재개 로드맵", "<ol><li><strong>채무 현황 파악</strong>: 신용정보원(allcredit.or.kr)에서 내 연체 정보 조회</li><li><strong>신용 회복 위원회 상담</strong>: 채무 조정·분할 상환 프로그램 신청</li><li><strong>채무 해결</strong>: 분할 상환 또는 협상 감면으로 채무 정리</li><li><strong>신용정보 삭제 요청</strong>: 채무 해결 후 신용정보 삭제 신청</li><li><strong>신용점수 재건</strong>: 소액 카드 사용 + 성실 납부로 점수 회복</li><li><strong>일반 대출 재개</strong>: 신용점수 600점 이상 도달 후 정책 대출 신청</li></ol>"),
            ("불법 사금융 피하는 방법", "<ul><li><strong>법정 최고 금리(연 20%) 초과</strong>하는 대출은 모두 불법입니다</li><li>SNS·문자 광고로 접근하는 대출업체는 대부분 불법 사금융입니다</li><li>합법 대부업체 확인: 금감원 금융소비자포털에서 등록 여부 조회</li><li>피해 발생 시: 불법 사금융 신고센터(1332)에 즉시 신고</li></ul>"),
            ("신용점수 빠르게 올리는 실전 방법", "<ul><li>통신비·관리비·국민연금을 신용평가에 반영 신청 (NICE·KCB 앱)</li><li>소액 체크카드 또는 신용카드로 <strong>3개월 이상 꾸준히 사용</strong>하고 전액 납부</li><li>기존 연체 채무 일부라도 상환하면 신용점수 즉시 반영</li><li>불필요한 신용 조회 최소화</li></ul>"),
        ],
        "faq": [
            ("신용불량자도 전세 자금 대출을 받을 수 있나요?", "일반 전세 대출은 불가능합니다. 채무를 해결하고 신용 회복 후 신청하거나, <strong>주거 급여(임차급여)</strong>와 같은 복지 제도를 활용하는 방법을 고려하세요."),
            ("신용 회복 위원회 채무 조정을 하면 대출에 불이익이 있나요?", "채무 조정 이력은 신용정보에 등록되어 <strong>향후 5~7년간 대출 심사에 영향</strong>을 줄 수 있습니다. 그러나 계속 연체하는 것보다는 조정을 통해 정상화하는 편이 장기적으로 훨씬 유리합니다."),
            ("신용불량 상태에서 급히 생활비가 필요하면?", "<strong>미소금융 긴급 생계 자금(100만원, 무이자)</strong> 또는 지자체 긴급복지지원제도를 신청하세요. 불법 사금융은 절대 이용하지 마세요."),
        ],
        "ctas": [
            {"text": "신용 회복 및 서민 금융 상담받기", "desc": "금융소비자포털에서 신용 회복 방법과 합법 대출을 상담받으세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "내 신용 등급에 맞는 대출 찾기", "desc": "핀크에서 신용점수별 이용 가능한 합법 대출 상품을 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "신용 회복 무료 상담 신청하기", "desc": "토스에서 신용불량 탈출을 위한 단계별 방법을 무료로 안내받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 32 =====
    {
        "title": "개인회생 중 대출 가능 여부 2026 완벽 정리",
        "cat": 6,
        "slug": "personal-rehabilitation-loan-2026",
        "intro": "<strong>개인회생</strong> 진행 중에는 대부분의 일반 대출이 제한됩니다. 그러나 생계 유지에 필요한 긴급 자금 조달 방법이 완전히 없는 것은 아닙니다. 2026년 기준 개인회생 중 대출 가능 여부, 허용되는 금융 서비스, 주의사항을 상세히 안내합니다.",
        "sections": [
            ("개인회생 중 대출이 제한되는 이유", "<p>개인회생은 법원이 채무자의 재산과 수입을 관리하는 절차입니다. 회생 중 임의로 새 채무를 지면 <strong>회생 인가 취소</strong> 사유가 될 수 있습니다.</p><ul><li>법원의 재산 처분 제한 명령</li><li>금융기관의 자체 심사에서 회생 이력 조회 차단</li><li>신용정보에 개인회생 사실 등록</li></ul>"),
            ("개인회생 중 가능한 금융 서비스", "<table><thead><tr><th>서비스</th><th>가능 여부</th><th>비고</th></tr></thead><tbody><tr><td>체크카드 발급</td><td>가능</td><td>신용카드는 불가</td></tr><tr><td>입출금 통장 개설</td><td>가능</td><td>기본 예금 서비스</td></tr><tr><td>신용카드 발급</td><td>불가</td><td>회생 기간 중 전면 차단</td></tr><tr><td>일반 신용대출</td><td>불가</td><td>은행·저축은행 모두 차단</td></tr><tr><td>미소금융 긴급 생계 자금</td><td>조건부 가능</td><td>담당 변호사·관재인 확인 필요</td></tr><tr><td>가족 차용</td><td>법원 허가 필요</td><td>법원에 사전 신청</td></tr></tbody></table>"),
            ("개인회생 중 긴급 자금이 필요할 때", "<ol><li><strong>법원 허가 받아 긴급 차용</strong>: 법원에 긴급 생활비 차용 신청서 제출</li><li><strong>가족·지인 무이자 차용</strong>: 법원 허가 후 가족에게 빌리는 방법 (증빙 보관 필수)</li><li><strong>긴급복지지원 신청</strong>: 지자체 긴급복지지원제도 활용 (대출 아닌 지원금)</li><li><strong>미소금융 상담</strong>: 서민금융진흥원(1397)에 상황 설명 후 가능 여부 확인</li></ol>"),
            ("개인회생 완료 후 대출 재개 전략", "<ul><li>회생 완료(인가 후 3~5년 상환) 후 신용정보 등록 삭제: <strong>최대 5년 이력</strong></li><li>완료 직후: 신협·새마을금고 등 소액 대출부터 시작</li><li>6~12개월 성실 상환 후: 사잇돌·햇살론 뱅크 신청 가능</li><li>2~3년 후: 1금융권 일반 신용대출 가능해질 수 있음</li></ul>"),
            ("개인회생 vs 개인파산 비교", "<table><thead><tr><th>구분</th><th>개인회생</th><th>개인파산</th></tr></thead><tbody><tr><td>수입 조건</td><td>정기 수입 있어야 함</td><td>수입 없어도 가능</td></tr><tr><td>채무 감면</td><td>일부 감면 + 3~5년 분할 상환</td><td>면책 결정 시 전액 소멸</td></tr><tr><td>기간</td><td>3~5년</td><td>1~2년</td></tr><tr><td>신용정보</td><td>5년 이력</td><td>5~7년 이력</td></tr><tr><td>재산 처분</td><td>일부 유지 가능</td><td>대부분 처분</td></tr></tbody></table>"),
        ],
        "faq": [
            ("개인회생 중 생활비가 부족하면 어떻게 하나요?", "법원에 <strong>생계비 조정 신청</strong>을 먼저 해보세요. 회생 변제금을 줄이거나 긴급 차용 허가를 받는 방법이 있습니다. 담당 변호사와 꼭 상의하세요."),
            ("개인회생 중 통장이나 체크카드는 사용할 수 있나요?", "네, 입출금 통장과 체크카드는 <strong>정상적으로 사용 가능</strong>합니다. 신용카드는 불가하며, 통장 잔액은 법원에 수입·지출 보고 대상이 됩니다."),
            ("개인회생을 하면 가족 명의 대출에도 영향이 있나요?", "개인회생은 본인의 신용 정보에만 영향을 줍니다. <strong>가족 명의 대출에는 직접적인 영향이 없습니다.</strong> 다만 연대보증인이 있다면 보증인에게 청구될 수 있습니다."),
        ],
        "ctas": [
            {"text": "개인회생·파산 무료 법률 상담", "desc": "금융소비자포털에서 개인회생 관련 무료 상담을 받으세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "신용 회복 후 이용 가능 대출 비교", "desc": "핀크에서 신용 회복 단계별 이용 가능 대출 상품을 확인하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "채무 해결 무료 상담 신청하기", "desc": "토스에서 개인회생·파산 이후 재무 재건 방법을 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 33 =====
    {
        "title": "채무통합 대출 다중채무 해결법 2026 완벽 가이드",
        "cat": 6,
        "slug": "debt-consolidation-loan-2026",
        "intro": "<strong>채무통합 대출</strong>은 여러 곳에 흩어진 고금리 대출을 하나의 저금리 대출로 통합하는 방법입니다. 월 이자 부담을 줄이고 관리를 단순화할 수 있습니다. 2026년 기준 합법적인 채무통합 방법, 이용 조건, 주의사항을 상세히 안내합니다.",
        "sections": [
            ("채무통합 대출이란?", "<p><strong>채무통합 대출(빚 통합)</strong>은 여러 금융기관의 고금리 부채를 하나의 저금리 대출로 한 번에 상환하는 방식입니다. 다중채무자의 이자 부담을 줄이고 관리 복잡성을 해소하는 데 효과적입니다.</p><ul><li>예: 카드론 4개 + 저축은행 대출 1개 → 시중은행 신용대출 1개로 통합</li><li>기대 효과: 평균 금리 인하, 월 상환액 감소, 관리 단순화</li></ul>"),
            ("채무통합 가능한 방법 비교", "<table><thead><tr><th>방법</th><th>대상</th><th>금리</th><th>특징</th></tr></thead><tbody><tr><td>1금융권 신용대출 통합</td><td>신용점수 700점 이상</td><td>연 4~8%</td><td>이자 절감 효과 최대</td></tr><tr><td>주담대 담보 통합</td><td>주택 보유자</td><td>연 3~5%</td><td>담보로 저금리 가능</td></tr><tr><td>사잇돌 대환</td><td>중신용자 (620~839점)</td><td>연 5.9~14.9%</td><td>정책 대출 활용</td></tr><tr><td>신용회복위원회 채무 조정</td><td>다중 채무자</td><td>금리 인하 협상</td><td>연체 시 유효</td></tr><tr><td>법원 개인회생</td><td>상환 불가 다중 채무자</td><td>해당 없음</td><td>채무 강제 감면</td></tr></tbody></table>"),
            ("채무통합 대출 신청 전 체크리스트", "<ul><li><strong>현재 채무 현황 파악</strong>: 총 잔액, 금리, 중도상환수수료 계산</li><li><strong>통합 후 금리 비교</strong>: 통합 대출 금리 + 수수료 vs 기존 이자 총액</li><li><strong>신용점수 확인</strong>: 낮은 신용점수로는 저금리 통합 대출이 어려움</li><li><strong>DSR 계산</strong>: 연 소득 대비 원리금 상환액이 40%(비은행 50%)를 넘으면 불가</li></ul>"),
            ("합법 vs 불법 채무통합 구분법", "<ul><li><strong>합법 채무통합</strong>: 은행·저축은행·신협·서민금융 상품, 신용회복위원회</li><li><strong>불법 채무통합</strong>: SNS 광고로 접근하는 업체, 선불 수수료 요구, 등록되지 않은 대부업체</li><li>합법 대부업체 확인: 금감원 파인(fine.fss.or.kr)에서 등록 여부 조회</li><li>불법 피해 신고: 금융감독원(1332)</li></ul>"),
            ("채무통합 대출 절약 효과 계산 예시", "<table><thead><tr><th>구분</th><th>통합 전</th><th>통합 후</th><th>연간 절감</th></tr></thead><tbody><tr><td>총 잔액 3,000만원</td><td>평균 금리 18%</td><td>금리 8%</td><td>약 300만원</td></tr><tr><td>총 잔액 5,000만원</td><td>평균 금리 15%</td><td>금리 6%</td><td>약 450만원</td></tr></tbody></table>"),
        ],
        "faq": [
            ("채무통합을 하면 신용점수가 올라가나요?", "단순히 통합한다고 신용점수가 오르지는 않습니다. 그러나 <strong>성실하게 상환하면서 기존 고금리 채무가 줄어들면</strong> 시간이 지남에 따라 신용점수가 개선됩니다."),
            ("채무통합 대출 신청 시 중도상환수수료는 어떻게 되나요?", "기존 대출을 상환할 때 <strong>중도상환수수료(보통 0.5~1.5%)</strong>가 발생할 수 있습니다. 수수료가 이자 절감액보다 크다면 통합이 불리합니다. 반드시 계산 후 결정하세요."),
            ("연체 중에도 채무통합 대출을 받을 수 있나요?", "현재 연체 중이면 일반 대출로는 통합이 어렵습니다. 이 경우 <strong>신용회복위원회(채무 조정)</strong>나 법원 개인회생 절차를 통해 채무를 정리하는 것이 현실적입니다."),
        ],
        "ctas": [
            {"text": "채무 조정 무료 상담 신청하기", "desc": "신용회복위원회 또는 금융소비자포털에서 채무 통합 방법을 상담받으세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "채무통합 대출 상품 비교하기", "desc": "핀크에서 채무통합에 적합한 저금리 대출 상품을 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "다중채무 해결 무료 상담 받기", "desc": "토스에서 내 채무 상황에 맞는 통합 방법을 무료로 안내받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 34 =====
    {
        "title": "스트레스 DSR 계산법 2026 완벽 가이드",
        "cat": 6,
        "slug": "stress-dsr-calculation-guide-2026",
        "intro": "<strong>스트레스 DSR</strong>은 금리 인상 위험을 감안한 강화된 대출 한도 규제입니다. 2024년부터 단계적으로 도입되어 2026년에는 전면 적용됩니다. 내 대출 한도가 갑자기 줄어든 이유가 스트레스 DSR 때문일 수 있습니다. 계산법과 대응 전략을 상세히 안내합니다.",
        "sections": [
            ("스트레스 DSR이란?", "<p><strong>DSR(총부채원리금상환비율)</strong>은 연소득 대비 연간 원리금 상환액의 비율입니다. <strong>스트레스 DSR</strong>은 여기에 금리 인상 가능성(스트레스 금리)을 추가로 반영한 강화 규제입니다.</p><ul><li>일반 DSR: 실제 적용 금리 기준</li><li>스트레스 DSR: 실제 금리 + 스트레스 금리(0.75~1.5%p) 기준</li><li>목적: 금리 상승 시 채무 불이행 방지</li></ul>"),
            ("2026년 스트레스 DSR 규제 현황", "<table><thead><tr><th>적용 단계</th><th>시기</th><th>대상</th><th>스트레스 금리</th></tr></thead><tbody><tr><td>1단계</td><td>2024년 2월~</td><td>은행권 주담대</td><td>0.75%p</td></tr><tr><td>2단계</td><td>2024년 9월~</td><td>은행권 전체 + 2금융권 주담대</td><td>1.2%p</td></tr><tr><td>3단계</td><td>2025년 7월~</td><td>전 금융권</td><td>1.5%p</td></tr></tbody></table><p>2026년 현재는 <strong>3단계 전면 적용</strong> 중입니다.</p>"),
            ("스트레스 DSR 계산 방법", "<p><strong>기본 DSR 공식:</strong></p><p>DSR = 연간 원리금 상환액 ÷ 연소득 × 100</p><p><strong>스트레스 DSR 계산 예시:</strong></p><ul><li>연소득: 6,000만원</li><li>DSR 한도: 40%</li><li>실제 대출 금리: 4.0%</li><li>스트레스 금리 추가: +1.5%p → 5.5% 기준으로 한도 계산</li><li>30년 원리금균등, 연 5.5% 적용 시 → 한도 약 <strong>4억 2천만원</strong></li><li>같은 조건에서 스트레스 없이 4.0% 적용 시 → 한도 약 <strong>5억원</strong></li></ul>"),
            ("스트레스 DSR로 줄어드는 대출 한도 예시", "<table><thead><tr><th>연소득</th><th>스트레스 전 한도</th><th>스트레스 후 한도(1.5%p 가산)</th><th>감소액</th></tr></thead><tbody><tr><td>5,000만원</td><td>약 4.2억원</td><td>약 3.5억원</td><td>약 7,000만원</td></tr><tr><td>7,000만원</td><td>약 5.9억원</td><td>약 4.9억원</td><td>약 1억원</td></tr><tr><td>1억원</td><td>약 8.4억원</td><td>약 7억원</td><td>약 1.4억원</td></tr></tbody></table>"),
            ("스트레스 DSR 대응 전략", "<ul><li><strong>고정 금리 선택</strong>: 변동금리보다 고정금리에 스트레스 금리를 낮게 적용하는 경우가 있습니다</li><li><strong>소득 증빙 강화</strong>: 근로소득 외 사업소득·임대소득 합산 신고로 인정 소득 높이기</li><li><strong>기존 부채 상환</strong>: DSR에 합산되는 기존 대출을 미리 줄여 여유 한도 확보</li><li><strong>대출 기간 연장</strong>: 상환 기간을 늘리면 연간 원리금이 줄어 DSR 여유가 생깁니다 (이자 총액은 증가)</li></ul>"),
        ],
        "faq": [
            ("스트레스 DSR 때문에 대출 한도가 얼마나 줄어드나요?", "연소득 6,000만원 기준으로 주담대 한도가 <strong>약 5,000~8,000만원 감소</strong>하는 경우가 일반적입니다. 금리 수준과 대출 기간에 따라 크게 달라집니다."),
            ("고정금리 대출은 스트레스 DSR 적용이 다른가요?", "네, 고정금리 대출은 변동 위험이 낮아 스트레스 금리를 <strong>더 낮게(0.75%p) 적용</strong>하는 경우가 있습니다. 고정금리 선택이 한도 면에서 유리할 수 있습니다."),
            ("2금융권 대출도 스트레스 DSR 적용을 받나요?", "2025년 7월 3단계 시행 이후 <strong>저축은행·카드사·캐피탈 등 2금융권도 전면 적용</strong>됩니다. 2026년 현재 예외 없이 적용됩니다."),
        ],
        "ctas": [
            {"text": "내 DSR 한도 계산해보기", "desc": "금융소비자포털에서 내 대출 가능 한도를 계산해보세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "DSR 고려한 최적 대출 상품 찾기", "desc": "핀크에서 스트레스 DSR 기준 내 이용 가능한 대출을 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "대출 한도 무료 상담 신청하기", "desc": "토스에서 스트레스 DSR 고려한 최적 대출 한도를 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 35 =====
    {
        "title": "청년 전용 버팀목 전세 대출 조건 한도 금리 2026",
        "cat": 6,
        "slug": "youth-jeonse-loan-guide-2026",
        "intro": "<strong>청년 전용 버팀목 전세 대출</strong>은 만 19~34세 청년이 전세 보증금을 마련할 수 있도록 정부가 연 1.5~2.7%의 초저금리로 지원하는 정책 상품입니다. 2026년 기준 청년 버팀목의 자격 조건, 한도, 금리, 신청 방법을 상세히 정리했습니다.",
        "sections": [
            ("청년 전용 버팀목 전세 대출이란?", "<p><strong>청년 전용 버팀목 전세 대출</strong>은 주택도시기금(HUG)이 공급하고 우리·국민·신한·하나·농협·기업·부산은행 등에서 취급하는 청년 특화 전세 자금 대출입니다.</p><ul><li>대상: 만 19~34세 무주택 단독 세대주</li><li>금리: 연 1.5~2.7% (소득 구간별)</li><li>최대 한도: 3억원</li></ul>"),
            ("2026년 청년 버팀목 자격 조건", "<table><thead><tr><th>구분</th><th>조건</th></tr></thead><tbody><tr><td>나이</td><td>만 19~34세 (신청일 기준)</td></tr><tr><td>세대 구성</td><td>단독 세대주 또는 예비 세대주</td></tr><tr><td>주택 보유</td><td>무주택자</td></tr><tr><td>연소득</td><td>5,000만원 이하 (부부 합산 6,000만원)</td></tr><tr><td>순자산</td><td>3.45억원 이하</td></tr><tr><td>보증금</td><td>수도권 3억원·지방 2억원 이하 전세</td></tr></tbody></table>"),
            ("소득 구간별 금리표", "<table><thead><tr><th>연소득</th><th>기본 금리</th></tr></thead><tbody><tr><td>2,000만원 이하</td><td>연 1.5%</td></tr><tr><td>2,000~4,000만원</td><td>연 1.8%</td></tr><tr><td>4,000~6,000만원</td><td>연 2.1%</td></tr><tr><td>우대 금리 추가 적용 시</td><td>최저 연 1.2%까지 가능</td></tr></tbody></table><h3>우대 금리 항목 (각 0.1~0.3%p)</h3><ul><li>부동산 전자계약 체결: -0.1%p</li><li>주거안정 월세 대출 성실 상환: -0.1%p</li><li>다자녀 가구: -0.5%p</li></ul>"),
            ("신청 방법 및 필요 서류", "<ol><li>전세 계약서 작성 (잔금일 전)</li><li>취급 은행 방문 또는 앱 신청 (일부 비대면 가능)</li><li>주택도시기금 보증 심사</li><li>대출 실행</li></ol><h3>필요 서류</h3><ul><li>신분증, 주민등록등본</li><li>전세계약서</li><li>소득 증빙: 원천징수영수증 또는 건강보험료 납부 확인서</li><li>무주택 확인서 (등기부등본)</li></ul>"),
            ("청년 버팀목 vs 일반 버팀목 비교", "<table><thead><tr><th>구분</th><th>청년 전용 버팀목</th><th>일반 버팀목</th></tr></thead><tbody><tr><td>나이 조건</td><td>만 19~34세</td><td>제한 없음</td></tr><tr><td>최저 금리</td><td>연 1.5%</td><td>연 2.1%</td></tr><tr><td>최대 한도</td><td>3억원</td><td>수도권 3억/지방 2억</td></tr><tr><td>소득 기준</td><td>5,000만원 이하</td><td>5,000만원 이하</td></tr></tbody></table>"),
        ],
        "faq": [
            ("취업 준비 중인 청년도 청년 버팀목을 받을 수 있나요?", "소득이 없어도 신청 가능하지만, 소득 증빙이 없으면 <strong>건강보험 피부양자 자격 증명서</strong> 등으로 대체할 수 있습니다. 다만 소득이 없으면 한도와 심사에 영향이 있을 수 있습니다."),
            ("청년 버팀목은 전세 계약 후 언제까지 신청해야 하나요?", "전세 계약 <strong>잔금일 전</strong>까지 신청 접수가 완료되어야 합니다. 계약 후 최소 2~4주 전에 신청하는 것이 안전합니다."),
            ("기존 버팀목 대출을 청년 전용으로 갈아탈 수 있나요?", "일반 버팀목을 이용 중인 경우 <strong>만기 도래 시 청년 전용으로 갱신 신청</strong>이 가능합니다. 나이·소득 조건을 충족해야 합니다."),
        ],
        "ctas": [
            {"text": "청년 버팀목 전세 대출 신청하기", "desc": "주택도시기금에서 청년 전용 전세 대출 자격을 확인하세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "청년 전세 대출 금리 비교하기", "desc": "핀크에서 청년 맞춤 전세 대출 상품을 한눈에 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "청년 주거 금융 무료 상담 받기", "desc": "토스에서 청년 전용 전세·주거 금융 상품을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 36 =====
    {
        "title": "신혼부부 주택 구입 대출 총정리 2026 완벽 가이드",
        "cat": 6,
        "slug": "newlywed-home-purchase-loan-2026",
        "intro": "<strong>신혼부부 주택 구입 대출</strong>은 혼인 7년 이내 신혼부부에게 더 낮은 금리와 높은 한도를 제공하는 특례 모기지 상품입니다. 신생아 특례, 디딤돌, 보금자리론 등 다양한 정책 상품을 비교해 가장 유리한 선택을 하세요. 2026년 기준 신혼부부 대출 옵션을 모두 정리했습니다.",
        "sections": [
            ("신혼부부 주택 대출 주요 상품 비교", "<table><thead><tr><th>상품명</th><th>금리</th><th>최대 한도</th><th>소득 기준</th></tr></thead><tbody><tr><td>신생아 특례 구입 자금</td><td>연 1.6~3.3%</td><td>5억원</td><td>부부 합산 1.3억 이하</td></tr><tr><td>디딤돌 대출(신혼 우대)</td><td>연 2.35~3.65%</td><td>4억원</td><td>부부 합산 6,000만원 이하</td></tr><tr><td>보금자리론(신혼 우대)</td><td>연 3.65~4.25%</td><td>5억원</td><td>제한 없음(우대 7,000만원)</td></tr><tr><td>특례 보금자리론(한시)</td><td>연 3.25~3.95%</td><td>5억원</td><td>소득 무관</td></tr></tbody></table>"),
            ("신생아 특례 구입 자금 상세", "<p><strong>신생아 특례 구입 자금</strong>은 2023년 이후 출산한 가구를 위한 최저 금리 상품입니다.</p><ul><li>자격: 대출 신청일 기준 2년 내 출산한 무주택 가구</li><li>금리: 연 1.6~3.3% (소득·만기별)</li><li>최대 한도: 5억원</li><li>주택 가격: 9억원 이하</li><li>소득: 부부 합산 1.3억원 이하</li><li>추가 혜택: 자녀 1명 추가 출산 시 0.2%p 금리 인하</li></ul>"),
            ("디딤돌 대출 신혼 우대 조건", "<ul><li><strong>대상</strong>: 혼인 7년 이내 또는 3개월 내 결혼 예정인 무주택 세대주</li><li><strong>금리</strong>: 일반 대비 0.1~0.2%p 우대</li><li><strong>한도</strong>: 최대 4억원 (LTV 70%)</li><li><strong>소득</strong>: 부부 합산 6,000만원 이하 (신혼 7,000만원)</li><li><strong>주택 가격</strong>: 5억원 이하 (수도권 6억원)</li></ul>"),
            ("신혼부부 대출 신청 전 체크리스트", "<ul><li>혼인신고일 확인 (7년 이내 여부)</li><li>부부 합산 연소득 계산 (세전 기준)</li><li>무주택 여부 확인 (배우자 포함)</li><li>구입 예정 주택 가격 및 위치 확인</li><li>기존 대출 현황 파악 (DSR 여유 계산)</li><li>전입신고 계획 확인 (실거주 요건)</li></ul>"),
            ("신혼부부 대출 활용 전략", "<ul><li>출산 계획이 있다면 <strong>신생아 특례 구입 자금</strong>이 가장 유리합니다</li><li>소득이 6,000만원 이하라면 <strong>디딤돌 신혼 우대</strong>로 시작하세요</li><li>소득이 높아 정책 대출이 안 된다면 <strong>보금자리론 신혼 우대</strong> 검토</li><li>시중은행 혼합금리 상품과 비교해 최적 선택</li></ul>"),
        ],
        "faq": [
            ("결혼 전에도 신혼부부 대출을 신청할 수 있나요?", "디딤돌·버팀목의 경우 <strong>3개월 이내 결혼 예정</strong>이면 신청 가능합니다. 단, 대출 실행 전까지 혼인신고를 마쳐야 합니다."),
            ("신생아 특례 대출 대상 자녀의 나이 기준은?", "대출 신청일 기준 <strong>2세 미만(만 2세 이하)</strong> 자녀가 있어야 합니다. 2023년 1월 1일 이후 출생아부터 해당됩니다."),
            ("신혼부부 대출 후 추가 출산 시 혜택은?", "신생아 특례 구입 자금은 <strong>추가 출산 1명당 0.2%p 금리 인하</strong>, 만기 연장 혜택이 있습니다. 디딤돌도 추가 자녀 우대 금리가 적용됩니다."),
        ],
        "ctas": [
            {"text": "신혼부부 주택 구입 자금 신청하기", "desc": "주택도시기금에서 신혼부부 특화 구입 자금 자격을 확인하세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "신혼부부 대출 상품 비교하기", "desc": "핀크에서 신혼부부 맞춤 주택 대출 상품을 한눈에 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "신혼부부 주거 금융 무료 상담", "desc": "토스에서 신혼부부를 위한 최적 주택 대출 방법을 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 37 =====
    {
        "title": "빌라 다세대 담보대출 조건 한도 2026 완벽 정리",
        "cat": 6,
        "slug": "villa-multiplex-mortgage-2026",
        "intro": "<strong>빌라·다세대 담보대출</strong>은 아파트에 비해 조건이 까다롭고 한도도 낮습니다. 전세 사기 이후 은행들이 빌라 담보 심사를 더욱 강화했습니다. 2026년 기준 빌라·다세대 담보대출을 받는 방법, 가능한 기관, 주의사항을 상세히 안내합니다.",
        "sections": [
            ("빌라·다세대 담보대출이 어려운 이유", "<ul><li><strong>가격 산정 어려움</strong>: 아파트와 달리 실거래가 비교가 어렵고 감정가 산정이 주관적</li><li><strong>전세 사기 여파</strong>: 2022~2023년 전세 사기 이후 은행들이 빌라 담보 대출 심사 대폭 강화</li><li><strong>유동성 부족</strong>: 아파트 대비 매각 유동성이 낮아 담보 가치 인정 낮음</li><li><strong>LTV 제한</strong>: 일반적으로 감정가의 60~70%만 인정</li></ul>"),
            ("빌라·다세대 담보대출 가능한 기관", "<table><thead><tr><th>기관</th><th>LTV</th><th>금리</th><th>특징</th></tr></thead><tbody><tr><td>시중은행</td><td>60~70%</td><td>연 4~6%</td><td>심사 까다로움</td></tr><tr><td>저축은행</td><td>50~65%</td><td>연 6~12%</td><td>상대적으로 승인 쉬움</td></tr><tr><td>신협·새마을금고</td><td>60~70%</td><td>연 5~9%</td><td>지역 조합원 우대</td></tr><tr><td>캐피탈·보험사</td><td>50~60%</td><td>연 8~15%</td><td>부동산담보신탁 활용</td></tr></tbody></table>"),
            ("빌라 담보대출 심사 강화 항목", "<ul><li><strong>전세 세입자 유무</strong>: 임차인이 있으면 배당 순위 문제로 한도 축소</li><li><strong>건물 노후도</strong>: 준공 30년 이상 노후 건물은 담보 인정 비율 추가 감소</li><li><strong>등기 현황</strong>: 선순위 근저당·가압류 여부 필수 확인</li><li><strong>불법 건축물 여부</strong>: 불법 증축 등은 담보 거절 사유</li><li><strong>위치 및 가격 흐름</strong>: 하락 지역 빌라는 더욱 엄격히 심사</li></ul>"),
            ("빌라 담보대출 한도 높이는 방법", "<ul><li><strong>임차인 퇴거 후 신청</strong>: 빈 집 상태로 신청하면 선순위 임차 보증금 미공제</li><li><strong>신탁 등기 활용</strong>: 부동산담보신탁 방식으로 한도 상향 가능</li><li><strong>감정 평가 기관 선택</strong>: 여러 기관의 감정가를 비교해 높은 쪽 선택 (기관에 문의)</li><li><strong>추가 담보 제공</strong>: 다른 부동산이나 예금을 추가 담보로 제공</li></ul>"),
            ("빌라 담보대출 주의사항", "<ul><li>깡통전세 여부를 반드시 확인하세요 (전세 보증금 > 담보 가치면 위험)</li><li>등기부등본에서 선순위 채권, 가압류, 가등기를 꼭 확인하세요</li><li>전세 사기 위험 지역의 빌라는 담보 대출 자체를 재고하세요</li><li>불법 전세 사기 피해 시 전세피해지원센터(☎1533-8119)에 문의하세요</li></ul>"),
        ],
        "faq": [
            ("빌라 담보대출 LTV가 아파트보다 낮은 이유는?", "빌라는 아파트에 비해 <strong>처분 유동성과 가격 투명성</strong>이 낮아 은행이 담보 가치를 보수적으로 평가합니다. 전세 사기 위험이 더해지면서 2026년 현재 LTV 기준이 더욱 강화되어 있습니다."),
            ("선순위 임차인이 있을 때 빌라 담보대출 한도는?", "선순위 임차 보증금은 담보 가치에서 차감됩니다. 예를 들어 감정가 2억원, LTV 70%=1.4억원인데 선순위 전세 8,000만원이 있다면 실제 대출 가능 금액은 <strong>최대 6,000만원</strong>으로 크게 줄어듭니다."),
            ("빌라 담보대출 거절 후 다른 방법은?", "저축은행·신협·새마을금고를 추가로 시도하거나, <strong>부동산 담보신탁 대출</strong> 방식을 검토해보세요. 금리는 높아지지만 승인 가능성이 높아집니다."),
        ],
        "ctas": [
            {"text": "빌라 담보대출 조건 확인하기", "desc": "금융소비자포털에서 빌라·다세대 담보대출 가능 상품을 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "빌라 담보대출 상품 비교하기", "desc": "핀크에서 빌라·다세대 담보 대출 상품을 한눈에 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "빌라 담보대출 무료 상담 받기", "desc": "토스에서 내 빌라 담보 가치 및 대출 가능 한도를 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 38 =====
    {
        "title": "상가 오피스텔 임대 대출 비교 2026 완벽 가이드",
        "cat": 6,
        "slug": "commercial-property-loan-2026",
        "intro": "<strong>상가·오피스텔 담보대출</strong>은 주택 담보 대출과 다른 별도 규제를 적용받습니다. LTV가 주택보다 낮고 금리도 높지만, 임대 수익을 레버리지로 활용하는 투자 전략으로 많이 이용됩니다. 2026년 기준 상가·오피스텔 대출 조건, 금리, 주의사항을 비교 정리했습니다.",
        "sections": [
            ("상가·오피스텔 대출 기본 조건", "<table><thead><tr><th>구분</th><th>상가</th><th>오피스텔(업무용)</th><th>오피스텔(주거용)</th></tr></thead><tbody><tr><td>LTV</td><td>50~70%</td><td>50~70%</td><td>60~70%</td></tr><tr><td>금리</td><td>연 4.5~8%</td><td>연 4~7%</td><td>연 4~6.5%</td></tr><tr><td>DSR 적용</td><td>적용</td><td>적용</td><td>적용</td></tr><tr><td>주택 수 포함</td><td>해당 없음</td><td>주거용이면 포함</td><td>포함</td></tr></tbody></table>"),
            ("상가 담보대출 특징 및 주의사항", "<ul><li><strong>임대 수익 반영</strong>: 임대 수입을 소득으로 인정하여 DSR 여유 확보 가능</li><li><strong>공실 위험</strong>: 공실 중이면 임대 소득 불인정으로 한도 감소</li><li><strong>업종 제한</strong>: 유흥업소·성인업소 등 일부 업종은 담보 대출 거절 사유</li><li><strong>건물 노후도</strong>: 30년 이상 노후 건물은 담보 인정 비율 추가 감소</li><li><strong>권리 분석</strong>: 임차인의 상가임대차보호법 상 권리를 반드시 확인</li></ul>"),
            ("오피스텔 담보대출 주거용 vs 업무용", "<table><thead><tr><th>구분</th><th>주거용 오피스텔</th><th>업무용 오피스텔</th></tr></thead><tbody><tr><td>주택 수 포함</td><td>포함 (다주택 규제 적용)</td><td>미포함</td></tr><tr><td>LTV</td><td>60~70%</td><td>50~70%</td></tr><tr><td>취득세</td><td>주택 취득세율 적용</td><td>4.6%</td></tr><tr><td>임대 수입</td><td>주거 임대 수입</td><td>업무 임대 수입</td></tr></tbody></table><p>오피스텔을 주거용으로 사용 중이라면 <strong>주택 수에 포함</strong>되어 다주택자 규제를 받을 수 있습니다.</p>"),
            ("상가·오피스텔 대출 절차", "<ol><li>물건 선택 후 등기부등본·건축물대장 확인</li><li>은행 또는 저축은행에 사전 상담</li><li>감정평가 의뢰 (은행 지정 감정사)</li><li>대출 심사 및 승인</li><li>근저당권 설정 후 대출 실행</li></ol><h3>필요 서류</h3><ul><li>신분증, 등기부등본, 건축물대장</li><li>임대차계약서 (임차인 있는 경우)</li><li>소득 증빙, 사업소득 서류</li></ul>"),
            ("상가·오피스텔 투자 수익률 계산", "<p>투자 전 <strong>실질 수익률</strong>을 계산해보세요.</p><ul><li>연 임대 수입 ÷ 투자 총액 × 100 = 총 수익률</li><li>총 수익률 - 대출 이자율 = 레버리지 효과</li></ul><h3>예시</h3><table><thead><tr><th>구분</th><th>내용</th></tr></thead><tbody><tr><td>매입가</td><td>3억원</td></tr><tr><td>대출</td><td>2억원, 연 5%</td></tr><tr><td>연 임대 수입</td><td>1,800만원 (수익률 6%)</td></tr><tr><td>연 이자</td><td>1,000만원</td></tr><tr><td>실질 수익</td><td>800만원 (자기자본 1억 기준 8%)</td></tr></tbody></table>"),
        ],
        "faq": [
            ("오피스텔을 주거용으로 사용해도 업무용 대출을 받을 수 있나요?", "대출 신청 시 용도를 업무용으로 신청할 수 있지만, 실제 주거 사용이 확인되면 <strong>주택 담보 대출 규제가 적용</strong>될 수 있습니다. 취득세·세금도 달라지므로 주의가 필요합니다."),
            ("상가 공실 상태에서도 담보대출이 가능한가요?", "가능합니다. 다만 <strong>임대 수입을 소득으로 인정받지 못해</strong> DSR 여유가 줄어들고 한도가 낮아집니다. 공실 해소 후 한도 재심사를 요청하는 것이 유리합니다."),
            ("상가 담보대출 중도상환수수료는 얼마나 되나요?", "보통 대출 실행 후 3년 이내 상환 시 <strong>잔액의 0.6~1.5%</strong>가 수수료로 부과됩니다. 3년 이후에는 수수료 없이 상환 가능한 경우가 많습니다."),
        ],
        "ctas": [
            {"text": "상가·오피스텔 대출 조건 확인하기", "desc": "금융소비자포털에서 상업용 부동산 담보 대출 상품을 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "상업용 부동산 대출 상품 비교", "desc": "핀크에서 상가·오피스텔 담보 대출 금리를 한눈에 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "상업용 부동산 대출 무료 상담", "desc": "토스에서 상가·오피스텔 투자 대출 최적 조건을 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 39 =====
    {
        "title": "대출 이자 줄이는 방법 금리 협상 전략 2026",
        "cat": 6,
        "slug": "reduce-loan-interest-tips-2026",
        "intro": "<strong>대출 이자를 줄이는 가장 효과적인 방법</strong>은 금리 협상과 갈아타기입니다. 많은 사람들이 모르고 지나치는 금리 우대 혜택과 협상 전략만 알아도 연간 수십~수백만원을 절약할 수 있습니다. 2026년 기준 금리 협상 방법, 우대 금리 활용법, 대환 전략을 단계별로 안내합니다.",
        "sections": [
            ("금리 협상이 가능한 이유", "<p>대출 금리는 <strong>기준금리 + 가산금리 - 우대금리</strong>로 결정됩니다. 가산금리와 우대금리는 은행이 재량으로 조정할 수 있어 협상의 여지가 있습니다.</p><ul><li>기준금리: COFIX, 금융채 등 시장 기준 (변경 불가)</li><li>가산금리: 은행 자체 설정 (협상 가능)</li><li>우대금리: 조건 충족 시 차감 (적극 활용)</li></ul>"),
            ("금리 협상 실전 전략", "<ol><li><strong>타 은행 대출 견적 받기</strong>: 경쟁 은행의 제안서를 받아 현재 거래 은행에 제시하면 협상력이 높아집니다</li><li><strong>우대 금리 항목 전부 확인</strong>: 급여 이체, 카드 실적, 자동이체 설정 등 우대 조건을 모두 충족하세요</li><li><strong>신용점수 올리기</strong>: 신용점수 50점 상승만으로도 0.2~0.5%p 금리 인하 가능</li><li><strong>PB(자산관리) 채널 활용</strong>: 고액 자산가 전용 PB 서비스 이용 시 추가 금리 우대</li><li><strong>금리 인하 요구권 행사</strong>: 신용 상태 개선 시 공식 금리 인하 요구 가능</li></ol>"),
            ("금리 인하 요구권 사용 방법", "<p><strong>금리 인하 요구권</strong>은 법적으로 보장된 권리입니다. 신용 상태가 개선됐다면 반드시 사용하세요.</p><ul><li>신용점수 상승 시</li><li>소득 증가 (이직·승진·부업 소득 발생) 시</li><li>기존 대출 일부 상환으로 DTI 개선 시</li></ul><h3>신청 방법</h3><ol><li>은행 앱 또는 영업점에서 금리 인하 요구 신청</li><li>소득·신용 개선 서류 제출</li><li>은행 심사 후 결과 통보 (보통 10~20일)</li></ol>"),
            ("대환대출로 이자 줄이기", "<table><thead><tr><th>방법</th><th>이자 절감 효과</th><th>주의사항</th></tr></thead><tbody><tr><td>1금융권으로 갈아타기</td><td>연 2~5%p 절감</td><td>신용점수 700점 이상 필요</td></tr><tr><td>정책 대출로 갈아타기</td><td>연 1~3%p 절감</td><td>소득·자산 조건 충족</td></tr><tr><td>장기·고정금리로 전환</td><td>금리 안정 효과</td><td>중도상환수수료 확인</td></tr></tbody></table>"),
            ("연간 이자 절감 효과 계산 예시", "<table><thead><tr><th>대출 잔액</th><th>금리 인하폭</th><th>연간 절감액</th></tr></thead><tbody><tr><td>1억원</td><td>0.5%p</td><td>약 50만원</td></tr><tr><td>3억원</td><td>1%p</td><td>약 300만원</td></tr><tr><td>5억원</td><td>1.5%p</td><td>약 750만원</td></tr></tbody></table>"),
        ],
        "faq": [
            ("금리 인하 요구권을 행사하면 무조건 금리가 내려가나요?", "아닙니다. 은행이 심사 후 거절할 수 있습니다. 그러나 <strong>신용점수 상승이나 소득 증가 등 명확한 개선이 있다면</strong> 수락될 가능성이 높습니다. 거절되더라도 재신청이 가능합니다."),
            ("타 은행 견적서 없이도 금리 협상이 되나요?", "가능하지만 협상력이 약해집니다. <strong>핀다·카카오페이·토스 앱에서 무료로 여러 은행 금리를 비교</strong>한 뒤 현재 거래 은행에 제시하는 것이 가장 효과적입니다."),
            ("대출 갈아타기 시 중도상환수수료는 어떻게 되나요?", "보통 대출 실행 후 3년 이내 상환 시 잔액의 <strong>0.6~1.5% 수수료</strong>가 발생합니다. 수수료 금액이 이자 절감액보다 작을 때만 갈아타기가 유리합니다."),
        ],
        "ctas": [
            {"text": "금리 인하 요구권 행사 방법 확인", "desc": "금융소비자포털에서 금리 인하 요구권 행사 방법을 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "내 대출 금리 경쟁 견적 받기", "desc": "핀크에서 현재 대출보다 낮은 금리 상품을 무료로 비교해보세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "대출 이자 절감 무료 상담 받기", "desc": "토스에서 내 대출 이자를 줄일 수 있는 방법을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 40 =====
    {
        "title": "원금균등 vs 원리금균등 상환 비교 2026 어떤 것이 유리할까",
        "cat": 6,
        "slug": "principal-vs-equal-payment-2026",
        "intro": "<strong>원금균등 상환과 원리금균등 상환</strong>은 대출 상환 방식의 두 가지 기본 유형입니다. 선택에 따라 총 이자 부담, 월 상환액, 재정 계획이 크게 달라집니다. 내 상황에 맞는 상환 방식을 선택하는 방법을 2026년 기준으로 상세히 안내합니다.",
        "sections": [
            ("두 가지 상환 방식 핵심 차이", "<table><thead><tr><th>구분</th><th>원금균등 상환</th><th>원리금균등 상환</th></tr></thead><tbody><tr><td>개념</td><td>원금을 매달 동일하게 상환, 이자는 줄어듦</td><td>원금+이자 합계를 매달 동일하게 상환</td></tr><tr><td>초기 월 납부액</td><td>높음</td><td>낮음</td></tr><tr><td>말기 월 납부액</td><td>낮음</td><td>동일</td></tr><tr><td>총 이자 부담</td><td>적음</td><td>많음</td></tr><tr><td>부담 시기</td><td>초기에 집중</td><td>균등 분산</td></tr></tbody></table>"),
            ("수치 비교 예시 (1억원, 연 5%, 20년)", "<table><thead><tr><th>구분</th><th>원금균등</th><th>원리금균등</th></tr></thead><tbody><tr><td>첫 달 납부액</td><td>약 833,333원 + 이자 = 약 125만원</td><td>약 66만원</td></tr><tr><td>마지막 달 납부액</td><td>약 83만원</td><td>약 66만원</td></tr><tr><td>총 납부 이자</td><td>약 2,525만원</td><td>약 2,840만원</td></tr><tr><td>총 이자 차이</td><td colspan=\"2\">약 315만원 절약 (원금균등 유리)</td></tr></tbody></table>"),
            ("어떤 상황에서 어떤 방식이 유리한가", "<h3>원금균등 상환이 유리한 경우</h3><ul><li>초기에 소득이 충분하고 총 이자를 줄이고 싶을 때</li><li>대출 기간이 길수록 절감 효과가 커집니다</li><li>조기 상환 가능성이 높은 경우</li></ul><h3>원리금균등 상환이 유리한 경우</h3><ul><li>초기 월 부담을 최소화해야 할 때</li><li>현금 흐름이 빡빡한 신혼·첫 주택 구입자</li><li>매달 일정한 납부액으로 재정 계획을 세우고 싶을 때</li></ul>"),
            ("만기일시상환 방식도 있다", "<p><strong>만기일시상환</strong>은 대출 기간 동안 이자만 납부하다가 만기에 원금을 전액 상환하는 방식입니다.</p><ul><li>월 납부액이 가장 낮음 (이자만 납부)</li><li>총 이자 부담이 가장 높음</li><li>주로 투자용 대출, 단기 자금 조달에 사용</li><li>만기 시 원금 마련 계획 필수</li></ul>"),
            ("상환 방식 선택 시 체크리스트", "<ul><li>현재 월 소득 대비 납부 여력 계산</li><li>향후 소득 증가 가능성 고려</li><li>총 이자 절감 vs 초기 부담 경감 트레이드오프 계산</li><li>중도 상환 계획 여부 (있다면 원금균등이 더 유리)</li><li>대출 만기 이후 재정 계획 수립</li></ul>"),
        ],
        "faq": [
            ("상환 방식은 대출 실행 후에 바꿀 수 있나요?", "대부분의 경우 대출 실행 후 상환 방식 변경이 어렵습니다. <strong>대환대출(갈아타기)</strong>을 통해 상환 방식을 바꾸는 방법이 있지만 중도상환수수료가 발생할 수 있습니다."),
            ("원금균등 상환에서 초기 이자가 높은 이유는?", "처음에는 원금 잔액이 최대이므로 이자 계산 기준이 됩니다. <strong>잔액 × 월 이자율</strong>로 계산되기 때문에 원금이 줄어들수록 이자도 감소합니다."),
            ("전세 대출처럼 단기 대출도 원리금균등 상환인가요?", "전세 대출은 대부분 <strong>만기일시상환 방식</strong>으로 계약 기간 중 이자만 납부하고 만기(전세 계약 종료)에 보증금으로 원금을 상환합니다."),
        ],
        "ctas": [
            {"text": "대출 상환 방식 시뮬레이션 해보기", "desc": "금융소비자포털에서 상환 방식별 이자 비교를 해보세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "내 상황에 맞는 대출 상품 찾기", "desc": "핀크에서 상환 방식별 최적 대출 상품을 비교해보세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "대출 상환 전략 무료 상담 받기", "desc": "토스에서 내 재정 상황에 맞는 최적 상환 방식을 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 41 =====
    {
        "title": "국민은행 주담대 금리 조건 2026 최신 정리",
        "cat": 6,
        "slug": "kb-bank-mortgage-rate-2026",
        "intro": "<strong>국민은행(KB) 주택담보대출</strong>은 국내 최대 시중은행의 대표 주담대 상품입니다. 고정금리, 혼합금리, 변동금리 등 다양한 선택지와 함께 KB 스타클럽 등 우대 혜택도 풍부합니다. 2026년 기준 국민은행 주담대 금리, 조건, 한도를 상세히 정리했습니다.",
        "sections": [
            ("2026년 국민은행 주담대 금리 현황", "<table><thead><tr><th>상품</th><th>금리 유형</th><th>금리 범위</th><th>특징</th></tr></thead><tbody><tr><td>KB 주택담보대출</td><td>변동금리</td><td>연 3.8~5.5%</td><td>COFIX 연동</td></tr><tr><td>KB 주택담보대출</td><td>혼합금리(5년 고정)</td><td>연 3.9~5.7%</td><td>5년 고정 후 변동</td></tr><tr><td>KB 주택담보대출</td><td>고정금리</td><td>연 4.2~6.0%</td><td>전 기간 고정</td></tr><tr><td>KB 디딤돌(정책)</td><td>고정금리</td><td>연 2.35~3.65%</td><td>정부 지원 상품</td></tr></tbody></table><p>※ 2026년 3월 기준 참고값이며 실제 적용 금리는 신용·담보 조건에 따라 다를 수 있습니다.</p>"),
            ("국민은행 주담대 자격 조건", "<ul><li><strong>대출 대상</strong>: 주택 구입 또는 기존 주택 보유자</li><li><strong>주택 유형</strong>: 아파트·단독주택·다세대·연립 등</li><li><strong>LTV</strong>: 규제 지역 50%, 비규제 지역 70% (2026년 규제 현황 기준)</li><li><strong>DSR</strong>: 40% 이내 (스트레스 DSR 포함)</li><li><strong>신용점수</strong>: 보통 NICE 700점 이상 권장</li></ul>"),
            ("KB 주담대 우대 금리 항목", "<table><thead><tr><th>우대 조건</th><th>우대율</th></tr></thead><tbody><tr><td>KB 급여 이체 고객</td><td>0.1~0.2%p</td></tr><tr><td>KB카드 사용 실적</td><td>0.1%p</td></tr><tr><td>자동이체 3건 이상</td><td>0.1%p</td></tr><tr><td>KB 스타클럽 등급</td><td>0.2~0.4%p</td></tr><tr><td>전자계약 체결</td><td>0.1%p</td></tr><tr><td>KB 청약종합저축 보유</td><td>0.1%p</td></tr></tbody></table>"),
            ("KB 주담대 신청 방법 및 절차", "<ol><li>KB스타뱅킹 앱 또는 영업점에서 사전 한도 조회</li><li>담보 물건 평가 (감정평가)</li><li>대출 신청 및 서류 제출</li><li>심사 및 승인</li><li>근저당권 설정 후 대출 실행</li></ol><h3>필요 서류</h3><ul><li>신분증, 등기부등본</li><li>소득 증빙 (원천징수영수증, 근로소득원천징수)</li><li>매매계약서 (구입 자금)</li></ul>"),
            ("국민은행 vs 타 은행 주담대 비교 팁", "<ul><li>KB 주담대가 항상 최저 금리는 아닙니다. <strong>핀다·카카오페이 등에서 실시간 비교</strong>하세요</li><li>이미 KB 주거래 고객이라면 우대 금리가 최대 0.8%p까지 가능해 유리합니다</li><li>신규 고객이라면 적극적으로 급여 이체, 카드 개설 조건을 충족해 우대 금리를 최대한 받으세요</li><li>고정금리와 변동금리 선택 시 향후 2~3년 금리 전망을 참고하세요</li></ul>"),
        ],
        "faq": [
            ("KB 주담대 사전 한도 조회는 신용점수에 영향을 주나요?", "KB스타뱅킹 앱에서 하는 <strong>사전 한도 조회(소프트 조회)</strong>는 신용점수에 영향을 주지 않습니다. 실제 대출 신청 시 정식 조회가 이루어집니다."),
            ("KB 주담대 금리 인하 요구권 행사가 가능한가요?", "네, 신용점수 상승 또는 소득 증가 시 <strong>KB스타뱅킹 앱 또는 영업점에서 금리 인하 요구</strong>가 가능합니다. 심사 후 0.1~0.5%p 인하된 사례도 많습니다."),
            ("KB 주담대 중도상환수수료는 얼마인가요?", "고정금리 대출은 대출 실행 후 <strong>3년 이내 상환 시 잔액의 1.2%</strong>가 수수료로 부과됩니다. 변동금리는 보통 0.6~0.8% 수준이며, 3년 이후에는 수수료가 없습니다."),
        ],
        "ctas": [
            {"text": "KB 주담대 금리 및 한도 확인하기", "desc": "국민은행에서 2026년 최신 주담대 금리와 한도를 확인하세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "주담대 금리 실시간 비교하기", "desc": "핀크에서 KB 포함 전 은행 주담대 금리를 한눈에 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "주담대 무료 금리 상담 받기", "desc": "토스에서 내 조건에 맞는 최저 금리 주담대를 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 42 =====
    {
        "title": "신한은행 전세대출 금리 조건 2026 완벽 정리",
        "cat": 6,
        "slug": "shinhan-jeonse-loan-2026",
        "intro": "<strong>신한은행 전세 대출</strong>은 신한쏠(SOL) 앱으로 비대면 신청이 가능하고 다양한 우대 금리 혜택을 제공합니다. 2026년 기준 신한은행 전세 대출의 종류, 금리, 조건, 신청 방법을 완벽하게 정리했습니다.",
        "sections": [
            ("2026년 신한은행 전세 대출 상품 비교", "<table><thead><tr><th>상품명</th><th>금리</th><th>한도</th><th>특징</th></tr></thead><tbody><tr><td>신한 쏠편한 전세 대출</td><td>연 3.5~5.5%</td><td>전세가 80%</td><td>비대면 신청 가능</td></tr><tr><td>버팀목 전세 대출(신한)</td><td>연 2.1~2.9%</td><td>수도권 3억/지방 2억</td><td>정부 정책 상품</td></tr><tr><td>청년 버팀목(신한)</td><td>연 1.5~2.7%</td><td>3억원</td><td>만 19~34세 전용</td></tr><tr><td>신혼부부 버팀목(신한)</td><td>연 1.2~2.7%</td><td>3억원</td><td>혼인 7년 이내</td></tr></tbody></table>"),
            ("신한 쏠편한 전세 대출 상세", "<ul><li><strong>대상</strong>: 무주택 세대주 또는 단독 세대주</li><li><strong>금리</strong>: 연 3.5~5.5% (신용·조건에 따라 상이)</li><li><strong>한도</strong>: 전세 보증금의 80%</li><li><strong>보증</strong>: HUG·HF·SGI 중 선택</li><li><strong>신청 방법</strong>: 신한쏠 앱 비대면 또는 영업점 방문</li></ul>"),
            ("신한은행 전세 대출 우대 금리 항목", "<table><thead><tr><th>우대 조건</th><th>우대율</th></tr></thead><tbody><tr><td>신한 급여 이체</td><td>0.2%p</td></tr><tr><td>신한카드 실적 30만원 이상</td><td>0.1%p</td></tr><tr><td>자동이체 3건 이상</td><td>0.1%p</td></tr><tr><td>신한 청약저축 보유</td><td>0.1%p</td></tr><tr><td>전자계약 체결</td><td>0.1%p</td></tr></tbody></table>"),
            ("신청 방법 및 필요 서류", "<h3>비대면 신청 (신한쏠 앱)</h3><ol><li>신한쏠 앱 → 대출 → 전세 대출 신청</li><li>본인 인증 후 전세계약서 등록</li><li>소득 증빙 서류 업로드</li><li>보증 기관 심사</li><li>대출 실행</li></ol><h3>필요 서류</h3><ul><li>신분증, 주민등록등본</li><li>전세계약서</li><li>소득 증빙: 원천징수영수증 또는 건강보험료 납부 확인서</li></ul>"),
            ("신한 전세 대출 vs 타 은행 비교 전략", "<ul><li>신한은행의 강점은 <strong>비대면 신청 편의성과 쏠(SOL) 앱 연계 우대</strong>입니다</li><li>정책 상품(버팀목·청년)은 취급 은행마다 금리가 같으므로 <strong>주거래 은행</strong>으로 선택하는 것이 유리합니다</li><li>일반 전세 대출은 핀다·카카오페이로 실시간 비교 후 가장 낮은 곳 선택</li></ul>"),
        ],
        "faq": [
            ("신한 전세 대출은 비대면으로 완전히 처리 가능한가요?", "신한쏠 앱에서 신청·서류 제출·승인까지 <strong>대부분 비대면 처리</strong>가 가능합니다. 다만 일부 보증 기관 심사나 임대인 확인이 필요한 경우 방문이 필요할 수 있습니다."),
            ("신한은행 버팀목 전세 대출과 일반 전세 대출의 차이는?", "버팀목은 <strong>정부가 금리를 지원하는 초저금리 정책 상품</strong>으로 소득·자산 기준이 있습니다. 일반 전세 대출은 기준이 없지만 금리가 높습니다."),
            ("전세 계약서 없이 먼저 한도 조회가 가능한가요?", "네, 신한쏠 앱에서 <strong>사전 한도 조회</strong>가 가능합니다. 계약서 없이도 예상 한도와 금리를 미리 확인할 수 있습니다."),
        ],
        "ctas": [
            {"text": "버팀목 전세 대출 자격 확인하기", "desc": "주택도시기금에서 신한은행 취급 버팀목 전세 대출을 확인하세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "전세 대출 금리 실시간 비교하기", "desc": "핀크에서 신한 포함 전 은행 전세 대출 금리를 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "전세 대출 무료 상담 받기", "desc": "토스에서 내 조건에 맞는 최저 금리 전세 대출을 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 43 =====
    {
        "title": "하나은행 주담대 금리 조건 2026 완벽 정리",
        "cat": 6,
        "slug": "hana-bank-mortgage-2026",
        "intro": "<strong>하나은행 주택담보대출</strong>은 하나원큐 앱을 통한 비대면 신청과 다양한 우대 금리가 특징입니다. 2026년 기준 하나은행 주담대 금리, 조건, 우대 혜택, 신청 방법을 상세히 안내합니다.",
        "sections": [
            ("2026년 하나은행 주담대 금리 현황", "<table><thead><tr><th>상품</th><th>금리 유형</th><th>금리 범위</th></tr></thead><tbody><tr><td>하나 주택담보대출</td><td>변동금리(6개월 COFIX)</td><td>연 3.9~5.6%</td></tr><tr><td>하나 주택담보대출</td><td>혼합금리(5년 고정)</td><td>연 4.0~5.8%</td></tr><tr><td>하나 주택담보대출</td><td>고정금리(10년)</td><td>연 4.3~6.1%</td></tr><tr><td>하나 디딤돌(정책)</td><td>고정금리</td><td>연 2.35~3.65%</td></tr></tbody></table>"),
            ("하나은행 주담대 우대 금리", "<table><thead><tr><th>우대 조건</th><th>우대율</th></tr></thead><tbody><tr><td>하나은행 급여 이체</td><td>0.2%p</td></tr><tr><td>하나카드 실적 30만원</td><td>0.1%p</td></tr><tr><td>하나머니 자동이체 3건</td><td>0.1%p</td></tr><tr><td>하나멤버스 VIP 등급</td><td>0.2~0.3%p</td></tr><tr><td>전자계약 체결</td><td>0.1%p</td></tr></tbody></table>"),
            ("하나은행 주담대 자격 및 한도", "<ul><li><strong>LTV</strong>: 규제 지역 50%, 비규제 70% (주택 유형·가격에 따라 상이)</li><li><strong>DSR</strong>: 연소득의 40% 이내 (스트레스 DSR 포함)</li><li><strong>신용점수</strong>: NICE 700점 이상 권장</li><li><strong>최대 한도</strong>: LTV × 감정가 이내 (수억원 규모 가능)</li></ul>"),
            ("하나원큐 비대면 신청 절차", "<ol><li>하나원큐 앱 → 대출 → 주택담보대출 신청</li><li>본인 인증 및 주택 정보 입력</li><li>소득 증빙 서류 업로드</li><li>감정평가 의뢰 (앱에서 연결)</li><li>심사 및 대출 실행</li></ol>"),
            ("하나은행 주담대 활용 전략", "<ul><li>하나은행 주거래 고객이라면 <strong>하나멤버스 VIP 등급 우대</strong>로 금리를 최대 0.5%p까지 낮출 수 있습니다</li><li>급여 이체 + 카드 실적 + 자동이체 3건을 모두 충족하면 우대 금리 0.4%p 확보</li><li>비대면 신청은 영업점 방문보다 처리 시간이 길 수 있으므로 <strong>잔금일 3~4주 전</strong>에 신청하세요</li></ul>"),
        ],
        "faq": [
            ("하나은행 주담대와 타 은행 금리 비교는 어떻게 하나요?", "핀다·카카오페이·토스 앱에서 <strong>실시간으로 전 은행 주담대 금리</strong>를 비교할 수 있습니다. 하나은행 단독 조회보다 여러 은행을 동시에 비교하는 것이 유리합니다."),
            ("하나은행 주담대 중도상환수수료는?", "고정금리 대출은 실행 후 <strong>3년 이내 상환 시 잔액의 1.2%</strong>, 변동금리는 0.6~0.8% 수준입니다. 3년 이후에는 수수료가 없습니다."),
            ("하나은행 주담대 금리 인하 요구권은 어떻게 행사하나요?", "하나원큐 앱 → 대출 관리 → 금리 인하 요구에서 신청 가능합니다. <strong>신용점수 상승이나 소득 증가 서류</strong>를 첨부하면 심사 후 금리 인하 결정을 받을 수 있습니다."),
        ],
        "ctas": [
            {"text": "하나은행 주담대 한도 확인하기", "desc": "주택도시기금에서 하나은행 취급 정책 주담대 조건을 확인하세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "하나 포함 주담대 금리 비교하기", "desc": "핀크에서 하나은행 포함 전 은행 주담대 금리를 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "주담대 무료 상담 신청하기", "desc": "토스에서 하나은행 포함 최저 금리 주담대를 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 44 =====
    {
        "title": "농협 NH 주담대 전세대출 비교 2026 총정리",
        "cat": 6,
        "slug": "nonghyup-mortgage-jeonse-2026",
        "intro": "<strong>농협은행(NH) 주담대·전세 대출</strong>은 농어촌 지역과 수도권 모두에서 광범위한 영업망을 갖춘 국내 최대 협동조합 금융의 대출 상품입니다. 2026년 기준 농협 주담대와 전세 대출의 금리, 조건, 우대 혜택을 상세히 비교합니다.",
        "sections": [
            ("2026년 농협 주담대 vs 전세 대출 금리 비교", "<table><thead><tr><th>상품</th><th>금리</th><th>한도</th><th>특징</th></tr></thead><tbody><tr><td>NH 주택담보대출(변동)</td><td>연 3.8~5.5%</td><td>LTV 범위 내</td><td>COFIX 연동</td></tr><tr><td>NH 주택담보대출(혼합)</td><td>연 4.0~5.8%</td><td>LTV 범위 내</td><td>5년 고정 후 변동</td></tr><tr><td>NH 전세 대출</td><td>연 3.5~5.3%</td><td>전세가 80%</td><td>HUG·HF 보증</td></tr><tr><td>버팀목(NH 취급)</td><td>연 2.1~2.9%</td><td>수도권 3억</td><td>정책 상품</td></tr></tbody></table>"),
            ("농협 주담대 우대 금리 항목", "<table><thead><tr><th>우대 조건</th><th>우대율</th></tr></thead><tbody><tr><td>NH 급여 이체</td><td>0.2%p</td></tr><tr><td>NH농협카드 30만원 실적</td><td>0.1%p</td></tr><tr><td>자동이체 3건 이상</td><td>0.1%p</td></tr><tr><td>NH올원뱅크 앱 비대면</td><td>0.1%p</td></tr><tr><td>농업인·조합원</td><td>0.1~0.3%p</td></tr></tbody></table>"),
            ("농협 전세 대출 특징 및 조건", "<ul><li><strong>비대면 신청</strong>: NH올원뱅크 앱으로 전세 대출 완전 비대면 처리 가능</li><li><strong>보증 선택</strong>: HUG, HF(한국주택금융공사), SGI 중 선택</li><li><strong>농어촌 지역 우대</strong>: 농어촌 소재 전세는 추가 우대 금리 적용 가능</li><li><strong>조합원 우대</strong>: 농협 조합원 가입 시 추가 우대 금리</li></ul>"),
            ("NH 주담대 신청 절차", "<ol><li>NH올원뱅크 앱 또는 영업점 방문</li><li>사전 한도 조회 (앱 내 즉시 가능)</li><li>서류 제출 및 감정평가</li><li>심사 후 근저당 설정</li><li>대출 실행</li></ol>"),
            ("농협 vs 타 은행 선택 기준", "<ul><li>농어촌 지역이나 농업인이라면 <strong>농협 우대 혜택</strong>이 가장 강력합니다</li><li>도시 지역 일반인이라면 KB·신한·하나·우리 은행과 금리 비교 후 최저 선택</li><li>NH카드 주거래 고객이라면 카드 실적 우대를 최대로 활용하세요</li><li>버팀목·디딤돌 등 정책 상품은 취급 은행별 금리가 동일하므로 주거래 은행 선택 OK</li></ul>"),
        ],
        "faq": [
            ("농협 전세 대출과 버팀목 중 어떤 것이 더 유리한가요?", "소득 조건(연 5,000만원 이하)이 맞는다면 <strong>버팀목이 금리 면에서 훨씬 유리</strong>합니다(연 2%대 vs 4%대). 소득이 초과한다면 NH 일반 전세 대출을 이용하세요."),
            ("농협 조합원 가입이 대출에 유리한가요?", "네, 농협 조합원(출자금 1~5만원)으로 가입하면 <strong>주담대·신용대출 금리 우대(0.1~0.3%p)</strong>를 받을 수 있습니다. 출자금 대비 혜택이 매우 크므로 적극 활용하세요."),
            ("농협은행 주담대 중도상환수수료는?", "고정금리는 <strong>3년 이내 상환 시 잔액의 1.2%</strong>, 변동금리는 0.6~0.8%입니다. 3년 이후에는 수수료 없이 상환 가능합니다."),
        ],
        "ctas": [
            {"text": "농협 주담대·전세 대출 조건 확인", "desc": "주택도시기금에서 NH 취급 정책 대출 자격을 확인하세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "NH 포함 주담대 금리 비교하기", "desc": "핀크에서 농협 포함 전 은행 주담대·전세 금리를 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "농협 대출 무료 상담 받기", "desc": "토스에서 농협 포함 최저 금리 대출 상품을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 45 =====
    {
        "title": "대출 플랫폼 비교 핀다 토스 카카오페이 2026",
        "cat": 6,
        "slug": "loan-platform-comparison-2026",
        "intro": "<strong>대출 비교 플랫폼</strong>을 활용하면 여러 금융기관의 대출 금리와 한도를 한 번에 비교할 수 있습니다. 핀다, 토스, 카카오페이, 뱅크샐러드 등 주요 플랫폼의 특징과 차이를 2026년 기준으로 비교 정리했습니다.",
        "sections": [
            ("주요 대출 비교 플랫폼 한눈에 비교", "<table><thead><tr><th>플랫폼</th><th>강점</th><th>취급 기관 수</th><th>신용점수 영향</th></tr></thead><tbody><tr><td>핀다(Finda)</td><td>대출 전문, 금융사 수 최다</td><td>60개 이상</td><td>없음(소프트 조회)</td></tr><tr><td>토스(Toss)</td><td>UX 편의성, 신용점수 관리 연계</td><td>40개 이상</td><td>없음</td></tr><tr><td>카카오페이</td><td>카카오 생태계 연계</td><td>30개 이상</td><td>없음</td></tr><tr><td>뱅크샐러드</td><td>자산 관리 + 대출 비교</td><td>30개 이상</td><td>없음</td></tr></tbody></table>"),
            ("핀다(Finda) 상세 분석", "<ul><li><strong>특징</strong>: 국내 최대 대출 전문 비교 플랫폼, 주담대·전세·신용·사업자 대출 모두 비교</li><li><strong>취급 기관</strong>: 1금융권 + 2금융권 + 핀테크 60개 이상</li><li><strong>장점</strong>: 실시간 금리 업데이트, 한도·금리 동시 비교, 비대면 신청 연결</li><li><strong>단점</strong>: 실제 승인 금리는 개인 조건에 따라 다를 수 있음</li><li><strong>추천 상황</strong>: 주담대·사업자 대출 등 큰 금액 대출 비교 시</li></ul>"),
            ("토스(Toss) 대출 비교 분석", "<ul><li><strong>특징</strong>: 신용점수 관리·보험·투자와 연계된 종합 금융 앱 내 대출 비교</li><li><strong>장점</strong>: 간편한 UX, 신용점수 실시간 확인, 부채 현황 통합 관리</li><li><strong>단점</strong>: 핀다 대비 취급 기관 수 적음</li><li><strong>추천 상황</strong>: 신용 관리와 대출을 동시에 관리하고 싶을 때</li></ul>"),
            ("카카오페이 대출 비교 분석", "<ul><li><strong>특징</strong>: 카카오 계정 기반으로 간편한 신청, 카카오뱅크 상품 직접 연결</li><li><strong>장점</strong>: 카카오뱅크 최저 금리 바로 비교, 쉬운 인증</li><li><strong>단점</strong>: 타 은행 상품 비교 깊이가 핀다에 비해 부족</li><li><strong>추천 상황</strong>: 카카오뱅크 위주로 신용 대출을 원할 때</li></ul>"),
            ("대출 플랫폼 활용 전략", "<ol><li><strong>핀다로 시작</strong>: 가장 많은 기관을 한 번에 비교, 최저 금리 후보 3개 선정</li><li><strong>토스에서 2차 확인</strong>: 신용점수와 함께 조건 재확인</li><li><strong>직접 은행 앱으로 최종 확인</strong>: 우대 금리 포함한 실제 금리 조회</li><li><strong>협상 카드로 활용</strong>: 플랫폼에서 받은 견적을 현재 거래 은행에 제시</li></ol>"),
        ],
        "faq": [
            ("대출 비교 플랫폼 사용 시 개인정보가 금융사에 넘어가나요?", "실제 대출 신청을 하지 않는 한, 비교·조회 단계에서는 <strong>금융사에 개인 정보가 공유되지 않습니다.</strong> 신청 버튼을 누를 때 정보 제공 동의가 필요합니다."),
            ("플랫폼에서 보이는 금리가 실제 적용 금리와 다른 경우가 있나요?", "네, <strong>플랫폼의 금리는 최저 금리 기준</strong>으로 표시되는 경우가 많습니다. 실제 적용 금리는 신용점수, 소득, 담보 등 조건에 따라 달라집니다."),
            ("여러 플랫폼에서 동시에 조회하면 신용점수가 내려가나요?", "비교 조회(소프트 조회)는 신용점수에 영향이 없습니다. 실제 <strong>대출 신청(하드 조회)</strong>을 여러 곳에 동시에 하면 일시적으로 신용점수가 하락할 수 있습니다."),
        ],
        "ctas": [
            {"text": "핀다에서 대출 금리 비교하기", "desc": "핀다에서 60개 이상 금융사의 대출 금리를 한 번에 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "토스에서 신용점수 확인 후 비교", "desc": "토스에서 내 신용점수와 이용 가능 대출 상품을 한 번에 확인하세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
            {"text": "정책 대출 자격 별도 확인하기", "desc": "금융소비자포털에서 플랫폼에 없는 정책 대출 상품도 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
        ]
    },
    # ===== POST 46 =====
    {
        "title": "청년도약계좌 대출 연계 활용법 2026 완벽 가이드",
        "cat": 6,
        "slug": "youth-leap-account-loan-2026",
        "intro": "<strong>청년도약계좌</strong>는 월 70만원 납입 시 정부 기여금과 비과세 혜택으로 5년 후 최대 5,000만원을 만들 수 있는 청년 자산 형성 상품입니다. 이 계좌를 전세·주택 구입 대출과 연계하면 더욱 강력한 재정 전략이 됩니다. 2026년 기준 청년도약계좌와 대출 연계 활용법을 안내합니다.",
        "sections": [
            ("청년도약계좌 기본 조건 및 혜택", "<table><thead><tr><th>구분</th><th>내용</th></tr></thead><tbody><tr><td>가입 대상</td><td>만 19~34세 (병역 기간 제외)</td></tr><tr><td>소득 기준</td><td>연소득 7,500만원 이하</td></tr><tr><td>납입 한도</td><td>월 최대 70만원</td></tr><tr><td>만기</td><td>5년</td></tr><tr><td>정부 기여금</td><td>월 최대 2.4만원 (소득별 차등)</td></tr><tr><td>금리</td><td>연 4.5~6.0% (은행별 상이)</td></tr><tr><td>세제 혜택</td><td>이자 소득 비과세</td></tr></tbody></table>"),
            ("청년도약계좌 + 청년 전세 대출 연계 전략", "<ul><li>청년도약계좌로 <strong>전세 보증금 차액(자기 자본 부분)을 적립</strong>하면서 청년 버팀목 전세 대출을 병행 이용</li><li>5년 만기 후 약 4,200~5,000만원 목돈 마련 → 전세 갱신 시 보증금 인상분 충당 또는 주택 구입 종자돈으로 활용</li><li><strong>월 납입 vs 대출 이자</strong> 동시에 지출되지만, 도약계좌 금리(4.5~6%)가 전세 대출 이자(2~4%)보다 높은 경우 순이익이 발생합니다</li></ul>"),
            ("청년도약계좌 중도 해지 주의사항", "<ul><li>5년 만기 전 중도 해지 시 <strong>정부 기여금 전액 반환 + 비과세 혜택 소멸</strong></li><li>예외: 사망·사고·폐업·천재지변·해외 이주·결혼 시 중도 해지 가능 (기여금 일부 유지)</li><li>주택 구입 자금 필요 시에는 중도 해지 전에 <strong>정책 주담대 먼저 신청</strong>하고 계좌를 유지하는 전략이 유리합니다</li></ul>"),
            ("청년도약계좌 + 주택 청약 연계", "<ul><li>청년도약계좌와 <strong>주택청약종합저축</strong>을 동시에 유지하는 것이 가능합니다</li><li>청약 당첨 후 주택 구입 자금이 필요할 때 도약계좌 만기 금액을 활용</li><li>디딤돌·신생아 특례 등 정책 주담대와 병행해 이자 부담을 낮추는 전략 추천</li></ul>"),
            ("청년 재정 전략 예시 (5년 플랜)", "<table><thead><tr><th>연도</th><th>행동 계획</th></tr></thead><tbody><tr><td>1년차</td><td>청년도약계좌 가입 + 청년 버팀목 전세 대출 이용</td></tr><tr><td>2~3년차</td><td>월 70만원 납입 지속 + 신용점수 관리</td></tr><tr><td>4년차</td><td>주택 청약 적극 신청 + 디딤돌 대출 조건 점검</td></tr><tr><td>5년차 만기</td><td>약 4,200~5,000만원 수령 → 주택 구입 자기자본 활용</td></tr></tbody></table>"),
        ],
        "faq": [
            ("청년도약계좌와 청년희망적금은 동시에 가입할 수 있나요?", "청년희망적금 만기 해지 후 청년도약계좌 가입이 가능합니다. <strong>동시 가입은 불가</strong>합니다."),
            ("청년도약계좌 납입 중에 전세 대출을 받을 수 있나요?", "네, 청년도약계좌 납입과 전세 대출은 <strong>동시에 유지</strong>가 가능합니다. 대출 신청 시 청년도약계좌 잔액이 자산으로 인정될 수 있습니다."),
            ("청년도약계좌 가입 시 어떤 은행이 가장 유리한가요?", "정부 기여금은 동일하지만 <strong>은행 자체 금리는 차이</strong>가 납니다. 2026년 기준 금리를 비교해 가장 높은 은행을 선택하세요. 기업은행·하나은행 등이 높은 금리를 제공한 사례가 있습니다."),
        ],
        "ctas": [
            {"text": "청년도약계좌 가입 자격 확인하기", "desc": "주택도시기금에서 청년 맞춤 금융 상품 자격을 확인하세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "청년 맞춤 금융 상품 비교하기", "desc": "핀크에서 청년 전용 저축·대출 상품을 한눈에 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "청년 재정 전략 무료 상담 받기", "desc": "토스에서 청년도약계좌와 대출 연계 전략을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 47 =====
    {
        "title": "주택청약 당첨 후 대출 절차 2026 완벽 가이드",
        "cat": 6,
        "slug": "housing-subscription-loan-process",
        "intro": "<strong>주택청약 당첨 후</strong>에는 계약금 납부, 중도금 대출, 잔금 대출까지 단계별로 대출을 실행해야 합니다. 각 단계의 타이밍과 준비 사항을 놓치면 계약이 취소될 수 있습니다. 2026년 기준 청약 당첨 후 대출 절차를 단계별로 상세히 안내합니다.",
        "sections": [
            ("청약 당첨 후 전체 대출 흐름", "<ol><li><strong>당첨 확인</strong> → 계약 일정 통보 수령</li><li><strong>계약금 납부</strong> (분양가의 10~20%, 개인 자금)</li><li><strong>중도금 대출</strong> (보통 분양가의 60%, 건설사 지정 은행)</li><li><strong>입주 전 잔금 대출 준비</strong> (분양가의 20~30%, 일반 주담대로 전환)</li><li><strong>입주 + 잔금 납부</strong> → 소유권 이전 등기</li></ol>"),
            ("중도금 대출 상세 안내", "<ul><li><strong>중도금</strong>은 보통 분양가의 60%를 6회 나눠 납부합니다</li><li>건설사가 지정한 은행에서 집단 대출 방식으로 진행</li><li>금리: 보통 연 4~6% (고정 또는 변동)</li><li>2026년 현재 일부 건설사는 무이자 중도금 대출을 지원하기도 합니다</li><li>중도금 대출은 DSR 적용 제외(입주 전까지)</li></ul>"),
            ("잔금 대출 준비 시 체크리스트", "<ul><li>잔금 대출은 입주 예정일 <strong>3~4개월 전</strong>부터 준비 시작</li><li>DTI·DSR·LTV 규제 확인 (입주 시점 규제 적용)</li><li>중도금 대출을 주담대로 전환 or 별도 주담대 실행 선택</li><li>공동 명의 여부 결정 (부부 공동 명의 시 취득세 절감 효과)</li><li>금리 비교: 건설사 지정 은행 vs 타 은행</li></ul>"),
            ("청약 당첨 후 주의사항", "<ul><li>계약금은 <strong>개인 자금</strong>으로 납부해야 하며, 대출로 계약금을 마련하면 DSR 계산에 포함됩니다</li><li>중도금 대출 실행 중 이직·퇴직 등 소득 변동이 생기면 잔금 대출 승인에 영향을 줄 수 있습니다</li><li>잔금 납부 기한을 초과하면 <strong>연체 이자 및 계약 해제</strong> 위험이 있습니다</li><li>전매 제한 기간 확인: 규제 지역은 최대 10년 전매 금지</li></ul>"),
            ("청약 당첨자 활용 가능한 정책 대출", "<table><thead><tr><th>상품</th><th>조건</th><th>금리</th></tr></thead><tbody><tr><td>디딤돌 구입 자금</td><td>연소득 7,000만원 이하, 주택가 5억 이하</td><td>연 2.35~3.65%</td></tr><tr><td>신생아 특례 구입 자금</td><td>2년 내 출산 가구</td><td>연 1.6~3.3%</td></tr><tr><td>보금자리론</td><td>소득 무관 (일부 우대)</td><td>연 3.65~4.25%</td></tr></tbody></table>"),
        ],
        "faq": [
            ("중도금 대출이 있는 상태에서 다른 대출을 받을 수 있나요?", "중도금 집단 대출은 <strong>입주 전까지 DSR 적용이 제외</strong>됩니다. 따라서 중도금 대출이 있어도 다른 대출을 받을 수 있지만, 실행 후 DSR 합산 계산에 포함되므로 주의하세요."),
            ("청약 당첨 후 계약을 취소하면 계약금을 돌려받을 수 있나요?", "계약자 사정으로 해제 시 <strong>계약금을 몰취(돌려받지 못함)</strong>하는 것이 일반적입니다. 불가피한 경우 청약홈 또는 건설사와 협의하세요."),
            ("부부 공동 명의로 청약 당첨이 가능한가요?", "공공 분양은 세대주 1인 명의로만 청약이 가능합니다. 민간 분양은 공동 청약이 가능한 경우도 있습니다. <strong>입주 시 공동 명의로 변경</strong>은 가능합니다."),
        ],
        "ctas": [
            {"text": "청약 당첨 후 정책 주담대 확인하기", "desc": "주택도시기금에서 청약 당첨자를 위한 디딤돌·신생아 특례를 확인하세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "잔금 대출 금리 미리 비교하기", "desc": "핀크에서 청약 당첨 후 잔금 대출 상품을 미리 비교해두세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "청약 당첨 후 대출 전략 상담하기", "desc": "토스에서 중도금·잔금 대출 최적 전략을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 48 =====
    {
        "title": "역모기지론 주택연금 조건 신청 방법 2026 총정리",
        "cat": 6,
        "slug": "reverse-mortgage-guide-2026",
        "intro": "<strong>역모기지론(주택연금)</strong>은 집을 담보로 맡기고 매달 연금처럼 생활비를 받는 고령자 전용 금융 상품입니다. 소유한 주택을 처분하지 않고도 안정적인 노후 소득을 확보할 수 있어 은퇴 후 재정 계획에 중요한 역할을 합니다. 2026년 기준 주택연금의 조건, 수령액, 신청 방법을 상세히 안내합니다.",
        "sections": [
            ("주택연금(역모기지론)이란?", "<p><strong>주택연금</strong>은 한국주택금융공사(HF)가 보증하고 은행이 취급하는 역모기지 상품입니다. 주택을 담보로 맡기고 사망 시까지 매달 연금을 수령합니다.</p><ul><li>운영 기관: 한국주택금융공사(HF)</li><li>대상: 만 55세 이상, 주택 보유자</li><li>특징: 살던 집에서 그대로 거주하면서 연금 수령</li><li>국가 보증으로 안전성 높음</li></ul>"),
            ("2026년 주택연금 자격 조건", "<table><thead><tr><th>구분</th><th>조건</th></tr></thead><tbody><tr><td>가입 연령</td><td>부부 중 연장자 만 55세 이상</td></tr><tr><td>주택 보유</td><td>1주택 소유자 (2주택도 가능, 조건 있음)</td></tr><tr><td>주택 가격</td><td>공시가격 9억원 이하 (2주택자는 합산)</td></tr><tr><td>거주 요건</td><td>가입 주택에 실제 거주</td></tr></tbody></table>"),
            ("주택연금 월 수령액 예시", "<table><thead><tr><th>가입 연령</th><th>주택 가격 3억원</th><th>주택 가격 5억원</th><th>주택 가격 7억원</th></tr></thead><tbody><tr><td>60세</td><td>약 62만원</td><td>약 104만원</td><td>약 145만원</td></tr><tr><td>65세</td><td>약 76만원</td><td>약 127만원</td><td>약 178만원</td></tr><tr><td>70세</td><td>약 95만원</td><td>약 159만원</td><td>약 223만원</td></tr></tbody></table><p>※ 종신지급 방식, 정액형 기준 (2026년 참고값)</p>"),
            ("주택연금 지급 방식 비교", "<table><thead><tr><th>방식</th><th>특징</th><th>추천 대상</th></tr></thead><tbody><tr><td>종신지급</td><td>사망 시까지 동일 금액</td><td>오래 살수록 유리, 기본 선택</td></tr><tr><td>확정기간</td><td>10·15·20·30년 중 선택</td><td>특정 기간 목돈이 필요한 경우</td></tr><tr><td>대출상환</td><td>기존 주담대 먼저 상환 후 잔액 연금 수령</td><td>기존 대출 있는 경우</td></tr></tbody></table>"),
            ("주택연금 신청 절차", "<ol><li>한국주택금융공사 홈페이지(hf.go.kr) 또는 취급 은행 방문 상담</li><li>신청서 작성 및 서류 제출</li><li>주택 감정평가</li><li>공사 심사 및 보증서 발급</li><li>은행에서 대출 약정 체결</li><li>매월 연금 수령 시작</li></ol><h3>필요 서류</h3><ul><li>신분증, 가족관계증명서</li><li>등기부등본, 건축물대장</li><li>건강보험료 납부 확인서</li></ul>"),
        ],
        "faq": [
            ("주택연금 가입 후 집을 팔 수 있나요?", "주택연금에 가입하면 <strong>주택 처분이 제한</strong>됩니다. 단, 이사가 필요할 경우 다른 주택으로 담보 변경(이전)이 가능합니다."),
            ("사망 시 남은 집은 어떻게 되나요?", "사망 후 집을 처분해 <strong>누적 연금 수령액을 정산</strong>합니다. 집값이 연금 수령액보다 크면 차액을 상속인에게 돌려줍니다. 반대로 연금이 집값을 초과해도 상속인에게 청구하지 않습니다(국가 보증)."),
            ("주택연금을 중도에 해지할 수 있나요?", "해지 가능하지만 <strong>그동안 받은 연금과 이자를 전부 상환</strong>해야 합니다. 해지 전 반드시 전체 상환 금액을 확인하세요."),
        ],
        "ctas": [
            {"text": "주택연금 수령액 미리 계산하기", "desc": "한국주택금융공사에서 내 주택 기준 예상 수령액을 계산해보세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "노후 주거 금융 상품 비교하기", "desc": "핀크에서 역모기지 및 노후 주거 금융 상품을 비교하세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "주택연금 무료 상담 신청하기", "desc": "토스에서 노후 재정 설계와 주택연금 활용 방법을 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 49 =====
    {
        "title": "1금융권 vs 2금융권 대출 차이 2026 완벽 비교",
        "cat": 6,
        "slug": "first-second-tier-bank-loan-comparison",
        "intro": "<strong>1금융권과 2금융권의 대출</strong>은 금리, 심사 조건, 한도, 신용 영향 등 여러 면에서 차이가 있습니다. 어디서 빌리느냐에 따라 이자 부담이 수백만원 달라질 수 있습니다. 2026년 기준 1금융권과 2금융권 대출의 모든 차이를 비교 정리했습니다.",
        "sections": [
            ("1금융권 vs 2금융권 기본 개념", "<table><thead><tr><th>구분</th><th>1금융권</th><th>2금융권</th></tr></thead><tbody><tr><td>종류</td><td>시중은행, 국책은행, 인터넷은행</td><td>저축은행, 카드사, 캐피탈, 보험사, 신협, 새마을금고</td></tr><tr><td>예시</td><td>국민·신한·하나·우리·농협·카카오뱅크 등</td><td>OK저축은행·웰컴저축은행·현대카드·롯데캐피탈 등</td></tr><tr><td>감독 기관</td><td>금융감독원</td><td>금융감독원 (동일하지만 규제 차이 있음)</td></tr></tbody></table>"),
            ("금리 비교", "<table><thead><tr><th>대출 종류</th><th>1금융권 평균 금리</th><th>2금융권 평균 금리</th></tr></thead><tbody><tr><td>주택담보대출</td><td>연 3.5~5.5%</td><td>연 5.0~12%</td></tr><tr><td>전세 대출</td><td>연 3.5~5.3%</td><td>연 5.0~10%</td></tr><tr><td>신용 대출</td><td>연 4~8%</td><td>연 8~20%</td></tr><tr><td>마이너스통장</td><td>연 4~7%</td><td>연 8~18%</td></tr></tbody></table>"),
            ("심사 조건 비교", "<table><thead><tr><th>조건</th><th>1금융권</th><th>2금융권</th></tr></thead><tbody><tr><td>신용점수</td><td>보통 700점 이상</td><td>600점 이하도 가능</td></tr><tr><td>소득 증빙</td><td>엄격 (2년 이상 신고 이력)</td><td>상대적으로 유연</td></tr><tr><td>심사 속도</td><td>2~5일</td><td>당일~2일</td></tr><tr><td>연체 이력</td><td>매우 민감</td><td>상대적으로 유연</td></tr></tbody></table>"),
            ("신용점수에 미치는 영향", "<ul><li><strong>1금융권 대출</strong>: 신용점수에 긍정적 또는 중립적 영향</li><li><strong>2금융권 대출</strong>: 보유 자체가 신용점수에 소폭 부정적 영향 (특히 저축은행·캐피탈)</li><li>2금융권 대출이 <strong>여러 건 누적</strong>될수록 신용점수 하락폭 커짐</li><li>2금융권 이용 후 성실 상환 → 1금융권으로 갈아타기 전략이 효과적</li></ul>"),
            ("1금융권 거절 후 대처 전략", "<ol><li>인터넷 은행(카카오·케이뱅크·토스뱅크) 재시도: 심사 기준이 다소 유연</li><li>신협·새마을금고: 지역 기반으로 조합원 우대 가능</li><li>사잇돌·햇살론 등 정책 대출 확인</li><li>저축은행: 고금리지만 빠른 심사</li><li>신용점수 개선 후 1금융권 재도전</li></ol>"),
        ],
        "faq": [
            ("2금융권 대출을 받으면 신용점수가 얼마나 떨어지나요?", "저축은행 1건 이용 시 신용점수가 <strong>10~30점 정도 하락</strong>할 수 있습니다. 다만 이후 성실 상환 시 회복이 가능합니다."),
            ("새마을금고·신협은 1금융권인가요 2금융권인가요?", "새마을금고·신협은 <strong>상호금융으로 2금융권</strong>에 속합니다. 그러나 은행권보다 지역 밀착 서비스와 조합원 우대가 강점입니다."),
            ("2금융권 대출을 1금융권으로 빠르게 갈아타는 방법은?", "<strong>6~12개월 성실 상환 + 신용점수 10점 이상 상승</strong>이 확인되면 1금융권에 대환 신청을 시도하세요. 핀다·토스에서 대환 가능 여부를 실시간으로 확인할 수 있습니다."),
        ],
        "ctas": [
            {"text": "1금융권 정책 대출 자격 확인하기", "desc": "금융소비자포털에서 1금융권 이용 가능 정책 대출을 확인하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "1·2금융권 금리 한눈에 비교하기", "desc": "핀크에서 1·2금융권 대출 금리를 동시에 비교하고 최적 상품을 찾으세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "내 신용에 맞는 대출 무료 상담", "desc": "토스에서 신용점수 기반 최적 금융권 대출을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== POST 50 =====
    {
        "title": "대출 총정리 2026 종류별 금리 한도 비교 완벽 가이드",
        "cat": 6,
        "slug": "all-loan-types-comparison-2026",
        "intro": "<strong>2026년 대출 총정리</strong>입니다. 주택 대출부터 신용 대출, 서민 금융, 사업자 대출까지 모든 종류의 대출을 금리·한도·조건 기준으로 한눈에 비교합니다. 내 상황에 맞는 최적의 대출을 선택하는 데 이 가이드 하나로 충분합니다.",
        "sections": [
            ("2026년 주요 대출 종류 전체 비교표", "<table><thead><tr><th>대출 종류</th><th>금리</th><th>한도</th><th>대상</th></tr></thead><tbody><tr><td>디딤돌 대출</td><td>연 2.35~3.65%</td><td>4~5억원</td><td>무주택, 소득 7,000만원 이하</td></tr><tr><td>버팀목 전세 대출</td><td>연 2.1~2.9%</td><td>3억원</td><td>무주택 세대주</td></tr><tr><td>신생아 특례 구입</td><td>연 1.6~3.3%</td><td>5억원</td><td>2년 내 출산 가구</td></tr><tr><td>1금융권 주담대</td><td>연 3.5~5.5%</td><td>LTV 범위</td><td>누구나 (조건 충족 시)</td></tr><tr><td>신용 대출</td><td>연 4~8%</td><td>1~5억원</td><td>소득 있는 직장인·사업자</td></tr><tr><td>사잇돌 대출</td><td>연 5.9~14.9%</td><td>2,000만원</td><td>중신용자</td></tr><tr><td>햇살론 뱅크</td><td>연 6.5~10.5%</td><td>2,000만원</td><td>저소득·저신용</td></tr><tr><td>햇살론 15</td><td>연 15.9%</td><td>700만원</td><td>저소득·저신용</td></tr><tr><td>미소금융</td><td>연 4.5%</td><td>7,000만원</td><td>기초생활수급자</td></tr></tbody></table>"),
            ("내 상황별 최적 대출 선택 가이드", "<h3>상황 1: 집 사고 싶은 무주택자</h3><ul><li>소득 7,000만원 이하 → <strong>디딤돌 대출</strong> 우선</li><li>출산 2년 이내 → <strong>신생아 특례 구입 자금</strong></li><li>소득 초과 → <strong>보금자리론 → 시중은행 주담대</strong></li></ul><h3>상황 2: 전세 자금 필요</h3><ul><li>소득 5,000만원 이하, 만 34세 이하 → <strong>청년 버팀목</strong></li><li>소득 5,000만원 이하 → <strong>버팀목 전세 대출</strong></li><li>소득 초과 → 시중은행 전세 대출 비교</li></ul><h3>상황 3: 소액 생활비·긴급 자금</h3><ul><li>신용점수 700점 이상 → <strong>1금융권 신용 대출</strong></li><li>신용점수 620~839점 → <strong>사잇돌 대출</strong></li><li>저소득·저신용 → <strong>햇살론 뱅크 → 햇살론 15</strong></li></ul>"),
            ("대출 선택 전 반드시 확인할 5가지", "<ol><li><strong>DSR 한도 계산</strong>: 연소득의 40%(은행) 이내인지 확인</li><li><strong>LTV 확인</strong>: 담보 가치 대비 대출 비율 규제 확인</li><li><strong>금리 유형</strong>: 변동·혼합·고정 금리의 장단점 비교</li><li><strong>중도상환수수료</strong>: 조기 상환 계획 있으면 반드시 확인</li><li><strong>우대 금리 조건</strong>: 급여 이체·카드 실적·자동이체 설정으로 금리 낮추기</li></ol>"),
            ("2026년 대출 시장 트렌드", "<ul><li><strong>스트레스 DSR 전면 적용</strong>: 대출 한도 축소 추세</li><li><strong>비대면 대출 확산</strong>: 인터넷 은행·핀테크 플랫폼으로 편리한 대환 가능</li><li><strong>정책 대출 확대</strong>: 신생아 특례·청년 도약 등 정부 지원 상품 강화</li><li><strong>금리 하락 추세</strong>: 기준금리 인하로 2026년 전반적 금리 하락세</li></ul>"),
            ("대출 완전 활용 로드맵", "<ol><li><strong>자격 확인</strong>: 정책 대출 → 1금융권 → 2금융권 순으로 검토</li><li><strong>비교 플랫폼 활용</strong>: 핀다·토스·카카오페이에서 실시간 비교</li><li><strong>우대 금리 최대화</strong>: 주거래 은행에서 급여 이체·카드 조건 충족</li><li><strong>금리 인하 요구</strong>: 신용 개선 시 금리 인하 요구권 행사</li><li><strong>갈아타기 전략</strong>: 중도상환수수료 없는 시점에 저금리 대환</li></ol>"),
        ],
        "faq": [
            ("2026년에 대출받기 좋은 시기가 언제인가요?", "기준금리 변동 추이를 확인하세요. <strong>기준금리 인하 발표 후 은행 금리가 반영되기까지 1~2개월</strong>이 걸립니다. 금리 하락 추세라면 변동금리가, 불확실하다면 혼합금리가 안전합니다."),
            ("정책 대출과 일반 대출을 동시에 받을 수 있나요?", "원칙적으로 가능하지만 <strong>DSR 합산</strong>이 되므로 총 한도가 제한됩니다. 정책 대출로 전세·주택 자금을 조달하고, 생활비는 신용 대출로 분리하는 것이 효율적입니다."),
            ("대출 신청 시 신용점수 조회가 몇 번까지 안전한가요?", "공식 대출 신청(하드 조회)은 <strong>1개월 내 3회 이내</strong>로 제한하는 것이 좋습니다. 여러 은행에 동시 신청하면 신용점수가 일시적으로 하락할 수 있습니다. 비교 플랫폼의 소프트 조회는 횟수 제한 없이 안전합니다."),
        ],
        "ctas": [
            {"text": "정책 대출 자격 한 번에 확인하기", "desc": "주택도시기금·금융소비자포털에서 모든 정책 대출 자격을 확인하세요", "url": "https://nhuf.molit.go.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "내 상황에 맞는 최저 금리 대출 찾기", "desc": "핀크에서 전체 금융권 대출 금리를 한 번에 비교하고 최적 상품을 찾으세요", "url": "https://www.finnq.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "대출 전략 1:1 무료 상담 받기", "desc": "토스에서 내 재정 상황에 최적화된 대출 전략을 무료로 상담받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
]


if __name__ == "__main__":
    print("PUBLISHING LOAN 50 POSTS")
    print("=" * 60)
    count = 0
    success = 0
    fail = 0
    for post in POSTS:
        count += 1
        ok = publish_post(post)
        if ok:
            success += 1
        else:
            fail += 1
        time.sleep(2)
    print("=" * 60)
    print(f"완료! 성공: {success} / 실패: {fail} / 합계: {count}")

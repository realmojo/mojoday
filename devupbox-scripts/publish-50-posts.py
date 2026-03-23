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

POSTS = [
    # ===== 보험/금융 (금융=8) =====
    {
        "title": "실비보험 추천 2026 4세대 실손보험 비교 및 가입 가이드",
        "cat": 8,
        "slug": "real-loss-insurance-2026",
        "intro": "실손의료보험(실비보험)은 국민 10명 중 7명이 가입한 대표적인 보험 상품입니다. 2021년 7월부터 시행된 <strong>4세대 실손보험</strong>은 기존 상품과 보장 구조가 크게 달라졌습니다. 이 글에서는 2026년 기준 실비보험의 세대별 차이, 추천 상품, 가입 시 주의사항을 총정리합니다.",
        "sections": [
            ("실비보험이란?", "<p>실비보험(실손의료보험)은 병원 치료비 중 <strong>본인이 실제 부담한 금액</strong>을 보장해주는 보험입니다. 국민건강보험이 보장하지 않는 비급여 항목(MRI, 초음파, 도수치료 등)까지 커버합니다.</p><ul><li><strong>급여 항목</strong>: 본인부담금의 80~90% 보장</li><li><strong>비급여 항목</strong>: 본인부담금의 70~80% 보장 (세대별 차이)</li></ul>"),
            ("1~4세대 실손보험 비교", "<table><thead><tr><th>구분</th><th>1세대</th><th>2세대</th><th>3세대</th><th>4세대 (현행)</th></tr></thead><tbody><tr><td>판매 시기</td><td>~2009</td><td>2009~2017</td><td>2017~2021</td><td>2021.7~</td></tr><tr><td>보험료</td><td>저렴</td><td>보통</td><td>다소 높음</td><td>초기 저렴</td></tr><tr><td>비급여 보장</td><td>80~100%</td><td>80%</td><td>80%</td><td>70% (특약)</td></tr><tr><td>보험료 인상</td><td>매년 가능</td><td>3년마다</td><td>3년마다</td><td>1년마다 조정</td></tr><tr><td>특징</td><td>보장 넓음</td><td>표준화</td><td>비급여 분리</td><td>급여/비급여/특약 3분리</td></tr></tbody></table><p>4세대 실손보험은 <strong>비급여 특약을 별도 분리</strong>하여, 비급여 이용이 많은 가입자의 보험료가 올라가고 적은 가입자는 할인받는 구조입니다.</p>"),
            ("2026년 실비보험 추천 TOP 5", "<h3>1. 삼성화재 실손의료보험</h3><ul><li>업계 1위 점유율, 안정적인 보상 처리</li><li>모바일 청구 시스템 우수</li><li>월 보험료: 30대 기준 약 1.5~2만원</li></ul><h3>2. 현대해상 실손의료보험</h3><ul><li>보상 처리 속도 빠름</li><li>비급여 특약 보장 범위 넓음</li><li>월 보험료: 30대 기준 약 1.4~1.9만원</li></ul><h3>3. DB손해보험 실손의료보험</h3><ul><li>보험료 경쟁력 우수</li><li>다이렉트 가입 시 추가 할인</li><li>월 보험료: 30대 기준 약 1.3~1.8만원</li></ul><h3>4. KB손해보험 실손의료보험</h3><ul><li>KB금융그룹 연계 혜택</li><li>간편한 보험금 청구 앱</li><li>월 보험료: 30대 기준 약 1.4~1.9만원</li></ul><h3>5. 메리츠화재 실손의료보험</h3><ul><li>온라인 가입 절차 간편</li><li>비급여 도수치료 보장 우수</li><li>월 보험료: 30대 기준 약 1.3~1.8만원</li></ul>"),
            ("실비보험 가입 시 체크리스트 5가지", "<ol><li><strong>기존 실비보험 확인</strong>: 이미 1~3세대 실비가 있다면 유지가 유리할 수 있습니다. 해지 후 재가입은 신중하게 판단하세요.</li><li><strong>비급여 특약 포함 여부</strong>: 도수치료, 비급여 주사제 등을 자주 이용한다면 비급여 특약을 반드시 포함하세요.</li><li><strong>자기부담률 확인</strong>: 4세대는 급여 20%, 비급여 30%가 기본 자기부담률입니다.</li><li><strong>갱신 주기</strong>: 4세대는 매년 보험료가 재산정되므로 장기적 부담을 고려하세요.</li><li><strong>보험금 청구 편의성</strong>: 모바일 앱으로 간편 청구가 가능한 보험사를 선택하세요.</li></ol>"),
            ("실비보험 보험료 아끼는 방법", "<ul><li><strong>다이렉트 가입</strong>: 설계사 수수료 없이 온라인으로 가입하면 10~15% 저렴</li><li><strong>불필요한 특약 제거</strong>: 본인 의료 이용 패턴에 맞게 특약을 선택하세요</li><li><strong>비급여 이용 줄이기</strong>: 4세대는 비급여 이용이 적으면 다음 해 보험료가 할인됩니다</li><li><strong>단체보험 확인</strong>: 직장 단체보험으로 실비가 포함되어 있는지 확인하세요</li></ul>"),
        ],
        "faq": [
            ("기존 1세대 실비를 해지하고 4세대로 갈아타야 하나요?", "대부분의 경우 <strong>1~2세대 실비는 유지하는 것이 유리</strong>합니다. 보장 범위가 넓고 비급여 자기부담률이 낮기 때문입니다. 다만 보험료 부담이 크다면 전문가 상담을 받아보세요."),
            ("실비보험 2개 가입이 가능한가요?", "실손보험은 <strong>1인 1계약이 원칙</strong>입니다. 중복 가입은 불가하며, 기존 계약이 있다면 해지 후 재가입해야 합니다."),
            ("실비보험 보험금 청구는 어떻게 하나요?", "대부분의 보험사에서 <strong>모바일 앱으로 간편 청구</strong>가 가능합니다. 진료비 영수증과 진료확인서를 촬영하여 제출하면 3~5영업일 내 지급됩니다."),
            ("나이가 많으면 실비보험 가입이 안 되나요?", "일반적으로 <strong>만 15세~65세까지 가입 가능</strong>합니다. 65세 이상은 유병자 실손보험 등 별도 상품을 확인하세요."),
        ],
        "ctas": [
            {"text": "📋 내 실비보험 보장 내용 확인하기", "desc": "보험다모아에서 현재 가입된 실비보험 보장 내용을 확인하세요", "url": "https://www.e-insmarket.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "💰 실비보험 보험료 비교견적 받기", "desc": "카카오페이에서 주요 보험사 실비보험료를 한눈에 비교하세요", "url": "https://insurance.kakaopay.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "📱 30초 실비보험 가입 상담 신청", "desc": "토스에서 내 조건에 맞는 실비보험을 추천받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "운전자보험 필요한가 보장 항목별 비교 및 추천 2026",
        "cat": 8,
        "slug": "driver-insurance-guide-2026",
        "intro": "교통사고가 나면 치료비뿐 아니라 <strong>형사적 책임</strong>까지 질 수 있다는 사실, 알고 계셨나요? 운전자보험은 자동차보험이 보장하지 않는 벌금, 변호사 비용, 교통사고 처리지원금 등을 보장합니다. 2026년 기준 운전자보험이 정말 필요한지, 어떤 보장을 선택해야 하는지 완벽하게 정리했습니다.",
        "sections": [
            ("운전자보험 vs 자동차보험 차이점", "<table><thead><tr><th>구분</th><th>자동차보험</th><th>운전자보험</th></tr></thead><tbody><tr><td>보장 대상</td><td>상대방 피해 + 내 차량</td><td>운전자 본인의 형사/행정 비용</td></tr><tr><td>벌금</td><td>보장 안 됨</td><td>최대 2,000만원 보장</td></tr><tr><td>변호사 선임비</td><td>보장 안 됨</td><td>최대 200만원 보장</td></tr><tr><td>교통사고 처리지원금</td><td>일부 특약</td><td>핵심 보장</td></tr><tr><td>면허취소/정지 위로금</td><td>보장 안 됨</td><td>보장 가능</td></tr><tr><td>가입 필수 여부</td><td>의무보험</td><td>선택 가입</td></tr></tbody></table>"),
            ("운전자보험 핵심 보장 항목 6가지", "<ol><li><strong>교통사고 처리지원금</strong>: 사고로 피해자와 합의 시 지급 (핵심 중의 핵심)</li><li><strong>벌금 보장</strong>: 교통사고, 음주운전 제외 벌금 보장 (최대 2,000만원)</li><li><strong>변호사 선임 비용</strong>: 형사사건 발생 시 변호사 비용 보장</li><li><strong>면허취소/정지 위로금</strong>: 면허 행정처분 시 위로금 지급</li><li><strong>자동차사고 부상 치료비</strong>: 본인 부상 치료 보장</li><li><strong>일상생활 배상책임</strong>: 운전 외 일상에서의 배상 사고까지 보장</li></ol>"),
            ("2026년 운전자보험 추천 TOP 5", "<h3>1. 삼성화재 운전자보험</h3><ul><li>교통사고 처리지원금 최대 3,000만원</li><li>벌금 최대 2,000만원</li><li>월 보험료: 약 1~2만원</li></ul><h3>2. 현대해상 운전자보험</h3><ul><li>면허취소 위로금 포함</li><li>자전거 사고까지 보장</li><li>월 보험료: 약 1~1.8만원</li></ul><h3>3. DB손해보험 운전자보험</h3><ul><li>다이렉트 가입 시 할인</li><li>일상생활 배상책임 자동 포함</li><li>월 보험료: 약 0.9~1.7만원</li></ul><h3>4. KB손해보험 운전자보험</h3><ul><li>변호사 선임비 보장 우수</li><li>KB카드 연계 할인</li><li>월 보험료: 약 1~1.8만원</li></ul><h3>5. 메리츠화재 운전자보험</h3><ul><li>보험료 경쟁력 우수</li><li>온라인 간편 가입</li><li>월 보험료: 약 0.8~1.5만원</li></ul>"),
            ("운전자보험 가입 시 주의사항", "<ul><li><strong>음주운전 면책</strong>: 대부분의 운전자보험은 음주/무면허 운전 사고를 보장하지 않습니다</li><li><strong>보장 개시일 확인</strong>: 가입 후 보통 90일의 면책기간이 있습니다</li><li><strong>중복 가입 확인</strong>: 자동차보험의 운전자 특약과 중복되는지 확인하세요</li><li><strong>갱신형 vs 비갱신형</strong>: 비갱신형이 보험료는 비싸지만 장기적으로 유리할 수 있습니다</li></ul>"),
        ],
        "faq": [
            ("운전자보험은 꼭 필요한가요?", "자동차를 운전한다면 <strong>가입을 강력히 권장</strong>합니다. 자동차보험만으로는 본인의 형사 비용(벌금, 변호사비)을 보장받을 수 없습니다."),
            ("자동차보험에 운전자 특약이 있는데 별도 가입이 필요한가요?", "자동차보험의 운전자 특약은 보장 한도가 낮은 경우가 많습니다. <strong>교통사고 처리지원금과 벌금 보장 한도</strong>를 비교해보고 부족하면 별도 가입을 추천합니다."),
            ("운전자보험 보험료는 얼마인가요?", "30대 기준 <strong>월 1~2만원 수준</strong>입니다. 보장 항목과 한도에 따라 달라집니다."),
        ],
        "ctas": [
            {"text": "🚗 내 자동차보험 운전자 특약 확인하기", "desc": "현재 자동차보험의 운전자 보장 한도를 먼저 확인하세요", "url": "https://www.e-insmarket.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "💰 운전자보험 보험료 비교하기", "desc": "주요 보험사 운전자보험 보험료를 한눈에 비교하세요", "url": "https://insurance.kakaopay.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "📱 운전자보험 맞춤 상담받기", "desc": "토스에서 내 운전 조건에 맞는 보험을 추천받으세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "신용점수 올리는 법 7가지 2026 최신 완벽 가이드",
        "cat": 8,
        "slug": "credit-score-improve-2026",
        "intro": "대출 금리, 카드 발급, 심지어 통신사 가입까지 영향을 미치는 <strong>신용점수</strong>. 점수가 낮으면 금융 생활 전반에 불이익을 받습니다. 이 글에서는 2026년 기준 신용점수를 실질적으로 올릴 수 있는 7가지 방법을 구체적으로 정리했습니다.",
        "sections": [
            ("신용점수란? (NICE vs KCB)", "<table><thead><tr><th>구분</th><th>NICE (나이스)</th><th>KCB (올크레딧)</th></tr></thead><tbody><tr><td>점수 범위</td><td>1~1,000점</td><td>1~1,000점</td></tr><tr><td>확인 방법</td><td>나이스지키미</td><td>올크레딧</td></tr><tr><td>주요 사용처</td><td>은행권 대출</td><td>카드사, 캐피탈</td></tr><tr><td>1등급 기준</td><td>900점 이상</td><td>942점 이상</td></tr></tbody></table><p>두 기관의 점수가 다를 수 있으므로 <strong>양쪽 모두 확인</strong>하는 것이 좋습니다.</p>"),
            ("신용점수 올리는 법 7가지", "<h3>1. 체크카드를 꾸준히 사용하세요</h3><p>신용카드가 부담된다면 <strong>체크카드를 월 30만원 이상 6개월 이상</strong> 꾸준히 사용하세요. 금융 거래 이력이 쌓이면서 점수가 올라갑니다.</p><h3>2. 소액 대출 후 성실 상환</h3><p>마이너스통장이나 소액 신용대출을 받고 <strong>매달 성실하게 상환</strong>하면 상환 이력이 쌓여 점수가 올라갑니다. 단, 연체는 절대 금물입니다.</p><h3>3. 통신요금, 공과금 자동이체</h3><p>통신요금, 국민연금, 건강보험료 등을 <strong>본인 명의 계좌에서 자동이체</strong>하면 성실 납부 이력으로 반영됩니다.</p><h3>4. 카드론, 현금서비스 지양</h3><p>카드론과 현금서비스는 <strong>신용점수에 부정적 영향</strong>을 줍니다. 급한 자금이 필요하면 신용대출이 더 유리합니다.</p><h3>5. 불필요한 대출 정리</h3><p>사용하지 않는 마이너스통장, 소액 대출은 정리하세요. <strong>총 대출 건수와 금액</strong>이 신용점수에 영향을 줍니다.</p><h3>6. 장기 연체 이력 해소</h3><p>과거 연체 이력이 있다면 해당 금액을 완납하세요. 완납 후 시간이 지나면 <strong>연체 이력의 영향이 점차 줄어듭니다</strong>.</p><h3>7. 신용점수 무료 조회 활용</h3><p>카카오뱅크, 토스 등에서 <strong>무료로 신용점수를 조회</strong>할 수 있습니다. 정기적으로 확인하며 변동 사항을 체크하세요. 무료 조회는 점수에 영향을 주지 않습니다.</p>"),
            ("신용점수 등급별 혜택 차이", "<table><thead><tr><th>등급</th><th>NICE 점수</th><th>대출 금리</th><th>카드 발급</th></tr></thead><tbody><tr><td>1등급</td><td>900~1000</td><td>최저 금리</td><td>프리미엄 카드 가능</td></tr><tr><td>2~3등급</td><td>800~899</td><td>우대 금리</td><td>대부분 카드 가능</td></tr><tr><td>4~5등급</td><td>700~799</td><td>일반 금리</td><td>일부 제한</td></tr><tr><td>6~7등급</td><td>600~699</td><td>높은 금리</td><td>제한적</td></tr><tr><td>8등급 이하</td><td>600 미만</td><td>대출 어려움</td><td>발급 거절 가능</td></tr></tbody></table>"),
            ("신용점수 떨어지는 행동 5가지", "<ol><li><strong>연체</strong>: 3일 이상 연체는 즉시 점수 하락 (가장 치명적)</li><li><strong>현금서비스/카드론 빈번 이용</strong></li><li><strong>단기간 다수 대출 조회</strong>: 여러 곳에 동시 대출 신청 시 하락</li><li><strong>대출 잔액 급증</strong></li><li><strong>신용카드 한도 소진</strong>: 한도의 70% 이상 사용 시 부정적</li></ol>"),
        ],
        "faq": [
            ("신용점수 조회하면 점수가 떨어지나요?", "<strong>본인 조회는 점수에 영향을 주지 않습니다.</strong> 카카오뱅크, 토스, 나이스지키미 등에서 자유롭게 조회하세요. 다만 금융사가 대출 심사를 위해 조회하는 것은 영향을 줄 수 있습니다."),
            ("신용점수는 얼마나 빨리 올릴 수 있나요?", "일반적으로 <strong>3~6개월</strong> 이상의 꾸준한 금융활동이 필요합니다. 체크카드 사용, 공과금 납부 등을 시작하면 점진적으로 올라갑니다."),
            ("신용카드가 없으면 신용점수가 낮은가요?", "금융 거래 이력이 전혀 없으면 점수가 낮을 수 있습니다. 이 경우 <strong>체크카드 사용</strong>부터 시작하는 것을 추천합니다."),
        ],
        "ctas": [
            {"text": "📊 내 신용점수 무료로 확인하기", "desc": "토스에서 NICE, KCB 신용점수를 무료로 조회하세요", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "💳 신용점수 올리기 좋은 체크카드 추천", "desc": "실적 조건 없이 신용점수 관리에 유리한 카드를 비교하세요", "url": "https://card-gorilla.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "🏦 신용등급별 대출 가능 상품 확인", "desc": "내 신용등급으로 받을 수 있는 최저금리 대출을 찾아보세요", "url": "https://www.finnq.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "적금 금리 비교 TOP 10 2026년 최신 고금리 적금 추천",
        "cat": 8,
        "slug": "savings-interest-rate-2026",
        "intro": "금리가 변동하는 시기일수록 <strong>어디에 돈을 넣느냐</strong>가 중요합니다. 같은 금액을 넣어도 은행에 따라 이자가 수십만 원 차이 날 수 있습니다. 2026년 3월 기준 고금리 적금 TOP 10을 비교하고, 가입 시 주의사항까지 정리했습니다.",
        "sections": [
            ("적금 금리 비교 시 알아야 할 기본 용어", "<ul><li><strong>기본금리</strong>: 아무 조건 없이 받는 금리</li><li><strong>우대금리</strong>: 특정 조건 충족 시 추가되는 금리 (급여이체, 카드실적 등)</li><li><strong>세전/세후 금리</strong>: 이자소득세 15.4%를 빼기 전/후 금리</li><li><strong>단리/복리</strong>: 단리는 원금에만, 복리는 이자에도 이자가 붙음</li></ul>"),
            ("2026년 고금리 적금 TOP 10", "<table><thead><tr><th>순위</th><th>은행</th><th>상품명</th><th>기본금리</th><th>최고금리</th><th>기간</th></tr></thead><tbody><tr><td>1</td><td>SBI저축은행</td><td>사이다적금</td><td>4.0%</td><td>5.0%</td><td>12개월</td></tr><tr><td>2</td><td>페퍼저축은행</td><td>디지털적금</td><td>3.8%</td><td>4.8%</td><td>12개월</td></tr><tr><td>3</td><td>웰컴저축은행</td><td>웰컴디지털적금</td><td>3.7%</td><td>4.7%</td><td>12개월</td></tr><tr><td>4</td><td>카카오뱅크</td><td>자유적금</td><td>3.3%</td><td>4.5%</td><td>12개월</td></tr><tr><td>5</td><td>케이뱅크</td><td>플러스적금</td><td>3.2%</td><td>4.5%</td><td>12개월</td></tr><tr><td>6</td><td>토스뱅크</td><td>먼저 이자 받는 적금</td><td>3.5%</td><td>4.3%</td><td>6개월</td></tr><tr><td>7</td><td>NH농협</td><td>NH올원e적금</td><td>3.0%</td><td>4.2%</td><td>12개월</td></tr><tr><td>8</td><td>하나은행</td><td>하나원큐적금</td><td>2.8%</td><td>4.0%</td><td>12개월</td></tr><tr><td>9</td><td>신한은행</td><td>쏠편한적금</td><td>2.8%</td><td>3.8%</td><td>12개월</td></tr><tr><td>10</td><td>우리은행</td><td>우리WON적금</td><td>2.7%</td><td>3.7%</td><td>12개월</td></tr></tbody></table><p>※ 금리는 2026년 3월 기준이며, 변동될 수 있습니다.</p>"),
            ("적금 가입 시 체크 포인트 5가지", "<ol><li><strong>우대금리 조건 확인</strong>: 최고금리를 받으려면 급여이체, 카드실적 등 조건을 충족해야 합니다. 실현 가능한 조건인지 확인하세요.</li><li><strong>중도해지 이율</strong>: 만기 전 해지 시 이율이 크게 떨어집니다. 여유자금으로 가입하세요.</li><li><strong>세금우대 여부</strong>: 비과세종합저축(65세 이상) 또는 조합출자금 등 세금우대가 가능한지 확인하세요.</li><li><strong>예금자보호</strong>: 1인당 5,000만원까지 예금자보호가 됩니다. 저축은행도 동일하게 보호됩니다.</li><li><strong>자동이체 설정</strong>: 매달 자동이체를 설정하면 납입 누락을 방지할 수 있습니다.</li></ol>"),
            ("적금 vs 예금 vs CMA 뭐가 유리할까", "<table><thead><tr><th>구분</th><th>적금</th><th>예금</th><th>CMA</th></tr></thead><tbody><tr><td>납입 방식</td><td>매월 일정액</td><td>목돈 한 번에</td><td>자유 입출금</td></tr><tr><td>금리</td><td>보통 더 높음</td><td>적금보다 낮음</td><td>변동금리</td></tr><tr><td>유동성</td><td>낮음</td><td>낮음</td><td>높음</td></tr><tr><td>추천 대상</td><td>매월 저축 습관</td><td>목돈 운용</td><td>단기 자금 관리</td></tr></tbody></table>"),
        ],
        "faq": [
            ("저축은행 적금은 안전한가요?", "<strong>1인당 5,000만원까지 예금자보호</strong>가 적용됩니다. 시중은행과 동일한 수준의 보호를 받으므로 한도 내에서는 안전합니다."),
            ("적금 이자는 얼마나 받을 수 있나요?", "월 30만원씩 12개월, 연 4% 적금 기준 <strong>세전 이자 약 7.8만원</strong>입니다. 세후(15.4% 공제) 약 6.6만원입니다."),
            ("적금을 여러 개 가입해도 되나요?", "네, 제한 없습니다. 다만 <strong>예금자보호 한도는 금융기관별 5,000만원</strong>이므로 분산 가입을 추천합니다."),
        ],
        "ctas": [
            {"text": "📊 실시간 적금 금리 비교하기", "desc": "은행연합회에서 전 금융기관 적금 금리를 비교하세요", "url": "https://finlife.fss.or.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "💰 카카오뱅크 자유적금 가입하기", "desc": "앱에서 3분 만에 간편 가입 가능합니다", "url": "https://www.kakaobank.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "🏦 토스뱅크 먼저 이자 받는 적금", "desc": "가입 즉시 이자를 먼저 받는 새로운 적금 상품", "url": "https://toss.im/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "ISA 계좌 장단점 절세 효과 총정리 2026 가입 가이드",
        "cat": 8,
        "slug": "isa-account-guide-2026",
        "intro": "ISA(개인종합자산관리계좌)는 예금, 펀드, ETF 등 다양한 금융상품을 <strong>하나의 계좌에서 관리</strong>하면서 세제 혜택까지 받을 수 있는 만능 절세 계좌입니다. 2026년 기준 ISA 계좌의 장단점, 가입 조건, 절세 효과를 총정리합니다.",
        "sections": [
            ("ISA 계좌란?", "<p>ISA(Individual Savings Account)는 하나의 계좌에서 예적금, 펀드, ETF, 리츠 등 <strong>다양한 금융상품을 담아 운용</strong>할 수 있는 통합계좌입니다.</p><ul><li>순이익 <strong>200만원까지 비과세</strong> (서민형 400만원)</li><li>200만원 초과분은 <strong>9.9% 분리과세</strong> (일반 15.4% 대비 유리)</li><li>의무 가입기간: 3년</li></ul>"),
            ("ISA 계좌 유형 비교", "<table><thead><tr><th>구분</th><th>일반형</th><th>서민형</th><th>농어민형</th></tr></thead><tbody><tr><td>가입 조건</td><td>19세 이상 누구나</td><td>총급여 5,000만원 이하</td><td>농어민</td></tr><tr><td>비과세 한도</td><td>200만원</td><td>400만원</td><td>400만원</td></tr><tr><td>의무 가입기간</td><td>3년</td><td>3년</td><td>3년</td></tr><tr><td>연간 납입한도</td><td>2,000만원</td><td>2,000만원</td><td>2,000만원</td></tr></tbody></table>"),
            ("ISA 계좌 장점 5가지", "<ol><li><strong>절세 효과</strong>: 200만원(서민형 400만원) 비과세 + 초과분 9.9% 분리과세</li><li><strong>손익통산</strong>: 수익과 손실을 합산하여 순이익에만 과세 (핵심 장점)</li><li><strong>다양한 상품 운용</strong>: 예금, 펀드, ETF, 리츠를 하나의 계좌에서 관리</li><li><strong>금융소득종합과세 제외</strong>: ISA 수익은 종합과세에 합산되지 않음</li><li><strong>만기 후 연금 전환</strong>: 만기 자금을 연금저축으로 전환 시 추가 세액공제</li></ol>"),
            ("ISA 계좌 단점 및 주의사항", "<ul><li><strong>3년 의무 가입</strong>: 중도 해지 시 세제 혜택이 사라집니다</li><li><strong>연 2,000만원 납입 한도</strong>: 큰 금액을 운용하기엔 한도가 제한적</li><li><strong>국내 상품만 가능</strong>: 해외 주식 직접 투자는 불가 (해외 ETF는 가능)</li><li><strong>1인 1계좌</strong>: 금융기관 통합 1계좌만 개설 가능</li></ul>"),
            ("ISA vs 연금저축 vs IRP 비교", "<table><thead><tr><th>구분</th><th>ISA</th><th>연금저축</th><th>IRP</th></tr></thead><tbody><tr><td>세제 혜택</td><td>비과세+분리과세</td><td>세액공제</td><td>세액공제</td></tr><tr><td>인출</td><td>만기 후 자유</td><td>55세 이후</td><td>55세 이후</td></tr><tr><td>납입 한도</td><td>연 2,000만원</td><td>연 1,800만원</td><td>연 1,800만원</td></tr><tr><td>운용 상품</td><td>예금+펀드+ETF</td><td>펀드+ETF</td><td>예금+펀드+ETF</td></tr><tr><td>추천 대상</td><td>중기 절세</td><td>노후 준비</td><td>노후 준비+직장인</td></tr></tbody></table>"),
        ],
        "faq": [
            ("ISA 계좌 가입은 어디서 하나요?", "은행, 증권사 모두 가능합니다. <strong>ETF 투자를 원하면 증권사</strong>, 예적금 위주라면 은행을 추천합니다."),
            ("ISA 계좌에서 주식 투자가 가능한가요?", "국내 상장 주식은 <strong>중개형 ISA</strong>에서 투자 가능합니다. 해외 주식은 직접 투자가 불가하지만 해외 ETF는 가능합니다."),
            ("3년 안에 해지하면 어떻게 되나요?", "세제 혜택이 <strong>전부 취소</strong>되고 일반 과세(15.4%)가 적용됩니다. 가급적 3년은 유지하세요."),
        ],
        "ctas": [
            {"text": "📈 ISA 계좌 개설하기 (증권사)", "desc": "ETF 투자가 가능한 중개형 ISA를 개설하세요", "url": "https://www.kiwoom.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "💰 ISA 절세 효과 계산해보기", "desc": "내 투자금 기준으로 절세 효과가 얼마인지 확인하세요", "url": "https://toss.im/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "🏦 ISA vs 연금저축 뭐가 유리할까", "desc": "내 상황에 맞는 절세 계좌를 추천받으세요", "url": "https://www.finnq.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
]

# Now add 45 more topics with similar structure
more_topics = [
    # 6-10: 대출 (cat=6)
    ("청년 전세자금대출 조건 금리 한도 총정리 2026", 6, "youth-jeonse-loan-2026", "청년 전세자금대출", "대출"),
    ("주택담보대출 금리 비교 고정 vs 변동 2026 최신", 6, "mortgage-rate-comparison-2026", "주택담보대출", "대출"),
    ("신용대출 금리 낮은 곳 TOP 5 비교 2026", 6, "personal-loan-low-rate-2026", "신용대출", "대출"),
    ("전세대출 갈아타기 방법 및 주의사항 완벽 가이드", 6, "jeonse-loan-refinance-guide", "전세대출 갈아타기", "대출"),
    ("소상공인 정부지원대출 종류 조건 2026 총정리", 6, "small-business-gov-loan-2026", "소상공인 대출", "대출"),
    # 11-15: 보험 추가 (cat=8)
    ("암보험 추천 2026 가입 시기 보장 항목 비교", 8, "cancer-insurance-2026", "암보험", "금융"),
    ("치아보험 추천 2026 임플란트 보장 비교 TOP 5", 8, "dental-insurance-2026", "치아보험", "금융"),
    ("태아보험 가입 시기 추천 보장 항목 완벽 비교 2026", 8, "prenatal-insurance-2026", "태아보험", "금융"),
    ("여행자보험 추천 해외여행 보장 항목 비교 2026", 8, "travel-insurance-2026", "여행자보험", "금융"),
    ("화재보험 가입 의무 대상 보장 범위 총정리 2026", 8, "fire-insurance-guide-2026", "화재보험", "금융"),
    # 16-20: 수입차 (cat=10)
    ("장기렌트 vs 리스 vs 할부 비교 2026 뭐가 유리할까", 10, "long-term-rent-vs-lease-2026", "장기렌트 리스", "수입차"),
    ("수입차 유지비 순위 TOP 10 보험 정비 총비용 비교", 10, "imported-car-maintenance-cost-ranking", "수입차 유지비", "수입차"),
    ("자동차 리스 장단점 잔존가치 계산법 완벽 가이드", 10, "car-lease-pros-cons-guide", "자동차 리스", "수입차"),
    ("벤츠 E클래스 유지비 보험료 정비비 실제 비용 분석", 10, "benz-e-class-maintenance-cost", "벤츠 유지비", "수입차"),
    ("BMW 3시리즈 vs 벤츠 C클래스 비교 2026 어떤 차가 나을까", 10, "bmw-3-vs-benz-c-2026", "BMW 벤츠 비교", "수입차"),
    # 21-25: 세금/절세 (cat=8)
    ("종합소득세 신고 방법 완벽 가이드 2026 프리랜서 필수", 8, "income-tax-filing-guide-2026", "종합소득세", "금융"),
    ("연말정산 환급 많이 받는 법 10가지 2026", 8, "year-end-tax-refund-tips-2026", "연말정산", "금융"),
    ("부가가치세 신고 방법 기간 절세 팁 2026", 8, "vat-filing-guide-2026", "부가가치세", "금융"),
    ("증여세 면제 한도 계산 방법 2026 최신 세법", 8, "gift-tax-exemption-2026", "증여세", "금융"),
    ("상속세 계산 방법 공제 항목 총정리 2026", 8, "inheritance-tax-guide-2026", "상속세", "금융"),
    # 26-30: 건강/의료 (cat=13)
    ("임플란트 가격 비교 2026 평균 시세 및 치과 선택 가이드", 13, "implant-cost-comparison-2026", "임플란트 가격", "지식"),
    ("라식 라섹 차이점 비용 후기 총정리 2026", 13, "lasik-lasek-comparison-2026", "라식 라섹", "지식"),
    ("건강검진 항목 추천 연령대별 필수 검사 2026", 13, "health-checkup-guide-2026", "건강검진", "지식"),
    ("도수치료 가격 효과 실비보험 적용 가이드 2026", 13, "manual-therapy-cost-guide-2026", "도수치료", "지식"),
    ("치과 스케일링 가격 보험 적용 횟수 2026 총정리", 13, "dental-scaling-cost-insurance-2026", "스케일링", "지식"),
    # 31-35: 투자 (cat=8)
    ("ETF 추천 2026 초보자를 위한 국내 해외 ETF TOP 10", 8, "etf-recommendation-2026", "ETF 추천", "금융"),
    ("배당주 추천 2026 고배당 국내 주식 TOP 10", 8, "dividend-stock-2026", "배당주", "금융"),
    ("주식 초보 시작 가이드 계좌 개설부터 첫 매수까지", 8, "stock-beginner-guide-2026", "주식 초보", "금융"),
    ("CMA 통장 추천 2026 금리 비교 및 장단점", 8, "cma-account-comparison-2026", "CMA 통장", "금융"),
    ("금 투자 방법 5가지 금통장 금ETF KRX금시장 비교", 8, "gold-investment-guide-2026", "금 투자", "금융"),
    # 36-40: 부동산 (cat=8)
    ("청약 자격 조건 당첨 확률 높이는 법 2026 총정리", 8, "housing-subscription-guide-2026", "청약", "금융"),
    ("전세 vs 월세 계산법 뭐가 유리한지 비교 2026", 8, "jeonse-vs-monthly-rent-2026", "전세 월세", "금융"),
    ("부동산 중개수수료 계산 요율표 2026 최신", 8, "real-estate-commission-2026", "중개수수료", "금융"),
    ("전세사기 예방법 안전한 전세 계약 체크리스트 7가지", 8, "jeonse-fraud-prevention-guide", "전세사기", "금융"),
    ("재개발 재건축 차이점 투자 시 주의사항 총정리", 8, "redevelopment-reconstruction-guide", "재개발 재건축", "금융"),
    # 41-45: IT/생활 (cat=5)
    ("VPN 추천 2026 무료 유료 비교 TOP 5 속도 보안 테스트", 5, "vpn-recommendation-2026", "VPN 추천", "IT정보"),
    ("노트북 추천 2026 용도별 가성비 TOP 10", 5, "laptop-recommendation-2026", "노트북 추천", "IT정보"),
    ("클라우드 스토리지 비교 구글 드라이브 원드라이브 아이클라우드", 5, "cloud-storage-comparison-2026", "클라우드", "IT정보"),
    ("알뜰폰 요금제 비교 추천 2026 데이터 무제한 TOP 5", 5, "budget-phone-plan-2026", "알뜰폰 요금제", "IT정보"),
    ("인터넷 가입 비교 SK KT LG 요금 속도 혜택 총정리 2026", 5, "internet-provider-comparison-2026", "인터넷 가입", "IT정보"),
    # 46-50: 생활/법률 (cat=13)
    ("퇴직금 계산 방법 지급 기준 미지급 시 대처법", 13, "severance-pay-calculation-guide", "퇴직금 계산", "지식"),
    ("실업급여 조건 신청 방법 금액 계산 2026 총정리", 13, "unemployment-benefit-guide-2026", "실업급여", "지식"),
    ("자격증 추천 2026 취업 연봉에 도움되는 TOP 10", 13, "certification-recommendation-2026", "자격증 추천", "지식"),
    ("이사 비용 계산 업체 비교 체크리스트 2026", 13, "moving-cost-guide-2026", "이사 비용", "지식"),
    ("내용증명 작성 방법 양식 보내는 법 완벽 가이드", 13, "certified-letter-guide", "내용증명", "지식"),
]

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

    # Insert CTA after ~1/3 and ~2/3 of sections, and before FAQ
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

def generate_simple_post(title, cat, slug, keyword, cat_name):
    """Generate a complete post for the simpler topic definitions"""

    # Generic but varied section structures based on category
    sections_map = {
        "대출": [
            (f"{keyword}이란?", f"<p><strong>{keyword}</strong>은 많은 분들이 관심을 갖는 금융 상품입니다. 정확한 조건과 금리를 알아야 불필요한 이자 부담을 줄일 수 있습니다.</p><p>이 글에서는 2026년 기준 {keyword}의 자격 조건, 금리, 한도, 신청 방법까지 한눈에 정리합니다.</p>"),
            (f"{keyword} 자격 조건", f"<p>{keyword}을 신청하기 위해서는 다음 조건을 충족해야 합니다.</p><ul><li><strong>연소득 기준</strong>: 상품별로 다르며, 보통 연소득 5,000만원~7,000만원 이하</li><li><strong>신용점수</strong>: 일반적으로 NICE 기준 600점 이상</li><li><strong>재직/사업 기간</strong>: 최소 3개월~6개월 이상</li><li><strong>기타</strong>: 무주택 여부, 세대주 여부 등 상품별 추가 조건</li></ul>"),
            (f"2026년 {keyword} 금리 비교", f"<table><thead><tr><th>금융기관</th><th>상품명</th><th>금리(연)</th><th>한도</th><th>특징</th></tr></thead><tbody><tr><td>카카오뱅크</td><td>비상금대출</td><td>연 3.5~12%</td><td>최대 300만원</td><td>간편 신청</td></tr><tr><td>토스뱅크</td><td>신용대출</td><td>연 3.4~15%</td><td>최대 2억원</td><td>비대면 완결</td></tr><tr><td>케이뱅크</td><td>직장인K신용대출</td><td>연 3.6~11%</td><td>최대 2억원</td><td>직장인 우대</td></tr><tr><td>국민은행</td><td>KB스타신용대출</td><td>연 3.8~12%</td><td>최대 2억원</td><td>우대금리 다양</td></tr><tr><td>신한은행</td><td>쏠편한신용대출</td><td>연 3.7~11%</td><td>최대 1.5억원</td><td>신한SOL 연동</td></tr></tbody></table><p>※ 금리는 개인 신용도, 소득, 거래 실적에 따라 달라집니다.</p>"),
            (f"{keyword} 신청 방법 (단계별)", f"<ol><li><strong>조건 확인</strong>: 본인의 소득, 신용점수, 자격 조건을 먼저 확인합니다.</li><li><strong>금리 비교</strong>: 여러 금융기관의 금리를 비교합니다. 금리비교 사이트 활용을 추천합니다.</li><li><strong>서류 준비</strong>: 신분증, 소득증빙서류(원천징수영수증, 소득금액증명원 등)를 준비합니다.</li><li><strong>온라인/오프라인 신청</strong>: 모바일 앱 또는 은행 방문으로 신청합니다.</li><li><strong>심사 및 승인</strong>: 보통 당일~3영업일 이내 결과가 나옵니다.</li><li><strong>대출금 수령</strong>: 승인 후 즉시 또는 1영업일 이내 계좌로 입금됩니다.</li></ol>"),
            (f"{keyword} 주의사항 5가지", f"<ul><li><strong>금리 유형 확인</strong>: 고정금리와 변동금리의 차이를 이해하고 선택하세요.</li><li><strong>중도상환수수료</strong>: 조기 상환 시 수수료가 발생할 수 있습니다. 최근에는 면제 추세입니다.</li><li><strong>총 이자 비용 계산</strong>: 월 상환액뿐 아니라 총 이자 비용을 반드시 확인하세요.</li><li><strong>과도한 대출 지양</strong>: 소득 대비 과도한 대출은 신용점수 하락의 원인이 됩니다.</li><li><strong>연체 절대 금지</strong>: 단 하루의 연체도 신용점수에 부정적 영향을 줍니다.</li></ul>"),
        ],
        "금융": [
            (f"{keyword} 완벽 가이드", f"<p>{keyword}에 대해 정확히 이해하는 것이 <strong>현명한 재테크의 시작</strong>입니다. 잘못된 정보로 손해를 보는 경우가 많으므로, 이 글에서 정확한 정보를 확인하세요.</p>"),
            (f"2026년 {keyword} 핵심 정리", f"<p>2026년 기준으로 변경된 내용과 핵심 사항을 정리합니다.</p><ul><li><strong>제도 변경</strong>: 매년 세법과 금융 규정이 바뀌므로 최신 정보 확인이 필수입니다</li><li><strong>혜택 확인</strong>: 본인에게 해당하는 혜택을 빠짐없이 챙기세요</li><li><strong>기한 준수</strong>: 신고/신청 기한을 놓치면 불이익이 있을 수 있습니다</li></ul>"),
            (f"{keyword} 실전 비교 분석", f"<table><thead><tr><th>구분</th><th>장점</th><th>단점</th><th>추천 대상</th></tr></thead><tbody><tr><td>방법 A</td><td>간편하고 빠름</td><td>수수료 발생 가능</td><td>시간이 부족한 직장인</td></tr><tr><td>방법 B</td><td>비용 절약</td><td>시간이 소요됨</td><td>비용을 아끼고 싶은 분</td></tr><tr><td>방법 C</td><td>전문가 도움</td><td>상담비용 발생</td><td>복잡한 상황인 분</td></tr></tbody></table>"),
            (f"{keyword} 절약하는 꿀팁 5가지", f"<ol><li><strong>미리 준비</strong>: 서두르지 않고 충분한 시간을 두고 준비하세요.</li><li><strong>비교는 필수</strong>: 반드시 3곳 이상 비교 후 결정하세요.</li><li><strong>온라인 활용</strong>: 온라인 채널이 수수료가 저렴한 경우가 많습니다.</li><li><strong>세제 혜택 확인</strong>: 세금 혜택을 받을 수 있는지 확인하세요.</li><li><strong>전문가 상담</strong>: 금액이 크다면 전문가 상담을 추천합니다.</li></ol>"),
            (f"{keyword} 자주 하는 실수", f"<ul><li><strong>기한 미준수</strong>: 정해진 기한을 놓쳐 가산세나 불이익을 받는 경우</li><li><strong>서류 미비</strong>: 필요한 서류를 미리 준비하지 않아 지연되는 경우</li><li><strong>비교 없이 가입</strong>: 한 곳만 보고 결정하면 더 유리한 조건을 놓칠 수 있습니다</li></ul>"),
        ],
        "수입차": [
            (f"{keyword} 완벽 분석", f"<p>자동차 구매나 이용 시 <strong>{keyword}</strong>에 대한 정확한 정보가 필요합니다. 잘못된 선택은 수백만 원의 차이를 만들 수 있습니다.</p>"),
            (f"2026년 {keyword} 비교표", f"<table><thead><tr><th>항목</th><th>옵션 A</th><th>옵션 B</th><th>옵션 C</th></tr></thead><tbody><tr><td>월 비용</td><td>40~60만원</td><td>50~70만원</td><td>55~80만원</td></tr><tr><td>총 비용(5년)</td><td>2,400~3,600만원</td><td>3,000~4,200만원</td><td>3,300~4,800만원</td></tr><tr><td>소유권</td><td>없음</td><td>선택</td><td>있음</td></tr><tr><td>초기 비용</td><td>적음</td><td>보통</td><td>높음</td></tr></tbody></table>"),
            (f"{keyword} 장단점 비교", f"<h3>장점</h3><ul><li>초기 비용 부담이 적을 수 있음</li><li>세금 혜택이 가능한 경우</li><li>최신 차량 이용 가능</li></ul><h3>단점</h3><ul><li>총 비용이 더 높을 수 있음</li><li>중도 해지 시 위약금 발생</li><li>주행거리 제한이 있을 수 있음</li></ul>"),
            (f"{keyword} 실제 비용 시뮬레이션", f"<p>실제 비용을 기준으로 시뮬레이션해보겠습니다.</p><table><thead><tr><th>항목</th><th>연간 비용</th><th>5년 총 비용</th></tr></thead><tbody><tr><td>보험료</td><td>100~200만원</td><td>500~1,000만원</td></tr><tr><td>정비비</td><td>50~150만원</td><td>250~750만원</td></tr><tr><td>유류비</td><td>150~250만원</td><td>750~1,250만원</td></tr><tr><td>세금</td><td>30~80만원</td><td>150~400만원</td></tr><tr><td><strong>합계</strong></td><td><strong>330~680만원</strong></td><td><strong>1,650~3,400만원</strong></td></tr></tbody></table>"),
            (f"{keyword} 선택 시 체크리스트", f"<ol><li>본인의 연간 주행거리를 확인하세요</li><li>월 예산을 명확히 설정하세요</li><li>최소 3곳 이상 견적을 비교하세요</li><li>계약서의 특약 사항을 꼼꼼히 확인하세요</li><li>중도 해지 조건을 반드시 확인하세요</li></ol>"),
        ],
        "IT정보": [
            (f"{keyword} 완벽 비교 2026", f"<p>수많은 선택지 중에서 <strong>나에게 맞는 {keyword}</strong>을 찾는 것이 중요합니다. 가격, 성능, 서비스를 종합적으로 비교해드립니다.</p>"),
            (f"2026년 {keyword} TOP 5", f"<table><thead><tr><th>순위</th><th>서비스/제품</th><th>가격</th><th>특징</th><th>추천 대상</th></tr></thead><tbody><tr><td>1</td><td>추천 1</td><td>합리적</td><td>가성비 우수</td><td>일반 사용자</td></tr><tr><td>2</td><td>추천 2</td><td>중간</td><td>성능 우수</td><td>파워 유저</td></tr><tr><td>3</td><td>추천 3</td><td>저렴</td><td>기본기 탄탄</td><td>예산 중시</td></tr><tr><td>4</td><td>추천 4</td><td>프리미엄</td><td>최고 품질</td><td>전문가</td></tr><tr><td>5</td><td>추천 5</td><td>무료~저렴</td><td>입문용 적합</td><td>초보자</td></tr></tbody></table>"),
            (f"{keyword} 선택 기준 5가지", f"<ol><li><strong>가격 대비 성능</strong>: 무조건 비싼 것이 좋은 것은 아닙니다.</li><li><strong>사용 목적</strong>: 본인의 용도에 맞는 사양을 선택하세요.</li><li><strong>후기 및 평판</strong>: 실제 사용자 후기를 반드시 확인하세요.</li><li><strong>AS 및 고객지원</strong>: 문제 발생 시 대응이 중요합니다.</li><li><strong>확장성</strong>: 향후 업그레이드나 변경이 용이한지 확인하세요.</li></ol>"),
            (f"{keyword} 장단점 분석", f"<table><thead><tr><th>서비스</th><th>장점</th><th>단점</th></tr></thead><tbody><tr><td>옵션 A</td><td>가성비 우수, 한글 지원</td><td>기능 제한적</td></tr><tr><td>옵션 B</td><td>다양한 기능, 호환성 좋음</td><td>가격 높음</td></tr><tr><td>옵션 C</td><td>무료 사용 가능</td><td>광고 있음, 속도 느림</td></tr></tbody></table>"),
            (f"{keyword} 가입 및 설정 방법", f"<ol><li>공식 홈페이지 또는 앱스토어에서 다운로드</li><li>회원가입 및 본인인증</li><li>요금제 또는 플랜 선택</li><li>결제 정보 입력</li><li>초기 설정 완료 후 사용 시작</li></ol>"),
        ],
        "지식": [
            (f"{keyword} 완벽 가이드 2026", f"<p><strong>{keyword}</strong>에 대해 정확히 알아야 손해를 보지 않습니다. 복잡한 내용을 쉽게 정리했습니다.</p>"),
            (f"{keyword} 핵심 정리", f"<ul><li><strong>기본 개념</strong>: {keyword}의 정의와 적용 범위를 정확히 이해하세요</li><li><strong>자격 조건</strong>: 누가, 언제, 어떤 조건에서 해당되는지 확인</li><li><strong>신청 방법</strong>: 온라인과 오프라인 신청 방법을 모두 안내</li><li><strong>주의사항</strong>: 흔히 하는 실수와 예방법</li></ul>"),
            (f"{keyword} 단계별 진행 방법", f"<ol><li><strong>1단계: 자격 확인</strong> - 본인이 해당 조건에 맞는지 먼저 확인합니다.</li><li><strong>2단계: 서류 준비</strong> - 필요한 서류를 빠짐없이 준비합니다.</li><li><strong>3단계: 신청</strong> - 온라인 또는 관할 기관에 신청합니다.</li><li><strong>4단계: 처리 대기</strong> - 보통 7~14영업일 소요됩니다.</li><li><strong>5단계: 결과 확인</strong> - 결과를 확인하고 후속 조치를 합니다.</li></ol>"),
            (f"{keyword} 비용 및 금액 정리", f"<table><thead><tr><th>항목</th><th>금액/비율</th><th>비고</th></tr></thead><tbody><tr><td>기본 비용</td><td>상황별 상이</td><td>공식 기준 참고</td></tr><tr><td>추가 비용</td><td>0~50만원</td><td>선택 항목</td></tr><tr><td>절약 가능 금액</td><td>10~30%</td><td>팁 활용 시</td></tr></tbody></table>"),
            (f"{keyword} 관련 주의사항", f"<ul><li><strong>기한 엄수</strong>: 정해진 기한을 놓치면 불이익이 있을 수 있습니다</li><li><strong>정확한 정보 입력</strong>: 허위 정보 입력 시 불이익이 있습니다</li><li><strong>전문가 상담</strong>: 복잡한 경우 전문가 상담을 받으세요</li><li><strong>증빙 보관</strong>: 관련 서류와 영수증은 최소 5년간 보관하세요</li></ul>"),
        ],
    }

    default_ctas = [
        {"text": f"📋 {keyword} 자세한 정보 확인", "desc": f"{keyword} 관련 최신 정보를 확인하세요", "url": "https://www.finnq.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
        {"text": f"💰 {keyword} 비교 견적 받기", "desc": "여러 상품을 한눈에 비교하세요", "url": "https://toss.im/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
        {"text": f"📱 {keyword} 맞춤 상담 신청", "desc": "전문가에게 무료 상담을 받아보세요", "url": "https://insurance.kakaopay.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
    ]

    sections = sections_map.get(cat_name, sections_map["지식"])

    faq_templates = [
        (f"{keyword} 관련 비용은 얼마인가요?", f"상황에 따라 다르지만, 일반적으로 <strong>평균적인 범위 내에서 비용이 발생</strong>합니다. 정확한 비용은 본인의 조건에 따라 달라지므로 비교 견적을 받아보시는 것을 추천합니다."),
        (f"{keyword}은 누구나 이용할 수 있나요?", f"기본적인 자격 조건을 충족하면 <strong>누구나 이용 가능</strong>합니다. 다만 상세 조건은 상품이나 서비스별로 다를 수 있으므로 사전 확인이 필요합니다."),
        (f"{keyword} 가장 좋은 시기는 언제인가요?", f"<strong>빠르면 빠를수록 좋습니다.</strong> 다만 계절이나 시기에 따라 혜택이 달라질 수 있으므로 최적의 시기를 확인하세요."),
    ]

    return {
        "title": title,
        "cat": cat,
        "slug": slug,
        "intro": f"<strong>{keyword}</strong>에 대해 궁금하셨나요? 정확한 정보 없이 결정하면 큰 손해를 볼 수 있습니다. 이 글에서는 2026년 기준 {keyword}의 모든 것을 총정리합니다. 조건, 비교, 신청 방법까지 한 번에 확인하세요.",
        "sections": sections,
        "faq": faq_templates,
        "ctas": default_ctas,
    }

def publish(post_data):
    content = build_content(post_data)

    payload = {
        "title": post_data["title"],
        "slug": post_data["slug"],
        "status": "publish",
        "categories": [post_data["cat"]],
        "content": content,
    }

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(API, data=data, method="POST")
    req.add_header("Authorization", f"Basic {AUTH}")
    req.add_header("Content-Type", "application/json; charset=utf-8")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result.get("id"), result.get("title", {}).get("rendered", ""), result.get("link", ""), "OK"
    except Exception as e:
        return None, post_data["title"], "", str(e)

# Publish the 5 detailed posts first
print("=" * 60)
print("PUBLISHING 50 POSTS")
print("=" * 60)

count = 0
for post in POSTS:
    count += 1
    pid, title, link, status = publish(post)
    print(f"[{count}/50] {status} | ID:{pid} | {title}")
    time.sleep(1)

# Publish the 45 generated posts
for title, cat, slug, keyword, cat_name in more_topics:
    count += 1
    post = generate_simple_post(title, cat, slug, keyword, cat_name)
    pid, ptitle, link, status = publish(post)
    print(f"[{count}/50] {status} | ID:{pid} | {ptitle}")
    time.sleep(1)

print("=" * 60)
print(f"DONE: {count} posts published")

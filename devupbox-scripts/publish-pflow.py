import json
import urllib.request
import urllib.error
import base64
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API = "https://devupbox.com/wp-json/wp/v2/posts"

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

PF = "https://pflow.app"
PFA = f'<a href="{PF}" target="_blank" rel="noopener noreferrer">pflow.app</a>'
PFN = f'<a href="{PF}" target="_blank" rel="noopener noreferrer"><strong>피플로(PFlow)</strong></a>'

content = f'''<p style="font-size:17px;line-height:1.8;">주식 투자를 하면서 여러 앱과 사이트를 번갈아 써본 경험이 있으신가요? 국내 주식은 이 앱, 해외 주식은 저 앱, 암호화폐는 또 다른 앱... 이런 불편함을 한 번에 해결해주는 <strong>무료 투자 분석 플랫폼</strong>이 있습니다. 바로 {PFN}입니다. 국내외 주식부터 암호화폐까지, AI 기반 분석과 다양한 투자 계산기를 <strong>완전 무료</strong>로 제공하는 피플로의 주요 기능과 활용법을 총정리합니다.</p>

<h2>피플로(PFlow)란?</h2>
<p>{PFN}는 <strong>국내·해외 주식, 암호화폐를 실시간으로 분석</strong>할 수 있는 통합 투자 플랫폼입니다. "복잡한 금융 시장의 흐름을 한눈에"라는 슬로건 아래, 개인 투자자들이 쉽고 빠르게 시장을 파악할 수 있도록 설계되었습니다.</p>
<table><thead><tr><th>항목</th><th>내용</th></tr></thead><tbody>
<tr><td>서비스명</td><td>피플로 (PFlow)</td></tr>
<tr><td>주요 기능</td><td>실시간 시세, AI 분석, 투자 계산기, 포트폴리오 관리</td></tr>
<tr><td>지원 자산</td><td>국내주식(코스피·코스닥), 해외주식(나스닥·S&amp;P500), 암호화폐</td></tr>
<tr><td>가격</td><td>완전 무료</td></tr>
<tr><td>플랫폼</td><td>웹 + PWA 앱 (별도 설치 없이 바로 사용)</td></tr>
<tr><td>언어</td><td>한국어, 영어</td></tr>
<tr><td>사이트</td><td>{PFA}</td></tr>
</tbody></table>

{cta_block("피플로(PFlow) 바로가기", "국내외 주식·코인 실시간 분석을 무료로 시작하세요", PF, "blue")}

<h2>피플로 핵심 기능 5가지</h2>

<h3>1. 실시간 시세 조회 (1,900개+ 종목)</h3>
<p>피플로에서는 <strong>코스피·코스닥 전 종목</strong>, 나스닥·S&amp;P 500 주요 종목, 업비트 KRW 마켓 암호화폐의 실시간 시세를 한 화면에서 확인할 수 있습니다. 별도 앱 설치 없이 웹 브라우저에서 바로 접속하면 됩니다.</p>
<table><thead><tr><th>시장</th><th>종목 수</th><th>데이터</th></tr></thead><tbody>
<tr><td>코스피</td><td>800개+</td><td>실시간 시세, 거래량, 등락률</td></tr>
<tr><td>코스닥</td><td>1,100개+</td><td>실시간 시세, 거래량, 등락률</td></tr>
<tr><td>나스닥 / S&amp;P 500</td><td>주요 종목</td><td>실시간 시세 (USD/KRW)</td></tr>
<tr><td>암호화폐 (업비트)</td><td>KRW 마켓 전체</td><td>실시간 시세, 김치프리미엄</td></tr>
</tbody></table>

<h3>2. AI 기반 종목 분석</h3>
<p>피플로의 가장 큰 강점은 <strong>AI가 자동으로 기술적 분석을 해석</strong>해준다는 점입니다. 이동평균선, RSI, MACD 등 복잡한 지표를 AI가 분석하여 <strong>매수·매도 신호</strong>를 알기 쉽게 제공합니다. 초보 투자자도 전문가 수준의 차트 분석 결과를 한눈에 파악할 수 있습니다.</p>
<ul>
<li><strong>기술적 지표 자동 해석</strong>: 이동평균선, 볼린저밴드, RSI, MACD 등</li>
<li><strong>매수·매도 시그널</strong>: AI가 판단한 매매 신호 제공</li>
<li><strong>뉴스 센티먼트 분석</strong>: 관련 뉴스의 긍정/부정 감성 분석</li>
<li><strong>종목 비교 분석</strong>: 2개 이상 종목을 나란히 비교</li>
</ul>

<h3>3. 투자 계산기 모음</h3>
<p>투자 시 꼭 필요한 다양한 계산기를 <strong>무료</strong>로 제공합니다. 특히 물타기 계산기와 양도소득세 계산기는 실제 투자자들이 가장 많이 찾는 기능입니다.</p>
<table><thead><tr><th>계산기</th><th>기능</th><th>활용 상황</th></tr></thead><tbody>
<tr><td><a href="{PF}/ko/calculator/averaging-down" target="_blank" rel="noopener noreferrer">물타기 계산기</a></td><td>추가 매수 시 평균 단가 계산</td><td>하락장에서 물타기 판단</td></tr>
<tr><td>수익률 계산기</td><td>매수·매도가 기준 손익 계산</td><td>수익 실현 전 시뮬레이션</td></tr>
<tr><td>배당금 계산기</td><td>배당수익률 기반 예상 배당금</td><td>배당주 투자 계획</td></tr>
<tr><td>복리 계산기</td><td>장기 투자 복리 수익 시뮬레이션</td><td>적립식 투자 계획 수립</td></tr>
<tr><td>환율 계산기</td><td>49개 통화 실시간 환율 변환</td><td>해외주식 투자금 환산</td></tr>
<tr><td>양도소득세 계산기</td><td>국내·해외·가상자산 세금 계산</td><td>연말 세금 정산 준비</td></tr>
</tbody></table>

{cta_block("물타기 계산기 사용하기", "주식 추가 매수 시 평균 단가를 바로 계산해보세요", PF + "/ko/calculator/averaging-down", "yellow")}

<h3>4. 배당 캘린더 &amp; 경제 캘린더</h3>
<p><strong>배당 캘린더</strong>에서는 국내외 주요 기업의 배당 일정(배당기준일, 지급일, 배당수익률)을 한눈에 확인할 수 있습니다. <strong>경제 캘린더</strong>에서는 FOMC 회의, 고용지표 발표, 금리 결정 등 글로벌 경제 이벤트 일정을 제공하여 투자 타이밍을 잡는 데 도움을 줍니다.</p>

<h3>5. 포트폴리오 트래커</h3>
<p>보유 종목을 등록하면 <strong>전체 포트폴리오의 수익률, 자산 배분, 손익</strong>을 실시간으로 추적할 수 있습니다. 국내주식, 해외주식, 암호화폐를 하나의 포트폴리오에서 통합 관리할 수 있어 분산 투자자에게 특히 유용합니다.</p>

<h2>피플로 vs 다른 투자 앱 비교</h2>
<table><thead><tr><th>기능</th><th>피플로</th><th>증권사 앱</th><th>코인 거래소</th></tr></thead><tbody>
<tr><td>국내주식 시세</td><td>O</td><td>O</td><td>X</td></tr>
<tr><td>해외주식 시세</td><td>O</td><td>O (일부)</td><td>X</td></tr>
<tr><td>암호화폐 시세</td><td>O</td><td>X</td><td>O</td></tr>
<tr><td>AI 분석</td><td>O</td><td>X</td><td>X</td></tr>
<tr><td>투자 계산기</td><td>6종+</td><td>일부</td><td>X</td></tr>
<tr><td>포트폴리오 통합</td><td>주식+코인 통합</td><td>자사 종목만</td><td>코인만</td></tr>
<tr><td>김치프리미엄</td><td>O</td><td>X</td><td>일부</td></tr>
<tr><td>가격</td><td>무료</td><td>무료 (거래 시 수수료)</td><td>무료 (거래 시 수수료)</td></tr>
</tbody></table>

{cta_block("피플로에서 AI 종목 분석 받기", "관심 종목의 AI 기술 분석과 매매 신호를 무료로 확인하세요", PF, "green")}

<h2>피플로 시작하는 방법</h2>
<ol>
<li><strong>{PFA} 접속</strong> (PC, 모바일 모두 가능)</li>
<li><strong>회원가입</strong> (이메일 또는 소셜 로그인)</li>
<li><strong>관심 종목 등록</strong>하고 실시간 시세 확인</li>
<li><strong>AI 분석 탭</strong>에서 기술적 분석 결과 확인</li>
<li><strong>포트폴리오</strong>에 보유 종목 등록하여 통합 관리 시작</li>
</ol>
<p>별도 앱 설치 없이 웹 브라우저에서 바로 사용할 수 있으며, 모바일에서는 <strong>PWA(홈 화면 추가)</strong>로 앱처럼 사용할 수 있습니다.</p>

<h2>이런 분들에게 추천합니다</h2>
<ul>
<li><strong>투자 초보자</strong>: AI가 복잡한 차트를 해석해주니 전문 지식 없이도 활용 가능</li>
<li><strong>국내+해외 분산 투자자</strong>: 한 플랫폼에서 코스피, 나스닥, 코인까지 통합 조회</li>
<li><strong>배당주 투자자</strong>: 배당 캘린더와 배당금 계산기로 배당 전략 수립</li>
<li><strong>절세가 필요한 투자자</strong>: 양도소득세 계산기로 매도 전 세금 시뮬레이션</li>
<li><strong>비용에 민감한 투자자</strong>: 유료 구독 없이 모든 기능 무료 사용</li>
</ul>

<h2>자주 묻는 질문 (FAQ)</h2>
<h3>Q. 피플로는 정말 무료인가요?</h3>
<p>A. 네, <strong>모든 기능이 완전 무료</strong>입니다. 프리미엄 요금제나 숨겨진 비용이 없습니다. 실시간 시세, AI 분석, 투자 계산기, 포트폴리오 트래커까지 무료로 이용할 수 있습니다.</p>

<h3>Q. 피플로에서 직접 주식을 매매할 수 있나요?</h3>
<p>A. 피플로는 <strong>분석 전용 플랫폼</strong>입니다. 직접 매매 기능은 제공하지 않으며, 시세 조회·분석·계산 도구를 통해 투자 의사결정을 도와줍니다. 실제 매매는 증권사 앱이나 거래소를 이용하시면 됩니다.</p>

<h3>Q. 모바일에서도 사용할 수 있나요?</h3>
<p>A. 네, 모바일 웹 브라우저에서 {PFA}에 접속하면 됩니다. 더 편하게 사용하려면 <strong>홈 화면에 추가(PWA)</strong>하면 앱처럼 사용할 수 있습니다.</p>

<h3>Q. 데이터는 실시간인가요?</h3>
<p>A. 국내주식은 <strong>실시간 시세</strong>를 제공하며, 해외주식과 암호화폐도 실시간으로 업데이트됩니다. 환율 정보는 49개 통화를 실시간으로 지원합니다.</p>

<h3>Q. AI 분석은 얼마나 정확한가요?</h3>
<p>A. AI 분석은 기술적 지표와 뉴스 센티먼트를 기반으로 한 <strong>참고용 분석 도구</strong>입니다. 투자 의사결정에 도움을 주지만, 최종 판단은 본인이 내려야 합니다. 여러 지표를 종합적으로 참고하시는 것을 권장합니다.</p>

{cta_block("피플로(PFlow) 무료로 시작하기", "국내외 주식·코인 통합 분석 플랫폼을 지금 바로 체험하세요", PF, "blue")}

<h2>마무리</h2>
<p>피플로(PFlow)는 국내외 주식과 암호화폐를 한 곳에서 분석할 수 있는 <strong>무료 통합 투자 플랫폼</strong>입니다. AI 기반 종목 분석, 다양한 투자 계산기, 실시간 시세 조회까지 별도 비용 없이 사용할 수 있어 초보 투자자부터 경험 많은 투자자까지 유용하게 활용할 수 있습니다. {PFA}에 접속해서 직접 체험해보세요.</p>'''

# 발행
payload = {
    "title": "피플로(PFlow) 무료 주식 코인 AI 분석 플랫폼 기능 총정리",
    "content": content,
    "status": "publish",
    "slug": "pflow-free-stock-crypto-ai-analysis",
    "categories": [8],
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(API, data=data, method="POST")
req.add_header("Authorization", f"Basic {AUTH}")
req.add_header("Content-Type", "application/json")
with urllib.request.urlopen(req, timeout=30) as resp:
    r = json.loads(resp.read().decode())
    pid = r.get("id")
    link = r.get("link", "")
    print(f"WordPress OK | ID:{pid} | {link}")

# IndexNow
if link:
    naver_payload = {
        "host": "devupbox.com",
        "key": "8dbbd7d6729b4a65b7dce4b9083c65e3",
        "keyLocation": "https://devupbox.com/8dbbd7d6729b4a65b7dce4b9083c65e3.txt",
        "urlList": [link]
    }
    ndata = json.dumps(naver_payload).encode("utf-8")
    for name, url in [("Naver", "https://searchadvisor.naver.com/indexnow"), ("Bing", "https://www.bing.com/indexnow"), ("Yandex", "https://yandex.com/indexnow")]:
        req2 = urllib.request.Request(url, data=ndata, method="POST")
        req2.add_header("Content-Type", "application/json; charset=utf-8")
        try:
            with urllib.request.urlopen(req2, timeout=30) as resp2:
                print(f"  {name}: HTTP {resp2.status}")
        except urllib.error.HTTPError as e:
            print(f"  {name}: HTTP {e.code}")
        except Exception as e:
            print(f"  {name}: {e}")

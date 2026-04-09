import json, urllib.request, urllib.error, base64, time, ssl, os, tempfile

ssl._create_default_https_context = ssl._create_unverified_context
AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API = "https://devupbox.com/wp-json/wp/v2/posts"
MEDIA_API = "https://devupbox.com/wp-json/wp/v2/media"
CAT_IT = 5
UPLOADED_IMAGES = {}

IMAGES = {
    "claude-ai-beginner-guide": [("photo-1677442136019-21780ecad995", "클로드 AI 사용법 가이드"), ("photo-1655720828018-edd2daec9349", "AI 챗봇 인터페이스")],
    "claude-vs-chatgpt": [("photo-1655720828018-edd2daec9349", "클로드 vs ChatGPT 비교"), ("photo-1677442136019-21780ecad995", "AI 모델 성능 비교")],
    "claude-pricing-free-plan": [("photo-1579532537598-459ecdaf39cc", "클로드 요금제 비교"), ("photo-1611974789855-9c2a0a7236a3", "AI 서비스 가격 분석")],
    "claude-prompt-tips": [("photo-1516321318423-f06f85e504b3", "클로드 프롬프트 작성 팁"), ("photo-1677442136019-21780ecad995", "AI 프롬프트 엔지니어링")],
    "claude-blog-writing": [("photo-1499750310107-5fef28a66643", "클로드로 블로그 글쓰기"), ("photo-1486312338219-ce68d2c6f44d", "AI 블로그 콘텐츠 작성")],
    "claude-api-guide": [("photo-1504639725590-34d0984388bd", "클로드 API 개발 가이드"), ("photo-1488590528505-98d2b5aba04b", "API 코딩 개발 환경")],
    "claude-code-guide": [("photo-1488590528505-98d2b5aba04b", "클로드 코드 터미널 AI"), ("photo-1504639725590-34d0984388bd", "AI 코딩 어시스턴트")],
    "claude-pdf-summary": [("photo-1586281380349-632531db7ed4", "클로드 PDF 문서 요약"), ("photo-1450101499163-c8848c66ca85", "긴 문서 AI 분석")],
    "claude-work-productivity": [("photo-1497215728101-856f4ea42174", "클로드 업무 활용 오피스"), ("photo-1521737711867-e3b97375f902", "AI 업무 자동화 팀")],
    "claude-korean-review": [("photo-1677442136019-21780ecad995", "클로드 한국어 성능 테스트"), ("photo-1563013544-824ae1b704d3", "AI 한국어 사용 후기")],
}


def download_image(photo_id):
    url = f"https://images.unsplash.com/{photo_id}?w=800&h=450&fit=crop&auto=format&q=80"
    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    try:
        req = urllib.request.Request(url); req.add_header("User-Agent", "Mozilla/5.0")
        with urllib.request.urlopen(req, timeout=30) as resp: tmp.write(resp.read())
        tmp.close(); return tmp.name
    except Exception as e:
        tmp.close(); os.unlink(tmp.name); print(f"  이미지 실패 ({photo_id}): {e}"); return None

def upload_image_to_wp(file_path, filename, alt_text):
    with open(file_path, "rb") as f: image_data = f.read()
    req = urllib.request.Request(MEDIA_API, data=image_data, method="POST")
    req.add_header("Authorization", f"Basic {AUTH}"); req.add_header("Content-Type", "image/jpeg")
    req.add_header("Content-Disposition", f'attachment; filename="{filename}.jpg"')
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode())
            mid, murl = result.get("id"), result.get("source_url", "")
            if mid and alt_text:
                ur = urllib.request.Request(f"{MEDIA_API}/{mid}", data=json.dumps({"alt_text": alt_text}).encode(), method="POST")
                ur.add_header("Authorization", f"Basic {AUTH}"); ur.add_header("Content-Type", "application/json")
                try: urllib.request.urlopen(ur, timeout=15)
                except: pass
            return mid, murl
    except Exception as e: print(f"  WP 업로드 실패: {e}"); return None, None

def upload_all_images():
    total = sum(len(v) for v in IMAGES.values()); up = fail = 0
    print(f"{'='*60}\n이미지 업로드 ({total}장)\n{'='*60}")
    for slug, imgs in IMAGES.items():
        UPLOADED_IMAGES[slug] = []
        for i, (pid, alt) in enumerate(imgs):
            fn = f"cl-{slug}-{i+1}"; tmp = download_image(pid)
            if not tmp: UPLOADED_IMAGES[slug].append(("","",alt)); fail += 1; continue
            mid, murl = upload_image_to_wp(tmp, fn, alt); os.unlink(tmp)
            if murl: UPLOADED_IMAGES[slug].append((mid,murl,alt)); up += 1; print(f"  [{up+fail}/{total}] OK | {fn}")
            else: UPLOADED_IMAGES[slug].append(("","",alt)); fail += 1
            time.sleep(0.5)
    print(f"\n이미지: 성공 {up}, 실패 {fail}\n")

def get_img(slug, idx):
    imgs = UPLOADED_IMAGES.get(slug, [])
    if idx >= len(imgs): return ""
    _, url, alt = imgs[idx]
    if not url: return ""
    return f'<figure style="margin:32px 0;text-align:center;"><img src="{url}" alt="{alt}" style="width:100%;max-width:800px;height:auto;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.10);" loading="lazy" /><figcaption style="margin-top:8px;font-size:13px;color:#6b7280;">{alt}</figcaption></figure>'

def get_fid(slug):
    imgs = UPLOADED_IMAGES.get(slug, [])
    return imgs[0][0] if imgs and imgs[0][0] else None

def cta_html(c):
    b = f"border:{c['border']};" if c.get("border") else ""
    return f'<div style="background:{c["bg"]};{b}border-radius:12px;padding:28px 32px;margin:32px 0;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;"><div><p style="margin:0 0 6px;font-size:18px;font-weight:700;color:{c["text_color"]};">{c["text"]}</p><p style="margin:0;font-size:14px;color:{c["desc_color"]};">{c["desc"]}</p></div><a href="{c["url"]}" target="_blank" rel="noopener noreferrer" style="background:{c["btn_bg"]};color:{c["btn_color"]};padding:12px 24px;border-radius:8px;font-weight:700;text-decoration:none;white-space:nowrap;font-size:15px;">바로가기 &rarr;</a></div>'

def build(post):
    p, slug = [], post["slug"]
    p.append(f'<p style="font-size:17px;line-height:1.8;margin-bottom:24px;">{post["intro"]}</p>')
    i1 = get_img(slug, 0)
    if i1: p.append(i1)
    secs, ctas = post["sections"], post["ctas"]
    ns = len(secs); i2p = max(2, int(ns*0.6))
    for i, (t, body) in enumerate(secs):
        p.append(f'<h2 style="font-size:22px;font-weight:700;margin:40px 0 16px;border-left:4px solid #2563eb;padding-left:12px;">{t}</h2>')
        p.append(body)
        if i == 1 and ctas: p.append(cta_html(ctas[0]))
        elif i == ns//2 and len(ctas)>1: p.append(cta_html(ctas[1]))
        if i == i2p:
            i2 = get_img(slug, 1)
            if i2: p.append(i2)
    p.append('<h2 style="font-size:22px;font-weight:700;margin:40px 0 16px;border-left:4px solid #2563eb;padding-left:12px;">자주 묻는 질문 (FAQ)</h2>')
    for q, a in post["faq"]:
        p.append(f'<h3 style="font-size:17px;font-weight:600;color:#1e40af;margin:20px 0 8px;">Q. {q}</h3>')
        p.append(f'<p style="margin:0 0 16px;line-height:1.8;">A. {a}</p>')
    if len(ctas)>2: p.append(cta_html(ctas[2]))
    return "\n".join(p)

C1 = {"text": "클로드 AI 무료 시작하기", "desc": "Anthropic의 AI 어시스턴트 클로드를 무료로 체험하세요", "url": "https://claude.ai/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"}
C2 = {"text": "클로드 Pro 구독하기", "desc": "GPT-4 수준의 Opus 모델을 무제한 사용하세요", "url": "https://claude.ai/settings/billing", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"}
C3 = {"text": "클로드 API 문서 보기", "desc": "개발자를 위한 Anthropic API 공식 문서", "url": "https://docs.anthropic.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"}

POSTS = [
    # 1. 클로드 AI 사용법 완벽 가이드
    {"title": "클로드 AI 사용법 완벽 가이드 초보자 시작하기 총정리", "cat": CAT_IT, "slug": "claude-ai-beginner-guide",
     "intro": "<strong>클로드(Claude)</strong>는 Anthropic이 개발한 AI 어시스턴트로, ChatGPT의 강력한 대안으로 떠오르고 있습니다. 긴 문서 분석, 코딩, 글쓰기 등에서 뛰어난 성능을 보여주며, 특히 안전하고 정직한 답변을 지향하는 것이 특징입니다. 이 글에서는 클로드 AI에 처음 접하는 분을 위해 회원가입부터 실전 활용까지 모든 것을 안내합니다.",
     "sections": [
         ("클로드 AI란 무엇인가", "<p>클로드는 미국 AI 기업 <strong>Anthropic</strong>이 만든 대화형 AI 모델입니다. OpenAI 출신 연구자들이 설립한 회사로, '안전한 AI'를 최우선 가치로 삼고 있습니다.</p><ul><li><strong>개발사</strong>: Anthropic (2021년 설립, 구글·아마존 투자)</li><li><strong>최신 모델</strong>: Claude Opus 4, Sonnet 4, Haiku (2024~2025)</li><li><strong>핵심 강점</strong>: 긴 문서 처리(최대 20만 토큰), 정확한 지시 따르기, 안전한 답변</li><li><strong>사용 방법</strong>: 웹(claude.ai), 모바일 앱, API, Claude Code(CLI)</li></ul><p>ChatGPT가 '가장 유명한 AI'라면, 클로드는 <strong>'가장 신뢰할 수 있는 AI'</strong>를 지향합니다.</p>"),
         ("클로드 회원가입 및 시작하기", "<ol><li><strong>claude.ai</strong> 접속</li><li>'Sign up' 클릭 → 이메일 또는 구글 계정으로 가입</li><li>이메일 인증 완료</li><li>바로 대화 시작 가능 (무료)</li></ol><p><strong>모바일 앱</strong>도 제공됩니다.</p><ul><li>iOS: App Store에서 'Claude' 검색</li><li>Android: Google Play에서 'Claude' 검색</li></ul><p>가입 후 바로 무료로 사용할 수 있으며, 무료 버전에서도 Sonnet 모델을 사용할 수 있습니다.</p>"),
         ("클로드 기본 사용법", "<p>클로드는 <strong>대화형 인터페이스</strong>로 사용합니다. 아래 입력창에 질문이나 요청을 타이핑하면 됩니다.</p><ul><li><strong>질문하기</strong>: '한국의 수도는 어디야?' → 즉시 답변</li><li><strong>글쓰기 요청</strong>: '여행 블로그 글을 2000자로 써줘' → 글 생성</li><li><strong>번역</strong>: '이 영문 이메일을 한국어로 번역해줘' → 번역 결과</li><li><strong>코드 작성</strong>: 'Python으로 구구단 프로그램 만들어줘' → 코드 생성</li><li><strong>문서 분석</strong>: PDF, 이미지, 텍스트 파일을 업로드하여 분석·요약 요청</li></ul><p><strong>팁</strong>: 질문이 구체적일수록 답변 품질이 높아집니다. '마케팅 전략 알려줘'보다 '20대 여성 대상 인스타그램 마케팅 전략 5가지를 표로 정리해줘'가 훨씬 좋은 답변을 받을 수 있습니다.</p>"),
         ("클로드 핵심 기능 5가지", "<ol><li><strong>파일 업로드</strong>: PDF, 이미지, CSV, 코드 파일 등을 업로드하여 분석할 수 있습니다. 최대 20만 토큰(약 500페이지 분량)의 문서를 한 번에 처리합니다.</li><li><strong>Artifacts</strong>: 코드, 문서, 다이어그램 등을 별도 패널에서 미리보기할 수 있는 기능입니다. 코드 실행 결과를 바로 확인 가능합니다.</li><li><strong>Projects</strong>: 관련 대화를 프로젝트로 묶어 관리할 수 있습니다. 프로젝트별 지시사항을 설정하면 매번 반복 설명할 필요가 없습니다.</li><li><strong>이미지 인식</strong>: 사진, 스크린샷, 차트 이미지를 업로드하면 내용을 분석하고 설명합니다.</li><li><strong>다국어 지원</strong>: 한국어를 포함한 다양한 언어를 지원하며, 한국어 성능이 ChatGPT와 대등하거나 일부 영역에서 더 우수합니다.</li></ol>"),
         ("클로드 실전 활용 예시 10가지", "<table><thead><tr><th>#</th><th>활용 분야</th><th>프롬프트 예시</th></tr></thead><tbody><tr><td>1</td><td>이메일 작성</td><td>'거래처에 납기 연장을 요청하는 공손한 이메일을 써줘'</td></tr><tr><td>2</td><td>보고서 요약</td><td>'이 PDF를 읽고 핵심 내용을 3줄로 요약해줘'</td></tr><tr><td>3</td><td>엑셀 수식</td><td>'VLOOKUP으로 두 시트의 데이터를 매칭하는 수식을 알려줘'</td></tr><tr><td>4</td><td>코딩</td><td>'React로 투두리스트 앱을 만들어줘'</td></tr><tr><td>5</td><td>번역</td><td>'이 계약서를 영어로 번역하되, 법률 용어를 유지해줘'</td></tr><tr><td>6</td><td>브레인스토밍</td><td>'카페 창업 아이디어 10개를 장단점과 함께 정리해줘'</td></tr><tr><td>7</td><td>학습</td><td>'미적분의 기본 개념을 고등학생 수준으로 설명해줘'</td></tr><tr><td>8</td><td>마케팅</td><td>'인스타그램 광고 문구를 3가지 톤으로 작성해줘'</td></tr><tr><td>9</td><td>데이터 분석</td><td>'이 CSV 파일의 매출 추이를 분석하고 인사이트를 알려줘'</td></tr><tr><td>10</td><td>일정 관리</td><td>'이번 주 할 일 목록을 우선순위별로 정리해줘'</td></tr></tbody></table>"),
         ("클로드 사용 시 주의사항", "<ul><li><strong>할루시네이션</strong>: AI는 사실이 아닌 내용을 자신 있게 말할 수 있습니다. 중요한 정보는 반드시 팩트체크하세요.</li><li><strong>개인정보</strong>: 주민번호, 비밀번호 등 민감한 개인정보를 입력하지 마세요.</li><li><strong>저작권</strong>: AI가 생성한 콘텐츠의 저작권은 법적으로 아직 불명확합니다. 상업적 사용 시 주의하세요.</li><li><strong>최신 정보</strong>: 클로드의 학습 데이터에는 최신 뉴스가 반영되지 않을 수 있습니다.</li><li><strong>대화 기록</strong>: 대화 내용이 모델 개선에 사용될 수 있습니다. 설정에서 비활성화 가능합니다.</li></ul>"),
     ],
     "faq": [
         ("클로드는 무료로 사용할 수 있나요?", "<strong>네</strong>, claude.ai에서 무료로 사용 가능합니다. 무료 버전은 Sonnet 모델을 제공하며 일일 사용량에 제한이 있습니다. 무제한 사용과 최고 성능 모델(Opus)을 원하면 Pro 구독($20/월)이 필요합니다."),
         ("클로드와 ChatGPT 중 어떤 것을 써야 하나요?", "긴 문서 분석, 코딩, 정확한 지시 따르기는 <strong>클로드</strong>가 우수합니다. 플러그인 생태계, 이미지 생성(DALL-E), 실시간 검색은 <strong>ChatGPT</strong>가 강점입니다. 두 가지를 함께 사용하는 것을 추천합니다."),
         ("한국어로 질문해도 잘 답변하나요?", "<strong>네</strong>, 클로드는 한국어를 잘 이해하고 자연스러운 한국어로 답변합니다. 일부 전문 분야에서는 영어로 질문하면 더 정확한 답변을 받을 수 있습니다."),
         ("클로드에게 파일을 보내도 안전한가요?", "Anthropic은 업로드된 파일을 <strong>대화 처리 목적으로만 사용</strong>한다고 명시합니다. 그래도 극도로 민감한 기밀 문서는 업로드를 피하는 것이 안전합니다."),
     ],
     "ctas": [C1, C2, C3]},

    # 2. 클로드 vs ChatGPT 비교
    {"title": "클로드 vs ChatGPT 비교 어떤 AI가 더 좋을까 총정리", "cat": CAT_IT, "slug": "claude-vs-chatgpt",
     "intro": "AI 어시스턴트를 선택할 때 가장 많이 비교하는 것이 <strong>클로드(Claude)와 ChatGPT</strong>입니다. 두 서비스는 각각 다른 강점을 가지고 있어 용도에 따라 최적의 선택이 달라집니다. 성능, 가격, 기능, 한국어 지원 등 모든 측면에서 비교합니다.",
     "sections": [
         ("클로드 vs ChatGPT 핵심 비교표", "<table><thead><tr><th>항목</th><th>클로드 (Anthropic)</th><th>ChatGPT (OpenAI)</th></tr></thead><tbody><tr><td>최신 모델</td><td>Claude Opus 4, Sonnet 4</td><td>GPT-4o, o1</td></tr><tr><td>무료 모델</td><td>Sonnet</td><td>GPT-4o mini</td></tr><tr><td>유료 가격</td><td>$20/월 (Pro)</td><td>$20/월 (Plus)</td></tr><tr><td>컨텍스트 길이</td><td>20만 토큰 (약 500페이지)</td><td>12.8만 토큰</td></tr><tr><td>파일 업로드</td><td>PDF, 이미지, CSV 등</td><td>PDF, 이미지, CSV 등</td></tr><tr><td>이미지 생성</td><td>미지원</td><td>DALL-E 3 내장</td></tr><tr><td>웹 검색</td><td>미지원 (학습 데이터만)</td><td>실시간 웹 검색 가능</td></tr><tr><td>플러그인/GPTs</td><td>미지원</td><td>GPT Store, 플러그인</td></tr><tr><td>코딩 능력</td><td>매우 우수</td><td>매우 우수</td></tr><tr><td>한국어</td><td>우수</td><td>우수</td></tr><tr><td>안전성</td><td>최우선 (Constitutional AI)</td><td>높음</td></tr></tbody></table>"),
         ("클로드가 더 좋은 경우", "<ul><li><strong>긴 문서 분석</strong>: 20만 토큰 컨텍스트로 논문, 계약서, 보고서를 한 번에 분석할 수 있습니다. ChatGPT보다 1.5배 이상 긴 문서를 처리합니다.</li><li><strong>정확한 지시 따르기</strong>: '5줄로 요약해줘', '표 형식으로 정리해줘' 등 형식 지시를 클로드가 더 정확하게 따릅니다.</li><li><strong>코딩 작업</strong>: 코드 작성, 리팩토링, 디버깅에서 클로드 Opus가 GPT-4와 동등하거나 우수합니다.</li><li><strong>안전한 답변</strong>: 유해하거나 편향된 답변을 최소화하는 Constitutional AI 기술을 적용합니다.</li><li><strong>글쓰기</strong>: 자연스럽고 일관된 문체로 긴 글을 잘 작성합니다. 소설, 에세이 등 창작 글쓰기에 강합니다.</li></ul>"),
         ("ChatGPT가 더 좋은 경우", "<ul><li><strong>이미지 생성</strong>: DALL-E 3가 내장되어 텍스트로 이미지를 만들 수 있습니다. 클로드는 이미지 생성 기능이 없습니다.</li><li><strong>실시간 웹 검색</strong>: ChatGPT는 인터넷을 검색하여 최신 정보를 제공합니다. 클로드는 학습 데이터 범위 내에서만 답변합니다.</li><li><strong>플러그인/GPTs</strong>: GPT Store에서 수천 개의 커스텀 GPT를 사용할 수 있습니다. 업무 자동화에 유리합니다.</li><li><strong>음성 대화</strong>: ChatGPT는 음성으로 대화할 수 있는 Voice 모드를 제공합니다.</li><li><strong>생태계</strong>: ChatGPT의 사용자 수가 압도적으로 많아 커뮤니티, 튜토리얼, 프롬프트 공유가 활발합니다.</li></ul>"),
         ("실제 성능 비교 테스트", "<p>같은 질문을 클로드와 ChatGPT에 던져본 결과입니다.</p><table><thead><tr><th>테스트</th><th>클로드</th><th>ChatGPT</th><th>승자</th></tr></thead><tbody><tr><td>한국어 에세이 (1000자)</td><td>자연스럽고 구조적</td><td>자연스럽지만 반복적</td><td>클로드</td></tr><tr><td>Python 코드 작성</td><td>깔끔하고 주석 충실</td><td>깔끔하고 설명 충실</td><td>무승부</td></tr><tr><td>영한 번역 (계약서)</td><td>법률 용어 정확</td><td>법률 용어 정확</td><td>무승부</td></tr><tr><td>10페이지 PDF 요약</td><td>핵심 정확히 추출</td><td>핵심 정확히 추출</td><td>무승부</td></tr><tr><td>최신 뉴스 질문</td><td>답변 불가</td><td>웹 검색으로 답변</td><td>ChatGPT</td></tr><tr><td>이미지 생성</td><td>미지원</td><td>DALL-E로 생성</td><td>ChatGPT</td></tr></tbody></table>"),
         ("두 가지를 함께 쓰는 전략", "<p>클로드와 ChatGPT를 <strong>용도별로 나눠 쓰는 것</strong>이 가장 효율적입니다.</p><ul><li><strong>긴 문서 분석, 글쓰기, 코딩</strong> → 클로드</li><li><strong>이미지 생성, 최신 정보 검색, 음성 대화</strong> → ChatGPT</li><li><strong>중요한 작업</strong> → 양쪽에 모두 물어보고 더 좋은 답변 채택</li></ul><p>두 서비스 모두 무료 버전이 있으니, 먼저 무료로 사용해보고 자신에게 맞는 쪽을 Pro로 업그레이드하세요.</p>"),
     ],
     "faq": [
         ("클로드와 ChatGPT 중 어떤 것이 더 저렴한가요?", "유료 버전은 둘 다 <strong>$20/월</strong>로 동일합니다. 무료 버전도 둘 다 제공하므로 먼저 무료로 비교해보세요."),
         ("클로드가 ChatGPT를 완전히 대체할 수 있나요?", "<strong>아직은 어렵습니다.</strong> 이미지 생성과 실시간 웹 검색은 ChatGPT만 가능합니다. 하지만 텍스트 기반 작업(글쓰기, 코딩, 분석)에서는 클로드가 대등하거나 우수합니다."),
         ("Gemini(구글)도 비교해야 하지 않나요?", "Gemini도 좋은 AI이지만, 현재 한국어 성능과 코딩 능력은 <strong>클로드·ChatGPT가 더 우수</strong>합니다. 구글 생태계(Gmail, Drive)와 연동이 필요하면 Gemini가 유리합니다."),
         ("회사에서 AI를 도입하려면 어떤 것이 좋나요?", "보안이 중요하면 <strong>클로드(Anthropic API)</strong>, 다양한 기능이 필요하면 <strong>ChatGPT Enterprise</strong>를 추천합니다. 둘 다 기업용 API와 데이터 보호 정책을 제공합니다."),
     ],
     "ctas": [C1, C2, C3]},

    # 3. 클로드 무료 사용법 요금제 비교
    {"title": "클로드 무료 사용법 요금제 비교 Pro 가입 방법 총정리", "cat": CAT_IT, "slug": "claude-pricing-free-plan",
     "intro": "클로드 AI를 <strong>무료로 사용하는 방법</strong>과 유료 Pro 구독의 차이점이 궁금하신가요? 무료 버전의 제한사항, Pro·Team·Enterprise 요금제 비교, 가입 방법을 총정리합니다.",
     "sections": [
         ("클로드 요금제 비교표", "<table><thead><tr><th>항목</th><th>무료</th><th>Pro ($20/월)</th><th>Team ($25/인/월)</th><th>Enterprise</th></tr></thead><tbody><tr><td>모델</td><td>Sonnet</td><td>Opus, Sonnet, Haiku</td><td>전체</td><td>전체</td></tr><tr><td>사용량</td><td>제한적</td><td>5배 이상</td><td>높음</td><td>맞춤</td></tr><tr><td>파일 업로드</td><td>가능</td><td>가능</td><td>가능</td><td>가능</td></tr><tr><td>Projects</td><td>제한적</td><td>무제한</td><td>무제한</td><td>무제한</td></tr><tr><td>우선 접속</td><td>없음</td><td>있음</td><td>있음</td><td>있음</td></tr><tr><td>API 접근</td><td>별도</td><td>별도</td><td>별도</td><td>포함</td></tr><tr><td>데이터 보호</td><td>기본</td><td>기본</td><td>강화</td><td>최고</td></tr></tbody></table>"),
         ("무료 버전으로 할 수 있는 것", "<ul><li><strong>Sonnet 모델 사용</strong>: 일상적인 질문, 글쓰기, 번역, 간단한 코딩에 충분한 성능</li><li><strong>파일 업로드</strong>: PDF, 이미지, CSV 등을 업로드하여 분석 가능</li><li><strong>대화 기록</strong>: 이전 대화를 저장하고 이어서 진행 가능</li><li><strong>Artifacts</strong>: 코드 미리보기, 문서 생성 등 사용 가능</li></ul><p><strong>제한사항</strong>: 일일 메시지 수에 제한이 있으며, 피크 시간대에 응답이 느려질 수 있습니다. Opus 모델은 사용할 수 없습니다.</p>"),
         ("Pro 구독이 필요한 경우", "<ul><li><strong>Opus 모델 사용</strong>: 가장 뛰어난 성능. 복잡한 분석, 고급 코딩, 창작에 적합.</li><li><strong>사용량 5배</strong>: 무료 대비 5배 이상의 메시지를 보낼 수 있어 업무용으로 충분합니다.</li><li><strong>우선 접속</strong>: 사용자가 많은 피크 시간대에도 빠르게 응답받을 수 있습니다.</li><li><strong>Projects 무제한</strong>: 프로젝트별로 대화를 관리하고, 맞춤 지시사항을 설정할 수 있습니다.</li></ul><p><strong>추천</strong>: 하루 10회 이상 AI를 사용하거나, 복잡한 업무에 AI를 활용한다면 Pro가 가치 있습니다.</p>"),
         ("Pro 가입 방법", "<ol><li><strong>claude.ai</strong> 접속 → 로그인</li><li>왼쪽 하단 사용자 아이콘 → <strong>'Upgrade to Pro'</strong> 클릭</li><li>결제 정보 입력 (해외 결제 가능한 신용카드/체크카드)</li><li>$20/월 결제 → 즉시 Pro 기능 활성화</li></ol><p><strong>해지</strong>: 언제든 구독을 취소할 수 있으며, 취소 후에도 결제 기간 끝까지 Pro를 사용할 수 있습니다.</p>"),
         ("클로드 API 가격", "<p>개발자가 클로드를 앱에 통합할 때 사용하는 API 가격입니다.</p><table><thead><tr><th>모델</th><th>입력 (100만 토큰)</th><th>출력 (100만 토큰)</th><th>특징</th></tr></thead><tbody><tr><td>Haiku</td><td>$0.25</td><td>$1.25</td><td>가장 빠르고 저렴</td></tr><tr><td>Sonnet</td><td>$3</td><td>$15</td><td>성능·가격 균형</td></tr><tr><td>Opus</td><td>$15</td><td>$75</td><td>최고 성능</td></tr></tbody></table><p>API는 사용한 만큼만 과금되므로 소규모 프로젝트에 적합합니다.</p>"),
     ],
     "faq": [
         ("한국 카드로 Pro 결제가 가능한가요?", "<strong>네</strong>, 해외 결제가 가능한 신용카드(VISA, Mastercard)로 결제 가능합니다. 원화가 아닌 달러($20)로 청구됩니다."),
         ("무료 버전만으로 충분한가요?", "가벼운 질문, 간단한 글쓰기, 번역 등에는 <strong>무료로 충분</strong>합니다. 업무용으로 하루 10회 이상 사용하거나 Opus 모델이 필요하면 Pro를 추천합니다."),
         ("Pro를 구독하면 API도 무료인가요?", "<strong>아닙니다.</strong> Pro 구독과 API는 별개입니다. Pro는 claude.ai 웹/앱 사용, API는 개발자가 앱에 통합할 때 사용합니다."),
         ("학생 할인이 있나요?", "현재 학생 할인은 <strong>제공되지 않습니다</strong>. 무료 버전을 활용하거나, 학교에서 제공하는 AI 라이선스를 확인하세요."),
     ],
     "ctas": [C1, C2, C3]},

    # 4. 클로드 프롬프트 잘 쓰는 법
    {"title": "클로드 프롬프트 잘 쓰는 법 10가지 실전 활용 팁", "cat": CAT_IT, "slug": "claude-prompt-tips",
     "intro": "같은 AI라도 <strong>어떻게 질문하느냐</strong>에 따라 답변 품질이 천지차이입니다. 클로드에게 원하는 답변을 정확히 받을 수 있는 프롬프트 작성법 10가지를 실전 예제와 함께 안내합니다.",
     "sections": [
         ("프롬프트 기본 원칙", "<p>클로드에게 좋은 답변을 받으려면 <strong>구체적이고 명확한 지시</strong>가 핵심입니다.</p><table><thead><tr><th>나쁜 프롬프트</th><th>좋은 프롬프트</th><th>차이점</th></tr></thead><tbody><tr><td>마케팅 전략 알려줘</td><td>20대 여성 대상 인스타그램 마케팅 전략 5가지를 표로 정리해줘</td><td>대상, 채널, 형식 명시</td></tr><tr><td>이메일 써줘</td><td>거래처에 납기 1주일 연장을 요청하는 공손한 비즈니스 이메일을 300자로 써줘</td><td>목적, 톤, 길이 명시</td></tr><tr><td>코드 짜줘</td><td>Python으로 CSV 파일을 읽어 매출 상위 10개 항목을 막대 차트로 시각화하는 코드를 작성해줘</td><td>언어, 기능, 결과 명시</td></tr></tbody></table>"),
         ("프롬프트 팁 10가지", "<ol><li><strong>역할 부여하기</strong>: '너는 10년 경력 마케팅 전문가야. ~에 대해 조언해줘'</li><li><strong>출력 형식 지정</strong>: '표로 정리해줘', '번호 목록으로', 'JSON 형식으로'</li><li><strong>글자 수 제한</strong>: '500자로 요약해줘', '3줄로 핵심만'</li><li><strong>톤 지정</strong>: '친근하게', '격식체로', '유머를 섞어서'</li><li><strong>예시 제공</strong>: '아래 예시처럼 작성해줘: [예시]'</li><li><strong>단계별 사고</strong>: '단계별로 생각하며 풀어줘 (step by step)'</li><li><strong>제약 조건 명시</strong>: '전문 용어 없이 쉽게', '초등학생도 이해할 수 있게'</li><li><strong>맥락 제공</strong>: '나는 3년차 마케터이고, 상사에게 보고서를 제출해야 해'</li><li><strong>반복 수정</strong>: '좋은데, 2번 항목을 더 구체적으로 수정해줘'</li><li><strong>XML 태그 활용</strong>: '&lt;document&gt; 여기에 문서 &lt;/document&gt; 이 문서를 분석해줘'</li></ol>"),
         ("분야별 프롬프트 템플릿", "<p><strong>글쓰기</strong></p><pre>다음 조건으로 블로그 글을 작성해줘:\n- 주제: [주제]\n- 대상 독자: [대상]\n- 글자 수: [n]자\n- 톤: [톤]\n- 구성: 서론-본론(소제목 3개)-결론-FAQ 3개</pre><p><strong>코딩</strong></p><pre>다음 요구사항으로 코드를 작성해줘:\n- 언어: [Python/JavaScript 등]\n- 기능: [상세 설명]\n- 입력: [입력 형식]\n- 출력: [출력 형식]\n- 에러 처리를 포함해줘\n- 주석으로 설명을 달아줘</pre><p><strong>데이터 분석</strong></p><pre>첨부한 CSV 파일을 분석해줘:\n1. 주요 트렌드를 파악해줘\n2. 이상치가 있는지 확인해줘\n3. 핵심 인사이트 5가지를 bullet point로 정리해줘\n4. 경영진에게 보고할 요약문을 3줄로 작성해줘</pre>"),
         ("클로드만의 특수 기능 활용", "<ul><li><strong>System Prompt</strong>: Projects 기능에서 '지시사항'을 설정하면 모든 대화에 적용됩니다. 예: '항상 한국어로 답변하고, 존댓말을 사용해줘.'</li><li><strong>Artifacts 활용</strong>: '이 코드를 Artifact로 보여줘'라고 하면 별도 패널에서 코드를 미리보기할 수 있습니다.</li><li><strong>긴 문서 분석</strong>: 문서를 업로드한 후 '이 문서에서 ~를 찾아줘'처럼 구체적으로 질문하면 정확한 답변을 받을 수 있습니다.</li><li><strong>멀티턴 대화</strong>: 이전 대화 맥락을 기억하므로, '위에서 3번 항목을 더 자세히 설명해줘'처럼 이어서 대화할 수 있습니다.</li></ul>"),
         ("흔한 프롬프트 실수와 개선", "<table><thead><tr><th>실수</th><th>문제점</th><th>개선 방법</th></tr></thead><tbody><tr><td>'잘 모르겠어'라고 하지 마</td><td>AI가 거짓 정보를 만들 수 있음</td><td>'모르면 모른다고 말해줘'로 변경</td></tr><tr><td>한 번에 너무 많은 요청</td><td>답변 품질 저하</td><td>하나씩 단계적으로 요청</td></tr><tr><td>모호한 질문</td><td>모호한 답변</td><td>구체적 조건·형식·대상 명시</td></tr><tr><td>맥락 없는 질문</td><td>일반적인 답변</td><td>본인 상황·목적을 설명</td></tr></tbody></table>"),
     ],
     "faq": [
         ("프롬프트를 영어로 써야 더 좋은 답변을 받나요?", "일상적인 질문은 <strong>한국어로 충분</strong>합니다. 다만 전문 기술 분야(프로그래밍, 학술)에서는 영어로 질문하면 더 정확한 답변을 받을 수 있습니다."),
         ("프롬프트 길이가 길수록 좋은가요?", "무조건 길다고 좋은 것은 아닙니다. <strong>필요한 정보를 빠짐없이, 간결하게</strong> 전달하는 것이 핵심입니다. 불필요한 정보는 오히려 방해가 됩니다."),
         ("ChatGPT용 프롬프트를 클로드에서도 쓸 수 있나요?", "대부분 <strong>그대로 사용 가능</strong>합니다. 클로드는 XML 태그(&lt;tag&gt;)를 활용한 구조화된 프롬프트에 특히 잘 반응합니다."),
         ("좋은 프롬프트를 어디서 배울 수 있나요?", "Anthropic 공식 <strong>프롬프트 가이드</strong>(docs.anthropic.com/docs/prompt-engineering)가 가장 체계적입니다. 한국어 커뮤니티에서도 프롬프트 공유가 활발합니다."),
     ],
     "ctas": [C1, C2, C3]},

    # 5. 클로드로 블로그 글쓰기
    {"title": "클로드로 블로그 글쓰기 자동화하는 방법 실전 가이드", "cat": CAT_IT, "slug": "claude-blog-writing",
     "intro": "블로그 글을 쓸 때 <strong>클로드 AI</strong>를 활용하면 리서치, 초안 작성, 편집까지 시간을 크게 절약할 수 있습니다. AI에만 의존하지 않으면서 효율적으로 블로그를 운영하는 실전 전략을 안내합니다.",
     "sections": [
         ("클로드로 블로그 글쓰는 5단계 프로세스", "<ol><li><strong>키워드·주제 선정</strong>: '요즘 검색량이 높은 [분야] 블로그 주제 10개를 추천해줘' → 클로드가 트렌드 기반 주제 목록 생성</li><li><strong>아웃라인 작성</strong>: '이 주제로 블로그 글의 목차를 만들어줘. 서론, 본론(H2 소제목 5개), FAQ 3개 포함' → 글 구조 자동 생성</li><li><strong>초안 작성</strong>: '위 목차대로 3000자 분량의 블로그 글을 작성해줘. 대상 독자는 20~30대 직장인. 친근한 톤으로.' → 초안 생성</li><li><strong>수정·보완</strong>: 클로드가 쓴 초안에 본인의 경험, 데이터, 의견을 추가. 이 단계가 가장 중요합니다.</li><li><strong>SEO 최적화</strong>: '이 글의 메타 설명(150자), 키워드 태그 5개를 만들어줘' → SEO 요소 자동 생성</li></ol>"),
         ("블로그 글쓰기 프롬프트 템플릿", "<pre>다음 조건으로 블로그 글을 작성해줘:\n\n- 주제: [주제]\n- 타겟 키워드: [키워드]\n- 대상 독자: [대상]\n- 글자 수: 3000자 이상\n- 톤: 친근하면서 전문적\n- 구성:\n  1. 서론 (독자의 문제 제기)\n  2. 본론 (H2 소제목 4~5개, 각 소제목에 구체적 내용)\n  3. 비교표 1개 포함\n  4. FAQ 3개 (Q&A 형식)\n  5. 결론 (핵심 요약 + CTA)\n\n- 중요: 사실에 기반하여 작성하고,\n  확인되지 않은 정보는 포함하지 마.\n- HTML 형식이 아닌 마크다운으로 작성해줘.</pre>"),
         ("AI 블로그 글의 한계와 보완법", "<p>AI가 쓴 글을 그대로 게시하면 여러 문제가 발생합니다.</p><ul><li><strong>독창성 부족</strong>: AI 글은 평균적이고 개성이 없습니다. → <strong>본인의 경험·사례·의견</strong>을 반드시 추가하세요.</li><li><strong>정보 정확성</strong>: AI가 틀린 정보를 쓸 수 있습니다. → <strong>팩트체크</strong>를 반드시 거치세요.</li><li><strong>SEO 불이익</strong>: 구글은 저품질 AI 콘텐츠의 순위를 낮출 수 있습니다. → AI 초안에 <strong>가치를 추가</strong>해야 합니다.</li><li><strong>AI 탐지</strong>: AI가 쓴 글은 패턴이 있어 탐지될 수 있습니다. → 문체를 본인 스타일로 수정하세요.</li></ul><p><strong>핵심 원칙</strong>: 클로드는 '비서'이지 '작가'가 아닙니다. 초안 작성 도구로 활용하고, 최종 글에는 반드시 본인의 가치를 더하세요.</p>"),
         ("클로드 블로그 활용 고급 팁", "<ol><li><strong>시리즈 글 기획</strong>: '이 주제로 10편짜리 시리즈를 기획해줘. 각 편의 제목과 핵심 내용을 정리해줘' → 콘텐츠 캘린더 자동 생성</li><li><strong>경쟁 분석</strong>: 경쟁 블로그 글을 붙여넣고 '이 글의 장단점을 분석하고, 더 나은 글을 쓰려면 어떤 점을 보완해야 하는지 알려줘'</li><li><strong>제목 최적화</strong>: '이 주제로 클릭률 높은 블로그 제목 10개를 만들어줘. 숫자, 질문형, 비교형을 포함해줘'</li><li><strong>내부 링크 제안</strong>: 기존 글 목록을 주고 '이 글에서 내부 링크를 걸 수 있는 부분을 찾아줘'</li></ol>"),
         ("월 30편 블로그 운영 전략", "<table><thead><tr><th>단계</th><th>소요 시간</th><th>클로드 활용</th><th>본인 작업</th></tr></thead><tbody><tr><td>주제 선정</td><td>10분</td><td>키워드 아이디어 생성</td><td>최종 주제 선택</td></tr><tr><td>아웃라인</td><td>5분</td><td>목차 자동 생성</td><td>구조 수정</td></tr><tr><td>초안 작성</td><td>5분</td><td>3000자 초안 생성</td><td>-</td></tr><tr><td>수정·보완</td><td>30분</td><td>-</td><td>경험 추가, 팩트체크</td></tr><tr><td>SEO 최적화</td><td>5분</td><td>메타·태그 생성</td><td>최종 확인</td></tr><tr><td><strong>총</strong></td><td><strong>55분/편</strong></td><td></td><td></td></tr></tbody></table><p>기존 2~3시간 걸리던 블로그 글 작성이 <strong>1시간 이내</strong>로 단축됩니다.</p>"),
     ],
     "faq": [
         ("AI가 쓴 블로그 글을 구글이 감점하나요?", "구글은 'AI가 썼는지'가 아니라 <strong>'유용한 콘텐츠인지'</strong>를 기준으로 평가합니다. AI 초안에 본인의 경험과 가치를 추가하면 문제 없습니다."),
         ("클로드로 하루에 몇 편까지 쓸 수 있나요?", "무료 버전은 일일 사용량 제한이 있어 <strong>3~5편</strong> 정도 가능합니다. Pro 구독하면 <strong>10편 이상</strong> 작성 가능합니다."),
         ("어떤 블로그 플랫폼이 AI 글쓰기에 적합한가요?", "<strong>워드프레스</strong>가 가장 유연합니다. 클로드가 생성한 HTML을 바로 붙여넣을 수 있고, SEO 플러그인(Yoast, Rank Math)과 연동이 좋습니다."),
         ("AI 글쓰기를 독자에게 공개해야 하나요?", "법적 의무는 없지만, <strong>투명하게 공개</strong>하는 것이 신뢰에 도움됩니다. 'AI의 도움을 받아 작성했습니다' 정도의 표기를 권합니다."),
     ],
     "ctas": [C1, C2, C3]},

    # 6. 클로드 API 사용법
    {"title": "클로드 API 사용법 개발자 입문 가이드 총정리", "cat": CAT_IT, "slug": "claude-api-guide",
     "intro": "클로드를 내 앱이나 서비스에 통합하려면 <strong>Anthropic API</strong>를 사용해야 합니다. API 키 발급부터 Python으로 첫 요청을 보내는 것까지 개발자 입문 가이드를 안내합니다.",
     "sections": [
         ("클로드 API 시작하기", "<ol><li><strong>console.anthropic.com</strong> 접속 → 회원가입</li><li>결제 정보 등록 (사용한 만큼 과금)</li><li><strong>API Keys</strong> 메뉴에서 API 키 생성</li><li>Python SDK 설치: <code>pip install anthropic</code></li><li>첫 요청 보내기</li></ol>"),
         ("Python 첫 요청 코드", "<pre>import anthropic\n\nclient = anthropic.Anthropic(\n    api_key=\"your-api-key-here\"\n)\n\nmessage = client.messages.create(\n    model=\"claude-sonnet-4-20250514\",\n    max_tokens=1024,\n    messages=[\n        {\"role\": \"user\", \"content\": \"안녕하세요! 자기소개를 해주세요.\"}\n    ]\n)\n\nprint(message.content[0].text)</pre><p>이 코드를 실행하면 클로드가 자기소개 답변을 생성합니다.</p>"),
         ("API 모델 선택 가이드", "<table><thead><tr><th>모델</th><th>속도</th><th>성능</th><th>가격 (입력/출력, 100만 토큰)</th><th>추천 용도</th></tr></thead><tbody><tr><td>Haiku</td><td>가장 빠름</td><td>보통</td><td>$0.25 / $1.25</td><td>챗봇, 분류, 간단 작업</td></tr><tr><td>Sonnet</td><td>빠름</td><td>우수</td><td>$3 / $15</td><td>일반 업무, 글쓰기, 코딩</td></tr><tr><td>Opus</td><td>보통</td><td>최고</td><td>$15 / $75</td><td>복잡한 분석, 고급 코딩</td></tr></tbody></table><p><strong>대부분의 프로젝트는 Sonnet으로 충분</strong>합니다. 비용 효율을 위해 간단한 작업은 Haiku, 복잡한 작업만 Opus를 사용하세요.</p>"),
         ("System Prompt 활용", "<pre>message = client.messages.create(\n    model=\"claude-sonnet-4-20250514\",\n    max_tokens=1024,\n    system=\"너는 한국어 전문 번역가야. 모든 번역은 자연스러운 한국어로 해줘.\",\n    messages=[\n        {\"role\": \"user\", \"content\": \"Translate: The quick brown fox jumps over the lazy dog.\"}\n    ]\n)</pre><p>System Prompt로 AI의 역할, 톤, 제약 조건을 설정할 수 있습니다.</p>"),
         ("API 비용 관리 팁", "<ul><li><strong>토큰 카운팅</strong>: API 응답에 사용된 토큰 수가 포함됩니다. 모니터링하여 예산을 관리하세요.</li><li><strong>max_tokens 설정</strong>: 필요한 만큼만 출력하도록 제한하면 비용을 줄일 수 있습니다.</li><li><strong>캐싱</strong>: 같은 질문에 대한 답변을 캐싱하면 API 호출 횟수를 줄일 수 있습니다.</li><li><strong>모델 분기</strong>: 간단한 작업은 Haiku, 복잡한 작업만 Sonnet/Opus로 라우팅하면 비용이 크게 줄어듭니다.</li><li><strong>사용량 알림</strong>: Anthropic 콘솔에서 일일/월간 사용량 알림을 설정하세요.</li></ul>"),
     ],
     "faq": [
         ("API 무료 크레딧이 있나요?", "신규 가입 시 <strong>$5 무료 크레딧</strong>을 제공하는 경우가 있습니다. Anthropic 콘솔에서 확인하세요."),
         ("API로 이미지를 분석할 수 있나요?", "<strong>네</strong>, 클로드 API는 이미지를 base64로 인코딩하여 전송하면 이미지 내용을 분석할 수 있습니다 (Vision 기능)."),
         ("API 응답 속도는 어떤가요?", "Haiku는 <strong>1~2초</strong>, Sonnet은 <strong>2~5초</strong>, Opus는 <strong>5~15초</strong> 정도입니다. 스트리밍 모드를 사용하면 첫 토큰이 더 빨리 나옵니다."),
         ("한국에서 API 사용에 제한이 있나요?", "<strong>없습니다.</strong> 한국에서 정상적으로 API를 사용할 수 있으며, 결제도 해외 결제 가능한 카드로 가능합니다."),
     ],
     "ctas": [C1, C2, C3]},

    # 7. 클로드 코드 사용법
    {"title": "클로드 코드 사용법 터미널에서 AI 코딩하는 방법 가이드", "cat": CAT_IT, "slug": "claude-code-guide",
     "intro": "<strong>클로드 코드(Claude Code)</strong>는 터미널에서 직접 AI와 대화하며 코딩할 수 있는 Anthropic의 공식 CLI 도구입니다. 파일 읽기·쓰기, git 관리, 테스트 실행까지 개발 워크플로우 전체를 AI가 지원합니다.",
     "sections": [
         ("클로드 코드란", "<p>Claude Code는 <strong>터미널(명령줄)에서 실행되는 AI 코딩 어시스턴트</strong>입니다.</p><ul><li>코드베이스 전체를 이해하고 수정 제안</li><li>파일을 직접 읽고, 편집하고, 생성</li><li>git commit, push 등 버전 관리</li><li>테스트 실행 및 디버깅</li><li>터미널 명령어 실행</li></ul><p>VS Code 확장, JetBrains 플러그인, 웹 앱(claude.ai/code)으로도 사용 가능합니다.</p>"),
         ("설치 및 시작", "<ol><li><strong>Node.js 18+</strong> 설치 확인</li><li>터미널에서 설치: <code>npm install -g @anthropic-ai/claude-code</code></li><li>프로젝트 폴더로 이동: <code>cd my-project</code></li><li>실행: <code>claude</code></li><li>Anthropic 계정으로 인증 (처음 1회)</li><li>바로 대화 시작!</li></ol>"),
         ("실전 사용 예시", "<ul><li><strong>코드 설명</strong>: 'src/app.js 파일을 설명해줘' → 코드 분석 및 설명</li><li><strong>버그 수정</strong>: '이 에러를 고쳐줘: [에러 메시지]' → 원인 분석 + 코드 수정</li><li><strong>기능 추가</strong>: '로그인 기능을 추가해줘' → 파일 생성·수정</li><li><strong>리팩토링</strong>: '이 함수를 더 효율적으로 개선해줘' → 코드 개선</li><li><strong>테스트 작성</strong>: '이 함수의 유닛 테스트를 작성해줘' → 테스트 코드 생성</li><li><strong>커밋</strong>: '/commit' → 변경 사항을 분석하고 커밋 메시지를 자동 생성</li></ul>"),
         ("클로드 코드 vs GitHub Copilot 비교", "<table><thead><tr><th>항목</th><th>클로드 코드</th><th>GitHub Copilot</th></tr></thead><tbody><tr><td>방식</td><td>대화형 (채팅)</td><td>자동 완성 + 채팅</td></tr><tr><td>코드베이스 이해</td><td>전체 프로젝트 이해</td><td>현재 파일 중심</td></tr><tr><td>파일 수정</td><td>직접 수정 가능</td><td>제안만 (수동 적용)</td></tr><tr><td>터미널 명령</td><td>실행 가능</td><td>불가</td></tr><tr><td>가격</td><td>API 사용량 기반</td><td>$10/월</td></tr><tr><td>오프라인</td><td>불가</td><td>불가</td></tr></tbody></table>"),
         ("효과적인 사용 팁", "<ol><li><strong>CLAUDE.md 파일 작성</strong>: 프로젝트 루트에 CLAUDE.md를 만들어 코딩 컨벤션, 아키텍처 정보를 적으면 AI가 프로젝트를 더 잘 이해합니다.</li><li><strong>작은 단위로 요청</strong>: '전체 앱을 만들어줘'보다 '로그인 폼 컴포넌트를 만들어줘'처럼 작은 단위로 요청하세요.</li><li><strong>변경 사항 리뷰</strong>: AI가 수정한 코드를 반드시 리뷰하세요. git diff로 변경 내용을 확인합니다.</li><li><strong>/help 활용</strong>: 터미널에서 /help를 입력하면 사용 가능한 명령어 목록을 볼 수 있습니다.</li></ol>"),
     ],
     "faq": [
         ("클로드 코드는 무료인가요?", "클로드 코드 도구 자체는 무료이지만, <strong>API 사용량에 따라 과금</strong>됩니다. Anthropic API 키가 필요합니다. Max 플랜($100/월~)을 사용하면 별도 API 비용 없이 사용할 수 있습니다."),
         ("어떤 프로그래밍 언어를 지원하나요?", "<strong>모든 언어</strong>를 지원합니다. Python, JavaScript, TypeScript, Java, Go, Rust, C++ 등 언어에 관계없이 코드를 이해하고 작성합니다."),
         ("기존 프로젝트에서 바로 사용할 수 있나요?", "<strong>네</strong>, 프로젝트 폴더에서 claude를 실행하면 기존 코드베이스를 자동으로 분석합니다."),
         ("보안상 코드가 외부로 전송되나요?", "대화 내용과 코드는 <strong>Anthropic 서버로 전송</strong>됩니다. 보안이 민감한 프로젝트는 데이터 보호 정책을 확인하세요."),
     ],
     "ctas": [C1, C2, C3]},

    # 8. 클로드로 PDF 요약
    {"title": "클로드로 PDF 요약하는 방법 긴 문서 분석 활용법 총정리", "cat": CAT_IT, "slug": "claude-pdf-summary",
     "intro": "수십~수백 페이지의 PDF를 읽는 데 몇 시간이 걸리지만, <strong>클로드에 업로드하면 몇 초 만에 핵심을 파악</strong>할 수 있습니다. PDF 요약, 질문 답변, 데이터 추출 등 클로드의 문서 분석 기능을 총정리합니다.",
     "sections": [
         ("클로드에 PDF 업로드하는 방법", "<ol><li>claude.ai 접속 → 로그인</li><li>대화 입력창 왼쪽의 <strong>📎 (클립) 아이콘</strong> 클릭</li><li>PDF 파일 선택 → 업로드 (최대 10개 파일 동시 업로드)</li><li>업로드 완료 후 질문 입력</li><li>클로드가 문서를 분석하여 답변</li></ol><p><strong>지원 파일</strong>: PDF, TXT, CSV, DOCX, 이미지(JPG, PNG) 등</p><p><strong>용량 제한</strong>: 파일당 약 30MB, 총 대화 컨텍스트 20만 토큰(약 500페이지)</p>"),
         ("PDF 분석 프롬프트 예시", "<table><thead><tr><th>목적</th><th>프롬프트</th></tr></thead><tbody><tr><td>전체 요약</td><td>'이 PDF를 3줄로 요약해줘'</td></tr><tr><td>핵심 포인트</td><td>'이 문서의 핵심 포인트 5가지를 bullet point로 정리해줘'</td></tr><tr><td>특정 정보 찾기</td><td>'이 계약서에서 위약금 조항을 찾아 설명해줘'</td></tr><tr><td>비교 분석</td><td>'이 두 PDF의 주장을 비교하여 표로 정리해줘'</td></tr><tr><td>번역</td><td>'이 영문 PDF의 핵심 내용을 한국어로 요약해줘'</td></tr><tr><td>데이터 추출</td><td>'이 PDF에서 모든 날짜와 금액을 표로 정리해줘'</td></tr><tr><td>질문 답변</td><td>'이 논문에 따르면 [특정 주제]에 대한 결론은 무엇인가?'</td></tr></tbody></table>"),
         ("PDF 분석 활용 사례", "<ul><li><strong>논문 리뷰</strong>: 30페이지 논문을 업로드하고 '이 논문의 연구 방법론, 결과, 한계를 정리해줘'</li><li><strong>계약서 검토</strong>: 계약서를 업로드하고 '불리한 조항이 있는지 확인해줘'</li><li><strong>회의 자료 준비</strong>: 보고서를 업로드하고 '이 보고서의 핵심을 5분 발표용으로 정리해줘'</li><li><strong>이력서 분석</strong>: 지원자 이력서를 업로드하고 '이 지원자의 강점과 약점을 분석해줘'</li><li><strong>재무제표 분석</strong>: 재무제표 PDF를 업로드하고 '매출 추이와 수익성을 분석해줘'</li></ul>"),
         ("여러 PDF 동시 비교 분석", "<p>클로드는 <strong>여러 파일을 동시에 업로드</strong>하여 비교 분석할 수 있습니다.</p><ol><li>2~3개의 PDF를 동시에 업로드</li><li>'이 세 문서의 핵심 주장을 비교하여 표로 정리해줘'</li><li>클로드가 각 문서의 핵심을 추출하여 비교표를 생성</li></ol><p>학술 연구, 경쟁사 분석, 법률 문서 비교 등에 매우 유용합니다.</p>"),
         ("PDF 분석 시 주의사항", "<ul><li><strong>스캔 PDF 제한</strong>: 이미지로 스캔된 PDF는 텍스트 추출이 안 될 수 있습니다. OCR 처리된 PDF를 사용하세요.</li><li><strong>보안 문서</strong>: 기밀 문서는 업로드를 신중하게 결정하세요. Anthropic의 데이터 처리 정책을 확인하세요.</li><li><strong>정확성 확인</strong>: 클로드의 요약이 원문과 일치하는지 중요한 부분은 교차 확인하세요.</li><li><strong>페이지 제한</strong>: 20만 토큰(약 500페이지)을 초과하는 문서는 나눠서 업로드해야 합니다.</li></ul>"),
     ],
     "faq": [
         ("스캔된 PDF도 분석할 수 있나요?", "텍스트가 인식 가능한 PDF는 분석 가능합니다. 이미지만 있는 스캔 PDF는 <strong>OCR 처리 후</strong> 업로드하세요. Adobe Acrobat이나 무료 OCR 도구로 변환 가능합니다."),
         ("PDF 업로드 시 데이터가 저장되나요?", "Anthropic은 업로드된 파일을 <strong>대화 처리 목적으로만 사용</strong>한다고 명시합니다. 대화가 끝나면 파일은 서버에서 삭제됩니다."),
         ("무료 버전에서도 PDF 업로드가 가능한가요?", "<strong>네</strong>, 무료 버전에서도 PDF 업로드와 분석이 가능합니다. 다만 일일 사용량 제한이 있습니다."),
         ("엑셀(CSV) 파일도 분석할 수 있나요?", "<strong>네</strong>, CSV 파일을 업로드하면 데이터를 분석하고 인사이트를 제공합니다. '이 데이터의 추이를 분석해줘', '이상치를 찾아줘' 등의 요청이 가능합니다."),
     ],
     "ctas": [C1, C2, C3]},

    # 9. 클로드 업무 활용법
    {"title": "클로드 업무 활용법 이메일 보고서 회의록 자동 작성 가이드", "cat": CAT_IT, "slug": "claude-work-productivity",
     "intro": "직장에서 <strong>클로드 AI</strong>를 활용하면 이메일, 보고서, 회의록 등 반복적인 문서 작업을 크게 줄일 수 있습니다. 업무별 프롬프트와 실전 활용법을 안내합니다.",
     "sections": [
         ("업무별 클로드 활용 가이드", "<table><thead><tr><th>업무</th><th>절약 시간</th><th>프롬프트 예시</th></tr></thead><tbody><tr><td>이메일 작성</td><td>10분 → 2분</td><td>'거래처에 미팅 일정 확인 이메일을 공손하게 써줘'</td></tr><tr><td>보고서 초안</td><td>2시간 → 20분</td><td>'Q3 마케팅 성과 보고서 초안을 작성해줘. 데이터: [데이터]'</td></tr><tr><td>회의록 정리</td><td>30분 → 5분</td><td>'이 회의 녹취록을 정리해줘. 결정사항과 Action Item을 분리해줘'</td></tr><tr><td>기획서 작성</td><td>3시간 → 30분</td><td>'[프로젝트] 기획서를 작성해줘. 목적, 범위, 일정, 예산 포함'</td></tr><tr><td>번역</td><td>1시간 → 5분</td><td>'이 영문 이메일을 비즈니스 한국어로 번역해줘'</td></tr><tr><td>데이터 분석</td><td>1시간 → 10분</td><td>'이 매출 데이터를 분석하고 인사이트 5가지를 알려줘'</td></tr></tbody></table>"),
         ("이메일 작성 프롬프트 모음", "<ul><li><strong>미팅 요청</strong>: '다음 주 화요일 오후 2시에 프로젝트 진행 상황 미팅을 요청하는 이메일을 팀장님께 보내는 형식으로 써줘.'</li><li><strong>사과 이메일</strong>: '납기가 3일 지연된 것에 대해 거래처에 사과하고 새로운 납기를 안내하는 이메일을 공손하게 써줘.'</li><li><strong>협조 요청</strong>: '마케팅팀에 다음 달 캠페인을 위한 디자인 소재를 요청하는 이메일을 써줘. 마감은 금요일.'</li><li><strong>거절</strong>: '제안을 정중하게 거절하되, 향후 협력 가능성을 열어두는 이메일을 써줘.'</li></ul>"),
         ("보고서·기획서 작성 팁", "<ol><li><strong>데이터 제공</strong>: 보고서에 필요한 숫자, 데이터를 함께 입력하면 정확한 보고서가 나옵니다.</li><li><strong>형식 지정</strong>: '표 2개, 차트 설명 1개를 포함해줘'처럼 원하는 형식을 명시하세요.</li><li><strong>대상 명시</strong>: '경영진 대상 보고서'와 '팀원 대상 보고서'는 톤과 깊이가 달라야 합니다.</li><li><strong>이전 보고서 참고</strong>: 이전 보고서를 업로드하고 '이 형식에 맞춰 새 보고서를 써줘'라고 하면 일관성을 유지할 수 있습니다.</li></ol>"),
         ("회의록 정리 프롬프트", "<pre>다음 회의 녹취록을 정리해줘:\n\n[녹취록 붙여넣기]\n\n정리 형식:\n1. 회의 기본 정보 (일시, 참석자)\n2. 주요 논의 사항 (bullet point)\n3. 결정 사항 (확정된 것만)\n4. Action Item 테이블:\n   | 항목 | 담당자 | 기한 | 상태 |\n5. 다음 회의 안건</pre>"),
         ("업무 자동화 워크플로우", "<p>클로드를 일상 업무에 녹여내는 워크플로우입니다.</p><ol><li><strong>아침</strong>: '오늘 할 일 목록을 우선순위별로 정리해줘' → 일일 계획 수립</li><li><strong>오전</strong>: 이메일 작성, 보고서 초안 작성에 클로드 활용</li><li><strong>오후</strong>: 회의 후 녹취록 정리, Action Item 추출</li><li><strong>퇴근 전</strong>: '오늘 한 일을 요약하고 내일 할 일을 정리해줘' → 일일 보고</li></ol><p>이 워크플로우로 <strong>하루 1~2시간</strong>을 절약할 수 있습니다.</p>"),
     ],
     "faq": [
         ("회사에서 클로드를 사용해도 되나요?", "회사의 <strong>AI 사용 정책</strong>을 먼저 확인하세요. 기밀 정보는 입력하지 않는 것이 원칙입니다. 기업용으로는 Team 또는 Enterprise 플랜을 사용하면 데이터 보호가 강화됩니다."),
         ("클로드가 쓴 보고서를 그대로 제출해도 되나요?", "초안으로 활용하되, <strong>반드시 본인이 검토·수정</strong>한 후 제출하세요. 숫자 오류, 맥락 불일치 등이 있을 수 있습니다."),
         ("영어 이메일도 잘 써주나요?", "<strong>매우 잘 씁니다.</strong> '비즈니스 영어로', '캐주얼한 톤으로' 등을 지정하면 상황에 맞는 영문 이메일을 작성합니다."),
         ("팀 전체가 클로드를 쓰려면?", "Anthropic <strong>Team 플랜</strong>($25/인/월)을 사용하면 팀원 관리, 공유 Projects, 강화된 데이터 보호 기능을 사용할 수 있습니다."),
     ],
     "ctas": [C1, C2, C3]},

    # 10. 클로드 한국어 성능 테스트
    {"title": "클로드 AI 한국어 성능 테스트 실제 사용 후기 총정리", "cat": CAT_IT, "slug": "claude-korean-review",
     "intro": "AI를 한국어로 사용할 때 가장 궁금한 것은 <strong>'한국어를 얼마나 잘 이해하고 답변하는가'</strong>입니다. 클로드의 한국어 성능을 다양한 테스트로 검증하고 실제 사용 후기를 공유합니다.",
     "sections": [
         ("한국어 성능 테스트 결과 요약", "<table><thead><tr><th>테스트 항목</th><th>점수 (10점)</th><th>평가</th></tr></thead><tbody><tr><td>일상 대화</td><td>9/10</td><td>자연스러운 존댓말, 문맥 이해 우수</td></tr><tr><td>비즈니스 이메일</td><td>9/10</td><td>격식체, 경어 정확</td></tr><tr><td>기술 문서 번역</td><td>8/10</td><td>전문 용어 대부분 정확</td></tr><tr><td>창작 글쓰기</td><td>8/10</td><td>자연스러운 문체, 가끔 어색한 표현</td></tr><tr><td>한국 문화 이해</td><td>7/10</td><td>기본 문화는 이해, 최신 트렌드 부족</td></tr><tr><td>한국어 맞춤법</td><td>9/10</td><td>맞춤법 정확, 띄어쓰기 양호</td></tr><tr><td>속어·신조어</td><td>6/10</td><td>일부 이해하지만 최신 유행어 부족</td></tr></tbody></table>"),
         ("테스트 1: 비즈니스 이메일 작성", "<p><strong>프롬프트</strong>: '신규 거래처에 첫 미팅을 제안하는 비즈니스 이메일을 작성해줘. 격식체로, 300자 내외로.'</p><p><strong>결과</strong>: 매우 자연스러운 비즈니스 한국어로 작성. '귀사', '협력', '일정 조율' 등 적절한 비즈니스 용어 사용. 존댓말 일관성 유지. <strong>9/10점</strong></p>"),
         ("테스트 2: 한국 문화 관련 질문", "<p><strong>프롬프트</strong>: '한국의 설날 문화와 세배 예절에 대해 설명해줘'</p><p><strong>결과</strong>: 세배 순서, 세뱃돈 문화, 떡국 의미 등을 정확하게 설명. 다만 최신 트렌드(모바일 세뱃돈 등)는 부족. <strong>7/10점</strong></p>"),
         ("테스트 3: 기술 문서 한영 번역", "<p><strong>프롬프트</strong>: '다음 한국어 기술 문서를 영어로 번역해줘. 전문 용어는 영문 그대로 유지해줘.'</p><p><strong>결과</strong>: 전문 용어(API, SDK, 클라우드 등)를 정확히 유지하면서 자연스러운 영어로 번역. 일부 한국식 표현이 직역되는 경우 있음. <strong>8/10점</strong></p>"),
         ("ChatGPT와 한국어 비교", "<table><thead><tr><th>항목</th><th>클로드</th><th>ChatGPT</th></tr></thead><tbody><tr><td>존댓말 일관성</td><td>우수</td><td>우수</td></tr><tr><td>비즈니스 문서</td><td>우수</td><td>우수</td></tr><tr><td>창작 글쓰기</td><td>약간 우세</td><td>양호</td></tr><tr><td>한국 문화 이해</td><td>양호</td><td>양호</td></tr><tr><td>최신 유행어</td><td>부족</td><td>약간 나음</td></tr><tr><td>맞춤법</td><td>우수</td><td>우수</td></tr></tbody></table><p><strong>결론</strong>: 한국어 성능은 두 서비스가 거의 대등합니다. 클로드가 긴 글의 일관성에서 약간 우세하고, ChatGPT가 최신 정보 반영에서 약간 우세합니다.</p>"),
         ("한국어 사용 팁", "<ol><li><strong>존댓말 지정</strong>: '항상 존댓말로 답변해줘'를 첫 메시지에 넣으면 일관된 존댓말을 유지합니다.</li><li><strong>전문 용어</strong>: 전문 분야 질문 시 '한국어로 답변하되 전문 용어는 영어로 표기해줘'라고 지정하면 혼란이 줄어듭니다.</li><li><strong>맥락 제공</strong>: '나는 한국 IT 회사의 3년차 개발자야'처럼 한국 맥락을 설명하면 더 적절한 답변을 받습니다.</li><li><strong>영어 혼용</strong>: 기술 질문은 영어로 하면 더 정확한 답변을 받을 수 있습니다. 결과를 한국어로 번역 요청하세요.</li></ol>"),
     ],
     "faq": [
         ("클로드가 한국어를 못 알아듣는 경우가 있나요?", "일상적인 한국어는 거의 완벽하게 이해합니다. 다만 <strong>극도로 구어적인 표현, 최신 신조어, 방언</strong>은 이해하지 못할 수 있습니다."),
         ("한국어와 영어 중 어떤 언어로 질문하는 것이 좋나요?", "일상적인 질문은 <strong>한국어</strong>로 충분합니다. 프로그래밍, 학술, 기술 분야는 <strong>영어</strong>로 질문하면 더 정확합니다."),
         ("클로드가 한국 법률이나 세금 정보를 잘 알고 있나요?", "기본적인 한국 법률·세금 정보는 알고 있지만, <strong>최신 법령 개정</strong>은 반영되지 않을 수 있습니다. 법률·세금 관련 정보는 반드시 공식 출처에서 확인하세요."),
         ("클로드로 한국어 맞춤법 검사를 할 수 있나요?", "<strong>가능합니다.</strong> '이 글의 맞춤법과 띄어쓰기를 교정해줘'라고 요청하면 교정해줍니다. 다만 전문 맞춤법 검사기(네이버, 부산대)보다는 정확도가 약간 낮을 수 있습니다."),
     ],
     "ctas": [C1, C2, C3]},
]


def publish(post_data):
    data = json.dumps(post_data).encode()
    req = urllib.request.Request(API, data=data, headers={"Authorization": f"Basic {AUTH}", "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            r = json.loads(resp.read().decode()); return r.get("id"), r.get("link", "")
    except urllib.error.HTTPError as e: print(f"  HTTP {e.code}: {e.read().decode()[:200]}"); return None, None
    except Exception as e: print(f"  Error: {e}"); return None, None

def main():
    upload_all_images()
    total = len(POSTS)
    print(f"{'='*60}\n총 {total}개 발행 시작\n{'='*60}")
    for i, post in enumerate(POSTS, 1):
        content = build(post)
        payload = {"title": post["title"], "content": content, "status": "publish", "slug": post["slug"], "categories": [post["cat"]]}
        fid = get_fid(post["slug"])
        if fid: payload["featured_media"] = fid
        pid, link = publish(payload)
        if pid: print(f"[{i}/{total}] OK | ID:{pid} | {post['title']}"); print(f"  -> {link}" if link else "")
        else: print(f"[{i}/{total}] FAIL | {post['title']}")
        time.sleep(1)
    print("\n발행 완료!")

    # 인덱싱
    print(f"\n{'='*60}\nIndexNow 색인 요청\n{'='*60}")
    urls = []
    for pid_start in range(1, total+1): pass  # URL은 발행 후 수집
    # WP API로 최근 10개 포스트 URL 가져오기
    try:
        req = urllib.request.Request(f"{API}?per_page=10&orderby=date&order=desc&_fields=link", headers={"Authorization": f"Basic {AUTH}"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            posts = json.loads(resp.read().decode())
            urls = [p["link"] for p in posts if p.get("link")]
    except Exception as e:
        print(f"  URL 수집 실패: {e}")

    if urls:
        payload = {"host": "devupbox.com", "key": "8dbbd7d6729b4a65b7dce4b9083c65e3", "keyLocation": "https://devupbox.com/8dbbd7d6729b4a65b7dce4b9083c65e3.txt", "urlList": urls}
        data = json.dumps(payload).encode()
        for n, ep in [("Naver","https://searchadvisor.naver.com/indexnow"),("Bing","https://www.bing.com/indexnow"),("Yandex","https://yandex.com/indexnow")]:
            req = urllib.request.Request(ep, data=data, method="POST"); req.add_header("Content-Type","application/json; charset=utf-8")
            try:
                with urllib.request.urlopen(req, timeout=30) as r: print(f"  {n}: HTTP {r.status}")
            except urllib.error.HTTPError as e: print(f"  {n}: HTTP {e.code}")
            except Exception as e: print(f"  {n}: {e}")

        # Google Indexing
        print(f"\n{'='*60}\nGoogle Indexing API\n{'='*60}")
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build as gbuild
            creds = service_account.Credentials.from_service_account_file("devupbox.json", scopes=["https://www.googleapis.com/auth/indexing"])
            svc = gbuild("indexing","v3",credentials=creds)
            ok=0
            for idx,u in enumerate(urls,1):
                try: svc.urlNotifications().publish(body={"url":u,"type":"URL_UPDATED"}).execute(); print(f"  [{idx}/{len(urls)}] OK | {u}"); ok+=1
                except Exception as e: print(f"  [{idx}/{len(urls)}] FAIL | {str(e)[:60]}")
                time.sleep(3)
            print(f"\n  Google: {ok}/{len(urls)}")
        except Exception as e:
            print(f"  Google Indexing 실패: {e}")

    print("\n모든 작업 완료!")

if __name__ == "__main__":
    main()

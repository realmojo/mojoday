import json,urllib.request,urllib.error,base64,time,ssl,os,tempfile
ssl._create_default_https_context=ssl._create_unverified_context
AUTH=base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API="https://devupbox.com/wp-json/wp/v2/posts"
MEDIA_API="https://devupbox.com/wp-json/wp/v2/media"

def download_image(pid):
    url=f"https://images.unsplash.com/{pid}?w=800&h=450&fit=crop&auto=format&q=80"
    tmp=tempfile.NamedTemporaryFile(suffix=".jpg",delete=False)
    req=urllib.request.Request(url);req.add_header("User-Agent","Mozilla/5.0")
    try:
        with urllib.request.urlopen(req,timeout=30) as r:tmp.write(r.read());tmp.close();return tmp.name
    except Exception as e:tmp.close();os.unlink(tmp.name);print(f"  DL실패:{e}");return None

def upload_image(fp,fn,alt):
    with open(fp,"rb") as f:d=f.read()
    req=urllib.request.Request(MEDIA_API,data=d,method="POST")
    req.add_header("Authorization",f"Basic {AUTH}");req.add_header("Content-Type","image/jpeg")
    req.add_header("Content-Disposition",f'attachment; filename="{fn}.jpg"')
    try:
        with urllib.request.urlopen(req,timeout=60) as r:
            j=json.loads(r.read().decode());mid=j.get("id");mu=j.get("source_url","")
            if mid:
                ud=json.dumps({"alt_text":alt}).encode()
                ur=urllib.request.Request(f"{MEDIA_API}/{mid}",data=ud,method="POST")
                ur.add_header("Authorization",f"Basic {AUTH}");ur.add_header("Content-Type","application/json")
                try:urllib.request.urlopen(ur,timeout=15)
                except:pass
            return mid,mu
    except Exception as e:print(f"  UP실패:{e}");return None,None

def ib(url,alt):
    return f'<!-- wp:image {{"sizeSlug":"large"}} -->\n<figure class="wp-block-image size-large"><img src="{url}" alt="{alt}"/><figcaption class="wp-element-caption">{alt}</figcaption></figure>\n<!-- /wp:image -->'

def cb(t,d,u,s="blue"):
    st={"blue":{"bg":"linear-gradient(135deg,#1e3a5f,#2d5a8e)","bb":"#fff","bc":"#1e3a5f","tc":"#fff","dc":"#cde0f5","bd":"none"},"yellow":{"bg":"#fffbeb","bb":"#f59e0b","bc":"#fff","tc":"#92400e","dc":"#78716c","bd":"2px solid #f59e0b"},"green":{"bg":"linear-gradient(135deg,#0f766e,#14b8a6)","bb":"#fff","bc":"#0f766e","tc":"#fff","dc":"#ccfbf1","bd":"none"}}[s]
    return f'<div style="background:{st["bg"]};border:{st["bd"]};border-radius:12px;padding:28px 32px;margin:32px 0;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;"><div><p style="margin:0 0 6px;font-size:18px;font-weight:700;color:{st["tc"]};">{t}</p><p style="margin:0;font-size:14px;color:{st["dc"]};">{d}</p></div><a href="{u}" target="_blank" rel="noopener noreferrer" style="background:{st["bb"]};color:{st["bc"]};padding:12px 24px;border-radius:8px;font-weight:700;text-decoration:none;font-size:15px;">바로가기 →</a></div>'

def pc(intro,secs,faqs,ctas,imgs):
    h=f'<p style="font-size:17px;line-height:1.8;">{intro}</p>\n'
    if len(imgs)>0 and imgs[0]:h+=imgs[0]+"\n"
    ci=0
    for i,(t,b) in enumerate(secs):
        h+=f'<h2>{t}</h2>\n{b}\n'
        if i==1 and ci<len(ctas):h+=ctas[ci]+"\n";ci+=1
        if i==len(secs)//2 and len(imgs)>1 and imgs[1]:h+=imgs[1]+"\n"
    if ci<len(ctas):h+=ctas[ci]+"\n";ci+=1
    h+='<h2>자주 묻는 질문 (FAQ)</h2>\n'
    for q,a in faqs:h+=f'<h3>Q. {q}</h3>\n<p>A. {a}</p>\n'
    if ci<len(ctas):h+=ctas[ci]+"\n"
    h+='<h2>마무리</h2>\n<p>이 글이 도움이 되셨다면 주변에도 공유해주세요.</p>'
    return h

TOPICS=[
("무료 화면 공유 도구 추천 팀뷰어 대체 TOP 5 2026","free-screen-sharing-tools-2026",
[("photo-1516321318423-f06f85e504b3","화면공유"),("photo-1504639725590-34d0984388bd","원격접속")],
"팀뷰어 무료 버전이 제한되면서 <strong>대체 원격 접속 도구</strong>를 찾는 분이 많습니다. 완전 무료부터 저렴한 유료까지, RustDesk, Chrome Remote Desktop, AnyDesk 등을 비교합니다.",
[("무료 원격 도구 비교","<table><thead><tr><th>도구</th><th>가격</th><th>지연</th><th>파일전송</th><th>특징</th></tr></thead><tbody><tr><td>Chrome Remote Desktop</td><td>무료</td><td>보통</td><td>X</td><td>크롬만 있으면 OK</td></tr><tr><td>RustDesk</td><td>무료(오픈소스)</td><td>낮음</td><td>O</td><td>자체 서버 구축 가능</td></tr><tr><td>AnyDesk</td><td>무료(개인)</td><td>매우낮음</td><td>O</td><td>가볍고 빠름</td></tr><tr><td>Parsec</td><td>무료(개인)</td><td>최저</td><td>X</td><td>게이밍 원격 최강</td></tr><tr><td>Windows RDP</td><td>무료(Pro 이상)</td><td>낮음</td><td>O</td><td>윈도우 기본 내장</td></tr></tbody></table>"),
("용도별 추천","<ul><li><strong>간단한 원격지원</strong>: Chrome Remote Desktop</li><li><strong>보안 중시</strong>: RustDesk (자체 서버)</li><li><strong>빠른 속도</strong>: AnyDesk 또는 Parsec</li><li><strong>윈도우 PC간</strong>: Windows RDP</li></ul>")],
[("팀뷰어 무료가 왜 제한되나요?","상업적 사용이 감지되면 <strong>5분 세션 제한</strong>이 걸립니다. 개인 사용도 오탐되는 경우가 많아 대안을 찾는 분이 늘었습니다."),
("원격 접속이 보안상 위험하지 않나요?","<strong>2단계 인증, 비밀번호 설정</strong>을 하면 안전합니다. RustDesk는 자체 서버를 사용해 데이터가 외부를 거치지 않습니다.")]),

("아이폰 보안 설정 방법 개인정보 보호 필수 설정 10가지 2026","iphone-security-settings-guide-2026",
[("photo-1563013544-824ae1b704d3","아이폰 보안"),("photo-1555949963-ff9fe0c870eb","개인정보 보호")],
"아이폰은 기본적으로 보안이 강하지만, <strong>설정을 최적화하면 더 안전</strong>합니다. Face ID, 앱 추적 투명성, iCloud 보안 등 필수 보안 설정 10가지를 안내합니다.",
[("아이폰 필수 보안 설정 10가지","<ol><li><strong>Face ID/Touch ID + 6자리 이상 암호</strong> 설정</li><li><strong>앱 추적 투명성</strong>: 설정 > 개인정보 보호 > 추적 > 모든 앱 차단</li><li><strong>2단계 인증</strong>: Apple ID > 보안 > 2단계 인증 활성화</li><li><strong>잠금 화면 알림 미리보기 비활성화</strong>: 설정 > 알림 > 미리보기 > 잠금해제 시</li><li><strong>Safari 사기 사이트 경고</strong>: 설정 > Safari > 사기 사이트 경고 ON</li><li><strong>위치 서비스 제한</strong>: 앱별 '사용 중에만' 또는 '안 함'으로 설정</li><li><strong>iCloud 키체인 활성화</strong>: 비밀번호 자동 저장 + 보안 경고</li><li><strong>나의 iPhone 찾기</strong>: 설정 > [이름] > 나의 찾기 > ON</li><li><strong>자동 잠금 30초~1분</strong>: 설정 > 디스플레이 > 자동 잠금</li><li><strong>USB 액세서리 차단</strong>: 설정 > Face ID > 액세서리 > 1시간 후 잠금</li></ol>"),
("설정 확인 방법","<p>설정 > 개인정보 보호 및 보안 > <strong>안전 점검</strong>에서 현재 보안 상태를 한눈에 확인할 수 있습니다.</p>")],
[("아이폰은 백신 앱이 필요한가요?","iOS는 샌드박스 구조로 <strong>백신이 불필요</strong>합니다. 오히려 가짜 백신 앱에 주의하세요."),
("VPN을 쓰면 더 안전한가요?","공공 와이파이 사용 시 <strong>VPN은 필수</strong>입니다. iCloud Private Relay(iCloud+ 가입자)도 대안입니다.")]),

("갤럭시 보안 설정 방법 안드로이드 필수 보안 체크리스트 2026","galaxy-security-settings-guide-2026",
[("photo-1512941937669-90a1b58e7e9c","갤럭시 보안"),("photo-1555949963-ff9fe0c870eb","안드로이드 보안")],
"안드로이드는 자유도가 높은 만큼 <strong>보안 설정이 더 중요</strong>합니다. 갤럭시 사용자를 위한 필수 보안 체크리스트를 단계별로 안내합니다.",
[("갤럭시 필수 보안 설정","<ol><li><strong>생체인증(지문/얼굴) + PIN 6자리 이상</strong></li><li><strong>Google Play 프로텍트</strong>: Play 스토어 > 프로필 > Play 프로텍트 ON</li><li><strong>출처를 알 수 없는 앱 설치 차단</strong>: 설정 > 보안 > 출처 미상 앱 OFF</li><li><strong>보안 폴더 활용</strong>: Knox 기반 격리 공간에 중요 앱/파일 보관</li><li><strong>앱 권한 관리</strong>: 설정 > 개인정보 > 권한 관리자에서 불필요 권한 제거</li><li><strong>2단계 인증</strong>: Google 계정 > 보안 > 2단계 인증 활성화</li><li><strong>기기 찾기</strong>: 설정 > 생체인식 > 원격 잠금 활성화</li><li><strong>자동 업데이트</strong>: 보안 패치를 항상 최신으로 유지</li></ol>"),
("Knox 보안 폴더란?","<p>Samsung Knox는 <strong>하드웨어 레벨 보안</strong>을 제공합니다. 보안 폴더 안의 앱과 데이터는 일반 영역과 완전히 분리되어 있어, 금융앱이나 사적인 사진을 안전하게 보관할 수 있습니다.</p>")],
[("갤럭시에 백신 앱이 필요한가요?","갤럭시에는 <strong>McAfee 기반 보안이 내장</strong>되어 있습니다. 추가 백신은 불필요하며, 오히려 배터리를 소모할 수 있습니다."),
("루팅하면 보안이 위험한가요?","<strong>루팅은 보안을 크게 약화</strong>시킵니다. Knox 보안이 무효화되고 금융앱 사용이 제한됩니다. 일반 사용자는 루팅을 하지 않는 것을 권장합니다.")]),

("피싱 사이트 구별법 가짜 사이트 확인 방법 총정리 2026","phishing-site-detection-guide-2026",
[("photo-1555949963-ff9fe0c870eb","피싱사이트 경고"),("photo-1563013544-824ae1b704d3","보안 점검")],
"택배 문자, 은행 이메일로 위장한 <strong>피싱 사이트</strong>가 매년 증가하고 있습니다. 가짜 사이트를 구별하는 5가지 방법과 피해 시 대처법을 총정리합니다.",
[("피싱 사이트 구별법 5가지","<ol><li><strong>URL 확인</strong>: 공식 도메인인지 확인 (예: kbstar.com vs kb-star.com)</li><li><strong>HTTPS 확인</strong>: 주소창 자물쇠 아이콘 + https:// 확인</li><li><strong>도메인 WHOIS 조회</strong>: whois.kr에서 등록일이 최근이면 의심</li><li><strong>디자인 오류</strong>: 로고 흐림, 오탈자, 어색한 한국어 표현</li><li><strong>개인정보 요구</strong>: 주민번호, 카드번호, OTP 전체를 요구하면 100% 피싱</li></ol>"),
("피해 시 대처법","<ol><li>즉시 <strong>비밀번호 변경</strong> (입력한 사이트와 동일 비밀번호 사용 사이트 전부)</li><li><strong>카드사/은행 연락</strong>하여 카드 정지 또는 계좌 지급정지</li><li><strong>경찰청 사이버안전국</strong>(182) 또는 KISA(118) 신고</li><li><strong>악성 앱 설치 여부</strong> 확인 후 삭제</li></ol>")],
[("피싱 문자와 정상 문자를 어떻게 구별하나요?","정상 문자는 <strong>절대로 링크 클릭을 유도하지 않습니다</strong>. 은행, 택배사는 앱 내 알림을 사용합니다. 링크가 있으면 의심하세요."),
("피싱 사이트에 비밀번호를 입력했는데 어떻게 하나요?","<strong>즉시 해당 비밀번호를 사용하는 모든 사이트의 비밀번호를 변경</strong>하세요. 같은 비밀번호를 여러 곳에 쓴 경우 모두 변경해야 합니다.")]),

("카카오톡 보안 설정 방법 비밀채팅 잠금 2단계인증 총정리 2026","kakaotalk-security-settings-2026",
[("photo-1563013544-824ae1b704d3","카카오톡 보안"),("photo-1512941937669-90a1b58e7e9c","메신저 보안")],
"카카오톡은 국민 메신저인 만큼 <strong>보안 설정이 매우 중요</strong>합니다. 비밀채팅, 앱 잠금, 2단계 인증 등 카카오톡 필수 보안 설정을 총정리합니다.",
[("카카오톡 보안 설정 7가지","<ol><li><strong>앱 잠금</strong>: 더보기 > 설정 > 개인/보안 > 잠금모드 (지문/PIN)</li><li><strong>2단계 인증</strong>: 설정 > 개인/보안 > 카카오계정 > 2단계 인증</li><li><strong>비밀채팅</strong>: 채팅방 > + > 비밀채팅 (종단간 암호화)</li><li><strong>로그인 관리</strong>: 설정 > 개인/보안 > 로그인 관리 > 사용하지 않는 기기 로그아웃</li><li><strong>프로필 공개 범위</strong>: 설정 > 프로필 > 공개 범위 설정</li><li><strong>친구 자동 추가 OFF</strong>: 설정 > 친구 > 연락처 친구 자동 추가 끄기</li><li><strong>카카오 인증서 관리</strong>: 더보기 > 인증서 > 사용 내역 확인</li></ol>"),
("비밀채팅 vs 일반채팅","<table><thead><tr><th>구분</th><th>일반채팅</th><th>비밀채팅</th></tr></thead><tbody><tr><td>암호화</td><td>서버 암호화</td><td>종단간 암호화(E2E)</td></tr><tr><td>카카오 서버</td><td>메시지 저장됨</td><td>저장 안 됨</td></tr><tr><td>타이머</td><td>없음</td><td>읽은 후 자동 삭제 가능</td></tr><tr><td>캡처 알림</td><td>없음</td><td>캡처 시 상대방 알림</td></tr></tbody></table>")],
[("카카오톡 비밀채팅은 정말 안전한가요?","비밀채팅은 <strong>종단간 암호화(E2E)</strong>로 카카오 서버에서도 내용을 볼 수 없습니다. 가장 안전한 채팅 방식입니다."),
("카카오톡 계정이 해킹되면 어떻게 하나요?","카카오 고객센터(1577-3754)에 <strong>계정 잠금 요청</strong> 후, 비밀번호 변경 및 2단계 인증을 설정하세요.")]),

("맥북 입문 가이드 2026 윈도우 사용자를 위한 macOS 적응법","macbook-beginner-guide-2026",
[("photo-1496181133206-80ce9b88a853","맥북 입문"),("photo-1486312338219-ce68d2c6f44d","macOS 작업")],
"윈도우에서 맥북으로 전환하면 <strong>처음 2주가 가장 힘듭니다</strong>. 트랙패드 제스처, Finder 사용법, 단축키 대응표, 필수 앱 등 윈도우 사용자를 위한 macOS 적응 가이드입니다.",
[("윈도우 vs macOS 단축키 대응표","<table><thead><tr><th>기능</th><th>Windows</th><th>macOS</th></tr></thead><tbody><tr><td>복사</td><td>Ctrl+C</td><td>Cmd+C</td></tr><tr><td>붙여넣기</td><td>Ctrl+V</td><td>Cmd+V</td></tr><tr><td>실행취소</td><td>Ctrl+Z</td><td>Cmd+Z</td></tr><tr><td>앱 전환</td><td>Alt+Tab</td><td>Cmd+Tab</td></tr><tr><td>앱 종료</td><td>Alt+F4</td><td>Cmd+Q</td></tr><tr><td>전체화면</td><td>F11</td><td>Ctrl+Cmd+F</td></tr><tr><td>스크린샷</td><td>Win+Shift+S</td><td>Cmd+Shift+4</td></tr><tr><td>파일탐색기</td><td>Win+E</td><td>Cmd+N (Finder)</td></tr><tr><td>작업관리자</td><td>Ctrl+Shift+Esc</td><td>Cmd+Opt+Esc</td></tr><tr><td>검색</td><td>Win+S</td><td>Cmd+Space (Spotlight)</td></tr></tbody></table>"),
("맥북 필수 앱 10선","<ol><li><strong>Alfred</strong> - Spotlight 대체 런처 (무료)</li><li><strong>Rectangle</strong> - 창 정렬 (무료, 윈도우 Snap 대체)</li><li><strong>IINA</strong> - 동영상 플레이어 (무료)</li><li><strong>Keka</strong> - 압축/해제 (무료)</li><li><strong>AppCleaner</strong> - 앱 완전 삭제 (무료)</li><li><strong>Hidden Bar</strong> - 메뉴바 정리 (무료)</li><li><strong>Stats</strong> - CPU/메모리 모니터 (무료)</li><li><strong>Amphetamine</strong> - 잠자기 방지 (무료)</li><li><strong>Bartender</strong> - 메뉴바 관리 (유료)</li><li><strong>Raycast</strong> - 생산성 런처 (무료)</li></ol>")],
[("맥북에서 한글 프로그램을 사용할 수 있나요?","한컴오피스 Mac 버전이 있습니다. 또는 <strong>Pages(무료)</strong>로 hwp를 열 수 있고, 구글 Docs도 대안입니다."),
("맥북으로 게임을 할 수 있나요?","M시리즈 칩 성능이 좋아졌지만, 윈도우 대비 <strong>게임 라이브러리가 제한적</strong>입니다. 스팀 일부 게임은 가능하며, Apple Arcade도 활용할 수 있습니다.")]),

("아이패드 200% 활용법 공부 업무 그림 생산성 팁 2026","ipad-productivity-tips-2026",
[("photo-1434030216411-0b793f4b4173","아이패드 공부"),("photo-1484154218962-a197022b5858","아이패드 업무")],
"아이패드를 유튜브 머신으로만 쓰고 계신가요? <strong>공부, 업무, 그림, 영상편집</strong>까지 아이패드를 200% 활용하는 방법을 용도별로 총정리합니다.",
[("용도별 활용법","<h3>공부용</h3><ul><li><strong>GoodNotes/Notability</strong>: Apple Pencil로 필기, PDF 교재에 직접 메모</li><li><strong>Anki</strong>: 플래시카드 앱으로 반복 학습</li><li><strong>Forest</strong>: 집중 타이머 (폰 사용 방지)</li></ul><h3>업무용</h3><ul><li><strong>스테이지 매니저</strong>: 멀티태스킹으로 앱 4개 동시 사용</li><li><strong>Sidecar</strong>: 맥북의 보조 모니터로 사용</li><li><strong>Microsoft 365</strong>: Word, Excel, PowerPoint 풀기능 사용</li></ul><h3>그림/디자인</h3><ul><li><strong>Procreate</strong>: 전문 일러스트 앱 (14,000원 일회성)</li><li><strong>Adobe Fresco</strong>: 수채화/유화 느낌 브러시</li></ul>"),
("아이패드 필수 액세서리","<table><thead><tr><th>액세서리</th><th>가격</th><th>필수도</th><th>용도</th></tr></thead><tbody><tr><td>Apple Pencil</td><td>13~19만원</td><td>필수</td><td>필기, 그림</td></tr><tr><td>Magic Keyboard</td><td>40~50만원</td><td>업무용 필수</td><td>타이핑, 트랙패드</td></tr><tr><td>종이질감 필름</td><td>1~3만원</td><td>필기용 추천</td><td>펜슬 마찰감 향상</td></tr><tr><td>케이스</td><td>2~5만원</td><td>필수</td><td>보호, 거치</td></tr></tbody></table>")],
[("아이패드로 노트북을 대체할 수 있나요?","문서 작업, 웹서핑, 미디어 소비 위주라면 <strong>80% 이상 대체 가능</strong>합니다. 코딩, 복잡한 엑셀, 전문 소프트웨어가 필요하면 노트북이 필수입니다."),
("아이패드 어떤 모델을 사야 하나요?","필기/공부 → <strong>iPad Air</strong>, 전문 창작 → <strong>iPad Pro</strong>, 가성비 → <strong>iPad 10세대</strong>를 추천합니다.")]),

("갤럭시 숨은 기능 20가지 몰랐던 편의 기능 총정리 2026","galaxy-hidden-features-2026",
[("photo-1512941937669-90a1b58e7e9c","갤럭시 기능"),("photo-1563013544-824ae1b704d3","스마트폰 팁")],
"갤럭시에는 <strong>알려지지 않은 숨은 기능</strong>이 정말 많습니다. 엣지 패널, 루틴, Good Lock, 삼성 덱스 등 생산성을 높여줄 기능 20가지를 소개합니다.",
[("갤럭시 숨은 기능 TOP 20","<ol><li><strong>엣지 패널</strong>: 화면 옆에서 스와이프하면 앱 바로가기, 클립보드, 연락처 등 빠른 접근</li><li><strong>루틴</strong>: 조건 설정으로 자동화 (예: 회사 도착 → 와이파이 ON + 무음)</li><li><strong>분할 화면</strong>: 최근 앱 버튼 → 앱 아이콘 길게 → 분할 화면으로 열기</li><li><strong>팝업 창</strong>: 앱을 작은 창으로 띄워 동시 사용</li><li><strong>삼성 덱스</strong>: TV/모니터에 연결하면 PC처럼 사용</li><li><strong>Good Lock</strong>: 삼성 공식 커스터마이징 앱 (잠금화면, 테마 등)</li><li><strong>보안 폴더</strong>: 앱, 사진, 파일을 암호화된 별도 공간에 보관</li><li><strong>디지털 웰빙</strong>: 앱별 사용 시간 제한 설정</li><li><strong>빠른 공유</strong>: 근처 갤럭시 기기와 AirDrop처럼 파일 전송</li><li><strong>화면 녹화</strong>: 빠른 설정 패널에서 바로 화면 녹화</li><li><strong>제스처 네비게이션</strong>: 버튼 대신 스와이프로 내비게이션</li><li><strong>측면 버튼 이중 클릭</strong>: 카메라 바로 실행 설정</li><li><strong>Smart Select</strong>: 화면 일부를 캡처하거나 GIF 만들기</li><li><strong>삼성 키보드 번역</strong>: 키보드에서 바로 번역</li><li><strong>알림 기록</strong>: 설정 > 알림 > 알림 기록에서 지운 알림 확인</li><li><strong>잠금 화면 위젯</strong>: 시계 스타일, 연락처, 음악 위젯 추가</li><li><strong>전원 버튼 길게 = 빅스비/전원</strong>: 설정에서 전원 메뉴로 변경 가능</li><li><strong>듀얼 메신저</strong>: 카카오톡 등을 2개 계정으로 사용</li><li><strong>사운드 어시스턴트</strong>: 앱별 음량 개별 조절</li><li><strong>캘린더 스티커</strong>: 삼성 캘린더에 귀여운 스티커로 일정 표시</li></ol>"),
("Good Lock 추천 모듈","<ul><li><strong>LockStar</strong>: 잠금화면 커스터마이징</li><li><strong>NavStar</strong>: 내비게이션바 커스터마이징</li><li><strong>One Hand Operation+</strong>: 한 손 조작 제스처</li><li><strong>SoundAssistant</strong>: 앱별 음량 조절</li></ul>")],
[("Good Lock은 어디서 다운받나요?","<strong>Galaxy Store</strong>에서 'Good Lock'을 검색하면 됩니다. 무료입니다."),
("삼성 덱스는 어떤 모니터에서 되나요?","<strong>USB-C 또는 HDMI 연결이 가능한 모든 모니터</strong>에서 사용 가능합니다. 무선 덱스는 Miracast 지원 TV에서 됩니다.")]),

("유튜브 채널 시작 가이드 2026 장비 편집 수익화 총정리","youtube-channel-start-guide-2026",
[("photo-1611162617213-7d7a39e9b1d7","유튜브 스트리밍"),("photo-1499750310107-5fef28a66643","콘텐츠 제작")],
"2026년에도 유튜브는 <strong>개인 브랜딩과 수익화</strong>의 최고 플랫폼입니다. 채널 개설부터 장비, 편집, 수익화 조건까지 유튜브 시작에 필요한 모든 것을 총정리합니다.",
[("유튜브 수익화 조건 (2026년)","<table><thead><tr><th>조건</th><th>기준</th></tr></thead><tbody><tr><td>구독자</td><td>1,000명 이상</td></tr><tr><td>시청시간</td><td>최근 12개월 4,000시간 또는 Shorts 1,000만 조회</td></tr><tr><td>커뮤니티 가이드</td><td>위반 없음</td></tr><tr><td>2단계 인증</td><td>필수 설정</td></tr><tr><td>AdSense 계정</td><td>연동 필요</td></tr></tbody></table>"),
("유튜브 장비 추천 (예산별)","<table><thead><tr><th>예산</th><th>카메라</th><th>마이크</th><th>조명</th><th>편집</th></tr></thead><tbody><tr><td>0원(스마트폰)</td><td>갤럭시/아이폰</td><td>내장 마이크</td><td>자연광</td><td>CapCut(무료)</td></tr><tr><td>30만원</td><td>스마트폰+짐벌</td><td>RODE Wireless Go(12만)</td><td>LED 패널(5만)</td><td>DaVinci Resolve(무료)</td></tr><tr><td>100만원</td><td>소니 ZV-E10(70만)</td><td>RODE VideoMic(10만)</td><td>링라이트(5만)</td><td>프리미어 프로(월2.4만)</td></tr></tbody></table>")],
[("유튜브 시작하는데 비싼 장비가 필요한가요?","<strong>스마트폰만으로 충분</strong>합니다. 최근 인기 유튜버 중 아이폰/갤럭시로만 촬영하는 분도 많습니다. 콘텐츠 기획이 장비보다 중요합니다."),
("유튜브 수익은 얼마나 되나요?","한국 기준 <strong>조회수 1,000회당 약 1,000~3,000원</strong>입니다. 니치(전문 분야)일수록 CPM이 높습니다. 월 100만 조회 = 약 100~300만원 수준입니다.")]),

("블로그 수익화 방법 2026 애드센스 쿠팡파트너스 제휴마케팅","blog-monetization-guide-2026",
[("photo-1499750310107-5fef28a66643","블로그 수익화"),("photo-1486312338219-ce68d2c6f44d","블로그 작성")],
"블로그로 <strong>월 100만원 이상</strong> 버는 분들이 늘고 있습니다. 구글 애드센스, 쿠팡파트너스, 텐핑, 제휴마케팅 등 블로그 수익화 방법을 수익 구조와 함께 총정리합니다.",
[("블로그 수익화 방법 비교","<table><thead><tr><th>방법</th><th>예상 수익</th><th>난이도</th><th>플랫폼</th><th>특징</th></tr></thead><tbody><tr><td>구글 애드센스</td><td>월 10~100만원</td><td>중</td><td>워드프레스/티스토리</td><td>자동 광고 배치</td></tr><tr><td>쿠팡파트너스</td><td>월 5~50만원</td><td>하</td><td>모든 블로그</td><td>구매 시 3% 수수료</td></tr><tr><td>네이버 애드포스트</td><td>월 1~30만원</td><td>하</td><td>네이버 블로그</td><td>네이버 전용</td></tr><tr><td>텐핑/리더스CPA</td><td>건당 1,000~50,000원</td><td>중</td><td>모든 블로그</td><td>신청/가입 유도</td></tr><tr><td>전자책/강의 판매</td><td>월 50~500만원</td><td>상</td><td>자체/클래스101</td><td>고수익 가능</td></tr></tbody></table>"),
("블로그 수익화 단계별 로드맵","<ol><li><strong>1~3개월</strong>: 양질의 글 30~50개 작성, SEO 기초 학습</li><li><strong>3~6개월</strong>: 구글 애드센스 승인, 쿠팡파트너스 시작</li><li><strong>6~12개월</strong>: 일 방문자 1,000명 달성, 월 30~50만원 수익</li><li><strong>1년+</strong>: 제휴마케팅 확대, 전자책/강의 판매로 수익 다각화</li></ol>")],
[("블로그로 현실적으로 얼마나 벌 수 있나요?","꾸준히 1년 이상 운영하면 <strong>월 30~100만원</strong>은 현실적인 목표입니다. 상위 블로거는 월 500만원 이상 수익을 올립니다."),
("네이버 블로그와 워드프레스 중 수익화에 유리한 것은?","수익화는 <strong>워드프레스가 압도적</strong>입니다. 구글 애드센스를 자유롭게 배치할 수 있고, SEO 제어가 가능합니다. 네이버는 애드포스트 수익이 낮습니다.")]),

("윈도우 11 vs macOS 비교 2026 어떤 OS가 나에게 맞을까","windows-vs-macos-comparison-2026",
[("photo-1516321318423-f06f85e504b3","윈도우 vs 맥"),("photo-1496181133206-80ce9b88a853","OS 비교")],
"노트북이나 데스크톱을 살 때 <strong>윈도우 vs macOS</strong> 고민은 필수입니다. 호환성, 생산성, 게이밍, 가격, 보안 등 모든 측면에서 두 OS를 비교합니다.",
[("윈도우 vs macOS 비교표","<table><thead><tr><th>항목</th><th>Windows 11</th><th>macOS Sequoia</th></tr></thead><tbody><tr><td>소프트웨어 호환</td><td>최고 (대부분 지원)</td><td>제한적 (일부 미지원)</td></tr><tr><td>게이밍</td><td>최고</td><td>제한적</td></tr><tr><td>개발 환경</td><td>좋음 (WSL2)</td><td>최고 (Unix 기반)</td></tr><tr><td>디자인/영상</td><td>좋음</td><td>최고 (Final Cut, Logic)</td></tr><tr><td>보안</td><td>좋음 (디펜더)</td><td>매우 좋음</td></tr><tr><td>가격</td><td>다양 (50만~)</td><td>고가 (130만~)</td></tr><tr><td>배터리</td><td>보통</td><td>우수 (M시리즈)</td></tr><tr><td>생태계</td><td>안드로이드 연동</td><td>아이폰/아이패드 연동</td></tr></tbody></table>"),
("용도별 추천","<ul><li><strong>게이밍</strong>: Windows (유일한 선택)</li><li><strong>웹개발/iOS개발</strong>: macOS</li><li><strong>영상편집</strong>: macOS (Final Cut Pro, M칩 성능)</li><li><strong>사무/일반</strong>: 둘 다 OK, 예산이면 Windows</li><li><strong>아이폰 사용자</strong>: macOS (에어드롭, 핸드오프 등)</li></ul>")],
[("맥에서 윈도우 프로그램을 쓸 수 있나요?","<strong>Parallels Desktop</strong>(유료)으로 macOS에서 윈도우를 동시에 실행할 수 있습니다. M칩에서도 ARM 윈도우가 잘 동작합니다."),
("맥북이 비싼 만큼 가치가 있나요?","배터리 수명, 빌드 퀄리티, macOS 최적화를 고려하면 <strong>5년 이상 사용 가능</strong>하여 장기적 가성비가 좋습니다.")]),

("사진 잘 찍는 법 스마트폰 카메라 설정 구도 팁 총정리","smartphone-photography-tips-2026",
[("photo-1434030216411-0b793f4b4173","스마트폰 촬영"),("photo-1460925895917-afdab827c52f","사진 구도")],
"비싼 카메라 없이도 <strong>스마트폰으로 인생샷</strong>을 찍을 수 있습니다. 3분할 구도, 빛 활용법, 야간 모드 등 누구나 바로 적용할 수 있는 사진 팁을 총정리합니다.",
[("사진 잘 찍는 핵심 팁 7가지","<ol><li><strong>3분할 구도</strong>: 카메라 격자선 켜고, 주요 피사체를 교차점에 배치</li><li><strong>빛 활용</strong>: 순광(얼굴 쪽에 빛)이 가장 예쁨. 역광은 실루엣 효과</li><li><strong>골든아워</strong>: 해 뜬 직후 / 해지기 직전 1시간이 가장 예쁜 빛</li><li><strong>배경 정리</strong>: 배경이 깔끔할수록 사진 퀄리티 상승</li><li><strong>인물 사진</strong>: 인물모드(보케) 활용, 눈 높이에서 촬영</li><li><strong>음식 사진</strong>: 45도 각도 + 자연광, 접시를 정면에서</li><li><strong>안정적 촬영</strong>: 양손으로 잡고 팔꿈치를 몸에 붙이기</li></ol>"),
("카메라 설정 팁","<ul><li><strong>격자선 ON</strong>: 설정 > 카메라 > 격자선 활성화</li><li><strong>HDR 자동</strong>: 밝기 차이 큰 장면에서 유용</li><li><strong>야간 모드</strong>: 어두운 곳에서 자동 활성화 (삼각대 추천)</li><li><strong>ProRAW/Pro 모드</strong>: 후보정 할 예정이면 RAW로 촬영</li><li><strong>해상도</strong>: 최대 해상도로 촬영 후 나중에 줄이기</li></ul>")],
[("어떤 스마트폰이 카메라가 가장 좋나요?","2026년 기준 <strong>아이폰 16 Pro, 갤럭시 S26 Ultra</strong>가 카메라 성능 최고입니다. 중급은 Pixel 9a가 가성비 우수합니다."),
("사진 후보정 앱 추천해주세요","<strong>Lightroom Mobile(무료)</strong>이 가장 강력합니다. 간편하게는 <strong>VSCO, Snapseed</strong>를 추천합니다.")]),

("무선 충전기 추천 2026 고속충전 패드 스탠드 비교 TOP 7","wireless-charger-recommendation-2026",
[("photo-1518770660439-4636190af475","무선 충전기"),("photo-1563013544-824ae1b704d3","스마트폰 충전")],
"무선 충전기는 <strong>Qi2, MagSafe</strong> 등 규격이 다양해져 선택이 어렵습니다. 삼성, 벨킨, 앤커 등 인기 무선충전기를 충전 속도, 호환성, 가격 기준으로 비교합니다.",
[("무선 충전기 TOP 7 비교","<table><thead><tr><th>모델</th><th>가격</th><th>충전속도</th><th>규격</th><th>형태</th><th>특징</th></tr></thead><tbody><tr><td>삼성 15W 듀오패드</td><td>5만원</td><td>15W</td><td>Qi</td><td>패드</td><td>폰+워치 동시 충전</td></tr><tr><td>벨킨 MagSafe 2-in-1</td><td>10만원</td><td>15W</td><td>MagSafe</td><td>스탠드</td><td>아이폰+애플워치</td></tr><tr><td>앤커 MagGo Qi2</td><td>4만원</td><td>15W</td><td>Qi2</td><td>패드</td><td>Qi2 가성비</td></tr><tr><td>모피 3-in-1</td><td>15만원</td><td>15W</td><td>MagSafe</td><td>스탠드</td><td>폰+워치+에어팟</td></tr><tr><td>삼성 컨버터블 25W</td><td>4만원</td><td>25W</td><td>Qi</td><td>패드/스탠드</td><td>갤럭시 최고속도</td></tr><tr><td>유그린 Qi2 15W</td><td>2만원</td><td>15W</td><td>Qi2</td><td>패드</td><td>초가성비</td></tr><tr><td>아이큐리 3-in-1</td><td>3만원</td><td>15W</td><td>Qi</td><td>스탠드</td><td>국산 가성비</td></tr></tbody></table>"),
("Qi vs Qi2 vs MagSafe","<table><thead><tr><th>규격</th><th>최대출력</th><th>자석정렬</th><th>호환기기</th></tr></thead><tbody><tr><td>Qi</td><td>15W</td><td>X</td><td>대부분 스마트폰</td></tr><tr><td>Qi2</td><td>15W</td><td>O</td><td>최신 안드로이드+아이폰</td></tr><tr><td>MagSafe</td><td>15W</td><td>O</td><td>아이폰 12 이상 전용</td></tr></tbody></table>")],
[("무선 충전이 배터리에 해로운가요?","최신 스마트폰은 <strong>충전 관리 기능</strong>이 있어 무선 충전이 배터리에 해롭지 않습니다. 다만 두꺼운 케이스는 발열을 유발할 수 있습니다."),
("무선 충전 속도가 유선보다 느린가요?","유선 고속충전(25~45W) 대비 무선은 <strong>15~25W로 느립니다</strong>. 급할 때는 유선, 밤새 충전은 무선이 편합니다.")]),

("한컴오피스 vs MS오피스 비교 2026 가격 기능 호환성 총정리","hancom-vs-msoffice-comparison-2026",
[("photo-1460925895917-afdab827c52f","오피스 비교"),("photo-1556742049-0cfed4f6a45d","문서 작업")],
"한국에서는 <strong>한컴오피스와 MS 오피스</strong> 중 고민하는 분이 많습니다. 가격, 기능, 호환성, 클라우드 등 모든 측면에서 두 제품을 비교합니다.",
[("가격 비교","<table><thead><tr><th>구분</th><th>한컴오피스 2024</th><th>Microsoft 365</th></tr></thead><tbody><tr><td>구매 방식</td><td>일회성 구매</td><td>월/년 구독</td></tr><tr><td>개인용</td><td>약 8만원(영구)</td><td>월 8,900원/년 89,000원</td></tr><tr><td>포함 프로그램</td><td>한글, 한셀, 한쇼</td><td>Word, Excel, PPT, OneDrive 1TB</td></tr><tr><td>클라우드</td><td>한컴스페이스 5GB</td><td>OneDrive 1TB</td></tr><tr><td>업데이트</td><td>메이저 버전별 구매</td><td>항상 최신 버전</td></tr></tbody></table>"),
("호환성 비교","<ul><li><strong>한글(.hwp)</strong>: MS Word에서 직접 열기 불가. 변환 필요</li><li><strong>Word(.docx)</strong>: 한컴에서 열기 가능하나 일부 서식 깨짐</li><li><strong>Excel(.xlsx)</strong>: 한셀에서 대부분 호환, 복잡한 매크로는 오류 가능</li><li><strong>결론</strong>: 관공서/학교는 한컴, 기업/글로벌은 MS가 표준</li></ul>")],
[("학생은 어떤 걸 써야 하나요?","대학생은 <strong>학교에서 MS 365 무료 제공</strong>하는 경우가 많습니다. 확인 후 무료 사용하세요. 공무원 시험 등은 한글이 필수입니다."),
("한글 파일을 MS Word로 변환할 수 있나요?","한컴오피스에서 '다른 이름으로 저장 > .docx'로 변환 가능합니다. 온라인 변환기(smallpdf 등)도 활용할 수 있습니다.")]),
]

POSTS=[]
for t,sl,im,intro,secs,faqs in TOPICS:
    POSTS.append({"title":t,"cat":5,"slug":sl,"images":im,
        "content":lambda imgs,intro=intro,secs=secs,faqs=faqs:pc(intro,secs,faqs,
            [cb("관련 정보 더 보기","최신 정보를 확인하세요","https://www.danawa.com/","blue"),
             cb("쿠팡에서 확인","로켓배송으로 빠르게 받아보세요","https://www.coupang.com/","yellow"),
             cb("네이버에서 검색","관련 정보를 네이버에서 확인하세요","https://search.naver.com/","green")],imgs)})

def main():
    published=[]
    for idx,post in enumerate(POSTS,1):
        print(f"\n{'='*60}\n[{idx}/{len(POSTS)}] {post['title']}\n{'='*60}")
        img_htmls=[];fmid=None
        for j,(pid,alt) in enumerate(post["images"]):
            tmp=download_image(pid)
            if not tmp:img_htmls.append("");continue
            mid,murl=upload_image(tmp,f"{post['slug']}-{j+1}",alt);os.unlink(tmp)
            if murl:img_htmls.append(ib(murl,alt));fmid=fmid or mid;print(f"  이미지{j+1} OK->{murl}")
            else:img_htmls.append("")
            time.sleep(0.5)
        content=post["content"](img_htmls)
        pl={"title":post["title"],"content":content,"status":"publish","slug":post["slug"],"categories":[post["cat"]]}
        if fmid:pl["featured_media"]=fmid
        d=json.dumps(pl).encode()
        req=urllib.request.Request(API,data=d,method="POST")
        req.add_header("Authorization",f"Basic {AUTH}");req.add_header("Content-Type","application/json")
        try:
            with urllib.request.urlopen(req,timeout=30) as r:
                j=json.loads(r.read().decode());print(f"  발행OK|ID:{j.get('id')}|{j.get('link','')}");published.append(j.get("link",""))
        except Exception as e:print(f"  발행FAIL|{e}")
        time.sleep(1)
    if published:
        print(f"\n{'='*60}\nIndexNow\n{'='*60}")
        np={"host":"devupbox.com","key":"8dbbd7d6729b4a65b7dce4b9083c65e3","keyLocation":"https://devupbox.com/8dbbd7d6729b4a65b7dce4b9083c65e3.txt","urlList":published}
        nd=json.dumps(np).encode()
        for n,u in[("Naver","https://searchadvisor.naver.com/indexnow"),("Bing","https://www.bing.com/indexnow"),("Yandex","https://yandex.com/indexnow")]:
            req=urllib.request.Request(u,data=nd,method="POST");req.add_header("Content-Type","application/json; charset=utf-8")
            try:
                with urllib.request.urlopen(req,timeout=30) as r:print(f"  {n}:HTTP {r.status}")
            except Exception as e:print(f"  {n}:{e}")
    print(f"\n완료!{len(published)}개 발행")

if __name__=="__main__":main()

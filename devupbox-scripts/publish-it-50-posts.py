import json
import urllib.request
import urllib.error
import base64
import time
import ssl
import os
import tempfile

ssl._create_default_https_context = ssl._create_unverified_context

AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API = "https://devupbox.com/wp-json/wp/v2/posts"
MEDIA_API = "https://devupbox.com/wp-json/wp/v2/media"

# 업로드된 이미지 URL 캐시 (slug -> [url1, url2])
UPLOADED_IMAGES = {}

# 주제별 Unsplash 이미지 매핑 (photo ID)
IMAGES = {
    "tablet-recommendation-2026": [
        ("photo-1544244015-0df4b3ffc6b0", "태블릿으로 작업하는 모습"),
        ("photo-1585790050230-5dd28404ccb9", "다양한 태블릿 비교"),
    ],
    "wireless-earbuds-recommendation-2026": [
        ("photo-1590658268037-6bf12f032f55", "무선 이어폰 착용 모습"),
        ("photo-1606220588913-b3aacb4d2f46", "무선 이어폰 제품 비교"),
    ],
    "monitor-recommendation-2026": [
        ("photo-1527443224154-c4a3942d3acf", "데스크 위 모니터 세팅"),
        ("photo-1593062096033-9a26b09da705", "듀얼 모니터 작업 환경"),
    ],
    "external-storage-recommendation-2026": [
        ("photo-1597872200969-2b65d56bd16b", "외장 SSD 제품"),
        ("photo-1531492746076-161ca9afad44", "데이터 저장 장치"),
    ],
    "keyboard-recommendation-2026": [
        ("photo-1587829741301-dc798b83add3", "기계식 키보드 클로즈업"),
        ("photo-1618384887929-16ec33fab9ef", "깔끔한 데스크 셋업"),
    ],
    "webcam-recommendation-2026": [
        ("photo-1596742578443-7682ef5251cd", "화상회의 모습"),
        ("photo-1609252925710-887a0a11f4ef", "웹캠 셋업"),
    ],
    "wifi-router-recommendation-2026": [
        ("photo-1606904825846-647eb07f5be2", "와이파이 공유기"),
        ("photo-1558494949-ef010cbdcc31", "네트워크 장비"),
    ],
    "ebook-reader-comparison-2026": [
        ("photo-1507003211169-0a1dd7228f2d", "전자책 리더기로 독서"),
        ("photo-1512820790803-83ca734da794", "전자책 읽기"),
    ],
    "nas-recommendation-2026": [
        ("photo-1558494949-ef010cbdcc31", "NAS 서버 장비"),
        ("photo-1544197150-b99a580bb7a8", "홈 네트워크 스토리지"),
    ],
    "power-bank-recommendation-2026": [
        ("photo-1609091839311-d5365f9ff1c5", "보조배터리 충전"),
        ("photo-1585338107529-13afc5f02586", "보조배터리 제품들"),
    ],
    "free-video-editor-recommendation-2026": [
        ("photo-1574717024653-61fd2cf4d44d", "영상 편집 화면"),
        ("photo-1536240478700-b869070f9279", "동영상 편집 작업"),
    ],
    "pdf-editor-recommendation-2026": [
        ("photo-1586281380349-632531db7ed4", "PDF 문서 작업"),
        ("photo-1450101499163-c8848c66ca85", "문서 편집 업무"),
    ],
    "screen-recorder-recommendation-2026": [
        ("photo-1611532736597-de2d4265fba3", "화면 녹화 중인 모니터"),
        ("photo-1516321318423-f06f85e504b3", "컴퓨터 화면 작업"),
    ],
    "photo-editor-recommendation-2026": [
        ("photo-1572044162444-ad60f128bdea", "사진 편집 화면"),
        ("photo-1611532736597-de2d4265fba3", "포토 에디팅 작업"),
    ],
    "note-app-comparison-2026": [
        ("photo-1517842645767-c639042777db", "메모 및 노트 정리"),
        ("photo-1484480974693-6ca0a78fb36b", "할 일 목록 정리"),
    ],
    "password-manager-recommendation-2026": [
        ("photo-1555949963-ff9fe0c870eb", "비밀번호 보안 화면"),
        ("photo-1614064641938-3bbee52942c7", "디지털 보안 잠금"),
    ],
    "free-antivirus-recommendation-2026": [
        ("photo-1563206767-5b18f218e8de", "컴퓨터 보안 화면"),
        ("photo-1510511459019-5dda7724fd87", "바이러스 보호 실드"),
    ],
    "file-compression-program-comparison-2026": [
        ("photo-1544197150-b99a580bb7a8", "파일 관리 화면"),
        ("photo-1551288049-bebda4e38f71", "데이터 파일 정리"),
    ],
    "remote-desktop-recommendation-2026": [
        ("photo-1588702547923-7093a6c3ba33", "원격 근무 화면"),
        ("photo-1585241645927-c7a158742f4a", "재택근무 데스크 셋업"),
    ],
    "ai-writing-tool-comparison-2026": [
        ("photo-1677442136019-21780ecad995", "AI 챗봇 인터페이스"),
        ("photo-1655720828018-edd2daec9349", "AI 기술 이미지"),
    ],
    "ott-service-comparison-2026": [
        ("photo-1522869635100-9f4c5e86aa37", "TV 스트리밍 시청"),
        ("photo-1611162617213-7d7a39e9b1d7", "넷플릭스 시청 모습"),
    ],
    "music-streaming-comparison-2026": [
        ("photo-1614680376593-902f74cf0d41", "음악 스트리밍 앱"),
        ("photo-1505740420928-5e560c06d30e", "헤드폰으로 음악 듣기"),
    ],
    "email-service-comparison-2026": [
        ("photo-1596526131083-e8c633c948d2", "이메일 수신함 화면"),
        ("photo-1563986768609-322da13575f2", "이메일 업무 화면"),
    ],
    "free-cloud-storage-comparison-2026": [
        ("photo-1544197150-b99a580bb7a8", "클라우드 스토리지"),
        ("photo-1451187580459-43490279c0fa", "클라우드 컴퓨팅 개념"),
    ],
    "domain-registration-comparison-2026": [
        ("photo-1460925895917-afdab827c52f", "웹사이트 도메인 화면"),
        ("photo-1504639725590-34d0984388bd", "웹 개발 코딩"),
    ],
    "web-hosting-recommendation-2026": [
        ("photo-1558494949-ef010cbdcc31", "서버 호스팅 장비"),
        ("photo-1504639725590-34d0984388bd", "웹 개발 화면"),
    ],
    "nocode-website-builder-comparison-2026": [
        ("photo-1460925895917-afdab827c52f", "웹사이트 디자인"),
        ("photo-1547658719-da2b51169166", "반응형 웹 디자인"),
    ],
    "e-signature-service-comparison-2026": [
        ("photo-1450101499163-c8848c66ca85", "전자서명 문서 작업"),
        ("photo-1554224155-6726b3ff858f", "계약서 서명"),
    ],
    "video-conference-comparison-2026": [
        ("photo-1609619385076-36a431dc1bcc", "화상회의 진행"),
        ("photo-1588196749597-9ff075ee6b5b", "온라인 미팅"),
    ],
    "blog-platform-comparison-2026": [
        ("photo-1499750310107-5fef28a66643", "블로그 작성 화면"),
        ("photo-1486312338219-ce68d2c6f44d", "노트북으로 글쓰기"),
    ],
    "smishing-prevention-guide-2026": [
        ("photo-1563013544-824ae1b704d3", "스마트폰 보안 경고"),
        ("photo-1614064641938-3bbee52942c7", "모바일 보안"),
    ],
    "two-factor-authentication-guide-2026": [
        ("photo-1555949963-ff9fe0c870eb", "2단계 인증 화면"),
        ("photo-1614064641938-3bbee52942c7", "보안 인증 절차"),
    ],
    "personal-data-breach-check-2026": [
        ("photo-1563013544-824ae1b704d3", "개인정보 보호"),
        ("photo-1510511459019-5dda7724fd87", "데이터 보안 실드"),
    ],
    "public-wifi-security-guide-2026": [
        ("photo-1606904825846-647eb07f5be2", "공공 와이파이"),
        ("photo-1555949963-ff9fe0c870eb", "네트워크 보안"),
    ],
    "smartphone-hacking-check-guide-2026": [
        ("photo-1563013544-824ae1b704d3", "스마트폰 해킹 경고"),
        ("photo-1614064641938-3bbee52942c7", "모바일 보안 점검"),
    ],
    "ad-tracking-block-guide-2026": [
        ("photo-1555949963-ff9fe0c870eb", "광고 차단 설정"),
        ("photo-1516321318423-f06f85e504b3", "브라우저 보안 설정"),
    ],
    "ransomware-prevention-guide-2026": [
        ("photo-1563206767-5b18f218e8de", "랜섬웨어 경고 화면"),
        ("photo-1510511459019-5dda7724fd87", "사이버 보안"),
    ],
    "windows-11-optimization-guide-2026": [
        ("photo-1624571409412-1f253a335b17", "윈도우 11 데스크톱"),
        ("photo-1516321318423-f06f85e504b3", "PC 최적화 설정"),
    ],
    "windows-reinstall-guide-2026": [
        ("photo-1624571409412-1f253a335b17", "윈도우 설치 화면"),
        ("photo-1597872200969-2b65d56bd16b", "USB 부팅 디스크"),
    ],
    "smartphone-storage-cleanup-guide-2026": [
        ("photo-1563013544-824ae1b704d3", "스마트폰 저장공간 관리"),
        ("photo-1512941937669-90a1b58e7e9c", "스마트폰 앱 정리"),
    ],
    "iphone-vs-galaxy-comparison-2026": [
        ("photo-1592750475338-74b7b21085ab", "아이폰 vs 갤럭시 비교"),
        ("photo-1511707171634-5f897ff02aa9", "스마트폰 비교"),
    ],
    "dual-monitor-setup-guide-2026": [
        ("photo-1593062096033-9a26b09da705", "듀얼 모니터 셋업"),
        ("photo-1527443224154-c4a3942d3acf", "다중 모니터 작업 환경"),
    ],
    "chrome-extension-recommendation-2026": [
        ("photo-1516321318423-f06f85e504b3", "크롬 브라우저 화면"),
        ("photo-1551288049-bebda4e38f71", "브라우저 확장 프로그램"),
    ],
    "windows-keyboard-shortcuts-2026": [
        ("photo-1587829741301-dc798b83add3", "키보드 단축키"),
        ("photo-1618384887929-16ec33fab9ef", "업무용 키보드"),
    ],
    "google-drive-tips-guide-2026": [
        ("photo-1544197150-b99a580bb7a8", "구글 드라이브 클라우드"),
        ("photo-1451187580459-43490279c0fa", "클라우드 활용"),
    ],
    "youtube-premium-guide-2026": [
        ("photo-1611162616475-46b635cb6868", "유튜브 시청 화면"),
        ("photo-1522869635100-9f4c5e86aa37", "영상 스트리밍"),
    ],
    "smart-home-beginner-guide-2026": [
        ("photo-1558618666-fcd25c85f82e", "스마트홈 IoT 기기"),
        ("photo-1556761175-b413da4baf72", "AI 스피커"),
    ],
    "qr-code-generator-guide-2026": [
        ("photo-1595079676339-1534801ad6cf", "QR코드 스캔"),
        ("photo-1556742049-0cfed4f6a45d", "QR코드 활용"),
    ],
    "wifi-speed-fix-guide-2026": [
        ("photo-1606904825846-647eb07f5be2", "와이파이 공유기"),
        ("photo-1558494949-ef010cbdcc31", "네트워크 속도 측정"),
    ],
    "used-laptop-buying-guide-2026": [
        ("photo-1496181133206-80ce9b88a853", "중고 노트북 점검"),
        ("photo-1525547719571-a2d4ac8945e2", "노트북 구매 가이드"),
    ],
}

def download_image(photo_id):
    """Unsplash에서 이미지를 다운로드하여 임시 파일 경로 반환"""
    url = f"https://images.unsplash.com/{photo_id}?w=800&h=450&fit=crop&auto=format&q=80"
    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0")
        with urllib.request.urlopen(req, timeout=30) as resp:
            tmp.write(resp.read())
        tmp.close()
        return tmp.name
    except Exception as e:
        tmp.close()
        os.unlink(tmp.name)
        print(f"  이미지 다운로드 실패 ({photo_id}): {e}")
        return None


def upload_image_to_wp(file_path, filename, alt_text):
    """WordPress 미디어 라이브러리에 이미지 업로드 후 URL 반환"""
    with open(file_path, "rb") as f:
        image_data = f.read()

    req = urllib.request.Request(MEDIA_API, data=image_data, method="POST")
    req.add_header("Authorization", f"Basic {AUTH}")
    req.add_header("Content-Type", "image/jpeg")
    req.add_header("Content-Disposition", f'attachment; filename="{filename}.jpg"')

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            media_id = result.get("id")
            media_url = result.get("source_url", "")

            # alt_text 업데이트
            if media_id and alt_text:
                update_data = json.dumps({"alt_text": alt_text}).encode("utf-8")
                update_req = urllib.request.Request(
                    f"{MEDIA_API}/{media_id}", data=update_data, method="POST"
                )
                update_req.add_header("Authorization", f"Basic {AUTH}")
                update_req.add_header("Content-Type", "application/json")
                try:
                    urllib.request.urlopen(update_req, timeout=15)
                except Exception:
                    pass

            return media_url
    except urllib.error.HTTPError as e:
        print(f"  WP 업로드 실패: HTTP {e.code} - {e.read().decode()[:200]}")
        return None
    except Exception as e:
        print(f"  WP 업로드 실패: {e}")
        return None


def upload_all_images():
    """모든 이미지를 WordPress에 업로드하고 URL 캐시에 저장"""
    total = sum(len(v) for v in IMAGES.items().__iter__() if False)
    total = sum(len(imgs) for imgs in IMAGES.values())
    uploaded = 0
    failed = 0

    print("=" * 60)
    print(f"이미지 업로드 시작 (총 {total}장)")
    print("=" * 60)

    for slug, img_list in IMAGES.items():
        UPLOADED_IMAGES[slug] = []
        for idx, (photo_id, alt_text) in enumerate(img_list):
            filename = f"{slug}-{idx+1}"
            # 다운로드
            tmp_path = download_image(photo_id)
            if not tmp_path:
                UPLOADED_IMAGES[slug].append(("", alt_text))
                failed += 1
                continue

            # 업로드
            wp_url = upload_image_to_wp(tmp_path, filename, alt_text)
            os.unlink(tmp_path)  # 임시파일 삭제

            if wp_url:
                UPLOADED_IMAGES[slug].append((wp_url, alt_text))
                uploaded += 1
                print(f"  [{uploaded+failed}/{total}] OK | {filename} -> {wp_url}")
            else:
                UPLOADED_IMAGES[slug].append(("", alt_text))
                failed += 1
                print(f"  [{uploaded+failed}/{total}] FAIL | {filename}")

            time.sleep(0.5)

    print(f"\n이미지 업로드 완료: 성공 {uploaded}, 실패 {failed}\n")


def get_image_html(slug, index):
    """업로드된 WordPress 이미지로 HTML 생성"""
    imgs = UPLOADED_IMAGES.get(slug, [])
    if index >= len(imgs):
        return ""
    wp_url, alt_text = imgs[index]
    if not wp_url:
        return ""
    return f'''<figure style="margin:32px 0;text-align:center;">
<img src="{wp_url}" alt="{alt_text}" style="width:100%;max-width:800px;height:auto;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.10);" loading="lazy" />
<figcaption style="margin-top:8px;font-size:13px;color:#6b7280;">{alt_text}</figcaption>
</figure>'''

POSTS = [
    # ===== 기기/하드웨어 (1-10) =====
    {
        "title": "태블릿 추천 2026 용도별 가성비 TOP 10",
        "cat": 5,
        "slug": "tablet-recommendation-2026",
        "intro": "스마트폰과 노트북 사이, 딱 맞는 디바이스를 찾고 계신가요? <strong>태블릿</strong>은 동영상 감상, 전자책, 그림 그리기, 업무까지 용도에 따라 천차만별입니다. 2026년 기준 iPad, 갤럭시 탭, 레노버까지 국내에서 구매 가능한 태블릿 전 모델을 비교하고, 용도별·가격대별 최적의 선택을 안내합니다.",
        "sections": [
            ("태블릿 전체 스펙 비교표 2026", "<table><thead><tr><th>모델</th><th>출시가</th><th>화면</th><th>AP</th><th>RAM</th><th>배터리</th><th>특징</th></tr></thead><tbody><tr><td>iPad Pro 13인치 M4</td><td>179만원~</td><td>13인치 OLED</td><td>Apple M4</td><td>16GB</td><td>10,290mAh</td><td>최고 성능, 창작 전문가용</td></tr><tr><td>iPad Air 13인치 M2</td><td>109만원~</td><td>13인치 LCD</td><td>Apple M2</td><td>8GB</td><td>8,635mAh</td><td>고성능 가성비</td></tr><tr><td>iPad 10세대</td><td>59만원~</td><td>10.9인치 LCD</td><td>A14 Bionic</td><td>4GB</td><td>7,606mAh</td><td>입문용 최적</td></tr><tr><td>Galaxy Tab S10 Ultra</td><td>189만원~</td><td>14.6인치 AMOLED</td><td>Snapdragon 8 Gen 3</td><td>12GB</td><td>11,200mAh</td><td>안드로이드 최강</td></tr><tr><td>Galaxy Tab S10 FE</td><td>69만원~</td><td>10.9인치 LCD</td><td>Exynos 1580</td><td>8GB</td><td>10,090mAh</td><td>안드로이드 가성비</td></tr><tr><td>Galaxy Tab A9+</td><td>39만원~</td><td>11인치 LCD</td><td>Snapdragon 695</td><td>4GB</td><td>7,040mAh</td><td>저가형 최강</td></tr><tr><td>Lenovo Tab P12 Pro</td><td>79만원~</td><td>12.6인치 AMOLED</td><td>Snapdragon 870</td><td>8GB</td><td>10,200mAh</td><td>가성비 대화면</td></tr><tr><td>Lenovo Tab M11</td><td>25만원~</td><td>11인치 LCD</td><td>Helio G88</td><td>4GB</td><td>7,700mAh</td><td>초저가 입문</td></tr></tbody></table>"),
            ("용도별 태블릿 추천", "<h3>영상 감상용</h3><p>영상 감상이 주목적이라면 <strong>디스플레이 품질</strong>이 가장 중요합니다. OLED 패널의 Galaxy Tab S10 Ultra 또는 iPad Pro가 최상이지만, 가성비를 원한다면 Lenovo Tab P12 Pro(AMOLED, 79만원)가 탁월한 선택입니다.</p><h3>그림/디자인 창작용</h3><p>Apple Pencil 지원의 <strong>iPad Pro M4</strong>가 압도적입니다. Procreate, Adobe Fresco 등 창작 앱 생태계가 독보적입니다. S-Pen을 선호하면 Galaxy Tab S10+를 추천합니다.</p><h3>업무/문서 작업용</h3><p>키보드 커버와 함께 사용하는 업무용이라면 <strong>iPad Air M2 + Magic Keyboard</strong> 조합이 최고입니다. 윈도우 호환성이 필요하면 Surface Go 3를 검토하세요.</p><h3>전자책/공부용</h3><p>무게가 가볍고 배터리가 긴 제품이 유리합니다. <strong>iPad 10세대</strong>(468g)나 <strong>Galaxy Tab A9+</strong>(480g)가 오래 들고 다니기 좋습니다.</p><h3>게임용</h3><p>고성능 게임은 <strong>iPad Pro M4</strong> 또는 <strong>Galaxy Tab S10</strong>이 최적입니다. 원신, 리니지M 같은 고사양 게임도 끊김 없이 구동됩니다.</p>"),
            ("가격대별 최적 추천", "<h3>30만원 이하 (입문/서브)</h3><ul><li><strong>Lenovo Tab M11</strong> (25만원): 유튜브, 전자책, 가벼운 사용</li><li><strong>Galaxy Tab A9+</strong> (39만원): 넓은 화면, 안드로이드 앱 활용</li></ul><h3>50~80만원 (중급)</h3><ul><li><strong>iPad 10세대</strong> (59만원): Apple 생태계, iPadOS 앱 활용</li><li><strong>Galaxy Tab S10 FE</strong> (69만원): 안드로이드 준고급, S-Pen 지원</li><li><strong>Lenovo Tab P12 Pro</strong> (79만원): AMOLED 대화면 가성비</li></ul><h3>100만원 이상 (고급)</h3><ul><li><strong>iPad Air M2</strong> (109만원~): 고성능 작업, Apple 생태계</li><li><strong>Galaxy Tab S10 Ultra</strong> (189만원~): 최대 화면, 안드로이드 최강</li><li><strong>iPad Pro M4</strong> (179만원~): 궁극의 성능과 디스플레이</li></ul>"),
            ("태블릿 vs 노트북 어떤 것을 선택해야 할까", "<p>많은 분들이 태블릿과 노트북 사이에서 고민합니다. 선택 기준을 정리하면:</p><table><thead><tr><th>구분</th><th>태블릿</th><th>노트북</th></tr></thead><tbody><tr><td>휴대성</td><td>매우 우수</td><td>보통</td></tr><tr><td>터치/필기</td><td>우수</td><td>제한적</td></tr><tr><td>타이핑 작업</td><td>불편 (커버 필요)</td><td>우수</td></tr><tr><td>멀티태스킹</td><td>제한적</td><td>우수</td></tr><tr><td>소프트웨어 호환</td><td>제한적</td><td>윈도우 앱 전체</td></tr><tr><td>가격</td><td>다양</td><td>다양</td></tr><tr><td>배터리</td><td>우수</td><td>보통</td></tr></tbody></table><p><strong>결론</strong>: 콘텐츠 소비, 창작, 이동이 많다면 태블릿. 코딩, 엑셀, 문서 작업이 많다면 노트북을 선택하세요.</p>"),
            ("태블릿 구매 시 반드시 체크할 5가지", "<ol><li><strong>셀룰러 vs Wi-Fi 모델</strong>: 야외에서 LTE/5G가 필요하면 셀룰러 모델(5~10만원 추가)을 선택하세요.</li><li><strong>스토리지 용량</strong>: 최소 128GB 추천. 동영상·앱이 많다면 256GB 이상. 안드로이드 태블릿은 microSD 확장 가능 여부 확인.</li><li><strong>스타일러스 호환 여부</strong>: iPad는 Apple Pencil, 갤럭시 탭은 S-Pen 지원 여부를 확인하세요.</li><li><strong>OS 생태계</strong>: 아이폰 사용자는 iPad, 갤럭시 사용자는 갤럭시 탭이 연동성이 우수합니다.</li><li><strong>키보드 커버 가격</strong>: 업무용으로 사용 시 키보드 커버 가격(5~30만원)을 총 예산에 포함하세요.</li></ol>"),
        ],
        "faq": [
            ("아이패드와 갤럭시 탭 중 무엇이 더 좋나요?", "용도에 따라 다릅니다. <strong>앱 생태계와 창작 도구(Apple Pencil)</strong>는 iPad가 우수하고, <strong>안드로이드 파일 관리와 가격 다양성</strong>은 갤럭시 탭이 낫습니다. 아이폰 사용자라면 iPad, 갤럭시 사용자라면 갤럭시 탭을 추천합니다."),
            ("태블릿으로 MS 오피스 작업이 가능한가요?", "iPad와 갤럭시 탭 모두 <strong>Microsoft 365 앱</strong>이 지원됩니다. 다만 PC 버전에 비해 기능이 제한적이므로, 복잡한 엑셀/파워포인트 작업이 많다면 노트북을 추천합니다."),
            ("태블릿 AS는 어디서 받나요?", "iPad는 <strong>애플 공식 서비스 센터</strong> 또는 공인 서비스 제공업체(AASP), 갤럭시 탭은 <strong>삼성 서비스센터</strong>에서 받을 수 있습니다. 구매 시 AppleCare+ 또는 삼성케어플러스 가입을 고려하세요."),
            ("중고 태블릿 구매해도 괜찮을까요?", "배터리 상태(80% 이상 권장), 화면 잔상·불량화소 여부, 충전 포트 상태를 반드시 확인하세요. <strong>당근마켓, 번개장터</strong>에서 직거래 시 실물 확인 후 구매를 권장합니다."),
        ],
        "ctas": [
            {"text": "태블릿 최저가 비교하기", "desc": "다나와에서 전 모델 실시간 최저가를 확인하세요", "url": "https://www.danawa.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "쿠팡에서 태블릿 로켓배송 받기", "desc": "오늘 주문하면 내일 도착! 쿠팡 로켓배송으로 받아보세요", "url": "https://www.coupang.com/np/search?q=태블릿", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "네이버 쇼핑에서 최저가 찾기", "desc": "네이버 가격비교로 최저가 판매처를 한눈에 비교하세요", "url": "https://search.shopping.naver.com/search/all?query=태블릿", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "무선 이어폰 추천 2026 가성비 음질 비교 TOP 7",
        "cat": 5,
        "slug": "wireless-earbuds-recommendation-2026",
        "intro": "2026년 무선 이어폰 시장은 <strong>노이즈캔슬링, 공간음향, 30시간 이상 배터리</strong>가 기본 스펙이 됐습니다. AirPods Pro부터 5만원대 가성비 이어폰까지, 예산과 용도에 맞는 최적의 무선 이어폰을 비교합니다. 음질, ANC 성능, 배터리, 착용감까지 실제 사용 기준으로 랭킹을 매겼습니다.",
        "sections": [
            ("무선 이어폰 전체 스펙 비교표", "<table><thead><tr><th>모델</th><th>가격</th><th>ANC</th><th>배터리(케이스포함)</th><th>코덱</th><th>방수</th><th>특징</th></tr></thead><tbody><tr><td>AirPods Pro 2세대</td><td>35만원</td><td>최상급</td><td>6+24시간</td><td>AAC</td><td>IPX4</td><td>아이폰 최적화</td></tr><tr><td>Galaxy Buds 3 Pro</td><td>28만원</td><td>상급</td><td>6+21시간</td><td>aptX Adaptive</td><td>IPX7</td><td>갤럭시 최적화</td></tr><tr><td>Sony WF-1000XM6</td><td>39만원</td><td>최상급</td><td>8+24시간</td><td>LDAC</td><td>IPX4</td><td>음질 최강</td></tr><tr><td>Bose QuietComfort Earbuds II</td><td>32만원</td><td>최상급</td><td>6+18시간</td><td>AAC/SBC</td><td>IPX4</td><td>ANC 최강</td></tr><tr><td>Jabra Elite 10</td><td>25만원</td><td>상급</td><td>6+27시간</td><td>aptX Adaptive</td><td>IP57</td><td>착용감 우수</td></tr><tr><td>Anker Soundcore Liberty 4</td><td>9만원</td><td>중급</td><td>9+32시간</td><td>LDAC</td><td>IPX4</td><td>가성비 최강</td></tr><tr><td>EarFun Air Pro 4</td><td>6만원</td><td>중급</td><td>9+36시간</td><td>aptX Adaptive</td><td>IPX5</td><td>초가성비</td></tr></tbody></table>"),
            ("노이즈캔슬링(ANC) 성능 비교", "<p>ANC 성능은 단순 스펙표로 비교하기 어렵습니다. 실제 환경(지하철, 카페, 비행기)에서의 소음 차단 효과를 기준으로 평가했습니다.</p><h3>1위: Sony WF-1000XM6 / Bose QC Earbuds II (공동)</h3><p>두 제품 모두 업계 최고 수준의 ANC를 제공합니다. Sony는 LDAC 고음질과 ANC를 동시에 지원하고, Bose는 착용감이 더 편안합니다.</p><h3>2위: AirPods Pro 2세대</h3><p>H2 칩 기반 ANC로 아이폰 사용자에게는 최적입니다. 적응형 투명 모드가 매우 자연스럽습니다.</p><h3>3위: Galaxy Buds 3 Pro</h3><p>갤럭시 기기와 연동 시 360 오디오, 음성 감지 기능이 활성화됩니다.</p><h3>가성비 ANC: Anker Soundcore Liberty 4</h3><p>9만원대에서 중급 이상의 ANC 성능을 제공합니다. 지하철 소음 약 70% 차단.</p>"),
            ("음질 비교 코덱별 차이점", "<table><thead><tr><th>코덱</th><th>최대 비트레이트</th><th>음질</th><th>지연</th><th>지원 기기</th></tr></thead><tbody><tr><td>LDAC</td><td>990kbps</td><td>최상</td><td>높음</td><td>안드로이드</td></tr><tr><td>aptX Adaptive</td><td>952kbps</td><td>상</td><td>낮음</td><td>안드로이드(퀄컴)</td></tr><tr><td>AAC</td><td>256kbps</td><td>중상</td><td>낮음</td><td>iOS/안드로이드</td></tr><tr><td>SBC</td><td>328kbps</td><td>중</td><td>보통</td><td>모든 기기(기본)</td></tr></tbody></table><p><strong>음질 최우선</strong>이라면 LDAC 지원 제품(Sony WF-1000XM6, Anker Liberty 4)을 선택하세요. 단, LDAC는 안드로이드에서만 최대 성능이 발휘됩니다.</p>"),
            ("배터리 및 충전 비교", "<ul><li><strong>EarFun Air Pro 4</strong>: 9+36시간 = 총 45시간. 충전 케이스 무선충전 지원</li><li><strong>Anker Liberty 4</strong>: 9+32시간 = 총 41시간. 무선충전 지원</li><li><strong>Jabra Elite 10</strong>: 6+27시간 = 총 33시간. 고속충전(5분=1시간)</li><li><strong>AirPods Pro 2</strong>: 6+24시간. MagSafe 충전 지원</li><li><strong>Sony WF-1000XM6</strong>: 8+24시간. LDAC+ANC 동시 사용 시 6시간</li></ul>"),
            ("용도별 최종 추천", "<h3>아이폰 사용자</h3><p><strong>AirPods Pro 2세대</strong> - 애플 기기와의 완벽한 연동, 자동 전환, 공간음향이 타 제품 대비 압도적입니다.</p><h3>안드로이드/갤럭시 사용자</h3><p><strong>Galaxy Buds 3 Pro</strong> - 갤럭시와의 에코시스템 연동, Galaxy AI 기능 활용.</p><h3>음질 최우선</h3><p><strong>Sony WF-1000XM6</strong> - LDAC 고음질, 업계 최고 ANC 동시 제공.</p><h3>예산 10만원 이하 가성비</h3><p><strong>Anker Soundcore Liberty 4</strong> (9만원) - LDAC 지원, 중급 ANC, 32시간 배터리로 가성비 압도적.</p><h3>초가성비 5만원대</h3><p><strong>EarFun Air Pro 4</strong> (6만원) - aptX Adaptive, 45시간 배터리, IPX5 방수. 가성비로는 넘사벽.</p>"),
        ],
        "faq": [
            ("무선 이어폰 음질이 유선보다 나쁜가요?", "LDAC, aptX Adaptive 같은 고음질 코덱을 지원하는 제품이라면 <strong>일반 유선 이어폰과 비슷하거나 그 이상</strong>의 음질을 제공합니다. 단, 하이파이 오디오 수준을 원한다면 유선이 여전히 유리합니다."),
            ("운동할 때 쓰기 좋은 무선 이어폰은?", "<strong>Jabra Elite 10 (IP57, 완전방수)</strong> 또는 <strong>EarFun Air Pro 4 (IPX5)</strong>를 추천합니다. 핏(착용감) 유지가 중요하므로 반드시 착용해보고 구매하세요."),
            ("무선 이어폰 한쪽만 충전이 안 될 때 어떻게 하나요?", "케이스의 충전 핀 접촉 불량이 원인인 경우가 많습니다. <strong>면봉으로 핀 청소 후 재시도</strong>해보세요. 개선되지 않으면 공식 AS를 받으시기 바랍니다."),
        ],
        "ctas": [
            {"text": "무선 이어폰 최저가 비교", "desc": "다나와에서 전 모델 실시간 최저가와 스펙을 비교하세요", "url": "https://www.danawa.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "쿠팡 무선이어폰 특가 확인", "desc": "로켓배송 무선 이어폰 오늘의 특가를 확인하세요", "url": "https://www.coupang.com/np/search?q=무선이어폰", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "소니 공식몰에서 WF-1000XM6 보기", "desc": "소니 공식몰에서 정품 구매 및 AS 혜택을 확인하세요", "url": "https://www.sony.co.kr/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "모니터 추천 2026 사무용 게이밍 영상편집 용도별 비교",
        "cat": 5,
        "slug": "monitor-recommendation-2026",
        "intro": "모니터는 하루 8시간 이상 바라보는 디바이스입니다. <strong>사무용, 게이밍, 영상편집</strong>에 따라 필요한 스펙이 완전히 다릅니다. 2026년 기준 LG, 삼성, Dell, BenQ 등 주요 브랜드의 추천 모니터를 용도별로 비교합니다.",
        "sections": [
            ("모니터 구매 전 필수 용어 정리", "<table><thead><tr><th>용어</th><th>설명</th><th>권장 스펙</th></tr></thead><tbody><tr><td>해상도</td><td>화면 픽셀 수 (FHD/QHD/4K)</td><td>27인치 이상은 QHD 이상</td></tr><tr><td>패널 종류</td><td>IPS/VA/TN/OLED</td><td>IPS(색재현), VA(명암비), OLED(최고화질)</td></tr><tr><td>주사율</td><td>초당 화면 갱신 횟수(Hz)</td><td>게이밍 144Hz+, 사무 60~75Hz</td></tr><tr><td>응답속도</td><td>픽셀 색 변환 시간(ms)</td><td>게이밍 1ms, 사무 5ms 이하</td></tr><tr><td>색재현율</td><td>sRGB/DCI-P3 커버리지</td><td>영상편집 DCI-P3 95%+</td></tr><tr><td>HDR</td><td>밝기/명암비 확장 기술</td><td>HDR400 이상 권장</td></tr></tbody></table>"),
            ("사무용 모니터 추천 TOP 3", "<h3>1. LG 27QN600-B (27인치 QHD IPS) - 25만원</h3><p>사무용 모니터의 정석입니다. 27인치 QHD(2560×1440) IPS 패널로 텍스트가 선명하고 눈이 덜 피로합니다.</p><ul><li>해상도: 2560×1440 (QHD)</li><li>패널: IPS, sRGB 99%</li><li>주사율: 75Hz</li><li>특징: AMD FreeSync, HDR10, 블루라이트 차단</li></ul><h3>2. Dell S2722QC (27인치 4K IPS USB-C) - 45만원</h3><p>USB-C 단일 케이블로 노트북 연결+충전이 되는 실용적인 4K 모니터입니다.</p><ul><li>해상도: 3840×2160 (4K UHD)</li><li>USB-C 65W 충전 지원</li><li>MacBook, 갤럭시북 연결 최적</li></ul><h3>3. 삼성 S60A (24인치 FHD) - 18만원</h3><p>예산이 제한적이라면 삼성 S60A. FHD 해상도로 문서 작업에 충분합니다.</p>"),
            ("게이밍 모니터 추천 TOP 3", "<h3>1. LG 27GP850-B (27인치 QHD 180Hz Nano IPS) - 45만원</h3><p>게이밍 모니터 베스트셀러. 빠른 응답속도와 선명한 색재현을 동시에 제공합니다.</p><ul><li>해상도: 2560×1440 QHD</li><li>주사율: 180Hz (OC)</li><li>응답속도: 1ms GtG</li><li>G-Sync Compatible, AMD FreeSync Premium</li></ul><h3>2. Samsung Odyssey G7 (32인치 QHD 240Hz VA) - 75만원</h3><p>1000R 커브드 VA 패널로 몰입감이 최고입니다. 리그 오브 레전드, FPS에 최적.</p><ul><li>해상도: 2560×1440 QHD</li><li>주사율: 240Hz</li><li>응답속도: 1ms</li><li>DisplayHDR 600</li></ul><h3>3. BenQ EX2710Q (27인치 QHD 165Hz IPS) - 38만원</h3><p>눈 보호 기술(아이케어)이 우수하고 가성비도 좋은 게이밍 모니터입니다.</p>"),
            ("영상편집 모니터 추천 TOP 3", "<h3>1. LG 27UK850-W (27인치 4K IPS) - 55만원</h3><p>4K UHD 해상도에 sRGB 99%, DCI-P3 95% 색재현율로 영상 편집의 표준입니다.</p><ul><li>USB-C 60W 충전 지원</li><li>HDR10, True Color Pro 캘리브레이션</li></ul><h3>2. Dell UltraSharp U2723QE (27인치 4K IPS Black) - 90만원</h3><p>IPS Black 패널로 명암비가 기존 IPS 대비 2배 향상되었습니다. 전문 영상 작업자용.</p><ul><li>IPS Black 패널: 명암비 2000:1</li><li>색정확도 ΔE &lt; 2</li><li>USB-C 90W</li></ul><h3>3. ASUS ProArt PA279CV (27인치 4K IPS) - 65만원</h3><p>공장 캘리브레이션으로 구매 즉시 정확한 색을 사용할 수 있습니다.</p>"),
            ("모니터 크기별 최적 해상도 가이드", "<table><thead><tr><th>모니터 크기</th><th>최적 해상도</th><th>이유</th></tr></thead><tbody><tr><td>22~24인치</td><td>FHD (1920×1080)</td><td>PPI 충분, 가성비 최고</td></tr><tr><td>27인치</td><td>QHD (2560×1440)</td><td>FHD는 픽셀이 보임, 4K는 글씨가 작음</td></tr><tr><td>32인치</td><td>QHD 또는 4K</td><td>용도에 따라 선택</td></tr><tr><td>34인치 이상 (울트라와이드)</td><td>UWQHD (3440×1440)</td><td>21:9 비율, 화면 분할 작업 최적</td></tr></tbody></table>"),
        ],
        "faq": [
            ("27인치 모니터에 FHD와 QHD 중 어떤 것이 나은가요?", "27인치에서 FHD는 픽셀이 다소 거칠어 보입니다. <strong>QHD(2560×1440)를 강력 추천</strong>합니다. 가격 차이가 5~10만원 정도인데 체감 화질 차이는 매우 큽니다."),
            ("144Hz와 60Hz 모니터 차이가 실제로 느껴지나요?", "FPS 게임(배틀그라운드, 발로란트)을 한다면 <strong>144Hz 이상이 확실히 느껴집니다</strong>. 반면 사무·유튜브 용도라면 75Hz도 충분합니다."),
            ("모니터 눈 피로를 줄이는 방법은?", "플리커 프리(Flicker-Free) 인증 제품을 선택하고, <strong>블루라이트 차단 모드</strong>를 활성화하세요. 모니터 밝기는 100~150cd/m² 수준으로 낮추는 것이 좋습니다."),
        ],
        "ctas": [
            {"text": "모니터 실시간 최저가 비교하기", "desc": "다나와에서 브랜드·크기·해상도별 최저가를 비교하세요", "url": "https://www.danawa.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "LG 모니터 공식몰 특가 확인", "desc": "LG 공식몰에서 최신 모니터 특가 프로모션을 확인하세요", "url": "https://www.lge.co.kr/monitors", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "삼성 공식몰 모니터 보기", "desc": "삼성 오디세이 게이밍 모니터 공식 할인 혜택을 받으세요", "url": "https://www.samsung.com/sec/monitors/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "외장하드 vs SSD 외장 스토리지 추천 비교 2026",
        "cat": 5,
        "slug": "external-storage-recommendation-2026",
        "intro": "소중한 파일을 안전하게 보관하려면 외장 스토리지가 필수입니다. 2026년에는 <strong>외장 SSD 가격이 크게 낮아지면서</strong> 외장 HDD와의 선택이 더욱 고민됩니다. Samsung T9, SanDisk Extreme, WD My Passport 등 주요 제품을 속도·가격·안전성 기준으로 비교합니다.",
        "sections": [
            ("외장 HDD vs 외장 SSD 핵심 차이점", "<table><thead><tr><th>구분</th><th>외장 HDD</th><th>외장 SSD</th></tr></thead><tbody><tr><td>속도(읽기)</td><td>100~150MB/s</td><td>500~2,000MB/s</td></tr><tr><td>속도(쓰기)</td><td>80~120MB/s</td><td>400~1,900MB/s</td></tr><tr><td>가격(1TB)</td><td>5~8만원</td><td>10~15만원</td></tr><tr><td>충격 저항</td><td>낮음 (내부 플래터)</td><td>높음 (낙하 내성)</td></tr><tr><td>소음</td><td>있음</td><td>없음</td></tr><tr><td>발열</td><td>보통</td><td>낮음</td></tr><tr><td>수명</td><td>3~5년 (보관)</td><td>5~10년 (보관)</td></tr><tr><td>용량 옵션</td><td>1~8TB</td><td>500GB~4TB</td></tr></tbody></table>"),
            ("외장 SSD 추천 TOP 4 (2026)", "<h3>1. Samsung T9 (USB 3.2 Gen 2x2)</h3><ul><li>읽기: 최대 2,000MB/s, 쓰기: 1,950MB/s</li><li>가격: 1TB 15만원, 2TB 25만원</li><li>IP65 방진·방수, AES 256비트 암호화</li><li><strong>추천 대상</strong>: 영상 작업자, 고속 전송 필요</li></ul><h3>2. SanDisk Extreme Pro V2</h3><ul><li>읽기: 2,000MB/s, 쓰기: 2,000MB/s</li><li>가격: 1TB 14만원</li><li>IP65 방진·방수, 낙하 2m 내성</li><li><strong>추천 대상</strong>: 야외 활동, 사진작가</li></ul><h3>3. WD My Passport SSD</h3><ul><li>읽기: 1,050MB/s, 쓰기: 1,000MB/s</li><li>가격: 1TB 11만원</li><li>256비트 AES 암호화, NVM Express</li><li><strong>추천 대상</strong>: 일반 백업, 합리적 가격</li></ul><h3>4. Crucial X9 Pro</h3><ul><li>읽기: 1,050MB/s, 쓰기: 1,000MB/s</li><li>가격: 1TB 9만원</li><li>IP55 방진·방수</li><li><strong>추천 대상</strong>: 가성비 최우선</li></ul>"),
            ("외장 HDD 추천 TOP 3 (2026)", "<h3>1. WD My Passport 5TB</h3><ul><li>읽기/쓰기: 120~130MB/s</li><li>가격: 4TB 9만원, 5TB 12만원</li><li>USB 3.0, 256비트 AES 암호화</li><li><strong>추천 대상</strong>: 대용량 백업, 동영상 보관</li></ul><h3>2. Seagate Backup Plus Portable 4TB</h3><ul><li>읽기/쓰기: 130MB/s</li><li>가격: 4TB 8만원</li><li>Seagate Backup 소프트웨어 포함</li><li><strong>추천 대상</strong>: 자동 백업 설정 원하는 분</li></ul><h3>3. Toshiba Canvio Basics 4TB</h3><ul><li>읽기/쓰기: 120MB/s</li><li>가격: 4TB 7.5만원</li><li>플러그앤플레이, 드라이버 불필요</li><li><strong>추천 대상</strong>: 저렴한 대용량 백업</li></ul>"),
            ("용량별 가격 비교표 2026", "<table><thead><tr><th>용량</th><th>외장 HDD 평균가</th><th>외장 SSD 평균가</th><th>가격 차이</th></tr></thead><tbody><tr><td>500GB</td><td>4만원</td><td>7만원</td><td>3만원</td></tr><tr><td>1TB</td><td>6만원</td><td>12만원</td><td>6만원</td></tr><tr><td>2TB</td><td>8만원</td><td>22만원</td><td>14만원</td></tr><tr><td>4TB</td><td>10만원</td><td>45만원</td><td>35만원</td></tr></tbody></table><p>1TB 기준 가격 차이가 6만원 수준으로 줄었습니다. <strong>속도가 중요하면 SSD, 대용량 장기 보관이면 HDD</strong>를 선택하세요.</p>"),
            ("외장 스토리지 선택 가이드", "<h3>외장 SSD를 선택해야 하는 경우</h3><ul><li>영상 편집 등 대용량 파일 고속 전송이 필요할 때</li><li>가방에 넣고 다니며 자주 이동할 때 (충격 위험)</li><li>맥북, 노트북과 함께 사용할 때 (USB-C 연결)</li></ul><h3>외장 HDD를 선택해야 하는 경우</h3><ul><li>대용량(4TB 이상) 파일을 저렴하게 보관할 때</li><li>집이나 사무실에 고정하여 사용할 때</li><li>사진·동영상 아카이브 목적으로 사용할 때</li></ul>"),
        ],
        "faq": [
            ("외장 SSD도 충격에 강한가요?", "내부에 플래터가 없는 SSD는 <strong>낙하·진동에 훨씬 강합니다</strong>. SanDisk Extreme Pro는 2m 낙하 테스트를 통과했습니다. 가방에 넣고 다니는 용도라면 SSD를 강력 추천합니다."),
            ("외장하드 수명을 늘리는 방법은?", "사용 후 <strong>안전하게 제거(드라이브 분리)를 반드시 실행</strong>하고, 충격과 습기를 피하세요. 중요 파일은 2곳 이상에 백업하는 것이 기본입니다."),
            ("Mac에서도 외장 하드를 쓸 수 있나요?", "대부분 exFAT 또는 NTFS 포맷으로 출고됩니다. Mac에서 읽기/쓰기 모두 사용하려면 <strong>exFAT으로 포맷</strong>하거나, NTFS 드라이버 소프트웨어를 설치하세요."),
        ],
        "ctas": [
            {"text": "외장 SSD 최저가 비교하기", "desc": "다나와에서 삼성, WD, SanDisk 외장 SSD 최저가를 비교하세요", "url": "https://www.danawa.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "쿠팡 외장하드 특가 로켓배송", "desc": "쿠팡에서 외장하드 오늘의 특가를 확인하세요", "url": "https://www.coupang.com/np/search?q=외장SSD", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "삼성 T9 공식몰에서 보기", "desc": "삼성전자 공식몰에서 T9 정품과 AS 혜택을 확인하세요", "url": "https://www.samsung.com/sec/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "키보드 추천 2026 기계식 무선 사무용 TOP 10",
        "cat": 5,
        "slug": "keyboard-recommendation-2026",
        "intro": "키보드는 하루에 수천 번 손가락이 닿는 도구입니다. <strong>기계식, 멤브레인, 저소음, 무선</strong> 등 종류가 너무 많아 선택이 어렵습니다. 2026년 기준 Logitech MX Keys, Leopold, Realforce, Keychron, Apple Magic Keyboard 등 TOP 10 제품을 용도별로 비교합니다.",
        "sections": [
            ("키보드 종류별 특징 비교", "<table><thead><tr><th>종류</th><th>타건감</th><th>소음</th><th>가격대</th><th>추천 용도</th></tr></thead><tbody><tr><td>기계식 (클릭)</td><td>탁월, 명확한 피드백</td><td>크다</td><td>5~30만원</td><td>게이밍, 코딩</td></tr><tr><td>기계식 (리니어)</td><td>부드럽고 빠름</td><td>보통</td><td>5~30만원</td><td>게이밍, 빠른 타이핑</td></tr><tr><td>기계식 (택타일)</td><td>범프 피드백, 조용</td><td>적음</td><td>5~30만원</td><td>사무, 코딩</td></tr><tr><td>정전용량 무접점</td><td>최고급 부드러움</td><td>매우 적음</td><td>20~50만원</td><td>프리미엄 사무</td></tr><tr><td>멤브레인</td><td>물렁물렁</td><td>적음</td><td>1~5만원</td><td>가성비 사무</td></tr><tr><td>저프로파일 기계식</td><td>얕고 빠름</td><td>보통</td><td>10~20만원</td><td>사무, 휴대</td></tr></tbody></table>"),
            ("기계식 키보드 축 종류 완벽 정리", "<h3>Cherry MX 계열</h3><ul><li><strong>MX Red (리니어)</strong>: 가볍고 부드럽, 게이밍 대표 축</li><li><strong>MX Brown (택타일)</strong>: 약한 범프, 사무+게이밍 겸용으로 가장 인기</li><li><strong>MX Blue (클릭)</strong>: 명확한 클릭감, 소음이 커 사무실에는 부적합</li><li><strong>MX Speed Silver</strong>: 게이밍 최속, 1.2mm 초단 작동점</li></ul><h3>국산 축</h3><ul><li><strong>Gateron Red/Yellow</strong>: Cherry 대비 부드럽고 저렴</li><li><strong>Boba U4</strong>: 무소음 택타일, 사무실 최적</li></ul>"),
            ("TOP 10 키보드 추천 2026", "<h3>사무용 무선</h3><p><strong>1. Logitech MX Keys (9만원)</strong>: 저프로파일, 백라이트, 최대 3기기 전환. 맥과 윈도우 모두 완벽 지원.</p><p><strong>2. Apple Magic Keyboard (17만원)</strong>: 맥 사용자 최적, Touch ID 내장(최신형). 미려한 디자인.</p><p><strong>3. Keychron K3 Pro (12만원)</strong>: 75% 배열 기계식 무선, 핫스왑. 맥/윈도우 모두 지원.</p><h3>기계식 유선 (코딩/타이핑)</h3><p><strong>4. Leopold FC750R (11만원)</strong>: 국내 최고 인기 텐키리스. 체리 MX 갈축 추천. 내구성 압도적.</p><p><strong>5. Realforce R3 TKL (28만원)</strong>: 정전용량 무접점. 타건감 최고, 개발자들에게 인기.</p><p><strong>6. Keychron Q3 Pro (17만원)</strong>: 풀 알루미늄 CNC 하우징, 핫스왑, QMK 지원.</p><h3>게이밍</h3><p><strong>7. Wooting 60HE (20만원)</strong>: 홀 이펙트 센서, 리얼포스 트리거 기능. FPS 최강.</p><p><strong>8. Razer BlackWidow V4 Pro (25만원)</strong>: 무선, 마그네틱 리스트레스트. 게이밍 올인원.</p><h3>가성비</h3><p><strong>9. Keychron K2 V2 (8만원)</strong>: 75% 무선 기계식. 가성비 입문 최강.</p><p><strong>10. Akko 3068B Plus (7만원)</strong>: 기계식 무선, 65% 배열. 저렴하고 예쁜 디자인.</p>"),
            ("무선 vs 유선 키보드 선택 가이드", "<table><thead><tr><th>구분</th><th>무선 키보드</th><th>유선 키보드</th></tr></thead><tbody><tr><td>지연</td><td>2.4GHz: 1ms 이하 (게이밍 가능)</td><td>거의 없음</td></tr><tr><td>편의성</td><td>케이블 정리 불필요</td><td>충전 불필요</td></tr><tr><td>배터리</td><td>주기적 충전 필요</td><td>해당 없음</td></tr><tr><td>가격</td><td>같은 스펙 대비 2~3만원 비쌈</td><td>저렴</td></tr><tr><td>추천</td><td>멀티기기, 깔끔한 데스크 원할 때</td><td>게이밍, 예산 절약</td></tr></tbody></table>"),
        ],
        "faq": [
            ("기계식 키보드 소음이 너무 커서 사무실에서 못 쓸 것 같아요", "사무실에는 <strong>저소음 축(Cherry MX Silent Red, Boba U4)</strong> 또는 <strong>정전용량 무접점(Realforce)</strong>을 추천합니다. 멤브레인보다 조용한 기계식 키보드도 많습니다."),
            ("키보드 수명은 얼마나 되나요?", "Cherry MX 축 기준 <strong>1억 회 키스트로크</strong>를 보장합니다. 하루 8시간 타이핑 기준 10~15년 이상 사용 가능합니다."),
            ("60%, 75%, 100% 배열 중 무엇을 선택해야 하나요?", "숫자 패드를 자주 사용하면 100%, 마우스와 키보드 거리를 줄이고 싶다면 TKL(80%) 또는 75%를 추천합니다. 携帯성이 중요하면 65% 또는 60%를 선택하세요."),
        ],
        "ctas": [
            {"text": "키보드 최저가 비교하기", "desc": "다나와에서 기계식·무선 키보드 전 모델 최저가를 비교하세요", "url": "https://www.danawa.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "쿠팡 키보드 특가 확인", "desc": "쿠팡 로켓배송 키보드 오늘의 특가를 놓치지 마세요", "url": "https://www.coupang.com/np/search?q=기계식키보드", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "Keychron 공식몰 바로가기", "desc": "Keychron 공식 사이트에서 최신 모델을 확인하세요", "url": "https://keychron.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "웹캠 추천 2026 화상회의 유튜브 화질 비교",
        "cat": 5,
        "slug": "webcam-recommendation-2026",
        "intro": "재택근무와 유튜브 크리에이터 시대에 <strong>웹캠 화질</strong>은 첫인상을 결정합니다. Logitech C920부터 4K Brio, Razer Kiyo Pro까지 2026년 화상회의용·유튜브 촬영용 웹캠을 화질, 자동초점, 조명 성능 기준으로 비교합니다.",
        "sections": [
            ("웹캠 전체 스펙 비교표", "<table><thead><tr><th>모델</th><th>가격</th><th>해상도</th><th>프레임</th><th>자동초점</th><th>마이크</th><th>특징</th></tr></thead><tbody><tr><td>Logitech C920x HD Pro</td><td>10만원</td><td>1080p</td><td>30fps</td><td>자동</td><td>스테레오</td><td>가성비 베스트셀러</td></tr><tr><td>Logitech Brio 4K</td><td>25만원</td><td>4K (30fps)</td><td>60fps(1080p)</td><td>자동</td><td>스테레오</td><td>4K 최고 화질</td></tr><tr><td>Logitech StreamCam</td><td>15만원</td><td>1080p</td><td>60fps</td><td>AI 자동추적</td><td>스테레오</td><td>스트리밍 최적화</td></tr><tr><td>Razer Kiyo Pro</td><td>20만원</td><td>1080p</td><td>60fps</td><td>자동</td><td>단일지향</td><td>어두운 환경 강점</td></tr><tr><td>Elgato Facecam Pro</td><td>30만원</td><td>4K (60fps)</td><td>60fps</td><td>고정</td><td>없음(외장 권장)</td><td>방송·유튜버용</td></tr><tr><td>Anker PowerConf C300</td><td>7만원</td><td>1080p</td><td>60fps</td><td>AI 자동</td><td>노이즈캔슬링</td><td>가성비 화상회의</td></tr></tbody></table>"),
            ("화상회의용 웹캠 추천", "<h3>예산 10만원 이하: Anker PowerConf C300</h3><p>AI 노이즈캔슬링 마이크가 내장되어 있어 헤드셋 없이도 깨끗한 음성 전달이 됩니다. 1080p 60fps, AI 자동 프레이밍 기능으로 혼자 회의실에서 사용할 때도 카메라가 자동으로 얼굴을 추적합니다.</p><h3>예산 10~15만원: Logitech C920x</h3><p>화상회의 웹캠의 표준입니다. Zoom, Teams, Google Meet 최적화되어 있으며, 자동 조명 보정 기능으로 역광 환경에서도 얼굴이 밝게 보입니다.</p><h3>예산 20만원 이상: Logitech Brio 4K</h3><p>4K 해상도에 HDR 지원으로 밝기 차이가 심한 환경(창가 역광 등)에서도 화면이 자연스럽습니다. Windows Hello 안면 인식 지원.</p>"),
            ("유튜브·스트리밍용 웹캠 추천", "<h3>입문: Logitech StreamCam (15만원)</h3><p>세로(9:16) 촬영 지원으로 숏츠·릴스 제작에 편리합니다. AI 자동 얼굴 추적 기능, USB-C 연결.</p><h3>중급: Razer Kiyo Pro (20만원)</h3><p>1/2.8인치 대형 센서로 어두운 방에서도 노이즈 없이 촬영됩니다. HDR 지원, 언마운트 가능한 링라이트.</p><h3>전문: Elgato Facecam Pro (30만원)</h3><p>4K 60fps로 유튜브·트위치 스트리밍에 최고의 화질을 제공합니다. 내장 마이크가 없어 외장 마이크와 함께 사용해야 합니다.</p>"),
            ("웹캠 화질을 높이는 팁", "<ol><li><strong>조명이 핵심</strong>: 어떤 비싼 웹캠도 조명이 없으면 어둡고 노이즈가 많습니다. 링라이트(2~5만원) 하나로 화질이 비약적으로 향상됩니다.</li><li><strong>배경 처리</strong>: 가상 배경 대신 실제 깔끔한 배경이 더 전문적입니다.</li><li><strong>웹캠 위치</strong>: 눈높이보다 약간 위(5~10cm)에 설치하면 더 자연스럽습니다.</li><li><strong>해상도 설정</strong>: 인터넷이 느리면 1080p보다 720p 60fps가 더 부드럽게 보입니다.</li></ol>"),
        ],
        "faq": [
            ("웹캠과 DSLR 카메라 연결 중 무엇이 더 좋나요?", "화질만 보면 <strong>DSLR+캡처카드</strong>가 압도적이지만, 비용이 50만원 이상 추가됩니다. 일반 유튜브나 화상회의라면 <strong>Elgato Facecam Pro</strong>로도 충분합니다."),
            ("웹캠 마이크로 녹음해도 괜찮나요?", "C920, Brio 등 스테레오 마이크 내장 제품은 화상회의에 충분합니다. 하지만 유튜브·팟캐스트 녹음이라면 <strong>외장 USB 마이크(Blue Yeti, Rode NT-USB)</strong>를 따로 사용하는 것을 강력 추천합니다."),
            ("노트북 내장 카메라 대신 웹캠을 써야 하는 이유는?", "노트북 내장 카메라는 대부분 720p 또는 저화질 1080p입니다. 외장 웹캠은 <strong>화질, 자동초점, 화각 조절</strong> 모든 면에서 우수하며 중요한 비즈니스 미팅에서 좋은 인상을 남길 수 있습니다."),
        ],
        "ctas": [
            {"text": "웹캠 최저가 비교하기", "desc": "다나와에서 화상회의·스트리밍 웹캠 최저가를 비교하세요", "url": "https://www.danawa.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "Logitech 공식몰 웹캠 보기", "desc": "로지텍 공식몰에서 웹캠 전 라인업을 확인하세요", "url": "https://www.logitech.com/ko-kr/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "쿠팡 웹캠 특가 로켓배송", "desc": "오늘 주문하면 내일 도착하는 웹캠 특가를 확인하세요", "url": "https://www.coupang.com/np/search?q=웹캠", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "공유기 추천 2026 와이파이6E 가성비 속도 비교",
        "cat": 5,
        "slug": "wifi-router-recommendation-2026",
        "intro": "인터넷 속도가 느리다면 공유기가 문제일 수 있습니다. 2026년에는 <strong>WiFi 6E와 WiFi 7</strong>이 대중화되면서 기가비트 인터넷을 제대로 활용할 수 있는 공유기 선택이 중요해졌습니다. ipTIME, ASUS, TP-Link, Netgear 주요 제품을 속도·커버리지·가격 기준으로 비교합니다.",
        "sections": [
            ("WiFi 4/5/6/6E/7 세대별 차이점", "<table><thead><tr><th>세대</th><th>표준</th><th>최대 속도</th><th>주파수</th><th>특징</th></tr></thead><tbody><tr><td>WiFi 4</td><td>802.11n</td><td>300Mbps</td><td>2.4/5GHz</td><td>2009년, 구형</td></tr><tr><td>WiFi 5</td><td>802.11ac</td><td>3.5Gbps</td><td>5GHz</td><td>2013년, 현재 주류</td></tr><tr><td>WiFi 6</td><td>802.11ax</td><td>9.6Gbps</td><td>2.4/5GHz</td><td>2019년, 다중기기 최적</td></tr><tr><td>WiFi 6E</td><td>802.11ax</td><td>9.6Gbps</td><td>2.4/5/6GHz</td><td>6GHz 추가, 간섭 최소</td></tr><tr><td>WiFi 7</td><td>802.11be</td><td>46Gbps</td><td>2.4/5/6GHz</td><td>2024년, 최신</td></tr></tbody></table>"),
            ("공유기 추천 TOP 5 (2026)", "<h3>1. ipTIME AX8004M BCM (8만원)</h3><p>국내 판매 1위 공유기 브랜드. WiFi 6, 4×4 MU-MIMO, 2.4+5GHz 동시 지원.</p><ul><li>속도: 2.4GHz 800Mbps + 5GHz 4800Mbps</li><li>커버리지: 85㎡ (약 25평)</li><li>포트: 기가비트 × 4</li><li>추천: 20~30평대 아파트</li></ul><h3>2. ASUS RT-AX86U Pro (30만원)</h3><p>게이밍 최적화 공유기. Mobile Game Mode, AURA RGB 탑재.</p><ul><li>속도: WiFi 6, 총 5700Mbps</li><li>AI 네트워크 보호, Adaptive QoS</li><li>추천: 게이머, 고성능 필요</li></ul><h3>3. TP-Link Archer AX73 (12만원)</h3><p>가성비 WiFi 6 공유기. 6개 안테나로 넓은 커버리지.</p><ul><li>속도: WiFi 6, 총 5400Mbps</li><li>커버리지: 230㎡ (약 70평)</li><li>추천: 넓은 평수, 가성비</li></ul><h3>4. ASUS ZenWiFi Pro ET12 (60만원)</h3><p>WiFi 6E 메시 시스템 2팩. 3개 밴드(6GHz 포함)로 간섭 없음.</p><ul><li>속도: 최대 11Gbps</li><li>커버리지: 팩당 280㎡</li><li>추천: 복층 또는 넓은 주거 공간</li></ul><h3>5. ipTIME A3008NS (4만원)</h3><p>초가성비 WiFi 5 공유기. 2인 가구, 좁은 공간용.</p><ul><li>속도: WiFi 5, 총 1900Mbps</li><li>추천: 원룸, 1~2인 가구</li></ul>"),
            ("평수별 공유기 추천 가이드", "<table><thead><tr><th>평수</th><th>추천 공유기</th><th>예상 가격</th></tr></thead><tbody><tr><td>20평 이하 (원룸/오피스텔)</td><td>ipTIME A3008NS</td><td>4만원</td></tr><tr><td>20~30평 (아파트 표준)</td><td>ipTIME AX8004M</td><td>8만원</td></tr><tr><td>30~50평</td><td>TP-Link Archer AX73</td><td>12만원</td></tr><tr><td>50평 이상 / 복층</td><td>메시 시스템 (TP-Link Deco XE75)</td><td>30~60만원</td></tr><tr><td>게이밍/고성능</td><td>ASUS RT-AX86U Pro</td><td>30만원</td></tr></tbody></table>"),
            ("메시 와이파이 vs 일반 공유기 비교", "<p>넓은 공간이나 와이파이 음영 구역이 있다면 <strong>메시(Mesh) 시스템</strong>을 고려하세요.</p><ul><li><strong>일반 공유기</strong>: 저렴하지만 거리가 멀어질수록 속도 저하, 음영 구역 발생</li><li><strong>메시 시스템</strong>: 여러 노드가 seamless하게 연결, 집 전체 균일한 속도</li></ul><p><strong>추천 메시 제품</strong>: TP-Link Deco XE75 (2팩 35만원), ASUS ZenWiFi AX (2팩 40만원)</p>"),
        ],
        "faq": [
            ("공유기를 바꾸면 인터넷 속도가 빨라지나요?", "인터넷 계약 속도(예: 1Gbps)를 실제로 활용하지 못하고 있다면 공유기 업그레이드로 <strong>체감 속도가 빨라질 수 있습니다</strong>. 특히 구형 WiFi 5 이하 공유기를 WiFi 6으로 교체하면 다중 기기 환경에서 효과적입니다."),
            ("공유기 비밀번호를 왜 주기적으로 바꿔야 하나요?", "무단 접속자가 생기면 대역폭을 나눠쓰게 됩니다. <strong>WPA3 또는 WPA2 암호화</strong>로 설정하고, 초기 비밀번호는 반드시 변경하세요."),
            ("공유기를 껐다 켜면 왜 속도가 빨라지나요?", "공유기도 컴퓨터처럼 장시간 사용하면 메모리가 쌓입니다. <strong>월 1~2회 재시작</strong>하거나, 공유기 설정에서 자동 재시작 스케줄을 설정하세요."),
        ],
        "ctas": [
            {"text": "공유기 최저가 비교하기", "desc": "다나와에서 WiFi 6·6E 공유기 최저가를 비교하세요", "url": "https://www.danawa.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "ipTIME 공식몰 바로가기", "desc": "ipTIME 공식 쇼핑몰에서 신제품을 확인하세요", "url": "https://www.iptime.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "ASUS 공유기 공식몰 보기", "desc": "ASUS RT·ZenWiFi 공식 제품을 확인하세요", "url": "https://www.asus.com/kr/networking-iot-servers/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "전자책 리더기 추천 크레마 vs 리디페이퍼 vs 킨들 비교",
        "cat": 5,
        "slug": "ebook-reader-comparison-2026",
        "intro": "종이책 대신 전자책으로 독서하는 분들이 늘면서 <strong>전자책 리더기</strong> 시장도 커지고 있습니다. 국내 서비스인 크레마, 리디페이퍼부터 글로벌 표준 킨들, Kobo까지 E-Ink 디스플레이, 서점 생태계, 가격을 기준으로 2026년 최신 비교를 정리합니다.",
        "sections": [
            ("전자책 리더기 전체 비교표", "<table><thead><tr><th>모델</th><th>가격</th><th>화면</th><th>해상도</th><th>백라이트</th><th>방수</th><th>스토리지</th></tr></thead><tbody><tr><td>크레마 모티프</td><td>18만원</td><td>6인치 E-Ink</td><td>300ppi</td><td>색온도 조절</td><td>IPX8</td><td>32GB</td></tr><tr><td>리디페이퍼 프로</td><td>22만원</td><td>7.8인치 E-Ink</td><td>300ppi</td><td>색온도 조절</td><td>IPX8</td><td>32GB</td></tr><tr><td>Kindle Paperwhite 5</td><td>18만원</td><td>6.8인치 E-Ink</td><td>300ppi</td><td>색온도 조절</td><td>IPX8</td><td>8/16GB</td></tr><tr><td>Kindle Scribe</td><td>45만원</td><td>10.2인치 E-Ink</td><td>300ppi</td><td>가변 색온도</td><td>없음</td><td>16/32/64GB</td></tr><tr><td>Kobo Libra 2</td><td>25만원</td><td>7인치 E-Ink</td><td>300ppi</td><td>색온도 조절</td><td>IPX8</td><td>32GB</td></tr></tbody></table>"),
            ("서점 생태계 비교 (가장 중요!)", "<h3>크레마 (교보·YES24·알라딘·반디앤루니스)</h3><p>국내 4대 서점이 공동 운영합니다. 교보문고, YES24, 알라딘에서 구매한 책을 모두 하나의 기기에서 볼 수 있습니다. <strong>국내 콘텐츠 선택이 가장 넓습니다.</strong></p><h3>리디페이퍼 (리디북스)</h3><p>리디북스 전용 기기입니다. 리디북스 콘텐츠(만화, 웹소설 포함)에 최적화되어 있습니다. <strong>만화·웹소설 독자에게 최적</strong>. 리디 셀렉트 구독 서비스와 연동.</p><h3>킨들 (아마존)</h3><p>아마존 킨들 스토어를 사용합니다. 국내 한국어 책 구매가 불편하지만, 영어 원서·해외 도서는 압도적입니다. <strong>영어 독서가 목적이면 킨들</strong>.</p><h3>Kobo (락우텐)</h3><p>ePub 형식의 외부 파일 직접 넣기가 가능합니다. DRM 없는 전자책을 자유롭게 사용할 수 있습니다.</p>"),
            ("E-Ink 디스플레이 비교", "<p>E-Ink(전자잉크) 디스플레이는 스마트폰·태블릿과 달리 눈에 피로가 훨씬 적습니다.</p><ul><li><strong>300ppi</strong>: 현재 모든 주요 리더기의 표준. 종이책과 비슷한 선명도.</li><li><strong>색온도 조절</strong>: 밤에 읽을 때 따뜻한 노란색으로 전환, 눈 보호.</li><li><strong>IPX8 방수</strong>: 목욕·욕조에서도 독서 가능.</li><li><strong>배터리</strong>: 한 번 충전으로 수주~수개월 사용 가능 (약 6~8주, 하루 30분 기준).</li></ul>"),
            ("전자책 리더기 vs 스마트폰/태블릿", "<table><thead><tr><th>구분</th><th>전자책 리더기</th><th>스마트폰/태블릿</th></tr></thead><tbody><tr><td>눈 피로</td><td>매우 낮음</td><td>높음</td></tr><tr><td>햇빛 아래 가독성</td><td>우수</td><td>나쁨</td></tr><tr><td>배터리</td><td>수주</td><td>수시간</td></tr><tr><td>무게</td><td>180~200g</td><td>170~500g</td></tr><tr><td>가격</td><td>15~45만원</td><td>이미 보유</td></tr><tr><td>집중력</td><td>독서에만 집중</td><td>알림·SNS 방해</td></tr></tbody></table>"),
        ],
        "faq": [
            ("크레마와 킨들 중 어떤 것을 선택해야 하나요?", "한국어 도서를 주로 읽는다면 <strong>크레마</strong>, 영어 원서나 아마존 도서를 주로 읽는다면 <strong>킨들</strong>을 선택하세요."),
            ("전자책 리더기로 PDF를 볼 수 있나요?", "대부분의 리더기에서 PDF를 볼 수 있지만, PDF 최적화는 좋지 않습니다. <strong>7인치 이상 리더기</strong>나 Kindle Scribe(10.2인치)를 추천합니다."),
            ("전자책 리더기에서 밑줄·메모가 가능한가요?", "모든 주요 리더기에서 손가락으로 밑줄 및 메모 기능이 지원됩니다. 필기를 원하면 스타일러스가 포함된 <strong>Kindle Scribe</strong>나 리디페이퍼 프로를 선택하세요."),
        ],
        "ctas": [
            {"text": "크레마 공식몰 바로가기", "desc": "크레마 최신 모델과 프로모션을 확인하세요", "url": "https://crema.co.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "리디페이퍼 공식몰 바로가기", "desc": "리디페이퍼 프로 최신 모델 및 리디셀렉트를 확인하세요", "url": "https://ridibooks.com/devices", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "킨들 아마존에서 구매하기", "desc": "아마존에서 최신 킨들 페이퍼화이트를 확인하세요", "url": "https://www.amazon.com/kindle", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "NAS 추천 2026 개인용 가정용 입문 가이드",
        "cat": 5,
        "slug": "nas-recommendation-2026",
        "intro": "NAS(네트워크 연결 스토리지)는 집에서 운영하는 <strong>개인 클라우드 서버</strong>입니다. 구글 드라이브, 네이버 마이박스 같은 서비스를 월 구독료 없이 직접 구축할 수 있습니다. 2026년 Synology, QNAP, Asustor, ipTIME NAS 입문 모델을 비교하고, 처음 NAS를 구축하는 분을 위한 완전한 가이드를 제공합니다.",
        "sections": [
            ("NAS란 무엇인가? 장단점 정리", "<h3>NAS의 주요 활용법</h3><ul><li><strong>개인 클라우드</strong>: 구글 드라이브 대체, 월정액 없음</li><li><strong>미디어 서버</strong>: 집 어디서나 영화·음악 스트리밍 (Plex, Jellyfin)</li><li><strong>자동 백업</strong>: PC, 스마트폰 사진 자동 백업</li><li><strong>원격 접속</strong>: 출장 중에도 집 파일 접근</li><li><strong>Docker 서버</strong>: 각종 자동화 서비스 운영</li></ul><h3>단점</h3><ul><li>초기 구입 비용 (NAS 본체 + HDD)</li><li>설정 학습 곡선 필요</li><li>24시간 전기 소모 (HDD 1개당 월 500~2,000원)</li></ul>"),
            ("NAS 추천 비교표 2026", "<table><thead><tr><th>모델</th><th>가격(본체)</th><th>베이 수</th><th>CPU</th><th>RAM</th><th>특징</th></tr></thead><tbody><tr><td>Synology DS224+</td><td>39만원</td><td>2베이</td><td>Intel Celeron J4125</td><td>2GB (최대 6GB)</td><td>입문 최적, DSM OS 최고</td></tr><tr><td>QNAP TS-233</td><td>25만원</td><td>2베이</td><td>Cortex-A55 쿼드코어</td><td>2GB</td><td>가성비, QNAP QTS</td></tr><tr><td>Asustor Drivestor 2 Pro</td><td>20만원</td><td>2베이</td><td>Realtek RTD1296</td><td>2GB</td><td>초저가 입문</td></tr><tr><td>Synology DS923+</td><td>65만원</td><td>4베이</td><td>AMD Ryzen R1600</td><td>4GB (최대 32GB)</td><td>중급 가정용·소기업</td></tr><tr><td>ipTIME NAS2dual</td><td>15만원</td><td>2베이</td><td>ARM 듀얼코어</td><td>512MB</td><td>국내 AS 편리, 초입문</td></tr></tbody></table>"),
            ("NAS HDD 구성 가이드", "<h3>HDD 선택: NAS 전용 HDD vs 일반 HDD</h3><p>NAS에는 반드시 <strong>NAS 전용 HDD</strong>를 사용해야 합니다.</p><ul><li><strong>WD Red Plus</strong>: NAS 전용, RAID 지원, 가성비 (4TB 12만원)</li><li><strong>Seagate IronWolf</strong>: NAS 전용, 24/7 운영, AgileArray 기술 (4TB 11만원)</li><li><strong>WD Purple</strong>: CCTV·감시 카메라 특화</li></ul><h3>용량 구성 추천</h3><ul><li><strong>2베이 RAID 1</strong>: 4TB × 2 = 실용량 4TB (미러링, 1개 고장 시 데이터 보호)</li><li><strong>2베이 JBOD</strong>: 4TB + 4TB = 8TB (별도 관리)</li><li><strong>4베이 RAID 5</strong>: 4TB × 4 = 실용량 12TB (1개 고장 시 복구 가능)</li></ul>"),
            ("NAS 전기료 실제 계산", "<table><thead><tr><th>구성</th><th>소비전력</th><th>월 전기료(24시간)</th><th>연간 전기료</th></tr></thead><tbody><tr><td>NAS 본체 (HDD 대기)</td><td>5~10W</td><td>500원</td><td>6,000원</td></tr><tr><td>NAS + HDD 1개 (작동)</td><td>20~25W</td><td>2,000원</td><td>24,000원</td></tr><tr><td>NAS + HDD 2개 (작동)</td><td>30~35W</td><td>3,000원</td><td>36,000원</td></tr></tbody></table><p>구글 드라이브 2TB 요금제(월 3,900원)와 비교하면, <strong>NAS는 1~2년 후 비용 회수</strong>가 됩니다.</p>"),
        ],
        "faq": [
            ("NAS 입문자에게 어떤 모델을 추천하나요?", "<strong>Synology DS224+</strong>를 가장 추천합니다. DSM(DiskStation Manager) OS가 직관적이고, 커뮤니티와 한국어 자료가 풍부합니다. 가격 절약이 우선이라면 QNAP TS-233이나 Asustor를 고려하세요."),
            ("NAS를 24시간 켜두어야 하나요?", "원격 접속과 자동 백업을 위해서는 <strong>24시간 운영이 기본</strong>입니다. 다만 Synology의 절전 스케줄 기능으로 새벽에 HDD를 슬립 모드로 설정하면 전기료를 절약할 수 있습니다."),
            ("NAS 없이 외장하드만으로도 백업이 충분한가요?", "외장하드 단일 백업은 <strong>하드 고장 시 데이터 전체 손실 위험</strong>이 있습니다. NAS RAID 구성이나 최소 2개 외장하드 교차 백업을 권장합니다."),
        ],
        "ctas": [
            {"text": "Synology NAS 공식몰 바로가기", "desc": "시놀로지 공식몰에서 DS224+ 최신 모델을 확인하세요", "url": "https://www.synology.com/ko-kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "다나와 NAS 최저가 비교", "desc": "다나와에서 NAS 전 모델 최저가와 리뷰를 확인하세요", "url": "https://www.danawa.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "쿠팡 NAS+HDD 패키지 구매", "desc": "쿠팡에서 NAS 본체와 HDD를 함께 구매하세요", "url": "https://www.coupang.com/np/search?q=NAS", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "보조배터리 추천 2026 용량별 고속충전 비교 TOP 7",
        "cat": 5,
        "slug": "power-bank-recommendation-2026",
        "intro": "스마트폰 배터리가 부족할 때 꼭 필요한 <strong>보조배터리</strong>. 2026년에는 65W~100W 고속충전 보조배터리가 대중화되면서 노트북까지 충전할 수 있는 제품들이 늘었습니다. Anker, Baseus, 삼성, Xiaomi 주요 제품을 용량·충전속도·무게 기준으로 비교합니다.",
        "sections": [
            ("보조배터리 전체 비교표 2026", "<table><thead><tr><th>모델</th><th>용량</th><th>가격</th><th>최대 출력</th><th>무게</th><th>포트</th><th>특징</th></tr></thead><tbody><tr><td>Anker 622 Magnetic</td><td>5,000mAh</td><td>4만원</td><td>7.5W (MagSafe)</td><td>96g</td><td>USB-C × 1</td><td>아이폰 마그넷 부착</td></tr><tr><td>Anker 737 Power Bank</td><td>24,000mAh</td><td>9만원</td><td>140W</td><td>656g</td><td>USB-C × 2, USB-A × 1</td><td>노트북 충전 가능</td></tr><tr><td>Baseus Blade 2</td><td>20,000mAh</td><td>6만원</td><td>100W</td><td>398g</td><td>USB-C × 2, USB-A × 1</td><td>얇은 디자인, 노트북 OK</td></tr><tr><td>삼성 공식 보조배터리 25W</td><td>10,000mAh</td><td>4만원</td><td>25W</td><td>238g</td><td>USB-C × 1, USB-A × 1</td><td>삼성 생태계 최적</td></tr><tr><td>Xiaomi 33W 10000</td><td>10,000mAh</td><td>2만원</td><td>33W</td><td>230g</td><td>USB-C × 1, USB-A × 1</td><td>초가성비</td></tr><tr><td>Anker Prime 27650mAh</td><td>27,650mAh</td><td>14만원</td><td>250W</td><td>760g</td><td>USB-C × 2, USB-A × 1</td><td>최고 성능, 노트북 2개</td></tr><tr><td>INIU 30W 10000mAh</td><td>10,000mAh</td><td>2.5만원</td><td>30W</td><td>210g</td><td>USB-C × 1, USB-A × 2</td><td>가성비 고속충전</td></tr></tbody></table>"),
            ("용량별 보조배터리 선택 가이드", "<h3>5,000~10,000mAh (경량·일상용)</h3><p>스마트폰 1~2회 충전. 무게 100~250g으로 가볍습니다.</p><ul><li>아이폰 15 Pro(3,274mAh) 약 2.5회 충전</li><li>갤럭시 S25(4,000mAh) 약 2회 충전</li><li><strong>추천</strong>: Xiaomi 33W 10000 (2만원), INIU 30W (2.5만원)</li></ul><h3>20,000mAh (여행·장거리용)</h3><p>스마트폰 4~5회 충전. 아이패드, 갤럭시 탭도 1~2회 충전 가능.</p><ul><li><strong>추천</strong>: Baseus Blade 2 (6만원, 100W, 얇은 디자인)</li></ul><h3>25,000mAh 이상 (노트북·고성능)</h3><p>맥북 에어(52.6Wh), 갤럭시북 충전 가능. 무거운 것이 단점(600g+).</p><ul><li><strong>추천</strong>: Anker 737 (9만원, 140W), Anker Prime (14만원, 250W)</li></ul>"),
            ("고속충전 규격 비교", "<table><thead><tr><th>충전 규격</th><th>최대 출력</th><th>지원 기기</th></tr></thead><tbody><tr><td>PD (USB Power Delivery)</td><td>최대 240W</td><td>아이폰, 맥북, 갤럭시북 등 범용</td></tr><tr><td>Super VOOC</td><td>최대 240W</td><td>OPPO, OnePlus 전용</td></tr><tr><td>Warp Charge</td><td>최대 65W</td><td>OnePlus 전용</td></tr><tr><td>AFC / SFC</td><td>최대 25W</td><td>삼성 갤럭시 전용</td></tr><tr><td>QC (Qualcomm Quick Charge)</td><td>최대 100W</td><td>안드로이드 범용</td></tr></tbody></table><p><strong>PD(USB Power Delivery)</strong>를 지원하는 보조배터리가 가장 범용적입니다.</p>"),
            ("항공기 반입 기준 (중요!)", "<p>비행기에 보조배터리를 가지고 탈 때 반드시 알아야 할 규정:</p><ul><li><strong>기내 반입</strong>: 가능 (수하물 위탁 불가, 반드시 기내 휴대)</li><li><strong>160Wh 이하</strong>: 기내 반입 가능 (개당, 승인 없이)</li><li><strong>160Wh 초과</strong>: 항공사 사전 승인 필요</li></ul><p>Wh(와트시) 계산: mAh × V ÷ 1,000<br>예: 20,000mAh × 3.7V ÷ 1,000 = <strong>74Wh → 반입 가능</strong></p><ul><li>20,000mAh (3.7V): 약 74Wh ✓</li><li>30,000mAh (3.7V): 약 111Wh ✓</li><li>40,000mAh (3.7V): 약 148Wh ✓ (160Wh 이하)</li></ul>"),
        ],
        "faq": [
            ("보조배터리 용량 표시가 실제와 다른 이유는?", "배터리 셀은 3.7V 기준이지만 USB 출력은 5V로 변환됩니다. 이 과정에서 에너지 손실이 발생해 <strong>실제 사용 가능한 용량은 표시의 60~70%</strong> 수준입니다."),
            ("보조배터리 수명을 늘리는 방법은?", "완전 방전 상태를 자주 만들지 마세요. <strong>20~80% 구간에서 사용</strong>하는 것이 배터리 수명에 유리합니다. 고온 환경(차 안 등)은 피하세요."),
            ("스마트폰 무선 충전을 지원하는 보조배터리는?", "Anker 622 Magnetic(마그세이프), 삼성 공식 무선 보조배터리 등이 있습니다. 무선 충전은 유선 대비 발열이 높고 효율이 낮습니다."),
        ],
        "ctas": [
            {"text": "Anker 보조배터리 공식몰", "desc": "Anker 코리아 공식몰에서 최신 보조배터리를 확인하세요", "url": "https://www.anker.com/ko", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "쿠팡 보조배터리 특가 확인", "desc": "로켓배송 보조배터리 오늘의 특가를 놓치지 마세요", "url": "https://www.coupang.com/np/search?q=보조배터리", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "다나와 보조배터리 최저가 비교", "desc": "용량·충전속도별 보조배터리 최저가를 비교하세요", "url": "https://www.danawa.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
]

POSTS += [
    # ===== 소프트웨어/앱 (11-20) =====
    {
        "title": "무료 동영상 편집 프로그램 추천 TOP 7 초보자용",
        "cat": 5,
        "slug": "free-video-editor-recommendation-2026",
        "intro": "유튜브, 릴스, 틱톡 시대에 <strong>동영상 편집 능력</strong>은 누구에게나 필요한 스킬이 됐습니다. 비싼 어도비 프리미어 없이도 전문적인 영상을 만들 수 있는 무료 편집 프로그램 7가지를 초보자 관점에서 비교합니다. PC용부터 모바일 앱까지 용도에 맞는 최적의 프로그램을 찾아드립니다.",
        "sections": [
            ("무료 동영상 편집 프로그램 전체 비교표", "<table><thead><tr><th>프로그램</th><th>가격</th><th>플랫폼</th><th>난이도</th><th>4K 지원</th><th>워터마크</th></tr></thead><tbody><tr><td>DaVinci Resolve 19</td><td>무료 (Pro 35만원)</td><td>Windows/Mac/Linux</td><td>중~고급</td><td>O</td><td>없음</td></tr><tr><td>CapCut</td><td>무료 (Pro 월 6,900원)</td><td>PC/모바일</td><td>초급</td><td>O (Pro)</td><td>있음 (제거가능)</td></tr><tr><td>Shotcut</td><td>완전 무료</td><td>Windows/Mac/Linux</td><td>중급</td><td>O</td><td>없음</td></tr><tr><td>OpenShot</td><td>완전 무료</td><td>Windows/Mac/Linux</td><td>초~중급</td><td>O</td><td>없음</td></tr><tr><td>Clipchamp</td><td>무료 (윈도우 기본)</td><td>Windows/웹</td><td>초급</td><td>X (무료)</td><td>없음</td></tr><tr><td>VLLO</td><td>무료 (Pro 연 3.3만원)</td><td>iOS/Android</td><td>초급</td><td>O</td><td>있음 (제거가능)</td></tr><tr><td>KineMaster</td><td>무료 (Pro 월 5,500원)</td><td>iOS/Android</td><td>초~중급</td><td>O (Pro)</td><td>있음 (Pro 제거)</td></tr></tbody></table>"),
            ("DaVinci Resolve - 전문가급 무료 편집툴", "<p>할리우드 영화와 넷플릭스 드라마에도 쓰이는 <strong>업계 표준 편집 소프트웨어</strong>입니다. 무료 버전도 색보정(Color Grading), 오디오 믹싱(Fairlight), 시각효과(Fusion)를 모두 포함합니다.</p><ul><li><strong>장점</strong>: 전문가급 색보정, 무제한 타임라인, 워터마크 없음</li><li><strong>단점</strong>: 초보자 진입장벽 높음, 고사양 PC 필요 (RAM 16GB+)</li><li><strong>추천 대상</strong>: 진지하게 배우고 싶은 분, 유튜브 제작자</li><li><strong>시스템 요구사항</strong>: GPU VRAM 2GB+, RAM 16GB 권장</li></ul>"),
            ("CapCut - 틱톡·릴스 특화 무료 앱", "<p>바이트댄스(틱톡 모회사)가 만든 편집 앱입니다. <strong>SNS 영상 제작에 특화</strong>된 템플릿, 자동 자막, AI 기능이 풍부합니다.</p><ul><li><strong>장점</strong>: 쉬운 인터페이스, AI 자동 자막(한국어 지원), 트렌드 템플릿 풍부</li><li><strong>단점</strong>: 무료 버전 워터마크, 일부 기능 유료</li><li><strong>추천 대상</strong>: SNS 숏폼, 릴스, 틱톡 제작자</li></ul>"),
            ("초보자 추천 순위 및 선택 가이드", "<h3>PC 편집 입문자</h3><ol><li><strong>Clipchamp</strong>: 윈도우 11 기본 내장, 바로 시작 가능</li><li><strong>OpenShot</strong>: 간단하고 무료, 기본 편집에 충분</li><li><strong>DaVinci Resolve</strong>: 배울 의지가 있다면 최고의 무료 옵션</li></ol><h3>모바일 편집 입문자</h3><ol><li><strong>CapCut</strong>: AI 기능 풍부, 틱톡·릴스 제작 최적</li><li><strong>VLLO</strong>: 한국 개발 앱, 직관적 UI</li><li><strong>KineMaster</strong>: 다층 타임라인, 중급 기능 필요 시</li></ol>"),
        ],
        "faq": [
            ("워터마크 없는 완전 무료 편집 프로그램은?", "<strong>DaVinci Resolve, Shotcut, OpenShot</strong>은 워터마크 없이 완전 무료로 사용할 수 있습니다. CapCut, KineMaster는 무료 버전에서 워터마크가 표시됩니다."),
            ("동영상 편집 PC 사양은 어느 정도가 필요한가요?", "기본 편집(1080p)은 <strong>RAM 8GB, 내장 그래픽</strong>으로도 가능합니다. 4K 편집이나 DaVinci Resolve 사용 시 RAM 16GB, 전용 GPU 권장."),
            ("유튜브 영상 편집을 처음 배우려면 어떤 프로그램이 좋나요?", "완전 초보라면 <strong>CapCut(모바일) 또는 Clipchamp(PC)</strong>로 시작하세요. 어느 정도 익숙해지면 DaVinci Resolve로 넘어가면 됩니다."),
        ],
        "ctas": [
            {"text": "DaVinci Resolve 무료 다운로드", "desc": "블랙매직 공식 사이트에서 DaVinci Resolve를 무료로 받으세요", "url": "https://www.blackmagicdesign.com/kr/products/davinciresolve", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "CapCut 무료로 시작하기", "desc": "CapCut PC·모바일 앱을 무료로 다운로드하세요", "url": "https://www.capcut.com/ko-kr/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "VLLO 모바일 앱 다운로드", "desc": "국내 개발 VLLO로 스마트폰 영상 편집을 시작하세요", "url": "https://www.vllo.io/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "PDF 편집 프로그램 추천 무료 유료 비교 2026",
        "cat": 5,
        "slug": "pdf-editor-recommendation-2026",
        "intro": "PDF 파일을 편집해야 하는데 어도비 Acrobat은 너무 비쌉니다. 2026년에는 <strong>무료 PDF 편집 도구</strong>들이 크게 발전하면서 대부분의 작업을 무료로 해결할 수 있습니다. Adobe Acrobat, Foxit, 알PDF, Smallpdf, PDF24 등을 기능·가격별로 비교합니다.",
        "sections": [
            ("PDF 편집 프로그램 전체 비교표", "<table><thead><tr><th>프로그램</th><th>가격</th><th>플랫폼</th><th>텍스트 편집</th><th>서명</th><th>OCR</th><th>병합/분할</th></tr></thead><tbody><tr><td>Adobe Acrobat Pro</td><td>월 2.7만원</td><td>Windows/Mac</td><td>O</td><td>O</td><td>O</td><td>O</td></tr><tr><td>Foxit PDF Editor</td><td>월 1.2만원 / 7만원 구매</td><td>Windows/Mac</td><td>O</td><td>O</td><td>O</td><td>O</td></tr><tr><td>알PDF</td><td>무료</td><td>Windows</td><td>제한적</td><td>O</td><td>X</td><td>O</td></tr><tr><td>PDF24 Creator</td><td>무료</td><td>Windows/웹</td><td>X</td><td>O</td><td>X</td><td>O</td></tr><tr><td>Smallpdf</td><td>무료(제한)/월 1.2만원</td><td>웹</td><td>O (유료)</td><td>O</td><td>O (유료)</td><td>O</td></tr><tr><td>iLovePDF</td><td>무료(제한)/월 5달러</td><td>웹/모바일</td><td>O (유료)</td><td>O</td><td>O (유료)</td><td>O</td></tr></tbody></table>"),
            ("무료 PDF 도구로 해결할 수 있는 작업", "<h3>PDF24 Creator (완전 무료, 설치형)</h3><p>광고 없이 완전 무료. PDF 병합, 분할, 압축, 변환, 페이지 회전을 모두 무료로 사용할 수 있습니다.</p><h3>알PDF (국내 무료, Windows)</h3><p>한글 지원이 완벽하고 전자서명, 도장 기능이 무료입니다. PDF 병합·분할, 페이지 삭제도 무료.</p><h3>iLovePDF (웹, 일부 무료)</h3><p>PDF 병합, 분할, 압축, Word 변환이 무료입니다. 파일 크기 제한이 있지만 가끔 사용하기에 충분합니다.</p>"),
            ("유료 PDF 편집 프로그램 비교", "<h3>Adobe Acrobat Pro (월 2.7만원)</h3><p>업계 표준. PDF 텍스트·이미지 직접 편집, 고급 OCR, 전자서명(Adobe Sign) 등 모든 기능 포함. 기업·전문가용.</p><h3>Foxit PDF Editor (월 1.2만원 또는 7만원 일시불)</h3><p>어도비보다 저렴하면서 대부분의 기능을 제공합니다. 일시불 구매가 가능하여 장기 사용 시 경제적.</p>"),
            ("용도별 추천 요약", "<ul><li><strong>PDF 간단 병합·분할만</strong>: PDF24 Creator (무료) 또는 iLovePDF (무료)</li><li><strong>전자서명이 필요할 때</strong>: 알PDF (무료) 또는 Smallpdf</li><li><strong>PDF 텍스트 편집이 필요할 때</strong>: Foxit PDF Editor (7만원) 또는 Adobe Acrobat</li><li><strong>기업·계약서 처리</strong>: Adobe Acrobat Pro (월 2.7만원)</li></ul>"),
        ],
        "faq": [
            ("PDF 파일의 텍스트를 직접 수정할 수 있나요?", "텍스트 직접 편집은 <strong>유료 소프트웨어(Adobe Acrobat, Foxit)</strong>가 필요합니다. 무료 도구들은 주석 추가, 서명, 병합 등은 가능하지만 텍스트 편집은 제한적입니다."),
            ("스캔된 PDF에서 텍스트를 추출하려면?", "<strong>OCR(광학 문자 인식)</strong> 기능이 필요합니다. Adobe Acrobat Pro, Foxit가 지원하며, 무료로는 Google Drive에 업로드 후 Google Docs로 열면 기본 OCR을 사용할 수 있습니다."),
            ("PDF 파일 용량을 줄이려면?", "PDF24, iLovePDF, Smallpdf에서 <strong>무료로 PDF 압축</strong>이 가능합니다. 이미지가 많은 PDF는 최대 80%까지 용량이 줄어듭니다."),
        ],
        "ctas": [
            {"text": "PDF24 무료 다운로드", "desc": "완전 무료 PDF 편집 도구 PDF24를 지금 다운로드하세요", "url": "https://www.pdf24.org/ko/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "알PDF 무료로 사용하기", "desc": "한글 지원 완벽한 국내 무료 PDF 뷰어/편집기", "url": "https://www.altools.co.kr/Download/ALPdf.aspx", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "Adobe Acrobat 무료 체험하기", "desc": "어도비 아크로뱃 Pro 7일 무료 체험을 시작하세요", "url": "https://acrobat.adobe.com/kr/ko/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "화면 녹화 프로그램 추천 무료 TOP 5 사용법",
        "cat": 5,
        "slug": "screen-recorder-recommendation-2026",
        "intro": "강의 녹화, 게임 방송, 튜토리얼 제작에 필요한 <strong>화면 녹화 프로그램</strong>. 고가의 유료 소프트웨어 없이도 OBS Studio, Bandicam, 곰캠, ShareX, Windows 기본 기능으로 충분히 고품질 녹화가 가능합니다. 2026년 기준 무료 화면 녹화 프로그램 5가지를 비교합니다.",
        "sections": [
            ("화면 녹화 프로그램 비교표", "<table><thead><tr><th>프로그램</th><th>가격</th><th>플랫폼</th><th>화질</th><th>라이브 스트리밍</th><th>용도</th></tr></thead><tbody><tr><td>OBS Studio</td><td>완전 무료</td><td>Win/Mac/Linux</td><td>최상 (무제한)</td><td>O</td><td>방송·전문 녹화</td></tr><tr><td>Bandicam</td><td>무료(제한)/4.5만원</td><td>Windows</td><td>상</td><td>X</td><td>게임·화면 녹화</td></tr><tr><td>곰캠</td><td>무료(광고)/유료</td><td>Windows</td><td>중상</td><td>X</td><td>강의·튜토리얼</td></tr><tr><td>ShareX</td><td>완전 무료</td><td>Windows</td><td>상</td><td>X</td><td>스크린샷·녹화 전문</td></tr><tr><td>Xbox Game Bar</td><td>무료(Windows 기본)</td><td>Windows 10/11</td><td>중상</td><td>X</td><td>게임 클립</td></tr></tbody></table>"),
            ("OBS Studio 완전 무료 방송·녹화 가이드", "<p>OBS Studio는 유튜브, 트위치 방송의 <strong>업계 표준 무료 소프트웨어</strong>입니다.</p><h3>기본 설정 가이드</h3><ol><li>공식 사이트(obsproject.com)에서 무료 다운로드</li><li>자동 설정 마법사 실행 (녹화 or 방송 선택)</li><li>해상도: 1920×1080, FPS: 60으로 설정</li><li>인코더: NVENC(NVIDIA 그래픽카드) 또는 x264(CPU)</li><li>녹화 형식: MKV (나중에 MP4 변환 가능)</li></ol><h3>권장 녹화 설정</h3><ul><li>비트레이트: 1080p 60fps 기준 25,000~40,000 kbps</li><li>오디오: 스테레오, 320 kbps</li></ul>"),
            ("용도별 최적 프로그램 선택", "<h3>게임 클립 저장 (간단)</h3><p><strong>Xbox Game Bar(Win+G)</strong>: 별도 설치 불필요. Win+Alt+R로 즉시 녹화 시작.</p><h3>강의·튜토리얼 제작</h3><p><strong>곰캠</strong>: 화면 영역 선택, 웹캠 삽입, 편집 기능까지 포함.</p><h3>게임 고화질 녹화</h3><p><strong>Bandicam</strong>: 게임 화면 전용 DirectX 캡처로 성능 저하 최소화. 무료 버전은 10분 제한.</p><h3>전문 방송·다중 소스</h3><p><strong>OBS Studio</strong>: 카메라+화면+오버레이 동시 구성, 유튜브·트위치 직방송.</p><h3>스크린샷+녹화 동시에</h3><p><strong>ShareX</strong>: 스크린샷 자동 업로드, GIF 제작, 다양한 캡처 모드 무료.</p>"),
        ],
        "faq": [
            ("화면 녹화 시 PC가 버벅거리면 어떻게 하나요?", "인코더를 CPU(x264) 대신 <strong>GPU(NVENC, AMD AMF)</strong>로 변경하세요. 그래픽카드가 인코딩을 담당하여 CPU 부하가 크게 줄어듭니다."),
            ("4K 화면 녹화가 가능한 무료 프로그램은?", "<strong>OBS Studio</strong>는 4K 60fps 녹화를 무료로 지원합니다. 단, 4K 녹화는 스토리지와 CPU/GPU 성능이 많이 필요합니다."),
            ("마이크 소리만 빠지고 녹화되는 문제 해결법은?", "OBS Studio에서 <strong>오디오 > 마이크/보조 오디오</strong>에 사용하는 마이크가 선택되어 있는지 확인하세요. 장치 관리자에서 마이크 드라이버를 재설치하는 것도 도움이 됩니다."),
        ],
        "ctas": [
            {"text": "OBS Studio 무료 다운로드", "desc": "OBS 공식 사이트에서 최신 버전을 무료로 다운로드하세요", "url": "https://obsproject.com/ko", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "Bandicam 무료 체험하기", "desc": "반디캠 공식 사이트에서 게임·화면 녹화를 시작하세요", "url": "https://www.bandicam.com/ko/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "ShareX 무료 다운로드", "desc": "ShareX로 스크린샷과 화면 녹화를 한 번에 해결하세요", "url": "https://getsharex.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "사진 편집 프로그램 추천 무료 포토샵 대체 앱",
        "cat": 5,
        "slug": "photo-editor-recommendation-2026",
        "intro": "월 3만원짜리 포토샵 구독이 부담스럽다면? 2026년에는 <strong>무료 사진 편집 프로그램</strong>이 포토샵의 대부분 기능을 대체할 수 있습니다. GIMP, Photopea, Canva, Pixlr, 포토스케이프X 등을 기능·용도별로 비교하고 최적의 도구를 추천합니다.",
        "sections": [
            ("무료 사진 편집 프로그램 비교표", "<table><thead><tr><th>프로그램</th><th>가격</th><th>플랫폼</th><th>레이어</th><th>RAW 지원</th><th>한국어</th><th>주요 용도</th></tr></thead><tbody><tr><td>GIMP</td><td>완전 무료</td><td>Win/Mac/Linux</td><td>O</td><td>플러그인</td><td>O</td><td>포토샵 대체</td></tr><tr><td>Photopea</td><td>무료(광고)/월 5달러</td><td>웹브라우저</td><td>O</td><td>O</td><td>부분</td><td>PSD 편집, 포토샵 UI</td></tr><tr><td>Canva</td><td>무료(제한)/월 1.5만원</td><td>웹/모바일</td><td>제한적</td><td>X</td><td>O</td><td>SNS 디자인, 썸네일</td></tr><tr><td>Pixlr E</td><td>무료(광고)/유료</td><td>웹브라우저</td><td>O</td><td>X</td><td>부분</td><td>간단 편집</td></tr><tr><td>포토스케이프X</td><td>무료 (Pro 3만원)</td><td>Win/Mac</td><td>X</td><td>X</td><td>O</td><td>일괄 처리, 콜라주</td></tr></tbody></table>"),
            ("GIMP - 완전 무료 포토샵 대체", "<p>오픈소스 무료 이미지 편집 소프트웨어의 최강자입니다. 포토샵의 <strong>레이어, 마스크, 필터, 브러시</strong> 기능을 모두 무료로 사용할 수 있습니다.</p><ul><li>포토샵 PSD 파일 열기 지원</li><li>플러그인으로 기능 확장 가능</li><li>단점: 포토샵과 다른 UI, 학습 필요</li></ul>"),
            ("Photopea - 브라우저에서 포토샵을 무료로", "<p>설치 없이 브라우저에서 사용하는 <strong>포토샵과 거의 동일한 UI</strong>의 무료 편집 툴입니다.</p><ul><li>PSD, XD, Sketch 파일 직접 편집</li><li>레이어, 스마트 오브젝트, 조정 레이어 지원</li><li>인터넷만 있으면 어디서나 사용 가능</li><li>단점: 광고가 있음 (유료 시 제거), 느릴 수 있음</li></ul>"),
            ("용도별 추천 요약", "<h3>포토샵을 완전히 대체하고 싶다면</h3><p><strong>GIMP</strong> (설치형, 완전 무료) 또는 <strong>Photopea</strong> (웹, 포토샵 UI)</p><h3>SNS 썸네일·카드 뉴스 제작</h3><p><strong>Canva</strong> (무료 플랜으로 대부분 가능)</p><h3>사진 간단 보정·일괄 처리</h3><p><strong>포토스케이프X</strong> (국내 개발, 한국어 완벽 지원)</p><h3>PSD 파일 빠른 편집</h3><p><strong>Photopea</strong> (설치 불필요, 바로 사용)</p>"),
        ],
        "faq": [
            ("GIMP이 포토샵을 완전히 대체할 수 있나요?", "일반적인 사진 편집, 합성, 리터칭은 GIMP으로 충분히 가능합니다. 다만 <strong>일러스트레이터와의 통합, 특정 플러그인 호환</strong> 등 전문 작업에는 포토샵이 여전히 우위입니다."),
            ("스마트폰 사진 편집은 어떤 앱이 좋나요?", "모바일은 <strong>Snapseed(무료, Google)</strong>이 가장 강력합니다. RAW 편집, 선택적 보정, 직관적 인터페이스를 무료로 제공합니다."),
            ("Canva 무료 버전과 유료 버전 차이는?", "무료 버전도 대부분의 기능을 사용할 수 있습니다. 유료(Pro)는 <strong>배경 제거, 마법 리사이즈, 프리미엄 소재</strong>가 추가됩니다."),
        ],
        "ctas": [
            {"text": "GIMP 무료 다운로드", "desc": "완전 무료 포토샵 대체 GIMP을 다운로드하세요", "url": "https://www.gimp.org/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "Photopea 브라우저에서 바로 사용", "desc": "설치 없이 브라우저에서 PSD 편집을 시작하세요", "url": "https://www.photopea.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "Canva 무료로 시작하기", "desc": "SNS 디자인, 썸네일을 Canva로 무료 제작하세요", "url": "https://www.canva.com/ko_kr/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "메모 앱 추천 노션 vs 옵시디언 vs 원노트 비교",
        "cat": 5,
        "slug": "note-app-comparison-2026",
        "intro": "아이디어 기록부터 프로젝트 관리까지, 좋은 메모 앱 하나가 생산성을 크게 높여줍니다. <strong>Notion, Obsidian, OneNote, Apple Notes, Google Keep</strong>까지 2026년 주요 메모 앱을 기능·가격·동기화 방식으로 비교합니다.",
        "sections": [
            ("메모 앱 전체 비교표", "<table><thead><tr><th>앱</th><th>가격</th><th>플랫폼</th><th>오프라인</th><th>데이터 저장</th><th>특징</th></tr></thead><tbody><tr><td>Notion</td><td>무료/월 1.6만원(Plus)</td><td>전 플랫폼</td><td>제한적</td><td>클라우드</td><td>DB·협업·올인원</td></tr><tr><td>Obsidian</td><td>무료/Sync 월 1만원</td><td>전 플랫폼</td><td>완전 지원</td><td>로컬 파일</td><td>마크다운, 연결 사고</td></tr><tr><td>Microsoft OneNote</td><td>무료 (Office 포함)</td><td>전 플랫폼</td><td>O</td><td>OneDrive</td><td>자유 배치, 수기 지원</td></tr><tr><td>Apple Notes</td><td>무료 (Apple 기기)</td><td>iOS/Mac</td><td>O</td><td>iCloud</td><td>간단, 빠름</td></tr><tr><td>Google Keep</td><td>무료</td><td>전 플랫폼</td><td>제한적</td><td>Google Drive</td><td>색상 메모, 리마인더</td></tr><tr><td>Bear</td><td>무료/월 1.7달러</td><td>iOS/Mac</td><td>O</td><td>iCloud</td><td>마크다운, 깔끔한 UI</td></tr></tbody></table>"),
            ("Notion - 올인원 생산성 도구", "<p>Notion은 단순한 메모 앱을 넘어 <strong>데이터베이스, 프로젝트 관리, Wiki</strong>까지 가능한 올인원 워크스페이스입니다.</p><ul><li><strong>장점</strong>: 데이터베이스, 칸반 보드, 캘린더 뷰, 팀 협업, AI 기능</li><li><strong>단점</strong>: 오프라인 지원 제한, 복잡한 구조, 느린 로딩</li><li><strong>추천 대상</strong>: 프리랜서, 스타트업, 프로젝트 관리가 필요한 분</li></ul>"),
            ("Obsidian - 로컬 기반 마크다운 메모", "<p>모든 데이터가 <strong>내 컴퓨터에 마크다운 파일로 저장</strong>됩니다. 클라우드 서비스에 의존하지 않는 안전한 개인 지식 관리 시스템입니다.</p><ul><li><strong>장점</strong>: 완전한 오프라인, 파일 소유권 100%, 백링크·그래프 뷰, 플러그인 풍부</li><li><strong>단점</strong>: 동기화는 Obsidian Sync(유료) 또는 직접 설정, 초보자 진입 장벽</li><li><strong>추천 대상</strong>: 개발자, 연구자, 지식 관리에 진지한 분</li></ul>"),
            ("사용 사례별 추천", "<ul><li><strong>빠른 메모, 리마인더</strong>: Apple Notes (아이폰 사용자) 또는 Google Keep</li><li><strong>프로젝트 관리 + 메모</strong>: Notion</li><li><strong>장기 지식 축적, 연구 노트</strong>: Obsidian</li><li><strong>수기 필기 + 디지털 노트</strong>: OneNote (Surface, iPad와 함께)</li><li><strong>마크다운 블로그 겸용</strong>: Obsidian 또는 Bear</li></ul>"),
        ],
        "faq": [
            ("Notion과 Obsidian 중 무엇을 선택해야 하나요?", "협업과 프로젝트 관리가 필요하면 <strong>Notion</strong>, 개인 지식 관리와 데이터 소유권이 중요하면 <strong>Obsidian</strong>을 선택하세요. 둘 다 무료로 시작할 수 있으니 직접 써보는 것이 좋습니다."),
            ("메모 앱의 데이터는 안전한가요?", "Notion, Google Keep은 클라우드에 저장됩니다. 완전한 데이터 소유권을 원한다면 <strong>Obsidian(로컬 저장)</strong>이나 OneNote(OneDrive)를 사용하세요."),
            ("여러 기기에서 동기화가 잘 되는 앱은?", "Notion은 모든 플랫폼에서 실시간 동기화됩니다. Apple Notes는 애플 기기 간 동기화가 완벽합니다. Obsidian은 Sync 플러그인(유료)이나 iCloud/Google Drive를 활용하세요."),
        ],
        "ctas": [
            {"text": "Notion 무료로 시작하기", "desc": "노션 무료 계정으로 올인원 워크스페이스를 경험하세요", "url": "https://www.notion.so/ko-kr", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "Obsidian 무료 다운로드", "desc": "로컬 마크다운 메모 앱 Obsidian을 무료로 다운로드하세요", "url": "https://obsidian.md/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "Microsoft OneNote 무료 사용", "desc": "무료로 제공되는 원노트로 메모를 시작하세요", "url": "https://www.onenote.com/?public=1", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "비밀번호 관리자 추천 2026 무료 유료 비교 TOP 5",
        "cat": 5,
        "slug": "password-manager-recommendation-2026",
        "intro": "평균적인 사람이 관리하는 온라인 계정은 100개 이상입니다. 모든 곳에 같은 비밀번호를 사용하는 것은 <strong>해킹 위험을 극적으로 높입니다</strong>. 비밀번호 관리자는 복잡한 비밀번호를 안전하게 저장하고 자동 입력해줍니다. 1Password, Bitwarden, LastPass, Dashlane, NordPass를 비교합니다.",
        "sections": [
            ("비밀번호 관리자 비교표 2026", "<table><thead><tr><th>서비스</th><th>무료 플랜</th><th>유료 가격</th><th>암호화</th><th>2FA</th><th>가족 플랜</th></tr></thead><tbody><tr><td>1Password</td><td>X (14일 체험)</td><td>월 2.99달러</td><td>AES-256</td><td>O</td><td>월 4.99달러/5명</td></tr><tr><td>Bitwarden</td><td>O (무제한 기기)</td><td>연 10달러</td><td>AES-256</td><td>O</td><td>연 40달러/6명</td></tr><tr><td>LastPass</td><td>O (1기기 제한)</td><td>월 3달러</td><td>AES-256</td><td>O</td><td>월 4달러/6명</td></tr><tr><td>Dashlane</td><td>O (25개 제한)</td><td>월 4.99달러</td><td>AES-256</td><td>O</td><td>월 7.49달러/10명</td></tr><tr><td>NordPass</td><td>O (1기기)</td><td>월 1.99달러</td><td>XChaCha20</td><td>O</td><td>월 3.69달러/6명</td></tr></tbody></table>"),
            ("Bitwarden - 최고의 무료 비밀번호 관리자", "<p>오픈소스 비밀번호 관리자로, <strong>무료 플랜에서 무제한 기기·무제한 비밀번호</strong>를 지원합니다. 보안 전문가들이 가장 신뢰하는 무료 옵션입니다.</p><ul><li>완전 오픈소스 (코드 공개, 외부 감사)</li><li>무료로 모든 기기에서 동기화</li><li>자체 서버 호스팅 가능 (Vaultwarden)</li><li>유료(연 10달러)는 2FA 강화, 암호화 파일 첨부</li></ul>"),
            ("1Password - 사용성 최고의 유료 관리자", "<p>가장 직관적인 UI와 우수한 사용성으로 <strong>가족·팀 공유에 최적</strong>입니다.</p><ul><li>Travel Mode: 국경 통과 시 민감한 볼트 숨김</li><li>Watchtower: 유출된 비밀번호 자동 감지</li><li>14일 무료 체험 후 월 2.99달러</li></ul>"),
            ("비밀번호 관리자 보안 원리", "<p>비밀번호 관리자는 어떻게 안전한가요?</p><ol><li><strong>제로 지식 아키텍처</strong>: 서비스 회사도 내 비밀번호를 볼 수 없음</li><li><strong>AES-256 암호화</strong>: 군사급 암호화로 로컬·클라우드 보호</li><li><strong>마스터 비밀번호</strong>: 하나의 강력한 비밀번호로 전체 관리</li><li><strong>2FA 추가 보호</strong>: 마스터 비밀번호 도용 시에도 2차 인증 필요</li></ol>"),
        ],
        "faq": [
            ("비밀번호 관리자가 해킹되면 어떻게 되나요?", "LastPass는 2022년 해킹을 당했지만, <strong>제로 지식 암호화</strong>로 인해 실제 비밀번호는 보호되었습니다. 마스터 비밀번호만 강력하게 설정하면 안전합니다."),
            ("브라우저 내장 비밀번호 저장과 전용 관리자 차이는?", "크롬, 사파리 내장 저장은 편리하지만 <strong>기기·브라우저 간 완전 동기화, 보안 감사, 2FA 지원</strong>이 부족합니다. 전용 관리자가 훨씬 안전합니다."),
            ("무료로 충분한 비밀번호 관리자는?", "<strong>Bitwarden 무료 플랜</strong>이 최고입니다. 무제한 비밀번호, 무제한 기기, 오픈소스 보안을 완전 무료로 제공합니다."),
        ],
        "ctas": [
            {"text": "Bitwarden 무료로 시작하기", "desc": "오픈소스 비밀번호 관리자 Bitwarden을 무료로 사용하세요", "url": "https://bitwarden.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "1Password 14일 무료 체험", "desc": "1Password 14일 무료 체험을 통해 직접 경험해보세요", "url": "https://1password.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "NordPass 최저가 구매하기", "desc": "NordVPN과 함께 쓰면 더욱 저렴한 NordPass를 확인하세요", "url": "https://nordpass.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "무료 백신 프로그램 추천 2026 성능 비교 테스트",
        "cat": 5,
        "slug": "free-antivirus-recommendation-2026",
        "intro": "랜섬웨어, 피싱, 스파이웨어 위협이 날로 진화하는 2026년, <strong>백신 프로그램</strong>은 필수입니다. Windows Defender, Avast, AVG, Bitdefender Free, 알약, V3 Lite까지 무료 백신의 실제 성능과 시스템 영향을 비교합니다.",
        "sections": [
            ("무료 백신 프로그램 비교표", "<table><thead><tr><th>백신</th><th>가격</th><th>악성코드 탐지율</th><th>시스템 영향</th><th>실시간 보호</th><th>특징</th></tr></thead><tbody><tr><td>Windows Defender</td><td>무료 (내장)</td><td>99.8%</td><td>낮음</td><td>O</td><td>윈도우 기본, 설치 불필요</td></tr><tr><td>Avast Free</td><td>무료</td><td>99.9%</td><td>중간</td><td>O</td><td>Wi-Fi 스캔, 광고 많음</td></tr><tr><td>AVG AntiVirus Free</td><td>무료</td><td>99.9%</td><td>중간</td><td>O</td><td>Avast 계열, 간단한 UI</td></tr><tr><td>Bitdefender Free</td><td>무료</td><td>100%</td><td>낮음</td><td>O</td><td>최고 탐지율, 가벼움</td></tr><tr><td>알약</td><td>무료</td><td>97%</td><td>낮음</td><td>O</td><td>국내 악성코드 특화</td></tr><tr><td>V3 Lite</td><td>무료</td><td>97%</td><td>낮음</td><td>O</td><td>국내 개발, 한국어</td></tr></tbody></table>"),
            ("Windows Defender - 최고의 무료 백신", "<p>많은 사람들이 모르는 사실: <strong>Windows Defender는 이미 업계 최고 수준의 백신</strong>입니다. AV-TEST, AV-Comparatives 독립 기관에서 지속적으로 99.8% 이상의 탐지율을 기록합니다.</p><ul><li>별도 설치 불필요, 윈도우에 내장</li><li>시스템 리소스 사용량 최소</li><li>클라우드 기반 실시간 업데이트</li><li>마이크로소프트 보안 인텔리전스 활용</li></ul>"),
            ("Bitdefender Free - 최고 탐지율 가벼운 백신", "<p>독립 테스트에서 지속적으로 <strong>100% 탐지율</strong>을 기록하는 Bitdefender의 무료 버전입니다.</p><ul><li>Autopilot 모드: 자동으로 위협 처리</li><li>시스템 부하 최소 (클라우드 스캔)</li><li>단점: 설정 옵션 제한적</li></ul>"),
            ("알약 vs V3 Lite - 국내 백신 비교", "<h3>알약 (이스트소프트)</h3><ul><li>국내 악성코드, 피싱 사이트 차단에 특화</li><li>PC 최적화 기능 포함</li><li>단점: 광고 팝업, 번들 소프트웨어 주의</li></ul><h3>V3 Lite (안랩)</h3><ul><li>국내 최대 보안 기업 안랩 제품</li><li>APT 공격, 국내 해킹 그룹 대응 우수</li><li>단점: 고급 기능은 유료(V3 Internet Security)</li></ul>"),
        ],
        "faq": [
            ("백신 여러 개를 동시에 설치해도 되나요?", "<strong>절대 안 됩니다</strong>. 두 백신이 서로를 악성코드로 오인하여 충돌이 발생합니다. 하나의 백신만 설치하고 나머지는 제거하세요."),
            ("Windows Defender만으로 충분한가요?", "일반 사용자에게는 <strong>Windows Defender + 브라우저 내장 보호</strong>로 충분합니다. 추가 보안을 원하면 Bitdefender Free를 추천합니다."),
            ("무료 백신과 유료 백신 차이점은?", "무료 백신도 탐지율은 유료와 거의 동일합니다. 유료는 <strong>VPN, 암호 관리자, 피싱 차단, 부모 통제</strong> 등 부가 기능이 추가됩니다."),
        ],
        "ctas": [
            {"text": "Windows 보안 설정 바로가기", "desc": "Windows Defender 보안 상태를 지금 바로 확인하세요", "url": "https://support.microsoft.com/ko-kr/windows/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "Bitdefender Free 다운로드", "desc": "100% 탐지율 Bitdefender 무료 버전을 받으세요", "url": "https://www.bitdefender.com/solutions/free.html", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "알약 무료 다운로드", "desc": "국내 악성코드 특화 알약 무료 버전을 다운로드하세요", "url": "https://www.estsecurity.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "파일 압축 프로그램 추천 반디집 vs 7zip vs WinRAR",
        "cat": 5,
        "slug": "file-compression-program-comparison-2026",
        "intro": "ZIP, RAR, 7Z 등 압축 파일을 다루기 위한 <strong>파일 압축 프로그램</strong>. 반디집, 7-Zip, WinRAR, 알집 중 어떤 것이 가장 좋을까요? 2026년 압축률, 지원 포맷, 속도, 무료·유료 여부를 기준으로 완전 비교합니다.",
        "sections": [
            ("파일 압축 프로그램 비교표", "<table><thead><tr><th>프로그램</th><th>가격</th><th>지원 압축 포맷</th><th>압축률</th><th>속도</th><th>한국어</th></tr></thead><tbody><tr><td>반디집</td><td>무료 (광고)/3.3만원</td><td>ZIP, RAR, 7Z, TAR 등 30+</td><td>중상</td><td>빠름</td><td>O</td></tr><tr><td>7-Zip</td><td>완전 무료 (오픈소스)</td><td>ZIP, 7Z, RAR(해제), TAR 등</td><td>최상 (7Z)</td><td>중간</td><td>O</td></tr><tr><td>WinRAR</td><td>40일 무료/4만원</td><td>RAR, ZIP, 7Z 등</td><td>상 (RAR5)</td><td>빠름</td><td>O</td></tr><tr><td>PeaZip</td><td>완전 무료 (오픈소스)</td><td>200+ 포맷</td><td>상</td><td>중간</td><td>부분</td></tr><tr><td>알집</td><td>무료</td><td>ZIP, ALZ, EGG, RAR 등</td><td>중</td><td>보통</td><td>O</td></tr></tbody></table>"),
            ("7-Zip - 완전 무료 최강 압축률", "<p>오픈소스 무료 프로그램으로 <strong>7Z 포맷 압축률이 ZIP 대비 30~70% 우수</strong>합니다.</p><ul><li>7Z 포맷: 최고 압축률, AES-256 암호화</li><li>ZIP, TAR, GZIP 등 대부분 포맷 지원</li><li>단점: UI가 구식, RAR 생성 불가 (해제만 가능)</li><li><strong>개발자, 서버 작업자에게 최적</strong></li></ul>"),
            ("반디집 - 국내 최고 사용성", "<p>이스트소프트(알집)에서 만든 반디집은 <strong>국내 1위 점유율</strong>의 무료 압축 프로그램입니다.</p><ul><li>한글 파일명 깨짐 방지 (국내 최적화)</li><li>미리 보기 기능, 깔끔한 UI</li><li>무료 버전 광고 있음 (구매 시 제거)</li><li>EGG, ALZ 등 국내 포맷 완벽 지원</li></ul>"),
            ("압축 포맷별 특징 및 추천", "<table><thead><tr><th>포맷</th><th>압축률</th><th>호환성</th><th>암호화</th><th>추천 용도</th></tr></thead><tbody><tr><td>ZIP</td><td>중</td><td>최고 (모든 OS)</td><td>약함</td><td>범용 공유</td></tr><tr><td>7Z</td><td>최상</td><td>7-Zip 필요</td><td>AES-256</td><td>최대 압축, 로컬 보관</td></tr><tr><td>RAR/RAR5</td><td>상</td><td>WinRAR 필요</td><td>AES-256</td><td>멀티볼륨, 복구 레코드</td></tr><tr><td>TAR.GZ</td><td>상</td><td>Linux/Mac 기본</td><td>없음</td><td>서버, 개발 환경</td></tr></tbody></table>"),
        ],
        "faq": [
            ("반디집과 알집 중 어떤 것이 더 좋나요?", "<strong>반디집을 추천합니다</strong>. 알집은 ALZ 포맷 생성이 가능하지만, 번들 소프트웨어 설치 유도가 많습니다. 반디집은 더 가볍고 포맷 지원이 넓습니다."),
            ("압축 파일에 비밀번호를 걸 수 있나요?", "모든 주요 압축 프로그램에서 가능합니다. 보안을 원한다면 <strong>AES-256 암호화를 지원하는 7Z 또는 RAR5 포맷</strong>을 사용하세요."),
            ("WinRAR을 무료로 계속 쓸 수 있나요?", "WinRAR은 40일 이후에도 기능 제한 없이 사용 가능합니다. 다만 팝업이 뜹니다. <strong>완전 무료를 원하면 7-Zip 또는 반디집</strong>을 추천합니다."),
        ],
        "ctas": [
            {"text": "반디집 무료 다운로드", "desc": "반디집 공식 사이트에서 최신 버전을 무료로 받으세요", "url": "https://kr.bandisoft.com/bandizip/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "7-Zip 무료 다운로드", "desc": "완전 무료 오픈소스 7-Zip 최신 버전을 받으세요", "url": "https://www.7-zip.org/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "WinRAR 공식 다운로드", "desc": "WinRAR 공식 사이트에서 최신 버전을 다운로드하세요", "url": "https://www.win-rar.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "원격 데스크톱 프로그램 추천 무료 TOP 5 비교",
        "cat": 5,
        "slug": "remote-desktop-recommendation-2026",
        "intro": "집에서 회사 컴퓨터에 접속하거나, 부모님 PC를 원격으로 도와줄 때 <strong>원격 데스크톱 프로그램</strong>이 필요합니다. Chrome Remote Desktop, AnyDesk, TeamViewer, Parsec, Windows RDP를 속도·보안·무료 기능 범위 기준으로 비교합니다.",
        "sections": [
            ("원격 데스크톱 프로그램 비교표", "<table><thead><tr><th>프로그램</th><th>개인 무료</th><th>기업 무료</th><th>속도/지연</th><th>파일 전송</th><th>모바일 지원</th></tr></thead><tbody><tr><td>Chrome Remote Desktop</td><td>O</td><td>O</td><td>중간</td><td>X</td><td>O</td></tr><tr><td>AnyDesk</td><td>O</td><td>X (유료)</td><td>빠름</td><td>O</td><td>O</td></tr><tr><td>TeamViewer</td><td>O (개인)</td><td>X (유료)</td><td>빠름</td><td>O</td><td>O</td></tr><tr><td>Parsec</td><td>O</td><td>제한적</td><td>최상 (게이밍)</td><td>X</td><td>O</td></tr><tr><td>Windows RDP</td><td>O (Pro 이상)</td><td>O</td><td>매우 빠름 (LAN)</td><td>O</td><td>O</td></tr></tbody></table>"),
            ("Chrome Remote Desktop - 가장 간편한 무료 원격", "<p>구글에서 제공하는 완전 무료 원격 접속 서비스입니다. <strong>설치 후 1분 만에 시작</strong>할 수 있습니다.</p><ul><li>크롬 브라우저 확장 프로그램으로 설치</li><li>구글 계정으로 로그인하면 끝</li><li>모바일 앱에서 PC 제어 가능</li><li>단점: 파일 전송 기능 없음, 속도 다소 느림</li></ul>"),
            ("AnyDesk vs TeamViewer 비교", "<h3>AnyDesk (개인 무료)</h3><ul><li>독자 DeskRT 코덱으로 저지연 60fps 전송</li><li>파일 전송, 원격 인쇄 지원</li><li>개인 사용 무료, 상업 사용은 유료</li></ul><h3>TeamViewer (개인 무료)</h3><ul><li>가장 오래된 원격 솔루션, 안정성 최고</li><li>파일 전송, 화이트보드, 원격 회의 기능</li><li>상업용 감지 시 연결 제한 (개인용만 무료)</li></ul>"),
            ("Parsec - 게이밍 원격 접속 전문", "<p>게임을 원격으로 즐기기 위한 특화 솔루션입니다. <strong>4K 60fps, VRR 지원</strong>으로 집 PC의 고사양 게임을 외부에서 스트리밍할 수 있습니다.</p><ul><li>게임 스트리밍 전용 저지연 프로토콜</li><li>무료 플랜으로 일반 원격 사용 가능</li><li>Warp(유료): 공동 작업, 팀 기능 추가</li></ul>"),
        ],
        "faq": [
            ("원격 데스크톱 사용 시 보안은 안전한가요?", "모든 주요 원격 프로그램은 <strong>AES-256 암호화</strong>를 사용합니다. 세션 종료 후 자동 로그아웃 설정, 강력한 접속 비밀번호를 사용하면 안전합니다."),
            ("집에서 회사 내부망(인트라넷)에 접속할 수 있나요?", "회사 VPN과 결합하면 가능합니다. 또는 <strong>Windows RDP + VPN</strong> 조합이 가장 빠르고 안정적입니다."),
            ("무료 원격 프로그램으로 상업적으로 사용해도 되나요?", "TeamViewer, AnyDesk 무료 버전은 <strong>개인 사용 목적에만 무료</strong>입니다. 회사 업무에 사용하면 유료 라이선스가 필요합니다."),
        ],
        "ctas": [
            {"text": "Chrome Remote Desktop 무료 시작", "desc": "구글 원격 데스크톱을 지금 무료로 설치하세요", "url": "https://remotedesktop.google.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "AnyDesk 무료 다운로드", "desc": "빠른 원격 접속 AnyDesk를 무료로 다운로드하세요", "url": "https://anydesk.com/ko", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "Parsec 게이밍 원격 무료 시작", "desc": "집 PC 게임을 어디서나 즐기는 Parsec을 사용해보세요", "url": "https://parsec.app/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "AI 글쓰기 도구 추천 2026 ChatGPT vs Claude vs Gemini",
        "cat": 5,
        "slug": "ai-writing-tool-comparison-2026",
        "intro": "2026년 AI 글쓰기 도구는 단순 초안 생성을 넘어 <strong>리서치, 번역, 코딩, 브레인스토밍</strong>까지 업무 전반을 지원합니다. ChatGPT, Claude, Gemini, Copilot, Perplexity, 뤼튼을 한국어 성능·가격·용도 기준으로 비교합니다.",
        "sections": [
            ("AI 글쓰기 도구 전체 비교표 2026", "<table><thead><tr><th>서비스</th><th>무료 플랜</th><th>유료 가격</th><th>한국어</th><th>인터넷 검색</th><th>특징</th></tr></thead><tbody><tr><td>ChatGPT</td><td>O (GPT-4o mini)</td><td>월 20달러 (Plus)</td><td>우수</td><td>O (Plus)</td><td>범용성 최고, 플러그인</td></tr><tr><td>Claude</td><td>O (Claude Haiku)</td><td>월 20달러 (Pro)</td><td>우수</td><td>X (기본)</td><td>긴 문서 처리, 안전성</td></tr><tr><td>Gemini</td><td>O (Gemini 1.5 Flash)</td><td>월 2.8만원 (Advanced)</td><td>우수</td><td>O</td><td>구글 생태계 연동</td></tr><tr><td>Microsoft Copilot</td><td>O</td><td>월 30달러 (Pro)</td><td>우수</td><td>O</td><td>오피스 365 통합</td></tr><tr><td>Perplexity</td><td>O</td><td>월 20달러 (Pro)</td><td>중상</td><td>O (핵심)</td><td>AI 검색 전문</td></tr><tr><td>뤼튼</td><td>O</td><td>무료 (모델 제한)</td><td>최상</td><td>O</td><td>한국어 최적화</td></tr></tbody></table>"),
            ("ChatGPT - 가장 범용적인 AI 도구", "<p>OpenAI의 ChatGPT는 <strong>가장 넓은 사용자층과 플러그인 생태계</strong>를 보유하고 있습니다.</p><ul><li>GPT-4o: 텍스트·이미지·음성 멀티모달</li><li>DALL-E 3 이미지 생성 통합</li><li>Custom GPTs: 특화 봇 생성 가능</li><li>무료 플랜: GPT-4o mini (충분히 강력)</li></ul>"),
            ("Claude - 긴 문서와 안전한 글쓰기", "<p>Anthropic의 Claude는 <strong>긴 문서 처리(최대 20만 토큰)와 안전한 응답</strong>에서 우위를 보입니다.</p><ul><li>긴 계약서, 논문, 코드베이스 분석에 탁월</li><li>환각(Hallucination)이 적고 사실적</li><li>글쓰기 스타일이 자연스럽고 인간적</li><li>한국어 글쓰기 품질 매우 우수</li></ul>"),
            ("한국어 글쓰기 성능 비교", "<h3>블로그 포스팅 작성</h3><p>ChatGPT와 Claude 모두 우수합니다. <strong>뤼튼</strong>은 한국 인터넷 문화에 맞는 자연스러운 한국어를 생성합니다.</p><h3>학술 리포트·논문</h3><p><strong>Perplexity</strong>: 출처 인용 기능으로 리서치 논문에 최적.</p><h3>마케팅 카피라이팅</h3><p><strong>ChatGPT Plus</strong> (GPT-4o): 창의적 카피, 다양한 톤앤매너 지원.</p><h3>코드 작성</h3><p><strong>Claude</strong> 또는 <strong>GitHub Copilot</strong>: 코드 품질과 설명이 우수.</p>"),
        ],
        "faq": [
            ("ChatGPT와 Claude 중 어떤 것이 더 좋나요?", "용도에 따라 다릅니다. <strong>ChatGPT</strong>는 범용성·이미지 생성·플러그인이 강하고, <strong>Claude</strong>는 긴 문서 분석·안전한 응답·자연스러운 글쓰기에서 우위입니다."),
            ("무료 플랜으로도 충분히 사용할 수 있나요?", "ChatGPT, Claude, Gemini 모두 무료 플랜으로 기본 사용이 가능합니다. <strong>뤼튼은 완전 무료</strong>로 다양한 AI 모델을 사용할 수 있습니다."),
            ("AI 글쓰기 도구로 작성한 글을 그대로 사용해도 되나요?", "AI 생성 글을 <strong>그대로 사용하는 것은 권장하지 않습니다</strong>. 사실 확인, 개인 경험 추가, 톤 조정 등을 통해 퇴고하는 것이 필수입니다."),
        ],
        "ctas": [
            {"text": "ChatGPT 무료로 시작하기", "desc": "OpenAI ChatGPT를 무료로 시작해보세요", "url": "https://chatgpt.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "뤼튼 무료로 사용하기", "desc": "한국어 특화 AI 도구 뤼튼을 무료로 사용하세요", "url": "https://wrtn.ai/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "Claude AI 무료로 써보기", "desc": "Anthropic Claude를 무료로 체험해보세요", "url": "https://claude.ai/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== 서비스/플랫폼 (21-30) =====
    {
        "title": "OTT 서비스 비교 넷플릭스 웨이브 티빙 쿠팡플레이 2026",
        "cat": 5,
        "slug": "ott-service-comparison-2026",
        "intro": "2026년 국내 OTT 시장은 <strong>넷플릭스, 웨이브, 티빙, 쿠팡플레이, 디즈니+</strong>가 치열하게 경쟁 중입니다. 요금, 콘텐츠, 화질, 동시접속 수를 비교하고 본인에게 맞는 최적의 OTT 조합을 추천합니다.",
        "sections": [
            ("OTT 서비스 전체 요금제 비교표 2026", "<table><thead><tr><th>서비스</th><th>기본 요금</th><th>스탠다드</th><th>프리미엄</th><th>동시접속</th><th>화질</th></tr></thead><tbody><tr><td>넷플릭스</td><td>광고형 5,500원</td><td>13,500원</td><td>17,000원</td><td>2~4명</td><td>최대 4K UHD</td></tr><tr><td>웨이브</td><td>7,900원</td><td>10,900원</td><td>13,900원</td><td>1~4명</td><td>최대 FHD</td></tr><tr><td>티빙</td><td>광고형 5,500원</td><td>10,900원</td><td>13,900원</td><td>1~4명</td><td>최대 FHD</td></tr><tr><td>쿠팡플레이</td><td>로켓와우 포함</td><td>7,890원 (와우)</td><td>-</td><td>5명</td><td>최대 FHD</td></tr><tr><td>디즈니+</td><td>광고형 4,500원</td><td>9,900원</td><td>-</td><td>2~4명</td><td>최대 4K UHD</td></tr><tr><td>애플TV+</td><td>9,900원</td><td>-</td><td>-</td><td>6명</td><td>최대 4K HDR</td></tr></tbody></table>"),
            ("콘텐츠 비교 - 어디서 뭘 봐야 하나?", "<h3>넷플릭스 (글로벌 오리지널 최강)</h3><ul><li>오징어게임, 기묘한 이야기, 종이의 집 등 글로벌 오리지널</li><li>국내 오리지널 투자 확대 (D.P., 수리남 등)</li><li>영화 라이브러리 풍부</li></ul><h3>웨이브 (지상파 콘텐츠)</h3><ul><li>KBS, MBC, SBS 방송 다음날 무료 제공</li><li>국내 드라마 VOD 최강</li><li>스포츠 중계 (MLB, NBA 일부)</li></ul><h3>티빙 (CJ ENM + JTBC)</h3><ul><li>tvN, OCN, JTBC 드라마 당일 편성</li><li>파라마운트+ 채널 포함 (탑건, 마션 등)</li></ul><h3>쿠팡플레이 (스포츠 특화)</h3><ul><li>손흥민 토트넘 경기 독점 중계</li><li>손흥민 EPL 경기, K-리그, MLB</li><li>쿠팡 로켓와우 회원이면 무료</li></ul>"),
            ("비용 최적화 OTT 조합 추천", "<h3>월 1만원 이하로 OTT 즐기기</h3><ul><li><strong>쿠팡플레이</strong>: 로켓와우 회원이면 추가 비용 없음</li><li><strong>티빙 광고형</strong>: 월 5,500원으로 국내 드라마 해결</li></ul><h3>월 2만원으로 넷플릭스 + 국내 OTT</h3><ul><li><strong>넷플릭스 스탠다드</strong> (13,500원) + 쿠팡플레이(와우 포함)</li></ul><h3>가족 4인 OTT 최적화</h3><ul><li><strong>넷플릭스 프리미엄</strong> (17,000원 ÷ 4명 = 4,250원/인)</li><li>또는 쿠팡와우 가족 공유 + 티빙 조합</li></ul>"),
        ],
        "faq": [
            ("넷플릭스 계정 공유가 차단된 이후 어떻게 하면 좋나요?", "2023년부터 계정 공유 제한이 강화되었습니다. <strong>넷플릭스 공식 동거인 추가(월 5,000원)</strong>를 이용하거나, 각자 광고형 요금제(5,500원)에 가입하는 것이 현실적입니다."),
            ("4K 콘텐츠를 볼 수 있는 OTT는?", "국내 OTT 중 <strong>넷플릭스 프리미엄, 디즈니+, 애플TV+</strong>가 4K UHD 콘텐츠를 제공합니다. 웨이브, 티빙은 FHD까지 지원합니다."),
            ("OTT 무료 체험 기간이 있나요?", "대부분의 OTT는 무료 체험을 없앴습니다. <strong>쿠팡플레이</strong>는 쿠팡 로켓와우 무료 체험(30일)으로 함께 이용 가능합니다."),
        ],
        "ctas": [
            {"text": "넷플릭스 시작하기", "desc": "넷플릭스 광고형 요금제로 월 5,500원에 시작하세요", "url": "https://www.netflix.com/kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "쿠팡플레이 로켓와우로 무료 이용", "desc": "쿠팡 로켓와우 회원이면 쿠팡플레이가 무료입니다", "url": "https://www.coupangplay.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "티빙 첫 달 할인 가입하기", "desc": "티빙에서 tvN·JTBC 드라마를 당일 시청하세요", "url": "https://www.tving.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "음악 스트리밍 비교 멜론 스포티파이 애플뮤직 유튜브뮤직 2026",
        "cat": 5,
        "slug": "music-streaming-comparison-2026",
        "intro": "스마트폰으로 음악을 듣는 시대, 어떤 음악 스트리밍 서비스가 가장 좋을까요? <strong>멜론, 스포티파이, 애플뮤직, 유튜브뮤직, FLO, 지니</strong>를 음질, 가격, 한국 음악 라이브러리, 추천 알고리즘 기준으로 2026년 최신 비교합니다.",
        "sections": [
            ("음악 스트리밍 서비스 비교표 2026", "<table><thead><tr><th>서비스</th><th>월 요금</th><th>음질(최고)</th><th>로스리스</th><th>한국 음악</th><th>오프라인</th></tr></thead><tbody><tr><td>멜론</td><td>10,900원</td><td>AAC 320kbps</td><td>X</td><td>최강</td><td>O</td></tr><tr><td>스포티파이</td><td>10,900원</td><td>OGG 320kbps</td><td>X (미출시)</td><td>중간</td><td>O</td></tr><tr><td>애플뮤직</td><td>10,900원</td><td>ALAC 로스리스</td><td>O (무료)</td><td>우수</td><td>O</td></tr><tr><td>유튜브뮤직</td><td>10,900원</td><td>AAC 256kbps</td><td>X</td><td>우수</td><td>O (유료)</td></tr><tr><td>FLO</td><td>7,900원</td><td>FLAC 로스리스</td><td>O (유료)</td><td>최강</td><td>O</td></tr><tr><td>지니뮤직</td><td>7,900원</td><td>FLAC 24bit</td><td>O (유료)</td><td>최강</td><td>O</td></tr></tbody></table>"),
            ("음질 비교 - 로스리스 vs 일반", "<p>음질에 민감하다면 <strong>로스리스(무손실) 음원</strong>을 제공하는 서비스를 선택하세요.</p><h3>로스리스 지원 서비스</h3><ul><li><strong>애플뮤직</strong>: ALAC 로스리스를 추가 비용 없이 제공. 공간 음향(Dolby Atmos)도 무료.</li><li><strong>FLO</strong>: FLAC 로스리스 지원 (Hi-Fi 요금제)</li><li><strong>지니뮤직</strong>: FLAC 24bit 지원 (HD 요금제)</li></ul><h3>로스리스가 필요한가요?</h3><p>유선 이어폰이나 고급 DAC·앰프를 사용한다면 차이가 납니다. 블루투스 이어폰으로는 <strong>기기 코덱 한계(AAC, aptX)로 로스리스의 차이가 거의 없습니다</strong>.</p>"),
            ("한국 음악 팬을 위한 추천", "<h3>K-POP, 국내 음악 중심</h3><p><strong>멜론, FLO, 지니</strong>가 국내 음원 라이브러리가 가장 풍부합니다. 신곡 발매 즉시 스트리밍이 가능하고, 국내 차트가 정확합니다.</p><h3>해외 음악 + K-POP 동시</h3><p><strong>애플뮤직</strong>: 1억 곡 이상의 글로벌 라이브러리 + 한국 음악 풍부 + 로스리스 무료.</p><h3>뮤직비디오까지 함께</h3><p><strong>유튜브뮤직</strong>: 유튜브 뮤직비디오를 음악 앱에서 통합 시청. 유튜브 프리미엄 가입 시 포함.</p>"),
            ("가격 최적화 팁", "<ul><li><strong>가족 요금제</strong>: 스포티파이·애플뮤직·유튜브뮤직 모두 가족 요금제(6명 17,900원~) 제공</li><li><strong>학생 할인</strong>: 스포티파이 학생 5,500원/월, 애플뮤직 5,500원</li><li><strong>유튜브 프리미엄 포함</strong>: 유튜브 프리미엄(14,900원)에 유튜브뮤직 무료 포함</li></ul>"),
        ],
        "faq": [
            ("스포티파이와 애플뮤직 중 어느 것이 더 낫나요?", "한국 음악이 중요하면 <strong>애플뮤직</strong>이 더 낫습니다. 로스리스 음질을 무료로 제공하고 한국 음원도 풍부합니다. 플레이리스트 알고리즘은 스포티파이가 더 정교합니다."),
            ("멜론과 FLO 중 어디가 더 좋나요?", "음질 우선이라면 <strong>FLO(FLAC 로스리스)</strong>, 차트·최신 트렌드가 중요하면 <strong>멜론</strong>이 유리합니다. FLO가 가격이 2,000원 저렴합니다."),
            ("오프라인에서 음악을 듣고 싶으면?", "모든 유료 서비스에서 오프라인 다운로드를 지원합니다. <strong>유튜브뮤직은 유료 플랜에서만</strong> 오프라인이 가능합니다."),
        ],
        "ctas": [
            {"text": "애플뮤직 3개월 무료 체험", "desc": "로스리스 음질과 공간 음향을 3개월 무료로 체험하세요", "url": "https://music.apple.com/kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "멜론 1개월 무료 시작하기", "desc": "멜론 신규 가입 시 1개월 무료 혜택을 받으세요", "url": "https://www.melon.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "스포티파이 무료로 시작하기", "desc": "스포티파이 무료 플랜 또는 프리미엄을 확인하세요", "url": "https://www.spotify.com/kr/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "이메일 서비스 비교 Gmail vs 네이버메일 vs 아웃룩 2026",
        "cat": 5,
        "slug": "email-service-comparison-2026",
        "intro": "이메일은 가장 기본적인 디지털 커뮤니케이션 수단입니다. <strong>Gmail, 네이버 메일, 아웃룩, 프로톤메일</strong>의 저장 용량, 보안, 부가 기능을 2026년 기준으로 비교합니다.",
        "sections": [
            ("이메일 서비스 비교표 2026", "<table><thead><tr><th>서비스</th><th>무료 용량</th><th>광고</th><th>암호화</th><th>스팸 필터</th><th>부가 기능</th></tr></thead><tbody><tr><td>Gmail</td><td>15GB (드라이브 공유)</td><td>O (무료)</td><td>TLS</td><td>최상</td><td>Google 생태계 연동</td></tr><tr><td>네이버 메일</td><td>5GB</td><td>O</td><td>TLS</td><td>상</td><td>네이버 캘린더 연동</td></tr><tr><td>아웃룩</td><td>15GB (OneDrive 공유)</td><td>O (무료)</td><td>TLS</td><td>상</td><td>Office 365 연동</td></tr><tr><td>Proton Mail</td><td>500MB (무료)</td><td>X</td><td>E2E 암호화</td><td>상</td><td>완전 프라이버시</td></tr><tr><td>다음 메일</td><td>무제한</td><td>O</td><td>TLS</td><td>중</td><td>카카오 계정 연동</td></tr></tbody></table>"),
            ("Gmail - 가장 스마트한 이메일", "<p>구글의 AI가 적용된 <strong>스팸 필터, 자동 분류, 스마트 리플라이</strong>가 가장 발전했습니다.</p><ul><li>15GB 무료 (Google Drive, Gmail, Google Photos 공유)</li><li>Google Workspace와 완벽 연동</li><li>써드파티 앱 연동 (CRM, 자동화 등)</li><li>단점: 구글의 이메일 내용 분석 (광고 개인화)</li></ul>"),
            ("Proton Mail - 프라이버시 최우선", "<p>스위스 제네바에 서버를 두고, <strong>종단간 암호화(E2E)</strong>로 Proton도 이메일 내용을 볼 수 없습니다.</p><ul><li>무료: 500MB, 1주소, 기본 기능</li><li>유료(월 4달러): 15GB, 10주소, 커스텀 도메인</li><li>추천: 보안·프라이버시가 중요한 비즈니스</li></ul>"),
            ("이메일 사용 팁", "<ol><li><strong>이메일 주소 정리</strong>: 업무용, 개인용, 가입용 3개를 분리해서 사용하세요.</li><li><strong>2단계 인증</strong>: Gmail, 아웃룩 모두 반드시 2FA를 설정하세요.</li><li><strong>구독 취소 정기적으로</strong>: Unroll.me 등을 활용해 불필요한 뉴스레터를 정리하세요.</li><li><strong>PGP 암호화</strong>: 중요한 메일은 PGP(Pretty Good Privacy) 암호화를 추가하세요.</li></ol>"),
        ],
        "faq": [
            ("네이버 메일 vs Gmail 어느 것이 더 좋나요?", "업무용으로는 <strong>Gmail</strong>이 Google Workspace와의 연동, 스팸 필터 성능, 써드파티 연동에서 압도적입니다. 국내 서비스 위주라면 네이버 메일도 충분합니다."),
            ("Proton Mail은 무료로 쓸 수 있나요?", "무료 플랜은 <strong>500MB 저장, 1개 주소</strong>로 제한됩니다. 일반 사용에는 부족하지만, 보안이 중요한 주요 계정용으로 사용하기에 적합합니다."),
            ("이메일 계정이 해킹되면 어떻게 하나요?", "즉시 비밀번호를 변경하고, <strong>연결된 모든 기기에서 로그아웃</strong>하세요. 2FA를 설정하고 복구 이메일/전화번호를 최신 상태로 유지하세요."),
        ],
        "ctas": [
            {"text": "Gmail 계정 만들기", "desc": "구글 Gmail 계정을 무료로 만드세요", "url": "https://mail.google.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "Proton Mail 보안 메일 시작", "desc": "E2E 암호화 Proton Mail 무료 계정을 만드세요", "url": "https://proton.me/mail", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "Microsoft Outlook 무료 시작", "desc": "아웃룩 무료 계정으로 Office 생태계를 사용하세요", "url": "https://outlook.live.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "무료 클라우드 용량 비교 2026 최대한 확보하는 방법",
        "cat": 5,
        "slug": "free-cloud-storage-comparison-2026",
        "intro": "사진, 문서, 백업 파일을 안전하게 보관하려면 <strong>클라우드 스토리지</strong>가 필수입니다. Google Drive, OneDrive, iCloud, Dropbox, MEGA, 네이버 MYBOX의 무료 용량을 비교하고, 추가 비용 없이 클라우드 용량을 최대화하는 방법을 안내합니다.",
        "sections": [
            ("무료 클라우드 용량 비교표 2026", "<table><thead><tr><th>서비스</th><th>무료 용량</th><th>유료(최저)</th><th>앱 지원</th><th>특징</th></tr></thead><tbody><tr><td>Google Drive</td><td>15GB</td><td>월 2,900원 (100GB)</td><td>전 플랫폼</td><td>Google 문서 연동</td></tr><tr><td>OneDrive</td><td>5GB</td><td>월 3,900원 (100GB)</td><td>전 플랫폼</td><td>Office 연동, Windows 기본</td></tr><tr><td>iCloud Drive</td><td>5GB</td><td>월 1,100원 (50GB)</td><td>Apple 기기</td><td>애플 기기 자동 백업</td></tr><tr><td>Dropbox</td><td>2GB</td><td>월 9.99달러 (2TB)</td><td>전 플랫폼</td><td>팀 협업, 버전 관리</td></tr><tr><td>MEGA</td><td>20GB</td><td>월 4.99유로 (400GB)</td><td>전 플랫폼</td><td>E2E 암호화, 대용량 무료</td></tr><tr><td>네이버 MYBOX</td><td>30GB</td><td>월 990원 (80GB 추가)</td><td>전 플랫폼</td><td>국내 최대 무료 용량</td></tr></tbody></table>"),
            ("무료 클라우드 용량 최대화 전략", "<h3>전략 1: 여러 서비스 조합</h3><p>Google Drive(15GB) + MEGA(20GB) + 네이버 MYBOX(30GB) = <strong>65GB 무료</strong></p><h3>전략 2: Google One 프로모션 활용</h3><p>구글 기기(Pixel, Chromebook) 구매 시 추가 무료 저장 공간 제공. 삼성 갤럭시 구매 시 OneDrive 100GB 1년 무료 제공 확인.</p><h3>전략 3: 사진 최적화</h3><p>Google Photos의 '저장 용량 절약' 품질을 사용하면 사진 용량이 대폭 줄어듭니다.</p>"),
            ("클라우드 서비스별 보안 비교", "<ul><li><strong>MEGA</strong>: 종단간 암호화(E2E). 서비스 제공자도 파일을 볼 수 없음. 가장 안전.</li><li><strong>Proton Drive</strong>: E2E 암호화, 스위스 서버. 보안 최우선 사용자.</li><li><strong>Google Drive, OneDrive</strong>: 서버사이드 암호화. 서비스 제공자가 이론적으로 접근 가능.</li><li><strong>iCloud</strong>: Advanced Data Protection 활성화 시 E2E 암호화 가능.</li></ul>"),
        ],
        "faq": [
            ("무료로 가장 많은 클라우드 용량을 얻는 방법은?", "<strong>네이버 MYBOX(30GB) + MEGA(20GB) + Google Drive(15GB)</strong> 조합으로 총 65GB를 무료로 확보하세요."),
            ("클라우드에 올린 파일이 삭제될 위험은 없나요?", "서비스가 종료되거나 계정이 비활성화되면 파일이 삭제될 수 있습니다. <strong>중요한 파일은 2곳 이상에 백업</strong>하세요."),
            ("iCloud 5GB가 너무 부족한데 어떻게 하나요?", "사진을 Google Photos로 이전하거나, iCloud 50GB 요금제(월 1,100원)로 업그레이드하는 것이 가장 간단합니다."),
        ],
        "ctas": [
            {"text": "Google One 스토리지 업그레이드", "desc": "구글 드라이브 100GB 요금제를 월 2,900원으로 시작하세요", "url": "https://one.google.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "네이버 MYBOX 30GB 무료 시작", "desc": "네이버 MYBOX 30GB 무료 저장공간을 지금 사용하세요", "url": "https://mybox.naver.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "MEGA 20GB 무료 클라우드", "desc": "E2E 암호화 MEGA에서 20GB 무료 저장공간을 받으세요", "url": "https://mega.io/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "도메인 등록 사이트 추천 가격 비교 2026",
        "cat": 5,
        "slug": "domain-registration-comparison-2026",
        "intro": "블로그, 쇼핑몰, 포트폴리오 사이트를 시작하려면 <strong>도메인 등록</strong>이 첫 번째입니다. 가비아, Namecheap, GoDaddy, Cloudflare, 카페24를 가격·서비스·이전 절차 기준으로 비교합니다.",
        "sections": [
            ("도메인 등록 사이트 가격 비교표 2026", "<table><thead><tr><th>사이트</th><th>.com 첫해</th><th>.com 갱신</th><th>.kr 첫해</th><th>WHOIS 보호</th><th>특징</th></tr></thead><tbody><tr><td>가비아</td><td>15,000원</td><td>22,000원</td><td>22,000원</td><td>무료</td><td>국내 1위, 한국어 AS</td></tr><tr><td>Hosting.kr</td><td>10,000원</td><td>15,000원</td><td>20,000원</td><td>무료</td><td>국내, 저렴한 갱신</td></tr><tr><td>Namecheap</td><td>8달러</td><td>13달러</td><td>미지원</td><td>무료</td><td>글로벌 가성비 최강</td></tr><tr><td>GoDaddy</td><td>1달러(첫해)</td><td>22달러</td><td>미지원</td><td>유료</td><td>첫해 할인, 갱신비 비쌈</td></tr><tr><td>Cloudflare</td><td>원가 제공</td><td>원가 제공</td><td>미지원</td><td>무료</td><td>마진 없음, 최저 갱신</td></tr><tr><td>카페24</td><td>14,300원</td><td>22,000원</td><td>19,800원</td><td>무료</td><td>호스팅 연계 편리</td></tr></tbody></table>"),
            ("도메인 등록 시 주의사항", "<ol><li><strong>갱신 가격 확인</strong>: GoDaddy처럼 첫해 1달러에 판매하고 갱신은 22달러인 곳이 있습니다. 갱신 가격이 더 중요합니다.</li><li><strong>WHOIS 보호</strong>: 개인정보(이름, 주소, 전화번호) 노출을 막는 WHOIS 보호가 무료로 제공되는지 확인하세요.</li><li><strong>자동 갱신 설정</strong>: 도메인 만료를 방지하기 위해 자동 갱신을 설정하세요.</li><li><strong>도메인 잠금</strong>: 무단 이전을 방지하는 도메인 잠금 기능을 활성화하세요.</li></ol>"),
            ("도메인 이전(이관) 방법", "<p>현재 등록사에서 다른 곳으로 이전하는 절차:</p><ol><li>현재 등록사에서 <strong>EPP 코드(이전 인증 코드)</strong> 발급</li><li>이전 대상 등록사에서 이관 신청</li><li>등록사 이메일로 이전 승인 확인</li><li>이전 완료까지 5~7일 소요</li></ol><p>Cloudflare로 이전 시 갱신 가격이 원가(마진 0)로 가장 저렴합니다.</p>"),
        ],
        "faq": [
            ("한국 사이트는 .com과 .kr 중 어떤 것이 좋나요?", "국내 타겟이면 <strong>.kr</strong>이 신뢰도가 높습니다. 글로벌 진출을 고려하면 <strong>.com</strong>을 먼저 등록하세요. 예산이 된다면 둘 다 등록하고 .kr에서 .com으로 리다이렉트하는 것도 좋습니다."),
            ("도메인 가격이 왜 등록사마다 다른가요?", "각 등록사가 레지스트리에 지불하는 원가에 마진을 붙여 판매합니다. Cloudflare는 마진을 붙이지 않아 가장 저렴하지만, .kr 도메인은 지원하지 않습니다."),
            ("이미 등록된 도메인을 살 수 있나요?", "가능합니다. <strong>Sedo, Afternic</strong> 등 도메인 거래 마켓플레이스에서 매입할 수 있습니다. 프리미엄 도메인은 수백만~수억 원에 거래되기도 합니다."),
        ],
        "ctas": [
            {"text": "가비아 도메인 등록하기", "desc": "국내 1위 가비아에서 .com/.kr 도메인을 등록하세요", "url": "https://www.gabia.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "Namecheap 저렴한 도메인 등록", "desc": "글로벌 최저가 Namecheap에서 .com 도메인을 등록하세요", "url": "https://www.namecheap.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "Cloudflare 원가 도메인 등록", "desc": "마진 없는 원가 도메인 등록으로 갱신비를 절약하세요", "url": "https://www.cloudflare.com/products/registrar/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
]

POSTS += [
    {
        "title": "웹호스팅 추천 2026 워드프레스 블로그용 가성비 비교",
        "cat": 5,
        "slug": "web-hosting-recommendation-2026",
        "intro": "워드프레스 블로그나 쇼핑몰을 시작하려면 <strong>웹호스팅</strong>이 필요합니다. Cloudways, Vultr, 카페24, 가비아, AWS Lightsail을 속도·가격·워드프레스 최적화 기준으로 비교합니다.",
        "sections": [
            ("웹호스팅 유형별 비교", "<table><thead><tr><th>유형</th><th>특징</th><th>가격대</th><th>추천 대상</th></tr></thead><tbody><tr><td>공유 호스팅</td><td>서버 공유, 저렴</td><td>월 3,000~10,000원</td><td>입문, 저트래픽</td></tr><tr><td>VPS 호스팅</td><td>가상 서버 독립</td><td>월 5,000~50,000원</td><td>중급, 성장 블로그</td></tr><tr><td>관리형 WP 호스팅</td><td>WP 최적화, 관리 대행</td><td>월 15,000~100,000원</td><td>WP 전문 블로거</td></tr><tr><td>클라우드 호스팅</td><td>유연한 확장</td><td>트래픽 기반</td><td>고트래픽, 기업</td></tr></tbody></table>"),
            ("서비스별 상세 비교", "<h3>Cloudways (월 12달러~)</h3><p>관리형 클라우드 호스팅의 최고봉. DO, Vultr, AWS, GCP 위에서 워드프레스를 1클릭으로 배포. 자동 백업, 무료 SSL, Cloudflare 통합. 기술 지식이 없어도 쉽게 관리.</p><h3>카페24 (월 3,300원~)</h3><p>국내 최대 웹호스팅. 한국어 고객지원, 국내 서버로 국내 접속 속도 빠름. 입문자에게 가장 쉬운 선택.</p><h3>가비아 (월 5,500원~)</h3><p>도메인+호스팅 통합 관리. NVMe SSD, 무료 SSL, 자동 백업 포함.</p><h3>Vultr High Frequency (월 6달러~)</h3><p>기술적 지식이 있는 분에게 최고의 가성비. NVMe SSD, 전 세계 32개 데이터센터.</p>"),
            ("워드프레스 속도 최적화 팁", "<ol><li><strong>SSD 호스팅 선택</strong>: HDD 대비 5~10배 빠른 I/O 속도</li><li><strong>Cloudflare CDN</strong>: 무료 플랜으로 글로벌 캐시, 속도 향상</li><li><strong>캐시 플러그인</strong>: WP Rocket, W3 Total Cache 사용</li><li><strong>이미지 최적화</strong>: Smush, ShortPixel로 WebP 변환</li><li><strong>서버 위치</strong>: 한국 방문자 대상이면 서울 서버 선택</li></ol>"),
        ],
        "faq": [
            ("워드프레스 호스팅 입문자에게 무엇을 추천하나요?", "<strong>카페24 또는 가비아</strong>의 국내 공유 호스팅이 가장 쉽습니다. 트래픽이 늘면 Cloudways로 이전을 고려하세요."),
            ("무료 웹호스팅이 있나요?", "000webhost, InfinityFree 등이 있지만 속도·안정성·광고 삽입 문제가 있습니다. 진지한 블로그라면 <strong>최소 월 3,000~5,000원짜리 유료 호스팅</strong>을 사용하세요."),
            ("SSL 인증서는 꼭 필요한가요?", "<strong>필수입니다</strong>. HTTPS 없으면 구글 SEO 불이익, 브라우저 경고 표시가 납니다. 대부분의 호스팅에서 Let's Encrypt SSL을 무료로 제공합니다."),
        ],
        "ctas": [
            {"text": "Cloudways 무료 체험하기", "desc": "Cloudways 3일 무료 체험으로 워드프레스 속도를 확인하세요", "url": "https://www.cloudways.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "카페24 웹호스팅 가입하기", "desc": "국내 최대 카페24 웹호스팅을 월 3,300원에 시작하세요", "url": "https://www.cafe24.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "가비아 호스팅 신청하기", "desc": "도메인+호스팅 통합관리 가비아 호스팅을 확인하세요", "url": "https://www.gabia.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "노코드 웹사이트 빌더 추천 Wix vs 카페24 vs 식스샵 비교",
        "cat": 5,
        "slug": "nocode-website-builder-comparison-2026",
        "intro": "코딩 없이 웹사이트를 만드는 <strong>노코드 빌더</strong>가 2026년 더욱 강력해졌습니다. Wix, 카페24, 식스샵, 아임웹, Shopify를 기능·가격·디자인 자유도·쇼핑몰 기능 기준으로 비교합니다.",
        "sections": [
            ("노코드 웹사이트 빌더 비교표", "<table><thead><tr><th>서비스</th><th>무료 플랜</th><th>유료 최저</th><th>쇼핑몰</th><th>템플릿</th><th>특징</th></tr></thead><tbody><tr><td>Wix</td><td>O (광고 표시)</td><td>월 17달러</td><td>O</td><td>900+</td><td>드래그앤드롭, 자유도 높음</td></tr><tr><td>카페24</td><td>O (쇼핑몰)</td><td>무료 시작 가능</td><td>O (전문)</td><td>200+</td><td>국내 쇼핑몰 1위</td></tr><tr><td>식스샵</td><td>O (제한)</td><td>월 19,000원</td><td>O</td><td>100+</td><td>국내, 쉬운 쇼핑몰</td></tr><tr><td>아임웹</td><td>O (제한)</td><td>월 12,000원</td><td>O</td><td>150+</td><td>국내 포트폴리오, 브랜딩</td></tr><tr><td>Shopify</td><td>X (14일 체험)</td><td>월 29달러</td><td>O (전문)</td><td>100+</td><td>글로벌 쇼핑몰 1위</td></tr><tr><td>Squarespace</td><td>X (14일 체험)</td><td>월 16달러</td><td>O</td><td>150+</td><td>디자인 최고, 포트폴리오</td></tr></tbody></table>"),
            ("용도별 추천", "<h3>국내 쇼핑몰 창업</h3><p><strong>카페24 (무료 시작)</strong>: 국내 결제(카카오페이, 네이버페이, 토스)와 배송사 연동이 가장 완벽합니다. 코딩 없이 쇼핑몰 운영 가능.</p><h3>개인 브랜딩·포트폴리오</h3><p><strong>아임웹</strong>: 감각적인 디자인 템플릿, 국내 서비스로 한국어 지원 완벽.</p><h3>글로벌 쇼핑몰</h3><p><strong>Shopify</strong>: 전 세계 170만+ 상점이 사용하는 글로벌 표준. 해외 판매, 다국어 지원 탁월.</p><h3>프리랜서·개인 홈페이지</h3><p><strong>Wix</strong>: 가장 자유로운 드래그앤드롭, 앱 마켓 생태계.</p>"),
            ("노코드 빌더 장단점 비교", "<table><thead><tr><th>구분</th><th>장점</th><th>단점</th></tr></thead><tbody><tr><td>노코드 빌더</td><td>코딩 불필요, 빠른 시작, 관리 쉬움</td><td>커스터마이징 제한, 플랫폼 종속</td></tr><tr><td>워드프레스</td><td>무한 확장, 플러그인 생태계</td><td>학습 곡선, 보안·업데이트 관리 필요</td></tr></tbody></table>"),
        ],
        "faq": [
            ("카페24와 Shopify 중 어떤 것으로 쇼핑몰을 시작해야 하나요?", "국내 고객 대상이면 <strong>카페24</strong>, 해외 판매가 목표라면 <strong>Shopify</strong>를 추천합니다. 카페24는 무료로 시작 가능합니다."),
            ("노코드 빌더로 만든 사이트의 SEO는 괜찮나요?", "Wix, 아임웹 모두 기본 SEO 설정이 가능합니다. 다만 <strong>워드프레스 + Yoast SEO</strong> 조합에 비해 세밀한 최적화는 어렵습니다."),
            ("사이트 빌더에서 다른 플랫폼으로 이전이 가능한가요?", "대부분 어렵습니다. 콘텐츠 내보내기는 가능하지만 디자인은 새로 작업해야 합니다. 처음부터 플랫폼을 신중하게 선택하세요."),
        ],
        "ctas": [
            {"text": "카페24 무료 쇼핑몰 만들기", "desc": "카페24로 국내 쇼핑몰을 무료로 시작하세요", "url": "https://www.cafe24.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "아임웹 무료로 시작하기", "desc": "아임웹 무료 플랜으로 나만의 홈페이지를 만드세요", "url": "https://www.imweb.me/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "Shopify 14일 무료 체험", "desc": "글로벌 쇼핑몰 Shopify를 14일 무료로 체험하세요", "url": "https://www.shopify.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "전자서명 서비스 비교 카카오 네이버 모두싸인 2026",
        "cat": 5,
        "slug": "e-signature-service-comparison-2026",
        "intro": "계약서, 동의서, 입사 서류를 직접 만나지 않고 처리하는 <strong>전자서명 서비스</strong>. 카카오 전자서명, 네이버 전자서명, 모두싸인, DocuSign을 법적 효력, 무료 범위, 기업 기능 기준으로 비교합니다.",
        "sections": [
            ("전자서명 서비스 비교표 2026", "<table><thead><tr><th>서비스</th><th>무료 범위</th><th>유료 최저</th><th>법적 효력</th><th>기업 기능</th><th>특징</th></tr></thead><tbody><tr><td>카카오 전자서명</td><td>O (카카오 생태계)</td><td>별도 문의</td><td>O (전자서명법)</td><td>O</td><td>카카오 인증 연동</td></tr><tr><td>네이버 전자서명</td><td>O (네이버 생태계)</td><td>별도 문의</td><td>O</td><td>제한적</td><td>네이버 인증 연동</td></tr><tr><td>모두싸인</td><td>월 5건 무료</td><td>월 12,900원</td><td>O</td><td>O</td><td>국내 B2B 특화</td></tr><tr><td>싸인오케이</td><td>월 3건 무료</td><td>월 9,900원</td><td>O</td><td>O</td><td>국내 중소기업 최적</td></tr><tr><td>DocuSign</td><td>30일 무료</td><td>월 15달러</td><td>O (전 세계)</td><td>O</td><td>글로벌 표준</td></tr></tbody></table>"),
            ("한국 전자서명의 법적 효력", "<p>한국 전자서명법에 따라 <strong>공인전자서명</strong>은 서면 서명과 동일한 법적 효력을 갖습니다.</p><ul><li>카카오 인증서, 네이버 인증서: 공인전자서명 수준</li><li>모두싸인, 싸인오케이: 전자서명법 적용 계약 효력</li><li>단, 부동산 계약, 유언장 등 특정 법률 행위는 별도 규정 확인 필요</li></ul>"),
            ("용도별 추천", "<h3>개인 간 계약 (무료)</h3><p><strong>카카오 전자서명</strong> 또는 <strong>네이버 전자서명</strong>: 스마트폰 앱으로 무료로 간편 서명 가능.</p><h3>소규모 사업자</h3><p><strong>싸인오케이</strong> (월 9,900원): 월 30건까지 서명 요청, 국내 중소기업에 최적화.</p><h3>기업·대량 처리</h3><p><strong>모두싸인 기업 플랜</strong>: HR(입사 서류), 영업 계약, 파트너십 계약 대량 처리.</p>"),
        ],
        "faq": [
            ("전자서명은 법적으로 유효한가요?", "한국 전자서명법에 따라 적법한 전자서명은 <strong>법적 효력이 있습니다</strong>. 단, 서명 당사자 확인(본인 인증)이 이루어져야 효력이 인정됩니다."),
            ("무료로 전자서명을 사용할 수 있는 서비스는?", "<strong>카카오 전자서명, 네이버 전자서명</strong>은 개인 간 사용 시 무료입니다. 모두싸인·싸인오케이는 월 3~5건 무료."),
            ("전자서명 문서를 어떻게 보관해야 하나요?", "서명 완료된 문서를 <strong>PDF로 다운로드</strong>하여 클라우드와 로컬 두 곳에 보관하세요. 플랫폼 종료 시 데이터 접근이 불가능할 수 있습니다."),
        ],
        "ctas": [
            {"text": "모두싸인 무료로 시작하기", "desc": "모두싸인 월 5건 무료로 전자서명을 경험하세요", "url": "https://www.modusign.co.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "카카오 전자서명 사용하기", "desc": "카카오 인증서로 간편하게 전자서명을 하세요", "url": "https://accounts.kakao.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "싸인오케이 무료 체험하기", "desc": "싸인오케이로 계약서 전자서명을 바로 시작하세요", "url": "https://www.signokay.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "화상회의 프로그램 비교 줌 vs 구글미트 vs 팀즈 2026",
        "cat": 5,
        "slug": "video-conference-comparison-2026",
        "intro": "재택근무와 하이브리드 근무 시대, <strong>화상회의 프로그램</strong>은 업무의 핵심 도구가 됐습니다. Zoom, Google Meet, Microsoft Teams, Webex, Discord를 무료 기능, 참가자 제한, 화면공유, 보안 기준으로 2026년 최신 비교합니다.",
        "sections": [
            ("화상회의 프로그램 비교표 2026", "<table><thead><tr><th>서비스</th><th>무료 시간 제한</th><th>무료 참가자</th><th>화면공유</th><th>녹화</th><th>특징</th></tr></thead><tbody><tr><td>Zoom</td><td>40분 (3명+)</td><td>100명</td><td>O</td><td>유료</td><td>가장 안정적, 기업 표준</td></tr><tr><td>Google Meet</td><td>60분</td><td>100명</td><td>O</td><td>유료</td><td>Gmail 연동, 간편</td></tr><tr><td>Microsoft Teams</td><td>60분</td><td>100명</td><td>O</td><td>유료</td><td>Office 365 통합</td></tr><tr><td>Webex</td><td>40분</td><td>100명</td><td>O</td><td>유료</td><td>기업·보안 특화</td></tr><tr><td>Discord</td><td>무제한</td><td>25명</td><td>O</td><td>O (Nitro)</td><td>커뮤니티, 게이밍</td></tr></tbody></table>"),
            ("서비스별 특징 비교", "<h3>Zoom - 기업 화상회의 표준</h3><p>가장 안정적인 연결과 풍부한 기능. 무료 플랜은 3인 이상 40분 제한이 있지만, 재연결하면 계속 사용 가능합니다. Zoom AI Companion으로 회의록 자동 생성.</p><h3>Google Meet - 가장 간편한 선택</h3><p>Gmail, Google Calendar와 완벽 연동. 브라우저에서 바로 실행, 설치 불필요. Google Workspace 사용자라면 최고의 선택.</p><h3>Microsoft Teams - 기업 협업 통합</h3><p>Office 365(Word, Excel, Teams) 완벽 통합. 팀 채널, 파일 공유, 실시간 협업이 하나의 플랫폼에서. 기업 환경에 최적.</p>"),
            ("화상회의 화질·음질 개선 팁", "<ol><li><strong>유선 인터넷</strong>: Wi-Fi보다 랜선 연결이 안정적. 특히 중요한 회의 전에 확인.</li><li><strong>조명</strong>: 얼굴 앞쪽에 조명을 배치. 역광은 얼굴이 어두워 보임.</li><li><strong>헤드셋 사용</strong>: 외부 마이크 헤드셋으로 에코·노이즈 제거.</li><li><strong>배경 가상화</strong>: Zoom, Teams 모두 가상 배경 지원. 집 내부가 보이지 않게.</li></ol>"),
        ],
        "faq": [
            ("무료로 시간 제한 없이 화상회의를 할 수 있는 서비스는?", "<strong>Discord</strong>는 무료로 무제한 화상회의가 가능합니다. 단, 최대 25명까지. Google Meet도 개인 계정으로는 60분 무료입니다."),
            ("Zoom 40분 제한을 피하는 방법은?", "회의가 40분을 넘으면 재연결하면 됩니다. 또는 <strong>Google Meet(60분)</strong>으로 전환하거나 Zoom Pro(월 15.99달러)를 구독하세요."),
            ("화상회의 보안이 걱정됩니다. 어떻게 하나요?", "회의 비밀번호를 설정하고, <strong>대기실 기능을 활성화</strong>하여 참가자를 직접 승인하세요. Zoom Bombing(무단 접속)을 방지합니다."),
        ],
        "ctas": [
            {"text": "Zoom 무료로 시작하기", "desc": "줌 무료 계정을 만들고 화상회의를 시작하세요", "url": "https://zoom.us/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "Google Meet 바로 시작하기", "desc": "구글 계정으로 지금 바로 화상회의를 시작하세요", "url": "https://meet.google.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "Microsoft Teams 무료 사용", "desc": "팀즈 무료 버전으로 협업과 화상회의를 시작하세요", "url": "https://www.microsoft.com/ko-kr/microsoft-teams/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "개인 블로그 플랫폼 비교 티스토리 vs 워드프레스 vs 브런치 2026",
        "cat": 5,
        "slug": "blog-platform-comparison-2026",
        "intro": "블로그를 시작하려는데 어떤 플랫폼이 좋을지 고민이신가요? <strong>티스토리, 워드프레스, 브런치, 벨로그, 미디엄</strong>을 수익화, SEO, 커스터마이징, 시작 난이도 기준으로 2026년 비교합니다.",
        "sections": [
            ("블로그 플랫폼 비교표 2026", "<table><thead><tr><th>플랫폼</th><th>가격</th><th>광고 수익</th><th>SEO</th><th>커스터마이징</th><th>난이도</th></tr></thead><tbody><tr><td>티스토리</td><td>무료</td><td>O (카카오 애드핏)</td><td>중상</td><td>중간</td><td>쉬움</td></tr><tr><td>WordPress.org</td><td>호스팅비만</td><td>O (자유)</td><td>최상</td><td>무제한</td><td>중간</td></tr><tr><td>브런치</td><td>무료</td><td>X</td><td>중</td><td>최소</td><td>매우 쉬움</td></tr><tr><td>벨로그</td><td>무료</td><td>X</td><td>중</td><td>최소</td><td>쉬움</td></tr><tr><td>Medium</td><td>무료/월 5달러</td><td>파트너 프로그램</td><td>중</td><td>최소</td><td>매우 쉬움</td></tr><tr><td>GitHub Pages</td><td>무료</td><td>X (직접 삽입 가능)</td><td>상</td><td>높음 (코딩 필요)</td><td>어려움</td></tr></tbody></table>"),
            ("티스토리 - 국내 블로거 최적", "<p>카카오가 운영하는 <strong>국내 최대 블로그 플랫폼</strong>입니다. 네이버 검색 노출이 잘 되고, 카카오 애드핏으로 광고 수익화가 가능합니다.</p><ul><li>장점: 무료, 쉬운 시작, 구글·네이버 SEO 우수</li><li>단점: 카카오 정책 변경 리스크, 자유도 제한</li><li>추천: 수익화를 원하는 입문 블로거</li></ul>"),
            ("워드프레스 - 최고의 자유도", "<p>전 세계 웹사이트의 43%가 워드프레스로 만들어졌습니다. 플러그인, 테마, SEO 최적화가 무한히 가능합니다.</p><ul><li>장점: 완전한 소유권, 무한 확장, 최고의 SEO</li><li>단점: 호스팅비 월 5,000~15,000원, 학습 필요</li><li>추천: 전문 블로거, 수익화에 진지한 분</li></ul>"),
            ("블로그 수익화 전략 비교", "<table><thead><tr><th>수익화 방법</th><th>적합 플랫폼</th><th>예상 수익</th></tr></thead><tbody><tr><td>구글 애드센스</td><td>워드프레스, 티스토리</td><td>월 방문자 1만 기준 5~15만원</td></tr><tr><td>카카오 애드핏</td><td>티스토리</td><td>애드센스의 30~50% 수준</td></tr><tr><td>제휴 마케팅</td><td>모든 플랫폼</td><td>성과 기반, 무제한</td></tr><tr><td>유료 콘텐츠</td><td>워드프레스</td><td>구독자 수에 비례</td></tr></tbody></table>"),
        ],
        "faq": [
            ("블로그로 돈을 벌 수 있나요?", "가능합니다. 구글 애드센스 기준 월 방문자 1만 명이면 <strong>월 5~30만원</strong> 수익이 가능합니다. 하지만 6개월~1년 이상의 꾸준한 포스팅이 전제입니다."),
            ("티스토리와 워드프레스 중 무엇을 선택해야 하나요?", "빠른 시작과 무료를 원하면 <strong>티스토리</strong>, 장기적으로 진지하게 블로그를 키우고 싶다면 <strong>워드프레스</strong>를 추천합니다."),
            ("브런치에서 수익화가 되나요?", "카카오 브런치는 광고 수익화를 지원하지 않습니다. <strong>브랜딩과 포트폴리오</strong> 목적으로 활용하고, 수익화는 다른 플랫폼과 병행하세요."),
        ],
        "ctas": [
            {"text": "티스토리 블로그 무료 시작", "desc": "티스토리로 무료 블로그를 지금 바로 시작하세요", "url": "https://www.tistory.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "워드프레스 시작하기", "desc": "WordPress.org로 나만의 블로그를 만드세요", "url": "https://ko.wordpress.org/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "브런치 작가 신청하기", "desc": "브런치에서 나의 글을 세상에 알려보세요", "url": "https://brunch.co.kr/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    # ===== 보안/프라이버시 (31-37) =====
    {
        "title": "스미싱 문자 구별법 피해 예방 대처 방법 총정리 2026",
        "cat": 5,
        "slug": "smishing-prevention-guide-2026",
        "intro": "택배 도착 알림, 건강보험 환급, 정부 지원금 문자... 이 중에 <strong>스미싱(피싱 문자)</strong>이 섞여 있습니다. 2026년 스미싱 수법은 더욱 정교해져 실제 문자와 구별하기 어렵습니다. 유형별 사례, 구별법, 피해 시 대처법을 완벽히 정리합니다.",
        "sections": [
            ("2026년 주요 스미싱 유형 10가지", "<ol><li><strong>택배 불이행 알림</strong>: '고객님의 택배가 반송 처리됩니다. 주소 확인: [URL]'</li><li><strong>건강보험 환급금</strong>: '국민건강보험 환급금 XXX원 지급 대상자입니다'</li><li><strong>정부 지원금</strong>: '소상공인 지원금 신청 마감 D-1. 지금 신청하세요'</li><li><strong>금융 기관 사칭</strong>: '고객님의 계좌가 이상 거래로 잠겼습니다'</li><li><strong>가족 사칭</strong>: '엄마 나 폰 고장났어. 이 번호로 연락해줘'</li><li><strong>청첩장·부고 문자</strong>: '[청첩장] 링크 클릭 시 악성앱 설치</li><li><strong>공공기관 과태료</strong>: '교통법규 위반 과태료 고지서'</li><li><strong>대출 광고형 피싱</strong>: '저금리 대출 승인. 신청하기'</li><li><strong>쇼핑몰 할인 쿠폰</strong>: '이번 주만 80% 할인 쿠폰 발급'</li><li><strong>앱 업데이트 사칭</strong>: '카카오뱅크 긴급 업데이트 필요'</li></ol>"),
            ("스미싱 문자 구별법 5가지", "<h3>1. URL 주소 확인</h3><p>공식 기관은 절대 <strong>단축 URL(bit.ly, naver.me 등)</strong>을 사용하지 않습니다. 링크를 클릭하기 전 문자를 꾹 눌러 URL 전체 주소를 확인하세요.</p><h3>2. 발신 번호 확인</h3><p>070, 해외 번호(+1, +44 등), 또는 일반 스마트폰 번호(010)에서 오는 공공기관 문자는 의심하세요.</p><h3>3. 개인정보·금전 요구</h3><p>어떤 기관도 문자로 <strong>계좌번호, 비밀번호, 주민번호</strong>를 요구하지 않습니다.</p><h3>4. 긴박감 조성</h3><p>'오늘까지', '지금 바로', 'D-1' 등 긴박감을 조성하는 문자는 스미싱일 가능성이 높습니다.</p><h3>5. 맞춤법·어색한 표현</h3><p>공공기관 공문은 정확한 맞춤법을 사용합니다. 어색한 표현, 오타가 있으면 의심하세요.</p>"),
            ("스미싱 피해 시 대처법 (단계별)", "<ol><li><strong>즉시 비행기 모드</strong>: 악성 앱의 추가 정보 전송을 막기 위해 네트워크를 끊으세요</li><li><strong>악성 앱 삭제</strong>: 설정 > 앱 관리에서 최근 설치된 의심 앱 삭제</li><li><strong>금융기관 연락</strong>: 계좌·카드 정지 요청 (금융감독원: 1332)</li><li><strong>통신사 소액결제 차단</strong>: 통신사 고객센터에 소액결제 차단 요청</li><li><strong>경찰 신고</strong>: 경찰청 사이버범죄 신고(www.police.go.kr) 또는 112</li><li><strong>스마트폰 초기화</strong>: 악성 앱 완전 제거를 위해 초기화 권장</li></ol>"),
            ("스미싱 예방 앱 추천", "<table><thead><tr><th>앱</th><th>특징</th><th>가격</th></tr></thead><tbody><tr><td>후후 (KT)</td><td>스팸 문자 자동 차단, 발신자 정보</td><td>무료</td></tr><tr><td>T전화 (SKT)</td><td>스팸 필터링, 기업 발신 정보</td><td>무료 (SKT)</td></tr><tr><td>V3 Mobile</td><td>악성 앱 탐지, 스미싱 URL 차단</td><td>무료</td></tr><tr><td>카카오 보호나무</td><td>스미싱 링크 실시간 차단</td><td>무료</td></tr></tbody></table>"),
        ],
        "faq": [
            ("스미싱 링크를 클릭했는데 아무것도 안 했으면 괜찮나요?", "링크 클릭만으로 악성코드가 설치될 수 있습니다. 즉시 <strong>모바일 백신으로 검사</strong>하고, 최근 설치된 앱 목록을 확인하세요."),
            ("스미싱으로 돈을 이체했을 때 돌려받을 수 있나요?", "즉시 은행에 연락하면 <strong>지급정지</strong>를 통해 환급받을 수 있는 경우가 있습니다. 빠른 신고가 핵심입니다. 금융감독원(1332)에도 신고하세요."),
            ("통신사에서 스미싱을 차단해줄 수 있나요?", "<strong>SKT, KT, LG U+</strong> 모두 스팸 문자 필터링 서비스를 무료로 제공합니다. 통신사 앱이나 고객센터에서 활성화하세요."),
        ],
        "ctas": [
            {"text": "후후 스팸 차단 앱 다운로드", "desc": "스팸 문자를 자동 차단하는 후후 앱을 받으세요", "url": "https://www.whowho.co.kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "금융감독원 보이스피싱 신고센터", "desc": "피해 발생 시 즉시 금융감독원 1332로 신고하세요", "url": "https://www.fss.or.kr/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "경찰청 사이버범죄 신고하기", "desc": "경찰청 사이버수사국에 스미싱 피해를 신고하세요", "url": "https://ecrm.police.go.kr/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "2단계 인증 설정 방법 구글 네이버 카카오 총정리 2026",
        "cat": 5,
        "slug": "two-factor-authentication-guide-2026",
        "intro": "비밀번호가 유출되어도 계정을 지킬 수 있는 <strong>2단계 인증(2FA)</strong>. 구글, 네이버, 카카오 계정에 2단계 인증을 설정하는 방법을 단계별로 안내합니다. 5분이면 충분한 가장 효과적인 보안 조치입니다.",
        "sections": [
            ("2단계 인증(2FA)이란?", "<p>비밀번호(1단계) 외에 <strong>추가 인증 수단(2단계)</strong>을 요구하는 보안 방식입니다.</p><table><thead><tr><th>2FA 방식</th><th>보안 수준</th><th>편의성</th><th>특징</th></tr></thead><tbody><tr><td>SMS 문자 인증</td><td>중</td><td>높음</td><td>SIM 스와핑 취약</td></tr><tr><td>인증 앱 (TOTP)</td><td>높음</td><td>중</td><td>Google Authenticator, Authy</td></tr><tr><td>하드웨어 키 (YubiKey)</td><td>최상</td><td>낮음</td><td>물리적 보안 키</td></tr><tr><td>생체 인증</td><td>높음</td><td>높음</td><td>얼굴, 지문 인식</td></tr></tbody></table>"),
            ("구글 계정 2단계 인증 설정법", "<ol><li>myaccount.google.com 접속</li><li>보안 탭 클릭</li><li>'Google에 로그인' > '2단계 인증' 클릭</li><li>'시작하기' 클릭 후 비밀번호 확인</li><li>인증 방법 선택: <strong>Google 메시지(추천)</strong>, 인증 앱, SMS 중 선택</li><li>백업 코드 10개 저장 (분실 시 복구용)</li></ol><p>추천: <strong>Google Prompt</strong> (스마트폰에 '로그인 확인' 팝업이 뜨는 방식)가 가장 편리합니다.</p>"),
            ("네이버 계정 2단계 인증 설정법", "<ol><li>네이버 로그인 > 내 정보 > 보안 설정</li><li>'2단계 인증' 클릭</li><li>인증 수단 선택: 네이버 OTP 앱, 보안 SMS</li><li><strong>네이버 OTP 앱 설치</strong> 후 QR코드 스캔</li><li>6자리 OTP 코드 입력하여 설정 완료</li></ol>"),
            ("카카오 계정 2단계 인증 설정법", "<ol><li>카카오톡 > 설정 > 개인·보안 > 카카오계정</li><li>'2단계 인증 설정' 터치</li><li>인증 방법: 카카오톡 앱 인증 또는 SMS 선택</li><li>설정 완료 후 로그인 시마다 추가 인증 요구</li></ol>"),
            ("추천 인증 앱 비교", "<ul><li><strong>Google Authenticator</strong>: 구글 계정 연동, 기기 이전 가능 (백업 기능)</li><li><strong>Authy</strong>: 멀티 기기 지원, 백업 기능, 가장 편리</li><li><strong>Microsoft Authenticator</strong>: 마이크로소프트 계정 최적화, 푸시 알림</li></ul>"),
        ],
        "faq": [
            ("2단계 인증 앱 설치 기기를 분실하면 어떻게 되나요?", "미리 <strong>백업 코드를 저장</strong>해두세요. 구글은 10개의 백업 코드를 제공합니다. Authy는 클라우드 백업으로 기기 변경 시에도 복구 가능합니다."),
            ("2단계 인증을 설정하면 매번 인증해야 하나요?", "신뢰하는 기기로 등록하면 <strong>30일 또는 무기한 인증 생략</strong>이 가능합니다. 새 기기나 새 브라우저에서 로그인할 때만 인증이 요구됩니다."),
            ("SMS 인증과 앱 인증 중 무엇이 더 안전한가요?", "<strong>앱 인증(TOTP)이 더 안전합니다</strong>. SMS는 SIM 스와핑(휴대폰 번호 탈취) 공격에 취약합니다."),
        ],
        "ctas": [
            {"text": "구글 계정 보안 설정하기", "desc": "구글 계정 보안 설정에서 2단계 인증을 켜세요", "url": "https://myaccount.google.com/security", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "Authy 인증 앱 다운로드", "desc": "가장 편리한 2FA 앱 Authy를 지금 다운로드하세요", "url": "https://authy.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "네이버 보안 설정 바로가기", "desc": "네이버 계정 2단계 인증을 지금 설정하세요", "url": "https://nid.naver.com/user2/help/secureMain", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "개인정보 유출 확인 방법 조회 사이트 대처법 2026",
        "cat": 5,
        "slug": "personal-data-breach-check-2026",
        "intro": "내 이메일, 비밀번호가 이미 유출되었을 수 있습니다. <strong>개인정보 유출 여부를 확인</strong>하는 방법과, 유출이 확인된 경우의 단계별 대처법을 안내합니다.",
        "sections": [
            ("개인정보 유출 확인 사이트 TOP 4", "<h3>1. Have I Been Pwned (haveibeenpwned.com)</h3><p>이메일 주소를 입력하면 <strong>전 세계 데이터 유출 사고에 포함되었는지</strong> 즉시 확인할 수 있습니다. 75억 개 이상의 유출 계정 데이터베이스를 보유. 완전 무료.</p><h3>2. Firefox Monitor</h3><p>Mozilla Firefox에서 운영. Have I Been Pwned와 연동되며, 이메일 알림 서비스 제공.</p><h3>3. 한국인터넷진흥원 (KISA) 개인정보 침해신고센터</h3><p>국내 개인정보 유출 신고 및 피해 상담. 국내 기업의 개인정보 유출 사고 확인 가능.</p><h3>4. 카카오 디지털 보안검사</h3><p>카카오계정 기준 개인정보 유출 여부 알림 서비스.</p>"),
            ("유출이 확인됐을 때 대처법 (단계별)", "<ol><li><strong>해당 사이트 비밀번호 즉시 변경</strong>: 유출된 비밀번호와 같은 것을 사용하는 모든 사이트</li><li><strong>같은 비밀번호 사용 사이트 전체 변경</strong>: 비밀번호 재사용이 가장 위험</li><li><strong>2단계 인증 활성화</strong>: 이메일, 금융, 소셜미디어 계정 필수</li><li><strong>금융 계정 모니터링</strong>: 이상 거래 내역 확인, 은행 알림 서비스 등록</li><li><strong>신용카드 번호 유출 시</strong>: 해당 카드 즉시 정지 및 재발급 요청</li></ol>"),
            ("개인정보 유출 예방법", "<ul><li><strong>사이트별 다른 비밀번호</strong>: 비밀번호 관리자(Bitwarden) 활용</li><li><strong>정기적 비밀번호 변경</strong>: 중요 계정은 6개월마다 변경</li><li><strong>이메일 주소 분리</strong>: 중요 계정용, 가입용 이메일 분리</li><li><strong>Have I Been Pwned 모니터링</strong>: 이메일 등록 시 유출 즉시 알림</li></ul>"),
        ],
        "faq": [
            ("Have I Been Pwned에서 유출이 확인되면 바로 위험한가요?", "유출 시점이 오래됐다면 이미 비밀번호를 변경한 경우 안전할 수 있습니다. <strong>유출 항목(이메일, 비밀번호, 전화번호 등)을 확인</strong>하고, 해당 정보를 여전히 사용 중이면 즉시 변경하세요."),
            ("주민번호, 전화번호가 유출되면 어떻게 하나요?", "주민번호 유출은 <strong>KISA 개인정보 침해신고센터(privacy.kisa.or.kr)</strong>에 신고하세요. 명의도용 방지 서비스(명의보호원)에도 등록을 추천합니다."),
        ],
        "ctas": [
            {"text": "Have I Been Pwned 유출 확인", "desc": "내 이메일이 데이터 유출에 포함됐는지 무료로 확인하세요", "url": "https://haveibeenpwned.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "KISA 개인정보 침해신고", "desc": "한국인터넷진흥원에 개인정보 유출 피해를 신고하세요", "url": "https://privacy.kisa.or.kr/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "Bitwarden으로 비밀번호 관리", "desc": "유출 방지를 위해 비밀번호 관리자를 지금 시작하세요", "url": "https://bitwarden.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "공공 와이파이 안전하게 사용하는 방법 보안 팁 2026",
        "cat": 5,
        "slug": "public-wifi-security-guide-2026",
        "intro": "카페, 공항, 지하철의 <strong>무료 공공 와이파이</strong>는 편리하지만 해킹 위험이 있습니다. 중간자 공격(MITM), 가짜 핫스팟, 패킷 스니핑으로부터 내 데이터를 지키는 방법을 안내합니다.",
        "sections": [
            ("공공 와이파이의 위험성", "<ul><li><strong>중간자 공격(MITM)</strong>: 해커가 내 통신을 중간에서 가로채 개인정보 탈취</li><li><strong>가짜 핫스팟</strong>: 'Starbucks_Free', 'Airport_WiFi' 같은 가짜 AP를 만들어 접속 유도</li><li><strong>패킷 스니핑</strong>: 같은 네트워크 내 트래픽을 도청</li><li><strong>악성 앱 배포</strong>: 소프트웨어 업데이트를 가장한 악성코드 설치</li></ul>"),
            ("공공 와이파이 안전 사용 7가지 팁", "<ol><li><strong>HTTPS 사이트만 접속</strong>: 주소창에 자물쇠 아이콘이 있는 HTTPS 사이트만 이용하세요.</li><li><strong>VPN 사용 (핵심)</strong>: 모든 트래픽을 암호화하여 중간자 공격 방지. 무료 VPN보다 유료 신뢰 VPN 추천.</li><li><strong>자동 접속 비활성화</strong>: 스마트폰 Wi-Fi 자동 접속을 꺼두고 필요할 때만 연결.</li><li><strong>금융 거래 자제</strong>: 인터넷뱅킹, 신용카드 결제는 공공 Wi-Fi에서 절대 금지.</li><li><strong>공식 네트워크 확인</strong>: 매장 직원에게 정확한 SSID(와이파이 이름)를 확인하세요.</li><li><strong>파일 공유 끄기</strong>: 설정 > 공유에서 파일 공유, AirDrop을 끄세요.</li><li><strong>사용 후 즉시 연결 해제</strong>: 사용이 끝나면 와이파이에서 연결을 끊으세요.</li></ol>"),
            ("VPN 서비스 추천", "<table><thead><tr><th>VPN</th><th>가격</th><th>속도</th><th>개인정보 정책</th></tr></thead><tbody><tr><td>ExpressVPN</td><td>월 6.67달러~</td><td>최상</td><td>노로그 정책</td></tr><tr><td>NordVPN</td><td>월 3.99달러~</td><td>상</td><td>노로그, 감사 완료</td></tr><tr><td>ProtonVPN</td><td>무료/월 4달러~</td><td>중상</td><td>오픈소스, 스위스</td></tr></tbody></table>"),
        ],
        "faq": [
            ("VPN을 사용하면 완전히 안전한가요?", "VPN은 네트워크 도청을 막아주지만, <strong>피싱 사이트, 악성 앱</strong> 등은 별도로 주의해야 합니다. VPN + 백신 + 안전한 브라우징 습관을 함께 유지하세요."),
            ("무료 VPN을 사용해도 되나요?", "<strong>무료 VPN은 오히려 위험할 수 있습니다</strong>. 일부 무료 VPN은 사용자 데이터를 수집·판매합니다. ProtonVPN 무료 버전처럼 신뢰할 수 있는 오픈소스 서비스를 선택하세요."),
            ("공공 와이파이에서 인터넷뱅킹이 위험한 이유는?", "HTTPS를 사용해도 인증서 위조 공격(SSL Stripping)에 취약할 수 있습니다. <strong>금융 거래는 반드시 모바일 데이터(LTE/5G)</strong>를 사용하세요."),
        ],
        "ctas": [
            {"text": "NordVPN 최저가 구매하기", "desc": "공공 와이파이 보안을 위한 NordVPN을 시작하세요", "url": "https://nordvpn.com/ko/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "ProtonVPN 무료로 시작하기", "desc": "무료 VPN 중 가장 신뢰할 수 있는 ProtonVPN", "url": "https://protonvpn.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "ExpressVPN 30일 환불 보장", "desc": "ExpressVPN 30일 환불 보장으로 위험 없이 체험하세요", "url": "https://www.expressvpn.com/kr/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "스마트폰 해킹 확인 방법 증상 예방 조치 총정리 2026",
        "cat": 5,
        "slug": "smartphone-hacking-check-guide-2026",
        "intro": "내 스마트폰이 해킹당했을 수도 있습니다. <strong>배터리 방전이 빠르고, 데이터 사용량이 급증하고, 낯선 앱이 설치</strong>됐다면 해킹 의심 증상일 수 있습니다. 스마트폰 해킹 증상 10가지와 확인·예방·대처 방법을 총정리합니다.",
        "sections": [
            ("스마트폰 해킹 의심 증상 10가지", "<ol><li><strong>배터리 과방전</strong>: 백그라운드 악성 앱이 지속 실행되어 배터리 소모 급증</li><li><strong>데이터 사용량 급증</strong>: 악성 앱이 개인정보를 외부로 전송</li><li><strong>발열</strong>: 비정상적인 프로세스 실행으로 폰이 뜨거움</li><li><strong>모르는 앱 설치</strong>: 동의 없이 앱이 설치됨</li><li><strong>이상한 팝업</strong>: 광고, 경고 팝업이 지속적으로 표시</li><li><strong>느린 속도</strong>: 악성 프로세스로 전반적으로 느려짐</li><li><strong>모르는 발신 내역</strong>: 본인이 하지 않은 전화·문자 발신</li><li><strong>소액결제 내역</strong>: 동의하지 않은 결제가 발생</li><li><strong>잠금화면 변경</strong>: 기존 비밀번호가 작동 안 됨</li><li><strong>카메라/마이크 무단 활성화</strong>: 사용 중이 아닌데 표시등 켜짐</li></ol>"),
            ("해킹 여부 확인 방법", "<h3>Android</h3><ul><li>설정 > 앱 > 모든 앱 확인 (모르는 앱 확인)</li><li>설정 > 배터리 > 배터리 사용량 (비정상 앱 확인)</li><li>설정 > 데이터 사용 > 앱별 데이터 확인</li><li>Google Play Protect 스캔 실행</li></ul><h3>iPhone</h3><ul><li>설정 > 개인정보 보호 및 보안 > 앱 권한 확인</li><li>설정 > 배터리 > 앱별 사용량 확인</li><li>탈옥(Jailbreak) 여부 확인 (Cydia 앱 존재 여부)</li></ul>"),
            ("해킹 대처 및 예방법", "<h3>즉시 대처</h3><ol><li>의심 앱 즉시 삭제</li><li>비밀번호 전체 변경 (PC에서)</li><li>2FA 활성화</li><li>공장 초기화 (완전 제거)</li></ol><h3>예방법 7가지</h3><ul><li><strong>공식 앱스토어만</strong> 사용 (Play Store, App Store)</li><li>알 수 없는 출처 앱 설치 비허용</li><li>OS 및 앱 최신 업데이트 유지</li><li>공공 와이파이에서 VPN 사용</li><li>화면 잠금(PIN, 생체인식) 설정</li><li>정기적 보안 업데이트 확인</li><li>모바일 백신 설치(V3 Mobile, 알약M)</li></ul>"),
        ],
        "faq": [
            ("아이폰은 안드로이드보다 해킹에 강한가요?", "아이폰은 <strong>iOS 샌드박스 구조와 앱 심사 정책</strong>으로 악성 앱 설치가 훨씬 어렵습니다. 단, 탈옥(Jailbreak) 시 보안이 크게 약화됩니다."),
            ("스마트폰을 공장 초기화하면 해킹 앱이 제거되나요?", "<strong>네, 공장 초기화가 가장 확실한 방법</strong>입니다. 단, 클라우드 백업에 악성 앱이 포함되지 않도록 신선 설치를 권장합니다."),
            ("스파이앱(스토킹앱)이 설치됐는지 확인하는 방법은?", "안드로이드: 설정 > 접근성 > 다운로드한 앱 확인. 비정상적인 접근성 권한을 가진 앱 삭제. <strong>공장 초기화가 가장 확실한 해결책</strong>입니다."),
        ],
        "ctas": [
            {"text": "V3 Mobile 모바일 백신 다운로드", "desc": "안랩 V3 모바일 백신으로 스마트폰을 보호하세요", "url": "https://www.ahnlab.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "KISA 사이버침해 대응센터", "desc": "사이버 해킹 피해를 KISA에 신고하세요", "url": "https://www.kisa.or.kr/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "구글 Play Protect 스캔하기", "desc": "Google Play Protect로 지금 바로 보안 검사를 하세요", "url": "https://play.google.com/intl/ko/about/play-protect/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "광고 추적 차단하는 방법 브라우저 설정 확장 프로그램 2026",
        "cat": 5,
        "slug": "ad-tracking-block-guide-2026",
        "intro": "온라인에서 여러분의 <strong>모든 행동이 추적</strong>되고 있습니다. 광고 추적을 차단하면 프라이버시 보호는 물론 페이지 로딩 속도도 빨라집니다. 2026년 브라우저별 설정법과 최고의 광고 차단 확장 프로그램을 안내합니다.",
        "sections": [
            ("광고 추적 원리 이해하기", "<ul><li><strong>쿠키(Cookie)</strong>: 방문 사이트에서 저장하는 작은 파일. 재방문 시 행동 추적.</li><li><strong>핑거프린팅</strong>: 브라우저·기기 정보 조합으로 쿠키 없이도 개인 식별</li><li><strong>픽셀 추적</strong>: 이미지에 숨겨진 1×1픽셀로 이메일·사이트 방문 추적</li><li><strong>크로스사이트 추적</strong>: 다른 사이트에서의 행동을 구글·페이스북 등이 추적</li></ul>"),
            ("브라우저별 광고 차단 설정", "<h3>Chrome</h3><ul><li>설정 > 개인정보 및 보안 > 쿠키 및 기타 사이트 데이터 > 서드파티 쿠키 차단</li><li>설정 > 광고 > '광고 주제 기반' 끄기</li></ul><h3>Firefox</h3><ul><li>설정 > 개인정보 및 보안 > 향상된 추적 차단 > '엄격' 선택</li><li>Firefox 기본으로 광고 추적 차단 기능 내장</li></ul><h3>Safari</h3><ul><li>설정 > Safari > '크로스 사이트 추적 방지' 켜기</li><li>지능형 추적 방지(ITP) 기본 활성화</li></ul>"),
            ("최고의 광고 차단 확장 프로그램", "<table><thead><tr><th>확장 프로그램</th><th>차단 성능</th><th>속도 향상</th><th>가격</th><th>특징</th></tr></thead><tbody><tr><td>uBlock Origin</td><td>최상</td><td>최상</td><td>무료</td><td>오픈소스, 최강 차단</td></tr><tr><td>AdGuard</td><td>최상</td><td>상</td><td>무료/유료</td><td>앱 수준 차단, 모바일</td></tr><tr><td>Privacy Badger (EFF)</td><td>상</td><td>중상</td><td>무료</td><td>추적 학습형, EFF 개발</td></tr><tr><td>Ghostery</td><td>상</td><td>중상</td><td>무료</td><td>트래커 시각화</td></tr></tbody></table><p><strong>추천 조합</strong>: uBlock Origin + Privacy Badger</p>"),
            ("모바일에서 광고 차단하기", "<h3>Android</h3><ul><li><strong>Brave 브라우저</strong>: 기본 광고 차단 내장, 빠른 속도</li><li><strong>AdGuard 앱</strong>: 전체 시스템 광고 차단 (루팅 불필요)</li></ul><h3>iPhone</h3><ul><li><strong>Safari 콘텐츠 차단기</strong>: 앱스토어에서 '1Blocker' 또는 'AdGuard' 설치</li><li><strong>Brave 브라우저</strong>: iOS에서도 광고 차단 내장</li></ul>"),
        ],
        "faq": [
            ("광고 차단기를 쓰면 사이트 이용이 제한되나요?", "일부 언론사, 유튜브 등은 광고 차단기 감지 후 이용을 제한합니다. <strong>화이트리스트에 해당 사이트를 추가</strong>하거나, 해당 사이트는 광고를 허용하는 방식으로 대응하세요."),
            ("VPN과 광고 차단기를 함께 써도 되나요?", "네, 함께 사용하면 더욱 강력한 프라이버시 보호가 됩니다. <strong>NordVPN, ExpressVPN</strong> 등은 자체 광고 차단 기능도 포함하고 있습니다."),
            ("구글 크롬에서 광고 차단 확장이 제한된다는데?", "구글이 Manifest V3로 확장 API를 변경하면서 일부 차단 기능이 제한될 수 있습니다. <strong>Firefox + uBlock Origin</strong> 조합이 광고 차단에서 더 강력합니다."),
        ],
        "ctas": [
            {"text": "uBlock Origin 무료 설치", "desc": "최강의 무료 광고 차단기 uBlock Origin을 설치하세요", "url": "https://ublockorigin.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "Brave 브라우저 다운로드", "desc": "광고 차단 내장 Brave 브라우저로 속도와 보안을 잡으세요", "url": "https://brave.com/ko/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "AdGuard 모바일 앱 다운로드", "desc": "AdGuard로 모바일 전체 광고를 차단하세요", "url": "https://adguard.com/ko/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "랜섬웨어 예방 방법 감염 시 대처법 총정리 2026",
        "cat": 5,
        "slug": "ransomware-prevention-guide-2026",
        "intro": "랜섬웨어는 파일을 암호화하고 돈을 요구하는 <strong>가장 위험한 사이버 공격</strong>입니다. 2026년에도 기업과 개인을 대상으로 한 랜섬웨어 공격이 지속되고 있습니다. 예방법 7가지와 감염 시 단계별 대처법을 정리합니다.",
        "sections": [
            ("랜섬웨어란? 감염 경로 5가지", "<p>랜섬웨어(Ransomware)는 피해자의 파일을 암호화한 뒤 복호화 키를 빌미로 <strong>비트코인 등 암호화폐를 요구</strong>하는 악성코드입니다.</p><h3>주요 감염 경로</h3><ol><li><strong>이메일 첨부파일</strong>: 송장, 이력서, 계약서로 위장한 악성 첨부파일</li><li><strong>피싱 URL 클릭</strong>: 가짜 사이트에서 드라이브바이 다운로드</li><li><strong>불법 소프트웨어</strong>: 크랙, 키젠 프로그램에 포함</li><li><strong>원격 데스크톱(RDP) 취약점</strong>: 약한 비밀번호, 미패치 취약점</li><li><strong>USB 드라이브</strong>: 악성 코드가 담긴 USB 연결</li></ol>"),
            ("랜섬웨어 예방법 7가지", "<ol><li><strong>정기 백업 (3-2-1 법칙)</strong>: 3개 복사본, 2가지 다른 매체, 1개 오프사이트 보관. 백업이 가장 중요!</li><li><strong>OS 및 소프트웨어 즉시 업데이트</strong>: WannaCry는 패치된 취약점을 악용. 자동 업데이트 항상 켜두기.</li><li><strong>이메일 첨부파일 주의</strong>: 알 수 없는 발신자의 첨부파일(.exe, .js, .docm) 절대 열지 말 것.</li><li><strong>RDP 보안 강화</strong>: 사용하지 않으면 비활성화. 사용 시 강력한 비밀번호 + 2FA.</li><li><strong>불법 소프트웨어 금지</strong>: 크랙, 키젠 절대 사용 금지.</li><li><strong>최신 백신 유지</strong>: 실시간 보호 활성화, 정의 업데이트 자동화.</li><li><strong>사용자 교육</strong>: 의심스러운 링크·첨부파일 클릭 금지 교육.</li></ol>"),
            ("랜섬웨어 감염 시 대처법", "<ol><li><strong>즉시 네트워크 차단</strong>: LAN 케이블 뽑기, Wi-Fi 끄기 (추가 확산 방지)</li><li><strong>감염 PC 격리</strong>: 다른 기기와 네트워크 완전 차단</li><li><strong>복호화 키 검색</strong>: NoMoreRansom.org에서 무료 복호화 도구 검색</li><li><strong>전원 끄지 말 것</strong>: 일부 랜섬웨어는 전원을 끄면 더 많은 파일을 암호화</li><li><strong>경찰 신고</strong>: 사이버범죄 신고 (www.police.go.kr)</li><li><strong>절대 몸값 지불 금지</strong>: 돈을 줘도 복호화해주지 않는 경우 많음</li><li><strong>전문 업체 상담</strong>: 보안 전문 업체에 복구 가능성 확인</li></ol>"),
            ("3-2-1 백업 전략 가이드", "<p>랜섬웨어 대응의 핵심은 <strong>오프라인 백업</strong>입니다.</p><ul><li><strong>3</strong>: 데이터의 3개 복사본 유지 (원본 + 백업 2개)</li><li><strong>2</strong>: 2가지 다른 저장 매체 (PC + 외장하드, 또는 PC + NAS)</li><li><strong>1</strong>: 1개는 오프사이트 보관 (다른 장소 또는 클라우드)</li></ul><p>랜섬웨어는 연결된 드라이브까지 암호화합니다. <strong>백업 후 외장하드를 분리</strong>해두는 것이 핵심입니다.</p>"),
        ],
        "faq": [
            ("랜섬웨어에 걸리면 파일을 복구할 수 있나요?", "백업이 없다면 매우 어렵습니다. <strong>NoMoreRansom.org</strong>에서 무료 복호화 도구를 먼저 검색하세요. 없다면 전문 복구 업체에 의뢰하거나, 백업 없이는 복구가 불가능한 경우도 많습니다."),
            ("몸값을 지불하면 파일을 돌려받을 수 있나요?", "지불해도 복호화 키를 주지 않는 경우가 많습니다. <strong>절대 몸값 지불을 권장하지 않습니다</strong>. 지불하면 재공격 대상이 될 가능성도 높습니다."),
            ("Windows Defender가 랜섬웨어를 막아주나요?", "Windows Defender 내 <strong>제어된 폴더 액세스</strong> 기능을 활성화하면 랜섬웨어의 파일 암호화를 차단할 수 있습니다. 설정 > Windows 보안 > 바이러스 및 위협 방지 > 랜섬웨어 방지에서 켜세요."),
        ],
        "ctas": [
            {"text": "NoMoreRansom 무료 복호화 도구", "desc": "랜섬웨어 무료 복호화 도구를 NoMoreRansom에서 찾으세요", "url": "https://www.nomoreransom.org/ko/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "외장 SSD로 오프라인 백업 시작", "desc": "랜섬웨어로부터 데이터를 보호하는 오프라인 백업을 시작하세요", "url": "https://www.danawa.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "경찰청 사이버범죄 신고하기", "desc": "랜섬웨어 피해를 경찰청 사이버수사국에 신고하세요", "url": "https://ecrm.police.go.kr/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
]

POSTS += [
    # ===== 활용 가이드/팁 (38-50) =====
    {
        "title": "윈도우 11 최적화 설정 방법 느린 PC 빠르게 만들기 2026",
        "cat": 5,
        "slug": "windows-11-optimization-guide-2026",
        "intro": "새 컴퓨터를 샀는데 시간이 지나면서 느려지거나, 처음부터 느린 PC를 사용하고 계신가요? <strong>윈도우 11 최적화</strong>만 제대로 해도 체감 속도가 크게 향상됩니다. 시작프로그램 정리부터 SSD 최적화까지 실제로 효과 있는 방법만 정리합니다.",
        "sections": [
            ("시작프로그램 정리 (가장 효과적)", "<p>부팅 시 자동으로 실행되는 프로그램을 줄이는 것이 <strong>가장 효과적인 속도 향상</strong> 방법입니다.</p><h3>설정 방법</h3><ol><li>Ctrl+Shift+Esc → 작업 관리자 실행</li><li>'시작 프로그램' 탭 클릭</li><li>불필요한 항목 선택 후 '사용 안 함' 클릭</li></ol><h3>비활성화 추천 항목</h3><ul><li>카카오톡, 라인, 슬랙 (필요 시 직접 실행)</li><li>Adobe Update, Creative Cloud</li><li>OneDrive (클라우드 동기화 불필요 시)</li><li>Xbox Game Bar (게임 미사용 시)</li></ul>"),
            ("불필요한 효과 및 애니메이션 끄기", "<ol><li>Win+R → sysdm.cpl 입력</li><li>고급 탭 → 성능 설정</li><li>'최적 성능에 맞게 조정' 선택 또는 개별 항목 해제</li></ol><p>특히 <strong>RAM 8GB 이하 저사양 PC</strong>에서 효과가 큽니다.</p>"),
            ("불필요한 서비스 및 앱 제거", "<h3>Windows 11 불필요한 내장 앱 제거</h3><ul><li>설정 > 앱 > 설치된 앱에서 제거</li><li>Xbox, Mixed Reality Portal, 3D 뷰어 등 미사용 앱 제거</li></ul><h3>불필요한 서비스 비활성화</h3><ul><li>Win+R → services.msc</li><li>Fax, Print Spooler(프린터 미사용 시), Bluetooth(미사용 시) 비활성화</li></ul>"),
            ("SSD 최적화 설정", "<ul><li><strong>TRIM 활성화 확인</strong>: 관리자 CMD → fsutil behavior query DisableDeleteNotify (0이면 정상)</li><li><strong>디스크 조각 모음 끄기</strong>: SSD는 조각 모음이 오히려 수명 단축. Windows 11은 자동으로 SSD에 조각 모음을 비활성화.</li><li><strong>가상 메모리</strong>: RAM 16GB 이상이면 가상 메모리 최소화 가능</li><li><strong>전원 옵션</strong>: 설정 > 전원 > '고성능' 또는 '균형' 선택</li></ul>"),
            ("메모리 관리 최적화", "<table><thead><tr><th>RAM 용량</th><th>상태</th><th>권장 조치</th></tr></thead><tbody><tr><td>4GB</td><td>매우 부족</td><td>8GB로 업그레이드 강력 권장</td></tr><tr><td>8GB</td><td>기본</td><td>효과 최적화 끄기, 브라우저 탭 최소화</td></tr><tr><td>16GB</td><td>충분</td><td>추가 최적화 불필요</td></tr><tr><td>32GB+</td><td>여유</td><td>가상 메모리 비활성화 가능</td></tr></tbody></table>"),
        ],
        "faq": [
            ("윈도우 11이 윈도우 10보다 더 느린가요?", "같은 사양에서 Windows 11은 더 많은 리소스를 사용합니다. <strong>RAM 8GB 이하라면 Windows 10이 더 빠릅니다</strong>. Windows 11 최적을 위해서는 RAM 16GB를 권장합니다."),
            ("PC 최적화 프로그램(클리너)을 써도 되나요?", "CCleaner 같은 청소 프로그램은 레지스트리 수정이 오히려 문제를 일으킬 수 있습니다. <strong>Windows 기본 도구(디스크 정리, 저장소 센스)</strong>를 사용하세요."),
            ("게이밍 PC 최적화 방법이 따로 있나요?", "게임 모드 켜기(설정 > 게임 > 게임 모드), NVIDIA/AMD 드라이버 최신화, 고성능 전원 계획 선택이 효과적입니다. <strong>백그라운드 앱 최소화</strong>가 FPS 향상에 가장 직접적입니다."),
        ],
        "ctas": [
            {"text": "윈도우 11 공식 최적화 가이드", "desc": "마이크로소프트 공식 PC 성능 최적화 가이드를 확인하세요", "url": "https://support.microsoft.com/ko-kr/windows/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "RAM 업그레이드 최저가 찾기", "desc": "다나와에서 PC RAM 업그레이드 최저가를 비교하세요", "url": "https://www.danawa.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "SSD 업그레이드로 PC 속도 향상", "desc": "HDD를 SSD로 교체하면 부팅 속도가 10배 빨라집니다", "url": "https://www.coupang.com/np/search?q=SSD", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "컴퓨터 포맷 윈도우 재설치 방법 초보자 가이드 2026",
        "cat": 5,
        "slug": "windows-reinstall-guide-2026",
        "intro": "PC가 너무 느려지거나 오류가 계속 발생한다면 <strong>윈도우 재설치(포맷)</strong>가 근본 해결책입니다. 처음 해보시는 분도 따라할 수 있는 단계별 가이드입니다. 백업부터 드라이버 설치, 필수 프로그램까지 완벽히 안내합니다.",
        "sections": [
            ("포맷 전 반드시 백업할 것들", "<h3>체크리스트</h3><ul><li>바탕화면, 문서, 다운로드 폴더 전체</li><li>브라우저 북마크 (크롬: 설정 > 북마크 내보내기)</li><li>이메일 프로그램 데이터</li><li>게임 세이브 파일 (게임별 폴더 확인)</li><li>포토샵 등 설정 파일</li><li>인증서, 공인인증서</li><li>윈도우 정품 키 (슬라이 소프트웨어로 확인)</li></ul><p>백업 장소: 외장하드, USB, 구글 드라이브, OneDrive</p>"),
            ("USB 부팅디스크 만드는 방법", "<ol><li><strong>8GB 이상 USB</strong> 준비</li><li>마이크로소프트 공식 사이트에서 <strong>미디어 생성 도구(Media Creation Tool)</strong> 다운로드</li><li>도구 실행 > '다른 PC용 설치 미디어 만들기' 선택</li><li>USB 드라이브 선택 > 다운로드 및 생성 (15~30분 소요)</li></ol>"),
            ("윈도우 설치 단계별 가이드", "<ol><li>USB 삽입 후 PC 재시작</li><li>BIOS/UEFI 진입 (제조사별 F2, F12, Del 키)</li><li>부팅 순서를 USB로 변경</li><li>윈도우 설치 화면 진입</li><li>'지금 설치' > 제품 키 입력 (또는 '제품 키 없음')</li><li>설치 형식: <strong>'사용자 지정: Windows만 설치(고급)'</strong> 선택</li><li>기존 파티션 삭제 후 새로 파티션 생성 및 설치</li><li>설치 완료 후 초기 설정 (계정, 언어 등)</li></ol>"),
            ("재설치 후 필수 드라이버 및 프로그램", "<h3>드라이버 설치 순서</h3><ol><li>칩셋 드라이버 (메인보드 제조사 사이트)</li><li>그래픽 드라이버 (NVIDIA/AMD 공식)</li><li>네트워크 드라이버 (인터넷 연결용)</li><li>오디오 드라이버</li></ol><h3>필수 프로그램 목록</h3><ul><li>브라우저: Chrome 또는 Firefox</li><li>보안: Windows Defender (기본), Malwarebytes</li><li>압축: 반디집 또는 7-Zip</li><li>미디어: 팟플레이어, VLC</li><li>오피스: MS Office 또는 LibreOffice</li><li>뷰어: 알PDF 또는 Adobe Reader</li></ul>"),
        ],
        "faq": [
            ("포맷하면 윈도우 라이선스가 사라지나요?", "디지털 라이선스(마이크로소프트 계정 연결)라면 <strong>재설치 후 자동으로 인증</strong>됩니다. 스티커 제품 키는 미리 기록해두세요."),
            ("포맷 없이 윈도우를 초기화하는 방법이 있나요?", "설정 > 시스템 > 복구 > '<strong>이 PC 초기화</strong>'를 사용하면 포맷 없이 초기화 가능합니다. '내 파일 유지' 옵션을 선택하면 개인 파일은 보존됩니다."),
            ("설치 시 파티션을 어떻게 나눠야 하나요?", "간단히 C 드라이브 하나로 사용하는 것을 추천합니다. 데이터 보관용 D 드라이브를 따로 두려면 설치 시 파티션 분할이 가능합니다."),
        ],
        "ctas": [
            {"text": "윈도우 11 미디어 생성 도구 다운로드", "desc": "마이크로소프트 공식 사이트에서 설치 USB를 만드세요", "url": "https://www.microsoft.com/ko-kr/software-download/windows11", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "포맷용 USB 최저가 구매", "desc": "8GB 이상 USB를 다나와에서 최저가로 구매하세요", "url": "https://www.danawa.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "외장하드로 백업 시작하기", "desc": "포맷 전 중요한 파일을 외장하드에 백업하세요", "url": "https://www.coupang.com/np/search?q=외장하드", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "스마트폰 저장 공간 부족 해결 방법 정리 팁 2026",
        "cat": 5,
        "slug": "smartphone-storage-cleanup-guide-2026",
        "intro": "스마트폰 저장공간이 꽉 찼다는 알림이 뜨면서 앱이 정상 작동하지 않거나 사진이 저장이 안 되는 경험을 하셨나요? <strong>추가 비용 없이 스마트폰 용량을 확보</strong>하는 실용적인 방법을 정리합니다.",
        "sections": [
            ("저장 공간 점유율 확인 방법", "<h3>Android (갤럭시 기준)</h3><p>설정 > 배터리 및 디바이스 케어 > 저장공간</p><h3>iPhone</h3><p>설정 > 일반 > iPhone 저장공간</p><p>항목별로 용량을 차지하는 순서를 확인한 후 큰 항목부터 정리하세요.</p>"),
            ("가장 효과적인 용량 확보 방법", "<h3>1. 사진·동영상 클라우드 이전</h3><p><strong>Google Photos</strong>(무제한 백업 후 기기 사진 삭제) 또는 <strong>iCloud</strong>(최적화된 저장공간)을 활용하면 수 GB를 즉시 확보할 수 있습니다.</p><h3>2. 캐시 삭제</h3><p>Android: 설정 > 앱 관리 > 각 앱 > 캐시 삭제. 카카오톡, 인스타그램 등 SNS 앱의 캐시가 수백 MB~GB까지 쌓입니다.</p><h3>3. 사용하지 않는 앱 삭제</h3><p>6개월 이상 실행하지 않은 앱은 과감히 삭제하세요.</p><h3>4. 대용량 파일 확인</h3><p>Android: 파일 앱 > 저장공간 분석 > 대용량 파일 확인. 다운로드 폴더에 불필요한 파일이 많을 수 있습니다.</p><h3>5. WhatsApp·카카오톡 미디어 정리</h3><p>채팅 앱에서 받은 이미지, 영상이 자동 저장되어 용량을 많이 차지합니다.</p>"),
            ("마이크로SD 카드 활용 (Android)", "<p>삼성 갤럭시 일부 모델은 microSD 카드 슬롯을 지원합니다. <strong>Samsung Pro Plus 512GB microSD</strong> (약 8만원)로 사진·동영상을 외부 저장소로 이전하세요.</p><ul><li>호환 모델 확인: 갤럭시 A 시리즈 일부, S 시리즈 구형</li><li>주의: 갤럭시 S23 이후 마이크로SD 슬롯 제거됨</li></ul>"),
            ("클라우드 서비스 활용 전략", "<table><thead><tr><th>서비스</th><th>무료 용량</th><th>사진 자동 백업</th><th>삭제 후 용량 확보</th></tr></thead><tbody><tr><td>Google Photos</td><td>15GB</td><td>O</td><td>O (기기에서 삭제)</td></tr><tr><td>iCloud</td><td>5GB</td><td>O (iPhone)</td><td>O (최적화 설정)</td></tr><tr><td>네이버 MYBOX</td><td>30GB</td><td>O (앱 설치)</td><td>O</td></tr><tr><td>OneDrive</td><td>5GB</td><td>O</td><td>O</td></tr></tbody></table>"),
        ],
        "faq": [
            ("아이폰 저장공간 빠르게 확보하는 가장 좋은 방법은?", "설정 > 일반 > iPhone 저장공간에서 '<strong>대화 동영상 삭제, 메시지 전달</strong>' 및 '앱 오프로드'를 활성화하세요. iCloud 사진 '최적화된 저장공간'도 효과적입니다."),
            ("카카오톡 사진이 왜 이렇게 용량을 많이 차지하나요?", "카카오톡은 받은 모든 이미지를 기기에 저장합니다. 카카오톡 설정 > 채팅 > 미디어 파일 저장 > 저장 안 함으로 변경하고, 기존 파일은 <strong>카카오톡 > 설정 > 개인/보안 > 저장 공간 관리</strong>에서 삭제하세요."),
            ("삭제한 사진이 복구될까요?", "삭제 후 30일간 사진 휴지통에 보관됩니다. 완전 삭제하려면 <strong>사진 앱 > 최근 삭제된 항목 > 모두 삭제</strong>를 실행하세요."),
        ],
        "ctas": [
            {"text": "Google Photos 무제한 백업 시작", "desc": "Google Photos로 사진을 백업하고 기기 용량을 확보하세요", "url": "https://photos.google.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "네이버 MYBOX 30GB 무료", "desc": "네이버 MYBOX로 사진과 파일을 무료로 백업하세요", "url": "https://mybox.naver.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "microSD 카드 최저가 구매", "desc": "갤럭시 저장공간 확장용 microSD 카드를 구매하세요", "url": "https://www.coupang.com/np/search?q=microSD", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "아이폰 vs 갤럭시 비교 2026 기종 변경 시 알아야 할 것",
        "cat": 5,
        "slug": "iphone-vs-galaxy-comparison-2026",
        "intro": "아이폰에서 갤럭시로, 또는 갤럭시에서 아이폰으로 <strong>기종 변경</strong>을 고민 중이신가요? 2026년 최신 iPhone 17과 Galaxy S25를 기준으로 스펙, OS 차이, 생태계, 데이터 이전 방법을 총비교합니다.",
        "sections": [
            ("iPhone 17 vs Galaxy S25 스펙 비교", "<table><thead><tr><th>항목</th><th>iPhone 17 Pro</th><th>Galaxy S25 Ultra</th></tr></thead><tbody><tr><td>출시가</td><td>155만원~</td><td>179만원~</td></tr><tr><td>AP</td><td>Apple A19 Pro</td><td>Snapdragon 8 Elite</td></tr><tr><td>RAM</td><td>8GB</td><td>12GB</td></tr><tr><td>카메라 (메인)</td><td>48MP + 12MP + 12MP</td><td>200MP + 50MP + 10MP + 50MP</td></tr><tr><td>배터리</td><td>약 3,500mAh</td><td>5,000mAh</td></tr><tr><td>충전</td><td>30W 유선, MagSafe 무선</td><td>45W 유선, 15W 무선</td></tr><tr><td>OS</td><td>iOS 19</td><td>Android 15 (One UI 7)</td></tr><tr><td>S펜</td><td>없음</td><td>내장</td></tr></tbody></table>"),
            ("iOS vs Android 핵심 차이점", "<h3>iOS의 장점</h3><ul><li>5~6년 이상 OS 업데이트 지원</li><li>앱 품질과 보안 심사가 엄격</li><li>애플 생태계(맥북, 에어팟, 애플워치) 연동 탁월</li><li>게임 성능(Metal API)</li></ul><h3>Android(One UI)의 장점</h3><ul><li>파일 관리 자유로움 (USB 연결 파일 이동)</li><li>앱 설치 자유도 (APK 직접 설치)</li><li>커스터마이징 (위젯, 런처 변경)</li><li>S-Pen, DeX(외부 모니터 연결) 등 특화 기능</li></ul>"),
            ("생태계 비교", "<table><thead><tr><th>구분</th><th>애플 생태계</th><th>삼성/구글 생태계</th></tr></thead><tbody><tr><td>이어폰</td><td>AirPods (자동 연결, 공간음향)</td><td>Galaxy Buds</td></tr><tr><td>스마트워치</td><td>Apple Watch</td><td>Galaxy Watch</td></tr><tr><td>노트북</td><td>MacBook (AirDrop, Handoff)</td><td>갤럭시북 (Phone Link, Galaxy AI)</td></tr><tr><td>태블릿</td><td>iPad (사이드카, 유니버설 컨트롤)</td><td>Galaxy Tab (DeX, Multi Control)</td></tr></tbody></table>"),
            ("기종 변경 시 데이터 이전 방법", "<h3>갤럭시 → 아이폰</h3><ol><li>iPhone 초기 설정 시 '안드로이드에서 데이터 이전' 선택</li><li>Android에서 <strong>iPhone으로 이동 앱</strong> 설치</li><li>연락처, 사진, 앱 목록 자동 이전 (일부 앱은 재설치 필요)</li></ol><h3>아이폰 → 갤럭시</h3><ol><li>Galaxy 초기 설정 시 '이전 기기에서 데이터 이전' 선택</li><li><strong>Smart Switch</strong> 앱으로 연락처, 사진, 메시지 이전</li><li>단, 아이메시지, iCloud 앱 데이터는 이전 불가</li></ol>"),
        ],
        "faq": [
            ("아이폰에서 갤럭시로 바꾸면 데이터가 다 사라지나요?", "연락처, 사진, 일정은 <strong>Samsung Smart Switch</strong>로 이전 가능합니다. 단, 앱별 데이터(카톡 채팅 백업 포함)는 별도로 백업 후 복원해야 합니다."),
            ("아이폰과 갤럭시 카메라는 어떻게 다른가요?", "아이폰은 <strong>자연스러운 색감과 영상 품질</strong>이 탁월하고, 갤럭시는 <strong>200MP 고해상도와 망원 줌</strong>이 강점입니다. 사진가에게는 갤럭시 S25 Ultra, 영상 크리에이터에게는 iPhone이 유리합니다."),
            ("갤럭시 S25와 아이폰 17 중 어떤 것이 더 가성비가 좋나요?", "AS 기간, 중고 가격 유지율을 고려하면 <strong>아이폰이 장기적으로 더 가성비가 좋습니다</strong>. 다만 기능 다양성은 갤럭시가 앞섭니다."),
        ],
        "ctas": [
            {"text": "아이폰 17 공식몰 구매", "desc": "애플 공식몰에서 iPhone 17 최신 모델을 확인하세요", "url": "https://www.apple.com/kr/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "갤럭시 S25 공식몰 구매", "desc": "삼성 공식몰에서 Galaxy S25 Ultra를 확인하세요", "url": "https://www.samsung.com/sec/smartphones/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "스마트폰 최저가 비교하기", "desc": "다나와에서 최신 스마트폰 전 모델 최저가를 비교하세요", "url": "https://www.danawa.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "듀얼 모니터 설정 방법 연결 활용 팁 총정리 2026",
        "cat": 5,
        "slug": "dual-monitor-setup-guide-2026",
        "intro": "모니터 하나를 추가하는 것만으로 <strong>생산성이 20~40% 향상</strong>된다는 연구 결과가 있습니다. HDMI, DisplayPort, USB-C로 연결하는 방법부터 Windows·Mac 설정, 유용한 활용 팁까지 완벽 가이드를 제공합니다.",
        "sections": [
            ("듀얼 모니터 연결 방법", "<table><thead><tr><th>연결 방식</th><th>최대 해상도/주사율</th><th>특징</th></tr></thead><tbody><tr><td>HDMI 2.0</td><td>4K 60Hz</td><td>가장 보편적, TV·모니터 모두 지원</td></tr><tr><td>HDMI 2.1</td><td>4K 144Hz / 8K 30Hz</td><td>최신 그래픽카드 지원</td></tr><tr><td>DisplayPort 1.4</td><td>4K 144Hz</td><td>게이밍, daisy chain 지원</td></tr><tr><td>USB-C (Thunderbolt 4)</td><td>4K 120Hz</td><td>노트북, 맥북 연결 최적</td></tr><tr><td>VGA</td><td>최대 1080p 60Hz</td><td>구형, 아날로그 신호</td></tr></tbody></table>"),
            ("Windows 11 듀얼 모니터 설정", "<ol><li>Win+P 단축키 → 디스플레이 확장 선택</li><li>설정 > 시스템 > 디스플레이에서 모니터 배치 조정</li><li>주 모니터 설정: 원하는 모니터 선택 > '주 디스플레이로 만들기'</li><li>각 모니터별 해상도, 주사율, 배율 개별 설정 가능</li></ol>"),
            ("Mac 듀얼 모니터 설정", "<ol><li>시스템 설정 > 디스플레이</li><li>배열 탭에서 모니터 위치 조정</li><li>메뉴 막대를 표시할 모니터 선택</li><li>MacBook Air M2 이하: 외장 모니터 1개만 지원</li><li>MacBook Pro M3 이상: 외장 모니터 최대 3개 지원</li></ol>"),
            ("듀얼 모니터 생산성 활용 팁 7가지", "<ol><li><strong>주 모니터 = 작업, 보조 모니터 = 참고</strong>: 코딩 시 주 모니터에 편집기, 보조에 문서·브라우저</li><li><strong>FancyZones(Windows) 활용</strong>: 화면을 원하는 레이아웃으로 분할</li><li><strong>가로+세로 배치</strong>: 보조 모니터를 90도 회전하면 문서 읽기 편리</li><li><strong>다른 해상도 조합</strong>: 32인치 QHD(주) + 27인치 FHD(보조) 조합도 훌륭</li><li><strong>모니터 암 사용</strong>: 책상 공간 확보, 높이·각도 자유 조절</li><li><strong>비디오 컨퍼런스</strong>: 주 모니터에 자료, 보조에 화상회의 화면</li><li><strong>스트리밍 방송</strong>: 주 모니터에 게임, 보조에 채팅·OBS</li></ol>"),
        ],
        "faq": [
            ("노트북에 외장 모니터를 연결할 수 있나요?", "USB-C(Thunderbolt), HDMI, DisplayPort 포트가 있으면 가능합니다. 포트가 없다면 <strong>USB-C 허브나 독(Dock)</strong>을 사용하세요."),
            ("두 모니터 해상도가 달라도 괜찮나요?", "다른 해상도를 사용해도 Windows·Mac이 자동으로 처리합니다. 단, <strong>배율(DPI 스케일링)을 각각 설정</strong>해야 텍스트 크기가 자연스럽습니다."),
            ("그래픽카드 없이 듀얼 모니터가 가능한가요?", "내장 그래픽(Intel UHD, AMD Radeon)도 대부분 <strong>최소 2개의 외부 출력</strong>을 지원합니다. 노트북은 포트 수에 따라 제한됩니다."),
        ],
        "ctas": [
            {"text": "27인치 QHD 모니터 최저가 구매", "desc": "듀얼 모니터용 27인치 QHD 모니터를 다나와에서 비교하세요", "url": "https://www.danawa.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "모니터 암 최저가 구매", "desc": "쿠팡에서 듀얼 모니터 암을 로켓배송으로 받으세요", "url": "https://www.coupang.com/np/search?q=모니터암", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "USB-C 허브로 모니터 연결하기", "desc": "노트북 듀얼 모니터용 USB-C 허브를 확인하세요", "url": "https://www.coupang.com/np/search?q=USB-C허브", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "크롬 확장 프로그램 추천 생산성 필수 TOP 10 2026",
        "cat": 5,
        "slug": "chrome-extension-recommendation-2026",
        "intro": "크롬 확장 프로그램 하나가 하루 업무 시간을 1시간씩 단축할 수 있습니다. <strong>생산성, 보안, 쇼핑, 개발자용</strong>까지 2026년 반드시 설치해야 할 크롬 확장 프로그램 TOP 10을 소개합니다.",
        "sections": [
            ("생산성 확장 프로그램 TOP 4", "<h3>1. Notion Web Clipper</h3><p>웹페이지를 노션에 바로 저장. 나중에 읽기, 리서치 자료 수집에 필수.</p><h3>2. Todoist for Chrome</h3><p>웹서핑 중 할 일이 생기면 즉시 투두리스트에 추가. 생산성 극대화.</p><h3>3. Clockify Time Tracker</h3><p>프리랜서, 재택근무자에게 필수. 프로젝트별 시간 추적을 자동화.</p><h3>4. OneTab</h3><p>열려있는 탭을 모두 리스트로 저장. 메모리 사용량을 95% 줄임. 탭 과다 사용자 필수."),
            ("보안/프라이버시 확장 프로그램 TOP 3", "<h3>5. uBlock Origin</h3><p>가장 효율적인 광고 차단기. 페이지 로딩 속도 향상, 프라이버시 보호. 필수 설치.</p><h3>6. Bitwarden</h3><p>비밀번호 관리자. 사이트별 다른 비밀번호를 자동 생성·저장·입력.</p><h3>7. Privacy Badger (EFF)</h3><p>광고 추적기를 자동 학습하여 차단. EFF(전자프런티어재단) 개발, 신뢰도 높음.</p>"),
            ("개발자 필수 확장 TOP 2", "<h3>8. Wappalyzer</h3><p>방문 중인 사이트의 기술 스택(프레임워크, CMS, 서버 등)을 즉시 분석. 경쟁사 기술 파악.</p><h3>9. JSON Viewer</h3><p>브라우저에서 JSON을 색상 구분, 접기/펼치기로 보기 좋게 표시.</p>"),
            ("쇼핑 절약 확장 TOP 2", "<h3>10. Honey (PayPal)</h3><p>온라인 쇼핑 시 자동으로 쿠폰 코드를 적용해주는 절약 도우미. 쿠팡, 이마트몰, 해외 쇼핑에서도 동작.</p><h3>보너스: Keepa (아마존)</h3><p>아마존 상품의 가격 히스토리를 차트로 표시. 진짜 할인인지 판별 가능.</p>"),
        ],
        "faq": [
            ("크롬 확장 프로그램이 너무 많으면 브라우저가 느려지나요?", "확장 프로그램은 각각 메모리를 사용합니다. <strong>10개 이하</strong>로 유지하고, 자주 사용하지 않는 것은 비활성화하세요. OneTab이 탭과 메모리를 줄이는 데 도움이 됩니다."),
            ("확장 프로그램 설치는 안전한가요?", "Chrome 웹스토어의 공식 확장만 설치하고, <strong>권한 요청을 확인</strong>하세요. 필요 이상의 권한(모든 사이트 데이터 읽기 등)을 요구하면 설치를 재고하세요."),
            ("크롬 확장이 파이어폭스에서도 사용 가능한가요?", "대부분의 주요 확장은 Firefox 버전이 따로 있습니다. uBlock Origin, Bitwarden은 Firefox에서도 완벽하게 작동합니다."),
        ],
        "ctas": [
            {"text": "크롬 웹스토어 바로가기", "desc": "크롬 웹스토어에서 추천 확장 프로그램을 설치하세요", "url": "https://chrome.google.com/webstore/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "uBlock Origin 설치하기", "desc": "최강의 무료 광고 차단기를 지금 설치하세요", "url": "https://chrome.google.com/webstore/detail/ublock-origin/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "Bitwarden 비밀번호 관리자 설치", "desc": "Bitwarden으로 모든 비밀번호를 안전하게 관리하세요", "url": "https://bitwarden.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "윈도우 단축키 모음 업무 효율 높이는 필수 단축키 50선 2026",
        "cat": 5,
        "slug": "windows-keyboard-shortcuts-2026",
        "intro": "마우스 없이 키보드만으로 모든 작업을 처리할 수 있다면? <strong>윈도우 단축키</strong>를 완전히 익히면 업무 속도가 30% 이상 향상됩니다. 기본부터 고급까지, 꼭 알아야 할 필수 단축키 50가지를 정리했습니다.",
        "sections": [
            ("기본 필수 단축키 20선", "<table><thead><tr><th>단축키</th><th>기능</th></tr></thead><tbody><tr><td>Win+D</td><td>바탕화면 표시/숨기기</td></tr><tr><td>Win+E</td><td>파일 탐색기 열기</td></tr><tr><td>Win+L</td><td>화면 잠금</td></tr><tr><td>Win+R</td><td>실행 창 열기</td></tr><tr><td>Win+I</td><td>설정 열기</td></tr><tr><td>Win+S</td><td>검색 열기</td></tr><tr><td>Alt+F4</td><td>창 닫기 / 종료</td></tr><tr><td>Alt+Tab</td><td>앱 전환</td></tr><tr><td>Ctrl+Z</td><td>실행 취소</td></tr><tr><td>Ctrl+Y</td><td>다시 실행</td></tr><tr><td>Ctrl+A</td><td>전체 선택</td></tr><tr><td>Ctrl+C / V / X</td><td>복사 / 붙여넣기 / 잘라내기</td></tr><tr><td>Ctrl+F</td><td>찾기</td></tr><tr><td>Ctrl+H</td><td>찾아 바꾸기</td></tr><tr><td>Ctrl+P</td><td>인쇄</td></tr><tr><td>Ctrl+S</td><td>저장</td></tr><tr><td>Ctrl+W</td><td>탭/창 닫기</td></tr><tr><td>Ctrl+T</td><td>새 탭 열기</td></tr><tr><td>Ctrl+Shift+T</td><td>닫은 탭 다시 열기</td></tr><tr><td>F2</td><td>파일명 변경</td></tr></tbody></table>"),
            ("창 관리 및 가상 데스크톱 단축키", "<table><thead><tr><th>단축키</th><th>기능</th></tr></thead><tbody><tr><td>Win+←/→</td><td>창을 화면 좌/우 절반으로 스냅</td></tr><tr><td>Win+↑/↓</td><td>창 최대화/최소화</td></tr><tr><td>Win+Ctrl+D</td><td>새 가상 데스크톱 만들기</td></tr><tr><td>Win+Ctrl+←/→</td><td>가상 데스크톱 전환</td></tr><tr><td>Win+Ctrl+F4</td><td>현재 가상 데스크톱 닫기</td></tr><tr><td>Win+Tab</td><td>작업 보기 (타임라인)</td></tr></tbody></table>"),
            ("스크린샷 단축키 총정리", "<table><thead><tr><th>단축키</th><th>기능</th></tr></thead><tbody><tr><td>PrtSc</td><td>전체 화면 캡처 (클립보드)</td></tr><tr><td>Win+PrtSc</td><td>전체 화면 캡처 후 자동 저장</td></tr><tr><td>Win+Shift+S</td><td>영역 선택 캡처 (Snipping Tool)</td></tr><tr><td>Alt+PrtSc</td><td>현재 창만 캡처</td></tr><tr><td>Win+G</td><td>Xbox Game Bar (게임 녹화)</td></tr></tbody></table>"),
            ("브라우저 및 파일 탐색기 단축키", "<table><thead><tr><th>단축키</th><th>기능</th></tr></thead><tbody><tr><td>Ctrl+L</td><td>주소창으로 이동</td></tr><tr><td>Ctrl+D</td><td>즐겨찾기 추가</td></tr><tr><td>Ctrl+Shift+N</td><td>시크릿/InPrivate 창 열기</td></tr><tr><td>Ctrl+1~8</td><td>해당 번호 탭으로 이동</td></tr><tr><td>Ctrl+9</td><td>마지막 탭으로 이동</td></tr><tr><td>Ctrl+Shift+Del</td><td>검색 기록 삭제</td></tr><tr><td>Alt+←/→</td><td>이전/다음 페이지</td></tr></tbody></table>"),
        ],
        "faq": [
            ("단축키를 빨리 외우는 방법이 있나요?", "하루에 3~5개씩 의식적으로 사용하면 1~2주 안에 자연스럽게 익힙니다. <strong>가장 자주 하는 작업의 단축키부터</strong> 시작하세요. 포스트잇에 적어 모니터에 붙여두는 것도 효과적입니다."),
            ("Mac에서도 비슷한 단축키를 사용할 수 있나요?", "대부분 <strong>Ctrl → Cmd(Command)</strong>로 대체됩니다. Ctrl+C → Cmd+C, Ctrl+V → Cmd+V 등. Alt는 Option 키로 대응합니다."),
            ("단축키가 작동하지 않을 때는?", "키보드 언어가 영문인지 확인하세요(한/영 전환). 또는 다른 프로그램이 단축키를 사용 중일 수 있습니다. <strong>관리자 권한</strong>으로 실행해야 작동하는 단축키도 있습니다."),
        ],
        "ctas": [
            {"text": "마이크로소프트 공식 단축키 목록", "desc": "윈도우 공식 전체 단축키 목록을 확인하세요", "url": "https://support.microsoft.com/ko-kr/windows/keyboard-shortcuts-in-windows", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "생산성 키보드 추천 구매", "desc": "단축키 사용에 최적화된 기계식 키보드를 구매하세요", "url": "https://www.danawa.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "PowerToys로 단축키 커스터마이징", "desc": "Microsoft PowerToys로 윈도우 단축키를 자유롭게 설정하세요", "url": "https://learn.microsoft.com/ko-kr/windows/powertoys/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "구글 드라이브 200% 활용법 공유 백업 협업 팁 2026",
        "cat": 5,
        "slug": "google-drive-tips-guide-2026",
        "intro": "15GB 무료 용량에 Google Docs, Sheets, Slides까지 포함된 <strong>구글 드라이브</strong>는 세상에서 가장 강력한 무료 클라우드 서비스 중 하나입니다. 대부분이 모르는 고급 기능과 활용 팁을 소개합니다.",
        "sections": [
            ("구글 드라이브 핵심 기능 총정리", "<ul><li><strong>Google Docs</strong>: 워드 대체 문서 편집 (오프라인도 가능)</li><li><strong>Google Sheets</strong>: 엑셀 대체 스프레드시트</li><li><strong>Google Slides</strong>: 파워포인트 대체 프레젠테이션</li><li><strong>Google Forms</strong>: 설문지, 퀴즈 무료 제작</li><li><strong>실시간 공동 편집</strong>: 여러 명이 동시에 같은 문서 작업</li><li><strong>버전 기록</strong>: 과거 버전 복구 가능</li></ul>"),
            ("알면 유용한 고급 기능 10가지", "<ol><li><strong>오프라인 사용</strong>: 크롬 확장 'Google Docs Offline' 설치 시 인터넷 없이 편집</li><li><strong>검색 연산자</strong>: type:pdf, owner:나 등 정교한 파일 검색</li><li><strong>파일 OCR</strong>: PDF·이미지를 드라이브에 올리면 Google Docs로 열어 텍스트 추출 (무료 OCR)</li><li><strong>공유 만료 날짜 설정</strong>: 특정 날짜 이후 공유 링크 자동 만료</li><li><strong>드라이브 바로 가기</strong>: 파일을 복제하지 않고 여러 폴더에 바로 가기 추가</li><li><strong>AI 기능</strong>: Gemini AI로 문서 요약, 내용 생성</li><li><strong>서명 기능</strong>: Google Docs에서 직접 전자서명</li><li><strong>폼 자동화</strong>: 설문 응답을 Sheets에 자동 수집</li></ol>"),
            ("구글 드라이브 보안 설정", "<ul><li><strong>공유 권한 설정</strong>: 보기 전용 / 댓글 / 편집 세밀하게 제어</li><li><strong>다운로드 방지</strong>: 뷰어가 다운로드·인쇄·복사를 못하게 제한</li><li><strong>도메인 제한</strong>: 특정 회사 도메인(@company.com)만 접근 허용</li><li><strong>링크 만료</strong>: 공유 링크에 유효 기간 설정</li></ul>"),
        ],
        "faq": [
            ("구글 드라이브 15GB를 다 썼는데 어떻게 하나요?", "Google One 100GB (월 2,900원)으로 업그레이드하거나, <strong>Gmail 스팸·대용량 첨부파일 삭제</strong>, Google Photos 사진 품질 최적화로 용량을 확보하세요."),
            ("구글 드라이브 파일을 실수로 삭제했어요", "휴지통에 <strong>30일간 보관</strong>됩니다. 드라이브 > 휴지통에서 복구하세요. 30일 이후라도 Google 고객지원에 문의하면 복구 가능한 경우가 있습니다."),
            ("MS Office 파일을 구글 드라이브에서 열 수 있나요?", "네, .docx, .xlsx, .pptx 파일을 드라이브에 올리면 Google Docs/Sheets/Slides로 바로 편집할 수 있습니다. 저장 시 <strong>원본 Office 형식 유지</strong>도 가능합니다."),
        ],
        "ctas": [
            {"text": "구글 드라이브 시작하기", "desc": "Google Drive 15GB 무료 저장공간을 지금 사용하세요", "url": "https://drive.google.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "Google One 100GB 업그레이드", "desc": "월 2,900원으로 구글 드라이브를 100GB로 늘리세요", "url": "https://one.google.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "Google Workspace 팀 협업 시작", "desc": "팀을 위한 Google Workspace로 협업 효율을 높이세요", "url": "https://workspace.google.com/intl/ko/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "유튜브 프리미엄 가격 기능 우회 없이 할인받는 방법 2026",
        "cat": 5,
        "slug": "youtube-premium-guide-2026",
        "intro": "유튜브 광고가 너무 많아 지쳐있다면 <strong>유튜브 프리미엄</strong>이 해결책입니다. 월 14,900원이 부담스럽다면 학생 할인, 가족 요금제, 공식적인 할인 방법을 통해 더 저렴하게 이용하는 방법을 안내합니다.",
        "sections": [
            ("유튜브 프리미엄 요금제 비교 2026", "<table><thead><tr><th>요금제</th><th>가격</th><th>인원</th><th>특징</th></tr></thead><tbody><tr><td>개인</td><td>월 14,900원</td><td>1명</td><td>광고 제거, 오프라인, 백그라운드</td></tr><tr><td>학생</td><td>월 7,900원</td><td>1명</td><td>재학 증명 필요, 1년 갱신</td></tr><tr><td>가족</td><td>월 22,900원</td><td>최대 6명</td><td>인당 3,800원, 가성비 최고</td></tr></tbody></table>"),
            ("유튜브 프리미엄 기능 총정리", "<ul><li><strong>광고 제거</strong>: 모든 동영상에서 광고 완전 제거 (핵심 기능)</li><li><strong>백그라운드 재생</strong>: 화면 꺼진 상태에서도 음악·강의 계속 재생</li><li><strong>오프라인 다운로드</strong>: 동영상을 다운로드해서 인터넷 없이 시청</li><li><strong>유튜브 뮤직 포함</strong>: 별도 구독 필요 없이 유튜브 뮤직 무료 포함</li><li><strong>유튜브 Kids 포함</strong>: 자녀용 광고 없는 동영상 이용</li></ul>"),
            ("공식적으로 할인받는 방법", "<h3>1. 학생 할인 (월 7,900원)</h3><p>대학교 재학생이라면 SheerID 인증을 통해 50% 할인된 가격으로 이용 가능합니다.</p><h3>2. 가족 요금제 공유 (인당 3,800원)</h3><p>가족 6명이 공유하면 개인 요금의 4분의 1 가격입니다. 같은 주소에 사는 가족이 아니어도 이용 가능.</p><h3>3. 구글 One 번들</h3><p>Google One 프리미엄 요금제와 유튜브 프리미엄이 번들로 제공되는 프로모션을 주기적으로 확인하세요.</p><h3>4. 통신사 제휴 혜택</h3><p>SKT, KT, LG U+ 통신 요금제에 따라 유튜브 프리미엄이 포함되어 있을 수 있습니다.</p>"),
        ],
        "faq": [
            ("유튜브 프리미엄 없이 광고를 차단할 수 있나요?", "uBlock Origin 확장 프로그램으로 PC 브라우저에서는 광고를 차단할 수 있습니다. 단, <strong>유튜브가 광고 차단기를 감지하고 재생을 막는</strong> 경우가 늘고 있습니다. 백그라운드 재생, 오프라인 기능은 프리미엄만 가능합니다."),
            ("유튜브 프리미엄을 해지하면 어떻게 되나요?", "결제 기간이 끝나는 날까지는 이용 가능합니다. 다운로드한 영상은 <strong>해지 후 29일 이내</strong>에 온라인 확인이 필요하며, 이후 시청 불가합니다."),
            ("가족 요금제는 한 집에 살아야 하나요?", "구글 가족 그룹은 <strong>같은 가정에 사는 구성원</strong>을 대상으로 하지만, 실제 운영에서는 유연하게 적용됩니다. 가족 관리자의 국가와 같아야 합니다."),
        ],
        "ctas": [
            {"text": "유튜브 프리미엄 시작하기", "desc": "유튜브 프리미엄 1개월 무료 체험을 시작하세요", "url": "https://www.youtube.com/premium", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "유튜브 학생 할인 신청하기", "desc": "대학생이라면 월 7,900원 학생 요금제로 가입하세요", "url": "https://www.youtube.com/premium/student", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "유튜브 가족 요금제 시작하기", "desc": "가족 6명 공유로 인당 3,800원에 유튜브 프리미엄을 사용하세요", "url": "https://www.youtube.com/premium/family", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "스마트홈 입문 가이드 2026 AI 스피커 IoT 기기 추천",
        "cat": 5,
        "slug": "smart-home-beginner-guide-2026",
        "intro": "스마트폰 하나로 집 안의 모든 기기를 제어하는 <strong>스마트홈</strong>. 2026년에는 진입 장벽이 크게 낮아져 월 5만원 미만으로 스마트홈을 구축할 수 있습니다. AI 스피커 비교부터 추천 IoT 기기, 설치 가이드까지 총정리합니다.",
        "sections": [
            ("AI 스피커 비교 2026", "<table><thead><tr><th>스피커</th><th>가격</th><th>AI 어시스턴트</th><th>음질</th><th>스마트홈 호환</th></tr></thead><tbody><tr><td>카카오 미니 링크</td><td>8만원</td><td>카카오 i</td><td>중</td><td>카카오홈 기기</td></tr><tr><td>클로바 도크</td><td>9만원</td><td>클로바 (네이버)</td><td>중상</td><td>LG ThinQ, 삼성SmartThings</td></tr><tr><td>Google Nest Audio</td><td>12만원</td><td>Google Assistant</td><td>상</td><td>Google Home 생태계</td></tr><tr><td>Amazon Echo (4세대)</td><td>11만원</td><td>Alexa</td><td>중상</td><td>Matter, Zigbee</td></tr><tr><td>Apple HomePod mini</td><td>12만원</td><td>Siri</td><td>상</td><td>HomeKit (Apple 생태계)</td></tr></tbody></table>"),
            ("추천 스마트홈 IoT 기기 입문 패키지", "<h3>월 5만원 이하 입문 패키지</h3><ul><li><strong>스마트 플러그</strong>: 2~3만원. 기존 가전을 스마트하게. 에너지 모니터링 포함.</li><li><strong>스마트 전구 (필립스 Hue / Govee)</strong>: 1~3만원. 앱으로 색상·밝기 조절.</li><li><strong>스마트 스위치</strong>: 2~4만원. 기존 조명 스위치를 교체, 앱 제어.</li></ul><h3>5~15만원 중급 패키지</h3><ul><li><strong>스마트 도어락</strong>: 10~30만원. 삼성SDS, 게이트맨, 아이레보.</li><li><strong>스마트 온도계·공기청정기</strong>: 샤오미 생태계 기기들이 가성비 탁월.</li><li><strong>CCTV/홈캠</strong>: 다후아, 샤오미 등 3~10만원.</li></ul>"),
            ("스마트홈 플랫폼 선택 가이드", "<p>스마트홈 기기들은 플랫폼에 따라 호환성이 다릅니다.</p><ul><li><strong>Google Home</strong>: 가장 넓은 기기 호환성, 안드로이드 사용자 최적</li><li><strong>Apple HomeKit</strong>: 아이폰 사용자 최적, 보안 강점, 기기 제한적</li><li><strong>Amazon Alexa</strong>: 글로벌 기기 생태계 최강, 국내 지원 제한</li><li><strong>Matter 표준</strong>: 2024년부터 구글·애플·아마존 공통 지원하는 통합 표준</li><li><strong>삼성 SmartThings</strong>: 삼성 가전과 완벽 연동</li></ul>"),
            ("스마트홈 보안 주의사항", "<ul><li><strong>기기별 비밀번호 변경</strong>: 기본 비밀번호는 해킹에 취약합니다</li><li><strong>펌웨어 업데이트</strong>: 보안 취약점 패치를 위해 항상 최신 업데이트</li><li><strong>별도 게스트 WiFi</strong>: IoT 기기를 메인 네트워크와 분리</li><li><strong>중국산 저가 카메라 주의</strong>: 클라우드 서버 위치, 개인정보 처리 방침 확인</li></ul>"),
        ],
        "faq": [
            ("스마트홈 입문에 AI 스피커가 필수인가요?", "AI 스피커 없이도 스마트폰 앱으로 모든 기기를 제어할 수 있습니다. 단, <strong>음성 제어</strong>의 편리함은 생활을 크게 바꿔줍니다."),
            ("스마트홈 기기 설치가 어렵지 않나요?", "스마트 플러그, 스마트 전구는 <strong>기존 가전에 연결만 하면</strong> 됩니다. 스마트 스위치나 도어락은 전기 공사가 필요할 수 있어 전문가 시공을 권장합니다."),
            ("인터넷이 끊기면 스마트홈 기기가 작동을 안 하나요?", "클라우드 의존 기기는 인터넷 없이 작동 안 합니다. <strong>로컬 처리 가능한 기기(Matter, Zigbee)</strong>나 홈 어시스턴트(Home Assistant) 같은 로컬 서버를 구축하면 인터넷 없이도 작동합니다."),
        ],
        "ctas": [
            {"text": "카카오 미니 공식몰 구매", "desc": "카카오 AI 스피커로 스마트홈을 시작하세요", "url": "https://kakaostore.kakao.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "쿠팡 스마트홈 기기 특가", "desc": "스마트 플러그, 전구, 스위치 특가를 확인하세요", "url": "https://www.coupang.com/np/search?q=스마트홈", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "Google Nest Audio 구매하기", "desc": "Google Home 스마트홈 생태계를 Google Nest로 시작하세요", "url": "https://store.google.com/kr/category/speakers", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "QR코드 만들기 무료 생성 사이트 활용법 총정리 2026",
        "cat": 5,
        "slug": "qr-code-generator-guide-2026",
        "intro": "명함, 메뉴판, 전단지에 <strong>QR코드</strong>를 추가하면 오프라인에서 온라인으로 고객을 쉽게 안내할 수 있습니다. 무료 QR코드 생성 사이트, 디자인 QR코드, 다이내믹 QR코드까지 2026년 완벽 가이드를 제공합니다.",
        "sections": [
            ("QR코드 종류 비교", "<table><thead><tr><th>종류</th><th>특징</th><th>수정 가능</th><th>통계</th></tr></thead><tbody><tr><td>정적(Static) QR</td><td>URL이 QR 내부에 고정</td><td>X</td><td>X</td></tr><tr><td>동적(Dynamic) QR</td><td>URL을 나중에 변경 가능</td><td>O</td><td>O (스캔 수, 기기)</td></tr></tbody></table><p><strong>명함, 인쇄물에는 동적 QR코드</strong>가 유리합니다. URL이 바뀌어도 QR코드를 재인쇄할 필요가 없습니다.</p>"),
            ("무료 QR코드 생성 사이트 TOP 5", "<h3>1. QR Code Generator (qr-code-generator.com)</h3><p>정적 QR코드를 완전 무료로 생성. URL, 텍스트, 전화번호, 이메일 등 다양한 형식 지원.</p><h3>2. QR Tiger (qrcode-tiger.com)</h3><p>동적 QR코드 기본 제공, 색상·로고 커스터마이징. 무료 플랜은 3개 동적 QR 생성.</p><h3>3. Bitly</h3><p>URL 단축 + QR코드 생성. 무료 플랜으로 10개 QR 생성, 스캔 통계 제공.</p><h3>4. 네이버 QR코드</h3><p>네이버 플레이스, 네이버 예약과 연동. 국내 사용자에게 친숙한 인터페이스.</p><h3>5. Canva QR코드 생성기</h3><p>디자인 작업과 동시에 QR코드를 삽입. 명함, 포스터 제작 시 편리.</p>"),
            ("QR코드 활용법 비즈니스 사례", "<h3>식당·카페</h3><ul><li>테이블 QR코드로 모바일 메뉴 제공 (종이 메뉴판 절약)</li><li>리뷰 작성 링크 → 구글 지도, 네이버 플레이스</li></ul><h3>소매점</h3><ul><li>인스타그램, 네이버 스마트스토어 링크</li><li>제품 상세 정보, 사용 설명서 링크</li></ul><h3>명함</h3><ul><li>링크드인, 포트폴리오 사이트 링크</li><li>vCard(연락처 파일) 직접 저장</li></ul>"),
            ("디자인 QR코드 만드는 법", "<p>일반 검은색 QR코드 대신 브랜드 색상과 로고가 들어간 디자인 QR코드를 만들 수 있습니다.</p><ul><li>로고 중앙 삽입: 전체 QR의 30% 이하 크기로 로고 삽입 가능</li><li>색상 변경: 배경색과 전경색 변경 (명암 대비 유지 필수)</li><li>모서리 모양: 둥근 모서리, 다양한 패턴 적용</li></ul><p><strong>주의</strong>: 디자인을 너무 복잡하게 변경하면 스캔이 안 될 수 있습니다. 반드시 여러 기기에서 테스트하세요.</p>"),
        ],
        "faq": [
            ("QR코드를 인쇄할 때 최소 크기는?", "일반 스마트폰으로 스캔하려면 <strong>최소 2.5cm × 2.5cm</strong> 이상이어야 합니다. 멀리서 스캔할수록 더 크게 인쇄하세요."),
            ("QR코드 유효기간이 있나요?", "정적 QR코드는 영구적입니다. 동적 QR코드는 <strong>서비스 사용 여부에 따라</strong> 만료될 수 있습니다. 무료 서비스는 일정 기간 후 만료되는 경우가 있으니 중요한 용도에는 유료 서비스를 추천합니다."),
            ("QR코드로 사기 피해가 발생할 수 있나요?", "가짜 QR코드로 피싱 사이트로 유도하는 '큐싱(Qshing)' 공격이 있습니다. 스캔 전 <strong>URL 미리보기를 확인</strong>하고, 의심스러운 QR코드는 절대 스캔하지 마세요."),
        ],
        "ctas": [
            {"text": "무료 QR코드 지금 바로 만들기", "desc": "QR Code Generator에서 무료로 QR코드를 생성하세요", "url": "https://www.qr-code-generator.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "Canva로 디자인 QR코드 만들기", "desc": "캔바에서 로고와 색상이 들어간 디자인 QR코드를 만드세요", "url": "https://www.canva.com/ko_kr/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "Bitly 동적 QR코드 시작하기", "desc": "URL 단축 + 통계 제공 Bitly로 동적 QR코드를 만드세요", "url": "https://bitly.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "와이파이 속도 느릴 때 해결 방법 체크리스트 10가지 2026",
        "cat": 5,
        "slug": "wifi-speed-fix-guide-2026",
        "intro": "와이파이 속도가 갑자기 느려지거나, 특정 공간에서만 연결이 약하다면 <strong>다양한 원인</strong>이 있을 수 있습니다. 인터넷 속도 측정부터 공유기 설정 최적화까지, 체크리스트 10가지로 속도를 확실히 개선하세요.",
        "sections": [
            ("와이파이 속도 측정 방법", "<p>해결에 앞서 현재 속도를 정확히 측정하세요.</p><ul><li><strong>fast.com</strong>: 넷플릭스에서 운영하는 가장 간단한 속도 측정</li><li><strong>speedtest.net</strong>: 가장 정확한 속도 측정, 다양한 서버 선택 가능</li><li><strong>네이버 속도 측정</strong>: 네이버 검색창에 '인터넷 속도 측정' 검색</li></ul><p>측정 시 공유기 바로 옆에서 측정한 속도와 멀리서 측정한 속도를 비교하세요.</p>"),
            ("와이파이 느릴 때 체크리스트 10가지", "<h3>1. 공유기 재시작</h3><p>가장 기본적인 해결법. 전원을 뽑았다가 30초 후 재연결.</p><h3>2. 공유기 위치 최적화</h3><p>공유기는 집 중앙, 높은 위치에 설치. 벽·금속·전자레인지 근처 피하기.</p><h3>3. 2.4GHz vs 5GHz 선택</h3><p>2.4GHz: 멀리서도 연결, 속도 느림. 5GHz: 가까운 거리에서 빠름. 가까이 있다면 5GHz 연결.</p><h3>4. 채널 변경</h3><p>이웃 공유기와 채널이 겹치면 간섭 발생. 공유기 설정에서 혼잡하지 않은 채널로 변경(Wi-Fi Analyzer 앱 활용).</p><h3>5. 접속 기기 수 확인</h3><p>공유기 관리 페이지에서 모르는 기기가 접속 중인지 확인. 무단 접속자 차단.</p><h3>6. 펌웨어 업데이트</h3><p>공유기 관리 페이지(보통 192.168.0.1)에서 최신 펌웨어 업데이트.</p><h3>7. QoS 설정</h3><p>특정 기기나 서비스에 대역폭 우선순위를 부여하는 QoS 설정 활용.</p><h3>8. 인터넷 속도 계약 확인</h3><p>계약한 인터넷 속도가 실제 사용량에 맞는지 확인. 100Mbps 계약으로 OTT 4K 5대 동시 시청은 무리.</p><h3>9. 랜선 케이블 확인</h3><p>공유기~PC 랜선이 CAT5e 이상인지 확인. 낡은 케이블 교체.</p><h3>10. 공유기 교체 검토</h3><p>3년 이상 된 공유기는 WiFi 4/5 세대. WiFi 6 공유기로 교체 시 속도와 안정성 향상.</p>"),
            ("공유기 설정 최적화 방법", "<ol><li>공유기 관리 페이지 접속: 브라우저에서 192.168.0.1 또는 192.168.1.1 입력</li><li>무선 채널: 자동 대신 혼잡하지 않은 채널로 수동 설정</li><li>최신 보안 방식: WPA3 또는 WPA2 설정</li><li>손님 네트워크: 방문객용 별도 네트워크로 메인 대역폭 보호</li></ol>"),
        ],
        "faq": [
            ("와이파이 속도가 유선보다 느린 것이 정상인가요?", "네, 정상입니다. 무선 통신은 거리, 장애물, 간섭에 따라 속도가 저하됩니다. <strong>게이밍이나 중요한 작업에는 유선 랜선 연결</strong>을 권장합니다."),
            ("인터넷 계약 속도가 500Mbps인데 왜 느리나요?", "공유기 성능, 연결 기기 수, Wi-Fi 세대, 공유기 위치가 실제 속도에 영향을 줍니다. 공유기 바로 옆에서 <strong>유선으로 속도를 측정</strong>하여 기준을 잡으세요."),
            ("자동으로 와이파이 속도를 최적화해주는 앱이 있나요?", "공유기 앱(ipTIME, ASUS Router 등)에서 자동 채널 최적화, QoS 설정이 가능합니다. <strong>Wi-Fi Analyzer(안드로이드)</strong>로 주변 채널 혼잡도를 확인하세요."),
        ],
        "ctas": [
            {"text": "와이파이 속도 측정하기", "desc": "Speedtest.net에서 현재 와이파이 속도를 측정하세요", "url": "https://www.speedtest.net/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "WiFi 6 공유기 최저가 비교", "desc": "다나와에서 WiFi 6 공유기 최저가를 비교하세요", "url": "https://www.danawa.com/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "ipTIME 공유기 구매하기", "desc": "국내 1위 ipTIME WiFi 6 공유기로 업그레이드하세요", "url": "https://www.iptime.com/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
    {
        "title": "중고 노트북 구매 가이드 2026 체크리스트 주의사항",
        "cat": 5,
        "slug": "used-laptop-buying-guide-2026",
        "intro": "새 노트북 가격의 40~60% 수준에서 <strong>중고 노트북</strong>을 구매할 수 있습니다. 하지만 불량 배터리, 숨겨진 결함, 사기 피해 위험도 있습니다. 2026년 중고 노트북 구매 전 반드시 확인해야 할 체크리스트 10가지와 사기 예방법을 안내합니다.",
        "sections": [
            ("중고 노트북 구매 체크리스트 10가지", "<ol><li><strong>배터리 상태 확인</strong>: 최대 충전 용량 80% 이상 권장. Windows: Battery Report 명령어로 확인. Mac: 시스템 정보 > 전원에서 사이클 횟수 확인(500회 이하 권장).</li><li><strong>화면 불량화소·잔상 확인</strong>: 흰색, 검은색, 빨간색 단색 화면으로 불량화소 검사.</li><li><strong>키보드·터치패드 모든 키 작동</strong>: 키보드 테스트 사이트에서 모든 키를 눌러보세요.</li><li><strong>충전 포트 상태</strong>: 흔들어도 충전이 유지되는지 확인.</li><li><strong>USB, HDMI 등 모든 포트 확인</strong>: USB 드라이브를 연결해서 인식 여부 확인.</li><li><strong>스피커·마이크·카메라 작동</strong>: 영상통화 테스트.</li><li><strong>SSD/HDD 상태 확인</strong>: CrystalDiskInfo로 HDD/SSD 건강 상태 확인.</li><li><strong>RAM·CPU 성능 확인</strong>: CPU-Z, HWiNFO로 실제 스펙 확인(스펙 위조 방지).</li><li><strong>발열·소음 확인</strong>: 10분 이상 사용하여 발열 수준과 팬 소음 확인.</li><li><strong>외관 흠집·힌지 상태</strong>: 화면 힌지가 흔들리지 않는지, 뚜껑 틈이 균일한지 확인.</li></ol>"),
            ("중고 노트북 적정 가격 가이드 2026", "<table><thead><tr><th>모델</th><th>출시 연도</th><th>적정 중고가</th><th>주의사항</th></tr></thead><tbody><tr><td>맥북 에어 M2 (13인치)</td><td>2022</td><td>80~100만원</td><td>배터리 사이클 확인</td></tr><tr><td>맥북 프로 M3 (14인치)</td><td>2023</td><td>150~180만원</td><td>스크래치 주의</td></tr><tr><td>갤럭시북 4 프로 (16인치)</td><td>2024</td><td>90~120만원</td><td>OLED 번인 확인</td></tr><tr><td>LG 그램 17인치</td><td>2023</td><td>80~100만원</td><td>배터리 상태 필수</td></tr><tr><td>ThinkPad X1 Carbon</td><td>2022</td><td>70~90만원</td><td>키보드 마모 확인</td></tr></tbody></table>"),
            ("중고 거래 사이트 비교", "<table><thead><tr><th>플랫폼</th><th>특징</th><th>사기 위험</th><th>추천 거래</th></tr></thead><tbody><tr><td>당근마켓</td><td>동네 직거래</td><td>낮음</td><td>실물 확인 후 결제</td></tr><tr><td>번개장터</td><td>전국 거래, 번개페이</td><td>중간</td><td>번개페이 안전거래 사용</td></tr><tr><td>중고나라</td><td>가장 많은 매물</td><td>높음</td><td>직거래 또는 안전거래</td></tr><tr><td>세티즌</td><td>IT기기 전문</td><td>낮음</td><td>판매자 평점 확인</td></tr></tbody></table>"),
            ("중고 노트북 사기 예방법", "<ol><li><strong>직거래 원칙</strong>: 택배 거래 시 대포통장·원격제어 사기 위험. 가능하면 직접 만나서 확인 후 결제.</li><li><strong>안전결제 사용</strong>: 번개페이, 당근 안전거래 등 플랫폼의 안전결제 시스템 사용.</li><li><strong>계좌이체 선입금 금지</strong>: '택배 후 환불 보장' 문구는 전형적인 사기 수법.</li><li><strong>시세보다 30% 이상 저렴하면 의심</strong>: 미끼 상품일 가능성 높음.</li><li><strong>사기 이력 조회</strong>: 더치트(thecheat.co.kr)에서 판매자 전화번호·계좌 조회.</li></ol>"),
        ],
        "faq": [
            ("맥북 중고 구매 시 가장 중요한 점은?", "배터리 사이클 횟수(500회 이하 권장)와 <strong>애플 공식 스크린 상태 확인</strong>이 핵심입니다. 'iCloud 초기화 여부'도 반드시 확인하세요. 활성화 잠금이 걸려 있으면 사용이 불가합니다."),
            ("중고 노트북 구매 후 AS를 받을 수 있나요?", "중고 노트북은 제조사 보증이 대부분 만료됩니다. <strong>사설 수리점</strong>을 이용하거나, 구매 전 남은 보증 기간을 확인하세요. 일부 맥북은 애플케어+ 이전이 가능합니다."),
            ("중고 노트북 구매 후 포맷을 해야 하나요?", "<strong>반드시 포맷(초기화)을 권장합니다</strong>. 이전 사용자의 개인정보, 악성 소프트웨어가 남아있을 수 있습니다. 구매 후 Windows 재설치 또는 Mac 초기화를 진행하세요."),
        ],
        "ctas": [
            {"text": "당근마켓 중고 노트북 검색", "desc": "당근마켓에서 근처 중고 노트북 직거래를 찾아보세요", "url": "https://www.daangn.com/", "bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5"},
            {"text": "더치트 사기 이력 조회", "desc": "구매 전 판매자 사기 이력을 더치트에서 확인하세요", "url": "https://www.thecheat.co.kr/", "bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
            {"text": "번개장터 중고 노트북 안전거래", "desc": "번개페이 안전거래로 중고 노트북을 안전하게 구매하세요", "url": "https://www.bunjang.co.kr/", "bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1"},
        ]
    },
]


def make_cta(cta):
    border_style = f"border:{cta['border']};" if cta.get("border") else ""
    return f"""<div style="background:{cta['bg']};{border_style}border-radius:12px;padding:28px 32px;margin:32px 0;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;">
  <div>
    <p style="margin:0 0 6px;font-size:18px;font-weight:700;color:{cta['text_color']};">{cta['text']}</p>
    <p style="margin:0;font-size:14px;color:{cta['desc_color']};">{cta['desc']}</p>
  </div>
  <a href="{cta['url']}" target="_blank" rel="noopener noreferrer"
     style="background:{cta['btn_bg']};color:{cta['btn_color']};padding:12px 24px;border-radius:8px;font-weight:700;text-decoration:none;white-space:nowrap;font-size:15px;">
    바로가기 &rarr;
  </a>
</div>"""


def build_content(post):
    parts = []
    slug = post.get("slug", "")
    parts.append(f'<p style="font-size:17px;line-height:1.8;margin-bottom:24px;">{post["intro"]}</p>')

    # 첫 번째 이미지: 인트로 바로 아래
    img1 = get_image_html(slug, 0)
    if img1:
        parts.append(img1)

    sections = post["sections"]
    ctas = post["ctas"]
    num_sections = len(sections)

    # 두 번째 이미지 삽입 위치: 전체 섹션의 약 60% 지점
    img2_pos = max(2, int(num_sections * 0.6))

    for i, (title, body) in enumerate(sections):
        parts.append(f'<h2 style="font-size:22px;font-weight:700;margin:40px 0 16px;border-left:4px solid #2563eb;padding-left:12px;">{title}</h2>')
        parts.append(body)
        if i == 1 and len(ctas) > 0:
            parts.append(make_cta(ctas[0]))
        elif i == num_sections // 2 and len(ctas) > 1:
            parts.append(make_cta(ctas[1]))
        # 두 번째 이미지 삽입
        if i == img2_pos:
            img2 = get_image_html(slug, 1)
            if img2:
                parts.append(img2)

    parts.append('<h2 style="font-size:22px;font-weight:700;margin:40px 0 16px;border-left:4px solid #2563eb;padding-left:12px;">자주 묻는 질문 (FAQ)</h2>')
    for q, a in post["faq"]:
        parts.append(f'<h3 style="font-size:17px;font-weight:600;color:#1e40af;margin:20px 0 8px;">Q. {q}</h3>')
        parts.append(f'<p style="margin:0 0 16px;line-height:1.8;">A. {a}</p>')

    if len(ctas) > 2:
        parts.append(make_cta(ctas[2]))

    return "\n".join(parts)


def publish(post_data):
    data = json.dumps(post_data).encode("utf-8")
    req = urllib.request.Request(
        API,
        data=data,
        headers={
            "Authorization": f"Basic {AUTH}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("id"), result.get("link", "")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"  HTTP Error {e.code}: {body[:200]}")
        return None, None
    except Exception as e:
        print(f"  Error: {e}")
        return None, None


def main():
    # 1단계: 이미지 업로드
    upload_all_images()

    # 2단계: 포스트 발행
    total = len(POSTS)
    print("=" * 60)
    print(f"총 {total}개 포스트 발행 시작")
    print("=" * 60)
    for idx, post in enumerate(POSTS, 1):
        content = build_content(post)
        payload = {
            "title": post["title"],
            "content": content,
            "status": "publish",
            "slug": post["slug"],
            "categories": [post["cat"]],
        }
        post_id, link = publish(payload)
        if post_id:
            print(f"[{idx}/{total}] OK | ID:{post_id} | {post['title']}")
        else:
            print(f"[{idx}/{total}] FAIL | {post['title']}")
        time.sleep(1)
    print("\n완료!")


if __name__ == "__main__":
    main()

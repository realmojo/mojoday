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

# 실패한 10장 -> 대체 Unsplash photo ID
FIXES = [
    {"post_id": 34567, "slug": "wireless-earbuds-recommendation-2026", "idx": 1, "filename": "wireless-earbuds-recommendation-2026-1",
     "photo_id": "photo-1505740420928-5e560c06d30e", "alt": "무선 이어폰 착용 모습"},
    {"post_id": 34569, "slug": "external-storage-recommendation-2026", "idx": 2, "filename": "external-storage-recommendation-2026-2",
     "photo_id": "photo-1531492898926-e1afb5798f85", "alt": "데이터 저장 장치"},
    {"post_id": 34571, "slug": "webcam-recommendation-2026", "idx": 2, "filename": "webcam-recommendation-2026-2",
     "photo_id": "photo-1587825140708-dfaf18c4b234", "alt": "웹캠 셋업"},
    {"post_id": 34576, "slug": "free-video-editor-recommendation-2026", "idx": 2, "filename": "free-video-editor-recommendation-2026-2",
     "photo_id": "photo-1574717024653-61fd2cf4d44d", "alt": "동영상 편집 작업"},
    {"post_id": 34584, "slug": "remote-desktop-recommendation-2026", "idx": 2, "filename": "remote-desktop-recommendation-2026-2",
     "photo_id": "photo-1553877522-43269d4ea984", "alt": "재택근무 데스크 셋업"},
    {"post_id": 34588, "slug": "email-service-comparison-2026", "idx": 2, "filename": "email-service-comparison-2026-2",
     "photo_id": "photo-1557200134-90327ee9fafa", "alt": "이메일 업무 화면"},
    {"post_id": 34594, "slug": "video-conference-comparison-2026", "idx": 1, "filename": "video-conference-comparison-2026-1",
     "photo_id": "photo-1588196749597-9ff075ee6b5b", "alt": "화상회의 진행"},
    {"post_id": 34603, "slug": "windows-11-optimization-guide-2026", "idx": 1, "filename": "windows-11-optimization-guide-2026-1",
     "photo_id": "photo-1629654297299-c8506221ca97", "alt": "윈도우 11 데스크톱"},
    {"post_id": 34604, "slug": "windows-reinstall-guide-2026", "idx": 1, "filename": "windows-reinstall-guide-2026-1",
     "photo_id": "photo-1629654297299-c8506221ca97", "alt": "윈도우 설치 화면"},
    {"post_id": 34612, "slug": "smart-home-beginner-guide-2026", "idx": 1, "filename": "smart-home-beginner-guide-2026-1",
     "photo_id": "photo-1556761175-b413da4baf72", "alt": "스마트홈 IoT 기기"},
]


def download_image(photo_id):
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
        print(f"  다운로드 실패 ({photo_id}): {e}")
        return None


def upload_image_to_wp(file_path, filename, alt_text):
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
            if media_id and alt_text:
                update_data = json.dumps({"alt_text": alt_text}).encode("utf-8")
                update_req = urllib.request.Request(f"{MEDIA_API}/{media_id}", data=update_data, method="POST")
                update_req.add_header("Authorization", f"Basic {AUTH}")
                update_req.add_header("Content-Type", "application/json")
                try:
                    urllib.request.urlopen(update_req, timeout=15)
                except Exception:
                    pass
            return media_url
    except Exception as e:
        print(f"  업로드 실패: {e}")
        return None


def get_post_content(post_id):
    req = urllib.request.Request(f"{API}/{post_id}")
    req.add_header("Authorization", f"Basic {AUTH}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        return result.get("content", {}).get("raw", "") or result.get("content", {}).get("rendered", "")


def update_post_content(post_id, new_content):
    data = json.dumps({"content": new_content}).encode("utf-8")
    req = urllib.request.Request(f"{API}/{post_id}", data=data, method="POST")
    req.add_header("Authorization", f"Basic {AUTH}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8")).get("id")


def make_image_html(wp_url, alt_text):
    return f'''<figure style="margin:32px 0;text-align:center;">
<img src="{wp_url}" alt="{alt_text}" style="width:100%;max-width:800px;height:auto;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.10);" loading="lazy" />
<figcaption style="margin-top:8px;font-size:13px;color:#6b7280;">{alt_text}</figcaption>
</figure>'''


print(f"누락 이미지 {len(FIXES)}장 복구 시작\n")

for i, fix in enumerate(FIXES, 1):
    print(f"[{i}/{len(FIXES)}] {fix['filename']}")

    # 1. 다운로드
    tmp_path = download_image(fix["photo_id"])
    if not tmp_path:
        continue

    # 2. WP 업로드
    wp_url = upload_image_to_wp(tmp_path, fix["filename"], fix["alt"])
    os.unlink(tmp_path)
    if not wp_url:
        continue
    print(f"  업로드 OK -> {wp_url}")

    # 3. 포스트 가져오기
    content = get_post_content(fix["post_id"])
    if not content:
        print(f"  포스트 내용 가져오기 실패")
        continue

    # 4. 이미지 삽입
    img_html = make_image_html(wp_url, fix["alt"])

    if fix["idx"] == 1:
        # 첫 번째 이미지: 첫 번째 </p> 뒤에 삽입
        pos = content.find("</p>")
        if pos != -1:
            content = content[:pos+4] + "\n" + img_html + "\n" + content[pos+4:]
    else:
        # 두 번째 이미지: FAQ 섹션 앞에 삽입
        faq_pos = content.find("자주 묻는 질문")
        if faq_pos != -1:
            # 그 앞의 <h2 태그 찾기
            h2_pos = content.rfind("<h2", 0, faq_pos)
            if h2_pos != -1:
                content = content[:h2_pos] + img_html + "\n" + content[h2_pos:]

    # 5. 포스트 업데이트
    result_id = update_post_content(fix["post_id"], content)
    if result_id:
        print(f"  포스트 {result_id} 업데이트 OK")
    else:
        print(f"  포스트 업데이트 실패")

    time.sleep(1)

print("\n완료!")

"""
'함께 읽으면 좋은 글' 블록을 FAQ 위 → 첫 번째 H2 바로 위로 이동
"""
import json, urllib.request, base64, ssl, time, re

ssl._create_default_https_context = ssl._create_unverified_context
AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API = "https://devupbox.com/wp-json/wp/v2/posts"
POST_IDS = list(range(37503, 37549))


def main():
    print(f"{'='*60}\n위치 변경: FAQ 위 → 첫 번째 H2 위\n{'='*60}")
    success = fail = skip = 0

    for pid in POST_IDS:
        req = urllib.request.Request(f"{API}/{pid}?_fields=id,slug,content", headers={"Authorization": f"Basic {AUTH}"})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
                slug = data.get("slug", "")
                content = data["content"]["rendered"]
        except Exception as e:
            print(f"  FAIL | #{pid}: {e}")
            fail += 1
            continue

        # 블록 찾기
        idx = content.find("함께 읽으면 좋은 글")
        if idx < 0:
            print(f"  SKIP | {slug} (블록 없음)")
            skip += 1
            continue

        block_start = content.rfind("<div", 0, idx)
        if block_start < 0:
            print(f"  SKIP | {slug} (시작 못 찾음)")
            skip += 1
            continue

        # 마지막 </a> 이후 </div></div> 패턴으로 블록 끝 찾기
        last_a = content.rfind("</a>", block_start, block_start + 5000)
        if last_a < 0:
            print(f"  SKIP | {slug} (</a> 못 찾음)")
            skip += 1
            continue

        rest = content[last_a:]
        m = re.search(r'</a>(</div>\s*</div>\s*)', rest)
        if not m:
            print(f"  SKIP | {slug} (끝 패턴 못 찾음)")
            skip += 1
            continue

        block_end = last_a + m.end()
        related_block = content[block_start:block_end]

        # 블록 제거
        content_clean = content[:block_start] + content[block_end:]

        # 첫 번째 H2 찾기
        first_h2 = re.search(r'<h2[^>]*>', content_clean)
        if not first_h2:
            print(f"  SKIP | {slug} (H2 없음)")
            skip += 1
            continue

        # 첫 번째 H2 바로 위에 삽입
        new_content = content_clean[:first_h2.start()] + related_block + "\n" + content_clean[first_h2.start():]

        # 업데이트
        update_data = json.dumps({"content": new_content}).encode()
        req = urllib.request.Request(f"{API}/{pid}", data=update_data, method="POST")
        req.add_header("Authorization", f"Basic {AUTH}")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                json.loads(resp.read().decode())
                print(f"  OK | {slug}")
                success += 1
        except Exception as e:
            print(f"  FAIL | {slug}: {e}")
            fail += 1
        time.sleep(0.5)

    print(f"\n{'='*60}")
    print(f"완료! 성공: {success} / 실패: {fail} / 스킵: {skip}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

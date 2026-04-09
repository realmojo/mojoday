"""
내부 링크 UI v3: 구글 광고 스타일 파란 버튼 + 흰 글씨 + 큰 글씨 + 테두리 없음
"""
import json, urllib.request, base64, ssl, time, re

ssl._create_default_https_context = ssl._create_unverified_context
AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API = "https://devupbox.com/wp-json/wp/v2/posts"
POST_IDS = list(range(37503, 37549))

NEW_BLOCK_TEMPLATE = '''<div style="margin:40px 0;">
{links}
</div>'''

LINK_TEMPLATE = '''<a href="{url}" style="display:block;background:#1a73e8;border-radius:8px;padding:18px 22px;margin-bottom:12px;text-decoration:none;color:#fff;font-size:17px;font-weight:700;transition:background 0.2s;" onmouseover="this.style.background='#1558b0'" onmouseout="this.style.background='#1a73e8'">📄 {title}</a>'''


def main():
    print(f"{'='*60}\nUI v3: 파란 버튼 스타일로 변경\n{'='*60}")
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
        idx = content.find("이 글도 꼭 읽어보세요")
        if idx < 0:
            idx = content.find("함께 읽으면 좋은 글")
        if idx < 0:
            print(f"  SKIP | {slug}")
            skip += 1
            continue

        block_start = content.rfind("<div", 0, idx)

        # 링크 추출
        search_area = content[block_start:block_start+5000]
        links = re.findall(r'href="(https://devupbox\.com/[^"]+)"[^>]*>(?:→|📄)?\s*(.+?)</(?:a|span)>', search_area)

        if not links:
            print(f"  SKIP | {slug} (링크 없음)")
            skip += 1
            continue

        # 블록 끝 찾기
        last_link_end = 0
        for m in re.finditer(r'</a>', search_area):
            last_link_end = m.end()
        remaining = search_area[last_link_end:]
        div_match = re.match(r'(\s*</div>)+', remaining)
        block_end = block_start + (last_link_end + div_match.end() if div_match else last_link_end)

        # 새 UI 생성
        links_html = ""
        for url, title in links:
            title = title.strip()
            links_html += LINK_TEMPLATE.format(url=url, title=title) + "\n"

        new_block = NEW_BLOCK_TEMPLATE.format(links=links_html.strip())

        # 교체
        new_content = content[:block_start] + new_block + content[block_end:]

        # 업데이트
        update_data = json.dumps({"content": new_content}).encode()
        req = urllib.request.Request(f"{API}/{pid}", data=update_data, method="POST")
        req.add_header("Authorization", f"Basic {AUTH}")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                json.loads(resp.read().decode())
                print(f"  OK | {slug} ({len(links)}개)")
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

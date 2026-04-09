"""
내부 링크 UI v4: 아이콘 1개 + 우측 화살표 + 세로 1.5배
"""
import json, urllib.request, base64, ssl, time, re

ssl._create_default_https_context = ssl._create_unverified_context
AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API = "https://devupbox.com/wp-json/wp/v2/posts"
POST_IDS = list(range(37503, 37549))

NEW_BLOCK_TEMPLATE = '''<div style="margin:40px 0;">
{links}
</div>'''

LINK_TEMPLATE = '''<a href="{url}" style="display:flex;align-items:center;justify-content:space-between;background:#1a73e8;border-radius:8px;padding:27px 22px;margin-bottom:12px;text-decoration:none;color:#fff;font-size:17px;font-weight:700;transition:background 0.2s;" onmouseover="this.style.background='#1558b0'" onmouseout="this.style.background='#1a73e8'"><span>{title}</span><span style="font-size:22px;">→</span></a>'''


def main():
    print(f"{'='*60}\nUI v4: 아이콘 정리 + 화살표 + 높이 조정\n{'='*60}")
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

        # 기존 블록 찾기 (v3 스타일)
        # v3은 <div style="margin:40px 0;"> 안에 파란 버튼들
        # 📄 아이콘이 있는 링크를 찾기
        links = []
        # 파란 버튼 패턴
        for m in re.finditer(r'<a href="(https://devupbox\.com/excel/[^"]+)"[^>]*background:#1a73e8[^>]*>📄\s*(.+?)</a>', content):
            links.append((m.group(1), m.group(2).strip()))

        if not links:
            print(f"  SKIP | {slug}")
            skip += 1
            continue

        # 블록 전체 찾기: 첫 번째 파란 버튼의 감싸는 div부터
        first_link = re.search(r'<a href="https://devupbox\.com/excel/[^"]*"[^>]*background:#1a73e8', content)
        if not first_link:
            print(f"  SKIP | {slug} (첫 링크 못찾음)")
            skip += 1
            continue

        # 감싸는 <div style="margin:40px 찾기
        block_start = content.rfind('<div style="margin:40px', 0, first_link.start())
        if block_start < 0:
            block_start = content.rfind('<div', 0, first_link.start())

        # 마지막 </a> 이후 </div>
        last_a = content.rfind('</a>', first_link.start(), first_link.start() + 5000)
        remaining = content[last_a+4:]
        div_end = re.match(r'(\s*</div>)+', remaining)
        block_end = last_a + 4 + (div_end.end() if div_end else 0)

        # 새 UI
        links_html = "\n".join(LINK_TEMPLATE.format(url=u, title=t) for u, t in links)
        new_block = NEW_BLOCK_TEMPLATE.format(links=links_html)

        new_content = content[:block_start] + new_block + content[block_end:]

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

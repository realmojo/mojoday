"""
'함께 읽으면 좋은 글' UI를 클릭 유도하는 카드형 디자인으로 변경
"""
import json, urllib.request, base64, ssl, time, re

ssl._create_default_https_context = ssl._create_unverified_context
AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API = "https://devupbox.com/wp-json/wp/v2/posts"
POST_IDS = list(range(37503, 37549))

# 새로운 UI: 카드형 + 아이콘 + 호버 효과 + 화살표
NEW_STYLE_TEMPLATE = '''<div style="background:linear-gradient(135deg,#eff6ff 0%,#f0fdf4 100%);border:2px solid #bfdbfe;border-radius:16px;padding:24px;margin:40px 0;">
<p style="font-size:20px;font-weight:800;margin:0 0 16px;color:#1e3a5f;">🔗 이 글도 꼭 읽어보세요!</p>
{links}
</div>'''

LINK_TEMPLATE = '''<a href="{url}" style="display:flex;align-items:center;justify-content:space-between;background:#fff;border:1px solid #dbeafe;border-left:4px solid #3b82f6;border-radius:10px;padding:16px 20px;margin-bottom:10px;text-decoration:none;color:#1e293b;font-size:15px;font-weight:600;box-shadow:0 1px 3px rgba(0,0,0,0.06);transition:all 0.2s ease;" onmouseover="this.style.background='#eff6ff';this.style.borderLeftColor='#1d4ed8';this.style.transform='translateX(4px)';this.style.boxShadow='0 4px 12px rgba(59,130,246,0.15)'" onmouseout="this.style.background='#fff';this.style.borderLeftColor='#3b82f6';this.style.transform='none';this.style.boxShadow='0 1px 3px rgba(0,0,0,0.06)'"><span>📄 {title}</span><span style="color:#3b82f6;font-size:18px;">›</span></a>'''


def main():
    print(f"{'='*60}\n내부 링크 UI 업그레이드\n{'='*60}")
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

        # 기존 블록 찾기
        idx = content.find("함께 읽으면 좋은 글")
        if idx < 0:
            idx = content.find("이 글도 꼭 읽어보세요")
        if idx < 0:
            print(f"  SKIP | {slug} (블록 없음)")
            skip += 1
            continue

        block_start = content.rfind("<div", 0, idx)
        if block_start < 0:
            print(f"  SKIP | {slug} (시작 못찾음)")
            skip += 1
            continue

        # 블록 끝 찾기
        last_a = content.rfind("</a>", block_start, block_start + 5000)
        if last_a < 0:
            print(f"  SKIP | {slug} (</a> 없음)")
            skip += 1
            continue

        rest = content[last_a:]
        m = re.search(r'</a>(</div>\s*</div>\s*)', rest)
        if not m:
            print(f"  SKIP | {slug} (끝 패턴 없음)")
            skip += 1
            continue

        block_end = last_a + m.end()
        old_block = content[block_start:block_end]

        # 기존 블록에서 링크 추출 (href + title)
        links = re.findall(r'href="([^"]+)"[^>]*>(?:→|📄)\s*(.+?)</a>', old_block)
        if not links:
            print(f"  SKIP | {slug} (링크 없음)")
            skip += 1
            continue

        # 새 UI 생성
        links_html = ""
        for url, title in links:
            title = title.strip()
            links_html += LINK_TEMPLATE.format(url=url, title=title) + "\n"

        new_block = NEW_STYLE_TEMPLATE.format(links=links_html.strip())

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

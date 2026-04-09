"""
지원금 26개 포스트에 관련 글 내부 링크 버튼 삽입
지역별(광역시/경기도/강원도/충청도)로 그룹핑하여 거미줄 연결
첫 번째 H2 바로 위에 구글 파란 버튼 5개씩 삽입
"""
import json, urllib.request, base64, ssl, time, re

ssl._create_default_https_context = ssl._create_unverified_context
AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API = "https://devupbox.com/wp-json/wp/v2/posts"

# 26개 포스트 ID 범위
POST_IDS = [37781, 37783, 37785, 37786, 37788, 37790, 37792, 37794, 37796, 37798,
            37800, 37802, 37804, 37806, 37808, 37810, 37812, 37813, 37815, 37817,
            37819, 37821, 37823, 37825, 37827, 37829]

# 지역별 그룹 (slug 기준)
# 각 포스트에 최대 5개 관련 링크 연결
RELATED = {
    # === 충청북도 ===
    "2026-chungju-3rd-livelihood-coupon": ["2026-cheongju-3rd-livelihood-coupon", "2026-daejeon-3rd-livelihood-coupon", "2026-sejong-3rd-livelihood-coupon", "2026-asan-3rd-livelihood-coupon", "2026-seosan-3rd-livelihood-coupon"],
    "2026-cheongju-3rd-livelihood-coupon": ["2026-chungju-3rd-livelihood-coupon", "2026-daejeon-3rd-livelihood-coupon", "2026-sejong-3rd-livelihood-coupon", "2026-asan-3rd-livelihood-coupon", "2026-seosan-3rd-livelihood-coupon"],

    # === 강원도 ===
    "2026-samcheok-3rd-livelihood-coupon": ["2026-sokcho-3rd-livelihood-coupon", "2026-chungju-3rd-livelihood-coupon", "2026-cheongju-3rd-livelihood-coupon", "2026-seoul-3rd-livelihood-coupon", "2026-incheon-3rd-livelihood-coupon"],
    "2026-sokcho-3rd-livelihood-coupon": ["2026-samcheok-3rd-livelihood-coupon", "2026-chungju-3rd-livelihood-coupon", "2026-cheongju-3rd-livelihood-coupon", "2026-seoul-3rd-livelihood-coupon", "2026-incheon-3rd-livelihood-coupon"],

    # === 충청남도 ===
    "2026-seosan-3rd-livelihood-coupon": ["2026-asan-3rd-livelihood-coupon", "2026-daejeon-3rd-livelihood-coupon", "2026-sejong-3rd-livelihood-coupon", "2026-chungju-3rd-livelihood-coupon", "2026-cheongju-3rd-livelihood-coupon"],
    "2026-asan-3rd-livelihood-coupon": ["2026-seosan-3rd-livelihood-coupon", "2026-daejeon-3rd-livelihood-coupon", "2026-sejong-3rd-livelihood-coupon", "2026-cheongju-3rd-livelihood-coupon", "2026-chungju-3rd-livelihood-coupon"],

    # === 경기도 (많음) - 서로 교차 연결 ===
    "2026-icheon-3rd-livelihood-coupon": ["2026-osan-3rd-livelihood-coupon", "2026-anseong-3rd-livelihood-coupon", "2026-yongin-3rd-livelihood-coupon", "2026-suwon-3rd-livelihood-coupon", "2026-hanam-3rd-livelihood-coupon"],
    "2026-osan-3rd-livelihood-coupon": ["2026-suwon-3rd-livelihood-coupon", "2026-gunpo-3rd-livelihood-coupon", "2026-anseong-3rd-livelihood-coupon", "2026-yongin-3rd-livelihood-coupon", "2026-icheon-3rd-livelihood-coupon"],
    "2026-gunpo-3rd-livelihood-coupon": ["2026-suwon-3rd-livelihood-coupon", "2026-osan-3rd-livelihood-coupon", "2026-yongin-3rd-livelihood-coupon", "2026-hanam-3rd-livelihood-coupon", "2026-gimpo-3rd-livelihood-coupon"],
    "2026-yangju-3rd-livelihood-coupon": ["2026-uijeongbu-3rd-livelihood-coupon", "2026-guri-3rd-livelihood-coupon", "2026-hanam-3rd-livelihood-coupon", "2026-gimpo-3rd-livelihood-coupon", "2026-seoul-3rd-livelihood-coupon"],
    "2026-hanam-3rd-livelihood-coupon": ["2026-gwangju-gyeonggi-3rd-livelihood-coupon", "2026-guri-3rd-livelihood-coupon", "2026-seoul-3rd-livelihood-coupon", "2026-suwon-3rd-livelihood-coupon", "2026-yongin-3rd-livelihood-coupon"],
    "2026-gwangju-gyeonggi-3rd-livelihood-coupon": ["2026-hanam-3rd-livelihood-coupon", "2026-yongin-3rd-livelihood-coupon", "2026-icheon-3rd-livelihood-coupon", "2026-suwon-3rd-livelihood-coupon", "2026-anseong-3rd-livelihood-coupon"],
    "2026-uijeongbu-3rd-livelihood-coupon": ["2026-yangju-3rd-livelihood-coupon", "2026-guri-3rd-livelihood-coupon", "2026-hanam-3rd-livelihood-coupon", "2026-seoul-3rd-livelihood-coupon", "2026-gimpo-3rd-livelihood-coupon"],
    "2026-gimpo-3rd-livelihood-coupon": ["2026-seoul-3rd-livelihood-coupon", "2026-incheon-3rd-livelihood-coupon", "2026-hanam-3rd-livelihood-coupon", "2026-guri-3rd-livelihood-coupon", "2026-uijeongbu-3rd-livelihood-coupon"],
    "2026-guri-3rd-livelihood-coupon": ["2026-uijeongbu-3rd-livelihood-coupon", "2026-yangju-3rd-livelihood-coupon", "2026-hanam-3rd-livelihood-coupon", "2026-gimpo-3rd-livelihood-coupon", "2026-seoul-3rd-livelihood-coupon"],
    "2026-anseong-3rd-livelihood-coupon": ["2026-icheon-3rd-livelihood-coupon", "2026-yongin-3rd-livelihood-coupon", "2026-osan-3rd-livelihood-coupon", "2026-suwon-3rd-livelihood-coupon", "2026-gwangju-gyeonggi-3rd-livelihood-coupon"],
    "2026-yongin-3rd-livelihood-coupon": ["2026-suwon-3rd-livelihood-coupon", "2026-hanam-3rd-livelihood-coupon", "2026-osan-3rd-livelihood-coupon", "2026-icheon-3rd-livelihood-coupon", "2026-gwangju-gyeonggi-3rd-livelihood-coupon"],
    "2026-suwon-3rd-livelihood-coupon": ["2026-yongin-3rd-livelihood-coupon", "2026-osan-3rd-livelihood-coupon", "2026-gunpo-3rd-livelihood-coupon", "2026-hanam-3rd-livelihood-coupon", "2026-anseong-3rd-livelihood-coupon"],

    # === 광역시/특별시 - 대도시끼리 연결 ===
    "2026-sejong-3rd-livelihood-coupon": ["2026-daejeon-3rd-livelihood-coupon", "2026-cheongju-3rd-livelihood-coupon", "2026-chungju-3rd-livelihood-coupon", "2026-seoul-3rd-livelihood-coupon", "2026-asan-3rd-livelihood-coupon"],
    "2026-ulsan-3rd-livelihood-coupon": ["2026-busan-3rd-livelihood-coupon", "2026-daegu-3rd-livelihood-coupon", "2026-seoul-3rd-livelihood-coupon", "2026-gwangju-3rd-livelihood-coupon", "2026-incheon-3rd-livelihood-coupon"],
    "2026-gwangju-3rd-livelihood-coupon": ["2026-daejeon-3rd-livelihood-coupon", "2026-daegu-3rd-livelihood-coupon", "2026-busan-3rd-livelihood-coupon", "2026-seoul-3rd-livelihood-coupon", "2026-ulsan-3rd-livelihood-coupon"],
    "2026-daejeon-3rd-livelihood-coupon": ["2026-sejong-3rd-livelihood-coupon", "2026-cheongju-3rd-livelihood-coupon", "2026-chungju-3rd-livelihood-coupon", "2026-seoul-3rd-livelihood-coupon", "2026-gwangju-3rd-livelihood-coupon"],
    "2026-daegu-3rd-livelihood-coupon": ["2026-busan-3rd-livelihood-coupon", "2026-ulsan-3rd-livelihood-coupon", "2026-gwangju-3rd-livelihood-coupon", "2026-seoul-3rd-livelihood-coupon", "2026-incheon-3rd-livelihood-coupon"],
    "2026-incheon-3rd-livelihood-coupon": ["2026-seoul-3rd-livelihood-coupon", "2026-gimpo-3rd-livelihood-coupon", "2026-busan-3rd-livelihood-coupon", "2026-daegu-3rd-livelihood-coupon", "2026-ulsan-3rd-livelihood-coupon"],
    "2026-busan-3rd-livelihood-coupon": ["2026-ulsan-3rd-livelihood-coupon", "2026-daegu-3rd-livelihood-coupon", "2026-seoul-3rd-livelihood-coupon", "2026-incheon-3rd-livelihood-coupon", "2026-gwangju-3rd-livelihood-coupon"],
    "2026-seoul-3rd-livelihood-coupon": ["2026-incheon-3rd-livelihood-coupon", "2026-busan-3rd-livelihood-coupon", "2026-daegu-3rd-livelihood-coupon", "2026-suwon-3rd-livelihood-coupon", "2026-hanam-3rd-livelihood-coupon"],
}


# 버튼 HTML 템플릿
NEW_BLOCK = '''<div style="margin:40px 0;">
{links}
</div>'''

LINK = '''<a href="{url}" style="display:flex;align-items:center;justify-content:space-between;background:#1a73e8;border-radius:8px;padding:27px 22px;margin-bottom:12px;text-decoration:none;color:#fff;font-size:17px;font-weight:700;transition:background 0.2s;" onmouseover="this.style.background='#1558b0'" onmouseout="this.style.background='#1a73e8'"><span>{title}</span><span style="font-size:22px;">→</span></a>'''


def main():
    print(f"{'='*60}\n지원금 26개 내부 링크 버튼 삽입\n{'='*60}")

    # 1단계: 모든 포스트의 slug → {id, title, link} 수집
    print("1단계: 포스트 정보 수집")
    post_map = {}
    for pid in POST_IDS:
        req = urllib.request.Request(f"{API}/{pid}?_fields=id,slug,title,link", headers={"Authorization": f"Basic {AUTH}"})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
                slug = data.get("slug", "")
                post_map[slug] = {
                    "id": data["id"],
                    "title": data["title"]["rendered"],
                    "link": data["link"],
                }
                print(f"  #{pid} | {slug}")
        except Exception as e:
            print(f"  #{pid} 실패: {e}")
        time.sleep(0.3)
    print(f"\n수집 완료: {len(post_map)}개\n")

    # 2단계: 각 포스트에 관련 링크 삽입
    print("2단계: 내부 링크 삽입")
    success = fail = skip = 0

    for slug, related_slugs in RELATED.items():
        if slug not in post_map:
            print(f"  SKIP | {slug} (포스트 없음)")
            skip += 1
            continue

        post = post_map[slug]
        pid = post["id"]

        # 관련 링크 목록
        related_links = []
        for rs in related_slugs:
            if rs in post_map:
                related_links.append((post_map[rs]["title"], post_map[rs]["link"]))

        if not related_links:
            print(f"  SKIP | {slug} (관련글 없음)")
            skip += 1
            continue

        # 현재 content 가져오기
        req = urllib.request.Request(f"{API}/{pid}?_fields=content", headers={"Authorization": f"Basic {AUTH}"})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = json.loads(resp.read().decode())["content"]["rendered"]
        except Exception as e:
            print(f"  FAIL | {slug}: {e}")
            fail += 1
            continue

        # 이미 버튼이 삽입되어 있으면 스킵
        if "background:#1a73e8" in content and "→" in content:
            print(f"  SKIP | {slug} (이미 삽입됨)")
            skip += 1
            continue

        # 버튼 블록 생성
        links_html = "\n".join(LINK.format(url=url, title=title) for title, url in related_links)
        new_block = NEW_BLOCK.format(links=links_html)

        # 첫 번째 H2 바로 위에 삽입
        first_h2 = re.search(r'<h2[^>]*>', content)
        if first_h2:
            new_content = content[:first_h2.start()] + new_block + "\n" + content[first_h2.start():]
        else:
            new_content = new_block + "\n" + content

        # 업데이트
        update_data = json.dumps({"content": new_content}).encode()
        req = urllib.request.Request(f"{API}/{pid}", data=update_data, method="POST")
        req.add_header("Authorization", f"Basic {AUTH}")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                json.loads(resp.read().decode())
                print(f"  OK | {slug} ({len(related_links)}개)")
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

"""
엑셀 46개 포스트에 관련 글 내부 링크 버튼(최대 5개)을 본문 하단(FAQ 위)에 삽입.
거미줄처럼 서로 연결하여 체류시간·SEO를 개선.
"""
import json, urllib.request, urllib.error, base64, ssl, time, re

ssl._create_default_https_context = ssl._create_unverified_context
AUTH = base64.b64encode(b"strikers1999:zoahzjvl!@34").decode()
API = "https://devupbox.com/wp-json/wp/v2/posts"

# 46개 포스트 ID → slug → URL → title 매핑
POST_IDS = list(range(37503, 37549))

# 주제별 그룹 + 관련 slug 매핑 (각 포스트에 최대 5개 관련 글)
RELATED = {
    # === 무료 다운로드 그룹 ===
    "excel-free-download-guide": ["excel-web-free-version", "excel-student-free", "excel-mac-download", "excel-mobile-app-download", "excel-free-vs-paid"],
    "excel-web-free-version": ["excel-free-download-guide", "excel-online-browser", "excel-free-vs-paid", "excel-google-sheets-sync", "excel-free-alternative-2"],
    "excel-free-vs-paid": ["excel-free-download-guide", "excel-pricing-365", "excel-permanent-vs-subscription", "excel-web-free-version", "excel-365-vs-2021"],
    "excel-student-free": ["excel-free-download-guide", "excel-web-free-version", "excel-pricing-365", "excel-mac-download", "excel-free-alternative-2"],
    "excel-mac-download": ["excel-free-download-guide", "excel-student-free", "excel-ipad-usage", "excel-online-browser", "excel-mobile-vs-pc"],
    "excel-online-browser": ["excel-web-free-version", "excel-free-download-guide", "excel-google-sheets-sync", "excel-mobile-app-download", "excel-free-alternative-2"],
    "excel-mobile-app-download": ["excel-iphone-app", "excel-galaxy-app", "excel-mobile-usage", "excel-mobile-vs-pc", "excel-free-download-guide"],
    "excel-free-alternative-2": ["excel-web-free-version", "excel-free-download-guide", "excel-google-sheets-sync", "excel-online-browser", "excel-free-vs-paid"],

    # === 가격/구매 그룹 ===
    "excel-pricing-365": ["excel-permanent-vs-subscription", "microsoft-365-plans", "excel-365-vs-2021", "excel-free-vs-paid", "excel-product-key"],
    "excel-permanent-vs-subscription": ["excel-pricing-365", "excel-365-vs-2021", "microsoft-365-plans", "excel-2024-download", "excel-free-vs-paid"],
    "microsoft-365-plans": ["excel-pricing-365", "excel-permanent-vs-subscription", "excel-volume-license", "excel-student-free", "excel-365-vs-2021"],
    "excel-product-key": ["excel-pricing-365", "excel-install-error-fix", "excel-reinstall-guide", "excel-2024-download", "excel-volume-license"],
    "excel-volume-license": ["microsoft-365-plans", "excel-pricing-365", "excel-product-key", "excel-permanent-vs-subscription", "excel-2024-download"],

    # === 버전별 그룹 ===
    "excel-2024-download": ["excel-2021-download", "excel-365-vs-2021", "excel-permanent-vs-subscription", "excel-product-key", "excel-install-error-fix"],
    "excel-2021-download": ["excel-2024-download", "excel-365-vs-2021", "excel-2019-download", "excel-permanent-vs-subscription", "excel-product-key"],
    "excel-2019-download": ["excel-2021-download", "excel-2016-download", "excel-2024-download", "excel-365-vs-2021", "excel-free-download-guide"],
    "excel-2016-download": ["excel-2019-download", "excel-2021-download", "excel-file-compatibility", "excel-free-download-guide", "excel-viewer-download"],
    "excel-365-vs-2021": ["excel-pricing-365", "excel-permanent-vs-subscription", "excel-2024-download", "excel-2021-download", "excel-free-vs-paid"],

    # === 뷰어/파일 그룹 ===
    "excel-viewer-download": ["xlsx-open-without-excel", "excel-file-compatibility", "excel-free-download-guide", "excel-web-free-version", "excel-free-alternative-2"],
    "xlsx-open-without-excel": ["excel-viewer-download", "excel-file-compatibility", "excel-web-free-version", "excel-free-alternative-2", "excel-google-sheets-sync"],
    "excel-file-compatibility": ["xlsx-open-without-excel", "excel-viewer-download", "excel-2016-download", "excel-google-sheets-sync", "excel-pdf-one-page"],

    # === 설치/오류 그룹 ===
    "excel-install-error-fix": ["excel-reinstall-guide", "excel-product-key", "excel-windows-11", "excel-32bit-vs-64bit", "excel-slow-speed-fix"],
    "excel-reinstall-guide": ["excel-install-error-fix", "excel-product-key", "excel-slow-speed-fix", "excel-auto-save-recovery", "excel-windows-11"],
    "excel-slow-speed-fix": ["excel-reinstall-guide", "excel-install-error-fix", "excel-32bit-vs-64bit", "excel-auto-save-recovery", "excel-file-compatibility"],
    "excel-windows-11": ["excel-install-error-fix", "excel-32bit-vs-64bit", "excel-2024-download", "excel-reinstall-guide", "excel-product-key"],
    "excel-32bit-vs-64bit": ["excel-windows-11", "excel-install-error-fix", "excel-slow-speed-fix", "excel-2024-download", "excel-reinstall-guide"],

    # === PDF 그룹 ===
    "excel-pdf-one-page": ["pdf-table-to-excel", "excel-file-compatibility", "excel-viewer-download", "xlsx-open-without-excel", "excel-free-template-sites"],
    "pdf-table-to-excel": ["excel-pdf-one-page", "excel-file-compatibility", "xlsx-open-without-excel", "excel-google-sheets-sync", "excel-free-alternative-2"],

    # === 재테크 그룹 ===
    "excel-stock-portfolio": ["excel-savings-calculator", "excel-loan-calculator", "excel-asset-dashboard", "excel-blog-income-tracker", "excel-coupang-income"],
    "excel-savings-calculator": ["excel-loan-calculator", "excel-stock-portfolio", "excel-asset-dashboard", "excel-free-template-sites", "excel-budget-template"],
    "excel-loan-calculator": ["excel-savings-calculator", "excel-stock-portfolio", "excel-asset-dashboard", "excel-budget-template", "excel-free-template-sites"],
    "excel-asset-dashboard": ["excel-stock-portfolio", "excel-savings-calculator", "excel-loan-calculator", "excel-budget-template", "excel-blog-income-tracker"],

    # === 모바일 그룹 ===
    "excel-mobile-usage": ["excel-iphone-app", "excel-galaxy-app", "excel-mobile-vs-pc", "excel-ipad-usage", "excel-mobile-app-download"],
    "excel-iphone-app": ["excel-mobile-usage", "excel-galaxy-app", "excel-mobile-vs-pc", "excel-ipad-usage", "excel-mobile-app-download"],
    "excel-galaxy-app": ["excel-mobile-usage", "excel-iphone-app", "excel-mobile-vs-pc", "excel-ipad-usage", "excel-mobile-app-download"],
    "excel-mobile-vs-pc": ["excel-mobile-usage", "excel-iphone-app", "excel-galaxy-app", "excel-ipad-usage", "excel-web-free-version"],
    "excel-ipad-usage": ["excel-mobile-usage", "excel-mobile-vs-pc", "excel-mac-download", "excel-iphone-app", "excel-mobile-app-download"],

    # === 템플릿 그룹 ===
    "excel-free-template-sites": ["excel-project-template", "excel-sales-template", "excel-work-log-template", "excel-budget-template", "excel-blog-income-tracker"],
    "excel-project-template": ["excel-free-template-sites", "excel-work-log-template", "excel-budget-template", "excel-sales-template", "excel-asset-dashboard"],
    "excel-sales-template": ["excel-free-template-sites", "excel-budget-template", "excel-project-template", "excel-stock-portfolio", "excel-coupang-income"],
    "excel-work-log-template": ["excel-free-template-sites", "excel-project-template", "excel-budget-template", "excel-auto-save-recovery", "excel-sales-template"],
    "excel-budget-template": ["excel-free-template-sites", "excel-sales-template", "excel-project-template", "excel-asset-dashboard", "excel-savings-calculator"],

    # === 추가 주제 그룹 ===
    "excel-blog-income-tracker": ["excel-coupang-income", "excel-stock-portfolio", "excel-asset-dashboard", "excel-free-template-sites", "excel-sales-template"],
    "excel-google-sheets-sync": ["excel-free-alternative-2", "excel-web-free-version", "excel-online-browser", "excel-file-compatibility", "excel-auto-save-recovery"],
    "excel-auto-save-recovery": ["excel-reinstall-guide", "excel-slow-speed-fix", "excel-google-sheets-sync", "excel-install-error-fix", "excel-work-log-template"],
    "excel-coupang-income": ["excel-blog-income-tracker", "excel-stock-portfolio", "excel-asset-dashboard", "excel-sales-template", "excel-free-template-sites"],
}


def make_related_html(related_links):
    """관련 글 버튼 HTML 생성"""
    html = '<div style="background:#f8fafc;border-radius:12px;padding:28px 24px;margin:40px 0;">'
    html += '<p style="font-size:18px;font-weight:700;margin:0 0 16px;color:#1e293b;">📌 함께 읽으면 좋은 글</p>'
    html += '<div style="display:flex;flex-direction:column;gap:10px;">'
    for title, url in related_links:
        html += f'<a href="{url}" style="display:block;background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:14px 18px;text-decoration:none;color:#1e40af;font-weight:600;font-size:15px;transition:all 0.2s;" onmouseover="this.style.background=\'#eff6ff\';this.style.borderColor=\'#3b82f6\'" onmouseout="this.style.background=\'#fff\';this.style.borderColor=\'#e2e8f0\'">→ {title}</a>'
    html += '</div></div>'
    return html


def main():
    # 1단계: 모든 포스트의 slug → (id, title, link) 매핑 수집
    print("1단계: 포스트 정보 수집")
    post_map = {}  # slug → {id, title, link}
    for pid in POST_IDS:
        url = f"{API}/{pid}?_fields=id,slug,title,link"
        req = urllib.request.Request(url, headers={"Authorization": f"Basic {AUTH}"})
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
        time.sleep(0.2)
    print(f"\n수집 완료: {len(post_map)}개\n")

    # 2단계: 각 포스트에 관련 글 버튼 삽입
    print("2단계: 내부 링크 삽입")
    success = fail = skip = 0
    for slug, related_slugs in RELATED.items():
        if slug not in post_map:
            print(f"  SKIP | {slug} (없음)")
            skip += 1
            continue

        post = post_map[slug]
        pid = post["id"]

        # 관련 글의 title + link 수집
        related_links = []
        for rs in related_slugs:
            if rs in post_map:
                related_links.append((post_map[rs]["title"], post_map[rs]["link"]))

        if not related_links:
            print(f"  SKIP | {slug} (관련글 없음)")
            skip += 1
            continue

        # 현재 포스트 content 가져오기
        req = urllib.request.Request(f"{API}/{pid}?_fields=content", headers={"Authorization": f"Basic {AUTH}"})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = json.loads(resp.read().decode())["content"]["rendered"]
        except Exception as e:
            print(f"  FAIL | {slug} (내용 조회 실패: {e})")
            fail += 1
            continue

        # 이미 관련 글 섹션이 있으면 스킵
        if "함께 읽으면 좋은 글" in content:
            print(f"  SKIP | {slug} (이미 삽입됨)")
            skip += 1
            continue

        # FAQ 섹션 바로 앞에 관련 글 블록 삽입
        related_html = make_related_html(related_links)

        # FAQ h2 태그 찾기
        faq_pattern = r'(<h2[^>]*>자주 묻는 질문)'
        match = re.search(faq_pattern, content)
        if match:
            insert_pos = match.start()
            new_content = content[:insert_pos] + related_html + "\n" + content[insert_pos:]
        else:
            # FAQ가 없으면 맨 끝에 추가
            new_content = content + "\n" + related_html

        # 포스트 업데이트
        update_data = json.dumps({"content": new_content}).encode()
        req = urllib.request.Request(f"{API}/{pid}", data=update_data, method="POST")
        req.add_header("Authorization", f"Basic {AUTH}")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                json.loads(resp.read().decode())
                print(f"  OK | {slug} → {len(related_links)}개 링크")
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

"""
신용카드 30개 포스트의 이미지를 주제별로 다른 이미지로 교체하는 스크립트.
- 각 포스트마다 고유한 Unsplash 이미지 2장 (썸네일 + 본문)
- 기존 포스트(ID 35350~35379)의 featured_media와 본문 이미지를 업데이트
"""
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

# 포스트 ID 매핑 (slug -> post_id)
POST_IDS = {
    "cashback-credit-card-recommendation": 35350,
    "mileage-credit-card-recommendation": 35351,
    "gas-discount-credit-card": 35352,
    "telecom-discount-credit-card": 35353,
    "delivery-app-discount-credit-card": 35354,
    "mart-discount-credit-card": 35355,
    "transportation-credit-card": 35356,
    "online-shopping-credit-card": 35357,
    "office-worker-credit-card": 35358,
    "first-credit-card-recommendation": 35359,
    "business-credit-card-recommendation": 35360,
    "student-credit-card-recommendation": 35361,
    "housewife-credit-card-recommendation": 35362,
    "freelancer-credit-card-recommendation": 35363,
    "samsung-card-recommendation": 35364,
    "hyundai-card-recommendation": 35365,
    "shinhan-card-recommendation": 35366,
    "kb-card-recommendation": 35367,
    "lotte-card-recommendation": 35368,
    "woori-card-recommendation": 35369,
    "no-annual-fee-credit-card": 35370,
    "premium-credit-card-comparison": 35371,
    "check-card-recommendation": 35372,
    "plcc-card-recommendation": 35373,
    "postpaid-transportation-check-card": 35374,
    "credit-card-approval-requirements": 35375,
    "credit-card-limit-increase": 35376,
    "credit-card-cancellation-guide": 35377,
    "credit-card-point-cash-conversion": 35378,
    "credit-card-vs-check-card": 35379,
}

# 주제별 고유 이미지 매핑 (모든 ID 검증 완료)
IMAGES = {
    # 1. 캐시백 - 돈/지갑
    "cashback-credit-card-recommendation": [
        ("photo-1580519542036-c47de6196ba5", "캐시백으로 돌아오는 현금 혜택"),
        ("photo-1526304640581-d334cdbbf45e", "지갑 속 신용카드와 현금"),
    ],
    # 2. 마일리지 - 비행기/여행
    "mileage-credit-card-recommendation": [
        ("photo-1488085061387-422e29b40080", "마일리지 카드로 떠나는 공항"),
        ("photo-1517400508447-f8dd518b86db", "하늘 위 비행기 여행"),
    ],
    # 3. 주유 - 주유소/자동차
    "gas-discount-credit-card": [
        ("photo-1611605698335-8b1569810432", "주유소에서 주유하는 모습"),
        ("photo-1565043666747-69f6646db940", "주유 할인 카드로 절약"),
    ],
    # 4. 통신비 - 스마트폰
    "telecom-discount-credit-card": [
        ("photo-1523206489230-c012c64b2b48", "스마트폰 통신비 절약"),
        ("photo-1614680376573-df3480f0c6ff", "모바일 결제와 통신비 할인"),
    ],
    # 5. 배달앱 - 음식배달
    "delivery-app-discount-credit-card": [
        ("photo-1565299624946-b28f40a0ae38", "배달 음식 할인 혜택"),
        ("photo-1504674900247-0877df9cc836", "배달앱으로 주문한 맛있는 음식"),
    ],
    # 6. 대형마트 - 장보기
    "mart-discount-credit-card": [
        ("photo-1542838132-92c53300491e", "대형마트 장보기 할인"),
        ("photo-1583258292688-d0213dc5a3a8", "마트 카트에 가득한 장바구니"),
    ],
    # 7. 교통 - 대중교통
    "transportation-credit-card": [
        ("photo-1544620347-c4fd4a3d5957", "대중교통 버스 이용"),
        ("photo-1570125909232-eb263c188f7e", "지하철 교통카드 할인"),
    ],
    # 8. 온라인 쇼핑
    "online-shopping-credit-card": [
        ("photo-1460925895917-afdab827c52f", "온라인 쇼핑 웹사이트"),
        ("photo-1607082348824-0a96f2a4b9da", "스마트폰으로 온라인 쇼핑"),
    ],
    # 9. 직장인 - 오피스
    "office-worker-credit-card": [
        ("photo-1497215728101-856f4ea42174", "직장인의 깔끔한 오피스 데스크"),
        ("photo-1521737711867-e3b97375f902", "직장인 팀 회의 모습"),
    ],
    # 10. 사회초년생 - 첫 직장
    "first-credit-card-recommendation": [
        ("photo-1541339907198-e08756dedf3f", "사회초년생 졸업과 첫 시작"),
        ("photo-1573164713714-d95e436ab8d6", "새로운 시작을 준비하는 청년"),
    ],
    # 11. 자영업자 - 가게 운영
    "business-credit-card-recommendation": [
        ("photo-1556742044-3c52d6e88c62", "사업장 카드 결제 단말기"),
        ("photo-1450101499163-c8848c66ca85", "사업 서류와 경비 관리"),
    ],
    # 12. 대학생 - 캠퍼스
    "student-credit-card-recommendation": [
        ("photo-1517245386807-bb43f82c33c4", "대학생 캠퍼스 공부 모습"),
        ("photo-1516321318423-f06f85e504b3", "노트북으로 공부하는 학생"),
    ],
    # 13. 주부 - 가정 생활비
    "housewife-credit-card-recommendation": [
        ("photo-1556228578-0d85b1a4d571", "가정 생활비 절약 주방"),
        ("photo-1609220136736-443140cffec6", "가족 장보기와 생활비 관리"),
    ],
    # 14. 프리랜서 - 카페 작업
    "freelancer-credit-card-recommendation": [
        ("photo-1522202176988-66273c2fd55f", "카페에서 일하는 프리랜서"),
        ("photo-1521898284481-a5ec348cb555", "코워킹 스페이스 프리랜서"),
    ],
    # 15. 삼성카드 - 카드/결제
    "samsung-card-recommendation": [
        ("photo-1563986768494-4dee2763ff3f", "삼성카드 신용카드 비교"),
        ("photo-1556742502-ec7c0e9f34b1", "카드 결제 모습"),
    ],
    # 16. 현대카드 - 카드/디자인
    "hyundai-card-recommendation": [
        ("photo-1560472355-536de3962603", "현대카드 탭 결제"),
        ("photo-1621981386829-9b458a2cddde", "신용카드 탭 결제 모습"),
    ],
    # 17. 신한카드 - 금융/은행
    "shinhan-card-recommendation": [
        ("photo-1611974789855-9c2a0a7236a3", "신한카드 금융 차트 분석"),
        ("photo-1591696205602-2f950c417cb9", "카드 혜택 비교 분석"),
    ],
    # 18. KB국민카드 - 금융서비스
    "kb-card-recommendation": [
        ("photo-1579532537598-459ecdaf39cc", "KB카드 저금통 절약"),
        ("photo-1554224155-6726b3ff858f", "카드 혜택 서류 비교"),
    ],
    # 19. 롯데카드 - 쇼핑/백화점
    "lotte-card-recommendation": [
        ("photo-1483985988355-763728e1935b", "롯데카드 쇼핑 혜택"),
        ("photo-1607083206869-4c7672e72a8a", "백화점 쇼핑 카트"),
    ],
    # 20. 우리카드 - 은행/실속
    "woori-card-recommendation": [
        ("photo-1586281380349-632531db7ed4", "우리카드 금융 서류 관리"),
        ("photo-1496181133206-80ce9b88a853", "노트북으로 카드 혜택 비교"),
    ],
    # 21. 연회비 무료 - 무료/절약
    "no-annual-fee-credit-card": [
        ("photo-1559526324-593bc073d938", "연회비 무료 골드카드"),
        ("photo-1585338107529-13afc5f02586", "무료 혜택 비교"),
    ],
    # 22. 프리미엄 - 럭셔리/라운지
    "premium-credit-card-comparison": [
        ("photo-1540575467063-178a50c2df87", "프리미엄 카드 공항 라운지"),
        ("photo-1559526324-4b87b5e36e44", "프리미엄 럭셔리 서비스"),
    ],
    # 23. 체크카드 - ATM/직불
    "check-card-recommendation": [
        ("photo-1556742111-a301076d9d18", "체크카드 결제 단말기"),
        ("photo-1563013544-824ae1b704d3", "스마트폰 체크카드 관리"),
    ],
    # 24. PLCC - 브랜드 제휴
    "plcc-card-recommendation": [
        ("photo-1472851294608-062f824d29cc", "PLCC 브랜드 제휴 쇼핑"),
        ("photo-1604719312566-8912e9227c6a", "브랜드 매장 쇼핑 혜택"),
    ],
    # 25. 후불교통 체크카드
    "postpaid-transportation-check-card": [
        ("photo-1570125909232-eb263c188f7e", "후불교통 지하철 이용"),
        ("photo-1544620347-c4fd4a3d5957", "버스 후불교통 체크카드"),
    ],
    # 26. 발급 조건 - 서류/심사
    "credit-card-approval-requirements": [
        ("photo-1450101499163-c8848c66ca85", "카드 발급 심사 서류"),
        ("photo-1507003211169-0a1dd7228f2d", "카드 발급 상담"),
    ],
    # 27. 한도 올리기 - 성장/증가
    "credit-card-limit-increase": [
        ("photo-1611974789855-9c2a0a7236a3", "카드 한도 상향 그래프"),
        ("photo-1454165804606-c3d57bc86b40", "한도 상향 업무 처리"),
    ],
    # 28. 해지 - 가위/정리
    "credit-card-cancellation-guide": [
        ("photo-1554224155-6726b3ff858f", "카드 해지 서류 확인"),
        ("photo-1586281380349-632531db7ed4", "카드 정리 체크리스트"),
    ],
    # 29. 포인트 전환 - 보상/선물
    "credit-card-point-cash-conversion": [
        ("photo-1579532537598-459ecdaf39cc", "포인트 현금 전환 저금통"),
        ("photo-1580519542036-c47de6196ba5", "포인트를 현금으로 전환"),
    ],
    # 30. 신용카드 vs 체크카드 - 비교
    "credit-card-vs-check-card": [
        ("photo-1563986768494-4dee2763ff3f", "신용카드와 체크카드 비교"),
        ("photo-1556742044-3c52d6e88c62", "카드 선택 결제 비교"),
    ],
}


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
        print(f"  이미지 다운로드 실패 ({photo_id}): {e}")
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
            return media_id, media_url
    except Exception as e:
        print(f"  WP 업로드 실패: {e}")
        return None, None


def update_post(post_id, featured_media_id, img1_url, img1_alt, img2_url, img2_alt):
    """기존 포스트의 featured_media와 본문 이미지 교체"""
    # 1. 포스트 내용 가져오기
    req = urllib.request.Request(f"{API}/{post_id}")
    req.add_header("Authorization", f"Basic {AUTH}")
    try:
        with urllib.request.urlopen(req) as resp:
            post = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  포스트 조회 실패: {e}")
        return False

    content = post.get("content", {}).get("rendered", "")

    # 2. 기존 이미지 figure 태그를 새 이미지로 교체
    import re
    figures = list(re.finditer(r'<figure[^>]*>.*?</figure>', content, re.DOTALL))

    if len(figures) >= 1 and img1_url:
        new_fig1 = f'''<figure style="margin:32px 0;text-align:center;">
<img src="{img1_url}" alt="{img1_alt}" style="width:100%;max-width:800px;height:auto;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.10);" loading="lazy" />
<figcaption style="margin-top:8px;font-size:13px;color:#6b7280;">{img1_alt}</figcaption>
</figure>'''
        content = content[:figures[0].start()] + new_fig1 + content[figures[0].end():]
        # 재검색 (content 변경됨)
        figures = list(re.finditer(r'<figure[^>]*>.*?</figure>', content, re.DOTALL))

    if len(figures) >= 2 and img2_url:
        new_fig2 = f'''<figure style="margin:32px 0;text-align:center;">
<img src="{img2_url}" alt="{img2_alt}" style="width:100%;max-width:800px;height:auto;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.10);" loading="lazy" />
<figcaption style="margin-top:8px;font-size:13px;color:#6b7280;">{img2_alt}</figcaption>
</figure>'''
        content = content[:figures[1].start()] + new_fig2 + content[figures[1].end():]

    # 이미지가 없는 경우 (figure 태그 0개) - 인트로 뒤에 삽입
    if len(figures) == 0 and img1_url:
        first_h2 = content.find('<h2')
        if first_h2 > 0:
            new_fig1 = f'''<figure style="margin:32px 0;text-align:center;">
<img src="{img1_url}" alt="{img1_alt}" style="width:100%;max-width:800px;height:auto;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.10);" loading="lazy" />
<figcaption style="margin-top:8px;font-size:13px;color:#6b7280;">{img1_alt}</figcaption>
</figure>'''
            content = content[:first_h2] + new_fig1 + "\n" + content[first_h2:]

    # 3. 포스트 업데이트
    update_payload = {"content": content}
    if featured_media_id:
        update_payload["featured_media"] = featured_media_id

    data = json.dumps(update_payload).encode("utf-8")
    req = urllib.request.Request(f"{API}/{post_id}", data=data, method="POST")
    req.add_header("Authorization", f"Basic {AUTH}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            json.loads(resp.read().decode("utf-8"))
            return True
    except Exception as e:
        print(f"  포스트 업데이트 실패: {e}")
        return False


def main():
    total = len(IMAGES)
    print("=" * 60)
    print(f"신용카드 {total}개 포스트 이미지 교체 시작")
    print("=" * 60)

    success = 0
    for idx, (slug, img_list) in enumerate(IMAGES.items(), 1):
        post_id = POST_IDS.get(slug)
        if not post_id:
            print(f"[{idx}/{total}] SKIP | {slug} (ID 없음)")
            continue

        print(f"\n[{idx}/{total}] {slug} (ID: {post_id})")

        uploaded = []
        for img_idx, (photo_id, alt_text) in enumerate(img_list):
            filename = f"cc-{slug}-{img_idx+1}"
            tmp_path = download_image(photo_id)
            if not tmp_path:
                uploaded.append((None, None, alt_text))
                continue
            media_id, wp_url = upload_image_to_wp(tmp_path, filename, alt_text)
            os.unlink(tmp_path)
            if wp_url:
                uploaded.append((media_id, wp_url, alt_text))
                print(f"  이미지 {img_idx+1} OK: {wp_url}")
            else:
                uploaded.append((None, None, alt_text))
            time.sleep(0.3)

        # 포스트 업데이트
        featured_id = uploaded[0][0] if uploaded else None
        img1_url = uploaded[0][1] if len(uploaded) > 0 else None
        img1_alt = uploaded[0][2] if len(uploaded) > 0 else ""
        img2_url = uploaded[1][1] if len(uploaded) > 1 else None
        img2_alt = uploaded[1][2] if len(uploaded) > 1 else ""

        if update_post(post_id, featured_id, img1_url, img1_alt, img2_url, img2_alt):
            print(f"  포스트 업데이트 OK")
            success += 1
        else:
            print(f"  포스트 업데이트 FAIL")
        time.sleep(0.5)

    print(f"\n{'=' * 60}")
    print(f"완료! 성공: {success}/{total}")
    print("=" * 60)


if __name__ == "__main__":
    main()

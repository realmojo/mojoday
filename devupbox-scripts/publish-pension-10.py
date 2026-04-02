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


def download_image(photo_id):
    url = f"https://images.unsplash.com/{photo_id}?w=800&h=450&fit=crop&auto=format&q=80"
    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            tmp.write(resp.read())
        tmp.close()
        return tmp.name
    except Exception as e:
        tmp.close()
        os.unlink(tmp.name)
        print(f"  이미지 다운로드 실패: {e}")
        return None


def upload_image(file_path, filename, alt_text):
    with open(file_path, "rb") as f:
        data = f.read()
    req = urllib.request.Request(MEDIA_API, data=data, method="POST")
    req.add_header("Authorization", f"Basic {AUTH}")
    req.add_header("Content-Type", "image/jpeg")
    req.add_header("Content-Disposition", f'attachment; filename="{filename}.jpg"')
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            r = json.loads(resp.read().decode())
            mid = r.get("id")
            murl = r.get("source_url", "")
            if mid:
                ud = json.dumps({"alt_text": alt_text}).encode()
                ur = urllib.request.Request(f"{MEDIA_API}/{mid}", data=ud, method="POST")
                ur.add_header("Authorization", f"Basic {AUTH}")
                ur.add_header("Content-Type", "application/json")
                try: urllib.request.urlopen(ur, timeout=15)
                except: pass
            return mid, murl
    except Exception as e:
        print(f"  업로드 실패: {e}")
        return None, None


def img_block(url, alt):
    return f'''<!-- wp:image {{"sizeSlug":"large"}} -->
<figure class="wp-block-image size-large"><img src="{url}" alt="{alt}"/><figcaption class="wp-element-caption">{alt}</figcaption></figure>
<!-- /wp:image -->'''


def cta_block(text, desc, url, style="blue"):
    styles = {
        "blue": {"bg": "linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%)", "btn_bg": "#fff", "btn_color": "#1e3a5f", "text_color": "#fff", "desc_color": "#cde0f5", "border": "none"},
        "yellow": {"bg": "#fffbeb", "btn_bg": "#f59e0b", "btn_color": "#fff", "text_color": "#92400e", "desc_color": "#78716c", "border": "2px solid #f59e0b"},
        "green": {"bg": "linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)", "btn_bg": "#fff", "btn_color": "#0f766e", "text_color": "#fff", "desc_color": "#ccfbf1", "border": "none"},
    }
    s = styles[style]
    return f'''<div style="background:{s['bg']};border:{s['border']};border-radius:12px;padding:28px 32px;margin:32px 0;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;">
  <div>
    <p style="margin:0 0 6px;font-size:18px;font-weight:700;color:{s['text_color']};">{text}</p>
    <p style="margin:0;font-size:14px;color:{s['desc_color']};">{desc}</p>
  </div>
  <a href="{url}" target="_blank" rel="noopener noreferrer"
     style="background:{s['btn_bg']};color:{s['btn_color']};padding:12px 24px;border-radius:8px;font-weight:700;text-decoration:none;white-space:nowrap;font-size:15px;">
    바로가기 &rarr;
  </a>
</div>'''


def post1_content(imgs):
    cta1 = cta_block("복지로 모의계산 바로가기", "기초연금 수급 가능 여부를 온라인으로 즉시 확인하세요", "https://www.bokjiro.go.kr", "blue")
    cta2 = cta_block("국민연금공단 상담 신청", "전국 지사에서 1:1 무료 상담을 받아보세요", "https://www.nps.or.kr", "yellow")
    cta3 = cta_block("KB부동산 시세 확인", "아파트 시세를 정확히 파악하고 소득인정액을 계산하세요", "https://kbland.kr", "green")
    return f'''<!-- wp:paragraph -->
<p>2026년 기준 기초연금을 받으려면 소득인정액이 단독가구 월 <strong>2,228,000원</strong>, 부부가구 월 <strong>3,564,800원</strong> 이하여야 합니다. 아파트를 보유하고 있다면 해당 재산이 소득으로 환산되어 수급 여부에 직접 영향을 줍니다. 이 글에서는 재산의 소득환산액 계산법부터 아파트 시가별 실제 사례까지 상세히 안내합니다.</p>
<!-- /wp:paragraph -->

{imgs[0]}

<!-- wp:heading {{"level":2}} -->
<h2>재산의 소득환산액이란 무엇인가</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>기초연금 심사에서는 현금 소득 외에 부동산·금융재산 등을 <strong>소득으로 환산</strong>하여 합산합니다. 이를 소득인정액이라 하며, 공식은 다음과 같습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="background:#f8fafc;border-left:4px solid #2d5a8e;padding:20px 24px;margin:24px 0;border-radius:0 8px 8px 0;">
  <p style="margin:0;font-size:15px;font-weight:700;color:#1e3a5f;">소득인정액 계산 공식</p>
  <p style="margin:8px 0 0;font-size:14px;color:#334155;">소득인정액 = 월 소득평가액 + 재산의 월 소득환산액</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;">재산의 월 소득환산액 = (재산 - 기본재산액 - 부채) × 소득환산율(연 4%) ÷ 12</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>여기서 <strong>기본재산액</strong>은 지역에 따라 공제되는 금액으로, 생활에 필요한 기본 재산은 소득으로 보지 않겠다는 취지입니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":2}} -->
<h2>지역별 기본재산액 공제 기준 (2026년)</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">지역 구분</th>
  <th style="padding:12px 16px;text-align:center;">해당 지역 예시</th>
  <th style="padding:12px 16px;text-align:right;">기본재산액 공제</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">대도시</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">서울, 경기 주요 시, 광역시 구</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;font-weight:700;">1억 3,500만 원</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">중소도시</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">경기 군·중소 시, 광역시 군</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;font-weight:700;">8,500만 원</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;">농어촌</td>
  <td style="padding:12px 16px;text-align:center;">읍·면 지역</td>
  <td style="padding:12px 16px;text-align:right;font-weight:700;">7,250만 원</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>공제 금액을 초과하는 재산 부분만 소득으로 환산됩니다. 따라서 대도시에 거주하는 경우 1억 3,500만 원까지는 재산이 있어도 소득으로 보지 않습니다.</p>
<!-- /wp:paragraph -->

{cta1}

<!-- wp:heading {{"level":2}} -->
<h2>아파트 시가 기준 소득환산 계산 예시</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>아파트의 재산 가액은 <strong>공시가격</strong>을 기준으로 합니다. 공시가격은 국토교통부 부동산 공시가격 알리미에서 확인할 수 있으며, 일반적으로 시세의 60~70% 수준입니다. 아래는 대도시 기준 계산 예시입니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">아파트 시세</th>
  <th style="padding:12px 16px;text-align:right;">추정 공시가격</th>
  <th style="padding:12px 16px;text-align:right;">기본재산액 공제 후</th>
  <th style="padding:12px 16px;text-align:right;">월 소득환산액</th>
  <th style="padding:12px 16px;text-align:center;">수급 가능성</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">2억 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">약 1억 3,000만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">0원 (공제 내)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;color:#16a34a;font-weight:700;">0원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#16a34a;">높음</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">3억 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">약 1억 9,500만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">약 6,000만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;color:#d97706;font-weight:700;">약 200,000원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#d97706;">중간</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;">5억 원</td>
  <td style="padding:12px 16px;text-align:right;">약 3억 2,500만 원</td>
  <td style="padding:12px 16px;text-align:right;">약 1억 9,000만 원</td>
  <td style="padding:12px 16px;text-align:right;color:#dc2626;font-weight:700;">약 633,333원</td>
  <td style="padding:12px 16px;text-align:center;color:#dc2626;">낮음</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>위 계산에서 보듯 시세 3억 원 아파트의 경우 재산으로 인한 월 소득환산액은 약 20만 원으로, 다른 소득이 없다면 기초연금 수급이 충분히 가능합니다. 반면 5억 원 이상 아파트 보유자는 재산 환산액만으로 선정기준액의 상당 부분을 차지하게 됩니다.</p>
<!-- /wp:paragraph -->

{imgs[1]}

<!-- wp:heading {{"level":2}} -->
<h2>전월세 보증금은 어떻게 반영되나</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>임차보증금(전세 또는 월세 보증금)도 재산으로 산정됩니다. 계산 방식은 다음과 같습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="background:#f8fafc;border-left:4px solid #14b8a6;padding:20px 24px;margin:24px 0;border-radius:0 8px 8px 0;">
  <p style="margin:0;font-size:15px;font-weight:700;color:#0f766e;">임차보증금 소득환산</p>
  <p style="margin:8px 0 0;font-size:14px;color:#334155;">임차보증금 전액을 재산으로 봅니다.</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;">예: 전세 보증금 1억 원 → 1억 원을 재산에 합산</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;">월세의 경우: 보증금 + (월세 × 240) 중 낮은 금액을 재산으로 산정</p>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>단, 전세 보증금에서 전세대출 잔액은 부채로 차감됩니다. 따라서 전세자금 대출이 있다면 반드시 신청 시 관련 서류를 제출하여 부채를 인정받아야 합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":2}} -->
<h2>재산 기준 초과 시 대안 및 절세 전략</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>재산 초과로 기초연금을 받지 못한다고 판단될 경우, 합법적으로 소득인정액을 낮출 수 있는 방법이 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
  <li><strong>주택담보대출 활용:</strong> 주택담보대출 잔액은 부채로 인정되어 재산에서 차감됩니다. 단, 대출 자금을 다시 금융재산으로 보유하면 상쇄됩니다.</li>
  <li><strong>주거급여 신청:</strong> 소득인정액이 기준 이하라면 기초연금과 병행하여 주거급여도 수급 가능합니다.</li>
  <li><strong>증여 후 5년 경과:</strong> 재산을 증여한 경우 증여 후 5년이 경과하면 재산 산정에서 제외됩니다. 단, 5년 이내 증여는 재산으로 포함됩니다.</li>
  <li><strong>이의신청:</strong> 공시가격 산정 오류가 있는 경우 이의신청을 통해 재산 가액 정정이 가능합니다.</li>
</ul>
<!-- /wp:list -->

{cta2}

<!-- wp:heading {{"level":2}} -->
<h2>자주 묻는 질문 (FAQ)</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="margin:32px 0;">

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 아파트 공시가격은 어디서 확인하나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">국토교통부 부동산 공시가격 알리미(공시가격알리미.kr) 또는 국토교통부 홈페이지에서 주소 검색으로 확인할 수 있습니다. 매년 4월 말에 공시가격이 갱신되며, 기초연금 심사는 해당 연도 공시가격을 기준으로 합니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 재개발·재건축 예정 아파트는 어떻게 산정되나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">재개발·재건축 예정 구역의 아파트도 공시가격을 기준으로 산정됩니다. 단, 관리처분계획인가 이후 분양권으로 전환된 경우에는 분양권 가액을 재산으로 봅니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 아파트가 배우자 명의인 경우 어떻게 되나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">배우자 명의의 재산도 부부합산으로 소득인정액에 포함됩니다. 기초연금은 가구 단위로 심사하므로 배우자의 재산과 소득을 모두 합산하여 판단합니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 아파트 외 상가·토지도 함께 보유하고 있으면 어떻게 계산되나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">아파트, 상가, 토지 등 모든 부동산 재산이 합산됩니다. 각각의 공시가격을 합산한 후 기본재산액을 공제하고 소득환산율 4%를 적용합니다. 여러 부동산을 보유할수록 소득인정액이 높아지므로 불필요한 부동산은 정리하는 것이 유리할 수 있습니다.</p>
</div>

</div>
<!-- /wp:html -->

{cta3}
'''


def post2_content(imgs):
    cta1 = cta_block("복지로 부부 모의계산", "부부 각각의 소득인정액을 계산하고 수급 전략을 세워보세요", "https://www.bokjiro.go.kr", "blue")
    cta2 = cta_block("국민연금공단 상담 신청", "부부 기초연금 수령 전략에 대해 전문 상담을 받으세요", "https://www.nps.or.kr", "yellow")
    cta3 = cta_block("복지로 급여신청 바로가기", "온라인으로 간편하게 기초연금을 신청하세요", "https://www.bokjiro.go.kr/ssis-tbu/twatbz/mkclAsis/mkclBstrPage.do", "green")
    return f'''<!-- wp:paragraph -->
<p>기초연금 부부 감액 제도는 많은 어르신들이 예상치 못한 부분입니다. 부부가 함께 기초연금을 신청하면 각자 받을 수 있는 금액의 <strong>80%만 지급</strong>됩니다. 2026년 기준 최대 기초연금액은 단독 가구 월 <strong>342,510원</strong>이지만, 부부 모두 받는 경우 각각 <strong>274,010원</strong>(약 80%)으로 감액됩니다. 이 글에서는 부부 감액 계산법과 최적의 수령 전략을 상세히 안내합니다.</p>
<!-- /wp:paragraph -->

{imgs[0]}

<!-- wp:heading {{"level":2}} -->
<h2>부부 감액 20% 규정의 배경</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>부부 감액 규정은 함께 생활하는 부부는 단독 가구보다 생활비가 적게 든다는 점을 반영한 것입니다. 혼자 사는 어르신과 부부가 함께 사는 경우의 생활비 차이를 고려하여, 부부가 모두 수급 자격을 갖춘 경우에는 각자의 기초연금을 80%씩 지급합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="background:#f8fafc;border-left:4px solid #2d5a8e;padding:20px 24px;margin:24px 0;border-radius:0 8px 8px 0;">
  <p style="margin:0;font-size:15px;font-weight:700;color:#1e3a5f;">2026년 기초연금 부부 수령액 비교</p>
  <p style="margin:8px 0 0;font-size:14px;color:#334155;">단독 수령 (한 명만 해당): 월 최대 342,510원</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;">부부 각각 수령: 월 각 최대 274,010원 (합계 548,020원)</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;font-weight:700;">→ 부부 합계로는 단독의 약 1.6배 수령</p>
</div>
<!-- /wp:html -->

<!-- wp:heading {{"level":2}} -->
<h2>부부 합산 선정기준액 이해하기</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>부부 가구의 선정기준액은 단독 가구의 160%로 설정됩니다. 2026년 기준은 다음과 같습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">가구 유형</th>
  <th style="padding:12px 16px;text-align:right;">선정기준액 (월)</th>
  <th style="padding:12px 16px;text-align:right;">최대 기초연금</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">단독 가구</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">2,228,000원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;font-weight:700;">342,510원</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;">부부 가구 (합산)</td>
  <td style="padding:12px 16px;text-align:right;">3,564,800원</td>
  <td style="padding:12px 16px;text-align:right;font-weight:700;">각 274,010원 (합 548,020원)</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>부부 가구의 선정기준액은 두 사람의 소득인정액을 합산하여 판단합니다. 예를 들어, 남편 소득인정액 200만 원, 아내 소득인정액 100만 원이라면 합산 300만 원으로, 부부 기준 356만 4,800원 이하이므로 둘 다 수급 가능합니다.</p>
<!-- /wp:paragraph -->

{cta1}

{imgs[1]}

<!-- wp:heading {{"level":2}} -->
<h2>한 명만 신청 vs 둘 다 신청 비교 분석</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>배우자 중 한 명이 기준을 초과하거나 수급을 원하지 않는 경우, 한 명만 신청하는 것이 유리할 수 있습니다. 다음 비교를 참고하세요.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">구분</th>
  <th style="padding:12px 16px;text-align:center;">한 명만 신청</th>
  <th style="padding:12px 16px;text-align:center;">둘 다 신청</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">월 수령액</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">최대 342,510원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">각 274,010원 (합 548,020원)</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">소득인정액 계산</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">신청자만 단독 기준 적용</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">부부 합산 기준 적용</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">유리한 경우</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">배우자 소득이 높아 합산 시 기준 초과 우려</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">둘 다 소득이 낮아 합산 후에도 기준 이하</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;">주의사항</td>
  <td style="padding:12px 16px;text-align:center;">배우자 재산도 소득인정액에 반영됨</td>
  <td style="padding:12px 16px;text-align:center;">각 20% 감액되나 합산액은 더 큼</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>중요한 점은, 한 명만 신청하더라도 배우자의 소득과 재산은 계속 소득인정액 계산에 포함된다는 것입니다. 배우자 명의의 재산도 함께 산정되므로 전략적으로 판단해야 합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":2}} -->
<h2>감액 최소화 전략</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>부부 감액을 완전히 피할 수는 없지만, 다음과 같은 방법으로 총 수령액을 최적화할 수 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
  <li><strong>배우자 소득인정액 낮추기:</strong> 배우자 명의의 금융재산을 정리하거나, 부채를 증빙하여 소득인정액을 낮추면 부부 합산 기준 내에서 둘 다 수급이 가능합니다.</li>
  <li><strong>시기 조절:</strong> 배우자가 65세가 되어 수급 자격이 생기는 시점을 계획적으로 활용합니다.</li>
  <li><strong>가구원 분리:</strong> 법적으로 이혼하지 않는 한 주민등록 분리로는 부부 가구 판정을 피할 수 없습니다. 실제 별거 중인 경우에는 읍면동 주민센터에 사실 확인을 요청할 수 있습니다.</li>
</ul>
<!-- /wp:list -->

{cta2}

<!-- wp:heading {{"level":2}} -->
<h2>자주 묻는 질문 (FAQ)</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="margin:32px 0;">

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 부부 중 한 명이 기초연금 수급 중에 배우자가 65세가 되면 어떻게 되나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">배우자가 65세가 되어 기초연금을 신청하면 기존 수급자의 연금도 부부 감액(80%)으로 자동 조정됩니다. 따라서 배우자가 65세가 되면 읍면동 주민센터에 변경 신고를 해야 하며, 조정 전까지는 기존 금액이 지급됩니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 배우자가 사망하면 감액이 해제되나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">네, 배우자가 사망하면 단독 가구로 전환되어 감액이 해제됩니다. 이 경우 가능한 빨리 읍면동 주민센터에 신고하면 변경 월부터 단독 가구 기준으로 지급됩니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 부부 중 한 명이 시설에 입소하면 어떻게 되나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">요양시설 등에 입소한 경우에는 별도 가구로 보아 부부 감액이 적용되지 않을 수 있습니다. 다만, 시설 입소자는 기초연금 수급 시 시설 운영자에게 일부가 지급될 수 있으므로 시설 측과 확인이 필요합니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 사실혼 관계도 부부로 보나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">사실혼 관계는 법적으로 부부로 인정되지 않으므로 기초연금에서도 각각 단독 가구로 봅니다. 단, 주민등록상 같은 주소에 거주하더라도 법적 혼인관계가 없으면 부부 감액이 적용되지 않습니다.</p>
</div>

</div>
<!-- /wp:html -->

{cta3}
'''


def post3_content(imgs):
    cta1 = cta_block("국민연금 수령액 조회", "내 국민연금 예상 수령액을 미리 확인하세요", "https://www.nps.or.kr", "blue")
    cta2 = cta_block("복지로 모의계산", "국민연금과 기초연금 합산 수령액을 계산해보세요", "https://www.bokjiro.go.kr", "yellow")
    cta3 = cta_block("기초연금 신청 바로가기", "65세 이상이라면 지금 바로 신청하세요", "https://www.bokjiro.go.kr", "green")
    return f'''<!-- wp:paragraph -->
<p>국민연금을 받고 있으면 기초연금이 깎인다는 말을 들어보셨을 것입니다. 이를 <strong>연계감액 제도</strong>라고 하는데, 모든 국민연금 수급자에게 해당되는 것은 아닙니다. 2026년 기준으로 국민연금 수령액이 <strong>월 515,000원(기초연금 최대액의 150%)</strong>을 초과해야 감액이 시작됩니다. 이 글에서 연계감액 계산법을 완전히 이해해 드립니다.</p>
<!-- /wp:paragraph -->

{imgs[0]}

<!-- wp:heading {{"level":2}} -->
<h2>연계감액 제도란 무엇인가</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>연계감액 제도는 국민연금 가입 기간이 길고 국민연금 수령액이 많은 분들에게 기초연금을 일부 또는 전부 감액하는 제도입니다. 국민연금을 많이 냈으니 기초연금은 덜 받아야 한다는 논리로 도입되었습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="background:#f8fafc;border-left:4px solid #2d5a8e;padding:20px 24px;margin:24px 0;border-radius:0 8px 8px 0;">
  <p style="margin:0;font-size:15px;font-weight:700;color:#1e3a5f;">연계감액 적용 조건 (2026년)</p>
  <p style="margin:8px 0 0;font-size:14px;color:#334155;">국민연금 월 수령액이 기초연금 기준연금액의 150%를 초과할 때</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;">2026년 기준: 342,510원 × 150% = 513,765원 → 약 515,000원 초과 시 감액</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;font-weight:700;">→ 국민연금 월 515,000원 이하 수급자는 연계감액 없음</p>
</div>
<!-- /wp:html -->

<!-- wp:heading {{"level":2}} -->
<h2>연계감액 계산 공식과 예시</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>연계감액이 적용되면 기초연금은 다음 공식에 따라 감액됩니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="background:#f8fafc;border-left:4px solid #14b8a6;padding:20px 24px;margin:24px 0;border-radius:0 8px 8px 0;">
  <p style="margin:0;font-size:15px;font-weight:700;color:#0f766e;">연계감액 계산 공식</p>
  <p style="margin:8px 0 0;font-size:14px;color:#334155;">기초연금액 = 기준연금액 - (국민연금 월 수령액 - 기준연금액 × 150%) × 2/3</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;">단, 기초연금액이 기준연금액의 50% 미만이 되면 기준연금액의 50%로 고정</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;">즉, 최소 보장액 = 342,510원 × 50% = 약 171,255원</p>
</div>
<!-- /wp:html -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">국민연금 월 수령액</th>
  <th style="padding:12px 16px;text-align:right;">기초연금 감액 여부</th>
  <th style="padding:12px 16px;text-align:right;">실제 수령 기초연금</th>
  <th style="padding:12px 16px;text-align:right;">합계 (국민+기초)</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">30만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;color:#16a34a;">감액 없음</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;font-weight:700;">342,510원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">642,510원</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">50만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;color:#16a34a;">감액 없음</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;font-weight:700;">342,510원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">842,510원</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">70만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;color:#d97706;">일부 감액</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;font-weight:700;">약 217,000원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">약 917,000원</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">100만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;color:#d97706;">일부 감액</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;font-weight:700;">약 171,255원 (최소보장)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">약 1,171,255원</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;">150만 원</td>
  <td style="padding:12px 16px;text-align:right;color:#d97706;">최소보장 적용</td>
  <td style="padding:12px 16px;text-align:right;font-weight:700;">약 171,255원 (최소보장)</td>
  <td style="padding:12px 16px;text-align:right;">약 1,671,255원</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

{cta1}

{imgs[1]}

<!-- wp:heading {{"level":2}} -->
<h2>유족연금·장애연금과 기초연금의 관계</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>국민연금의 노령연금뿐 아니라 유족연금과 장애연금을 받는 경우에도 기초연금 수급이 가능합니다. 다만, 수령액이 소득인정액에 포함되어 선정기준액을 초과하면 기초연금을 받을 수 없게 됩니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">연금 종류</th>
  <th style="padding:12px 16px;text-align:center;">기초연금 동시 수급</th>
  <th style="padding:12px 16px;text-align:center;">연계감액 적용</th>
  <th style="padding:12px 16px;text-align:left;">비고</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">노령연금</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#16a34a;">가능</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#d97706;">적용</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">515,000원 초과 시 감액</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">유족연금</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#16a34a;">가능</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#16a34a;">미적용</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">소득인정액에는 반영</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">장애연금</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#16a34a;">가능</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#16a34a;">미적용</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">소득인정액에는 반영</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;">공무원·군인·사학연금</td>
  <td style="padding:12px 16px;text-align:center;color:#dc2626;">불가</td>
  <td style="padding:12px 16px;text-align:center;">해당없음</td>
  <td style="padding:12px 16px;">수급 자격 자체 없음</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

{cta2}

<!-- wp:heading {{"level":2}} -->
<h2>자주 묻는 질문 (FAQ)</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="margin:32px 0;">

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 국민연금을 받다가 기초연금 신청을 안 하면 손해인가요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">네, 기초연금은 자동으로 지급되는 것이 아니라 직접 신청해야 합니다. 65세 생일이 속하는 달의 1개월 전부터 신청할 수 있으며, 신청하지 않으면 지급되지 않습니다. 소급 지급은 신청일 기준으로 최대 소급이 제한되므로 빨리 신청하는 것이 유리합니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 국민연금 가입 기간이 짧으면 연계감액이 없나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">연계감액은 수령액 기준이지 가입 기간 기준이 아닙니다. 가입 기간이 짧아도 수령액이 월 515,000원을 초과하면 감액됩니다. 반대로 오래 가입해도 수령액이 이 기준 이하면 감액 없이 기초연금 전액을 받을 수 있습니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 국민연금을 반납하면 기초연금을 더 받을 수 있나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">국민연금 반납(반환일시금 수령) 후에는 더 이상 국민연금 수급자가 아니게 되어 연계감액 적용을 피할 수 있습니다. 그러나 반납한 국민연금 총액과 향후 기초연금 추가 수령액을 비교하여 득실을 계산해야 하며, 노후 생활비 보장 측면에서 신중히 결정해야 합니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 국민연금 조기수령 신청 시 기초연금에 영향이 있나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">국민연금을 조기수령하면 수령액이 감소하므로, 연계감액 적용 여부가 달라질 수 있습니다. 예를 들어 정상 수령 시 70만 원이지만 조기수령 시 56만 원이라면, 조기수령 시 연계감액이 줄어들어 기초연금을 더 받을 수 있습니다. 다만 65세 미만이면 기초연금을 받을 수 없으므로, 조기수령 기간 동안은 기초연금 수급이 불가합니다.</p>
</div>

</div>
<!-- /wp:html -->

{cta3}
'''


def post4_content(imgs):
    cta1 = cta_block("복지로 소득인정액 모의계산", "탈락 전에 미리 계산해서 수급 가능성을 확인하세요", "https://www.bokjiro.go.kr", "blue")
    cta2 = cta_block("국민연금공단 이의신청 안내", "부당하게 탈락했다면 이의신청 절차를 확인하세요", "https://www.nps.or.kr", "yellow")
    cta3 = cta_block("주민센터 방문 상담 예약", "가까운 주민센터에서 1:1 상담을 받아보세요", "https://www.bokjiro.go.kr", "green")
    return f'''<!-- wp:paragraph -->
<p>기초연금 신청 후 탈락 통보를 받으면 당황스럽습니다. 탈락에는 반드시 이유가 있으며, 이유를 정확히 파악해야 대책을 세울 수 있습니다. 2026년 기준으로 가장 많이 발생하는 탈락 사유 5가지와 각각의 해결책을 정리했습니다.</p>
<!-- /wp:paragraph -->

{imgs[0]}

<!-- wp:heading {{"level":2}} -->
<h2>탈락 사유 1위: 고가 부동산 보유</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>가장 많은 탈락 사유는 부동산 재산이 많아 소득인정액이 선정기준액을 초과하는 경우입니다. 특히 서울·수도권 아파트 보유자가 해당됩니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="background:#fef2f2;border-left:4px solid #dc2626;padding:20px 24px;margin:24px 0;border-radius:0 8px 8px 0;">
  <p style="margin:0;font-size:15px;font-weight:700;color:#991b1b;">탈락 기준 예시 (대도시 단독 가구)</p>
  <p style="margin:8px 0 0;font-size:14px;color:#334155;">선정기준액: 월 2,228,000원</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;">공시가격 4억 원 아파트(다른 소득 없음): (4억 - 1억 3,500만) × 4% ÷ 12 = 월 약 883,333원 → 수급 가능</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;">공시가격 8억 원 아파트(다른 소득 없음): (8억 - 1억 3,500만) × 4% ÷ 12 = 월 약 2,216,667원 → 수급 불가에 근접</p>
</div>
<!-- /wp:html -->

<!-- wp:heading {{"level":2}} -->
<h2>탈락 사유 2위: 금융재산 초과</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>예금, 적금, 주식, 보험 등 금융재산이 많은 경우입니다. 금융재산은 2,000만 원을 기본 공제 후 소득환산됩니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">금융재산 총액</th>
  <th style="padding:12px 16px;text-align:right;">공제 후 금액</th>
  <th style="padding:12px 16px;text-align:right;">월 소득환산액</th>
  <th style="padding:12px 16px;text-align:center;">영향도</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">3,000만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">1,000만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">33,333원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#16a34a;">낮음</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">1억 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">8,000만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">266,667원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#d97706;">중간</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;">3억 원</td>
  <td style="padding:12px 16px;text-align:right;">2억 8,000만 원</td>
  <td style="padding:12px 16px;text-align:right;">933,333원</td>
  <td style="padding:12px 16px;text-align:center;color:#dc2626;">높음</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

{cta1}

{imgs[1]}

<!-- wp:heading {{"level":2}} -->
<h2>탈락 사유 3위: 고급 자동차 보유</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>배기량 3,000cc 이상이거나 차량가액이 4,000만 원 이상인 고급 자동차는 재산 산정 시 <strong>전액</strong>이 재산에 포함됩니다. 일반 차량처럼 기본재산액 공제도 적용되지 않아 소득인정액에 미치는 영향이 큽니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="background:#fef2f2;border-left:4px solid #dc2626;padding:20px 24px;margin:24px 0;border-radius:0 8px 8px 0;">
  <p style="margin:0;font-size:15px;font-weight:700;color:#991b1b;">고급 차량 소득환산 예시</p>
  <p style="margin:8px 0 0;font-size:14px;color:#334155;">차량가액 5,000만 원 고급차 보유: 5,000만 원 × 월 소득환산율 적용</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;">고급차는 일반 부동산 환산율(연 4%)이 아닌 월 환산율 적용</p>
  <p style="margin:4px 0 0;font-size:14px;color:#dc2626;font-weight:700;">→ 고급차 1대만으로도 선정기준액 초과 가능</p>
</div>
<!-- /wp:html -->

<!-- wp:heading {{"level":2}} -->
<h2>탈락 사유 4위: 소득 초과</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>근로소득, 사업소득, 임대소득 등 실제 발생 소득이 많은 경우입니다. 근로소득은 월 108만 원까지 공제한 후 30%를 추가 공제하지만, 임대소득은 필요경비만 공제 후 전액 반영됩니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">소득 유형</th>
  <th style="padding:12px 16px;text-align:left;">공제 방법</th>
  <th style="padding:12px 16px;text-align:right;">월 100만 원 소득 시 반영액</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">근로소득</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">108만 원 공제 후 × 70%</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;color:#16a34a;">0원 (108만 원 이하)</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">사업소득</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">필요경비 공제 후 반영</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;color:#d97706;">필요경비에 따라 다름</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;">임대소득</td>
  <td style="padding:12px 16px;">필요경비 공제 후 전액</td>
  <td style="padding:12px 16px;text-align:right;color:#dc2626;">70~100만 원</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

<!-- wp:heading {{"level":2}} -->
<h2>탈락 사유 5위: 공무원·군인·사학연금 수급</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>공무원연금, 군인연금, 사학연금, 별정우체국연금을 받고 있으면 기초연금을 받을 수 없습니다. 단, <strong>배우자</strong>가 이러한 연금을 받는 경우에는 본인이 기초연금을 신청할 수 있으나 소득인정액 계산에 포함됩니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":2}} -->
<h2>이의신청 및 재신청 방법</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>탈락 결정에 이의가 있는 경우 다음과 같이 이의신청이 가능합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
  <li><strong>이의신청 기간:</strong> 탈락 통보를 받은 날로부터 90일 이내</li>
  <li><strong>신청 방법:</strong> 읍면동 주민센터 방문 또는 국민연금공단 지사 방문</li>
  <li><strong>필요 서류:</strong> 이의신청서, 이의신청 사유를 증명하는 서류</li>
  <li><strong>처리 기간:</strong> 접수일로부터 60일 이내 결정 통보</li>
  <li><strong>재신청:</strong> 이의신청과 별도로 소득인정액이 줄어드는 등 상황 변화 시 언제든 재신청 가능</li>
</ul>
<!-- /wp:list -->

{cta2}

<!-- wp:heading {{"level":2}} -->
<h2>자주 묻는 질문 (FAQ)</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="margin:32px 0;">

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 탈락 통보서에 탈락 사유가 나오지 않는 경우 어떻게 하나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">읍면동 주민센터 또는 국민연금공단 지사에 방문하거나 전화(1355)로 문의하면 탈락 사유와 소득인정액 계산 내역을 상세히 안내받을 수 있습니다. 구체적인 수치를 확인해야 이의신청 여부를 판단할 수 있습니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 재산을 처분하면 바로 재신청 가능한가요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">재산을 처분한 경우 처분일 다음 달부터 소득인정액이 변경됩니다. 단, 처분한 금액이 금융재산으로 전환되면 금융재산으로 산정되므로 총 소득인정액에 큰 변화가 없을 수 있습니다. 재산 처분 후 생활비로 사용한 부분은 제외되므로 시간이 지남에 따라 소득인정액이 줄어들 수 있습니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 자녀에게 재산을 증여하면 탈락 사유가 해결되나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">증여일로부터 5년이 지난 재산만 소득인정액 계산에서 제외됩니다. 5년 이내의 증여 재산은 여전히 재산으로 산정되므로 단기간 내 효과를 기대하기 어렵습니다. 또한 증여세 납부 의무도 발생할 수 있으므로 세무사 상담이 권장됩니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 탈락 후 몇 달 지나서 재신청하면 소급 지급되나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">기초연금은 신청일이 속하는 달부터 지급됩니다. 소득인정액이 기준 이하가 된 시점이 아니라 신청한 달을 기준으로 합니다. 따라서 소득인정액이 줄어드는 시점에 바로 신청하는 것이 유리하며, 소급 지급은 되지 않습니다.</p>
</div>

</div>
<!-- /wp:html -->

{cta3}
'''


def post5_content(imgs):
    cta1 = cta_block("복지로 수급자 혜택 조회", "기초연금 수급자가 받을 수 있는 모든 혜택을 확인하세요", "https://www.bokjiro.go.kr", "blue")
    cta2 = cta_block("문화누리카드 신청하기", "연간 13만 원 문화생활 지원을 받아보세요", "https://www.mnuri.kr", "yellow")
    cta3 = cta_block("에너지 바우처 신청", "냉난방비 에너지 바우처를 신청하세요", "https://www.energyv.or.kr", "green")
    return f'''<!-- wp:paragraph -->
<p>기초연금은 단순한 현금 지원이 아닙니다. 기초연금 수급자로 선정되면 의료비부터 교통비, 통신비, 문화생활비까지 다양한 추가 혜택을 받을 수 있습니다. 2026년 기준으로 기초연금 수급자가 받을 수 있는 모든 혜택을 정리했습니다.</p>
<!-- /wp:paragraph -->

{imgs[0]}

<!-- wp:heading {{"level":2}} -->
<h2>의료비 혜택 - 건강보험료 및 약값 감면</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>기초연금 수급자는 건강보험 피부양자 등록 및 건강보험료 경감 혜택을 받을 수 있습니다. 특히 기초생활수급자로 함께 인정되는 경우 의료급여를 통해 사실상 무료 의료서비스를 이용할 수 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">혜택 항목</th>
  <th style="padding:12px 16px;text-align:left;">내용</th>
  <th style="padding:12px 16px;text-align:right;">월 절감 효과</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">건강보험료 경감</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">지역가입자 보험료 최대 30% 경감</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">월 1~5만 원</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">본인부담 상한제</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">연간 의료비 상한액 초과분 환급</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">연 수십만 원</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">약값 경감</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">의료급여 수급자의 경우 약값 무료 또는 500원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">월 1~3만 원</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;">치매 검진</td>
  <td style="padding:12px 16px;">치매안심센터 무료 검진 및 상담</td>
  <td style="padding:12px 16px;text-align:right;">연 10만 원 이상</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

<!-- wp:heading {{"level":2}} -->
<h2>교통비 혜택 - 대중교통 무료 이용</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>만 65세 이상이면 지하철을 무료로 이용할 수 있습니다. 이는 기초연금 수급 여부와 관계없이 나이 기준으로 제공되는 혜택이지만, 기초연금 수급자는 추가적인 교통 지원을 받을 수 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
  <li><strong>지하철 무료:</strong> 전국 지하철 전 노선 무료 (만 65세 이상)</li>
  <li><strong>농어촌 버스:</strong> 일부 지역에서 버스 요금 면제 또는 50% 할인</li>
  <li><strong>KTX·고속버스 할인:</strong> 기초연금 수급자 대상 30% 할인 (일부 지자체)</li>
  <li><strong>택시 바우처:</strong> 교통 취약 지역 기초연금 수급 노인에게 택시비 지원</li>
</ul>
<!-- /wp:list -->

{cta1}

{imgs[1]}

<!-- wp:heading {{"level":2}} -->
<h2>통신비 할인 - 월 최대 26,000원 절감</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>기초연금 수급자는 통신사 제공 통신 요금 감면 혜택을 받을 수 있습니다. 과학기술정보통신부의 통신 요금 감면 제도에 따라 월 최대 26,000원까지 절감됩니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">서비스 구분</th>
  <th style="padding:12px 16px;text-align:right;">감면 금액</th>
  <th style="padding:12px 16px;text-align:left;">적용 대상</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">이동통신 (휴대폰)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">월 최대 11,000원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">기초연금 수급자</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">인터넷</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">월 최대 11,000원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">기초연금 수급자</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;">유선전화</td>
  <td style="padding:12px 16px;text-align:right;">월 최대 4,000원</td>
  <td style="padding:12px 16px;">기초연금 수급자</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>신청 방법: 통신사 대리점 방문 또는 고객센터 전화로 수급자 증명서(기초연금 수급 확인서)를 제출하면 다음 달부터 적용됩니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":2}} -->
<h2>공과금 할인 - 전기·가스·수도</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>한국전력, 도시가스, 상하수도 등 공과금에서도 할인 혜택을 받을 수 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
  <li><strong>전기요금:</strong> 월 최대 16,000원 할인 (한국전력 복지 할인)</li>
  <li><strong>도시가스:</strong> 월 최대 24,000원 할인 (동절기 강화)</li>
  <li><strong>수도요금:</strong> 지자체별로 감면 제공 (서울시 30% 감면 등)</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":2}} -->
<h2>문화누리카드 - 연 13만 원 문화생활 지원</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>기초연금 수급자는 문화누리카드를 신청할 수 있습니다. 연간 13만 원(2026년 기준)이 충전되어 영화관, 공연, 스포츠 관람, 독서, 여행 등 다양한 문화생활에 사용할 수 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":2}} -->
<h2>에너지 바우처 - 냉난방비 지원</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>기초연금 수급자 중 에너지 취약 계층(노인, 장애인, 영유아 포함 가구)은 에너지 바우처를 신청할 수 있습니다. 2026년 기준으로 동절기 최대 654,700원, 하절기 최대 54,000원이 지원됩니다.</p>
<!-- /wp:paragraph -->

{cta2}

<!-- wp:heading {{"level":2}} -->
<h2>자주 묻는 질문 (FAQ)</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="margin:32px 0;">

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 기초연금 수급자가 되면 혜택이 자동으로 적용되나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">일부 혜택은 자동 적용되지만, 통신 요금 감면, 에너지 바우처, 문화누리카드 등은 별도로 신청해야 합니다. 주민센터 또는 해당 기관에 수급자 증명서를 지참하여 신청하세요.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 주거급여를 기초연금과 함께 받을 수 있나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">기초연금 수급자라도 소득인정액이 주거급여 선정기준(중위소득 47% 이하)을 충족하면 주거급여를 함께 받을 수 있습니다. 주거급여는 월세 보조 또는 집 수리비 지원 등으로 제공됩니다. 복지로에서 함께 신청하면 됩니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 통신비 할인 신청 시 어떤 서류가 필요한가요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">기초연금 수급 확인서(주민센터 발급) 또는 복지로 앱에서 출력한 수급 인정 통지서를 통신사 대리점에 제출하면 됩니다. 일부 통신사는 고객센터 전화로도 신청 가능합니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 지자체별 추가 혜택은 어떻게 확인하나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">기초연금 혜택 외에도 거주 지자체에서 별도의 혜택을 제공합니다. 각 시·군·구 복지과 또는 주민센터에 문의하거나, 복지로(bokjiro.go.kr)의 복지서비스 검색에서 지역을 선택하면 해당 지역 혜택을 한눈에 확인할 수 있습니다.</p>
</div>

</div>
<!-- /wp:html -->

{cta3}
'''


def post6_content(imgs):
    cta1 = cta_block("복지로 온라인 신청 바로가기", "집에서 편하게 기초연금을 신청하세요", "https://www.bokjiro.go.kr", "blue")
    cta2 = cta_block("정부24 서류 발급", "필요 서류를 온라인으로 발급받으세요", "https://www.gov.kr", "yellow")
    cta3 = cta_block("국민연금공단 상담 예약", "신청 전 전문 상담을 받아보세요", "https://www.nps.or.kr", "green")
    return f'''<!-- wp:paragraph -->
<p>기초연금 신청은 생각보다 간단합니다. 2026년 기준으로 온라인(복지로)과 오프라인(주민센터, 국민연금공단 지사) 중 선택하여 신청할 수 있습니다. 이 글에서는 필요 서류 목록부터 신청 단계별 방법, 심사 기간까지 모든 과정을 상세히 안내합니다.</p>
<!-- /wp:paragraph -->

{imgs[0]}

<!-- wp:heading {{"level":2}} -->
<h2>기초연금 신청 자격 요건</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>신청 전에 기본 자격 요건을 먼저 확인하세요.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">자격 요건</th>
  <th style="padding:12px 16px;text-align:left;">세부 내용</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">나이</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">만 65세 이상 (생일이 속하는 달의 1개월 전부터 신청 가능)</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">국적·거주</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">대한민국 국적 보유, 국내 거주</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">소득인정액</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">단독 월 2,228,000원 이하 / 부부 월 3,564,800원 이하</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;">수급 제외</td>
  <td style="padding:12px 16px;">공무원·군인·사학·별정우체국 연금 수급자 (배우자 제외)</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

<!-- wp:heading {{"level":2}} -->
<h2>필수 제출 서류 목록</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>신청 시 기본적으로 필요한 서류는 다음과 같습니다. 상황에 따라 추가 서류가 요구될 수 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">서류 구분</th>
  <th style="padding:12px 16px;text-align:left;">세부 서류</th>
  <th style="padding:12px 16px;text-align:left;">발급처</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">신분 확인</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">신청자 신분증 (주민등록증, 운전면허증 등)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">본인 소지</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">금융 정보</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">금융 정보 제공 동의서 (현장 작성 또는 온라인)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">현장 작성</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">통장 사본</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">기초연금 수령할 본인 명의 통장 사본</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">은행</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">임대차 계약서</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">전·월세 거주 시 임대차계약서 사본</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">본인 소지</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;">부채 증빙</td>
  <td style="padding:12px 16px;">금융기관 대출 잔액 증명서 (부채 공제 신청 시)</td>
  <td style="padding:12px 16px;">금융기관</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

{cta1}

{imgs[1]}

<!-- wp:heading {{"level":2}} -->
<h2>온라인 신청 방법 (복지로)</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>복지로(bokjiro.go.kr)에서 공인인증서 또는 간편인증(카카오, 네이버 등)으로 로그인 후 신청할 수 있습니다. 다음은 단계별 절차입니다.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ol>
  <li><strong>복지로 접속:</strong> bokjiro.go.kr → 상단 메뉴 "복지서비스 신청" 클릭</li>
  <li><strong>로그인:</strong> 공인인증서 또는 카카오·네이버 간편인증으로 본인 확인</li>
  <li><strong>기초연금 신청:</strong> 검색창에 "기초연금" 검색 → 신청 화면 진입</li>
  <li><strong>개인 정보 입력:</strong> 주소, 가족관계, 금융정보 제공 동의</li>
  <li><strong>재산·소득 정보 입력:</strong> 부동산, 금융재산, 소득 등 입력</li>
  <li><strong>서류 첨부:</strong> 통장 사본 등 필요 서류 스캔본 첨부</li>
  <li><strong>신청 완료:</strong> 접수번호 확인 후 심사 대기</li>
</ol>
<!-- /wp:list -->

<!-- wp:heading {{"level":2}} -->
<h2>오프라인 신청 방법</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>온라인이 어려운 경우 아래 기관에 직접 방문하여 신청할 수 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
  <li><strong>읍면동 주민센터:</strong> 가장 일반적인 방법으로, 담당자가 신청서 작성을 도와줍니다.</li>
  <li><strong>국민연금공단 지사:</strong> 전국 지사에서 신청 및 상담 가능. 사전 예약 추천.</li>
  <li><strong>방문 신청 서비스:</strong> 거동이 불편한 경우 읍면동 주민센터에 연락하면 담당자가 가정으로 방문합니다.</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":2}} -->
<h2>대리 신청 방법</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>본인이 직접 신청하기 어려운 경우 가족이나 대리인이 신청할 수 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
  <li>대리인 신분증, 신청인 신분증, 위임장 필요</li>
  <li>법정대리인(성년후견인)은 법원 결정문 또는 가족관계증명서 지참</li>
  <li>사회복지사 등 전문 대리인 활용 가능</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":2}} -->
<h2>심사 기간 및 결과 통보</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>신청 후 처리 과정은 다음과 같습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
  <li><strong>심사 기간:</strong> 신청일로부터 30일 이내 (복잡한 경우 최대 60일)</li>
  <li><strong>결과 통보:</strong> 우편 또는 문자메시지로 통보</li>
  <li><strong>지급 시작:</strong> 수급 결정 시 신청월부터 소급 지급</li>
  <li><strong>지급일:</strong> 매월 25일 (25일이 공휴일이면 전날 지급)</li>
</ul>
<!-- /wp:list -->

{cta2}

<!-- wp:heading {{"level":2}} -->
<h2>자주 묻는 질문 (FAQ)</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="margin:32px 0;">

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 65세 생일 전에 미리 신청할 수 있나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">네, 65세 생일이 속하는 달의 1개월 전부터 신청할 수 있습니다. 예를 들어 생일이 8월 15일이라면 7월 1일부터 신청 가능합니다. 다만 실제 기초연금 지급은 65세가 되는 달(8월)부터 시작됩니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 금융 정보 제공 동의를 하면 어떤 정보가 조회되나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">예금, 적금, 주식, 보험, 채권, 대출 등 금융기관에 보유한 모든 금융 정보가 조회됩니다. 국세청과 연계하여 소득 정보도 확인됩니다. 조회한 정보는 소득인정액 산정에만 사용되며 외부에 유출되지 않습니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 신청 후 소득이나 재산에 변화가 생기면 신고해야 하나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">네, 수급 중 소득이나 재산에 중요한 변화가 생기면 읍면동 주민센터에 변경 신고를 해야 합니다. 미신고 시 이미 받은 연금을 환수당할 수 있습니다. 기초연금은 매년 정기적으로 소득·재산 조사를 실시하여 수급 자격을 재확인합니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 해외 장기 체류 시 기초연금이 정지되나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">국외에 60일 이상 체류하면 기초연금 지급이 일시 정지됩니다. 귀국 후 읍면동 주민센터에 신고하면 재개됩니다. 연속 60일이 기준이며, 단순 여행이라도 60일을 초과하면 정지됩니다.</p>
</div>

</div>
<!-- /wp:html -->

{cta3}
'''


def post7_content(imgs):
    cta1 = cta_block("복지로 수급 여부 확인", "자녀 소득 관계없이 내 수급 자격을 직접 확인하세요", "https://www.bokjiro.go.kr", "blue")
    cta2 = cta_block("국민연금공단 상담 신청", "부양의무자 폐지 이후 변화에 대해 상담받으세요", "https://www.nps.or.kr", "yellow")
    cta3 = cta_block("세대분리 방법 안내", "주민센터에서 세대분리를 진행하세요", "https://www.gov.kr", "green")
    return f'''<!-- wp:paragraph -->
<p>많은 어르신들이 "자녀 소득이 많으면 기초연금을 못 받는다"고 알고 계십니다. 이는 과거 부양의무자 기준이 있던 시절의 이야기입니다. 현재 기초연금은 <strong>부양의무자 기준이 완전히 폐지</strong>되어 자녀의 소득이나 재산이 기초연금 수급 여부에 영향을 주지 않습니다. 단, 몇 가지 주의사항이 있으니 자세히 살펴보겠습니다.</p>
<!-- /wp:paragraph -->

{imgs[0]}

<!-- wp:heading {{"level":2}} -->
<h2>부양의무자 기준 폐지 경위</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>과거 기초생활보장제도에는 부양의무자 기준이 있어 자녀의 소득이 높으면 부모가 급여를 받지 못하는 경우가 많았습니다. 기초연금은 2014년 도입 당시부터 부양의무자 기준을 적용하지 않았으며, 이는 기초연금의 핵심 원칙입니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="background:#f0fdf4;border-left:4px solid #16a34a;padding:20px 24px;margin:24px 0;border-radius:0 8px 8px 0;">
  <p style="margin:0;font-size:15px;font-weight:700;color:#166534;">기초연금 부양의무자 기준: 처음부터 없었습니다</p>
  <p style="margin:8px 0 0;font-size:14px;color:#334155;">기초연금법 제3조: 수급권은 본인 및 배우자의 소득인정액을 기준으로 하며, 자녀 등 부양의무자 기준은 적용하지 않습니다.</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;font-weight:700;">→ 자녀가 재벌이어도, 자녀 소득이 0원이어도 기초연금 수급에는 영향 없음</p>
</div>
<!-- /wp:html -->

<!-- wp:heading {{"level":2}} -->
<h2>자녀 소득이 영향을 미치지 않는 범위</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>다음 항목들은 기초연금 수급 여부 판단 시 고려되지 않습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
  <li>자녀의 근로소득, 사업소득, 임대소득</li>
  <li>자녀 명의의 부동산, 예금, 주식 등 재산</li>
  <li>자녀가 국민연금, 공무원연금 등을 받는 경우</li>
  <li>자녀의 배우자(며느리, 사위) 소득 및 재산</li>
  <li>손자녀의 소득 및 재산</li>
</ul>
<!-- /wp:list -->

{cta1}

{imgs[1]}

<!-- wp:heading {{"level":2}} -->
<h2>자녀와 동거 시 주의사항</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>부양의무자 기준은 없지만, 자녀와 함께 살면서 발생하는 일부 상황은 소득인정액에 영향을 줄 수 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">항목</th>
  <th style="padding:12px 16px;text-align:center;">기초연금 영향</th>
  <th style="padding:12px 16px;text-align:left;">설명</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">자녀 명의 집에 무상 거주</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#d97706;">영향 있음</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">무상 임차는 사적이전소득으로 일부 반영될 수 있음</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">자녀에게 정기적 용돈 수령</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#d97706;">일부 영향</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">월 40만 원 초과 정기 용돈은 사적이전소득으로 반영</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">자녀가 내 통장에 돈 넣어줌</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#d97706;">주의 필요</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">금융재산으로 잡혀 소득환산될 수 있음</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;">자녀 소득·직업·재산</td>
  <td style="padding:12px 16px;text-align:center;color:#16a34a;">영향 없음</td>
  <td style="padding:12px 16px;">부양의무자 기준 없음</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

<!-- wp:heading {{"level":2}} -->
<h2>사적이전소득 반영 기준</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>자녀 등 가족으로부터 정기적으로 받는 용돈은 사적이전소득으로 소득인정액에 반영됩니다. 단, 기준이 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="background:#f8fafc;border-left:4px solid #2d5a8e;padding:20px 24px;margin:24px 0;border-radius:0 8px 8px 0;">
  <p style="margin:0;font-size:15px;font-weight:700;color:#1e3a5f;">사적이전소득 반영 기준</p>
  <p style="margin:8px 0 0;font-size:14px;color:#334155;">기본공제: 월 40만 원까지는 사적이전소득으로 보지 않음</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;">예: 자녀에게 매달 30만 원 용돈 받음 → 소득으로 반영되지 않음</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;">예: 자녀에게 매달 60만 원 용돈 받음 → (60만 - 40만) = 20만 원이 사적이전소득으로 반영</p>
</div>
<!-- /wp:html -->

<!-- wp:heading {{"level":2}} -->
<h2>세대분리 방법과 주의사항</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>자녀와 같은 주소에 주민등록이 되어 있더라도 기초연금 수급에는 영향이 없습니다. 그러나 일부 복지 서비스(기초생활보장급여 등)에서는 세대 구성이 중요할 수 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
  <li><strong>세대분리 방법:</strong> 읍면동 주민센터에 방문하여 세대분리 신청서 제출</li>
  <li><strong>필요 서류:</strong> 신분증, 이유서(경우에 따라)</li>
  <li><strong>기초연금 영향:</strong> 세대분리 여부와 무관하게 부부 외 가족의 소득·재산은 반영되지 않음</li>
  <li><strong>주의:</strong> 세대분리가 기초연금 수급을 자동으로 보장하지는 않음</li>
</ul>
<!-- /wp:list -->

{cta2}

<!-- wp:heading {{"level":2}} -->
<h2>자주 묻는 질문 (FAQ)</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="margin:32px 0;">

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 자녀가 자동차를 사줬는데 재산으로 잡히나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">자녀가 사줬더라도 본인 또는 배우자 명의로 등록된 차량은 재산으로 산정됩니다. 자녀 명의 차량은 재산에 포함되지 않습니다. 따라서 차량 명의를 자녀 명의로 유지하는 것이 소득인정액 관리에 유리합니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 자녀가 집을 사줬는데 재산으로 잡히나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">본인 또는 배우자 명의로 등기된 부동산은 재산으로 산정됩니다. 자녀가 비용을 부담했더라도 명의가 본인이면 본인 재산입니다. 자녀 명의 집에 무상으로 거주하는 경우에는 사적이전소득으로 일부 반영될 수 있습니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 자녀가 해외에 있으면 어떻게 되나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">자녀가 해외에 거주하는 경우에도 부양의무자 기준이 없으므로 기초연금 수급에 영향을 주지 않습니다. 다만 자녀가 해외에서 송금하는 금액이 사적이전소득으로 반영될 수 있습니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 형제자매가 기초연금을 받으면 나도 받을 수 있나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">기초연금은 가구 단위(본인 + 배우자)로 심사하며, 형제자매와는 무관합니다. 형제자매가 기초연금을 받더라도 또는 받지 않더라도 본인의 수급 자격에는 영향을 주지 않습니다. 각자의 소득인정액을 기준으로 개별 심사합니다.</p>
</div>

</div>
<!-- /wp:html -->

{cta3}
'''


def post8_content(imgs):
    cta1 = cta_block("국민연금 예상 수령액 조회", "내 노령연금 수령액을 미리 확인하세요", "https://www.nps.or.kr", "blue")
    cta2 = cta_block("복지로 기초연금 신청", "노령연금과 함께 기초연금도 신청하세요", "https://www.bokjiro.go.kr", "yellow")
    cta3 = cta_block("연금 통합 상담 예약", "두 연금을 함께 받는 최적 전략을 상담하세요", "https://www.nps.or.kr", "green")
    return f'''<!-- wp:paragraph -->
<p>기초연금과 노령연금(국민연금)은 이름이 비슷하지만 전혀 다른 제도입니다. 두 연금을 모두 받을 수 있는지, 받으면 얼마나 감액되는지 정확히 알아야 노후 소득을 최대화할 수 있습니다. 2026년 기준으로 두 연금의 차이점과 동시 수령 전략을 정리합니다.</p>
<!-- /wp:paragraph -->

{imgs[0]}

<!-- wp:heading {{"level":2}} -->
<h2>기초연금 vs 노령연금 핵심 비교</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">구분</th>
  <th style="padding:12px 16px;text-align:center;">기초연금</th>
  <th style="padding:12px 16px;text-align:center;">노령연금 (국민연금)</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;font-weight:700;">재원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">국가 재정 (세금)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">보험료 (본인 납부)</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;font-weight:700;">수급 조건</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">만 65세 이상 + 소득인정액 기준</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">10년 이상 납부 + 수급 연령 도달</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;font-weight:700;">2026년 최대 금액</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">월 342,510원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">가입 기간·금액에 따라 다름</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;font-weight:700;">소득 심사</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">있음 (소득인정액 기준)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">없음 (납부 기록만 확인)</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;font-weight:700;">신청 기관</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">주민센터 / 복지로</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">국민연금공단 지사</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;font-weight:700;">동시 수령</td>
  <td style="padding:12px 16px;text-align:center;color:#16a34a;" colspan="2">가능 (단, 연계감액 발생할 수 있음)</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

<!-- wp:heading {{"level":2}} -->
<h2>둘 다 받을 수 있는 조건</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>기초연금과 노령연금을 동시에 받으려면 각각의 수급 조건을 모두 충족해야 합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
  <li>만 65세 이상</li>
  <li>대한민국 국적 및 국내 거주</li>
  <li>국민연금 10년 이상 납부 (노령연금 조건)</li>
  <li>소득인정액이 기초연금 선정기준액 이하</li>
  <li>공무원·군인·사학·별정우체국 연금 비수급자</li>
</ul>
<!-- /wp:list -->

{cta1}

{imgs[1]}

<!-- wp:heading {{"level":2}} -->
<h2>연계감액 발생 조건과 계산</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>두 연금을 동시에 받는 경우, 국민연금 수령액이 일정 기준을 초과하면 기초연금이 감액됩니다. 이를 연계감액이라 합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="background:#fef3c7;border-left:4px solid #f59e0b;padding:20px 24px;margin:24px 0;border-radius:0 8px 8px 0;">
  <p style="margin:0;font-size:15px;font-weight:700;color:#92400e;">연계감액 적용 기준 (2026년)</p>
  <p style="margin:8px 0 0;font-size:14px;color:#334155;">국민연금 노령연금 월 수령액 515,000원 초과 시 감액 시작</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;">감액 하한: 기초연금의 50% (약 171,255원)는 반드시 보장</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;">→ 국민연금이 아무리 많아도 기초연금이 완전히 0원이 되지는 않음</p>
</div>
<!-- /wp:html -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">국민연금 수령액</th>
  <th style="padding:12px 16px;text-align:right;">기초연금</th>
  <th style="padding:12px 16px;text-align:right;">두 연금 합계</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">월 30만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;color:#16a34a;">342,510원 (감액없음)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;font-weight:700;">642,510원</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">월 50만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;color:#16a34a;">342,510원 (감액없음)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;font-weight:700;">842,510원</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">월 70만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;color:#d97706;">약 217,000원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;font-weight:700;">약 917,000원</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">월 100만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;color:#d97706;">171,255원 (최소보장)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;font-weight:700;">약 1,171,255원</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;">월 200만 원</td>
  <td style="padding:12px 16px;text-align:right;color:#d97706;">171,255원 (최소보장)</td>
  <td style="padding:12px 16px;text-align:right;font-weight:700;">약 2,171,255원</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

<!-- wp:heading {{"level":2}} -->
<h2>최적 수령 전략</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>두 연금의 합계를 최대화하려면 다음 전략을 고려하세요.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
  <li><strong>국민연금 연기 수령:</strong> 국민연금 수령을 늦추면 월 수령액이 최대 36% 증가하지만, 연계감액도 커질 수 있습니다. 국민연금 수령액이 515,000원 초과 여부를 기준으로 판단하세요.</li>
  <li><strong>기초연금 먼저 신청:</strong> 65세가 되면 기초연금은 바로 신청하고, 국민연금은 상황에 따라 연기를 검토하세요.</li>
  <li><strong>부부 합산 계획:</strong> 배우자와 함께 두 연금을 고려한 수령 계획을 세우면 가구 전체 수령액을 최적화할 수 있습니다.</li>
</ul>
<!-- /wp:list -->

{cta2}

<!-- wp:heading {{"level":2}} -->
<h2>자주 묻는 질문 (FAQ)</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="margin:32px 0;">

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 국민연금을 한 번도 안 냈는데 기초연금 받을 수 있나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">네, 국민연금 가입 여부와 관계없이 만 65세 이상이고 소득인정액이 기준 이하면 기초연금을 받을 수 있습니다. 오히려 국민연금 미가입자는 연계감액이 없어 기초연금 전액(월 342,510원)을 받을 수 있습니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 노령연금 수급 나이가 되지 않아도 기초연금을 받을 수 있나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">네, 기초연금은 만 65세 이상이면 신청 가능합니다. 노령연금(국민연금) 수급 개시 연령(1969년생 이후 출생자는 만 65세)과 동일하지만, 국민연금을 받지 않아도 기초연금은 받을 수 있습니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 국민연금 조기수령을 선택하면 기초연금에 어떤 영향이 있나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">국민연금 조기수령(만 60~64세)을 선택하면 수령액이 감소합니다. 만약 조기수령액이 월 515,000원 이하라면 기초연금 연계감액이 없어 유리할 수 있습니다. 단, 65세 이전에는 기초연금을 받을 수 없으므로 조기수령 기간(60~64세)에는 국민연금만 수령합니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 기초연금과 노령연금 신청을 동시에 할 수 있나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">신청 창구는 다릅니다. 기초연금은 주민센터 또는 복지로에서, 노령연금은 국민연금공단 지사 또는 국민연금공단 홈페이지에서 신청합니다. 단, 국민연금공단 지사 방문 시 기초연금도 함께 신청할 수 있도록 안내해 드리는 경우가 많습니다.</p>
</div>

</div>
<!-- /wp:html -->

{cta3}
'''


def post9_content(imgs):
    cta1 = cta_block("복지로 금융재산 모의계산", "예금 금액에 따른 소득인정액을 미리 계산하세요", "https://www.bokjiro.go.kr", "blue")
    cta2 = cta_block("국민연금공단 재산 상담", "금융재산 정리 전략을 전문가에게 상담하세요", "https://www.nps.or.kr", "yellow")
    cta3 = cta_block("기초연금 신청 바로가기", "금융재산 정리 후 바로 신청하세요", "https://www.bokjiro.go.kr", "green")
    return f'''<!-- wp:paragraph -->
<p>기초연금을 받으려면 예금(금융재산)을 얼마까지 보유할 수 있는지 궁금하신 분들이 많습니다. 결론부터 말씀드리면, 금융재산에는 2,000만 원 기본공제가 있어 2,000만 원 이하의 예금은 소득인정액에 영향을 주지 않습니다. 2026년 기준으로 금융재산과 기초연금의 관계를 상세히 설명합니다.</p>
<!-- /wp:paragraph -->

{imgs[0]}

<!-- wp:heading {{"level":2}} -->
<h2>금융재산의 범위와 기본공제</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>기초연금 심사에서 금융재산으로 보는 항목은 다음과 같습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">금융재산 종류</th>
  <th style="padding:12px 16px;text-align:center;">포함 여부</th>
  <th style="padding:12px 16px;text-align:left;">비고</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">예금·적금·저축</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#dc2626;">포함</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">잔액 기준</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">주식·펀드·ETF</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#dc2626;">포함</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">평가액 기준</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">채권·어음</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#dc2626;">포함</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">액면가 기준</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">보험 (해지환급금)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#dc2626;">포함</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">해지환급금 기준</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;">금·은 등 귀금속</td>
  <td style="padding:12px 16px;text-align:center;color:#16a34a;">미포함 (일반재산)</td>
  <td style="padding:12px 16px;">별도 재산으로 산정</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

<!-- wp:html -->
<div style="background:#f0fdf4;border-left:4px solid #16a34a;padding:20px 24px;margin:24px 0;border-radius:0 8px 8px 0;">
  <p style="margin:0;font-size:15px;font-weight:700;color:#166534;">2026년 금융재산 기본공제</p>
  <p style="margin:8px 0 0;font-size:14px;color:#334155;">2,000만 원 기본공제 적용</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;">→ 금융재산 합계가 2,000만 원 이하면 소득환산액 = 0원</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;">→ 2,000만 원 초과분만 소득환산율(연 6.26%) 적용</p>
</div>
<!-- /wp:html -->

{cta1}

{imgs[1]}

<!-- wp:heading {{"level":2}} -->
<h2>금융재산 소득환산 계산법</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>금융재산의 소득환산율은 일반 재산(연 4%)보다 높은 <strong>연 6.26%</strong>입니다. 2,000만 원 공제 후 금액에 이 비율을 적용합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="background:#f8fafc;border-left:4px solid #2d5a8e;padding:20px 24px;margin:24px 0;border-radius:0 8px 8px 0;">
  <p style="margin:0;font-size:15px;font-weight:700;color:#1e3a5f;">금융재산 월 소득환산액 계산 공식</p>
  <p style="margin:8px 0 0;font-size:14px;color:#334155;">월 소득환산액 = (금융재산 총액 - 2,000만 원) × 6.26% ÷ 12</p>
  <p style="margin:4px 0 0;font-size:14px;color:#334155;">단, 금융재산 총액이 2,000만 원 이하면 0원</p>
</div>
<!-- /wp:html -->

<!-- wp:heading {{"level":2}} -->
<h2>예금 금액별 소득인정액 영향 시뮬레이션</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">예금 총액</th>
  <th style="padding:12px 16px;text-align:right;">공제 후 금액</th>
  <th style="padding:12px 16px;text-align:right;">월 소득환산액</th>
  <th style="padding:12px 16px;text-align:center;">기초연금 영향</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">1,500만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">0원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;font-weight:700;color:#16a34a;">0원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#16a34a;">없음</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">3,000만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">1,000만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;font-weight:700;color:#16a34a;">약 52,167원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#16a34a;">소폭</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">5,000만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">3,000만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;font-weight:700;color:#d97706;">약 156,500원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#d97706;">중간</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">1억 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">8,000만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;font-weight:700;color:#dc2626;">약 417,333원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#dc2626;">큼</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;">2억 원</td>
  <td style="padding:12px 16px;text-align:right;">1억 8,000만 원</td>
  <td style="padding:12px 16px;text-align:right;font-weight:700;color:#dc2626;">약 939,000원</td>
  <td style="padding:12px 16px;text-align:center;color:#dc2626;">매우 큼</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

<!-- wp:heading {{"level":2}} -->
<h2>금융재산 줄이는 합법적 방법</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>금융재산이 많아 기초연금 수급에 어려움이 있는 경우 다음과 같은 합법적 방법을 고려할 수 있습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
  <li><strong>생활비 사용:</strong> 여유 자금을 생활비로 사용하면 자연스럽게 금융재산이 감소합니다.</li>
  <li><strong>부채 상환:</strong> 대출금 등 부채를 예금으로 상환하면 금융재산과 부채가 동시에 감소하여 순자산 기준이 낮아집니다.</li>
  <li><strong>보험 정리:</strong> 해지환급금이 높은 보험을 정리하는 것을 고려하세요. 단, 의료비 보장 등을 고려하여 신중히 결정해야 합니다.</li>
  <li><strong>의료비 지출:</strong> 의료비, 약값 등 필요한 지출을 예금에서 하면 금융재산이 줄어듭니다.</li>
</ul>
<!-- /wp:list -->

{cta2}

<!-- wp:heading {{"level":2}} -->
<h2>자주 묻는 질문 (FAQ)</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="margin:32px 0;">

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 적금과 예금은 따로 2,000만 원씩 공제되나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">아닙니다. 예금, 적금, 주식, 보험 등 모든 금융재산을 합산한 총액에서 2,000만 원이 공제됩니다. 즉, 예금 1,500만 원 + 적금 1,000만 원이면 합계 2,500만 원에서 2,000만 원을 공제한 500만 원에 대해서만 소득환산이 적용됩니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 주식 평가액이 등락할 경우 어떻게 산정하나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">조사 기준일 현재의 평가액을 기준으로 합니다. 조사 후 주가가 하락하더라도 다음 정기 조사까지는 이전 평가액이 적용됩니다. 주식 평가액이 크게 하락한 경우에는 중간에 변경 신청을 할 수 있습니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 배우자 명의 예금도 합산되나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">네, 배우자 명의의 금융재산도 합산됩니다. 부부 가구로 심사하므로 본인과 배우자의 모든 금융재산을 합산한 후 2,000만 원을 공제합니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 예금이자 수익은 소득으로 잡히나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">예금이자는 별도의 이자소득으로 소득평가액에 반영됩니다. 단, 금융재산의 소득환산과 이자소득을 이중으로 적용하지 않고, 일반적으로 금융재산 환산 방식으로 통합 적용합니다. 연간 이자소득이 2,000만 원을 초과하는 경우에는 별도로 반영될 수 있습니다.</p>
</div>

</div>
<!-- /wp:html -->

{cta3}
'''


def post10_content(imgs):
    cta1 = cta_block("보험개발원 차량가액 조회", "내 차량의 정확한 가액을 무료로 확인하세요", "https://www.kidi.or.kr", "blue")
    cta2 = cta_block("복지로 소득인정액 모의계산", "차량 보유 시 소득인정액을 미리 계산하세요", "https://www.bokjiro.go.kr", "yellow")
    cta3 = cta_block("국민연금공단 차량 상담", "차량 처분 전 전문가 상담을 먼저 받으세요", "https://www.nps.or.kr", "green")
    return f'''<!-- wp:paragraph -->
<p>자동차를 보유하면 기초연금을 받을 수 없다고 알고 계신 분들이 많습니다. 사실 일반 차량은 일정 기준에 따라 재산으로 산정되지만, 무조건 탈락하는 것은 아닙니다. 반면 배기량 3,000cc 이상이거나 차량가액 4,000만 원 이상의 고급 차량은 전액이 재산에 포함되어 불리합니다. 2026년 기준으로 차량 기준을 상세히 정리합니다.</p>
<!-- /wp:paragraph -->

{imgs[0]}

<!-- wp:heading {{"level":2}} -->
<h2>일반 차량 vs 고급 차량 재산 반영 방식</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">구분</th>
  <th style="padding:12px 16px;text-align:center;">일반 차량</th>
  <th style="padding:12px 16px;text-align:center;">고급 차량</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;font-weight:700;">기준</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">배기량 3,000cc 미만 AND 가액 4,000만 원 미만</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">배기량 3,000cc 이상 OR 가액 4,000만 원 이상</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;font-weight:700">재산 반영</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">일반 재산으로 합산 (기본재산액 공제 대상)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">전액 반영 (기본재산액 공제 없음)</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;font-weight:700;">소득환산율</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">연 4%</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;">월 4.17% (연 50%)</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;font-weight:700;">예시</td>
  <td style="padding:12px 16px;text-align:center;">2,000cc 2,000만 원 차량 → 월 약 20,000원 반영</td>
  <td style="padding:12px 16px;text-align:center;">3,500cc 5,000만 원 차량 → 월 약 2,085,000원 반영</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

<!-- wp:paragraph -->
<p>고급 차량의 소득환산율이 일반 재산보다 월등히 높은 이유는 사치성 재산에 대한 불이익을 강화하기 위해서입니다. 고급차 한 대만으로도 선정기준액을 초과할 수 있습니다.</p>
<!-- /wp:paragraph -->

{cta1}

{imgs[1]}

<!-- wp:heading {{"level":2}} -->
<h2>차량가액 조회 방법</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>차량가액은 보험개발원에서 제공하는 기준가액표를 사용합니다. 직접 조회하는 방법은 다음과 같습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ol>
  <li>보험개발원 홈페이지(kidi.or.kr) 접속</li>
  <li>상단 메뉴 "자동차보험 참고서비스" 클릭</li>
  <li>"차량가액조회" 선택</li>
  <li>차량번호 또는 차종·연식·배기량 입력</li>
  <li>기준가액 확인</li>
</ol>
<!-- /wp:list -->

<!-- wp:heading {{"level":2}} -->
<h2>차량 연식별 감가 계산</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>차량은 시간이 지남에 따라 가치가 하락합니다. 보험개발원 차량가액은 매년 감가상각을 반영하여 갱신됩니다. 일반적인 감가 패턴은 다음과 같습니다.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">차량 연식</th>
  <th style="padding:12px 16px;text-align:right;">신차 대비 잔존 가치 (예시)</th>
  <th style="padding:12px 16px;text-align:left;">비고</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">신차 (1년 이하)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">80~90%</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">출고 직후 급격히 감가</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">3년 차</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">60~70%</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;"></td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">5년 차</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">45~55%</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;"></td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">10년 차</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">20~30%</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;"></td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;">15년 이상</td>
  <td style="padding:12px 16px;text-align:right;">10% 이하</td>
  <td style="padding:12px 16px;">폐차 가치 수준</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

<!-- wp:heading {{"level":2}} -->
<h2>차량 처분 및 명의변경 시 주의사항</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>기초연금 수급을 위해 차량을 처분하거나 명의를 변경하는 경우 다음 사항을 주의해야 합니다.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
  <li><strong>차량 처분:</strong> 매도 금액이 금융재산으로 전환됩니다. 처분 금액이 2,000만 원 이하라면 금융재산 기본공제 범위 내에 있어 유리합니다.</li>
  <li><strong>명의변경:</strong> 자녀 등에게 명의를 이전해도 5년 이내에는 증여 재산으로 볼 수 있습니다. 단, 차량은 5년 기준이 다소 다르게 적용될 수 있으므로 주민센터에 확인이 필요합니다.</li>
  <li><strong>담보 차량:</strong> 차량에 대출 담보가 설정된 경우, 대출 잔액을 부채로 차감할 수 있습니다.</li>
  <li><strong>장애인 차량:</strong> 장애인 보조용 차량은 재산 산정에서 제외됩니다. 장애인 등록 차량임을 증명해야 합니다.</li>
  <li><strong>10년 초과 차량:</strong> 차량가액이 매우 낮아져 소득인정액에 미치는 영향이 미미해집니다.</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":2}} -->
<h2>차량 보유별 소득인정액 영향 시뮬레이션</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="overflow-x:auto;margin:24px 0;">
<table style="width:100%;border-collapse:collapse;font-size:15px;">
<thead>
<tr style="background:#1e3a5f;color:#fff;">
  <th style="padding:12px 16px;text-align:left;">차량 유형</th>
  <th style="padding:12px 16px;text-align:right;">차량가액</th>
  <th style="padding:12px 16px;text-align:right;">월 소득환산액</th>
  <th style="padding:12px 16px;text-align:center;">기초연금 영향</th>
</tr>
</thead>
<tbody>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">국산 소형 (2,000cc, 10년)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">약 500만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;color:#16a34a;">약 16,667원 (일반 재산)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#16a34a;">소폭</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">국산 중형 (2,000cc, 5년)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">약 1,500만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;color:#16a34a;">약 50,000원 (일반 재산)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#16a34a;">소폭</td>
</tr>
<tr style="background:#fff;">
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;">수입 SUV (3,500cc, 5년)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;">약 4,000만 원</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:right;color:#dc2626;">약 1,668,000원 (고급차)</td>
  <td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;text-align:center;color:#dc2626;">매우 큼</td>
</tr>
<tr style="background:#f8fafc;">
  <td style="padding:12px 16px;">국산 고급세단 (3,300cc, 3년)</td>
  <td style="padding:12px 16px;text-align:right;">약 5,000만 원</td>
  <td style="padding:12px 16px;text-align:right;color:#dc2626;">약 2,085,000원 (고급차)</td>
  <td style="padding:12px 16px;text-align:center;color:#dc2626;">탈락 가능성</td>
</tr>
</tbody>
</table>
</div>
<!-- /wp:html -->

{cta2}

<!-- wp:heading {{"level":2}} -->
<h2>자주 묻는 질문 (FAQ)</h2>
<!-- /wp:heading -->

<!-- wp:html -->
<div style="margin:32px 0;">

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 하이브리드 차량은 배기량을 어떻게 계산하나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">하이브리드 차량의 배기량은 내연기관 부분의 배기량을 기준으로 합니다. 예를 들어 2,500cc 하이브리드는 배기량 기준으로 고급차에 해당하지 않습니다. 전기차는 배기량이 없으므로 차량가액(4,000만 원) 기준만 적용됩니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 차량이 두 대인 경우 어떻게 계산되나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">본인과 배우자 명의의 차량이 각 1대씩이면 각각 산정합니다. 두 차량 모두 일반 차량이면 가액을 합산하여 일반 재산으로 처리합니다. 한 대라도 고급 차량이면 해당 차량은 고급차 기준으로 별도 산정됩니다.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;margin-bottom:16px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 생업용 차량도 재산으로 잡히나요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">생업용 차량(화물차, 택시 등)도 원칙적으로 재산으로 산정됩니다. 단, 사업소득 신고 시 감가상각 처리된 차량은 가액이 낮아져 있을 수 있습니다. 생업용 차량임을 증명하는 경우 소득환산 방식이 달라질 수 있으니 담당자에게 문의하세요.</p>
</div>

<div style="border:1px solid #e2e8f0;border-radius:10px;padding:20px 24px;">
  <p style="margin:0 0 8px;font-size:16px;font-weight:700;color:#1e3a5f;">Q. 차량을 처분하면 즉시 재신청 가능한가요?</p>
  <p style="margin:0;font-size:14px;color:#475569;">차량을 처분(말소 또는 양도)하면 다음 달부터 재산에서 제외됩니다. 처분 직후 바로 기초연금을 재신청하거나 변경 신청을 하면 다음 지급 월부터 반영됩니다. 단, 매도 대금이 금융재산으로 남아있으면 금융재산으로 산정되므로 실제로 사용하거나 부채 상환에 활용하는 것이 유리합니다.</p>
</div>

</div>
<!-- /wp:html -->

{cta3}
'''


POSTS = [
    {
        "title": "기초연금 재산 기준 얼마까지 받을 수 있나 아파트 보유자 계산법 2026",
        "cat": 13,
        "slug": "basic-pension-property-standard-2026",
        "images": [
            ("photo-1560448204-e02f11c3d0e2", "기초연금 아파트 재산 기준"),
            ("photo-1551288049-bebda4e38f71", "소득인정액 계산 데이터"),
        ],
        "content": post1_content,
    },
    {
        "title": "기초연금 부부 수령액 감액 기준 부부 모두 받는 방법 2026",
        "cat": 13,
        "slug": "basic-pension-couple-reduction-2026",
        "images": [
            ("photo-1554224155-6726b3ff858f", "기초연금 부부 감액 기준"),
            ("photo-1521791136064-7986c2920216", "부부 연금 상담"),
        ],
        "content": post2_content,
    },
    {
        "title": "국민연금 받으면 기초연금 깎이나 연계감액 계산법 총정리 2026",
        "cat": 13,
        "slug": "national-pension-basic-pension-overlap-2026",
        "images": [
            ("photo-1460925895917-afdab827c52f", "국민연금 기초연금 연계"),
            ("photo-1551288049-bebda4e38f71", "연금 데이터 분석"),
        ],
        "content": post3_content,
    },
    {
        "title": "기초연금 탈락 사유 TOP 5 소득인정액 초과 기준 총정리 2026",
        "cat": 13,
        "slug": "basic-pension-disqualification-reasons-2026",
        "images": [
            ("photo-1556742049-0cfed4f6a45d", "기초연금 서류 검토"),
            ("photo-1450101499163-c8848c66ca85", "소득 재산 서류"),
        ],
        "content": post4_content,
    },
    {
        "title": "기초연금 수급자 혜택 총정리 의료비 교통비 통신비 할인 2026",
        "cat": 13,
        "slug": "basic-pension-recipient-benefits-2026",
        "images": [
            ("photo-1486312338219-ce68d2c6f44d", "기초연금 수급자 혜택"),
            ("photo-1434030216411-0b793f4b4173", "복지 혜택 학습"),
        ],
        "content": post5_content,
    },
    {
        "title": "기초연금 신청 서류 준비물 온라인 신청 방법 완벽 가이드 2026",
        "cat": 13,
        "slug": "basic-pension-application-documents-2026",
        "images": [
            ("photo-1554224155-6726b3ff858f", "기초연금 신청 서류"),
            ("photo-1504639725590-34d0984388bd", "온라인 신청"),
        ],
        "content": post6_content,
    },
    {
        "title": "기초연금 자녀 소득 영향 있나 부양의무자 기준 폐지 후 변화 2026",
        "cat": 13,
        "slug": "basic-pension-children-income-effect-2026",
        "images": [
            ("photo-1507003211169-0a1dd7228f2d", "가족 부양 관계"),
            ("photo-1521791136064-7986c2920216", "기초연금 상담"),
        ],
        "content": post7_content,
    },
    {
        "title": "기초연금 vs 노령연금 차이점 둘 다 받을 수 있는 조건 정리 2026",
        "cat": 13,
        "slug": "basic-pension-vs-old-age-pension-2026",
        "images": [
            ("photo-1460925895917-afdab827c52f", "기초연금 노령연금 비교"),
            ("photo-1551288049-bebda4e38f71", "연금 비교 분석"),
        ],
        "content": post8_content,
    },
    {
        "title": "기초연금 예금 얼마까지 가능한가 금융재산 공제 기준 2026",
        "cat": 13,
        "slug": "basic-pension-savings-limit-2026",
        "images": [
            ("photo-1556742049-0cfed4f6a45d", "기초연금 예금 한도"),
            ("photo-1554224155-6726b3ff858f", "금융재산 서류"),
        ],
        "content": post9_content,
    },
    {
        "title": "기초연금 자동차 기준 차량가액 계산법 3000cc 이상 주의사항 2026",
        "cat": 13,
        "slug": "basic-pension-car-standard-2026",
        "images": [
            ("photo-1449965408869-eaa3f722e40d", "기초연금 자동차 기준"),
            ("photo-1560518883-ce09059eeffa", "차량 가액 계산"),
        ],
        "content": post10_content,
    },
]


def main():
    published = []
    for idx, post in enumerate(POSTS, 1):
        print(f"\n{'='*60}")
        print(f"[{idx}/{len(POSTS)}] {post['title']}")
        print(f"{'='*60}")

        # 1) 이미지 업로드
        img_htmls = []
        first_media_id = None
        for j, (photo_id, alt) in enumerate(post["images"]):
            tmp = download_image(photo_id)
            if not tmp:
                img_htmls.append("")
                continue
            mid, murl = upload_image(tmp, f"{post['slug']}-{j+1}", alt)
            os.unlink(tmp)
            if murl:
                img_htmls.append(img_block(murl, alt))
                if first_media_id is None:
                    first_media_id = mid
                print(f"  이미지 {j+1} OK -> {murl}")
            else:
                img_htmls.append("")
            time.sleep(0.5)

        # 2) 콘텐츠 생성
        content = post["content"](img_htmls)

        # 3) 발행
        payload = {
            "title": post["title"],
            "content": content,
            "status": "publish",
            "slug": post["slug"],
            "categories": [post["cat"]],
        }
        if first_media_id:
            payload["featured_media"] = first_media_id

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(API, data=data, method="POST")
        req.add_header("Authorization", f"Basic {AUTH}")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                r = json.loads(resp.read().decode())
                pid = r.get("id")
                link = r.get("link", "")
                print(f"  발행 OK | ID:{pid} | {link}")
                published.append(link)
        except Exception as e:
            print(f"  발행 FAIL | {e}")
        time.sleep(1)

    # 네이버/Bing/Yandex IndexNow
    if published:
        print(f"\n{'='*60}")
        print("네이버/Bing/Yandex IndexNow 제출")
        print(f"{'='*60}")
        naver_payload = {
            "host": "devupbox.com",
            "key": "8dbbd7d6729b4a65b7dce4b9083c65e3",
            "keyLocation": "https://devupbox.com/8dbbd7d6729b4a65b7dce4b9083c65e3.txt",
            "urlList": published
        }
        ndata = json.dumps(naver_payload).encode("utf-8")
        for name, eurl in [("Naver", "https://searchadvisor.naver.com/indexnow"), ("Bing", "https://www.bing.com/indexnow"), ("Yandex", "https://yandex.com/indexnow")]:
            req = urllib.request.Request(eurl, data=ndata, method="POST")
            req.add_header("Content-Type", "application/json; charset=utf-8")
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    print(f"  {name}: HTTP {resp.status}")
            except urllib.error.HTTPError as e:
                print(f"  {name}: HTTP {e.code}")
            except Exception as e:
                print(f"  {name}: {e}")
    print(f"\n완료! 총 {len(published)}개 포스트 발행")


if __name__ == "__main__":
    main()

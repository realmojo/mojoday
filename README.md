# Mojoday — 회사 소개 웹사이트

모조데이(Mojoday)의 회사 소개 웹사이트입니다. Next.js(App Router) + Tailwind CSS로 만들어졌으며,
Cloudflare Workers(OpenNext)로 배포합니다.

## 회사 정보

| 항목 | 내용 |
| --- | --- |
| 상호 | 모조데이 (Mojoday) |
| 대표자 | 정만경 (JungManKyung) |
| 업종 | 인터넷 / 정보 서비스 (Internet / Information services) |
| 사업 분야 | 웹페이지 디자인 및 마케팅 서비스 (Web page designing and marketing services) |
| 소재지 | (07280) 서울특별시 영등포구 선유로 71 |
| Address | 71, Seonyu-ro, Yeongdeungpo-gu, Seoul, Republic of Korea |
| 전화 | 010-8126-1326 |
| 웹사이트 | https://mojoday.app |

회사 정보는 `lib/company.ts` 한 곳에서 관리합니다. 정보가 변경되면 이 파일만 수정하면
모든 페이지와 구조화 데이터(JSON-LD)에 반영됩니다.

## 페이지 구성

| 경로 | 설명 |
| --- | --- |
| `/` | 메인 — 소개, 서비스 요약, 일하는 방식, 회사 개요, 연락처 |
| `/about` | 회사 소개 — 대표 인사말, 가치, 연혁, 회사 개요 |
| `/services` | 서비스 — 웹페이지 디자인, 웹 개발·운영, 디지털 마케팅, 진행 절차 |
| `/contact` | 문의하기 — 연락처, 오시는 길, 자주 묻는 질문 |
| `/terms` | 이용약관 |
| `/privacy` | 개인정보처리방침 |

## 개발

```bash
npm install
npm run dev      # http://localhost:3000
npm run lint
npm run build
```

## 배포 (Cloudflare Workers)

```bash
npm run preview  # 로컬에서 Worker 빌드 결과 확인
npm run deploy   # Cloudflare에 배포
```

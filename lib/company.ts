/**
 * 모조데이(Mojoday) 회사 정보 — 사이트 전역에서 참조하는 단일 출처.
 * 회사 정보가 바뀌면 이 파일만 수정하면 모든 페이지에 반영됩니다.
 */

export const company = {
  name: "모조데이",
  nameEn: "Mojoday",
  legalName: "Mojoday",
  tagline: "웹으로 브랜드의 하루를 디자인합니다",
  description:
    "모조데이는 웹사이트 디자인·개발부터 검색 최적화와 디지털 마케팅까지, 브랜드가 온라인에서 성장하는 데 필요한 모든 과정을 함께하는 인터넷 정보 서비스 기업입니다.",
  representative: {
    name: "정만경",
    nameEn: "JungManKyung",
    title: "대표",
  },
  founded: "2024",
  industry: {
    major: "인터넷 / 정보 서비스",
    majorEn: "Internet / Information services",
    sub: "웹페이지 디자인 및 마케팅 서비스",
    subEn: "Web page designing and marketing services",
  },
  address: {
    country: "대한민국",
    countryEn: "South Korea",
    postalCode: "07280",
    full: "서울특별시 영등포구 선유로 71",
    fullEn: "71, Seonyu-ro, Yeongdeungpo-gu, Seoul, Republic of Korea",
    region: "서울특별시",
    regionEn: "Seoul",
    locality: "영등포구",
    localityEn: "Yeongdeungpo-gu",
    street: "선유로 71",
    streetEn: "71, Seonyu-ro",
  },
  phone: {
    display: "010-8126-1326",
    raw: "01081261326",
    tel: "+82-10-8126-1326",
  },
  email: "hello@mojoday.app",
  website: "https://mojoday.app",
  businessHours: "평일 10:00 – 19:00 (주말 · 공휴일 휴무)",
} as const;

export const services = [
  {
    id: "web-design",
    title: "웹페이지 디자인",
    summary:
      "브랜드의 성격을 그대로 옮긴 화면을 설계합니다. 기획부터 UI 디자인, 반응형 퍼블리싱까지 한 팀에서 진행합니다.",
    items: [
      "브랜드 · 서비스 소개 웹사이트",
      "랜딩페이지 및 캠페인 페이지",
      "반응형 UI/UX 디자인",
      "디자인 시스템 · 브랜드 가이드",
    ],
  },
  {
    id: "web-development",
    title: "웹 개발 · 운영",
    summary:
      "빠르게 뜨고 오래 유지되는 웹을 만듭니다. 최신 웹 표준 기반으로 구축하고, 오픈 이후 운영까지 책임집니다.",
    items: [
      "Next.js 기반 웹사이트 구축",
      "CMS · 관리자 페이지 연동",
      "웹 성능 · 접근성 개선",
      "유지보수 및 기술 지원",
    ],
  },
  {
    id: "marketing",
    title: "디지털 마케팅",
    summary:
      "만들어 놓고 기다리지 않습니다. 검색 유입과 광고 채널을 함께 설계해 실제 성과로 이어지도록 운영합니다.",
    items: [
      "검색 최적화(SEO) 컨설팅",
      "콘텐츠 기획 및 제작",
      "검색 · 디스플레이 광고 운영",
      "성과 측정 및 리포팅",
    ],
  },
] as const;

export const values = [
  {
    title: "본질에 집중합니다",
    body: "화려한 장식보다 고객이 원하는 정보에 가장 빨리 닿는 구조를 먼저 고민합니다.",
  },
  {
    title: "숫자로 증명합니다",
    body: "감각에 기대지 않고 유입, 체류, 전환 지표를 기준으로 개선 방향을 정합니다.",
  },
  {
    title: "오래 함께합니다",
    body: "오픈은 시작일 뿐입니다. 운영하며 쌓이는 데이터를 바탕으로 계속 다듬어 갑니다.",
  },
] as const;

export const milestones = [
  { year: "2024", body: "모조데이 설립, 웹사이트 디자인 · 개발 서비스 시작" },
  { year: "2025", body: "디지털 마케팅 · 검색 최적화(SEO) 컨설팅 영역 확장" },
  { year: "2026", body: "자체 웹 서비스 운영 및 브랜드 성장 파트너십 확대" },
] as const;

import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { Button } from "@/components/ui/button";
import { company, milestones, values } from "@/lib/company";

export const metadata: Metadata = {
  title: "회사 소개",
  description: `${company.name}(${company.nameEn})는 웹페이지 디자인과 디지털 마케팅을 함께 제공하는 인터넷 정보 서비스 기업입니다. 대표 ${company.representative.name}, 서울 영등포구 소재.`,
  alternates: { canonical: "/about" },
};

const profile = [
  { label: "상호", value: `${company.name} (${company.nameEn})` },
  { label: "대표자", value: `${company.representative.name} (${company.representative.nameEn})` },
  { label: "설립", value: `${company.founded}년` },
  {
    label: "업종",
    value: `${company.industry.major} / ${company.industry.majorEn}`,
  },
  {
    label: "사업 분야",
    value: `${company.industry.sub} / ${company.industry.subEn}`,
  },
  {
    label: "소재지",
    value: `(${company.address.postalCode}) ${company.address.full}`,
  },
  { label: "Address", value: company.address.fullEn },
  { label: "대표 전화", value: company.phone.display },
  { label: "이메일", value: company.email },
  { label: "웹사이트", value: company.website },
];

export default function AboutPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <SiteHeader />

      <main className="flex-1">
        {/* Header */}
        <section className="border-b bg-muted/40">
          <div className="container mx-auto px-4 py-16 md:px-6 md:py-24">
            <div className="max-w-3xl">
              <span className="text-sm font-medium text-muted-foreground">About</span>
              <h1 className="mt-3 text-4xl font-bold tracking-tight md:text-5xl">
                회사 소개
              </h1>
              <p className="mt-6 text-base leading-relaxed text-muted-foreground md:text-lg">
                {company.description}
              </p>
            </div>
          </div>
        </section>

        {/* 대표 인사말 */}
        <section className="border-b py-20 md:py-24">
          <div className="container mx-auto px-4 md:px-6">
            <div className="grid gap-12 lg:grid-cols-[1fr_1.4fr]">
              <div>
                <h2 className="text-2xl font-bold tracking-tight md:text-3xl">
                  대표 인사말
                </h2>
              </div>
              <div className="space-y-5 leading-relaxed text-muted-foreground">
                <p>
                  안녕하세요, {company.name} 대표 {company.representative.name}입니다.
                </p>
                <p>
                  웹사이트는 많은 브랜드가 고객을 처음 만나는 자리입니다. 그런데 잘 만든 웹사이트가
                  아무에게도 닿지 않거나, 사람은 모였는데 정작 화면이 그 기대를 받아내지 못하는
                  경우를 자주 보았습니다. 모조데이는 그 간극을 좁히기 위해 시작했습니다.
                </p>
                <p>
                  저희는 디자인과 개발, 그리고 마케팅을 따로 떼어 생각하지 않습니다. 어떤 검색어로
                  들어올 사람인지 먼저 그려보고 화면을 설계하며, 공개한 뒤에는 실제 데이터를 보며
                  계속 다듬습니다. 규모가 큰 프로젝트든 한 페이지짜리 소개 사이트든, 같은 기준으로
                  임합니다.
                </p>
                <p>
                  브랜드의 하루하루가 더 잘 보이도록, 오래 함께할 수 있는 파트너가 되겠습니다.
                  감사합니다.
                </p>
                <p className="pt-2 font-medium text-foreground">
                  {company.name} {company.representative.title} {company.representative.name}
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* 가치 */}
        <section className="border-b bg-muted/40 py-20 md:py-24">
          <div className="container mx-auto px-4 md:px-6">
            <h2 className="text-2xl font-bold tracking-tight md:text-3xl">일하는 방식</h2>
            <div className="mt-10 grid gap-6 md:grid-cols-3">
              {values.map((value) => (
                <div key={value.title} className="rounded-2xl bg-background p-7">
                  <h3 className="text-lg font-semibold">{value.title}</h3>
                  <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
                    {value.body}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 연혁 */}
        <section className="border-b py-20 md:py-24">
          <div className="container mx-auto px-4 md:px-6">
            <h2 className="text-2xl font-bold tracking-tight md:text-3xl">연혁</h2>
            <ol className="mt-10 space-y-0 border-l">
              {milestones.map((milestone) => (
                <li key={milestone.year} className="relative py-5 pl-8">
                  <span
                    aria-hidden
                    className="absolute -left-[5px] top-7 h-2.5 w-2.5 rounded-full bg-foreground"
                  />
                  <div className="text-sm font-semibold">{milestone.year}</div>
                  <p className="mt-1 text-sm text-muted-foreground">{milestone.body}</p>
                </li>
              ))}
            </ol>
          </div>
        </section>

        {/* 회사 개요 */}
        <section className="border-b py-20 md:py-24">
          <div className="container mx-auto px-4 md:px-6">
            <h2 className="text-2xl font-bold tracking-tight md:text-3xl">회사 개요</h2>
            <dl className="mt-10 divide-y rounded-2xl border">
              {profile.map(({ label, value }) => (
                <div
                  key={label}
                  className="grid grid-cols-1 gap-1 px-6 py-4 sm:grid-cols-[10rem_1fr] sm:gap-4"
                >
                  <dt className="text-sm font-medium text-muted-foreground">{label}</dt>
                  <dd className="text-sm break-words">{value}</dd>
                </div>
              ))}
            </dl>
          </div>
        </section>

        {/* CTA */}
        <section className="py-20 md:py-24">
          <div className="container mx-auto px-4 text-center md:px-6">
            <h2 className="text-2xl font-bold tracking-tight md:text-3xl">
              모조데이와 이야기 나눠보세요
            </h2>
            <p className="mt-4 text-muted-foreground">
              프로젝트 문의부터 간단한 상담까지 언제든 환영합니다.
            </p>
            <Button asChild size="lg" className="mt-8">
              <Link href="/contact">
                문의하기
                <ArrowRight className="ml-1 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </section>
      </main>

      <SiteFooter />
    </div>
  );
}

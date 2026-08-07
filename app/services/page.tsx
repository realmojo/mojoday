import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight, Check } from "lucide-react";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { Button } from "@/components/ui/button";
import { company, services } from "@/lib/company";

export const metadata: Metadata = {
  title: "서비스",
  description:
    "웹페이지 디자인, 웹 개발 및 운영, 디지털 마케팅. 모조데이가 제공하는 서비스와 진행 절차를 안내합니다.",
  alternates: { canonical: "/services" },
};

const process = [
  {
    step: "01",
    title: "상담 · 요구사항 정리",
    body: "만들고 싶은 것, 이미 가진 자산, 일정과 예산을 함께 확인하며 프로젝트 범위를 정합니다.",
  },
  {
    step: "02",
    title: "기획 · 구조 설계",
    body: "타깃과 검색 키워드를 기준으로 페이지 구성과 정보 구조를 설계합니다.",
  },
  {
    step: "03",
    title: "디자인 · 개발",
    body: "화면 디자인과 반응형 구현을 진행합니다. 중간 단계마다 확인용 링크를 공유합니다.",
  },
  {
    step: "04",
    title: "오픈 · 성과 개선",
    body: "검색엔진 등록과 분석 도구를 연결하고, 데이터를 보며 지속적으로 개선합니다.",
  },
];

export default function ServicesPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <SiteHeader />

      <main className="flex-1">
        {/* Header */}
        <section className="border-b bg-muted/40">
          <div className="container mx-auto px-4 py-16 md:px-6 md:py-24">
            <div className="max-w-3xl">
              <span className="text-sm font-medium text-muted-foreground">Services</span>
              <h1 className="mt-3 text-4xl font-bold tracking-tight md:text-5xl">서비스</h1>
              <p className="mt-6 text-base leading-relaxed text-muted-foreground md:text-lg">
                {company.industry.sub}를 중심으로, 브랜드가 온라인에서 자리 잡는 데 필요한 과정을
                단계별로 지원합니다.
              </p>
            </div>
          </div>
        </section>

        {/* Services */}
        <section className="border-b py-20 md:py-24">
          <div className="container mx-auto space-y-16 px-4 md:px-6">
            {services.map((service, index) => (
              <div key={service.id} id={service.id} className="grid gap-8 lg:grid-cols-[1fr_1.4fr]">
                <div>
                  <span className="text-sm font-semibold text-muted-foreground">
                    0{index + 1}
                  </span>
                  <h2 className="mt-3 text-2xl font-bold tracking-tight md:text-3xl">
                    {service.title}
                  </h2>
                </div>
                <div>
                  <p className="leading-relaxed text-muted-foreground">{service.summary}</p>
                  <ul className="mt-8 grid gap-3 sm:grid-cols-2">
                    {service.items.map((item) => (
                      <li
                        key={item}
                        className="flex items-start gap-3 rounded-xl border p-4 text-sm"
                      >
                        <Check className="mt-0.5 h-4 w-4 shrink-0 text-muted-foreground" />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Process */}
        <section className="border-b bg-muted/40 py-20 md:py-24">
          <div className="container mx-auto px-4 md:px-6">
            <div className="max-w-2xl">
              <h2 className="text-2xl font-bold tracking-tight md:text-3xl">진행 절차</h2>
              <p className="mt-4 text-muted-foreground">
                문의부터 오픈 이후 운영까지, 프로젝트는 보통 네 단계로 진행됩니다.
              </p>
            </div>
            <div className="mt-12 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
              {process.map(({ step, title, body }) => (
                <div key={step} className="rounded-2xl bg-background p-7">
                  <span className="text-sm font-semibold text-muted-foreground">{step}</span>
                  <h3 className="mt-3 font-semibold">{title}</h3>
                  <p className="mt-3 text-sm leading-relaxed text-muted-foreground">{body}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="py-20 md:py-24">
          <div className="container mx-auto px-4 text-center md:px-6">
            <h2 className="text-2xl font-bold tracking-tight md:text-3xl">
              어떤 것부터 시작하면 좋을지 함께 정해드립니다
            </h2>
            <p className="mt-4 text-muted-foreground">
              현재 상황을 알려주시면 필요한 범위와 일정을 정리해 회신드립니다.
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

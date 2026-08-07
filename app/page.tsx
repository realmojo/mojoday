import Link from "next/link";
import { ArrowRight, Building2, Mail, MapPin, Phone } from "lucide-react";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { Button } from "@/components/ui/button";
import { company, services, values } from "@/lib/company";

const overview = [
  { label: "상호", value: `${company.name} (${company.nameEn})` },
  { label: "대표자", value: company.representative.name },
  { label: "설립", value: `${company.founded}년` },
  { label: "업종", value: company.industry.major },
  { label: "사업 분야", value: company.industry.sub },
  { label: "소재지", value: `${company.address.full} (${company.address.postalCode})` },
  { label: "대표 전화", value: company.phone.display },
  { label: "이메일", value: company.email },
];

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col">
      <SiteHeader />

      <main className="flex-1">
        {/* Hero */}
        <section className="relative overflow-hidden border-b">
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0 bg-[radial-gradient(60rem_40rem_at_50%_-20%,var(--color-accent),transparent)]"
          />
          <div className="container relative mx-auto px-4 py-24 md:px-6 md:py-32">
            <div className="mx-auto max-w-3xl text-center">
              <span className="inline-flex items-center rounded-full border bg-background px-3 py-1 text-xs font-medium text-muted-foreground">
                Internet / Information Services · Seoul, Korea
              </span>
              <h1 className="mt-6 text-4xl font-bold leading-tight tracking-tight md:text-6xl">
                {company.tagline}
              </h1>
              <p className="mt-6 text-base leading-relaxed text-muted-foreground md:text-lg">
                {company.description}
              </p>
              <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row">
                <Button asChild size="lg">
                  <Link href="/contact">
                    프로젝트 문의하기
                    <ArrowRight className="ml-1 h-4 w-4" />
                  </Link>
                </Button>
                <Button asChild size="lg" variant="outline">
                  <Link href="/about">회사 소개 보기</Link>
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* Services */}
        <section id="services" className="border-b py-20 md:py-28">
          <div className="container mx-auto px-4 md:px-6">
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-3xl font-bold tracking-tight md:text-4xl">
                무엇을 하는 회사인가요
              </h2>
              <p className="mt-4 text-muted-foreground">
                웹페이지 디자인과 마케팅을 하나의 흐름으로 연결해, 만드는 일과 알리는 일을 함께
                책임집니다.
              </p>
            </div>

            <div className="mt-14 grid gap-6 md:grid-cols-3">
              {services.map((service) => (
                <div
                  key={service.id}
                  className="flex flex-col rounded-2xl border bg-card p-7 transition-shadow hover:shadow-md"
                >
                  <h3 className="text-lg font-semibold">{service.title}</h3>
                  <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
                    {service.summary}
                  </p>
                  <ul className="mt-6 space-y-2 border-t pt-6 text-sm text-muted-foreground">
                    {service.items.map((item) => (
                      <li key={item} className="flex gap-2">
                        <span aria-hidden className="text-foreground">
                          ·
                        </span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>

            <div className="mt-10 text-center">
              <Link
                href="/services"
                className="inline-flex items-center gap-1 text-sm font-medium hover:underline"
              >
                서비스 자세히 보기
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>
        </section>

        {/* Values */}
        <section className="border-b bg-muted/40 py-20 md:py-28">
          <div className="container mx-auto px-4 md:px-6">
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-3xl font-bold tracking-tight md:text-4xl">
                일하는 방식
              </h2>
              <p className="mt-4 text-muted-foreground">
                모조데이가 프로젝트를 대하는 세 가지 기준입니다.
              </p>
            </div>

            <div className="mt-14 grid gap-6 md:grid-cols-3">
              {values.map((value, index) => (
                <div key={value.title} className="rounded-2xl bg-background p-7">
                  <span className="text-sm font-semibold text-muted-foreground">
                    0{index + 1}
                  </span>
                  <h3 className="mt-3 text-lg font-semibold">{value.title}</h3>
                  <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
                    {value.body}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Company overview */}
        <section id="company" className="border-b py-20 md:py-28">
          <div className="container mx-auto px-4 md:px-6">
            <div className="grid gap-12 lg:grid-cols-[1fr_1.2fr]">
              <div>
                <span className="inline-flex items-center gap-2 text-sm font-medium text-muted-foreground">
                  <Building2 className="h-4 w-4" />
                  Company
                </span>
                <h2 className="mt-4 text-3xl font-bold tracking-tight md:text-4xl">
                  회사 개요
                </h2>
                <p className="mt-4 leading-relaxed text-muted-foreground">
                  모조데이는 서울 영등포구에 자리한 인터넷 정보 서비스 기업입니다. 웹페이지
                  디자인과 마케팅 서비스를 주된 사업으로 하며, 자체 웹 서비스도 직접 기획하고
                  운영하고 있습니다.
                </p>
              </div>

              <dl className="divide-y rounded-2xl border">
                {overview.map(({ label, value }) => (
                  <div
                    key={label}
                    className="grid grid-cols-1 gap-1 px-6 py-4 sm:grid-cols-[8rem_1fr] sm:gap-4"
                  >
                    <dt className="text-sm font-medium text-muted-foreground">{label}</dt>
                    <dd className="text-sm">{value}</dd>
                  </div>
                ))}
              </dl>
            </div>
          </div>
        </section>

        {/* Contact CTA */}
        <section className="py-20 md:py-28">
          <div className="container mx-auto px-4 md:px-6">
            <div className="mx-auto max-w-3xl text-center">
              <h2 className="text-3xl font-bold tracking-tight md:text-4xl">
                함께할 프로젝트가 있으신가요
              </h2>
              <p className="mt-4 leading-relaxed text-muted-foreground">
                간단한 아이디어 단계여도 좋습니다. 어떤 것을 만들고 싶은지 알려주시면 방향을 함께
                정리해 드립니다.
              </p>
            </div>

            <div className="mx-auto mt-12 grid max-w-3xl gap-4 sm:grid-cols-3">
              <a
                href={`tel:${company.phone.tel}`}
                className="flex flex-col items-center gap-2 rounded-2xl border p-6 text-center transition-colors hover:bg-accent"
              >
                <Phone className="h-5 w-5 text-muted-foreground" />
                <span className="text-xs text-muted-foreground">전화</span>
                <span className="text-sm font-medium">{company.phone.display}</span>
              </a>
              <a
                href={`mailto:${company.email}`}
                className="flex flex-col items-center gap-2 rounded-2xl border p-6 text-center transition-colors hover:bg-accent"
              >
                <Mail className="h-5 w-5 text-muted-foreground" />
                <span className="text-xs text-muted-foreground">이메일</span>
                <span className="text-sm font-medium">{company.email}</span>
              </a>
              <Link
                href="/contact"
                className="flex flex-col items-center gap-2 rounded-2xl border p-6 text-center transition-colors hover:bg-accent"
              >
                <MapPin className="h-5 w-5 text-muted-foreground" />
                <span className="text-xs text-muted-foreground">오시는 길</span>
                <span className="text-sm font-medium">{company.address.locality}</span>
              </Link>
            </div>
          </div>
        </section>
      </main>

      <SiteFooter />
    </div>
  );
}

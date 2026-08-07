import type { Metadata } from "next";
import { Clock, Globe, Mail, MapPin, Phone } from "lucide-react";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { Button } from "@/components/ui/button";
import { company } from "@/lib/company";

export const metadata: Metadata = {
  title: "문의하기",
  description: `${company.name}(${company.nameEn}) 연락처 안내. 전화 ${company.phone.display}, 이메일 ${company.email}, 주소 ${company.address.full}.`,
  alternates: { canonical: "/contact" },
};

const mapQuery = encodeURIComponent(company.address.fullEn);

const channels = [
  {
    icon: Phone,
    label: "전화",
    value: company.phone.display,
    href: `tel:${company.phone.tel}`,
  },
  {
    icon: Mail,
    label: "이메일",
    value: company.email,
    href: `mailto:${company.email}`,
  },
  {
    icon: Globe,
    label: "웹사이트",
    value: company.website.replace("https://", ""),
    href: company.website,
  },
];

const faqs = [
  {
    q: "어떤 규모의 프로젝트까지 가능한가요?",
    a: "한 페이지짜리 소개 사이트부터 여러 페이지로 구성된 브랜드 사이트, 운영이 필요한 웹 서비스까지 진행합니다. 문의 시 원하는 범위를 알려주시면 적정한 구성으로 제안드립니다.",
  },
  {
    q: "제작 기간은 얼마나 걸리나요?",
    a: "페이지 수와 준비된 자료에 따라 다르지만, 소개 사이트 기준으로 보통 2~4주 정도 소요됩니다. 상담 단계에서 정확한 일정을 안내드립니다.",
  },
  {
    q: "오픈 이후 운영도 맡길 수 있나요?",
    a: "네. 콘텐츠 업데이트, 검색 최적화, 광고 운영까지 이어서 진행할 수 있습니다. 필요한 항목만 선택해 요청하셔도 됩니다.",
  },
  {
    q: "문의하면 언제 답변을 받을 수 있나요?",
    a: `${company.businessHours} 기준으로 영업일 1~2일 이내에 회신드립니다.`,
  },
];

export default function ContactPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <SiteHeader />

      <main className="flex-1">
        {/* Header */}
        <section className="border-b bg-muted/40">
          <div className="container mx-auto px-4 py-16 md:px-6 md:py-24">
            <div className="max-w-3xl">
              <span className="text-sm font-medium text-muted-foreground">Contact</span>
              <h1 className="mt-3 text-4xl font-bold tracking-tight md:text-5xl">문의하기</h1>
              <p className="mt-6 text-base leading-relaxed text-muted-foreground md:text-lg">
                프로젝트 문의, 견적 요청, 제휴 제안 모두 환영합니다. 아래 연락처로 편하게
                연락주세요.
              </p>
            </div>
          </div>
        </section>

        {/* 연락처 */}
        <section className="border-b py-16 md:py-20">
          <div className="container mx-auto px-4 md:px-6">
            <div className="grid gap-4 sm:grid-cols-3">
              {channels.map(({ icon: Icon, label, value, href }) => (
                <a
                  key={label}
                  href={href}
                  className="flex flex-col gap-2 rounded-2xl border p-6 transition-colors hover:bg-accent"
                  {...(href.startsWith("http")
                    ? { target: "_blank", rel: "noreferrer" }
                    : {})}
                >
                  <Icon className="h-5 w-5 text-muted-foreground" />
                  <span className="text-xs text-muted-foreground">{label}</span>
                  <span className="text-sm font-medium break-all">{value}</span>
                </a>
              ))}
            </div>

            <div className="mt-10 rounded-2xl border p-8">
              <h2 className="text-lg font-semibold">이메일로 문의하기</h2>
              <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
                아래 내용을 함께 보내주시면 더 정확한 답변을 드릴 수 있습니다.
              </p>
              <ul className="mt-4 space-y-1.5 text-sm text-muted-foreground">
                <li>· 회사 또는 브랜드 소개</li>
                <li>· 필요한 작업(웹사이트 제작 / 리뉴얼 / 마케팅 등)</li>
                <li>· 희망 일정과 예산 범위</li>
                <li>· 참고할 만한 사이트나 자료</li>
              </ul>
              <Button asChild className="mt-6">
                <a href={`mailto:${company.email}?subject=${encodeURIComponent("[프로젝트 문의] ")}`}>
                  {company.email}로 메일 보내기
                </a>
              </Button>
            </div>
          </div>
        </section>

        {/* 오시는 길 */}
        <section className="border-b bg-muted/40 py-16 md:py-20">
          <div className="container mx-auto px-4 md:px-6">
            <h2 className="text-2xl font-bold tracking-tight md:text-3xl">오시는 길</h2>
            <div className="mt-8 grid gap-6 md:grid-cols-2">
              <div className="rounded-2xl bg-background p-7">
                <div className="flex items-start gap-3">
                  <MapPin className="mt-0.5 h-5 w-5 shrink-0 text-muted-foreground" />
                  <div className="space-y-1">
                    <p className="text-sm font-medium">주소</p>
                    <p className="text-sm text-muted-foreground">
                      ({company.address.postalCode}) {company.address.full}
                    </p>
                    <p className="text-sm text-muted-foreground">{company.address.fullEn}</p>
                  </div>
                </div>
                <Button asChild variant="outline" size="sm" className="mt-6">
                  <a
                    href={`https://www.google.com/maps/search/?api=1&query=${mapQuery}`}
                    target="_blank"
                    rel="noreferrer"
                  >
                    지도에서 보기
                  </a>
                </Button>
              </div>

              <div className="rounded-2xl bg-background p-7">
                <div className="flex items-start gap-3">
                  <Clock className="mt-0.5 h-5 w-5 shrink-0 text-muted-foreground" />
                  <div className="space-y-1">
                    <p className="text-sm font-medium">운영 시간</p>
                    <p className="text-sm text-muted-foreground">{company.businessHours}</p>
                    <p className="text-sm text-muted-foreground">
                      운영 시간 외 문의는 이메일로 남겨주시면 순차적으로 회신드립니다.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* FAQ */}
        <section className="py-16 md:py-20">
          <div className="container mx-auto px-4 md:px-6">
            <h2 className="text-2xl font-bold tracking-tight md:text-3xl">자주 묻는 질문</h2>
            <div className="mt-8 grid gap-4 md:grid-cols-2">
              {faqs.map(({ q, a }) => (
                <div key={q} className="rounded-2xl border p-6">
                  <h3 className="font-semibold">{q}</h3>
                  <p className="mt-3 text-sm leading-relaxed text-muted-foreground">{a}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>

      <SiteFooter />
    </div>
  );
}

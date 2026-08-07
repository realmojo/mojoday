import type { Metadata } from "next";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { company } from "@/lib/company";

export const metadata: Metadata = {
  title: "이용약관",
  description: `${company.name}(${company.nameEn}) 웹사이트 이용약관입니다.`,
  alternates: { canonical: "/terms" },
};

const EFFECTIVE_DATE = "2026년 1월 1일";

const sections = [
  {
    title: "제1조 (목적)",
    body: [
      `본 약관은 ${company.name}(${company.nameEn}, 이하 "회사")가 운영하는 웹사이트(${company.website}, 이하 "사이트")의 이용과 관련하여 회사와 이용자 간의 권리, 의무 및 책임사항을 규정함을 목적으로 합니다.`,
    ],
  },
  {
    title: "제2조 (정의)",
    body: [
      '"사이트"란 회사가 회사 및 서비스 정보를 제공하기 위하여 운영하는 웹사이트를 말합니다.',
      '"이용자"란 사이트에 접속하여 본 약관에 따라 사이트가 제공하는 정보를 이용하는 자를 말합니다.',
      '"콘텐츠"란 사이트에 게시된 문자, 이미지, 디자인, 로고 등 일체의 자료를 말합니다.',
    ],
  },
  {
    title: "제3조 (약관의 효력 및 변경)",
    body: [
      "본 약관은 사이트에 게시함으로써 효력이 발생합니다.",
      "회사는 관련 법령을 위반하지 않는 범위에서 본 약관을 변경할 수 있으며, 변경된 약관은 사이트에 공지한 시점부터 효력이 발생합니다.",
    ],
  },
  {
    title: "제4조 (서비스의 제공)",
    body: [
      "회사는 사이트를 통해 회사 소개, 서비스 소개, 문의 접수 안내 등의 정보를 제공합니다.",
      "회사는 사이트의 내용을 사전 통지 없이 변경하거나 중단할 수 있습니다. 다만 이용자에게 중대한 영향을 미치는 변경은 사전에 공지합니다.",
    ],
  },
  {
    title: "제5조 (이용자의 의무)",
    body: [
      "이용자는 사이트 이용 시 관련 법령과 본 약관을 준수하여야 합니다.",
      "이용자는 다음 각 호의 행위를 하여서는 안 됩니다.",
      "  가. 사이트의 정상적인 운영을 방해하는 행위",
      "  나. 회사 또는 제3자의 지식재산권을 침해하는 행위",
      "  다. 허위 정보를 게시하거나 타인의 명예를 훼손하는 행위",
      "  라. 자동화된 수단으로 사이트에 과도한 부하를 유발하는 행위",
    ],
  },
  {
    title: "제6조 (지식재산권)",
    body: [
      "사이트에 게시된 콘텐츠에 대한 저작권 및 기타 지식재산권은 회사에 귀속됩니다.",
      "이용자는 회사의 사전 서면 동의 없이 콘텐츠를 복제, 배포, 전송, 출판, 2차적 저작물 작성 등의 방법으로 이용할 수 없습니다.",
    ],
  },
  {
    title: "제7조 (면책조항)",
    body: [
      "회사는 천재지변, 정전, 통신 장애 등 불가항력으로 인하여 사이트를 제공할 수 없는 경우 책임을 지지 않습니다.",
      "회사는 사이트에 게시된 정보의 정확성을 확보하기 위해 노력하나, 정보의 이용으로 발생한 결과에 대하여는 이용자가 스스로 판단할 책임이 있습니다.",
      "사이트에 포함된 외부 링크를 통해 접속한 제3자 사이트의 내용에 대하여 회사는 책임을 지지 않습니다.",
    ],
  },
  {
    title: "제8조 (분쟁의 해결)",
    body: [
      "본 약관은 대한민국 법률에 따라 해석되고 적용됩니다.",
      "사이트 이용과 관련하여 회사와 이용자 간에 분쟁이 발생한 경우, 양 당사자는 성실히 협의하여 해결하며, 협의가 이루어지지 않을 경우 관할 법원은 민사소송법에 따릅니다.",
    ],
  },
];

export default function TermsPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <SiteHeader />

      <main className="flex-1">
        <section className="border-b bg-muted/40">
          <div className="container mx-auto px-4 py-16 md:px-6 md:py-20">
            <div className="max-w-3xl">
              <h1 className="text-4xl font-bold tracking-tight md:text-5xl">이용약관</h1>
              <p className="mt-4 text-sm text-muted-foreground">
                시행일 : {EFFECTIVE_DATE}
              </p>
            </div>
          </div>
        </section>

        <section className="py-16 md:py-20">
          <div className="container mx-auto px-4 md:px-6">
            <div className="max-w-3xl space-y-10">
              {sections.map(({ title, body }) => (
                <div key={title}>
                  <h2 className="text-lg font-semibold">{title}</h2>
                  <div className="mt-3 space-y-2">
                    {body.map((line) => (
                      <p
                        key={line}
                        className="text-sm leading-relaxed whitespace-pre-wrap text-muted-foreground"
                      >
                        {line}
                      </p>
                    ))}
                  </div>
                </div>
              ))}

              <div className="rounded-2xl border p-6 text-sm leading-relaxed text-muted-foreground">
                <p className="font-medium text-foreground">문의처</p>
                <p className="mt-2">
                  {company.name} ({company.nameEn}) · 대표 {company.representative.name}
                </p>
                <p>
                  ({company.address.postalCode}) {company.address.full}
                </p>
                <p>
                  전화 {company.phone.display} · 이메일 {company.email}
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>

      <SiteFooter />
    </div>
  );
}

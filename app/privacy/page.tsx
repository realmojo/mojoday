import type { Metadata } from "next";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { company } from "@/lib/company";

export const metadata: Metadata = {
  title: "개인정보처리방침",
  description: `${company.name}(${company.nameEn})의 개인정보처리방침입니다. 수집 항목, 이용 목적, 보유 기간 및 이용자 권리를 안내합니다.`,
  alternates: { canonical: "/privacy" },
};

const EFFECTIVE_DATE = "2026년 1월 1일";

const sections = [
  {
    title: "1. 총칙",
    body: [
      `${company.name}(${company.nameEn}, 이하 "회사")는 이용자의 개인정보를 중요하게 생각하며, 「개인정보 보호법」 등 관련 법령을 준수합니다.`,
      `본 방침은 회사가 운영하는 웹사이트(${company.website})에 적용됩니다.`,
    ],
  },
  {
    title: "2. 수집하는 개인정보 항목 및 수집 방법",
    body: [
      "회사 웹사이트는 회원가입 절차를 두지 않으며, 이용자가 직접 정보를 입력하는 온라인 양식을 운영하지 않습니다.",
      "다만 다음의 경우에 한하여 개인정보가 수집될 수 있습니다.",
      "  가. 이메일 또는 전화로 문의하신 경우 : 성명(또는 회사명), 이메일 주소, 연락처, 문의 내용 등 이용자가 직접 제공한 정보",
      "  나. 웹사이트 이용 과정에서 자동으로 생성되는 정보 : 접속 IP 주소, 브라우저 및 기기 정보, 방문 일시, 방문 경로 등",
    ],
  },
  {
    title: "3. 개인정보의 이용 목적",
    body: [
      "문의 사항에 대한 답변 및 상담, 견적 안내",
      "계약 체결 및 서비스 제공을 위한 연락",
      "웹사이트 이용 통계 분석 및 서비스 품질 개선",
    ],
  },
  {
    title: "4. 개인정보의 보유 및 이용 기간",
    body: [
      "문의 및 상담 관련 정보 : 문의 처리 완료 후 3년간 보관 후 파기합니다.",
      "계약이 체결된 경우 : 관련 법령에서 정한 기간(전자상거래 등에서의 소비자보호에 관한 법률 등)에 따라 보관합니다.",
      "이용자가 삭제를 요청하는 경우, 법령상 보관 의무가 없는 정보는 지체 없이 파기합니다.",
    ],
  },
  {
    title: "5. 개인정보의 제3자 제공",
    body: [
      "회사는 이용자의 개인정보를 제3자에게 제공하지 않습니다.",
      "다만 법령에 근거하거나 수사기관이 적법한 절차에 따라 요청하는 경우에는 예외로 합니다.",
    ],
  },
  {
    title: "6. 쿠키 및 웹 분석 도구의 이용",
    body: [
      "회사는 웹사이트 이용 현황을 파악하기 위해 Google Analytics를 사용하며, 이 과정에서 쿠키가 사용될 수 있습니다.",
      "수집되는 정보는 통계 분석 목적으로만 활용되며 개인을 식별하지 않습니다.",
      "이용자는 브라우저 설정을 통해 쿠키 저장을 거부할 수 있습니다. 다만 이 경우 일부 기능 이용에 제한이 있을 수 있습니다.",
      "Google의 개인정보 처리에 관한 내용은 Google 개인정보처리방침(https://policies.google.com/privacy)을 참고하시기 바랍니다.",
    ],
  },
  {
    title: "7. 이용자의 권리와 행사 방법",
    body: [
      "이용자는 언제든지 자신의 개인정보에 대한 열람, 정정, 삭제, 처리정지를 요청할 수 있습니다.",
      `요청은 아래 개인정보 보호책임자의 연락처(이메일 ${company.email}, 전화 ${company.phone.display})로 접수하실 수 있으며, 회사는 지체 없이 필요한 조치를 취합니다.`,
    ],
  },
  {
    title: "8. 개인정보의 파기 절차 및 방법",
    body: [
      "보유 기간이 경과하거나 처리 목적이 달성된 개인정보는 지체 없이 파기합니다.",
      "전자적 파일 형태의 정보는 복구할 수 없는 기술적 방법으로 삭제하며, 종이 문서는 분쇄하거나 소각하여 파기합니다.",
    ],
  },
  {
    title: "9. 개인정보의 안전성 확보 조치",
    body: [
      "개인정보에 대한 접근 권한을 최소한의 인원으로 제한하고 있습니다.",
      "전송 구간 암호화(HTTPS)를 적용하고 있습니다.",
      "개인정보를 취급하는 인원을 대상으로 보호 의무를 정기적으로 안내합니다.",
    ],
  },
  {
    title: "10. 개인정보 보호책임자",
    body: [
      `성명 : ${company.representative.name} (${company.representative.title})`,
      `이메일 : ${company.email}`,
      `전화 : ${company.phone.display}`,
      `주소 : (${company.address.postalCode}) ${company.address.full}`,
      "개인정보 침해에 관한 상담이 필요한 경우 개인정보침해신고센터(privacy.kisa.or.kr, 국번없이 118) 등에 문의하실 수 있습니다.",
    ],
  },
  {
    title: "11. 방침의 변경",
    body: [
      "본 방침의 내용이 추가, 삭제, 수정될 경우 시행일로부터 최소 7일 전에 웹사이트를 통해 공지합니다.",
    ],
  },
];

export default function PrivacyPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <SiteHeader />

      <main className="flex-1">
        <section className="border-b bg-muted/40">
          <div className="container mx-auto px-4 py-16 md:px-6 md:py-20">
            <div className="max-w-3xl">
              <h1 className="text-4xl font-bold tracking-tight md:text-5xl">
                개인정보처리방침
              </h1>
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
            </div>
          </div>
        </section>
      </main>

      <SiteFooter />
    </div>
  );
}

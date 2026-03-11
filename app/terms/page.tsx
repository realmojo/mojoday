import type { Metadata } from "next";
import Link from "next/link";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";

export const metadata: Metadata = {
  title: "이용약관 - Mojoday",
  description: "Mojoday 서비스 이용약관",
  alternates: { canonical: "/terms" },
};

const sections = [
  {
    title: "제1조 (목적)",
    content: `이 약관은 Mojoday(이하 "서비스")가 제공하는 AI 여행 계획 서비스의 이용과 관련하여 서비스와 이용자 간의 권리, 의무 및 책임사항, 기타 필요한 사항을 규정함을 목적으로 합니다.`,
  },
  {
    title: "제2조 (정의)",
    content: `① "서비스"란 Mojoday가 제공하는 AI 기반 여행 계획 생성 서비스 및 관련 제반 서비스를 의미합니다.\n② "이용자"란 이 약관에 따라 서비스를 이용하는 자를 말합니다.\n③ "콘텐츠"란 이용자가 서비스를 이용하여 생성하거나 열람하는 모든 정보를 말합니다.`,
  },
  {
    title: "제3조 (약관의 게시와 개정)",
    content: `① 서비스는 이 약관의 내용을 이용자가 쉽게 알 수 있도록 서비스 초기 화면에 게시합니다.\n② 서비스는 관련 법령을 위반하지 않는 범위에서 이 약관을 개정할 수 있습니다.\n③ 약관이 개정될 경우 서비스는 개정 내용과 적용 일자를 명시하여 공지합니다.`,
  },
  {
    title: "제4조 (서비스의 제공)",
    content: `① 서비스는 다음의 서비스를 제공합니다.\n- 유튜브 영상 URL 기반 여행 정보 분석 서비스\n- AI 기반 여행 일정 자동 생성 서비스\n- 여행 계획 편집 및 저장 서비스\n② 서비스는 운영상, 기술상의 필요에 따라 제공하는 서비스를 변경할 수 있습니다.`,
  },
  {
    title: "제5조 (서비스 이용)",
    content: `① 서비스는 연중무휴, 1일 24시간 제공함을 원칙으로 합니다.\n② 서비스는 시스템 점검, 증설 및 교체, 고장, 통신 두절 등의 경우 서비스의 제공을 일시적으로 중단할 수 있습니다.\n③ 이용자는 서비스 이용 시 타인의 저작권을 침해하지 않도록 주의해야 합니다.`,
  },
  {
    title: "제6조 (이용자의 의무)",
    content: `이용자는 다음 행위를 해서는 안 됩니다.\n① 타인의 정보 도용\n② 서비스에서 얻은 정보를 서비스의 사전 승낙 없이 복제, 송신, 출판, 배포하는 행위\n③ 서비스의 정상적인 운영을 방해하는 행위\n④ 기타 불법적이거나 부당한 행위`,
  },
  {
    title: "제7조 (서비스의 저작권)",
    content: `① 서비스가 제공하는 저작물에 대한 저작권 및 기타 지적재산권은 서비스에 귀속합니다.\n② 이용자는 서비스를 이용함으로써 얻은 정보를 서비스의 사전 승낙 없이 복제, 송신, 출판, 배포할 수 없습니다.\n③ 이용자가 직접 생성한 여행 계획에 대한 권리는 이용자에게 귀속됩니다.`,
  },
  {
    title: "제8조 (면책조항)",
    content: `① 서비스는 AI가 생성한 여행 정보의 정확성, 완전성, 유용성에 대해 보증하지 않습니다.\n② AI가 생성한 여행 계획은 참고용으로만 활용하시고, 실제 여행 시에는 공식 정보를 반드시 확인하시기 바랍니다.\n③ 서비스는 이용자의 귀책사유로 인한 서비스 이용 장애에 대하여 책임을 지지 않습니다.`,
  },
  {
    title: "제9조 (분쟁 해결)",
    content: `① 서비스와 이용자 간에 발생한 분쟁에 관한 소송은 대한민국 법원을 관할 법원으로 합니다.\n② 서비스와 이용자 간의 분쟁에 대해서는 대한민국 법률을 적용합니다.`,
  },
];

export default function TermsPage() {
  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <SiteHeader />
      <main className="flex-1">
        <section className="py-16 border-b">
          <div className="container mx-auto px-4 md:px-6 max-w-3xl space-y-3">
            <h1 className="text-4xl font-bold tracking-tight">이용약관</h1>
            <p className="text-muted-foreground">
              시행일: 2025년 1월 1일 &nbsp;|&nbsp; 최종 수정: 2025년 1월 1일
            </p>
          </div>
        </section>

        <section className="py-12">
          <div className="container mx-auto px-4 md:px-6 max-w-3xl">
            <div className="prose prose-sm max-w-none space-y-8">
              {sections.map(({ title, content }) => (
                <div key={title} className="space-y-3">
                  <h2 className="text-lg font-bold">{title}</h2>
                  <div className="text-sm text-muted-foreground leading-relaxed whitespace-pre-line">
                    {content}
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-12 pt-8 border-t flex flex-wrap gap-4 text-sm text-muted-foreground">
              <span>문의사항은 <Link href="/contact" className="text-primary hover:underline">Contact</Link>를 통해 연락주세요.</span>
              <Link href="/privacy" className="text-primary hover:underline ml-auto">개인정보처리방침 →</Link>
            </div>
          </div>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}

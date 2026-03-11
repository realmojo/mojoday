import type { Metadata } from "next";
import Link from "next/link";
import Image from "next/image";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";

export const metadata: Metadata = {
  title: "About - Mojoday",
  description:
    "Mojoday는 여행 유튜브 영상을 AI로 분석해 나만의 여행 계획을 자동으로 만들어주는 서비스입니다.",
  alternates: { canonical: "/about" },
};

const values = [
  {
    emoji: "🎬",
    title: "영상에서 계획으로",
    desc: "좋아하는 유튜버의 여행 영상 URL 하나만 있으면 됩니다. AI가 영상 속 모든 정보를 분석해 완성된 여행 계획을 만들어드립니다.",
  },
  {
    emoji: "🗺️",
    title: "모든 정보를 한 곳에",
    desc: "장소, 맛집, 숙소, 교통, 예산까지 영상에서 언급된 정보를 빠짐없이 추출해 정리합니다.",
  },
  {
    emoji: "✏️",
    title: "나만의 계획으로",
    desc: "자동 생성된 일정을 편집해 나만의 여행 계획으로 완성하세요. 날짜, 장소, 활동을 자유롭게 수정할 수 있습니다.",
  },
];

export default function AboutPage() {
  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <SiteHeader />
      <main className="flex-1">
        {/* Hero */}
        <section className="py-20 md:py-28 text-center border-b">
          <div className="container mx-auto px-4 md:px-6 max-w-3xl space-y-6">
            <Link
              href="/"
              className="inline-flex items-center gap-2 font-bold text-2xl tracking-tighter mb-4"
            >
              <Image
                src="/icon.png"
                alt="Mojoday"
                width={36}
                height={36}
                className="rounded-lg"
              />
              <span>Mojoday</span>
            </Link>
            <h1 className="text-4xl md:text-5xl font-bold tracking-tight leading-tight">
              여행을 더 쉽게,
              <br />더 즐겁게
            </h1>
            <p className="text-lg text-muted-foreground leading-relaxed">
              Mojoday는 여행 유튜브 영상을 AI로 분석해
              <br />
              나만의 완벽한 여행 계획을 자동으로 만들어주는 서비스입니다.
            </p>
          </div>
        </section>

        {/* 미션 */}
        <section className="py-16 md:py-24">
          <div className="container mx-auto px-4 md:px-6 max-w-4xl">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div className="space-y-4">
                <span className="text-sm font-medium text-primary uppercase tracking-wider">
                  Our Mission
                </span>
                <h2 className="text-3xl font-bold leading-tight">
                  유튜버의 경험을
                  <br />내 여행으로
                </h2>
                <p className="text-muted-foreground leading-relaxed">
                  수많은 여행 유튜버들이 직접 발로 뛰며 쌓은 노하우와 경험이
                  영상 속에 담겨 있습니다. Mojoday는 그 소중한 정보를 AI 기술로
                  추출해 누구나 쉽게 활용할 수 있는 여행 계획으로 변환합니다.
                </p>
                <p className="text-muted-foreground leading-relaxed">
                  더 이상 여행 계획에 며칠씩 시간을 쏟지 않아도 됩니다. 원하는
                  영상 URL 하나로 일정, 맛집, 숙소, 교통, 예산까지 한 번에
                  완성하세요.
                </p>
              </div>
              <div className="bg-muted rounded-2xl p-8 text-center space-y-6">
                <div className="text-5xl font-bold text-primary">1분</div>
                <p className="text-muted-foreground">
                  유튜브 URL 입력 후<br />
                  여행 계획 완성까지
                </p>
                <div className="h-px bg-border" />
                <div className="grid grid-cols-2 gap-4 text-center">
                  <div>
                    <div className="text-2xl font-bold">33+</div>
                    <div className="text-xs text-muted-foreground mt-1">
                      분석 가능 항목
                    </div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold">100%</div>
                    <div className="text-xs text-muted-foreground mt-1">
                      편집 가능
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* 핵심 가치 */}
        <section className="py-16 bg-muted/30 border-y">
          <div className="container mx-auto px-4 md:px-6 max-w-5xl">
            <h2 className="text-2xl font-bold text-center mb-12">
              Mojoday가 하는 일
            </h2>
            <div className="grid md:grid-cols-3 gap-6">
              {values.map(({ emoji, title, desc }) => (
                <div
                  key={title}
                  className="bg-background rounded-2xl p-6 space-y-3 border"
                >
                  <span className="text-3xl">{emoji}</span>
                  <h3 className="font-bold text-lg">{title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {desc}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="py-16 text-center">
          <div className="container mx-auto px-4 md:px-6 space-y-6">
            <h2 className="text-2xl font-bold">지금 바로 시작해보세요</h2>
            <p className="text-muted-foreground">
              좋아하는 여행 유튜버의 영상 URL을 붙여넣어보세요.
            </p>
            <Link
              href="/"
              className="inline-flex items-center gap-2 bg-primary text-primary-foreground font-medium px-8 py-3 rounded-xl hover:bg-primary/90 transition-colors"
            >
              여행 계획 만들기 →
            </Link>
            <div className="pt-4">
              <Link
                href="/contact"
                className="text-sm text-muted-foreground hover:text-primary transition-colors"
              >
                궁금한 점이 있으신가요? 문의하기 →
              </Link>
            </div>
          </div>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}

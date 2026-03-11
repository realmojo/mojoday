import type { Metadata } from "next";
import {
  Link2,
  MapPin,
  Sparkles,
  CalendarDays,
  UtensilsCrossed,
  Wallet,
} from "lucide-react";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { TravelPlanForm } from "@/components/travel-plan-form";
import { createServerClient } from "@/lib/supabase";
import { PlanCard, type PlanCardData } from "@/components/plan-card";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "AI 여행 플래너 - 유튜브로 완성하는 나만의 여행",
  description:
    "좋아하는 여행 유튜버의 영상 URL 하나로 일정, 맛집, 숙소, 교통까지 완벽한 여행 계획을 자동으로 만들어드립니다.",
  openGraph: {
    title: "AI 여행 플래너 - 유튜브로 완성하는 나만의 여행",
    description:
      "여행 유튜브를 분석해서 나만의 여행 계획을 만들어주는 AI 서비스",
    url: "/",
  },
  alternates: { canonical: "/" },
};

const steps = [
  {
    number: "01",
    icon: <Link2 className="h-6 w-6" />,
    title: "YouTube URL 입력",
    description: "좋아하는 여행 유튜버의 영상 URL을 붙여넣어주세요. 어떤 채널이든 OK!",
  },
  {
    number: "02",
    icon: <Sparkles className="h-6 w-6" />,
    title: "AI 자동 분석",
    description: "AI가 영상 속 장소, 맛집, 교통, 팁을 자동으로 추출하고 정리합니다.",
  },
  {
    number: "03",
    icon: <CalendarDays className="h-6 w-6" />,
    title: "여행 계획 완성",
    description: "편집 가능한 일정표, 지도, 예산 계산까지 한 번에 완성됩니다.",
  },
];

const features = [
  {
    icon: <CalendarDays className="h-5 w-5 text-primary" />,
    title: "자동 일정 생성",
    description: "영상 내용을 분석해 날짜별 여행 일정을 자동으로 구성해줍니다.",
  },
  {
    icon: <UtensilsCrossed className="h-5 w-5 text-primary" />,
    title: "맛집 & 카페 추출",
    description: "영상에서 언급된 맛집과 카페를 지도와 함께 정리해드립니다.",
  },
  {
    icon: <MapPin className="h-5 w-5 text-primary" />,
    title: "명소 & 교통 정보",
    description: "주요 관광지와 이동 경로, 교통 수단 정보를 한눈에 확인하세요.",
  },
  {
    icon: <Wallet className="h-5 w-5 text-primary" />,
    title: "예산 자동 계산",
    description: "숙소, 식비, 교통비를 포함한 여행 예산을 자동으로 추산해드립니다.",
  },
];

async function getPlans(): Promise<PlanCardData[]> {
  try {
    const db = createServerClient();
    const { data } = await db
      .from("plans")
      .select("video_id, title, thumbnail_url, channel_name, summary, country, regions, tags, trip_type, travel_schedule")
      .order("created_at", { ascending: false });
    return (data as PlanCardData[]) ?? [];
  } catch {
    return [];
  }
}

function getCountries(plans: PlanCardData[]) {
  const countryMap = new Map<string, number>();
  for (const p of plans) {
    if (p.country) countryMap.set(p.country, (countryMap.get(p.country) ?? 0) + 1);
  }
  return [...countryMap.entries()].map(([name, count]) => ({ name, count }));
}

export default async function Home() {
  const plans = await getPlans();
  const countries = getCountries(plans);

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <SiteHeader />

      <main className="flex-1">
        {/* 국가별 여행 */}
        {countries.length > 0 && (
          <section id="destinations" className="py-16">
            <div className="container mx-auto px-4 md:px-6">
              <h2 className="text-xl font-bold mb-5">국가별 여행</h2>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
                {countries.map(({ name, count }) => (
                  <a
                    key={name}
                    href={`/country/${encodeURIComponent(name)}`}
                    className="flex flex-col items-center justify-center gap-1 p-4 rounded-2xl border bg-background hover:border-primary hover:shadow-md transition-all text-center"
                  >
                    <MapPin className="h-5 w-5 text-primary" />
                    <span className="font-semibold text-sm">{name}</span>
                    <span className="text-xs text-muted-foreground">{count}개 일정</span>
                  </a>
                ))}
              </div>
            </div>
          </section>
        )}

        {/* 실제 여행 계획 */}
        {plans.length > 0 && (
          <section id="plans" className="py-20 bg-muted/30">
            <div className="container mx-auto px-4 md:px-6">
              <div className="text-center mb-12 space-y-3">
                <h2 className="text-3xl md:text-4xl font-bold tracking-tight">
                  AI가 만든 여행 계획
                </h2>
                <p className="text-muted-foreground text-lg max-w-xl mx-auto">
                  실제 유튜브 영상을 분석해 완성된 여행 계획을 바로 확인해보세요.
                </p>
              </div>

              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {plans.map((plan) => (
                  <PlanCard key={plan.video_id} plan={plan} />
                ))}
              </div>
            </div>
          </section>
        )}

        {/* How It Works */}
        <section id="how-it-works" className="py-20">
          <div className="container mx-auto px-4 md:px-6">
            <div className="text-center mb-12 space-y-3">
              <h2 className="text-3xl md:text-4xl font-bold tracking-tight">
                어떻게 사용하나요?
              </h2>
              <p className="text-muted-foreground text-lg">
                단 3단계로 나만의 여행 계획이 완성됩니다.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8 relative">
              <div className="hidden md:block absolute top-10 left-1/3 right-1/3 h-0.5 bg-border" />
              {steps.map((step) => (
                <div key={step.number} className="flex flex-col items-center text-center space-y-4">
                  <div className="relative">
                    <div className="h-20 w-20 rounded-2xl bg-primary/10 flex items-center justify-center text-primary">
                      {step.icon}
                    </div>
                    <span className="absolute -top-2 -right-2 bg-primary text-primary-foreground text-xs font-bold rounded-full h-6 w-6 flex items-center justify-center">
                      {step.number.replace("0", "")}
                    </span>
                  </div>
                  <h3 className="font-bold text-xl">{step.title}</h3>
                  <p className="text-muted-foreground leading-relaxed">{step.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Features */}
        <section id="features" className="py-20 bg-muted/30">
          <div className="container mx-auto px-4 md:px-6">
            <div className="text-center mb-12 space-y-3">
              <h2 className="text-3xl md:text-4xl font-bold tracking-tight">
                여행 계획의 모든 것
              </h2>
              <p className="text-muted-foreground text-lg">
                영상 하나로 완성되는 완벽한 여행 준비
              </p>
            </div>

            <div className="grid sm:grid-cols-2 gap-6 max-w-3xl mx-auto">
              {features.map((feature) => (
                <div
                  key={feature.title}
                  className="flex gap-4 p-6 rounded-2xl bg-background border hover:shadow-md transition-shadow"
                >
                  <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center shrink-0">
                    {feature.icon}
                  </div>
                  <div>
                    <h3 className="font-semibold mb-1">{feature.title}</h3>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {feature.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="py-20">
          <div className="container mx-auto px-4 md:px-6">
            <div className="max-w-2xl mx-auto text-center space-y-6 p-10 rounded-3xl bg-gradient-to-br from-primary/10 to-primary/5 border">
              <h2 className="text-3xl md:text-4xl font-bold">
                지금 바로 시작하세요
              </h2>
              <p className="text-muted-foreground text-lg">
                좋아하는 여행 영상 URL만 있으면 됩니다.
                <br />
                무료로 첫 번째 여행 계획을 만들어보세요.
              </p>
              <TravelPlanForm />
            </div>
          </div>
        </section>
      </main>

      <SiteFooter />
    </div>
  );
}

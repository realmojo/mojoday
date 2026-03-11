import type { Metadata } from "next";
import Image from "next/image";

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

const heroFeatures = [
  { emoji: "🎬", text: "유튜브 영상 URL 하나로 여행 계획 자동 완성" },
  { emoji: "🗺️", text: "장소·맛집·숙소·교통 자동 추출 및 정리" },
  { emoji: "📅", text: "날짜별 상세 일정표 자동 생성" },
  { emoji: "💰", text: "여행 예산 자동 계산" },
  { emoji: "✏️", text: "편집 가능한 나만의 여행 플래너" },
];

const avatarColors = ["#f97316", "#06b6d4", "#8b5cf6", "#ec4899", "#10b981"];
const avatarLetters = ["K", "J", "M", "S", "P"];

async function getPlans(): Promise<PlanCardData[]> {
  try {
    const db = createServerClient();
    const { data } = await db
      .from("plans")
      .select(
        "video_id, title, thumbnail_url, channel_name, summary, country, regions, tags, trip_type, travel_schedule",
      )
      .order("created_at", { ascending: false });
    return (data as PlanCardData[]) ?? [];
  } catch {
    return [];
  }
}

function getCountries(plans: PlanCardData[]) {
  const countryMap = new Map<string, number>();
  for (const p of plans) {
    if (p.country)
      countryMap.set(p.country, (countryMap.get(p.country) ?? 0) + 1);
  }
  return [...countryMap.entries()].map(([name, count]) => ({ name, count }));
}

export default async function Home() {
  const plans = await getPlans();
  const countries = getCountries(plans);

  // 데모 썸네일: 태국 우돈타니 영상
  const demoThumb = `https://img.youtube.com/vi/cBJ9oLoPcyE/hqdefault.jpg`;

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <SiteHeader />

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative min-h-[calc(100vh-4rem)] flex items-center py-16 overflow-hidden">
          {/* Image background */}
          <Image
            src="/hero-bg.png"
            alt="Travel background"
            fill
            priority
            className="object-cover"
          />
          {/* Dark overlay for readability */}
          <div className="absolute inset-0 bg-black/60" />

          {/* Atmospheric blurs */}
          <div className="absolute top-1/3 left-1/5 w-96 h-96 bg-emerald-900/30 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute bottom-1/4 right-1/5 w-96 h-96 bg-sky-900/30 rounded-full blur-3xl pointer-events-none" />

          <div className="relative container mx-auto px-4 md:px-6">
            <div className="flex flex-col items-center text-center max-w-2xl mx-auto">
              {/* Badge */}
              <div className="inline-flex items-center gap-2 border border-white/20 rounded-full px-4 py-1.5 text-sm text-white/80 bg-white/5 backdrop-blur-sm">
                <span className="text-yellow-400 tracking-widest">★★★★★</span>
                <span>AI 여행 플래너 · Mojoday</span>
              </div>

              {/* Heading */}
              <div className="space-y-4 mt-8">
                <h1 className="text-5xl md:text-6xl font-bold leading-tight tracking-tight text-white">
                  ✈️ 여행 계획
                  <br />
                  <span className="text-emerald-400">AI가</span> 해드립니다
                </h1>
                <p className="text-xl text-white/70 leading-relaxed">
                  좋아하는 여행 유튜버의 영상 URL 하나로
                  <br />
                  일정, 맛집, 숙소, 교통까지 완벽하게
                </p>
              </div>

              {/* Avatars + count */}
              <div className="flex items-center gap-3 mt-8">
                <div className="flex -space-x-2">
                  {avatarLetters.map((letter, i) => (
                    <div
                      key={i}
                      className="w-9 h-9 rounded-full border-2 border-slate-800 flex items-center justify-center text-xs font-bold text-white"
                      style={{ backgroundColor: avatarColors[i] }}
                    >
                      {letter}
                    </div>
                  ))}
                </div>
                <span className="text-sm text-white/60">
                  1,200+ 여행자가 사용 중
                </span>
              </div>

              {/* Feature List */}
              <ul className="flex flex-wrap justify-center gap-x-6 gap-y-3 mt-8">
                {heroFeatures.map(({ emoji, text }, i) => (
                  <li
                    key={i}
                    className="flex items-center gap-1.5 text-white/85"
                  >
                    <span className="text-xl leading-none">{emoji}</span>
                    <span className="text-sm">{text}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        {/* 여행 계획 그리드 */}
        {plans.length > 0 && (
          <section id="plans" className="py-12">
            <div className="container mx-auto px-4 md:px-6">
              {/* 상단 필터 바 */}
              <div className="flex items-center gap-2 mb-6 flex-wrap">
                <span className="bg-muted text-muted-foreground text-xs font-medium px-3 py-1.5 rounded-lg">
                  Popular
                </span>
                <a
                  href="#plans"
                  className="text-sm font-semibold border-b-2 border-foreground pb-0.5 mr-2"
                >
                  전체
                </a>
                {countries.map(({ name }) => (
                  <a
                    key={name}
                    href={`/country/${encodeURIComponent(name)}`}
                    className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {name}
                  </a>
                ))}
              </div>

              {/* 카드 그리드 */}
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                {plans.map((plan, i) => (
                  <PlanCard key={plan.video_id} plan={plan} rank={i + 1} />
                ))}
              </div>
            </div>
          </section>
        )}
      </main>

      <SiteFooter />
    </div>
  );
}

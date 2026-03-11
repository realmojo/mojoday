export const dynamic = "force-dynamic";

import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, MapPin } from "lucide-react";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { createServerClient } from "@/lib/supabase";
import { PlanCard, type PlanCardData } from "@/components/plan-card";

type Props = { params: Promise<{ region: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { region } = await params;
  const name = decodeURIComponent(region);
  return {
    title: `${name} 여행 계획 - mojoday`,
    description: `${name} 지역 여행 유튜브 영상을 분석한 AI 여행 계획 모음`,
  };
}

async function getPlansByRegion(region: string): Promise<PlanCardData[]> {
  try {
    const db = createServerClient();
    const { data } = await db
      .from("plans")
      .select("video_id, title, thumbnail_url, channel_name, summary, country, regions, tags, trip_type, travel_schedule")
      .contains("regions", [region])
      .order("created_at", { ascending: false });
    return (data as PlanCardData[]) ?? [];
  } catch {
    return [];
  }
}

export default async function RegionPage({ params }: Props) {
  const { region } = await params;
  const name = decodeURIComponent(region);
  const plans = await getPlansByRegion(name);

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <SiteHeader />

      <main className="flex-1">
        <section className="py-12 md:py-16">
          <div className="container mx-auto px-4 md:px-6">
            {/* 헤더 */}
            <div className="mb-10 space-y-4">
              <Link
                href="/"
                className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                <ArrowLeft className="h-4 w-4" />
                전체 여행
              </Link>

              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-xl bg-primary/10 flex items-center justify-center">
                  <MapPin className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <h1 className="text-3xl font-bold">{name}</h1>
                  <p className="text-muted-foreground text-sm">
                    {plans.length}개의 여행 계획
                  </p>
                </div>
              </div>
            </div>

            {/* 플랜 목록 */}
            {plans.length > 0 ? (
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {plans.map((plan) => (
                  <PlanCard key={plan.video_id} plan={plan} />
                ))}
              </div>
            ) : (
              <div className="text-center py-20 text-muted-foreground">
                <MapPin className="h-10 w-10 mx-auto mb-4 opacity-30" />
                <p className="text-lg">아직 {name} 지역 여행 계획이 없습니다.</p>
                <Link href="/" className="mt-4 inline-block text-primary hover:underline text-sm">
                  영상 URL로 첫 번째 계획 만들기 →
                </Link>
              </div>
            )}
          </div>
        </section>
      </main>

      <SiteFooter />
    </div>
  );
}

"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { SiteHeader } from "@/components/site-header";
import {
  TravelPlanDetail,
  type TravelPlanData,
} from "@/components/travel-plan-detail";
import { TravelPlanEditor } from "@/components/travel-plan-editor";
import { Loader2, Eye, Pencil } from "lucide-react";
import { Button } from "@/components/ui/button";
import { supabase } from "@/lib/supabase";

export default function PlanPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [plan, setPlan] = useState<TravelPlanData | null>(null);
  const [ready, setReady] = useState(false);
  const [tab, setTab] = useState<"view" | "edit">("view");

  useEffect(() => {
    async function loadPlan() {
      const { data } = await supabase
        .from("plans")
        .select("video_id, title, thumbnail_url, channel_name, summary, country, regions, trip_type, tags, travel_schedule, travel_tips, meta")
        .eq("video_id", id)
        .single();

      if (data) {
        const meta = data.meta ?? {};
        setPlan({
          video_info: {
            id: data.video_id,
            title: data.title,
            thumbnail_url: data.thumbnail_url,
            channel_name: data.channel_name,
            summary: data.summary,
            country: data.country,
            regions: data.regions,
            type: data.trip_type,
            tags: data.tags,
            trip_duration: meta.trip_duration ?? null,
            best_season: meta.best_season ?? null,
            budget_level: meta.budget_level ?? null,
            difficulty_level: meta.difficulty_level ?? null,
            travel_style: meta.travel_style ?? null,
            visa_info: meta.visa_info ?? null,
            currency: meta.currency ?? null,
            language: meta.language ?? null,
          },
          travel_schedule: data.travel_schedule,
          travel_tips: data.travel_tips,
        });
      }

      setReady(true);
    }

    loadPlan();
  }, [id]);

  const handleSave = async (updated: TravelPlanData) => {
    setPlan(updated);
    await fetch(`/api/plans/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updated),
    });
  };

  if (!ready) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!plan) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 text-center">
        <p className="text-muted-foreground">여행 계획 데이터가 없습니다.</p>
        <Button onClick={() => router.push("/")}>홈으로 돌아가기</Button>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <SiteHeader />

      {/* 탭 바 */}
      <div className="sticky top-16 z-40 bg-background/80 backdrop-blur border-b">
        <div className="container mx-auto px-4 md:px-6 max-w-4xl flex items-center gap-1 py-2">
          <button
            onClick={() => setTab("view")}
            className={`flex items-center gap-1.5 px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
              tab === "view"
                ? "bg-primary text-primary-foreground"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <Eye className="h-3.5 w-3.5" />
            상세보기
          </button>
          <button
            onClick={() => setTab("edit")}
            className={`flex items-center gap-1.5 px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
              tab === "edit"
                ? "bg-primary text-primary-foreground"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <Pencil className="h-3.5 w-3.5" />
            편집하기
          </button>
        </div>
      </div>

      <main className="flex-1">
        {tab === "view" ? (
          <TravelPlanDetail plan={plan} />
        ) : (
          <div className="container mx-auto px-4 md:px-6 max-w-4xl py-8">
            <TravelPlanEditor initialPlan={plan} onSave={handleSave} />
          </div>
        )}
      </main>
    </div>
  );
}

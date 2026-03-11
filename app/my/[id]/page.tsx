"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { SiteHeader } from "@/components/site-header";
import {
  TravelPlanDetail,
  type TravelPlanData,
} from "@/components/travel-plan-detail";
import { TravelPlanEditor } from "@/components/travel-plan-editor";
import { Loader2, Eye, Pencil, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function MyPlanPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [plan, setPlan] = useState<TravelPlanData | null>(null);
  const [ready, setReady] = useState(false);
  const [tab, setTab] = useState<"view" | "edit">("view");
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    fetch(`/api/my-plans/${id}`)
      .then((r) => {
        if (r.status === 401) { router.push("/login"); return null; }
        if (r.status === 404) { router.push("/my"); return null; }
        return r.json();
      })
      .then((json) => {
        if (!json) return;
        const d = json.data;
        const meta = d.meta ?? {};
        setPlan({
          video_info: {
            id: d.id,
            title: d.title,
            thumbnail_url: d.thumbnail_url,
            channel_name: d.channel_name,
            summary: d.summary,
            country: d.country,
            regions: d.regions,
            type: d.trip_type,
            tags: d.tags,
            trip_duration: meta.trip_duration ?? null,
            best_season: meta.best_season ?? null,
            budget_level: meta.budget_level ?? null,
            difficulty_level: meta.difficulty_level ?? null,
            travel_style: meta.travel_style ?? null,
            visa_info: meta.visa_info ?? null,
            currency: meta.currency ?? null,
            language: meta.language ?? null,
          },
          travel_schedule: d.travel_schedule,
          travel_tips: d.travel_tips,
        });
        setReady(true);
      });
  }, [id, router]);

  const handleSave = async (updated: TravelPlanData) => {
    setPlan(updated);
    await fetch(`/api/my-plans/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updated),
    });
  };

  const handleDelete = async () => {
    if (!confirm("이 여행 일정을 삭제하시겠습니까?")) return;
    setDeleting(true);
    await fetch(`/api/my-plans/${id}`, { method: "DELETE" });
    router.push("/my");
  };

  if (!ready) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!plan) return null;

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

          <div className="ml-auto flex items-center gap-2">
            <span className="text-xs text-muted-foreground bg-muted px-2.5 py-1 rounded-full">
              내 일정
            </span>
            <button
              onClick={handleDelete}
              disabled={deleting}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium transition-colors text-destructive hover:bg-destructive/10 disabled:opacity-60"
            >
              {deleting ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Trash2 className="h-3.5 w-3.5" />}
              삭제
            </button>
          </div>
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

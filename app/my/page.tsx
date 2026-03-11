"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { SiteHeader } from "@/components/site-header";
import { PlanCard, type PlanCardData } from "@/components/plan-card";
import { Loader2, BookmarkCheck } from "lucide-react";
import { Button } from "@/components/ui/button";

type MyPlan = PlanCardData & { id: string };

export default function MyPage() {
  const router = useRouter();
  const [plans, setPlans] = useState<MyPlan[]>([]);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    fetch("/api/my-plans")
      .then((r) => {
        if (r.status === 401) {
          router.push("/login");
          return null;
        }
        return r.json();
      })
      .then((json) => {
        if (!json) return;
        setPlans(json.data ?? []);
        setReady(true);
      });
  }, [router]);

  if (!ready) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <SiteHeader />

      <main className="flex-1 container mx-auto px-4 md:px-6 py-10 max-w-6xl">
        <div className="flex items-center gap-3 mb-8">
          <BookmarkCheck className="h-6 w-6 text-primary" />
          <h1 className="text-2xl font-bold">내 여행 일정</h1>
          <span className="text-muted-foreground text-sm">({plans.length}개)</span>
        </div>

        {plans.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-24 gap-4 text-center">
            <BookmarkCheck className="h-12 w-12 text-muted-foreground/40" />
            <p className="text-muted-foreground">아직 가져온 여행 일정이 없습니다.</p>
            <Button onClick={() => router.push("/")}>여행지 둘러보기</Button>
          </div>
        ) : (
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {plans.map((plan) => (
              <PlanCard
                key={plan.id}
                plan={plan}
                href={`/my/${plan.id}`}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

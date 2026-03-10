"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { YoutubeIcon, ArrowRight, Loader2 } from "lucide-react";

export function TravelPlanForm() {
  const router = useRouter();
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!url.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const res = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "오류가 발생했습니다.");
        return;
      }

      sessionStorage.setItem(`travelPlan:${data.videoId}`, JSON.stringify(data.plan));
      router.push(`/plan/${data.videoId}`);
    } catch {
      setError("네트워크 오류가 발생했습니다. 다시 시도해주세요.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="w-full space-y-3">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-2xl mx-auto flex flex-col sm:flex-row gap-3"
      >
        <div className="relative flex-1">
          <YoutubeIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
          <Input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://www.youtube.com/watch?v=..."
            className="pl-10 h-12 text-base"
            disabled={loading}
          />
        </div>
        <Button
          type="submit"
          size="lg"
          className="h-12 px-6 text-base shrink-0"
          disabled={loading || !url.trim()}
        >
          {loading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              분석 중...
            </>
          ) : (
            <>
              여행 계획 만들기 <ArrowRight className="ml-2 h-4 w-4" />
            </>
          )}
        </Button>
      </form>

      {error && (
        <p className="text-sm text-destructive text-center">{error}</p>
      )}

      {loading && (
        <p className="text-sm text-muted-foreground text-center">
          AI가 영상을 분석 중입니다. 영상 길이에 따라 30초~2분 소요됩니다.
        </p>
      )}
    </div>
  );
}

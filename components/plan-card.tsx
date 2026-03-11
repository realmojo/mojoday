import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { CalendarDays, MapPin, Play, ArrowRight } from "lucide-react";

export type PlanCardData = {
  video_id: string;
  title: string;
  thumbnail_url: string;
  channel_name: string;
  summary: string;
  country: string | null;
  regions: string[] | null;
  tags: string[] | null;
  trip_type: string | null;
  travel_schedule: { day: number }[];
};

export function PlanCard({ plan }: { plan: PlanCardData }) {
  const dayCount = plan.travel_schedule?.length ?? 0;
  const displayTags = (plan.tags ?? []).slice(0, 4);
  const displayRegions = (plan.regions ?? []).slice(0, 3);

  return (
    // position:relative + 절대 inset Link 패턴 → 카드 전체 클릭 + 내부 Link 중첩 허용
    <div className="group relative rounded-2xl border bg-background overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
      {/* 카드 전체 클릭 영역 */}
      <Link
        href={`/plan/${plan.video_id}`}
        className="absolute inset-0 z-0"
        aria-label={plan.title}
      />

      {/* Thumbnail */}
      <div className="relative aspect-video overflow-hidden bg-muted">
        <img
          src={plan.thumbnail_url}
          alt={plan.title}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />

        {/* 채널명 */}
        <div className="absolute top-3 left-3 z-10">
          <span className="bg-black/60 text-white text-xs px-2.5 py-1 rounded-full backdrop-blur-sm flex items-center gap-1.5">
            <Play className="h-3 w-3 fill-white" />
            {plan.channel_name}
          </span>
        </div>

        {/* 나라 - 클릭 가능 */}
        {plan.country && (
          <div className="absolute top-3 right-3 z-10">
            <Link
              href={`/country/${encodeURIComponent(plan.country)}`}
              className="bg-primary text-primary-foreground text-xs px-2.5 py-1 rounded-full font-medium hover:bg-primary/80 transition-colors"
            >
              {plan.country}
            </Link>
          </div>
        )}

        {/* 일정 수 */}
        {dayCount > 0 && (
          <div className="absolute bottom-3 right-3 z-10">
            <span className="bg-background/90 text-foreground text-xs px-2.5 py-1 rounded-full font-medium backdrop-blur-sm flex items-center gap-1">
              <CalendarDays className="h-3 w-3" />
              {dayCount}일 일정
            </span>
          </div>
        )}
      </div>

      {/* 내용 */}
      <div className="p-4 space-y-3">
        <h3 className="font-bold text-base leading-snug line-clamp-2 group-hover:text-primary transition-colors">
          {plan.title}
        </h3>

        {/* 지역 - 클릭 가능 */}
        {displayRegions.length > 0 && (
          <div className="relative z-10 flex items-center gap-1.5 flex-wrap">
            <MapPin className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
            {displayRegions.map((region) => (
              <Link
                key={region}
                href={`/region/${encodeURIComponent(region)}`}
                className="text-sm text-muted-foreground hover:text-primary hover:underline transition-colors"
              >
                {region}
              </Link>
            ))}
          </div>
        )}

        {/* 태그 */}
        {displayTags.length > 0 && (
          <div className="relative z-10 flex flex-wrap gap-1.5">
            {displayTags.map((tag) => (
              <Badge key={tag} variant="secondary" className="text-xs">
                #{tag}
              </Badge>
            ))}
          </div>
        )}

        <div className="flex items-center justify-between pt-1">
          <p className="text-xs text-muted-foreground line-clamp-1 flex-1 mr-2">
            {plan.summary}
          </p>
          <ArrowRight className="h-4 w-4 text-muted-foreground group-hover:text-primary group-hover:translate-x-1 transition-all shrink-0" />
        </div>
      </div>
    </div>
  );
}

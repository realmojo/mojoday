import Link from "next/link";
import { CalendarDays, Play } from "lucide-react";

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

export function PlanCard({
  plan,
  rank,
  href,
}: {
  plan: PlanCardData;
  rank?: number;
  href?: string;
}) {
  const dayCount = plan.travel_schedule?.length ?? 0;
  const mainCity = plan.regions?.[0] ?? plan.country ?? "";
  const subCity = plan.regions?.[1] ?? null;

  return (
    <Link
      href={href ?? `/plan/${plan.video_id}`}
      className="group relative rounded-2xl overflow-hidden aspect-video cursor-pointer hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 bg-muted block"
      aria-label={plan.title}
    >

      {/* 배경 이미지 */}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={plan.thumbnail_url}
        alt={plan.title}
        className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
      />

      {/* 그라디언트 오버레이 */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/20 to-black/15" />

      {/* 상단 좌: 순위 */}
      {rank !== undefined && (
        <div className="absolute top-4 left-4 z-10">
          <span className="text-white font-bold text-lg leading-none">{rank}</span>
          <div className="w-5 h-0.5 bg-white mt-1" />
        </div>
      )}

      {/* 상단 우: 일정 수 */}
      {dayCount > 0 && (
        <div className="absolute top-4 right-4 z-10 flex items-center gap-1 text-white/90">
          <CalendarDays className="h-4 w-4" />
          <span className="text-sm font-medium">{dayCount}일</span>
        </div>
      )}

      {/* 하단: 목적지 정보 */}
      <div className="absolute bottom-0 left-0 right-0 p-4 z-10">
        {/* 도시명 */}
        <h3 className="text-white text-lg font-bold leading-tight drop-shadow-md">
          {mainCity}
          {subCity && (
            <span className="text-white/70 text-base">, {subCity}</span>
          )}
        </h3>
        {/* 국가명 */}
        {plan.country && (
          <p className="text-white/70 text-sm mt-0.5">{plan.country}</p>
        )}

        {/* 하단 정보 행 */}
        <div className="flex items-center justify-between mt-3">
          {/* 채널명 */}
          <span className="flex items-center gap-1.5 text-white/60 text-xs">
            <Play className="h-3 w-3 fill-white/60" />
            {plan.channel_name}
          </span>

          {/* 여행 유형 */}
          {plan.trip_type && (
            <span className="bg-white/15 text-white text-xs px-2.5 py-1 rounded-full backdrop-blur-sm">
              {plan.trip_type}
            </span>
          )}
        </div>
      </div>
    </Link>
  );
}

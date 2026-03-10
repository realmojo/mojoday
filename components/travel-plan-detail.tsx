"use client";

import { useState } from "react";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import {
  ArrowLeft,
  Clock,
  MapPin,
  Bus,
  Utensils,
  BedDouble,
  Wallet,
  AlertTriangle,
  Backpack,
  Info,
  Play,
  ChevronDown,
  Loader2,
} from "lucide-react";

export type Activity = {
  time_range: string | null;
  location: string;
  description: string;
  transportation: string | null;
  accommodation: string | null;
  food: string | null;
  price_info: Record<string, string> | null;
  coordinates: { latitude: number; longitude: number } | null;
};

export type DaySchedule = {
  day: number;
  category: string;
  activities: Activity[];
};

export type TravelPlanData = {
  video_info: {
    id: string;
    title: string;
    thumbnail_url: string;
    channel_name: string;
    summary: string;
    country?: string | null;
    regions?: string[] | null;
    type?: string | null;
    tags?: string[] | null;
  };
  travel_schedule: DaySchedule[];
  travel_tips: {
    precautions: string;
    items: string;
    total_expense: string;
    useful_info: string;
  };
};

export function TravelPlanDetail({ plan }: { plan: TravelPlanData }) {
  const { video_info, travel_schedule, travel_tips } = plan;
  const [openMaps, setOpenMaps] = useState<Set<string>>(new Set());
  const [loadedMaps, setLoadedMaps] = useState<Set<string>>(new Set());

  function toggleMap(key: string) {
    setOpenMaps((prev) => {
      const next = new Set(prev);
      next.has(key) ? next.delete(key) : next.add(key);
      return next;
    });
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Back button */}
      <div className="sticky top-16 z-40 bg-background/80 backdrop-blur border-b">
        <div className="container mx-auto px-4 md:px-6 py-3">
          <Link
            href="/"
            className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            <ArrowLeft className="h-4 w-4" />
            돌아가기
          </Link>
        </div>
      </div>

      <div className="container mx-auto px-4 md:px-6 py-8 max-w-4xl space-y-10">

        {/* Video Info Hero */}
        <section>
          <div className="relative rounded-2xl overflow-hidden">
            {/* Thumbnail */}
            <div className="relative w-full aspect-video bg-muted">
              <img
                src={video_info.thumbnail_url}
                alt={video_info.title}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />

              {/* YouTube play link */}
              <a
                href={`https://www.youtube.com/watch?v=${video_info.id}`}
                target="_blank"
                rel="noopener noreferrer"
                className="absolute inset-0 flex items-center justify-center group"
              >
                <div className="h-16 w-16 rounded-full bg-red-600 flex items-center justify-center shadow-xl group-hover:scale-110 transition-transform">
                  <Play className="h-7 w-7 text-white fill-white ml-1" />
                </div>
              </a>

              {/* Channel + Title overlay */}
              <div className="absolute bottom-0 left-0 right-0 p-6 text-white">
                <Badge
                  variant="secondary"
                  className="mb-2 bg-white/20 text-white border-none backdrop-blur-sm"
                >
                  {video_info.channel_name}
                </Badge>
                <h1 className="text-xl md:text-2xl font-bold leading-tight">
                  {video_info.title}
                </h1>
              </div>
            </div>
          </div>

          {/* Summary */}
          <div className="mt-4 p-4 rounded-xl bg-muted/50 border">
            <p className="text-sm text-muted-foreground leading-relaxed">
              {video_info.summary}
            </p>
          </div>
        </section>

        {/* Travel Schedule */}
        {travel_schedule.length > 0 && (
          <section>
            <h2 className="text-xl font-bold mb-5 flex items-center gap-2">
              <Clock className="h-5 w-5 text-primary" />
              여행 일정
            </h2>

            <div className="space-y-6">
              {travel_schedule.map((day) => (
                <div key={day.day}>
                  {/* Day Header */}
                  <div className="flex items-center gap-3 mb-4">
                    <div className="h-9 w-9 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold text-sm shrink-0">
                      {day.day}
                    </div>
                    <h3 className="font-semibold text-base">{day.category}</h3>
                  </div>

                  {/* Activities */}
                  <div className="ml-4 border-l-2 border-border pl-6 space-y-5">
                    {day.activities.map((activity, idx) => (
                      <div key={idx} className="relative">
                        {/* Dot on timeline */}
                        <div className="absolute -left-[29px] top-1.5 h-3 w-3 rounded-full bg-primary/40 border-2 border-primary" />

                        <Card className="border shadow-sm">
                          <CardContent className="p-4 space-y-3">
                            {/* Location + time */}
                            <div className="flex flex-wrap items-start justify-between gap-2">
                              <div className="flex items-center gap-1.5 font-semibold">
                                <MapPin className="h-4 w-4 text-primary shrink-0" />
                                {activity.location}
                              </div>
                              {activity.time_range && (
                                <Badge
                                  variant="outline"
                                  className="text-xs font-mono shrink-0"
                                >
                                  {activity.time_range}
                                </Badge>
                              )}
                            </div>

                            {/* Description */}
                            <p className="text-sm text-muted-foreground leading-relaxed">
                              {activity.description}
                            </p>

                            {/* Meta info grid */}
                            <div className="grid sm:grid-cols-2 gap-2 text-sm">
                              {activity.transportation && (
                                <div className="flex items-start gap-2 p-2 rounded-lg bg-muted/50">
                                  <Bus className="h-4 w-4 text-muted-foreground mt-0.5 shrink-0" />
                                  <span className="text-muted-foreground">{activity.transportation}</span>
                                </div>
                              )}
                              {activity.accommodation && (
                                <div className="flex items-start gap-2 p-2 rounded-lg bg-muted/50">
                                  <BedDouble className="h-4 w-4 text-muted-foreground mt-0.5 shrink-0" />
                                  <span className="text-muted-foreground">{activity.accommodation}</span>
                                </div>
                              )}
                              {activity.food && (
                                <div className="flex items-start gap-2 p-2 rounded-lg bg-muted/50 sm:col-span-2">
                                  <Utensils className="h-4 w-4 text-muted-foreground mt-0.5 shrink-0" />
                                  <span className="text-muted-foreground">{activity.food}</span>
                                </div>
                              )}
                            </div>

                            {/* Price info table */}
                            {activity.price_info && Object.keys(activity.price_info).length > 0 && (
                              <div className="border rounded-lg overflow-hidden">
                                <div className="flex items-center gap-1.5 px-3 py-2 bg-muted/50 border-b">
                                  <Wallet className="h-3.5 w-3.5 text-primary" />
                                  <span className="text-xs font-semibold">가격 정보</span>
                                </div>
                                <div className="divide-y">
                                  {Object.entries(activity.price_info).map(([item, price]) => (
                                    <div key={item} className="flex justify-between items-center px-3 py-2 text-sm">
                                      <span className="text-muted-foreground">{item}</span>
                                      <span className="font-medium">{price}</span>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}

                            {/* Map collapse */}
                            {activity.coordinates && (() => {
                              const mapKey = `${day.day}-${idx}`;
                              const isOpen = openMaps.has(mapKey);
                              const { latitude, longitude } = activity.coordinates;
                              return (
                                <div>
                                  <button
                                    onClick={() => toggleMap(mapKey)}
                                    className="inline-flex items-center gap-1.5 text-xs text-primary hover:underline"
                                  >
                                    <MapPin className="h-3.5 w-3.5" />
                                    지도에서 보기
                                    <ChevronDown
                                      className={`h-3.5 w-3.5 transition-transform duration-200 ${isOpen ? "rotate-180" : ""}`}
                                    />
                                  </button>
                                  {isOpen && (
                                    <div className="mt-2 rounded-xl overflow-hidden border relative">
                                      {!loadedMaps.has(mapKey) && (
                                        <div className="absolute inset-0 flex items-center justify-center bg-muted/60 z-10" style={{ height: 220 }}>
                                          <Loader2 className="h-6 w-6 animate-spin text-primary" />
                                        </div>
                                      )}
                                      <iframe
                                        title={activity.location}
                                        src={`https://maps.google.com/maps?q=${latitude},${longitude}&z=15&output=embed`}
                                        width="100%"
                                        height="220"
                                        loading="lazy"
                                        className="block"
                                        onLoad={() =>
                                          setLoadedMaps((prev) => {
                                            const next = new Set(prev);
                                            next.add(mapKey);
                                            return next;
                                          })
                                        }
                                      />
                                    </div>
                                  )}
                                </div>
                              );
                            })()}
                          </CardContent>
                        </Card>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Travel Tips */}
        <section>
          <h2 className="text-xl font-bold mb-5 flex items-center gap-2">
            <Info className="h-5 w-5 text-primary" />
            여행 팁
          </h2>

          <div className="space-y-4">
            {/* Precautions - warning style */}
            {travel_tips.precautions && (
              <div className="flex gap-3 p-4 rounded-xl bg-amber-500/10 border border-amber-500/30">
                <AlertTriangle className="h-5 w-5 text-amber-500 shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-semibold text-amber-700 dark:text-amber-400 mb-1">주의사항</p>
                  <p className="text-sm text-amber-800 dark:text-amber-300 leading-relaxed">
                    {travel_tips.precautions}
                  </p>
                </div>
              </div>
            )}

            <div className="grid sm:grid-cols-3 gap-4">
              {travel_tips.items && (
                <div className="p-4 rounded-xl bg-muted/50 border space-y-2">
                  <div className="flex items-center gap-2 font-semibold text-sm">
                    <Backpack className="h-4 w-4 text-primary" />
                    준비물
                  </div>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {travel_tips.items}
                  </p>
                </div>
              )}
              {travel_tips.total_expense && (
                <div className="p-4 rounded-xl bg-muted/50 border space-y-2">
                  <div className="flex items-center gap-2 font-semibold text-sm">
                    <Wallet className="h-4 w-4 text-primary" />
                    예상 비용
                  </div>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {travel_tips.total_expense}
                  </p>
                </div>
              )}
              {travel_tips.useful_info && (
                <div className="p-4 rounded-xl bg-muted/50 border space-y-2">
                  <div className="flex items-center gap-2 font-semibold text-sm">
                    <Info className="h-4 w-4 text-primary" />
                    유용한 정보
                  </div>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {travel_tips.useful_info}
                  </p>
                </div>
              )}
            </div>
          </div>
        </section>

      </div>
    </div>
  );
}

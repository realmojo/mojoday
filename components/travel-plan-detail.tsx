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
  Tag,
  Globe,
  Calendar,
  DollarSign,
  Zap,
  Users,
  Shield,
  Smartphone,
  Phone,
  UtensilsCrossed,
  Hotel,
} from "lucide-react";

type PriceItem = { name: string; price: string };

export type Activity = {
  time_range: string | null;
  location: string;
  description: string;
  category: string | null;
  transportation: string | null;
  accommodation: string | null;
  food: string | null;
  price_info: PriceItem[] | Record<string, string> | null;
  entry_fee: string | null;
  duration: string | null;
  opening_hours: string | null;
  reservation_required: boolean | null;
  rating: string | null;
  tip: string | null;
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
    trip_duration?: string | null;
    best_season?: string | null;
    budget_level?: string | null;
    difficulty_level?: string | null;
    travel_style?: string | null;
    visa_info?: string | null;
    currency?: string | null;
    language?: string | null;
  };
  travel_schedule: DaySchedule[];
  travel_tips: {
    highlights?: string[] | null;
    precautions: string;
    cultural_notes?: string | null;
    health_tips?: string | null;
    items: string;
    total_expense: string;
    useful_info: string;
    sim_card?: string | null;
    apps?: string[] | null;
    emergency?: {
      police?: string | null;
      ambulance?: string | null;
      korean_embassy?: string | null;
    } | null;
    transport?: {
      from_airport?: string | null;
      local?: string | null;
      intercity?: string | null;
    } | null;
    restaurants?:
      | {
          name: string;
          menu: string;
          price: string;
          opening_hours?: string | null;
          reservation_required?: boolean;
          coordinates?: { latitude: number; longitude: number } | null;
        }[]
      | null;
    accommodations?:
      | {
          name: string;
          type: string;
          price_per_night: string;
          booking_url?: string | null;
          coordinates?: { latitude: number; longitude: number } | null;
        }[]
      | null;
  };
};

function normalizePriceInfo(raw: Activity["price_info"]): PriceItem[] {
  if (!raw) return [];
  if (Array.isArray(raw)) return raw;
  return Object.entries(raw).map(([name, price]) => ({ name, price }));
}

const BUDGET_COLOR: Record<string, string> = {
  저예산: "bg-green-100 text-green-700",
  중간: "bg-blue-100 text-blue-700",
  럭셔리: "bg-purple-100 text-purple-700",
};
const DIFFICULTY_COLOR: Record<string, string> = {
  쉬움: "bg-green-100 text-green-700",
  보통: "bg-yellow-100 text-yellow-700",
  어려움: "bg-red-100 text-red-700",
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
      <div className="container mx-auto px-4 md:px-6 py-8 max-w-4xl space-y-10">
        {/* Hero */}
        <section>
          <div className="relative rounded-2xl overflow-hidden">
            <div className="relative w-full aspect-video bg-muted">
              <img
                src={video_info.thumbnail_url}
                alt={video_info.title}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />
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

          {/* 국가 / 지역 / 태그 */}
          {(video_info.country ||
            video_info.regions?.length ||
            video_info.tags?.length) && (
            <div className="mt-4 p-4 rounded-xl border space-y-3">
              <div className="flex flex-wrap gap-3 text-sm">
                {video_info.country && (
                  <div className="flex items-center gap-1.5">
                    <MapPin className="h-4 w-4 text-primary shrink-0" />
                    <Link
                      href={`/country/${encodeURIComponent(video_info.country)}`}
                      className="font-medium hover:text-primary transition-colors"
                    >
                      {video_info.country}
                    </Link>
                  </div>
                )}
                {video_info.regions?.map((r) => (
                  <div key={r} className="flex items-center gap-1.5">
                    <MapPin className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
                    <Link
                      href={`/region/${encodeURIComponent(r)}`}
                      className="text-muted-foreground hover:text-foreground transition-colors"
                    >
                      {r}
                    </Link>
                  </div>
                ))}
              </div>
              {video_info.type && (
                <p className="text-xs text-muted-foreground">
                  {video_info.type}
                </p>
              )}
              {video_info.tags && video_info.tags.length > 0 && (
                <div className="flex flex-wrap gap-1.5">
                  {video_info.tags.map((tag) => (
                    <Badge
                      key={tag}
                      variant="secondary"
                      className="text-xs gap-1"
                    >
                      <Tag className="h-3 w-3" />
                      {tag}
                    </Badge>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* 여행 메타 칩 */}
          {(video_info.trip_duration ||
            video_info.best_season ||
            video_info.budget_level ||
            video_info.difficulty_level ||
            video_info.travel_style) && (
            <div className="mt-3 flex flex-wrap gap-2">
              {video_info.trip_duration && (
                <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-muted text-sm">
                  <Clock className="h-3.5 w-3.5 text-muted-foreground" />
                  {video_info.trip_duration}
                </span>
              )}
              {video_info.best_season && (
                <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-muted text-sm">
                  <Calendar className="h-3.5 w-3.5 text-muted-foreground" />
                  {video_info.best_season}
                </span>
              )}
              {video_info.budget_level && (
                <span
                  className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium ${BUDGET_COLOR[video_info.budget_level] ?? "bg-muted"}`}
                >
                  <DollarSign className="h-3.5 w-3.5" />
                  {video_info.budget_level}
                </span>
              )}
              {video_info.difficulty_level && (
                <span
                  className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium ${DIFFICULTY_COLOR[video_info.difficulty_level] ?? "bg-muted"}`}
                >
                  <Zap className="h-3.5 w-3.5" />
                  {video_info.difficulty_level}
                </span>
              )}
              {video_info.travel_style && (
                <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-muted text-sm">
                  <Users className="h-3.5 w-3.5 text-muted-foreground" />
                  {video_info.travel_style}
                </span>
              )}
            </div>
          )}

          {/* 비자 / 통화 / 언어 */}
          {(video_info.visa_info ||
            video_info.currency ||
            video_info.language) && (
            <div className="mt-3 grid sm:grid-cols-3 gap-2">
              {video_info.visa_info && (
                <div className="flex items-start gap-2 p-3 rounded-xl bg-muted/50 border text-sm">
                  <Globe className="h-4 w-4 text-primary mt-0.5 shrink-0" />
                  <div>
                    <p className="font-medium text-xs mb-0.5">비자</p>
                    <p className="text-muted-foreground">
                      {video_info.visa_info}
                    </p>
                  </div>
                </div>
              )}
              {video_info.currency && (
                <div className="flex items-start gap-2 p-3 rounded-xl bg-muted/50 border text-sm">
                  <DollarSign className="h-4 w-4 text-primary mt-0.5 shrink-0" />
                  <div>
                    <p className="font-medium text-xs mb-0.5">통화</p>
                    <p className="text-muted-foreground">
                      {video_info.currency}
                    </p>
                  </div>
                </div>
              )}
              {video_info.language && (
                <div className="flex items-start gap-2 p-3 rounded-xl bg-muted/50 border text-sm">
                  <Globe className="h-4 w-4 text-primary mt-0.5 shrink-0" />
                  <div>
                    <p className="font-medium text-xs mb-0.5">언어</p>
                    <p className="text-muted-foreground">
                      {video_info.language}
                    </p>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Summary */}
          <div className="mt-3 p-4 rounded-xl bg-muted/50 border">
            <p className="text-sm text-muted-foreground leading-relaxed">
              {video_info.summary}
            </p>
          </div>
        </section>

        {/* Highlights */}
        {travel_tips.highlights && travel_tips.highlights.length > 0 && (
          <section>
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <Zap className="h-5 w-5 text-primary" />이 여행의 하이라이트
            </h2>
            <div className="flex flex-wrap gap-2">
              {travel_tips.highlights.map((h, i) => (
                <span
                  key={i}
                  className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full border bg-primary/5 text-sm font-medium"
                >
                  <span className="text-primary font-bold">{i + 1}</span>
                  {h}
                </span>
              ))}
            </div>
          </section>
        )}

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
                  <div className="flex items-center gap-3 mb-4">
                    <div className="h-9 w-9 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold text-sm shrink-0">
                      {day.day}
                    </div>
                    <h3 className="font-semibold text-base">{day.category}</h3>
                  </div>
                  <div className="ml-4 border-l-2 border-border pl-6 space-y-5">
                    {day.activities.map((activity, idx) => {
                      const priceItems = normalizePriceInfo(
                        activity.price_info,
                      );
                      return (
                        <div key={idx} className="relative">
                          <div className="absolute -left-[29px] top-1.5 h-3 w-3 rounded-full bg-primary/40 border-2 border-primary" />
                          <Card className="border shadow-sm">
                            <CardContent className="p-4 space-y-3">
                              <div className="flex flex-wrap items-start justify-between gap-2">
                                <div className="flex items-center gap-1.5 font-semibold">
                                  <MapPin className="h-4 w-4 text-primary shrink-0" />
                                  {activity.location}
                                </div>
                                <div className="flex items-center gap-1.5 flex-wrap">
                                  {activity.category && (
                                    <Badge
                                      variant="outline"
                                      className="text-xs"
                                    >
                                      {activity.category}
                                    </Badge>
                                  )}
                                  {activity.time_range && (
                                    <Badge
                                      variant="outline"
                                      className="text-xs font-mono shrink-0"
                                    >
                                      {activity.time_range}
                                    </Badge>
                                  )}
                                </div>
                              </div>

                              {(activity.rating ||
                                activity.duration ||
                                activity.opening_hours ||
                                activity.entry_fee) && (
                                <div className="flex flex-wrap gap-2 text-xs text-muted-foreground">
                                  {activity.rating && (
                                    <span className="text-amber-500 font-medium">
                                      {activity.rating}
                                    </span>
                                  )}
                                  {activity.duration && (
                                    <span>⏱ {activity.duration}</span>
                                  )}
                                  {activity.opening_hours && (
                                    <span>🕐 {activity.opening_hours}</span>
                                  )}
                                  {activity.entry_fee && (
                                    <span>🎫 입장료: {activity.entry_fee}</span>
                                  )}
                                  {activity.reservation_required && (
                                    <span className="text-red-500 font-medium">
                                      예약 필수
                                    </span>
                                  )}
                                </div>
                              )}

                              <p className="text-sm text-muted-foreground leading-relaxed">
                                {activity.description}
                              </p>

                              {activity.tip && (
                                <div className="flex items-start gap-2 p-2 rounded-lg bg-amber-50 border border-amber-200 text-xs text-amber-800">
                                  <Info className="h-3.5 w-3.5 mt-0.5 shrink-0" />
                                  {activity.tip}
                                </div>
                              )}

                              <div className="grid sm:grid-cols-2 gap-2 text-sm">
                                {activity.transportation && (
                                  <div className="flex items-start gap-2 p-2 rounded-lg bg-muted/50">
                                    <Bus className="h-4 w-4 text-muted-foreground mt-0.5 shrink-0" />
                                    <span className="text-muted-foreground">
                                      {activity.transportation}
                                    </span>
                                  </div>
                                )}
                                {activity.accommodation && (
                                  <div className="flex items-start gap-2 p-2 rounded-lg bg-muted/50">
                                    <BedDouble className="h-4 w-4 text-muted-foreground mt-0.5 shrink-0" />
                                    <span className="text-muted-foreground">
                                      {activity.accommodation}
                                    </span>
                                  </div>
                                )}
                                {activity.food && (
                                  <div className="flex items-start gap-2 p-2 rounded-lg bg-muted/50 sm:col-span-2">
                                    <Utensils className="h-4 w-4 text-muted-foreground mt-0.5 shrink-0" />
                                    <span className="text-muted-foreground">
                                      {activity.food}
                                    </span>
                                  </div>
                                )}
                              </div>

                              {priceItems.length > 0 && (
                                <div className="border rounded-lg overflow-hidden">
                                  <div className="flex items-center gap-1.5 px-3 py-2 bg-muted/50 border-b">
                                    <Wallet className="h-3.5 w-3.5 text-primary" />
                                    <span className="text-xs font-semibold">
                                      가격 정보
                                    </span>
                                  </div>
                                  <div className="divide-y">
                                    {priceItems.map((item) => (
                                      <div
                                        key={item.name}
                                        className="flex justify-between items-center px-3 py-2 text-sm"
                                      >
                                        <span className="text-muted-foreground">
                                          {item.name}
                                        </span>
                                        <span className="font-medium">
                                          {item.price}
                                        </span>
                                      </div>
                                    ))}
                                  </div>
                                </div>
                              )}

                              {activity.coordinates &&
                                (() => {
                                  const mapKey = `${day.day}-${idx}`;
                                  const isOpen = openMaps.has(mapKey);
                                  const { latitude, longitude } =
                                    activity.coordinates;
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
                                            <div
                                              className="absolute inset-0 flex items-center justify-center bg-muted/60 z-10"
                                              style={{ height: 220 }}
                                            >
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
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Restaurants */}
        {travel_tips.restaurants && travel_tips.restaurants.length > 0 && (
          <section>
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <UtensilsCrossed className="h-5 w-5 text-primary" />
              추천 맛집
            </h2>
            <div className="grid sm:grid-cols-2 gap-3">
              {travel_tips.restaurants.map((r, i) => {
                const mapKey = `rest-${i}`;
                const isOpen = openMaps.has(mapKey);
                return (
                  <div
                    key={i}
                    className="p-4 rounded-xl border bg-background space-y-1"
                  >
                    <p className="font-semibold text-sm">{r.name}</p>
                    <p className="text-xs text-muted-foreground">{r.menu}</p>
                    <div className="flex items-center justify-between text-xs text-muted-foreground">
                      <span>{r.price}</span>
                      {r.opening_hours && <span>🕐 {r.opening_hours}</span>}
                    </div>
                    {r.reservation_required && (
                      <p className="text-xs text-red-500 font-medium">
                        예약 필수
                      </p>
                    )}
                    {r.coordinates && (
                      <div className="pt-1">
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
                              <div
                                className="absolute inset-0 flex items-center justify-center bg-muted/60 z-10"
                                style={{ height: 200 }}
                              >
                                <Loader2 className="h-6 w-6 animate-spin text-primary" />
                              </div>
                            )}
                            <iframe
                              title={r.name}
                              src={`https://maps.google.com/maps?q=${r.coordinates.latitude},${r.coordinates.longitude}&z=15&output=embed`}
                              width="100%"
                              height="200"
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
                    )}
                  </div>
                );
              })}
            </div>
          </section>
        )}

        {/* Accommodations */}
        {travel_tips.accommodations &&
          travel_tips.accommodations.length > 0 && (
            <section>
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Hotel className="h-5 w-5 text-primary" />
                추천 숙소
              </h2>
              <div className="grid sm:grid-cols-2 gap-3">
                {travel_tips.accommodations.map((a, i) => {
                  const mapKey = `accom-${i}`;
                  const isOpen = openMaps.has(mapKey);
                  return (
                    <div
                      key={i}
                      className="p-4 rounded-xl border bg-background space-y-1"
                    >
                      <div className="flex items-center justify-between">
                        <p className="font-semibold text-sm">{a.name}</p>
                        <Badge variant="outline" className="text-xs">
                          {a.type}
                        </Badge>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        1박 {a.price_per_night}
                      </p>
                      {a.booking_url && (
                        <a
                          href={a.booking_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs text-primary hover:underline"
                        >
                          예약하기 →
                        </a>
                      )}
                      {a.coordinates && (
                        <div className="pt-1">
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
                                <div
                                  className="absolute inset-0 flex items-center justify-center bg-muted/60 z-10"
                                  style={{ height: 200 }}
                                >
                                  <Loader2 className="h-6 w-6 animate-spin text-primary" />
                                </div>
                              )}
                              <iframe
                                title={a.name}
                                src={`https://maps.google.com/maps?q=${a.coordinates.latitude},${a.coordinates.longitude}&z=15&output=embed`}
                                width="100%"
                                height="200"
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
                      )}
                    </div>
                  );
                })}
              </div>
            </section>
          )}

        {/* Transport */}
        {travel_tips.transport &&
          (travel_tips.transport.from_airport ||
            travel_tips.transport.local ||
            travel_tips.transport.intercity) && (
            <section>
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Bus className="h-5 w-5 text-primary" />
                교통 정보
              </h2>
              <div className="grid sm:grid-cols-3 gap-3">
                {travel_tips.transport.from_airport && (
                  <div className="p-4 rounded-xl bg-muted/50 border space-y-1">
                    <p className="text-xs font-semibold">공항 → 시내</p>
                    <p className="text-sm text-muted-foreground">
                      {travel_tips.transport.from_airport}
                    </p>
                  </div>
                )}
                {travel_tips.transport.local && (
                  <div className="p-4 rounded-xl bg-muted/50 border space-y-1">
                    <p className="text-xs font-semibold">현지 교통</p>
                    <p className="text-sm text-muted-foreground">
                      {travel_tips.transport.local}
                    </p>
                  </div>
                )}
                {travel_tips.transport.intercity && (
                  <div className="p-4 rounded-xl bg-muted/50 border space-y-1">
                    <p className="text-xs font-semibold">도시 간 이동</p>
                    <p className="text-sm text-muted-foreground">
                      {travel_tips.transport.intercity}
                    </p>
                  </div>
                )}
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
            {travel_tips.precautions && (
              <div className="flex gap-3 p-4 rounded-xl bg-amber-500/10 border border-amber-500/30">
                <AlertTriangle className="h-5 w-5 text-amber-500 shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-semibold text-amber-700 dark:text-amber-400 mb-1">
                    주의사항
                  </p>
                  <p className="text-sm text-amber-800 dark:text-amber-300 leading-relaxed">
                    {travel_tips.precautions}
                  </p>
                </div>
              </div>
            )}
            {travel_tips.cultural_notes && (
              <div className="flex gap-3 p-4 rounded-xl bg-blue-500/10 border border-blue-500/30">
                <Globe className="h-5 w-5 text-blue-500 shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-semibold text-blue-700 dark:text-blue-400 mb-1">
                    문화·예절
                  </p>
                  <p className="text-sm text-blue-800 dark:text-blue-300 leading-relaxed">
                    {travel_tips.cultural_notes}
                  </p>
                </div>
              </div>
            )}
            {travel_tips.health_tips && (
              <div className="flex gap-3 p-4 rounded-xl bg-red-500/10 border border-red-500/30">
                <Shield className="h-5 w-5 text-red-500 shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-semibold text-red-700 dark:text-red-400 mb-1">
                    건강 정보
                  </p>
                  <p className="text-sm text-red-800 dark:text-red-300 leading-relaxed">
                    {travel_tips.health_tips}
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

            {(travel_tips.sim_card ||
              (travel_tips.apps && travel_tips.apps.length > 0)) && (
              <div className="grid sm:grid-cols-2 gap-4">
                {travel_tips.sim_card && (
                  <div className="p-4 rounded-xl bg-muted/50 border space-y-2">
                    <div className="flex items-center gap-2 font-semibold text-sm">
                      <Smartphone className="h-4 w-4 text-primary" />
                      유심/인터넷
                    </div>
                    <p className="text-sm text-muted-foreground">
                      {travel_tips.sim_card}
                    </p>
                  </div>
                )}
                {travel_tips.apps && travel_tips.apps.length > 0 && (
                  <div className="p-4 rounded-xl bg-muted/50 border space-y-2">
                    <div className="flex items-center gap-2 font-semibold text-sm">
                      <Smartphone className="h-4 w-4 text-primary" />
                      유용한 앱
                    </div>
                    <div className="flex flex-wrap gap-1.5">
                      {travel_tips.apps.map((app, i) => (
                        <Badge key={i} variant="secondary" className="text-xs">
                          {app}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {travel_tips.emergency && (
              <div className="p-4 rounded-xl bg-muted/50 border space-y-2">
                <div className="flex items-center gap-2 font-semibold text-sm">
                  <Phone className="h-4 w-4 text-primary" />
                  긴급 연락처
                </div>
                <div className="grid sm:grid-cols-3 gap-2 text-sm text-muted-foreground">
                  {travel_tips.emergency.police && (
                    <span>🚔 경찰: {travel_tips.emergency.police}</span>
                  )}
                  {travel_tips.emergency.ambulance && (
                    <span>🚑 구급: {travel_tips.emergency.ambulance}</span>
                  )}
                  {travel_tips.emergency.korean_embassy && (
                    <span>
                      🇰🇷 대사관: {travel_tips.emergency.korean_embassy}
                    </span>
                  )}
                </div>
              </div>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}

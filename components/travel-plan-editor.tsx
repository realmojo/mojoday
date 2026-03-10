"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import {
  Plus,
  Trash2,
  Save,
  X,
  MapPin,
  Clock,
  Bus,
  BedDouble,
  Utensils,
  Wallet,
  AlertTriangle,
  Backpack,
  Info,
  GripVertical,
} from "lucide-react";
import type { TravelPlanData, Activity, DaySchedule } from "./travel-plan-detail";

/* ── 가격 항목 타입 ── */
type PriceEntry = { key: string; value: string };

function priceToEntries(p: Record<string, string> | null): PriceEntry[] {
  return p ? Object.entries(p).map(([key, value]) => ({ key, value })) : [];
}

function entriesToPrice(entries: PriceEntry[]): Record<string, string> | null {
  const result: Record<string, string> = {};
  entries.forEach(({ key, value }) => {
    if (key.trim()) result[key.trim()] = value;
  });
  return Object.keys(result).length > 0 ? result : null;
}

/* ── 빈 항목 생성 ── */
function emptyActivity(): Activity {
  return {
    time_range: "",
    location: "",
    description: "",
    transportation: null,
    accommodation: null,
    food: null,
    price_info: null,
    coordinates: null,
  };
}

function emptyDay(n: number): DaySchedule {
  return { day: n, category: `Day ${n} 일정`, activities: [emptyActivity()] };
}

/* ──────────────────────────────────────────────
   가격 정보 인라인 편집기
────────────────────────────────────────────── */
function PriceEditor({
  entries,
  onChange,
}: {
  entries: PriceEntry[];
  onChange: (entries: PriceEntry[]) => void;
}) {
  const add = () => onChange([...entries, { key: "", value: "" }]);
  const remove = (i: number) => onChange(entries.filter((_, idx) => idx !== i));
  const update = (i: number, field: "key" | "value", val: string) => {
    const next = entries.map((e, idx) => (idx === i ? { ...e, [field]: val } : e));
    onChange(next);
  };

  return (
    <div className="space-y-1.5">
      {entries.map((entry, i) => (
        <div key={i} className="flex gap-1.5 items-center">
          <Input
            value={entry.key}
            onChange={(e) => update(i, "key", e.target.value)}
            placeholder="항목"
            className="h-8 text-xs flex-1"
          />
          <span className="text-muted-foreground text-xs shrink-0">:</span>
          <Input
            value={entry.value}
            onChange={(e) => update(i, "value", e.target.value)}
            placeholder="가격"
            className="h-8 text-xs flex-1"
          />
          <button onClick={() => remove(i)} className="shrink-0 text-muted-foreground hover:text-destructive">
            <X className="h-3.5 w-3.5" />
          </button>
        </div>
      ))}
      <Button type="button" variant="ghost" size="sm" className="h-7 text-xs px-2 text-muted-foreground" onClick={add}>
        <Plus className="h-3 w-3 mr-1" />
        가격 항목 추가
      </Button>
    </div>
  );
}

/* ──────────────────────────────────────────────
   활동 카드 (편집 가능)
────────────────────────────────────────────── */
function ActivityCard({
  activity,
  onUpdate,
  onDelete,
}: {
  activity: Activity;
  onUpdate: (updated: Activity) => void;
  onDelete: () => void;
}) {
  const [priceEntries, setPriceEntries] = useState<PriceEntry[]>(
    () => priceToEntries(activity.price_info)
  );

  const set = <K extends keyof Activity>(key: K, value: Activity[K]) => {
    onUpdate({ ...activity, [key]: value });
  };

  const handlePriceChange = (entries: PriceEntry[]) => {
    setPriceEntries(entries);
    onUpdate({ ...activity, price_info: entriesToPrice(entries) });
  };

  return (
    <div className="rounded-xl border bg-background shadow-sm overflow-hidden">
      {/* 카드 헤더 */}
      <div className="flex items-center gap-2 px-3 py-2 bg-muted/30 border-b">
        <GripVertical className="h-4 w-4 text-muted-foreground/40 shrink-0" />
        <Clock className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
        <Input
          value={activity.time_range ?? ""}
          onChange={(e) => set("time_range", e.target.value || null)}
          placeholder="타임스탬프 (예: [00:05:00] - [00:12:00])"
          className="h-7 text-xs border-0 bg-transparent p-0 focus-visible:ring-0 font-mono"
        />
        <button onClick={onDelete} className="ml-auto shrink-0 text-muted-foreground hover:text-destructive transition-colors">
          <Trash2 className="h-4 w-4" />
        </button>
      </div>

      <div className="p-4 space-y-3">
        {/* 장소 */}
        <div className="flex items-center gap-2">
          <MapPin className="h-4 w-4 text-primary shrink-0" />
          <Input
            value={activity.location}
            onChange={(e) => set("location", e.target.value)}
            placeholder="장소 (예: 취리히 중앙역)"
            className="h-8 font-medium"
          />
        </div>

        {/* 설명 */}
        <Textarea
          value={activity.description}
          onChange={(e) => set("description", e.target.value)}
          placeholder="활동 설명..."
          className="text-sm min-h-[72px] resize-none"
        />

        {/* 교통 / 숙소 / 음식 */}
        <div className="grid sm:grid-cols-3 gap-2">
          <div className="flex items-center gap-1.5">
            <Bus className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
            <Input
              value={activity.transportation ?? ""}
              onChange={(e) => set("transportation", e.target.value || null)}
              placeholder="교통 수단"
              className="h-8 text-sm"
            />
          </div>
          <div className="flex items-center gap-1.5">
            <BedDouble className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
            <Input
              value={activity.accommodation ?? ""}
              onChange={(e) => set("accommodation", e.target.value || null)}
              placeholder="숙소"
              className="h-8 text-sm"
            />
          </div>
          <div className="flex items-center gap-1.5">
            <Utensils className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
            <Input
              value={activity.food ?? ""}
              onChange={(e) => set("food", e.target.value || null)}
              placeholder="음식"
              className="h-8 text-sm"
            />
          </div>
        </div>

        {/* 가격 정보 */}
        <div className="border rounded-lg p-3 space-y-2 bg-muted/20">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-muted-foreground">
            <Wallet className="h-3.5 w-3.5" />
            가격 정보
          </div>
          <PriceEditor entries={priceEntries} onChange={handlePriceChange} />
        </div>
      </div>
    </div>
  );
}

/* ──────────────────────────────────────────────
   Day 섹션
────────────────────────────────────────────── */
function DaySection({
  day,
  onUpdate,
  onDelete,
}: {
  day: DaySchedule;
  onUpdate: (updated: DaySchedule) => void;
  onDelete: () => void;
}) {
  const addActivity = () =>
    onUpdate({ ...day, activities: [...day.activities, emptyActivity()] });

  const updateActivity = (idx: number, updated: Activity) =>
    onUpdate({
      ...day,
      activities: day.activities.map((a, i) => (i === idx ? updated : a)),
    });

  const deleteActivity = (idx: number) =>
    onUpdate({ ...day, activities: day.activities.filter((_, i) => i !== idx) });

  return (
    <div className="space-y-3">
      {/* Day 헤더 */}
      <div className="flex items-center gap-3">
        <div className="h-9 w-9 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold text-sm shrink-0">
          {day.day}
        </div>
        <Input
          value={day.category}
          onChange={(e) => onUpdate({ ...day, category: e.target.value })}
          placeholder="Day 제목 (예: 취리히에서 리히텐슈타인으로)"
          className="h-9 font-semibold text-base"
        />
        <Button
          variant="ghost"
          size="icon"
          className="shrink-0 text-muted-foreground hover:text-destructive"
          onClick={onDelete}
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      </div>

      {/* 활동 카드들 */}
      <div className="ml-4 border-l-2 border-border pl-6 space-y-3">
        {day.activities.map((act, idx) => (
          <div key={idx} className="relative">
            <div className="absolute -left-[29px] top-4 h-3 w-3 rounded-full bg-primary/40 border-2 border-primary" />
            <ActivityCard
              activity={act}
              onUpdate={(updated) => updateActivity(idx, updated)}
              onDelete={() => deleteActivity(idx)}
            />
          </div>
        ))}

        <button
          onClick={addActivity}
          className="flex items-center gap-2 text-sm text-muted-foreground hover:text-primary transition-colors py-2"
        >
          <Plus className="h-4 w-4" />
          활동 추가
        </button>
      </div>
    </div>
  );
}

/* ──────────────────────────────────────────────
   메인 에디터
────────────────────────────────────────────── */
export function TravelPlanEditor({
  initialPlan,
  onSave,
}: {
  initialPlan: TravelPlanData;
  onSave: (plan: TravelPlanData) => void;
}) {
  const [plan, setPlan] = useState<TravelPlanData>(initialPlan);
  const [saved, setSaved] = useState(false);

  const updateDay = (idx: number, updated: DaySchedule) =>
    setPlan((p) => ({
      ...p,
      travel_schedule: p.travel_schedule.map((d, i) => (i === idx ? updated : d)),
    }));

  const deleteDay = (idx: number) =>
    setPlan((p) => ({
      ...p,
      travel_schedule: p.travel_schedule
        .filter((_, i) => i !== idx)
        .map((d, i) => ({ ...d, day: i + 1 })),
    }));

  const addDay = () =>
    setPlan((p) => ({
      ...p,
      travel_schedule: [
        ...p.travel_schedule,
        emptyDay(p.travel_schedule.length + 1),
      ],
    }));

  const setTip = (key: keyof typeof plan.travel_tips, value: string) =>
    setPlan((p) => ({ ...p, travel_tips: { ...p.travel_tips, [key]: value } }));

  const handleSave = () => {
    onSave(plan);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="space-y-10 pb-20">

      {/* 영상 정보 */}
      <section className="space-y-3">
        <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">
          영상 정보
        </h3>
        <div className="grid sm:grid-cols-2 gap-3">
          <div className="space-y-1">
            <label className="text-xs text-muted-foreground">제목</label>
            <Input
              value={plan.video_info.title}
              onChange={(e) =>
                setPlan((p) => ({
                  ...p,
                  video_info: { ...p.video_info, title: e.target.value },
                }))
              }
            />
          </div>
          <div className="space-y-1">
            <label className="text-xs text-muted-foreground">채널명</label>
            <Input
              value={plan.video_info.channel_name}
              onChange={(e) =>
                setPlan((p) => ({
                  ...p,
                  video_info: { ...p.video_info, channel_name: e.target.value },
                }))
              }
            />
          </div>
        </div>
        <div className="space-y-1">
          <label className="text-xs text-muted-foreground">요약</label>
          <Textarea
            value={plan.video_info.summary}
            onChange={(e) =>
              setPlan((p) => ({
                ...p,
                video_info: { ...p.video_info, summary: e.target.value },
              }))
            }
            className="resize-none min-h-[72px]"
          />
        </div>
      </section>

      {/* 여행 일정 */}
      <section className="space-y-6">
        <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">
          여행 일정
        </h3>

        {plan.travel_schedule.map((day, idx) => (
          <DaySection
            key={idx}
            day={day}
            onUpdate={(updated) => updateDay(idx, updated)}
            onDelete={() => deleteDay(idx)}
          />
        ))}

        <Button variant="outline" onClick={addDay} className="gap-2">
          <Plus className="h-4 w-4" />
          날 추가
        </Button>
      </section>

      {/* 여행 팁 */}
      <section className="space-y-4">
        <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">
          여행 팁
        </h3>

        <div className="space-y-1">
          <label className="text-xs flex items-center gap-1.5 text-muted-foreground">
            <AlertTriangle className="h-3.5 w-3.5 text-amber-500" />
            주의사항
          </label>
          <Textarea
            value={plan.travel_tips.precautions}
            onChange={(e) => setTip("precautions", e.target.value)}
            className="resize-none min-h-[72px] text-sm"
          />
        </div>

        <div className="grid sm:grid-cols-3 gap-3">
          <div className="space-y-1">
            <label className="text-xs flex items-center gap-1.5 text-muted-foreground">
              <Backpack className="h-3.5 w-3.5" />
              준비물
            </label>
            <Textarea
              value={plan.travel_tips.items}
              onChange={(e) => setTip("items", e.target.value)}
              className="resize-none min-h-[88px] text-sm"
            />
          </div>
          <div className="space-y-1">
            <label className="text-xs flex items-center gap-1.5 text-muted-foreground">
              <Wallet className="h-3.5 w-3.5" />
              예상 비용
            </label>
            <Textarea
              value={plan.travel_tips.total_expense}
              onChange={(e) => setTip("total_expense", e.target.value)}
              className="resize-none min-h-[88px] text-sm"
            />
          </div>
          <div className="space-y-1">
            <label className="text-xs flex items-center gap-1.5 text-muted-foreground">
              <Info className="h-3.5 w-3.5" />
              유용한 정보
            </label>
            <Textarea
              value={plan.travel_tips.useful_info}
              onChange={(e) => setTip("useful_info", e.target.value)}
              className="resize-none min-h-[88px] text-sm"
            />
          </div>
        </div>
      </section>

      {/* 저장 버튼 (하단 고정) */}
      <div className="fixed bottom-0 left-0 right-0 z-50 bg-background/90 backdrop-blur border-t py-3 px-4">
        <div className="container mx-auto max-w-4xl flex justify-end">
          <Button onClick={handleSave} size="lg" className="gap-2 min-w-[120px]">
            <Save className="h-4 w-4" />
            {saved ? "저장됨 ✓" : "저장하기"}
          </Button>
        </div>
      </div>
    </div>
  );
}

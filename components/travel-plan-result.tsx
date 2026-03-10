"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  CalendarDays,
  UtensilsCrossed,
  MapPin,
  Wallet,
  Bus,
  Lightbulb,
  Clock,
} from "lucide-react";

export type TravelPlan = {
  destination: string;
  country: string;
  duration: string;
  summary: string;
  itinerary: {
    day: number;
    title: string;
    places: string[];
    meals: string[];
    tip: string;
  }[];
  restaurants: {
    name: string;
    category: string;
    description: string;
  }[];
  attractions: {
    name: string;
    description: string;
  }[];
  transportation: string[];
  budget: {
    total: string;
    breakdown: {
      flight: string;
      accommodation: string;
      food: string;
      transport: string;
      activity: string;
    };
  };
  tips: string[];
};

export function TravelPlanResult({ plan }: { plan: TravelPlan }) {
  return (
    <div className="w-full max-w-4xl mx-auto space-y-6 pt-6">
      {/* Header */}
      <div className="text-center space-y-2 pb-4 border-b">
        <div className="flex items-center justify-center gap-2 flex-wrap">
          <Badge variant="secondary" className="text-sm px-3">
            <MapPin className="h-3.5 w-3.5 mr-1" />
            {plan.country}
          </Badge>
          <Badge variant="secondary" className="text-sm px-3">
            <Clock className="h-3.5 w-3.5 mr-1" />
            {plan.duration}
          </Badge>
        </div>
        <h2 className="text-2xl md:text-3xl font-bold">{plan.destination} 여행 계획</h2>
        <p className="text-muted-foreground">{plan.summary}</p>
      </div>

      {/* Itinerary */}
      {plan.itinerary.length > 0 && (
        <section>
          <h3 className="text-lg font-semibold flex items-center gap-2 mb-4">
            <CalendarDays className="h-5 w-5 text-primary" />
            일별 여행 일정
          </h3>
          <div className="space-y-3">
            {plan.itinerary.map((day) => (
              <Card key={day.day} className="border">
                <CardHeader className="pb-2 pt-4 px-4">
                  <CardTitle className="text-base flex items-center gap-2">
                    <span className="bg-primary text-primary-foreground rounded-full w-7 h-7 flex items-center justify-center text-sm font-bold shrink-0">
                      {day.day}
                    </span>
                    {day.title}
                  </CardTitle>
                </CardHeader>
                <CardContent className="px-4 pb-4 space-y-3">
                  {day.places.length > 0 && (
                    <div className="flex flex-wrap gap-1.5">
                      {day.places.map((place) => (
                        <Badge key={place} variant="outline" className="text-xs">
                          <MapPin className="h-3 w-3 mr-1" />
                          {place}
                        </Badge>
                      ))}
                    </div>
                  )}
                  {day.meals.length > 0 && (
                    <div className="text-sm text-muted-foreground space-y-0.5">
                      {day.meals.map((meal) => (
                        <p key={meal}>{meal}</p>
                      ))}
                    </div>
                  )}
                  {day.tip && (
                    <p className="text-sm bg-muted/50 rounded px-3 py-2 text-muted-foreground">
                      💡 {day.tip}
                    </p>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </section>
      )}

      <div className="grid md:grid-cols-2 gap-6">
        {/* Restaurants */}
        {plan.restaurants.length > 0 && (
          <section>
            <h3 className="text-lg font-semibold flex items-center gap-2 mb-4">
              <UtensilsCrossed className="h-5 w-5 text-primary" />
              추천 맛집
            </h3>
            <div className="space-y-2">
              {plan.restaurants.map((r) => (
                <div key={r.name} className="p-3 rounded-lg border bg-background">
                  <div className="flex items-start justify-between gap-2">
                    <p className="font-medium text-sm">{r.name}</p>
                    <Badge variant="secondary" className="text-xs shrink-0">
                      {r.category}
                    </Badge>
                  </div>
                  {r.description && (
                    <p className="text-xs text-muted-foreground mt-1">{r.description}</p>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Attractions */}
        {plan.attractions.length > 0 && (
          <section>
            <h3 className="text-lg font-semibold flex items-center gap-2 mb-4">
              <MapPin className="h-5 w-5 text-primary" />
              주요 명소
            </h3>
            <div className="space-y-2">
              {plan.attractions.map((a) => (
                <div key={a.name} className="p-3 rounded-lg border bg-background">
                  <p className="font-medium text-sm">{a.name}</p>
                  {a.description && (
                    <p className="text-xs text-muted-foreground mt-1">{a.description}</p>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}
      </div>

      {/* Budget */}
      {plan.budget?.total && (
        <section>
          <h3 className="text-lg font-semibold flex items-center gap-2 mb-4">
            <Wallet className="h-5 w-5 text-primary" />
            예상 예산
          </h3>
          <Card className="border">
            <CardContent className="p-4">
              <div className="flex items-center justify-between mb-4 pb-3 border-b">
                <span className="font-semibold">총 예상 비용</span>
                <span className="text-lg font-bold text-primary">{plan.budget.total}</span>
              </div>
              {plan.budget.breakdown && (
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-sm">
                  {plan.budget.breakdown.flight && (
                    <div className="p-2 rounded bg-muted/50">
                      <p className="text-xs text-muted-foreground">항공</p>
                      <p className="font-medium">{plan.budget.breakdown.flight}</p>
                    </div>
                  )}
                  {plan.budget.breakdown.accommodation && (
                    <div className="p-2 rounded bg-muted/50">
                      <p className="text-xs text-muted-foreground">숙소</p>
                      <p className="font-medium">{plan.budget.breakdown.accommodation}</p>
                    </div>
                  )}
                  {plan.budget.breakdown.food && (
                    <div className="p-2 rounded bg-muted/50">
                      <p className="text-xs text-muted-foreground">식비</p>
                      <p className="font-medium">{plan.budget.breakdown.food}</p>
                    </div>
                  )}
                  {plan.budget.breakdown.transport && (
                    <div className="p-2 rounded bg-muted/50">
                      <p className="text-xs text-muted-foreground">교통</p>
                      <p className="font-medium">{plan.budget.breakdown.transport}</p>
                    </div>
                  )}
                  {plan.budget.breakdown.activity && (
                    <div className="p-2 rounded bg-muted/50">
                      <p className="text-xs text-muted-foreground">활동/입장료</p>
                      <p className="font-medium">{plan.budget.breakdown.activity}</p>
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </section>
      )}

      {/* Transportation */}
      {plan.transportation.length > 0 && (
        <section>
          <h3 className="text-lg font-semibold flex items-center gap-2 mb-4">
            <Bus className="h-5 w-5 text-primary" />
            교통 정보
          </h3>
          <ul className="space-y-2">
            {plan.transportation.map((item) => (
              <li key={item} className="flex items-start gap-2 text-sm text-muted-foreground">
                <span className="mt-0.5 text-primary">•</span>
                {item}
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Tips */}
      {plan.tips.length > 0 && (
        <section>
          <h3 className="text-lg font-semibold flex items-center gap-2 mb-4">
            <Lightbulb className="h-5 w-5 text-primary" />
            여행 꿀팁
          </h3>
          <div className="grid sm:grid-cols-2 gap-3">
            {plan.tips.map((tip) => (
              <div key={tip} className="p-3 rounded-lg bg-primary/5 border border-primary/10 text-sm">
                {tip}
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

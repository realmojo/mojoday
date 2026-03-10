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


const DEMO_DATA: Record<string, TravelPlanData> = {
  cBJ9oLoPcyE: {
    video_info: {
      id: "cBJ9oLoPcyE",
      title: "태국 여행갔다가 상상도 못한 병에 걸렸습니다.. 지금은 가지 마세요",
      thumbnail_url: "https://i.ytimg.com/vi/cBJ9oLoPcyE/maxresdefault.jpg",
      channel_name: "꾸준 kkujun",
      summary:
        "2월~4월 사이 태국 북부(치앙마이 등)의 심각한 미세먼지(화전 농업으로 인한 연기) 위험성을 경고하고, 이를 피해 대안지로 선택한 태국 북동부 '우돈타니' 도시를 탐방하며 로컬 물가와 인프라를 소개하는 콘텐츠입니다.",
    },
    travel_schedule: [
      {
        day: 1,
        category: "치앙마이 미세먼지 원인 파악 및 우돈타니 이동",
        activities: [
          {
            time_range: "[00:00:00] - [00:05:54]",
            location: "태국 북부 국경 지대 (치앙라이 인근)",
            description:
              "치앙마이 미세먼지의 원인인 화전(산 태우기) 현장을 확인하기 위해 미얀마 국경 인근 산악지대 탐방",
            transportation: "오토바이 (렌트)",
            accommodation: null,
            food: null,
            price_info: null,
            coordinates: { latitude: 20.4431, longitude: 99.8811 },
          },
          {
            time_range: "[00:06:17] - [00:41:44]",
            location: "태국 우돈타니 (Udon Thani)",
            description:
              "치앙마이의 대안지로 선택한 우돈타니 시내 도착 및 도보 탐방. 쇼핑몰, 로컬 식당, 야시장 투어",
            transportation:
              "버스 (치앙라이-우돈타니 이동), 오토바이 택시 (시내 이동 25바트)",
            accommodation: "우돈타니 시내 4성급 호텔 (The Pannarai Hotel 추정)",
            food: "이산식 솜담(생새우 추가), 양념 꼬치, 태국식 국수(한방 국물), 수제 커피, 야시장 음식(오징어 구이, 소시지, 족발덮밥 등)",
            price_info: {
              "솜담 (생새우 추가)": "110 THB",
              "거리 꼬치": "5~10 THB",
              국수: "50~70 THB",
              "스페셜티 커피": "80 THB",
              "호텔 1박": "약 100,000 KRW",
              "야시장 식사": "약 200~300 THB",
            },
            coordinates: { latitude: 17.4138, longitude: 102.7872 },
          },
        ],
      },
    ],
    travel_tips: {
      precautions:
        "2월~4월 사이 태국 북부(치앙마이, 치앙라이 등)는 화전으로 인한 미세먼지가 매우 심각하여 호흡기 질환 및 중이염 위험이 높음. 이 시기 여행은 가급적 피할 것.",
      items: "마스크(미세먼지 차단용), 현금(로컬 시장 이용 시 필요)",
      total_expense:
        "숙박비 포함 하루 약 15~20만 원 내외 (럭셔리 숙박 기준, 로컬 생활 시 훨씬 저렴)",
      useful_info:
        "우돈타니는 치앙마이보다 물가가 저렴하며 센트럴 플라자 등 대형 쇼핑몰 인프라가 잘 되어 있어 한 달 살기 대안지로 적합함.",
    },
  },
  EcwYDCLSWSE: {
    video_info: {
      id: "EcwYDCLSWSE",
      title: "0.001%만 이민 갈 수 있는 비밀 국가",
      thumbnail_url: "https://i.ytimg.com/vi/EcwYDCLSWSE/maxresdefault.jpg",
      channel_name: "서재로36",
      summary:
        "유럽의 초소형 국가이자 세계에서 가장 부유한 나라 중 하나인 '리히텐슈타인'을 직접 방문하여, 독특한 국가 운영 방식(군대 없음, 스위스 위탁 외교 등), 높은 물가, 낮은 범죄율, 그리고 복지 혜택과 이민 정책 등을 소개하는 여행 콘텐츠입니다.",
    },
    travel_schedule: [
      {
        day: 1,
        category: "스위스 취리히에서 리히텐슈타인 이동 및 바두츠 탐방",
        activities: [
          {
            time_range: "[00:01:12] - [00:03:00]",
            location: "스위스 취리히 중앙역 (Zürich HB)",
            description:
              "리히텐슈타인에는 공항이 없어 인근 나라인 스위스 취리히에서 기차와 버스를 이용하여 이동 준비",
            transportation: "도보",
            accommodation: null,
            food: "취리히 마트 신라면(6,500원), 에비앙 생수 포함 총 14,000원 지출",
            price_info: {
              "자르간스행 기차표": "약 75,000 KRW (세금 포함)",
            },
            coordinates: { latitude: 47.3781, longitude: 8.5401 },
          },
          {
            time_range: "[00:03:00] - [00:04:30]",
            location: "스위스 자르간스 (Sargans) 및 국경 이동",
            description: "기차를 타고 자르간스에 도착하여 리히텐슈타인행 버스로 환승",
            transportation: "기차, 버스",
            accommodation: null,
            food: "자르간스 편의점 샌드위치 및 음료 (14,000원)",
            price_info: null,
            coordinates: { latitude: 47.0494, longitude: 9.4442 },
          },
          {
            time_range: "[00:05:25] - [00:10:55]",
            location: "리히텐슈타인 샤안 (Schaan)",
            description:
              "리히텐슈타인 최대 도시인 샤안에 위치한 유일한 호스텔 체크인 및 시내 탐방",
            transportation: "도보",
            accommodation: "Jugendherberge Schaan-Vaduz (유스호스텔)",
            food: null,
            price_info: {
              "숙박 1박": "약 200,000 KRW (제일 저렴한 방 기준)",
            },
            coordinates: { latitude: 47.1652, longitude: 9.5085 },
          },
          {
            time_range: "[00:22:38] - [00:24:25]",
            location: "리히텐슈타인 수도 바두츠 (Vaduz)",
            description:
              "수도 바두츠 시내 관광, 국회 의사당, 정부 청사 및 언덕 위 바두츠 성 조망",
            transportation: "도보 (샤안에서 바두츠까지 약 1시간 도보 이동)",
            accommodation: null,
            food: "로컬 마트 장보기(하몽, 빵, 와인, 클렌징폼 등 약 30,000원)",
            price_info: {
              버스요금: "약 10,000 KRW (단거리 기준)",
              "기념품 왕관 캔들": "40,000 KRW",
              "캔 와인": "12,000 KRW",
            },
            coordinates: { latitude: 47.141, longitude: 9.5215 },
          },
        ],
      },
      {
        day: 2,
        category: "체크아웃 및 여행 마무리",
        activities: [
          {
            time_range: "[00:26:29] - [00:28:09]",
            location: "호스텔 및 주변",
            description: "눈 내리는 풍경 감상 및 조식 식사 후 체크아웃",
            transportation: "버스 (다음 목적지 이동)",
            accommodation: null,
            food: "호스텔 조식 (색칠된 계란 등)",
            price_info: null,
            coordinates: { latitude: 47.1652, longitude: 9.5085 },
          },
        ],
      },
    ],
    travel_tips: {
      precautions:
        "물가가 매우 비싸므로 외식보다는 마트 이용을 권장하며, 숙박 시설이 적어 미리 예약이 필수임. 대중교통(버스) 비용도 상당함.",
      items: "스위스 프랑(CHF) 또는 유로, 우산/우비 (날씨가 변덕스러움), 구글 지도(AI 활용 길찾기 추천)",
      total_expense:
        "1박 2일 기준 숙박비 20만원 + 교통비 약 10만원 + 식비/기타 약 10만원 = 최소 40~50만 원 이상 소요",
      useful_info:
        "리히텐슈타인은 스위스와 경제/외교적으로 밀접하여 스위스 프랑을 통화로 사용함. 8월 15일 국경일에는 바두츠 성 정원이 개방되어 국왕이 와인을 나눠주는 행사가 열림.",
    },
  },
};

export default function PlanPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [plan, setPlan] = useState<TravelPlanData | null>(null);
  const [ready, setReady] = useState(false);
  const [tab, setTab] = useState<"view" | "edit">("view");

  useEffect(() => {
    async function loadPlan() {
      // 1. Supabase에서 조회
      const { data } = await supabase
        .from("plans")
        .select("video_id, title, thumbnail_url, channel_name, summary, country, regions, trip_type, tags, travel_schedule, travel_tips")
        .eq("video_id", id)
        .single();

      if (data) {
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
          },
          travel_schedule: data.travel_schedule,
          travel_tips: data.travel_tips,
        });
        setReady(true);
        return;
      }

      // 2. 데모 데이터 fallback
      if (DEMO_DATA[id]) {
        setPlan(DEMO_DATA[id]);
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

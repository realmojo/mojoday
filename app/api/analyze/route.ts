import { GoogleGenAI } from "@google/genai";
import { NextRequest, NextResponse } from "next/server";
import { createServerClient } from "@/lib/supabase";
import { YoutubeTranscript } from "youtube-transcript";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY! });

function extractVideoId(url: string): string | null {
  const match = url.match(
    /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\s?]+)/,
  );
  return match?.[1] ?? null;
}

function formatTimestamp(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  return `[${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}]`;
}

async function fetchTranscript(videoId: string): Promise<string | null> {
  try {
    const transcript = await YoutubeTranscript.fetchTranscript(videoId, { lang: "ko" });
    if (!transcript || transcript.length === 0) {
      const fallback = await YoutubeTranscript.fetchTranscript(videoId);
      if (!fallback || fallback.length === 0) return null;
      return fallback.map((t) => `${formatTimestamp(t.offset / 1000)} ${t.text}`).join("\n");
    }
    return transcript.map((t) => `${formatTimestamp(t.offset / 1000)} ${t.text}`).join("\n");
  } catch {
    return null;
  }
}

const SYSTEM_INSTRUCTION = `당신은 여행 유튜브 영상 분석 전문가입니다.
주어진 자막 또는 영상을 분석하고 여행자에게 실질적으로 도움이 되는 정보를 최대한 상세하게 추출합니다.

분석 원칙:
- 자막/영상에 실제로 언급된 정보만 추출하고, 없는 정보는 null로 표기합니다.
- 장소는 실제 구글 지도에서 찾을 수 있도록 위도/경도를 최대한 포함합니다.
- 가격은 자막/영상에서 언급된 원래 통화 단위로 표기합니다.
- 반드시 순수 JSON만 출력하고, 마크다운 코드블록을 사용하지 않습니다.`;

function buildPrompt(videoId: string, transcript: string | null): string {
  const source = transcript
    ? `아래는 영상의 자막입니다. 자막을 기반으로 분석하세요:\n\n<transcript>\n${transcript}\n</transcript>`
    : `영상 URL을 직접 분석하세요.`;

  return `${source}

위 내용을 분석해서 아래 JSON 형식으로 정확하게 반환하세요.
마크다운 코드블록 없이 순수 JSON만 출력하세요.

{
  "video_info": {
    "id": "${videoId}",
    "title": "영상 제목",
    "thumbnail_url": "https://i.ytimg.com/vi/${videoId}/maxresdefault.jpg",
    "channel_name": "채널명",
    "summary": "영상 전체 요약 (여행 콘텐츠 핵심 내용, 2~3문장)",
    "country": "여행 국가명 (한국어+영문 병기, 예: 태국 (Thailand))",
    "regions": ["여행한 지역/도시 목록 (한국어+현지어 병기)"],
    "type": "여행 타입 (맛집/쇼핑/문화/유적지/자연/힐링/배낭여행/오지탐험/한달살기/럭셔리 중 해당하는 것들, 쉼표 구분)",
    "tags": ["관련 태그 5~10개 (한국어)"],
    "trip_duration": "여행 기간 (예: 1박 2일, 당일치기, 불명확하면 null)",
    "best_season": "최적 방문 시기 (예: 10~11월 가을, 연중 가능, 영상 기준)",
    "budget_level": "저예산 또는 중간 또는 럭셔리",
    "difficulty_level": "쉬움 또는 보통 또는 어려움 (접근성/오지 여부 기준)",
    "travel_style": "솔로 또는 커플 또는 가족 또는 그룹 (영상 기준)",
    "visa_info": "한국인 기준 비자 정보 (예: 무비자 30일, 모르면 null)",
    "currency": "현지 통화명과 대략적인 환율 (예: 태국 바트 (THB), 1바트 ≈ 40원)",
    "language": "현지 주요 언어와 영어 통용 여부"
  },
  "travel_schedule": [
    {
      "day": 1,
      "category": "하루를 요약하는 제목",
      "activities": [
        {
          "time_range": "영상 타임스탬프 (예: [00:00:00] - [00:05:54])",
          "location": "장소명 (도시/구역 포함, 한국어+현지어 병기)",
          "description": "해당 활동에 대한 구체적인 설명 (2~4문장)",
          "category": "관광지 또는 맛집 또는 숙소 또는 교통 또는 쇼핑 또는 자연 또는 액티비티",
          "transportation": "이동 수단 및 요금 (없으면 null)",
          "accommodation": "숙소명 및 등급/가격 정보 (없으면 null)",
          "food": "먹은 음식 목록 및 간단한 설명 (없으면 null)",
          "price_info": [{"name": "항목명", "price": "가격 (통화 포함)"}],
          "entry_fee": "입장료 (예: 무료, 500원) 또는 null",
          "duration": "권장 체류 시간 (예: 약 1시간) 또는 null",
          "opening_hours": "영업/운영 시간 또는 null",
          "reservation_required": false,
          "rating": "유튜버 추천도 (예: ★★★★☆) 또는 null",
          "tip": "현장 팁 (예: 오전 방문 추천, 현금만 받음) 또는 null",
          "coordinates": {"latitude": 위도숫자, "longitude": 경도숫자}
        }
      ]
    }
  ],
  "travel_tips": {
    "highlights": ["핵심 볼거리/경험 Top 3~5"],
    "precautions": "주의사항 (건강, 안전, 시기, 문화적 주의점 등)",
    "cultural_notes": "현지 문화·예절 주의사항 또는 null",
    "health_tips": "건강 관련 주의사항 (예방접종, 식수 등) 또는 null",
    "items": "추천 준비물 목록 (쉼표 구분)",
    "total_expense": "영상 기준 예상 총 여행 경비 (기간 및 1인 기준 명시)",
    "useful_info": "유용한 현지 정보",
    "sim_card": "현지 유심 구매 방법 및 가격 또는 null",
    "apps": ["현지에서 유용한 앱 목록"],
    "emergency": {
      "police": "경찰 긴급번호",
      "ambulance": "구급 긴급번호",
      "korean_embassy": "주재국 한국 대사관 연락처 또는 null"
    },
    "transport": {
      "from_airport": "공항→시내 이동 방법 및 비용",
      "local": "현지 이동 수단 요약",
      "intercity": "도시 간 이동 방법 및 소요시간 또는 null"
    },
    "restaurants": [
      {
        "name": "식당명",
        "menu": "대표 메뉴",
        "price": "가격대",
        "opening_hours": "영업시간 또는 null",
        "reservation_required": false,
        "coordinates": {"latitude": 위도숫자, "longitude": 경도숫자}
      }
    ],
    "accommodations": [
      {
        "name": "숙소명",
        "type": "호스텔 또는 게스트하우스 또는 호텔",
        "price_per_night": "1박 가격",
        "booking_url": "예약 링크 또는 null",
        "coordinates": {"latitude": 위도숫자, "longitude": 경도숫자}
      }
    ]
  }
}

규칙:
- travel_schedule은 영상에 등장하는 날짜/시간순으로 구성하세요
- 영상에 정보가 없으면 null 또는 빈 배열로 표기하세요
- price_info는 반드시 배열 형태 [{name, price}]로 반환하세요
- coordinates는 실제 장소의 위도/경도를 숫자로 입력하세요
- 반드시 유효한 JSON만 반환하세요`;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function mapDbRowToPlan(row: any) {
  const meta = row.meta ?? {};
  return {
    video_info: {
      id: row.video_id,
      title: row.title,
      thumbnail_url: row.thumbnail_url,
      channel_name: row.channel_name,
      summary: row.summary,
      country: row.country,
      regions: row.regions,
      type: row.trip_type,
      tags: row.tags,
      trip_duration: meta.trip_duration ?? null,
      best_season: meta.best_season ?? null,
      budget_level: meta.budget_level ?? null,
      difficulty_level: meta.difficulty_level ?? null,
      travel_style: meta.travel_style ?? null,
      visa_info: meta.visa_info ?? null,
      currency: meta.currency ?? null,
      language: meta.language ?? null,
    },
    travel_schedule: row.travel_schedule,
    travel_tips: row.travel_tips,
  };
}

export async function POST(req: NextRequest) {
  try {
    const { url } = await req.json();

    if (!url || !url.includes("youtube")) {
      return NextResponse.json({ error: "유효한 YouTube URL을 입력해주세요." }, { status: 400 });
    }

    const videoId = extractVideoId(url);
    if (!videoId) {
      return NextResponse.json({ error: "YouTube 영상 ID를 찾을 수 없습니다." }, { status: 400 });
    }

    const db = createServerClient();

    // 캐시 확인
    const { data: cached } = await db
      .from("plans")
      .select("video_id, title, thumbnail_url, channel_name, summary, country, regions, trip_type, tags, travel_schedule, travel_tips, meta")
      .eq("video_id", videoId)
      .single();

    if (cached) {
      return NextResponse.json({ plan: mapDbRowToPlan(cached), videoId, cached: true });
    }

    // 자막 가져오기
    const transcript = await fetchTranscript(videoId);
    console.log(transcript ? `자막 ${transcript.length}자 로드됨` : "자막 없음 → 영상 직접 분석");

    const parts = transcript
      ? [{ text: buildPrompt(videoId, transcript) }]
      : [
          { fileData: { fileUri: url, mimeType: "video/mp4" } },
          { text: buildPrompt(videoId, null) },
        ];

    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      config: { systemInstruction: SYSTEM_INSTRUCTION },
      contents: [{ role: "user", parts }],
    });

    const text = response.text ?? "";
    const cleaned = text.replace(/```json\n?|\n?```/g, "").trim();
    const plan = JSON.parse(cleaned);

    await db.from("plans").upsert(
      {
        video_id: videoId,
        title: plan.video_info?.title ?? null,
        thumbnail_url: plan.video_info?.thumbnail_url ?? null,
        channel_name: plan.video_info?.channel_name ?? null,
        summary: plan.video_info?.summary ?? null,
        country: plan.video_info?.country ?? null,
        regions: plan.video_info?.regions ?? [],
        trip_type: plan.video_info?.type ?? null,
        tags: plan.video_info?.tags ?? [],
        travel_schedule: plan.travel_schedule ?? [],
        travel_tips: plan.travel_tips ?? {},
        meta: {
          trip_duration: plan.video_info?.trip_duration ?? null,
          best_season: plan.video_info?.best_season ?? null,
          budget_level: plan.video_info?.budget_level ?? null,
          difficulty_level: plan.video_info?.difficulty_level ?? null,
          travel_style: plan.video_info?.travel_style ?? null,
          visa_info: plan.video_info?.visa_info ?? null,
          currency: plan.video_info?.currency ?? null,
          language: plan.video_info?.language ?? null,
        },
      },
      { onConflict: "video_id" },
    );

    return NextResponse.json({ plan, videoId, transcriptUsed: !!transcript });
  } catch (error) {
    console.error("Gemini analyze error:", error);
    if (error instanceof SyntaxError) {
      return NextResponse.json({ error: "AI 응답 파싱 실패. 다시 시도해주세요." }, { status: 500 });
    }
    return NextResponse.json({ error: "영상 분석 중 오류가 발생했습니다. 다시 시도해주세요." }, { status: 500 });
  }
}

import { GoogleGenAI } from "@google/genai";
import { NextRequest, NextResponse } from "next/server";
import { createServerClient } from "@/lib/supabase";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY! });

function extractVideoId(url: string): string | null {
  const match = url.match(
    /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\s?]+)/
  );
  return match?.[1] ?? null;
}

function buildPrompt(videoId: string): string {
  return `이 유튜브 여행 영상을 분석해서 아래 JSON 형식으로 정확하게 반환하세요.
마크다운 코드블록 없이 순수 JSON만 출력하세요.

{
  "video_info": {
    "id": "${videoId}",
    "title": "영상 제목",
    "thumbnail_url": "https://i.ytimg.com/vi/${videoId}/maxresdefault.jpg",
    "channel_name": "채널명",
    "summary": "영상 한줄 요약 (여행 콘텐츠 핵심 설명)"
  },
  "travel_schedule": [
    {
      "day": 1,
      "category": "하루 전체를 요약하는 제목 (예: 치앙마이 미세먼지 원인 파악 및 우돈타니 이동)",
      "activities": [
        {
          "time_range": "영상 타임스탬프 (예: [00:00:00] - [00:05:54])",
          "location": "장소명 (도시/구역 포함)",
          "description": "해당 활동에 대한 구체적인 설명",
          "transportation": "이동 수단 (없으면 null)",
          "accommodation": "숙소 정보 (없으면 null)",
          "food": "먹은 음식 목록 (없으면 null)",
          "price_info": {"항목명": "가격 (통화 포함)"} 또는 null,
          "coordinates": {"latitude": 위도, "longitude": 경도} 또는 null
        }
      ]
    }
  ],
  "travel_tips": {
    "precautions": "주의사항 (건강, 안전, 시기 등)",
    "items": "준비물 목록 (쉼표로 구분)",
    "total_expense": "예상 총 비용",
    "useful_info": "유용한 현지 정보"
  }
}

규칙:
- travel_schedule은 영상에 등장하는 날짜/시간순으로 구성하세요
- 영상에 정보가 없으면 null로 표기하세요
- price_info는 영상에 언급된 실제 가격만 포함하세요
- 반드시 유효한 JSON만 반환하세요`;
}

export async function POST(req: NextRequest) {
  try {
    const { url } = await req.json();

    if (!url || !url.includes("youtube")) {
      return NextResponse.json(
        { error: "유효한 YouTube URL을 입력해주세요." },
        { status: 400 }
      );
    }

    const videoId = extractVideoId(url);
    if (!videoId) {
      return NextResponse.json(
        { error: "YouTube 영상 ID를 찾을 수 없습니다." },
        { status: 400 }
      );
    }

    const db = createServerClient();

    // 캐시 확인: 이미 분석된 영상이면 DB에서 반환
    const { data: cached } = await db
      .from("plans")
      .select("video_id, title, thumbnail_url, channel_name, summary, country, regions, trip_type, tags, travel_schedule, travel_tips")
      .eq("video_id", videoId)
      .single();

    if (cached) {
      const plan = {
        video_info: {
          id: cached.video_id,
          title: cached.title,
          thumbnail_url: cached.thumbnail_url,
          channel_name: cached.channel_name,
          summary: cached.summary,
          country: cached.country,
          regions: cached.regions,
          type: cached.trip_type,
          tags: cached.tags,
        },
        travel_schedule: cached.travel_schedule,
        travel_tips: cached.travel_tips,
      };
      return NextResponse.json({ plan, videoId, cached: true });
    }

    // Gemini 분석
    const response = await ai.models.generateContent({
      model: "gemini-2.0-flash",
      contents: [
        {
          role: "user",
          parts: [
            {
              fileData: {
                fileUri: url,
                mimeType: "video/mp4",
              },
            },
            { text: buildPrompt(videoId) },
          ],
        },
      ],
    });

    const text = response.text ?? "";
    const cleaned = text.replace(/```json\n?|\n?```/g, "").trim();
    const plan = JSON.parse(cleaned);

    // Supabase upsert
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
      },
      { onConflict: "video_id" }
    );

    return NextResponse.json({ plan, videoId });
  } catch (error) {
    console.error("Gemini analyze error:", error);

    if (error instanceof SyntaxError) {
      return NextResponse.json(
        { error: "AI 응답 파싱 실패. 다시 시도해주세요." },
        { status: 500 }
      );
    }

    return NextResponse.json(
      { error: "영상 분석 중 오류가 발생했습니다. 다시 시도해주세요." },
      { status: 500 }
    );
  }
}

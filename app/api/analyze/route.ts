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

// 타임스탬프를 [HH:MM:SS] 형식으로 변환
function formatTimestamp(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  return `[${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}]`;
}

// YouTube 자막 가져오기
async function fetchTranscript(videoId: string): Promise<string | null> {
  try {
    const transcript = await YoutubeTranscript.fetchTranscript(videoId, {
      lang: "ko",
    });
    if (!transcript || transcript.length === 0) {
      // 한국어 자막 없으면 기본 자막 시도
      const fallback = await YoutubeTranscript.fetchTranscript(videoId);
      if (!fallback || fallback.length === 0) return null;
      return fallback
        .map((t) => `${formatTimestamp(t.offset / 1000)} ${t.text}`)
        .join("\n");
    }
    return transcript
      .map((t) => `${formatTimestamp(t.offset / 1000)} ${t.text}`)
      .join("\n");
  } catch {
    return null;
  }
}

const SYSTEM_INSTRUCTION = `당신은 여행 유튜브 영상 분석 전문가입니다.
주어진 자막 또는 영상을 분석하고 여행자에게 실질적으로 도움이 되는 정보를 정확하게 추출합니다.

분석 원칙:
- 자막/영상에 실제로 언급된 정보만 추출하고, 없는 정보는 null로 표기합니다.
- 장소는 실제 구글 지도에서 찾을 수 있도록 위도/경도를 최대한 포함합니다.
- 가격은 자막/영상에서 언급된 원래 통화 단위로 표기합니다.
- 여행 타입과 태그는 콘텐츠를 분석하여 적절하게 분류합니다.
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
    "country": "여행 국가명 (한국어, 예: 태국)",
    "regions": ["여행한 지역/도시 목록 (한국어, 예: 치앙마이, 우돈타니)"],
    "type": "여행 타입 (맛집/쇼핑/문화/유적지/먹방/예술/패션/야경/액티비티/자연/힐링/배낭여행/럭셔리 중 영상에 맞는 것들, 쉼표 구분)",
    "tags": ["영상 관련 태그 (예: 한달살기, 물가, 현지음식, 미세먼지, 비자 등)"]
  },
  "travel_schedule": [
    {
      "day": 1,
      "category": "하루 전체를 요약하는 제목 (예: 치앙마이 미세먼지 원인 파악 및 우돈타니 이동)",
      "activities": [
        {
          "time_range": "영상 타임스탬프 (예: [00:00:00] - [00:05:54])",
          "location": "장소명 (도시/구역 포함, 한국어+현지어 병기)",
          "description": "해당 활동에 대한 구체적인 설명 (2~4문장)",
          "transportation": "이동 수단 및 요금 (없으면 null)",
          "accommodation": "숙소명 및 등급/가격 정보 (없으면 null)",
          "food": "먹은 음식 목록 및 간단한 설명 (없으면 null)",
          "price_info": {"항목명": "가격 (통화 포함)"} 또는 null,
          "coordinates": {"latitude": 위도숫자, "longitude": 경도숫자} 또는 null
        }
      ]
    }
  ],
  "travel_tips": {
    "precautions": "주의사항 (건강, 안전, 시기, 문화적 주의점 등)",
    "items": "추천 준비물 목록 (쉼표로 구분)",
    "total_expense": "영상 기준 예상 총 여행 경비 (기간 및 1인 기준 명시)",
    "useful_info": "유용한 현지 정보 (환율, 교통, 언어, 앱 등)"
  }
}

규칙:
- travel_schedule은 영상에 등장하는 날짜/시간순으로 구성하세요
- 영상에 정보가 없으면 null로 표기하세요
- price_info는 영상에 언급된 실제 가격만 포함하세요
- coordinates는 실제 장소의 위도/경도를 숫자로 입력하세요
- 반드시 유효한 JSON만 반환하세요`;
}

export async function POST(req: NextRequest) {
  try {
    const { url } = await req.json();

    if (!url || !url.includes("youtube")) {
      return NextResponse.json(
        { error: "유효한 YouTube URL을 입력해주세요." },
        { status: 400 },
      );
    }

    const videoId = extractVideoId(url);
    if (!videoId) {
      return NextResponse.json(
        { error: "YouTube 영상 ID를 찾을 수 없습니다." },
        { status: 400 },
      );
    }

    const db = createServerClient();

    // 캐시 확인: 이미 분석된 영상이면 DB에서 반환
    const { data: cached } = await db
      .from("plans")
      .select(
        "video_id, title, thumbnail_url, channel_name, summary, country, regions, trip_type, tags, travel_schedule, travel_tips",
      )
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

    // 자막 가져오기 시도
    const transcript = await fetchTranscript(videoId);
    console.log(transcript ? `자막 ${transcript.length}자 로드됨` : "자막 없음 → 영상 직접 분석");

    // Gemini 분석
    const parts = transcript
      ? [{ text: buildPrompt(videoId, transcript) }]
      : [
          { fileData: { fileUri: url, mimeType: "video/mp4" } },
          { text: buildPrompt(videoId, null) },
        ];

    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      config: {
        systemInstruction: SYSTEM_INSTRUCTION,
      },
      contents: [{ role: "user", parts }],
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
      { onConflict: "video_id" },
    );

    return NextResponse.json({ plan, videoId, transcriptUsed: !!transcript });
  } catch (error) {
    console.error("Gemini analyze error:", error);

    if (error instanceof SyntaxError) {
      return NextResponse.json(
        { error: "AI 응답 파싱 실패. 다시 시도해주세요." },
        { status: 500 },
      );
    }

    return NextResponse.json(
      { error: "영상 분석 중 오류가 발생했습니다. 다시 시도해주세요." },
      { status: 500 },
    );
  }
}

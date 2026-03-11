import { NextRequest, NextResponse } from "next/server";
import { createServerClient } from "@/lib/supabase";

// 외부에서 여행 계획을 등록하는 API
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { video_info, travel_schedule, travel_tips } = body;

    if (!video_info?.id) {
      return NextResponse.json(
        { error: "video_info.id는 필수입니다." },
        { status: 400 },
      );
    }

    const db = createServerClient();
    const { error } = await db.from("plans").upsert(
      {
        video_id: video_info.id,
        title: video_info?.title ?? null,
        thumbnail_url: video_info?.thumbnail_url ?? null,
        channel_name: video_info?.channel_name ?? null,
        summary: video_info?.summary ?? null,
        country: video_info?.country ?? null,
        regions: video_info?.regions ?? [],
        trip_type: video_info?.type ?? null,
        tags: video_info?.tags ?? [],
        travel_schedule: travel_schedule ?? [],
        travel_tips: travel_tips ?? {},
      },
      { onConflict: "video_id" },
    );

    if (error) {
      console.error("plans POST upsert error:", error);
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({ ok: true, video_id: video_info.id });
  } catch (error) {
    console.error("plans POST error:", error);
    return NextResponse.json({ error: "등록 실패" }, { status: 500 });
  }
}

import { NextRequest, NextResponse } from "next/server";
import { createServerClient } from "@/lib/supabase";

export async function PUT(
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const body = await req.json();
    const { video_info, travel_schedule, travel_tips } = body;

    const db = createServerClient();
    const { error } = await db.from("plans").upsert(
      {
        video_id: id,
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
      { onConflict: "video_id" }
    );

    if (error) {
      console.error("plans upsert error:", error);
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({ ok: true });
  } catch (error) {
    console.error("plans PUT error:", error);
    return NextResponse.json({ error: "저장 실패" }, { status: 500 });
  }
}

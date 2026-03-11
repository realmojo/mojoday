import { NextRequest, NextResponse } from "next/server";
import { createAuthServerClient } from "@/lib/supabase-auth-server";
import { createServerClient } from "@/lib/supabase";

// GET: 내 여행 일정 목록
export async function GET() {
  const supabase = await createAuthServerClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    return NextResponse.json({ error: "로그인이 필요합니다." }, { status: 401 });
  }

  const { data, error } = await supabase
    .from("my_plans")
    .select("id, title, thumbnail_url, channel_name, country, regions, trip_type, tags, travel_schedule, created_at, updated_at")
    .eq("user_id", user.id)
    .order("created_at", { ascending: false });

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json({ data });
}

// POST: 원본 플랜을 복사해서 내 일정으로 저장
export async function POST(req: NextRequest) {
  const supabase = await createAuthServerClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    return NextResponse.json({ error: "로그인이 필요합니다." }, { status: 401 });
  }

  const { video_id } = await req.json();
  if (!video_id) {
    return NextResponse.json({ error: "video_id가 필요합니다." }, { status: 400 });
  }

  // 원본 플랜 데이터 조회
  const db = createServerClient();
  const { data: original, error: fetchError } = await db
    .from("plans")
    .select("title, thumbnail_url, channel_name, summary, country, regions, trip_type, tags, travel_schedule, travel_tips, meta")
    .eq("video_id", video_id)
    .single();

  if (fetchError || !original) {
    return NextResponse.json({ error: "원본 플랜을 찾을 수 없습니다." }, { status: 404 });
  }

  // 완전한 복사본 생성
  const { data: created, error: insertError } = await supabase
    .from("my_plans")
    .insert({
      user_id: user.id,
      source_video_id: video_id,
      title: original.title,
      thumbnail_url: original.thumbnail_url,
      channel_name: original.channel_name,
      summary: original.summary,
      country: original.country,
      regions: original.regions,
      trip_type: original.trip_type,
      tags: original.tags,
      travel_schedule: original.travel_schedule,
      travel_tips: original.travel_tips,
      meta: original.meta ?? {},
    })
    .select("id")
    .single();

  if (insertError) {
    return NextResponse.json({ error: insertError.message }, { status: 500 });
  }

  return NextResponse.json({ ok: true, id: created.id });
}

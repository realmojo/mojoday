import { NextRequest, NextResponse } from "next/server";
import { createAuthServerClient } from "@/lib/supabase-auth-server";

type Params = { params: Promise<{ id: string }> };

// GET: 내 플랜 단건 조회
export async function GET(_req: NextRequest, { params }: Params) {
  const supabase = await createAuthServerClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    return NextResponse.json({ error: "로그인이 필요합니다." }, { status: 401 });
  }

  const { id } = await params;

  const { data, error } = await supabase
    .from("my_plans")
    .select("*")
    .eq("id", id)
    .eq("user_id", user.id)
    .single();

  if (error || !data) {
    return NextResponse.json({ error: "찾을 수 없습니다." }, { status: 404 });
  }

  return NextResponse.json({ data });
}

// PUT: 내 플랜 수정
export async function PUT(req: NextRequest, { params }: Params) {
  const supabase = await createAuthServerClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    return NextResponse.json({ error: "로그인이 필요합니다." }, { status: 401 });
  }

  const { id } = await params;
  const body = await req.json();
  const { video_info, travel_schedule, travel_tips } = body;

  const { error } = await supabase
    .from("my_plans")
    .update({
      title: video_info?.title,
      thumbnail_url: video_info?.thumbnail_url,
      channel_name: video_info?.channel_name,
      summary: video_info?.summary,
      country: video_info?.country,
      regions: video_info?.regions,
      trip_type: video_info?.type,
      tags: video_info?.tags,
      travel_schedule,
      travel_tips,
      meta: {
        trip_duration: video_info?.trip_duration,
        best_season: video_info?.best_season,
        budget_level: video_info?.budget_level,
        difficulty_level: video_info?.difficulty_level,
        travel_style: video_info?.travel_style,
        visa_info: video_info?.visa_info,
        currency: video_info?.currency,
        language: video_info?.language,
      },
      updated_at: new Date().toISOString(),
    })
    .eq("id", id)
    .eq("user_id", user.id);

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json({ ok: true });
}

// DELETE: 내 플랜 삭제
export async function DELETE(_req: NextRequest, { params }: Params) {
  const supabase = await createAuthServerClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    return NextResponse.json({ error: "로그인이 필요합니다." }, { status: 401 });
  }

  const { id } = await params;

  const { error } = await supabase
    .from("my_plans")
    .delete()
    .eq("id", id)
    .eq("user_id", user.id);

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json({ ok: true });
}

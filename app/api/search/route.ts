import { NextRequest, NextResponse } from "next/server";
import { createServerClient } from "@/lib/supabase";

/**
 * GET /api/search
 *
 * Query params (모두 optional):
 *   q        - 키워드 (FTS: title, summary, country, regions, tags, food, location, description)
 *   country  - 나라 정확 일치 (예: 일본)
 *   region   - 지역 포함 (예: 홋카이도)
 *   tag      - 태그 포함 (예: 이글루호텔)
 *   food     - 음식 키워드 (예: 스프카레)
 *   location - 장소 키워드 (예: 삿포로)
 *   type     - 여행 타입 포함 (예: 겨울)
 *   limit    - 결과 수 (기본 20, 최대 50)
 *   offset   - 페이지네이션 (기본 0)
 */
export async function GET(req: NextRequest) {
  const { searchParams } = req.nextUrl;

  const q        = searchParams.get("q")        || null;
  const country  = searchParams.get("country")  || null;
  const region   = searchParams.get("region")   || null;
  const tag      = searchParams.get("tag")      || null;
  const food     = searchParams.get("food")     || null;
  const location = searchParams.get("location") || null;
  const type     = searchParams.get("type")     || null;
  const limit    = Math.min(Number(searchParams.get("limit") || 20), 50);
  const offset   = Number(searchParams.get("offset") || 0);

  // 파라미터가 하나도 없으면 최신순 전체 반환
  if (!q && !country && !region && !tag && !food && !location && !type) {
    const db = createServerClient();
    const { data, error } = await db
      .from("plans")
      .select("video_id, title, thumbnail_url, channel_name, summary, country, regions, tags, trip_type, created_at")
      .order("created_at", { ascending: false })
      .range(offset, offset + limit - 1);

    if (error) return NextResponse.json({ error: error.message }, { status: 500 });
    return NextResponse.json({ results: data, total: data?.length ?? 0 });
  }

  const db = createServerClient();
  const { data, error } = await db.rpc("search_plans", {
    q,
    p_country:  country,
    p_region:   region,
    p_tag:      tag,
    p_food:     food,
    p_location: location,
    p_type:     type,
    p_limit:    limit,
    p_offset:   offset,
  });

  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ results: data, total: data?.length ?? 0 });
}

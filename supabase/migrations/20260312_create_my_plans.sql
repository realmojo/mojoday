-- 기존 user_plans 테이블 제거 (단순 참조였던 것)
drop table if exists user_plans;

-- my_plans: 사용자가 원본을 복사해서 자신만의 일정으로 관리하는 테이블
create table if not exists my_plans (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  source_video_id text,               -- 복사한 원본 video_id (참고용)
  title text,
  thumbnail_url text,
  channel_name text,
  summary text,
  country text,
  regions text[],
  trip_type text,
  tags text[],
  travel_schedule jsonb default '[]',
  travel_tips jsonb default '{}',
  meta jsonb default '{}',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table my_plans enable row level security;

create policy "Users can read own my_plans"
  on my_plans for select
  using (auth.uid() = user_id);

create policy "Users can insert own my_plans"
  on my_plans for insert
  with check (auth.uid() = user_id);

create policy "Users can update own my_plans"
  on my_plans for update
  using (auth.uid() = user_id);

create policy "Users can delete own my_plans"
  on my_plans for delete
  using (auth.uid() = user_id);

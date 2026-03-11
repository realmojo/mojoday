-- user_plans: 사용자가 저장한 여행 일정
create table if not exists user_plans (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  video_id text not null references plans(video_id) on delete cascade,
  created_at timestamptz not null default now(),
  unique(user_id, video_id)
);

alter table user_plans enable row level security;

create policy "Users can read own saved plans"
  on user_plans for select
  using (auth.uid() = user_id);

create policy "Users can insert own saved plans"
  on user_plans for insert
  with check (auth.uid() = user_id);

create policy "Users can delete own saved plans"
  on user_plans for delete
  using (auth.uid() = user_id);

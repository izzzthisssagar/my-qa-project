-- In-app feedback capture for QA Mastery
-- Run in Supabase SQL editor. Adds a feedback table tied to auth.users,
-- with Row Level Security so users only see/insert their own, and a
-- service-role-only read for your triage exports.
--
-- Mirrors your existing pattern: writes via authenticated client, sensitive
-- aggregation via service role. Keep it simple.

create table if not exists public.feedback (
  id          bigint generated always as identity primary key,
  created_at  timestamptz not null default now(),
  user_id     uuid references auth.users (id) on delete set null,
  -- context: where in the app were they when they submitted?
  context     text,                 -- e.g. 'lab:selenium-3', 'lesson:bug-reporting', 'general'
  type        text not null,        -- 'bug' | 'feature' | 'ux' | 'content' | 'pricing' | 'praise'
  message     text not null,
  -- optional structured fields the form can collect
  rating      smallint,             -- 1-5, nullable
  email       text,                 -- for non-logged-in fallback / follow-up consent
  -- triage fields (filled by you later, default null)
  theme       text,
  status      text not null default 'new',  -- new | triaged | planned | shipped | announced
  constraint feedback_type_check check (type in ('bug','feature','ux','content','pricing','praise')),
  constraint feedback_rating_check check (rating is null or (rating between 1 and 5))
);

create index if not exists feedback_status_idx on public.feedback (status);
create index if not exists feedback_type_idx   on public.feedback (type);
create index if not exists feedback_created_idx on public.feedback (created_at desc);

-- Row Level Security
alter table public.feedback enable row level security;

-- Anyone authenticated can submit feedback (their own user_id)
create policy "users insert own feedback"
  on public.feedback for insert
  to authenticated
  with check (auth.uid() = user_id);

-- Users can read only their own feedback
create policy "users read own feedback"
  on public.feedback for select
  to authenticated
  using (auth.uid() = user_id);

-- Optional: allow anonymous (logged-out) submissions from the public site.
-- Uncomment if your feedback widget appears before login. user_id will be null;
-- collect email instead for follow-up.
-- create policy "anon insert feedback"
--   on public.feedback for insert
--   to anon
--   with check (user_id is null);

-- NOTE: triage/export (reading ALL feedback) should use the service role key
-- inside a server action or your export script — it bypasses RLS. Never expose
-- the service role key to the client. Export to CSV in the shape of
-- feedback-intake.csv for the triage script.

-- Example export query (run as service role):
-- select id, created_at::date as date, 'in_app' as source, type, message as raw_text,
--        theme, status
-- from public.feedback order by created_at desc;

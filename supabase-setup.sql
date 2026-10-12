-- 224 Factory app: database setup. Run once in Supabase → SQL Editor → New query → Run.

-- People allowed to use the app. Only emails listed here can see or change factory data.
create table if not exists public.members (
  email text primary key,
  role text not null default 'member' check (role in ('owner','member')),
  created_at timestamptz not null default now()
);
insert into public.members (email, role) values ('hassangazzaz225@gmail.com','owner')
  on conflict (email) do update set role = 'owner';

create or replace function public.is_member() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.members where lower(email) = lower(coalesce(auth.jwt()->>'email','')));
$$;
create or replace function public.is_owner() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.members where lower(email) = lower(coalesce(auth.jwt()->>'email','')) and role = 'owner');
$$;

create table if not exists public.config (
  id int primary key default 1 check (id = 1),
  name text not null default '224 Factory',
  daily_target int not null default 50
);
insert into public.config (id) values (1) on conflict do nothing;

create table if not exists public.reports (
  day date primary key,
  finished int not null default 0,
  rejected int not null default 0,
  oven int not null default 0,
  wait_drill int not null default 0,
  wait_paint int not null default 0,
  wait_pack int not null default 0,
  note text default '',
  by_email text,
  updated_at timestamptz not null default now()
);

create table if not exists public.materials (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  unit text default '',
  qty numeric not null default 0,
  per_racket numeric not null default 0,
  lead_days int not null default 0,
  counted_day date not null default current_date,
  updated_at timestamptz not null default now()
);

create table if not exists public.molds (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  total int not null default 0,
  working int not null default 0,
  updated_at timestamptz not null default now()
);

alter table public.members   enable row level security;
alter table public.config    enable row level security;
alter table public.reports   enable row level security;
alter table public.materials enable row level security;
alter table public.molds     enable row level security;

drop policy if exists "members read" on public.members;
drop policy if exists "owner manages members" on public.members;
create policy "members read" on public.members for select to authenticated using (public.is_member());
create policy "owner manages members" on public.members for all to authenticated using (public.is_owner()) with check (public.is_owner());

drop policy if exists "members read config" on public.config;
drop policy if exists "owner edits config" on public.config;
create policy "members read config" on public.config for select to authenticated using (public.is_member());
create policy "owner edits config" on public.config for update to authenticated using (public.is_owner()) with check (public.is_owner());

do $$ declare t text; begin
  foreach t in array array['reports','materials','molds'] loop
    execute format('drop policy if exists "members full access" on public.%I', t);
    execute format('create policy "members full access" on public.%I for all to authenticated using (public.is_member()) with check (public.is_member())', t);
  end loop;
end $$;

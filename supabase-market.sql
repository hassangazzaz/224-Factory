-- 224 Factory app: adds your prices for the Market tab. Run once in Supabase → SQL Editor → New query → Run.
alter table public.config add column if not exists cost_sar numeric;
alter table public.config add column if not exists wholesale_sar numeric;
alter table public.config add column if not exists retail_sar numeric;
alter table public.config add column if not exists work_days int not null default 26;

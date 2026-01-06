-- Firecrawl Self-Hosted Supabase Setup Script
-- This script initializes the public schema with the required tables and RPCs
-- for a self-hosted Firecrawl instance using Supabase as the backend.

-- 1. Core Tables
CREATE TABLE IF NOT EXISTS teams (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS api_keys (
    id serial PRIMARY KEY,
    key text UNIQUE,
    team_id uuid REFERENCES teams(id),
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS requests (
    id uuid PRIMARY KEY,
    kind text,
    api_version text,
    team_id uuid,
    origin text,
    integration text,
    target_hint text,
    dr_clean_by timestamptz,
    api_key_id integer,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS scrapes (
    id uuid PRIMARY KEY,
    request_id uuid,
    url text,
    is_successful boolean,
    error text,
    time_taken numeric,
    team_id uuid,
    options jsonb,
    cost_tracking jsonb,
    pdf_num_pages integer,
    credits_cost integer,
    content text,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS crawls (
    id uuid PRIMARY KEY,
    request_id uuid,
    url text,
    team_id uuid,
    options jsonb,
    num_docs integer,
    credits_cost integer,
    cancelled boolean DEFAULT false,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS batch_scrapes (
    id uuid PRIMARY KEY,
    request_id uuid,
    team_id uuid,
    num_docs integer,
    credits_cost integer,
    cancelled boolean DEFAULT false,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS maps (
    id uuid PRIMARY KEY,
    request_id uuid,
    url text,
    team_id uuid,
    options jsonb,
    num_results integer,
    credits_cost integer,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS searches (
    id uuid PRIMARY KEY,
    request_id uuid,
    query text,
    team_id uuid,
    options jsonb,
    credits_cost integer,
    is_successful boolean,
    error text,
    num_results integer,
    time_taken integer,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS extracts (
    id uuid PRIMARY KEY,
    request_id uuid,
    urls text[],
    team_id uuid,
    options jsonb,
    model_kind text,
    credits_cost integer,
    is_successful boolean,
    error text,
    result jsonb,
    cost_tracking jsonb,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS llmstxts (
    id uuid PRIMARY KEY,
    request_id uuid,
    url text,
    team_id uuid,
    options jsonb,
    num_urls integer,
    credits_cost integer,
    cost_tracking jsonb,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS deep_researches (
    id uuid PRIMARY KEY,
    request_id uuid,
    query text,
    team_id uuid,
    options jsonb,
    time_taken integer,
    credits_cost integer,
    cost_tracking jsonb,
    created_at timestamptz DEFAULT now()
);

-- 2. Mock RPCs for Credit and Auth Management

CREATE OR REPLACE FUNCTION auth_credit_usage_chunk_38(
  input_key text,
  i_is_extract boolean,
  tally_untallied_credits boolean
)
RETURNS TABLE (
  api_key text,
  api_key_id int,
  team_id uuid,
  sub_id text,
  sub_current_period_start timestamptz,
  sub_current_period_end timestamptz,
  sub_user_id uuid,
  price_id text,
  price_credits bigint,
  price_should_be_graceful boolean,
  price_associated_auto_recharge_price_id text,
  credits_used bigint,
  coupon_credits bigint,
  adjusted_credits_used bigint,
  remaining_credits bigint,
  total_credits_sum bigint,
  plan_priority jsonb,
  rate_limits jsonb,
  concurrency int,
  flags jsonb
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    ak.key as api_key,
    ak.id as api_key_id,
    ak.team_id as team_id,
    'self-hosted'::text as sub_id,
    now() - interval '1 month' as sub_current_period_start,
    now() + interval '100 years' as sub_current_period_end,
    NULL::uuid as sub_user_id,
    'self-hosted-price'::text as price_id,
    999999999::bigint as price_credits,
    false as price_should_be_graceful,
    NULL::text as price_associated_auto_recharge_price_id,
    0::bigint as credits_used,
    0::bigint as coupon_credits,
    0::bigint as adjusted_credits_used,
    999999999::bigint as remaining_credits,
    999999999::bigint as total_credits_sum,
    '{"bucketLimit": 100, "planModifier": 1}'::jsonb as plan_priority,
    '{
      "crawl": 1000,
      "scrape": 1000,
      "search": 1000,
      "map": 1000,
      "extract": 1000,
      "preview": 1000,
      "crawlStatus": 1000,
      "extractStatus": 1000,
      "extractAgentPreview": 1000,
      "scrapeAgentPreview": 1000
    }'::jsonb as rate_limits,
    100 as concurrency,
    '{}'::jsonb as flags
  FROM api_keys ak
  WHERE ak.key = input_key;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION auth_credit_usage_chunk_38_from_team(
  input_team uuid,
  i_is_extract boolean,
  tally_untallied_credits boolean
)
RETURNS TABLE (
  api_key text,
  api_key_id int,
  team_id uuid,
  sub_id text,
  sub_current_period_start timestamptz,
  sub_current_period_end timestamptz,
  sub_user_id uuid,
  price_id text,
  price_credits bigint,
  price_should_be_graceful boolean,
  price_associated_auto_recharge_price_id text,
  credits_used bigint,
  coupon_credits bigint,
  adjusted_credits_used bigint,
  remaining_credits bigint,
  total_credits_sum bigint,
  plan_priority jsonb,
  rate_limits jsonb,
  concurrency int,
  flags jsonb
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    ak.key as api_key,
    ak.id as api_key_id,
    ak.team_id as team_id,
    'self-hosted'::text as sub_id,
    now() - interval '1 month' as sub_current_period_start,
    now() + interval '100 years' as sub_current_period_end,
    NULL::uuid as sub_user_id,
    'self-hosted-price'::text as price_id,
    999999999::bigint as price_credits,
    false as price_should_be_graceful,
    NULL::text as price_associated_auto_recharge_price_id,
    0::bigint as credits_used,
    0::bigint as coupon_credits,
    0::bigint as adjusted_credits_used,
    999999999::bigint as remaining_credits,
    999999999::bigint as total_credits_sum,
    '{"bucketLimit": 100, "planModifier": 1}'::jsonb as plan_priority,
    '{
      "crawl": 1000,
      "scrape": 1000,
      "search": 1000,
      "map": 1000,
      "extract": 1000,
      "preview": 1000,
      "crawlStatus": 1000,
      "extractStatus": 1000,
      "extractAgentPreview": 1000,
      "scrapeAgentPreview": 1000
    }'::jsonb as rate_limits,
    100 as concurrency,
    '{}'::jsonb as flags
  FROM api_keys ak
  WHERE ak.team_id = input_team
  LIMIT 1;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION bill_team_6(
  _team_id uuid,
  sub_id text,
  fetch_subscription boolean,
  credits bigint,
  i_api_key_id int,
  is_extract_param boolean
)
RETURNS TABLE (
  api_key text,
  api_key_id int,
  team_id uuid,
  sub_id_out text,
  sub_current_period_start timestamptz,
  sub_current_period_end timestamptz,
  sub_user_id uuid,
  price_id text,
  price_credits bigint,
  price_should_be_graceful boolean,
  price_associated_auto_recharge_price_id text,
  credits_used bigint,
  coupon_credits bigint,
  adjusted_credits_used bigint,
  remaining_credits bigint,
  total_credits_sum bigint,
  plan_priority jsonb,
  rate_limits jsonb,
  concurrency int,
  flags jsonb
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    ak.key as api_key,
    ak.id as api_key_id,
    ak.team_id as team_id,
    'self-hosted'::text as sub_id_out,
    now() - interval '1 month' as sub_current_period_start,
    now() + interval '100 years' as sub_current_period_end,
    NULL::uuid as sub_user_id,
    'self-hosted-price'::text as price_id,
    999999999::bigint as price_credits,
    false as price_should_be_graceful,
    NULL::text as price_associated_auto_recharge_price_id,
    0::bigint as credits_used,
    0::bigint as coupon_credits,
    0::bigint as adjusted_credits_used,
    999999999::bigint as remaining_credits,
    999999999::bigint as total_credits_sum,
    '{"bucketLimit": 100, "planModifier": 1}'::jsonb as plan_priority,
    '{
      "crawl": 1000,
      "scrape": 1000,
      "search": 1000,
      "map": 1000,
      "extract": 1000,
      "preview": 1000,
      "crawlStatus": 1000,
      "extractStatus": 1000,
      "extractAgentPreview": 1000,
      "scrapeAgentPreview": 1000
    }'::jsonb as rate_limits,
    100 as concurrency,
    '{}'::jsonb as flags
  FROM api_keys ak
  WHERE ak.team_id = _team_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION update_tally_7_team(
  i_team_id uuid
)
RETURNS void AS $$
BEGIN
  -- No-op for self-hosted
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION change_tracking_insert_scrape(
  p_team_id uuid,
  p_url text,
  p_job_id uuid,
  p_change_tracking_tag text,
  p_date_added timestamptz
)
RETURNS void AS $$
BEGIN
  -- No-op
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

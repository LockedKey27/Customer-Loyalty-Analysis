-- ── QUERY 1: Core KPI Dashboard ──────────────────────────────
-- Business question: What is the overall health of the customer base?
SELECT
    COUNT(*)                                          AS total_customers,
    ROUND(AVG(revenue), 2)                            AS avg_order_value,
    SUM(revenue)                                      AS total_revenue,
    ROUND(AVG(previous_purchases), 1)                 AS avg_purchase_depth,
    ROUND(SUM(CASE WHEN promo_flag = 1 THEN 1 ELSE 0 END) * 100.0
          / COUNT(*), 1)                              AS promo_rate_pct,
    ROUND(SUM(CASE WHEN subscription_flag = 1 THEN 1 ELSE 0 END) * 100.0
          / COUNT(*), 1)                              AS subscriber_rate_pct
FROM customer_segments;

-- ── QUERY 2: Promo Revenue Share (PRS) ───────────────────────
-- Business question: What % of revenue requires a discount to happen?
SELECT
    promo_code_used                                   AS promo_used,
    COUNT(*)                                          AS customer_count,
    SUM(revenue)                                      AS total_revenue,
    ROUND(SUM(revenue) * 100.0 /
          SUM(SUM(revenue)) OVER(), 1)                AS revenue_share_pct,
    ROUND(AVG(revenue), 2)                            AS avg_revenue
FROM customer_segments
GROUP BY promo_code_used
ORDER BY promo_code_used DESC;

-- ── QUERY 3: Segment Performance Summary ─────────────────────
-- Business question: Which segments drive value vs risk?
SELECT
    segment,
    COUNT(*)                                          AS customer_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS share_pct,
    ROUND(AVG(revenue), 2)                            AS avg_revenue,
    ROUND(AVG(previous_purchases), 1)                 AS avg_purchases,
    ROUND(AVG(promo_flag) * 100, 1)                   AS promo_rate_pct,
    ROUND(AVG(review_rating), 2)                      AS avg_rating,
    ROUND(AVG(loyalty_score), 2)                      AS avg_loyalty_score
FROM customer_segments
GROUP BY segment
ORDER BY segment;

-- ── QUERY 4: Category Retention Index ────────────────────────
-- Business question: Which product categories build loyal customers?
SELECT
    category,
    COUNT(*)                                          AS customers,
    ROUND(AVG(previous_purchases), 1)                 AS avg_purchase_depth,
    ROUND(AVG(promo_flag) * 100, 1)                   AS promo_rate_pct,
    ROUND(AVG(revenue), 2)                            AS avg_revenue,
    ROUND(AVG(review_rating), 2)                      AS avg_rating,
    SUM(CASE WHEN segment = '1_Genuinely_Loyal'
             THEN 1 ELSE 0 END)                       AS loyal_customers,
    ROUND(SUM(CASE WHEN segment = '1_Genuinely_Loyal'
             THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS loyal_pct
FROM customer_segments
GROUP BY category
ORDER BY loyal_pct DESC;

-- ── QUERY 5: Regional Organic Demand Analysis ────────────────
-- Business question: Which states show highest organic (non-promo) demand?
SELECT
    location                                          AS state,
    COUNT(*)                                          AS total_customers,
    SUM(CASE WHEN promo_flag = 0 THEN 1 ELSE 0 END)  AS organic_customers,
    ROUND(SUM(CASE WHEN promo_flag = 0 THEN 1 ELSE 0 END) * 100.0
          / COUNT(*), 1)                              AS organic_rate_pct,
    ROUND(AVG(revenue), 2)                            AS avg_revenue,
    ROUND(AVG(previous_purchases), 1)                 AS avg_purchase_depth
FROM customer_segments
GROUP BY location
HAVING COUNT(*) >= 50
ORDER BY organic_rate_pct DESC
LIMIT 10;

-- ── QUERY 6: Subscription Programme Audit ────────────────────
-- Business question: Is the subscription programme a loyalty tool or a discount vehicle?
SELECT
    subscription_status,
    COUNT(*)                                          AS customers,
    ROUND(AVG(promo_flag) * 100, 1)                   AS promo_rate_pct,
    ROUND(AVG(previous_purchases), 1)                 AS avg_purchases,
    ROUND(AVG(revenue), 2)                            AS avg_revenue,
    ROUND(AVG(loyalty_score), 2)                      AS avg_loyalty_score,
    ROUND(AVG(review_rating), 2)                      AS avg_rating
FROM customer_segments
GROUP BY subscription_status;

-- ── QUERY 7: Promo Dependency by Purchase Depth ──────────────
-- Business question: Does promo dependency increase or decrease as customers mature?
SELECT
    CASE
        WHEN previous_purchases BETWEEN 1  AND 5  THEN '1. New (1-5)'
        WHEN previous_purchases BETWEEN 6  AND 15 THEN '2. Developing (6-15)'
        WHEN previous_purchases BETWEEN 16 AND 30 THEN '3. Established (16-30)'
        WHEN previous_purchases BETWEEN 31 AND 50 THEN '4. Loyal (31-50)'
    END                                               AS loyalty_band,
    COUNT(*)                                          AS customers,
    ROUND(AVG(promo_flag) * 100, 1)                   AS promo_rate_pct,
    ROUND(AVG(revenue), 2)                            AS avg_revenue,
    ROUND(AVG(loyalty_score), 2)                      AS avg_loyalty_score
FROM customer_segments
GROUP BY loyalty_band
ORDER BY loyalty_band;

-- ── QUERY 8: High-Value Organic Customer Profile ─────────────
-- Business question: What does our ideal customer look like?
SELECT
    gender,
    ROUND(AVG(age), 1)                                AS avg_age,
    category                                          AS top_category,
    ROUND(AVG(revenue), 2)                            AS avg_revenue,
    ROUND(AVG(previous_purchases), 1)                 AS avg_purchases,
    COUNT(*)                                          AS customer_count,
    ROUND(AVG(review_rating), 2)                      AS avg_rating
FROM customer_segments
WHERE segment = '1_Genuinely_Loyal'
GROUP BY gender, category
ORDER BY avg_purchases DESC;
# Executive Summary
## Decoding Customer Value: A SQL-Driven Retention Strategy
### D2C Fashion Brand — Customer Loyalty Analysis

---

## Business Question

Is the business building a truly loyal customer base, or is it dependent on continuous promotions and discounts?

---

## Answer

**The business is not building genuine loyalty. It is renting customer behaviour through discounts.**

43% of all revenue requires a discount to be earned. The subscription programme — designed to drive loyalty — has a 100% promotional usage rate and produces below-average loyalty scores. Most critically, promo dependency increases as customers mature, meaning the brand's longest-standing customers have been trained to wait for discounts rather than buy at full price.

A genuine loyal core of 826 customers (21.2%) does exist — they buy consistently, never use promotions, and have 38 average previous purchases. But current strategy is not replicating this profile. It is doing the opposite.

---

## Key Metrics

| KPI | Value | Implication |
|---|---|---|
| Total Revenue | $233,081 | Baseline for ROI calculations |
| Avg Order Value | $59.76 | Consistent across all segments |
| Promo Revenue Share | 42.7% | Nearly half of revenue is discount-dependent |
| Organic AOV vs Promo AOV | $60.13 vs $59.28 | $0.85 gap — discounts protect no revenue |
| Subscriber promo rate | 100% | Programme is a discount vehicle |
| Genuinely Loyal customers | 826 (21.2%) | Core to protect and replicate |
| Promo rate — Loyal band | 43.9% | Highest of any band — loyalty programme is failing |

---

## Customer Segmentation

Five segments were identified using a composite loyalty score built from purchase depth, frequency, organic behaviour, satisfaction, and subscription status.

**Genuinely Loyal (21.2%)** — 826 customers with 38 average purchases, zero promo usage, and the highest loyalty score (3.93). These customers represent the brand's most sustainable revenue stream and require VIP recognition before they are lost to competitors.

**Promo Dependent (27.3%)** — 1,064 customers with deep purchase history (34.9 avg) but 100% promo rate. These customers know the brand but have been conditioned to only buy on discount. High churn risk if promotions are reduced without a transition strategy.

**Organic Developing (13.8%)** — 538 customers buying without discounts at 25 average purchases. The highest-ROI conversion opportunity. These customers demonstrate intrinsic brand affinity and need relationship investment, not price incentives, to reach the Loyal tier.

**At Risk New (10.6%)** — 412 new customers already using promotions at a 41.3% rate. The acquisition funnel is establishing discount expectations from the first purchase.

**Occasional Buyer (27.2%)** — 1,060 mid-frequency customers with mixed promo behaviour. Lowest loyalty scores. Require targeted engagement to prevent further disengagement.

---

## Critical Finding — Subscription Programme

The subscription programme is the most significant structural problem identified. Subscribers have:
- 100% promo rate (vs 21.9% for non-subscribers)
- Lower loyalty score: 2.42 vs 3.00
- Lower average revenue: $59.49 vs $59.87
- Marginally higher purchase depth: 26.1 vs 25.1

The programme is achieving the opposite of its purpose. It is functioning as a permanent discount entitlement rather than a loyalty incentive, while delivering below-average revenue per transaction.

---

## Strategic Recommendations

**Priority 1 — Redesign the subscription programme**
Replace blanket discounts with tiered benefits: early product access, free shipping thresholds, personalised category recommendations, and loyalty points. Measure impact on promo rate and loyalty score at 90-day intervals.

**Priority 2 — Invest in Organic Developing segment**
538 customers are one relationship investment away from becoming Genuinely Loyal. Launch a personalised cross-category recommendation programme targeting this group. Expected outcome: 15–20% conversion to Loyal tier within 6 months.

**Priority 3 — Regional promo reduction pilot**
Begin reducing promotional spend in Kansas (76.2% organic), Arizona (66.2%), and Connecticut (66.7%) — markets with demonstrated organic demand. Measure revenue impact over 60 days before rolling out nationally.

**Priority 4 — Fix new customer acquisition**
40.1% of new customers arrive via promo. Introduce at least one full-price acquisition channel (content marketing, referral programme, influencer partnerships) and track 90-day repeat purchase rate without discount.

**Priority 5 — Protect Genuinely Loyal customers**
Create a VIP tier with non-monetary benefits (exclusive previews, styling consultations, community access). These 826 customers represent the brand's most valuable long-term asset and currently receive no differentiated treatment.

---

## Business Trade-offs

Reducing promo dependency carries short-term revenue risk. The $99,411 currently generated through promotional orders cannot be eliminated overnight. A phased approach — piloting in high-organic regions, transitioning subscribers to value-based benefits, and converting Organic Developing customers — reduces this risk while building sustainable revenue over 12–18 months.

---

*Analysis based on 3,900 customer records across 4 product categories and 50 US states.*
*Methodology: Python (pandas), SQL (SQLite), Power BI. Loyalty score engineered from 5 behavioural signals.*

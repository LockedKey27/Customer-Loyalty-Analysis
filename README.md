# Customer Loyalty Analysis — D2C Fashion Brand

I built this project to answer one question a D2C brand's leadership team would actually care about: **are our repeat customers loyal, or are they just waiting for the next sale?**

The dataset has 3,900 customers, no timestamps, and no loyalty score. So the first real challenge was figuring out how to define loyalty from what I actually had — purchase depth, frequency, whether they ever bought without a discount, satisfaction, and subscription status. That became the foundation for everything else.

--

## What I found

The short answer: the brand has a discount dependency problem, and its own subscription programme is making it worse.

- **43% of all revenue requires a discount to happen.** Not because customers are price-sensitive — organic and promo buyers spend almost the same amount per transaction ($60.13 vs $59.28). The business is giving away margin for no measurable revenue upside.

- **The subscription programme has a 100% promo rate.** Every single subscriber used a discount. Non-subscribers? 21.9%. The programme designed to build loyalty is the most discount-dependent group in the entire customer base, and they have *lower* loyalty scores than non-subscribers.

- **Promo dependency increases as customers get older.** New customers have a 40.1% promo rate. The most loyal band (31–50 previous purchases) has a 43.9% promo rate. The brand has trained its best customers to wait for sales.

- **There is a genuine loyal core — 826 customers (21.2%) — who buy consistently, never use promos, and have 38 average previous purchases.** Current strategy isn't building more customers like them. It's doing the opposite.

---

## The five segments I built

Since there was no loyalty score in the data, I engineered one from five behavioural signals: purchase depth (40%), frequency (25%), whether they bought organically (20%), review rating (10%), and subscription status (5%). That produced five segments:

| Segment | Size | Promo Rate | Avg Purchases | What it means |
|---|---|---|---|---|
| Genuinely Loyal | 826 (21.2%) | 0% | 38.4 | The brand's best customers — ignored by current strategy |
| Promo Dependent | 1,064 (27.3%) | 100% | 34.9 | Deep history, fully conditioned to discount |
| Organic Developing | 538 (13.8%) | 0% | 25.3 | Highest ROI conversion opportunity |
| At Risk New | 412 (10.6%) | 41.3% | 3.1 | Already arriving via promo — bad sign |
| Occasional Buyer | 1,060 (27.2%) | 41.8% | 14.3 | Mid-frequency, disengaging |

---

## What I'd actually recommend

**Fix the subscription programme first.** It's supposed to drive loyalty but it's functioning as a permanent discount entitlement. The fix isn't complicated — replace blanket discounts with early access, free shipping thresholds, and personalised recommendations. Measure promo rate and loyalty score at 90-day intervals.

**Invest in Organic Developing customers before doing anything else.** 538 people are already buying without discounts. They just need a reason to buy more often. Cross-category recommendations, personalised outreach — nothing price-based. These are the easiest conversions in the entire customer base.

**Pilot promo reduction in high-organic states.** Kansas (76.2% organic rate), Arizona (66.2%), Connecticut (66.7%) — these markets are already buying without needing a discount. Start pulling back promotional spend there and measure 60-day revenue impact before doing anything nationally.

---

## How I built it

**Python** — cleaned the data, ran EDA, engineered the loyalty score, built the segments. I used pandas for everything and matplotlib/seaborn for the charts.

**SQL** — wrote 8 queries in SQLite to answer the core business questions: promo revenue share, segment performance, category retention index, regional organic demand, subscription programme audit, and promo dependency by purchase depth.

**Power BI** — 4-page dashboard covering executive overview, segmentation deep dive, promo dependency analysis, and regional/category breakdown.

---

## Files in this repo

| File | What it is |
|---|---|
| `analysis.py` | Data cleaning and EDA — 6 charts |
| `feature_engineering.py` | Loyalty scoring and segmentation logic |
| `queries.sql` | 8 SQL queries with business context comments |
| `customer_segments.csv` | Final segmented dataset — feeds the dashboard |
| `Executive_Summary.md` | Full findings and recommendations write-up |
| `charts/` | All EDA and segmentation visuals |

Power BI dashboard (.pbix) available on request.

---

## A note on methodology

This dataset has no order dates — every row is one customer snapshot, not a transaction log. That meant I couldn't do traditional cohort analysis or time-series RFM. So I adapted: `previous_purchases` became my purchase depth proxy, `frequency_of_purchases` became my engagement signal, and the cross-sectional data still allowed meaningful segmentation. It just captures a moment in time rather than tracking change.

The loyalty score weights are assumption-based. In a real setting I'd validate them against actual retention outcomes — ideally 90-day repurchase rates — and adjust accordingly.

---

*Tools: Python (pandas, matplotlib, seaborn) · SQL (SQLite / DB Browser) · Power BI*

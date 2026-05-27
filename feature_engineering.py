import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv('Dataset.csv')

# ── Clean ─────────────────────────────────────────────────────────────────
df.columns = df.columns.str.strip().str.lower()\
               .str.replace(' ', '_')\
               .str.replace('(', '').str.replace(')', '')
df = df.rename(columns={'purchase_amount_usd': 'revenue'})
df['promo_flag']        = (df['promo_code_used'] == 'Yes').astype(int)
df['subscription_flag'] = (df['subscription_status'] == 'Yes').astype(int)
df = df.drop(columns=['discount_applied'])
freq_map = {'Weekly':7,'Fortnightly':14,'Bi-Weekly':14,
            'Monthly':30,'Every 3 Months':90,'Quarterly':90,'Annually':365}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(freq_map)
df['review_rating'] = df.groupby('category')['review_rating']\
                        .transform(lambda x: x.fillna(x.median()))

os.makedirs('charts', exist_ok=True)

# ── FEATURE ENGINEERING ───────────────────────────────────────────────────

# 1. Purchase Depth Score (how many times they've bought — most important)
df['depth_score'] = pd.qcut(df['previous_purchases'],
                             q=5, labels=[1,2,3,4,5]).astype(int)

# 2. Frequency Score (how often — lower days = higher score)
freq_score_map = {7:5, 14:4, 30:3, 90:2, 365:1}
df['freq_score'] = df['purchase_frequency_days'].map(freq_score_map)

# 3. Organic Score (did they buy without a promo?)
df['organic_score'] = (1 - df['promo_flag']) * 5

# 4. Satisfaction Score (review rating normalised)
df['sat_score'] = pd.qcut(df['review_rating'],
                           q=5, labels=[1,2,3,4,5]).astype(int)

# 5. Subscription Score
df['sub_score'] = df['subscription_flag'] * 3

# ── COMPOSITE LOYALTY SCORE ───────────────────────────────────────────────
df['loyalty_score'] = (
    df['depth_score']   * 0.40 +
    df['freq_score']    * 0.25 +
    df['organic_score'] * 0.20 +
    df['sat_score']     * 0.10 +
    df['sub_score']     * 0.05
)

# ── SEGMENT CLASSIFICATION ────────────────────────────────────────────────
def assign_segment(row):
    if row['loyalty_score'] >= 3.5 and row['promo_flag'] == 0:
        return '1_Genuinely_Loyal'
    elif row['promo_flag'] == 1 and row['previous_purchases'] >= 20:
        return '2_Promo_Dependent'
    elif row['loyalty_score'] >= 3.0 and row['promo_flag'] == 0:
        return '3_Organic_Developing'
    elif row['previous_purchases'] <= 5:
        return '4_At_Risk_New'
    else:
        return '5_Occasional_Buyer'

df['segment'] = df.apply(assign_segment, axis=1)

# ── CHART 7: Loyalty Score Distribution ──────────────────────────────────
plt.figure(figsize=(10,5))
sns.histplot(df['loyalty_score'], bins=30, color='#1565C0', edgecolor='white')
plt.axvline(df['loyalty_score'].mean(), color='red',
            linestyle='--', label=f"Mean: {df['loyalty_score'].mean():.2f}")
plt.title('Customer Loyalty Score Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Loyalty Score')
plt.ylabel('Number of Customers')
plt.legend()
plt.tight_layout()
plt.savefig('charts/07_loyalty_score_distribution.png', dpi=150)
plt.close()

# ── CHART 8: Segment Sizes ────────────────────────────────────────────────
seg_counts = df['segment'].value_counts().sort_index()
clean_labels = [s.split('_',1)[1].replace('_',' ') for s in seg_counts.index]
colors = ['#43A047','#E53935','#FB8C00','#EF5350','#90A4AE']
plt.figure(figsize=(10,5))
bars = plt.bar(clean_labels, seg_counts.values, color=colors)
plt.title('Customer Segment Sizes', fontsize=14, fontweight='bold')
plt.ylabel('Number of Customers')
for bar, val in zip(bars, seg_counts.values):
    pct = val/len(df)*100
    plt.text(bar.get_x()+bar.get_width()/2, bar.get_height()+10,
             f'{val:,}\n({pct:.1f}%)', ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('charts/08_customer_segments.png', dpi=150)
plt.close()

# ── CHART 9: Segment Revenue Profile ─────────────────────────────────────
seg_profile = df.groupby('segment').agg(
    avg_revenue   =('revenue','mean'),
    avg_purchases =('previous_purchases','mean'),
    promo_rate    =('promo_flag','mean')
).round(2)
seg_profile.index = [s.split('_',1)[1].replace('_',' ')
                     for s in seg_profile.index]

fig, axes = plt.subplots(1, 3, figsize=(15,5))
fig.suptitle('Segment Revenue & Behaviour Profile', fontsize=14, fontweight='bold')
metrics = ['avg_revenue','avg_purchases','promo_rate']
titles  = ['Avg Revenue ($)','Avg Previous Purchases','Promo Rate']
for ax, metric, title in zip(axes, metrics, titles):
    ax.bar(seg_profile.index, seg_profile[metric],
           color=['#43A047','#E53935','#FB8C00','#EF5350','#90A4AE'])
    ax.set_title(title, fontweight='bold')
    ax.set_xticklabels(seg_profile.index, rotation=20, ha='right', fontsize=8)
plt.tight_layout()
plt.savefig('charts/09_segment_profiles.png', dpi=150)
plt.close()

# ── PRINT SEGMENT SUMMARY ─────────────────────────────────────────────────
print("=" * 60)
print("   FEATURE ENGINEERING + SEGMENTATION COMPLETE")
print("=" * 60)
print(f"\nLoyalty Score — Mean: {df['loyalty_score'].mean():.2f} "
      f"| Min: {df['loyalty_score'].min():.2f} "
      f"| Max: {df['loyalty_score'].max():.2f}\n")
print("SEGMENT BREAKDOWN:")
print("-" * 60)
for seg in sorted(df['segment'].unique()):
    sub = df[df['segment']==seg]
    label = seg.split('_',1)[1].replace('_',' ')
    print(f"\n  {label}")
    print(f"    Count:            {len(sub):,} ({len(sub)/len(df)*100:.1f}%)")
    print(f"    Avg Revenue:      ${sub['revenue'].mean():.2f}")
    print(f"    Avg Purchases:    {sub['previous_purchases'].mean():.1f}")
    print(f"    Promo Rate:       {sub['promo_flag'].mean()*100:.1f}%")
    print(f"    Avg Rating:       {sub['review_rating'].mean():.2f}")

df.to_csv('customer_segments.csv', index=False)
print("\n\nSegmented dataset saved to: customer_segments.csv")
print("3 new charts saved to: charts/")
print("Ready for Phase 5 — SQL Queries")
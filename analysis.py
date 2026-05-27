import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ── Load data ────────────────────────────────────────────────────────────────
df = pd.read_csv('Dataset.csv')

# ── Clean ────────────────────────────────────────────────────────────────────
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

# ── Chart 1: Revenue distribution ────────────────────────────────────────────
plt.figure(figsize=(10, 5))
sns.histplot(df['revenue'], bins=30, color='steelblue', edgecolor='white')
plt.title('Revenue Distribution per Transaction', fontsize=14, fontweight='bold')
plt.xlabel('Revenue (USD)')
plt.ylabel('Number of Customers')
plt.tight_layout()
plt.savefig('charts/01_revenue_distribution.png', dpi=150)
plt.close()

# ── Chart 2: Promo vs Organic revenue ────────────────────────────────────────
promo_rev = df.groupby('promo_code_used')['revenue'].mean().reset_index()
promo_rev.columns = ['Promo Used', 'Avg Revenue']
plt.figure(figsize=(7, 5))
colors = ['#2196F3', '#FF7043']
bars = plt.bar(promo_rev['Promo Used'], promo_rev['Avg Revenue'], color=colors, width=0.5)
plt.title('Avg Revenue: Promo vs Organic Purchases', fontsize=14, fontweight='bold')
plt.ylabel('Average Revenue (USD)')
for bar, val in zip(bars, promo_rev['Avg Revenue']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f'${val:.2f}', ha='center', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/02_promo_vs_organic_aov.png', dpi=150)
plt.close()

# ── Chart 3: Category revenue share ──────────────────────────────────────────
cat_rev = df.groupby('category')['revenue'].sum().sort_values(ascending=False)
plt.figure(figsize=(8, 5))
bars = plt.bar(cat_rev.index, cat_rev.values,
               color=['#1565C0','#1976D2','#42A5F5','#90CAF9'])
plt.title('Total Revenue by Category', fontsize=14, fontweight='bold')
plt.ylabel('Total Revenue (USD)')
for bar, val in zip(bars, cat_rev.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
             f'${val:,.0f}', ha='center', fontsize=11)
plt.tight_layout()
plt.savefig('charts/03_revenue_by_category.png', dpi=150)
plt.close()

# ── Chart 4: Promo rate by category ──────────────────────────────────────────
cat_promo = df.groupby('category')['promo_flag'].mean().sort_values(ascending=False)
plt.figure(figsize=(8, 5))
bars = plt.bar(cat_promo.index, cat_promo.values * 100,
               color=['#E53935','#EF5350','#EF9A9A','#FFCDD2'])
plt.title('Promo Dependency Rate by Category', fontsize=14, fontweight='bold')
plt.ylabel('% Orders with Promo')
plt.ylim(0, 60)
for bar, val in zip(bars, cat_promo.values * 100):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f'{val:.1f}%', ha='center', fontsize=11)
plt.tight_layout()
plt.savefig('charts/04_promo_rate_by_category.png', dpi=150)
plt.close()

# ── Chart 5: Subscription vs non-subscription ────────────────────────────────
sub = df.groupby('subscription_status').agg(
    avg_revenue=('revenue','mean'),
    avg_prev_purchases=('previous_purchases','mean'),
    promo_rate=('promo_flag','mean')
).round(2)
fig, axes = plt.subplots(1, 3, figsize=(14, 5))
fig.suptitle('Subscriber vs Non-Subscriber Profile', fontsize=14, fontweight='bold')
metrics = ['avg_revenue', 'avg_prev_purchases', 'promo_rate']
titles  = ['Avg Revenue ($)', 'Avg Previous Purchases', 'Promo Rate']
colors_list = [['#43A047','#E53935'],['#43A047','#E53935'],['#43A047','#E53935']]
for ax, metric, title, cols in zip(axes, metrics, titles, colors_list):
    vals = sub[metric]
    bars = ax.bar(vals.index, vals.values, color=cols, width=0.5)
    ax.set_title(title, fontweight='bold')
    for bar, val in zip(bars, vals.values):
        label = f'${val:.2f}' if 'revenue' in metric else f'{val:.2f}'
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() * 0.5, label,
                ha='center', color='white', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/05_subscriber_profile.png', dpi=150)
plt.close()

# ── Chart 6: Previous purchases distribution ─────────────────────────────────
bins   = [0, 5, 15, 30, 50]
labels = ['New\n(1-5)', 'Developing\n(6-15)', 'Established\n(16-30)', 'Loyal\n(31-50)']
df['loyalty_band'] = pd.cut(df['previous_purchases'],
                             bins=bins, labels=labels, include_lowest=True)
band_counts = df['loyalty_band'].value_counts().sort_index()
plt.figure(figsize=(9, 5))
bars = plt.bar(band_counts.index, band_counts.values,
               color=['#EF5350','#FFA726','#66BB6A','#1E88E5'])
plt.title('Customer Loyalty Bands (by Previous Purchases)', fontsize=14, fontweight='bold')
plt.ylabel('Number of Customers')
for bar, val in zip(bars, band_counts.values):
    pct = val / len(df) * 100
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
             f'{val:,}\n({pct:.1f}%)', ha='center', fontsize=11)
plt.tight_layout()
plt.savefig('charts/06_loyalty_bands.png', dpi=150)
plt.close()

# ── Print summary ─────────────────────────────────────────────────────────────
print("=" * 55)
print("   EDA COMPLETE — 6 charts saved to /charts folder")
print("=" * 55)
print(f"\nDataset:          {len(df):,} customers")
print(f"Total Revenue:    ${df['revenue'].sum():,.0f}")
print(f"Avg Order Value:  ${df['revenue'].mean():.2f}")
print(f"Promo Rate:       {df['promo_flag'].mean()*100:.1f}%")
print(f"Subscriber Rate:  {df['subscription_flag'].mean()*100:.1f}%")
print(f"\nLoyalty Band Breakdown:")
for band, count in band_counts.items():
    print(f"  {str(band):<22} {count:>5,}  ({count/len(df)*100:.1f}%)")
print(f"\n6 charts saved to: charts/")
print("Ready for Phase 3 — Feature Engineering")
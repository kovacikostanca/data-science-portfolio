# CustomerLens: Business Insights and Recommendations

Based on 93,357 customers with at least one delivered order on the Olist marketplace. All amounts are in Brazilian reais (R$). Source: `customer_rfm_final` and the CustomerLens Power BI dashboard.

---

## The 30-second summary

1. **Olist is a one-time-purchase marketplace.** 97.0% of customers bought once, and only 3.0% are repeat buyers.
2. **Three segments hold almost everything.** New Customers, Hibernating and Potential Loyalists are 98.7% of customers and about 97.5% of the R$ 15.42M revenue.
3. **Repeat buyers are worth much more.** Spend per customer rises from about R$ 164 (one order) to R$ 285 (two orders) and R$ 874 (Champions).
4. **The base has mostly gone quiet.** Average recency is 238 days, and a large share of customers have not bought for more than six months.
5. **The best lever is the second purchase**, not rewarding a tiny loyal core.

---

## Insights by dashboard page

### Page 1: Executive Overview

| Insight | Evidence | So what |
|---|---|---|
| Revenue depends on one-time buyers | R$ 15.42M total; New 38.5%, Hibernating 38.1%, Potential Loyalists 20.9% of revenue | The business grows by acquiring customers, so retention is untapped. |
| Repeat rate is very low | 3.0% of customers have 2+ orders; 90,556 customers have exactly one | Even a small lift in repeat rate matters in absolute terms. |
| The customer base is aging | Average recency 238 days; recency chart is concentrated in the 91-180, 181-365 and 365+ day buckets | Campaigns should be time-sensitive, because older customers are harder to win back. |
| Average customer value is modest | R$ 165.20 per customer | Acquisition cost must stay well below this figure to be profitable. |
| Champions are rare but very valuable | 32 customers at about R$ 874 average spend, about 5 times the average | Treat them individually, but do not build the strategy around them. |

### Page 2: RFM Segmentation

| Insight | Evidence | So what |
|---|---|---|
| The one-time segments differ only by timing | New: 91 days; Potential Loyalists: 213 days; Hibernating: 395 days, all about 1.0 order and about R$ 162-164 | Time since purchase decides the action: act on New now, nurture Potential Loyalists, run cheap reactivation on Hibernating. |
| At Risk is the best recoverable pool | 922 customers, 2 orders, R$ 285 average spend, 382 days since last order | Highest value per customer among the groups that can still be saved. A win-back offer is justified here. |
| Spend rises with frequency | R$ 164 (1 order) → R$ 285 (2) → R$ 424-460 (3 orders) → R$ 874 (about 5) | Every extra order signals a more valuable customer, which supports investing in the second purchase. |
| R and M scores are even by design, F is skewed by the data | R and M donuts show 20% per score; F shows 97% in score 1 | The F chart is the one-time-buyer story in one picture, and the R and M charts only confirm the scoring works. |

### Page 3: Customer Explorer and Action Center

| Insight | Evidence | So what |
|---|---|---|
| Segments translate directly into actions | The action table gives each segment a meaning and next step | Marketing can export a segment and launch a campaign without further analysis. |
| Targeting can be sharper than segments alone | Filters on segment and R, F, M scores narrow the list | For example, At Risk with a high M score is the first call list. |
| Single-customer view supports service teams | The selected-customer card shows orders, spend and days since last purchase | Account managers can check a customer's value before reaching out. |

---

## Recommended actions (in priority order)

| Priority | Segment | Customers | Action | Why |
|---|---|---|---|---|
| 1 | New Customers | 36,141 | Welcome journey and a second-purchase offer within the first weeks | Largest, freshest group, and the cheapest to influence. |
| 2 | Potential Loyalists | 19,714 | Remarketing and repeat-purchase nudges | Still warm, and some already have 2 orders. |
| 3 | At Risk | 922 | Win-back campaign with a personal offer | Highest spend among recoverable customers. |
| 4 | Can't Lose Them | 70 | Personal retention outreach | Used to buy often (3+ orders) and are now quiet. |
| 5 | Hibernating | 36,352 | Low-cost reactivation email, then stop | Large but low engagement, so keep cost per contact near zero. |
| 6 | Loyal Customers and Champions | 158 | VIP rewards, cross-sell, personalised offers | Small but the highest spenders, so protect them. |

**Illustrative scenario (an assumption, not a measured result):** if 1% of the 90,556 one-time buyers (about 906 customers) placed one more order at the average order value of about R$ 164, revenue would rise by roughly R$ 149K. The real figure depends on the campaign.

---

## How reliable are these insights?

- **Snapshot, not a trend.** The data has one row per customer, so it cannot show revenue over time or whether segments are growing.
- **Reference date.** Recency is measured from the last order in the dataset (2018), not from today.
- **Payment value is not profit.** Monetary includes freight, so margin by segment is unknown.
- **Thresholds are a choice.** Champions has only 32 customers under the current rule (R ≥ 4 and F ≥ 4). A looser rule would change segment sizes, but not the one-time-buyer conclusion.
- **Single marketplace.** Purchases made elsewhere are invisible.

## What I would add next

1. A **cohort retention view**, to see how quickly first-time buyers drop off and when a second-purchase offer works best.
2. **State and city filters**, to see whether repeat behaviour differs by region.
3. **Product category data** (from the order items table), to find which first purchases lead to repeat buyers.
4. A comparison with **K-means clustering**, to test whether data-driven segments match the rule-based ones.

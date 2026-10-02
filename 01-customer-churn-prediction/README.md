<h1 align="center">Customer Churn Prediction</h1>
<h3 align="center">Telco BMI Dataset</h3>

<p align="center">
  <img src="images/customer_churn.jpg" alt="Description" width="400">
</p>

A full end-to-end machine learning project that predicts whether a telecom customer will churn, built with Python and deployed as a live interactive web application.

**Streamlit Deploy:** [[https://datascienceportfolio-customer-churn-engine.streamlit.app/](https://data-science-portfolio-churn-model.streamlit.app/)]

## Project Objective

Customer churn is one of the most expensive problems in Telecom industry, the rate at which subscribers leave for competitors or cancel services. Because acquiring a new customer costs significantly more than retaining an existing one, telcos rely heavily on data analytics and predictive modeling to identify at-risk users before they leave.
This project builds a production-grade churn prediction system that:

- Identifies high-risk customers before they leave
- Explains *why* a customer is at risk
- Recommends specific retention actions per customer
- Achieves **89% recall** on churners with an optimized decision threshold

---

## The Business Problem

A telecom company loses money every time a customer cancels their subscription. Finding a new customer costs 5–7x more than retaining an existing one.

The goal of this project is to answer one question:

> **"Which customers are about to leave and what should we do about it?"**

Using historical data on 7,043 customers, I built a model that flags high-risk customers before they churn, explains why they are at risk, and recommends
specific retention actions for each one.

---

## Dataset

Telco Customer Churn dataset (7,049 customers, 21 features).
- Link: https://github.com/IBM/telco-customer-churn-on-icp4d/tree/master/data

---

## What the Data Told Us

### 1. The churn rate is 26.5% - a serious problem
More than 1 in 4 customers left the company. That is significantly above the industry average and means the business is losing a large portion of its revenue
base every year. This also means the dataset is imbalanced, there are far more loyal customers than churners, which we had to handle carefully during modeling.

### 2. Contract type is the single biggest predictor of churn
Customers on **month-to-month contracts churn at ~43%** compared to just 11% on one-year and 3% on two-year contracts. Month-to-month customers have no financial
lock-in, so they can leave any time with no penalty. This is the clearest signal in the entire dataset.

### 3. Fiber optic customers churn more than DSL customers
Despite fiber optic being the premium product, its customers churn at a higher rate. This suggests a **value-for-money problem**, customers paying more expect
better service and are more sensitive to any disappointment. Fiber optic also faces more competition from alternative providers, making customers churn between companies fast.

### 4. New customers are the highest risk group
Customers in their **first 12 months churn at nearly double the rate** of long-tenured customers. The first year is the critical retention window, if a
customer makes it past 12 months they are significantly more likely to stay long term. This points to an onboarding and early experience problem.

### 5. Electronic check payment signals disengagement
Customers paying by **electronic check churn at ~45%** compared to ~15–18% for automatic payment methods. Customers on autopay have made a passive commitment
to stay, because they are not actively thinking about their bill each month. Electronic check customers are re-evaluating the relationship every payment cycle.

### 6. Lack of support services drives churn
Customers **without tech support or online security churn at roughly twice the rate** of customers who have these services. These add-ons create stickiness, while
a customer who relies on your security service has a real cost to leaving. Without them, the relationship is purely transactional and easy to walk away from.

### 7. High monthly charges amplify all other risks
Customers paying **above $70/month** are more price-sensitive and churn at higher rates, especially when combined with month-to-month contracts. The combination of
high cost and no commitment is the most dangerous customer profile in the dataset.

---

## Model Performance

Three models were trained and compared (Logistic Regression, Random Forest, Gradient Boost), and according to the model evaluation and their total accuracy metrics comparison, the best model was chosen and evaluated again, so we can be sure the results are accurate and not just luck.

| Model | Accuracy | ROC-AUC |
|---|---|---|
| Logistic Regression | baseline | baseline |
| Random Forest | good | good |
| **Gradient Boosting** | **best** | **0.8824** |

**Gradient Boosting won** because it builds trees sequentially, each one learning from the mistakes of the previous one. It handles the mix of binary, categorical,
and continuous features in this dataset particularly well.

### Cross-validation confirmed the model is stable
The model was tested on 5 different data splits, just to be sure that the best model performance is not 'luck', but real performance. All 5 scored between 0.877 and 0.891, a very tight band. This means the model is genuinely learning patterns and not getting lucky on one particular split.

### Threshold tuning recovered 35 extra customers per cycle

By default, models predict churn when probability exceeds 0.50. By lowering the threshold to **0.34** and optimizing for recall:

| | Default (0.50) | Optimized (0.34) |
|---|---|---|
| Churners caught | 298 / 374 | 333 / 374 |
| Recall | 80% | **89%** |
| Missed churners | 76 | 41 |

**35 additional customers saved per scoring cycle.** At $1,200 average customer lifetime value, that is **~$42,000 in recovered annual revenue** per 1,409
customers scored, just from changing one threshold number.

The trade-off is 97 more false alarms, loyal customers who get a retention offer they didn't need. A discount coupon costs ~$10. Losing a customer costs $1,200.
The math strongly favors catching more churners.

---

## Business Recommendations

Based on the findings above, here are the five **highest-impact actions** the business should take, according to our data analysis:

**1. Target month-to-month customers with contract upgrade offers**
This is the single highest-leverage action. Offering a meaningful discount (15–20% off) to convert month-to-month customers to annual contracts directly
attacks the biggest churn driver. Even converting 20% of them would materially reduce overall churn rate.

**2. Build a dedicated new customer onboarding program**
The first 12 months are the danger zone. A structured onboarding experience, check-in calls at 30, 60, and 90 days, proactive support outreach, and a
satisfaction survey at 6 months, would significantly reduce early churn.

**3. Investigate the fiber optic value gap**
The fact that your premium product churns more than your standard product is a warning sign. Survey fiber optic churners specifically to understand whether the
issue is price, reliability, customer service, or competition. Fix the root cause before acquiring more fiber optic customers.

**4. Incentivize automatic payment enrollment**
Customers on autopay are measurably more loyal. Offering a small monthly discount (even $2–3) for switching to automatic payment would reduce both churn and
payment processing costs simultaneously.

**5. Bundle support services for high-risk profiles**
When the model flags a high-risk customer, the retention offer should prioritize tech support and online security trials. These services create genuine switching
costs. A customer who relies on your security service has a real reason to stay beyond just price.

---

## Conclusion

This project demonstrates that churn is not random, it follows clear, predictable patterns that a well-built model can detect before the customer ever makes the
decision to leave.

The most important lesson from this analysis is that churn is a symptom, not the root problem. Month-to-month contracts, high charges without perceived value,
lack of support services, and a weak onboarding experience are the actual problems. The model gives the business a window of opportunity, a list of customers who are showing early warning signs, but what the business does with that list is what determines the outcome.

A retention offer sent to the right customer at the right moment costs a fraction of what acquiring a new customer costs. This model, deployed as a live scoring
tool, makes that targeting possible at scale, moving the business from reactive (responding after a customer cancels) to proactive (intervening before they decide
to).

From a technical standpoint, the key decisions that drove performance were not the model choice itself, but the careful handling of class imbalance with SMOTE,
the deliberate threshold tuning weighted toward recall, and the clean feature engineering that removed noise and kept only meaningful signals. A Gradient
Boosting model with a tuned threshold of 0.34 achieved 89% recall on churners, meaning the business can now identify and act on 9 out of every 10 customers who
would have otherwise walked out the door silently.

The live application makes these predictions accessible to any member of the business, no technical knowledge required. Enter a customer profile, get a risk
score, understand why, and know exactly what to offer them. That is the full journey from raw data to business value.

---

## Project Structure


customer-churn-prediction/

├── data/                           # Dataset and saved charts

├── models/                         # Trained model, scaler, metadata

│   ├── churn_model.pkl

│   ├── scaler.pkl

│   └── model_metadata.json

├── notebooks/

│   └── 01_EDA_and_Modeling.ipynb  # Full EDA + training pipeline

├── src/

│   └── app.py                      # Streamlit web application

├── requirements.txt

└── README.md

---

## Machine Learning Pipeline

1. **Data** —> IBM Telco Customer Churn dataset (7,043 customers, 21 features)
2. **EDA** —> Churn distribution, feature correlations, categorical breakdowns
3. **Preprocessing** —> Label encoding, one-hot encoding, StandardScaler
4. **Class imbalance** —> SMOTE oversampling (26.5% minority class)
5. **Modeling** —> Logistic Regression, Random Forest, Gradient Boosting
6. **Evaluation** —> ROC-AUC, Precision-Recall curve, confusion matrix
7. **Threshold tuning** —> F2-score optimization (recall-weighted)
8. **Deployment** —> Streamlit web app with live inference

---

## Tech Stack

- **Python** — Pandas, NumPy, Scikit-learn, Imbalanced-learn
- **Visualization** — Matplotlib, Seaborn
- **Web App** — Streamlit
- **Deployment** — Streamlit Community Cloud

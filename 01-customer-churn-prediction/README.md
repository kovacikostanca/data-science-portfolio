# Customer Churn Prediction

An end-to-end machine learning system that predicts which telecom customers are about to leave, explains why, and recommends a retention action. Trained on 7,043 real customers and deployed as a live web app, not just a notebook.

**Live demo:** https://datascienceportfolio-customer-churn-engine.streamlit.app/


| ROC-AUC | Recall on churners | Tuned threshold | Est. revenue protected per cycle |
|:---:|:---:|:---:|:---:|
| **0.88** | **89%** | **0.34** (default 0.50) | **~$42,000** |

---

## Overview

Customer churn is one of the most expensive problems in telecom. Winning a new customer costs 5 to 7 times more than keeping an existing one, so telcos need to spot at-risk customers before they leave.

This project answers one question:

> **Which customers are about to leave, and what should we do about it?**

The system:

- identifies high-risk customers before they churn
- explains why each customer is at risk
- recommends a retention action for each one
- reaches **89% recall** on churners using a tuned decision threshold

## The business problem

A telecom company was losing about 1 in 4 customers every year. Its retention team sent discount offers to everyone, wasting budget on loyal customers while missing the ones actually about to leave. Four things made this harder than a standard classification task:

1. **High acquisition cost.** Every churner the business misses is an expensive loss.
2. **Blind retention spend.** With no scoring system, discounts went to loyal customers too.
3. **Imbalanced classes.** Only 26.5% of customers churn. A model that predicts "stay" for everyone is 73.5% accurate and completely useless.
4. **Unexplained churn signals.** The team knew fiber optic customers left more often, but had no evidence of why.

## What the data showed

The churn rate is **26.5%**: more than 1 in 4 customers left. That also makes the dataset imbalanced, which needed careful handling during modeling. Exploratory analysis found six patterns, each pointing to a business decision:

1. **Contract type is the biggest predictor.** Month-to-month customers churn at about 43%, against 11% on one-year and 3% on two-year contracts. With no lock-in, they can leave at any time.
2. **New customers are the highest-risk group.** In the first 12 months, customers churn at nearly double the rate of long-tenured ones. This points to an onboarding and early-experience problem.
3. **Fiber optic customers churn more than DSL customers,** despite fiber being the premium product. This suggests a value-for-money problem.
4. **Electronic check payment signals disengagement.** These customers churn at about 45%, against 15 to 18% on autopay.
5. **Missing support services drives churn.** Customers without tech support or online security churn at roughly twice the rate of those who have them. These add-ons create switching costs.
6. **High monthly charges amplify every other risk.** Customers paying above $70 a month are more price-sensitive, especially on month-to-month contracts.

## Model performance

Three models were compared: Logistic Regression (baseline), Random Forest and Gradient Boosting. **Gradient Boosting performed best, with a ROC-AUC of 0.8824.** It builds trees one after another, each correcting the mistakes of the last, which suits this mix of binary, categorical and continuous features.

**Cross-validation confirmed the model is stable.** On 5 different data splits, ROC-AUC stayed between 0.877 and 0.891, so the result is not luck on one split.

### Threshold tuning

By default, a model flags a customer as likely to churn when the predicted probability is above 0.50. I lowered the threshold to 0.34 using the F2-score, which weighs recall twice as heavily as precision, because a missed churner costs far more than a false alarm.

Results on the held-out test set (1,409 customers, 374 of them churners):

| | Default (0.50) | Tuned (0.34) |
|---|:---:|:---:|
| Churners caught | 298 / 374 | 333 / 374 |
| Recall | 80% | **89%** |
| Missed churners | 76 | **41** |
| False alarms | 293 | 390 |

**The business math**

- 35 extra churners caught × $1,200 average lifetime value = **$42,000**
- 97 extra false alarms × $10 per retention offer = **$970**
- Net gain: about **$41,000 per scoring cycle** of 1,409 customers, from changing one number.

> **Note:** these figures assume a $1,200 average customer lifetime value, a $10 offer cost, and that every extra flagged churner stays after the offer. In practice only some customers accept, so the real gain would be lower. A controlled test of the offers would measure the real save rate.

## Business recommendations

1. **Move month-to-month customers to annual contracts.** Offer a 15 to 20% discount to upgrade. This attacks the biggest churn driver directly.
2. **Build a 12-month onboarding program.** Check in at 30, 60, 90 and 180 days, with proactive support outreach.
3. **Investigate the fiber optic value gap.** The premium product should not churn more than the standard one. Survey fiber optic churners to find the root cause.
4. **Encourage autopay enrollment.** A $2 to $3 monthly discount lowers both churn and payment processing costs.
5. **Bundle support services for high-risk customers.** Lead retention offers with tech support and online security trials.

## Machine learning pipeline

| Stage | What I did |
|---|---|
| Data | IBM Telco Customer Churn dataset: 7,043 customers, 21 features |
| EDA | Churn distribution, feature correlations, categorical breakdowns. Converted `TotalCharges` to numeric and filled its 11 blanks with 0, since they were new customers with no billing history |
| Preprocessing | Binary encoding, one-hot encoding, `StandardScaler` fitted on training data only. Merged "No internet service" and "No phone service" into "No" |
| Class imbalance | SMOTE on the training set only (4,139 vs 1,495 balanced to 4,139 vs 4,139). The test set was left untouched |
| Modeling | Logistic Regression, Random Forest, Gradient Boosting |
| Evaluation | ROC-AUC, precision-recall curve, confusion matrix, 5-fold cross-validation |
| Threshold tuning | F2-score optimization (recall-weighted), from 0.50 to 0.34 |
| Deployment | Streamlit web app with live inference, hosted on Streamlit Community Cloud |

## Key learnings

- **Accuracy is a lying metric for imbalanced problems.** Predicting "stay" for everyone scores 73.5% accuracy and catches no churners. Match the metric to the real cost of each error.
- **Threshold tuning matters as much as model choice.** Moving the threshold from 0.50 to 0.34 caught 35 more churners per cycle.
- **Understand missing data before filling it.** The blank `TotalCharges` values were new customers, so filling them with the mean would have added false signal.
- **Explainability drives action.** A score with no explanation is hard to use. Showing the factors behind each prediction turns the model into a retention roadmap.

## Project structure

```
customer-churn-prediction/
├── data/                        # Dataset and saved charts
├── models/                      # Trained model, scaler, metadata
│   ├── churn_model.pkl
│   ├── scaler.pkl
│   └── model_metadata.json
├── notebooks/
│   └── 01_EDA_and_Modeling.ipynb   # Full EDA and training pipeline
├── src/
│   └── app.py                   # Streamlit web application
├── requirements.txt
└── README.md
```

## Run it locally

```bash
git clone https://github.com/kovacikostanca/01-customer-churn-prediction.git
cd 01-customer-churn-prediction
pip install -r requirements.txt
streamlit run src/app.py
```

## Dataset

[IBM Telco Customer Churn](https://github.com/IBM/telco-customer-churn-on-icp4d/tree/master/data): 7,043 customers and 21 features.

## Tech stack

- **Language and data:** Python, Pandas, NumPy
- **Modeling:** scikit-learn, imbalanced-learn
- **Visualization:** Matplotlib, Seaborn
- **Web app and deployment:** Streamlit, Streamlit Community Cloud

## Author

Built by **Kostanca Kovaci**. See more projects at [kostancakovaci.com](https://kostancakovaci.com).

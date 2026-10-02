import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os

st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📡",
    layout="wide"
)

# ── Load model artifacts ───────────────────────────────────────
@st.cache_resource
def load_artifacts():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model = joblib.load(os.path.join(base, 'models', 'churn_model.pkl'))
    scaler = joblib.load(os.path.join(base, 'models', 'scaler.pkl'))
    with open(os.path.join(base, 'models', 'model_metadata.json')) as f:
        metadata = json.load(f)
    return model, scaler, metadata

model, scaler, metadata = load_artifacts()
THRESHOLD = metadata['optimal_threshold']
FEATURE_COLUMNS = metadata['feature_columns']

# ── Header ─────────────────────────────────────────────────────
st.title("📡 Customer Churn Predictor")
st.markdown("""
Telecom companies lose **1 in 4 customers** every year to churn.
This tool uses a machine learning model trained on **7,043 real customers**
to predict who is about to leave — and what to do about it.
""")

with st.expander("📖 How to use this app"):
    st.markdown("""
    **Step 1** — Fill in the customer profile below (contract type, charges, services)

    **Step 2** — Click **Predict Churn Risk**

    **Step 3** — Read the result:
    - The churn probability (0–100%)
    - Whether the customer is HIGH or LOW risk
    - The specific reasons driving their risk
    - Recommended retention actions to keep them

    ---
    💡 **Tip:** Click **Load high-risk example** below to see the model in action instantly.
    """)

col_ex1, col_ex2 = st.columns([1, 4])
with col_ex1:
    if st.button("⚡ Load high-risk example"):
        st.session_state['example'] = True
    if st.button("🔄 Reset"):
        st.session_state['example'] = False
with col_ex2:
    st.caption("High-risk profile: month-to-month contract, fiber optic, 2 months tenure, electronic check, $89/month.")

st.divider()

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.header("📊 Model Info")
    st.metric("Algorithm", metadata['model_name'])
    st.metric("ROC-AUC", f"{metadata['roc_auc']:.4f}")
    st.metric("Optimal Threshold", f"{THRESHOLD:.2f}")
    st.divider()
    st.markdown("**What is ROC-AUC?**")
    st.caption("A score of 0.88 means the model correctly ranks a churner above a non-churner 88% of the time. Anything above 0.80 is considered strong.")
    st.divider()
    st.markdown("**What is the threshold?**")
    st.caption(f"If churn probability ≥ {THRESHOLD:.2f}, the customer is flagged as high risk. Lowered from default 0.50 to catch more churners.")
    st.divider()
    st.caption("Trained on IBM Telco Customer Churn dataset — 7,043 customers, 21 features.")

# ── Input form ─────────────────────────────────────────────────
st.subheader("🧾 Customer Profile")

example = st.session_state.get('example', False)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Account Details**")
    tenure = st.slider(
        "Tenure (months)",
        0, 72,
        2 if example else 12,
        help="How long this customer has been with the company"
    )
    contract = st.selectbox(
        "Contract Type",
        ["Month-to-month", "One year", "Two year"],
        index=0,
        help="Month-to-month customers are much more likely to churn"
    )
    payment_method = st.selectbox(
        "Payment Method",
        ["Electronic check", "Mailed check",
         "Bank transfer (automatic)", "Credit card (automatic)"],
        index=0,
        help="Customers on automatic payment are more engaged and less likely to churn"
    )
    paperless = st.selectbox("Paperless Billing", ["Yes", "No"], index=0)

with col2:
    st.markdown("**Charges**")
    monthly_charges = st.slider(
        "Monthly Charges ($)",
        20.0, 120.0,
        89.0 if example else 65.0,
        step=0.5,
        help="Higher charges increase churn risk, especially on month-to-month contracts"
    )
    total_charges = st.number_input(
        "Total Charges ($)",
        min_value=0.0,
        value=float((2 if example else 12) * (89.0 if example else 65.0)),
        help="Total amount paid over the customer's lifetime"
    )
    st.markdown("**Demographics**")
    senior = st.selectbox("Senior Citizen", ["No", "Yes"], index=0)
    partner = st.selectbox("Partner", ["Yes", "No"], index=0)
    dependents = st.selectbox("Dependents", ["No", "Yes"], index=0)

with col3:
    st.markdown("**Services**")
    internet = st.selectbox(
        "Internet Service",
        ["Fiber optic", "DSL", "No"],
        index=0,
        help="Fiber optic customers churn more — higher cost and more competition"
    )
    phone = st.selectbox("Phone Service", ["Yes", "No"], index=0)
    multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes"], index=0)
    online_security = st.selectbox(
        "Online Security", ["No", "Yes"],
        index=0,
        help="Customers without security services have less reason to stay"
    )
    online_backup = st.selectbox("Online Backup", ["No", "Yes"], index=0)
    device_protect = st.selectbox("Device Protection", ["No", "Yes"], index=0)
    tech_support = st.selectbox(
        "Tech Support", ["No", "Yes"],
        index=0,
        help="Customers without tech support feel underserved"
    )
    streaming_tv = st.selectbox("Streaming TV", ["No", "Yes"], index=0)
    streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes"], index=0)

# ── Build feature vector ───────────────────────────────────────
def build_features():
    binary = {'Yes': 1, 'No': 0}
    data = {
        'gender':                                   0,
        'SeniorCitizen':                            1 if senior == 'Yes' else 0,
        'Partner':                                  binary[partner],
        'Dependents':                               binary[dependents],
        'tenure':                                   tenure,
        'PhoneService':                             binary[phone],
        'MultipleLines':                            binary[multiple_lines],
        'OnlineSecurity':                           binary[online_security],
        'OnlineBackup':                             binary[online_backup],
        'DeviceProtection':                         binary[device_protect],
        'TechSupport':                              binary[tech_support],
        'StreamingTV':                              binary[streaming_tv],
        'StreamingMovies':                          binary[streaming_movies],
        'PaperlessBilling':                         binary[paperless],
        'MonthlyCharges':                           monthly_charges,
        'TotalCharges':                             total_charges,
        'InternetService_Fiber optic':              1 if internet == 'Fiber optic' else 0,
        'InternetService_No':                       1 if internet == 'No' else 0,
        'Contract_One year':                        1 if contract == 'One year' else 0,
        'Contract_Two year':                        1 if contract == 'Two year' else 0,
        'PaymentMethod_Credit card (automatic)':    1 if payment_method == 'Credit card (automatic)' else 0,
        'PaymentMethod_Electronic check':           1 if payment_method == 'Electronic check' else 0,
        'PaymentMethod_Mailed check':               1 if payment_method == 'Mailed check' else 0,
    }
    df_input = pd.DataFrame([data])
    df_input = df_input.reindex(columns=FEATURE_COLUMNS, fill_value=0)
    df_input[['tenure', 'MonthlyCharges', 'TotalCharges']] = scaler.transform(
        df_input[['tenure', 'MonthlyCharges', 'TotalCharges']]
    )
    return df_input

# ── Predict ────────────────────────────────────────────────────
st.divider()

if st.button("🔍 Predict Churn Risk", type="primary", use_container_width=True):

    features = build_features()
    probability = model.predict_proba(features)[0][1]
    prediction = int(probability >= THRESHOLD)

    st.divider()
    st.subheader("📈 Prediction Result")

    r1, r2, r3 = st.columns(3)
    with r1:
        st.metric("Churn Probability", f"{probability*100:.1f}%")
    with r2:
        st.metric("Threshold Used", f"{THRESHOLD:.2f}")
    with r3:
        if prediction == 1:
            st.error("⚠️ HIGH CHURN RISK")
        else:
            st.success("✅ LOW CHURN RISK")

    st.progress(
        float(probability),
        text=f"Risk level: {probability*100:.1f}% — {'Above' if prediction==1 else 'Below'} the {THRESHOLD:.2f} threshold"
    )

    st.divider()
    f1, f2 = st.columns(2)

    with f1:
        st.markdown("**🚨 Key Risk Signals**")
        signals = []
        if contract == "Month-to-month":
            signals.append("⚠️ Month-to-month contract — no lock-in, easiest to leave")
        if internet == "Fiber optic":
            signals.append("⚠️ Fiber optic — premium cost, high competition")
        if payment_method == "Electronic check":
            signals.append("⚠️ Electronic check — low engagement, no autopay commitment")
        if tenure < 12:
            signals.append(f"⚠️ Only {tenure} months tenure — still in high-churn window")
        if monthly_charges > 70:
            signals.append(f"⚠️ ${monthly_charges}/month — high charges increase price sensitivity")
        if tech_support == "No":
            signals.append("⚠️ No tech support — lower perceived value")
        if online_security == "No":
            signals.append("⚠️ No online security — less stickiness")
        if not signals:
            signals.append("✅ No major risk signals detected")
        for s in signals:
            st.markdown(s)

    with f2:
        st.markdown("**💡 Recommended Retention Actions**")
        if prediction == 1:
            if contract == "Month-to-month":
                st.markdown("💡 Offer 15–20% discount to upgrade to annual contract")
            if monthly_charges > 70:
                st.markdown("💡 Provide loyalty discount on current plan")
            if tech_support == "No":
                st.markdown("💡 Offer free 3-month tech support trial")
            if online_security == "No":
                st.markdown("💡 Bundle online security at reduced rate")
            if tenure < 12:
                st.markdown("💡 Assign dedicated onboarding support rep")
            if payment_method == "Electronic check":
                st.markdown("💡 Incentivize switch to automatic payment ($2–3/month discount)")
            st.markdown("💡 Schedule proactive check-in call within 7 days")
        else:
            st.markdown("✅ Customer appears stable — standard engagement sufficient")
            st.markdown("💡 Consider upsell opportunity on premium services")
            st.markdown("💡 Invite to loyalty rewards program")

    st.divider()
    st.markdown("**📊 What this means in business terms**")
    if prediction == 1:
        st.info(f"""
        This customer has a **{probability*100:.1f}% probability of churning**.
        At an average customer lifetime value of $1,200/year, losing this customer
        costs the business significantly more than the cost of a retention offer.
        Acting now is the right economic decision.
        """)
    else:
        st.info(f"""
        This customer has only a **{probability*100:.1f}% probability of churning**.
        They are likely to stay. Focus retention budget on higher-risk customers
        and consider this customer for upsell opportunities instead.
        """)

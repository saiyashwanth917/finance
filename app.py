import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page Config (FIXED VERSION)
st.set_page_config(page_title="Invisible 400M", layout="wide")

st.title("💳 The Invisible 400 Million")
st.markdown("### AI-Based Alternative Credit Scoring using UPI Data")

uploaded_file = st.file_uploader("Upload UPI Transaction CSV", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period("M")

    income = df[df['type'] == "CREDIT"]
    expense = df[df['type'] == "DEBIT"]

    monthly_income = income.groupby('month')['amount'].sum()
    monthly_expense = expense.groupby('month')['amount'].sum()

    avg_income = monthly_income.mean()
    income_std = monthly_income.std()

    total_income = monthly_income.sum()
    total_expense = abs(monthly_expense.sum())

    expense_ratio = total_expense / total_income if total_income != 0 else 1

    # Stability Score
    if income_std == 0 or avg_income == 0:
        stability_score = 50
    else:
        stability_score = max(0, 100 - (income_std / avg_income) * 100)

    # Savings Score
    savings_score = max(0, 100 - expense_ratio * 100)

    # Final Alt Credit Score
    alt_credit_score = (0.6 * stability_score) + (0.4 * savings_score)

    # Risk Category
    if alt_credit_score > 75:
        risk = "Low Risk 🟢"
        loan = "Eligible for Loan up to ₹50,000"
    elif alt_credit_score > 50:
        risk = "Medium Risk 🟡"
        loan = "Eligible for Loan up to ₹20,000"
    else:
        risk = "High Risk 🔴"
        loan = "Currently Not Eligible"

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Avg Monthly Income", f"₹{round(avg_income,0)}")
    col2.metric("Stability Score", round(stability_score,1))
    col3.metric("Alt Credit Score", round(alt_credit_score,1))

    st.subheader("Risk Level")
    st.write(risk)

    st.subheader("Loan Eligibility")
    st.write(loan)

    st.subheader("📈 Monthly Income Trend")

    fig, ax = plt.subplots()
    monthly_income.plot(kind='bar', ax=ax)
    ax.set_ylabel("Income")
    ax.set_title("Monthly Income Trend")
    st.pyplot(fig)

else:
    st.info("Please upload a CSV file to continue.")
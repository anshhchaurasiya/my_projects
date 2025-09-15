import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pathlib

# function to load css 
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

css_path = pathlib.Path("assets/style.css")      #loading css
load_css(css_path)

# Class for Fixed Deposit Calculation
class FixedDeposit:
    def __init__(self):
        st.title("💰 Fixed Deposit Interest Calculator")
        st.write("Select the tenure for your FD investment:")
        
        self.tenure = st.selectbox("Choose Tenure:", [1, 3, 5], key="fd_tenure")
        self.show_bank_options()

    def show_bank_options(self):
        st.subheader(f"🏦 Best FD Interest Rates for {self.tenure} Years:")
        
        interest_rates = {
            1: {"Jana Small Finance Bank": 8.25, "Suryoday Small Finance Bank": 8.25, "Ujjivan Small Finance Bank": 8.25},
            3: {"North East Small Finance Bank": 9.0, "Utkarsh Small Finance Bank": 8.5, "Suryoday Small Finance Bank": 8.25, "Jana Small Finance Bank": 8.25},
            5: {"Suryoday Small Finance Bank": 8.60, "Jana Small Finance Bank": 8.2, "Unity Small Finance Bank": 8.15}
        }

        for bank, rate in interest_rates[self.tenure].items():
            st.write(f"🏦 {bank}: **{rate}% p.a**")

        self.amount = st.number_input(f"💰 Enter the amount you want to invest for {self.tenure} years:", min_value=1000.0 , key="fd_amount")
        
        if st.button("📊 Calculate FD Returns", key="fd_return_button"):
            self.fd_return(interest_rates[self.tenure])

    def fd_return(self, interest_rates):
        st.subheader("📈 FD Returns After Completion:")
        for bank, rate in interest_rates.items():
            final_amount = round(self.amount * ((1 + (rate / 100)) ** self.tenure))
            st.write(f"🏦 {bank}: ₹{final_amount}")
            st.write("💡 Fixed Deposits provide a safe and stable way to grow your savings over time with guaranteed returns.")

# Finance Rules Class
class FinanceRules:
    def car_budget(self, car_price):
        interest_rate = 9
        loan_term = 4
        down_payment = 0.2 * car_price
        loan_amount = car_price - down_payment
        r = (interest_rate / 100) / 12
        n = loan_term * 12
        emi = loan_amount * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
        monthly_income_required = emi / 0.1
        return round(down_payment), round(emi), round(monthly_income_required)

    def investment_rule(self, investment):
        return round(0.01 * investment)

    def home_affordability(self, property_price, annual_income):
        return "Affordable" if property_price <= annual_income * 5 else "Not Affordable"

    def debt_to_income(self, income):
        return round(income * 0.36)

# Income Tax Calculation Function
def calculate_tax(income):
    gross = income     
    income -= 75000  
    
    total_tax_amount = []  
    tax_slabs = [(400000, 0.05), (800000, 0.10), (1200000, 0.15), (1600000, 0.20), (2000000, 0.25), (2400000, 0.30)]
    
    for slab, rate in tax_slabs:
        if income > slab:
            tax_amount = min(income - slab, 400000) * rate
            total_tax_amount.append(tax_amount)
    
    sum_total_tax_amount = sum(total_tax_amount)
    total_tax_amount = 0 if sum_total_tax_amount < 60000 else sum_total_tax_amount * 1.04
    return gross, total_tax_amount

# Main Streamlit App
st.sidebar.title("Finance App Navigation")
page = st.sidebar.selectbox("Choose a Feature", [
    "Personal Finance Dashboard", "Income Tax Calculator"
])

if page == "Personal Finance Dashboard":
    st.title("📊 Personal Finance Dashboard")
    option = st.sidebar.selectbox("Select a Feature", [
        "Fixed Deposit Calculator", "Car Budget Rule", "Investment Rule", "Home Affordability Rule", "Debt-to-Income Rule"
    ])

    st.subheader(option)

    finance = FinanceRules()
    
    if option == "Fixed Deposit Calculator":
        FixedDeposit()
    elif option == "Car Budget Rule":
        car_price = st.number_input("Car Price (₹)", min_value=100000.0, value=1000000.0)
        down_payment, emi, income_required = finance.car_budget(car_price)
        if st.button("Calculate Car Budget"):
            st.success(f"🚗 Down Payment: ₹{down_payment}, EMI: ₹{emi}/month, Required Monthly Income: ₹{income_required}")
            st.write("💡 Buying a car? Ensure your EMI doesn't exceed 10% of your monthly income to avoid financial strain.")
    elif option == "Investment Rule":
        investment = st.number_input("Investment Amount (₹)", min_value=1000.0, value=100000.0)
        suggested_investment = finance.investment_rule(investment)
        if st.button("Calculate Investment Rule"):
            st.success(f"💰 Suggested Monthly Investment: ₹{suggested_investment}")
            st.write("💡 Investing regularly helps build long-term wealth. It's recommended to invest at least 1% of your income monthly.")
    elif option == "Home Affordability Rule":
        property_price = st.number_input("Property Price (₹)", min_value=500000.0, value=5000000.0)
        annual_income = st.number_input("Annual Income (₹)", min_value=100000.0, value=1000000.0)
        result = finance.home_affordability(property_price, annual_income)
        if st.button("Check Affordability"):
            st.success(f"🏠 Home Affordability Status: {result}")
            st.write("💡 To avoid financial burden, ensure your home price is at most 5 times your annual income.")
    elif option == "Debt-to-Income Rule":
        income = st.number_input("Monthly Income (₹)", min_value=10000.0, value=50000.0)
        debt_limit = finance.debt_to_income(income)
        if st.button("Calculate Debt-to-Income Limit"):
            st.success(f"🏠 Maximum Recommended Debt: ₹{debt_limit}")
            st.write("💡 To stay financially stress-free, keep your total debt within 36% of your monthly income.")

elif page == "Income Tax Calculator":
    st.title("Income Tax Calculator 💰")
    income = st.number_input("Enter your Gross Income:", min_value=0, value=1000000, step=10000)
    if st.button("Calculate Tax"):
        gross, total_tax_amount = calculate_tax(income)
        st.write(f"### Gross Income: **₹{gross:.2f}**")
        st.write(f"### Total Tax Payable: **₹{total_tax_amount:.2f}**")
        st.write("💡 Understanding your tax helps in better financial planning and savings.")
        labels = ["Saved Income", "Tax on Income"]
        values = [gross - total_tax_amount, total_tax_amount]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
        fig.update_layout(title_text="Income vs. Tax Distribution")
        st.plotly_chart(fig)
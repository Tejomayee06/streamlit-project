import streamlit as st 
st.set_page_config(page_title="My finance dashboard", page_icon="💰")
# inside the app or page:
st.title("My Finance Dashboard")
st.markdown("""This a personal dashboard that helps u track your expenses and manage finacial """)
st.sidebar.header("Financial Inputs")
income = st.sidebar.number_input("Montlhy Income ($)", min_value=0.0, value =5000.0, step=100.0)
st.sidebar.subheader("Monthly Expenses")

rent = st.sidebar.number_input("Rent/Mortage", min_value=0.0, value = 1200.0)

food = st.sidebar.number_input("Food & Groceries", min_value=0.0, value= 400.0)

utilities = st.sidebar.number_input("utilities", min_value=0.0, value= 200.0)

entertainment = st.sidebar.number_input("entertainment", min_value=0.0, value= 150.0)

other= st.sidebar.number_input("other expenses", min_value=0.0, value= 300.0)

savings_goal = st.sidebar.number_input("monthly savings goal ($)", min_value=0.0, max_value=income, value=1000.0)
#calculations
total_expenses = rent + food + utilities + entertainment + other
remaining_balance = income - total_expenses
savings_percentage = (remaining_balance / income) * 100 if income > 0 else 0
#dashboar layout
col1, col2 , col3 = st.columns(3)

with col1:
    st.metric("Total income", f"${income:,.2f}")
with col2:
    st.metric("total expenses", f"${total_expenses:,.2f}", delta=f"-{total_expenses:,.2f}", delta_color="inverse")
with col3:
    st.metric("Remaining Balance", f"${remaining_balance:,.2f}", delta=f"{remaining_balance - savings_goal:,.2f} vs Goal")
st.divider()
#visualizations
st.subheader("Expense Breakdown")
expense_data = {
    "Category": ["rent/mortage","food & groceries", "utilities", "entertainment", "other"],
    "Amount": [rent, food , utilities, entertainment, other]
}
#using streamlit built in bar chart for simplicity
st.bar_chart(data=expense_data, x="Category", y="Amount")
st.subheader("Savings Progress")
if remaining_balance >= savings_goal:
    st.success("congratulations! u have met ur saving goal! by ${savings_percentage:2f} % of your income.")
else:
    st.warning("You r below ur goal. keep working towards it! by ${savings_percentage:.2f} % of your income.")
    # data table
if st.checkbox("Show detailed expenses"):
    st.subheader("Detailed Expenses")
    st.table(expense_data)
st.divider()
    #footer 
st.caption("Created with ❤️ using streamlit")
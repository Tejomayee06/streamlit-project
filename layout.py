import streamlit as st
st.sidebar.header("Setting Panel")
st.sidebar.checkbox("Dar Mode", key="dark_mode")
st.title("Sreamlit Layout Example")
st.write("This is an example of how to use Streamlit's layout features.")
col1,col2 = st.columns(2)
with col1:
    st.header("Column 1")
    st.write("This is the first column.")
with col2:
    st.header("Column 2")
    st.write("This is the second column.")

tab1, tab2 = st.tabs(["About us","Contact"])
with tab1:
    st.header("About Us")
    st.write("We are a company that loves Streamlit")
with tab2:
    st.header("Contact")
    st.write("Feel free to reach out to us!")
with st.form("my_form"):
    st.write("This is a form.Please fill it out.")
    query=st.text_input("Enter your query:")
    email=st.text_input("Enter your email:")
    submit=st.form_submit_button("Submit")
    if submit:
        st.success("Form submitted successfully!")
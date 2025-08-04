import streamlit as st

st.title("Hello, Streamlit!")
st.write("This is a simple Streamlit app to demonstrate the setup.")

number = st.slider("Pick a number", min_value=0, max_value=100, value=50)
st.write(f"You picked: {number}")

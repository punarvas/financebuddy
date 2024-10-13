"""
main.py
Authors: Akash Mahajan and Faraz Gurramkonda
Date: 10/13/2024
"""

from download import download_data
from analysis import analyze
import streamlit as st
import openai
from datetime import datetime
import json


def greet_based_on_time():
    current_hour = datetime.now().hour  # Get the current hour (0-23)
    if 0 <= current_hour < 12:
        greeting = "Good Morning!"
    elif 12 <= current_hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    return greeting


# Initialize session states for navigation and result
if 'res' not in st.session_state:
    st.session_state.res = None
if 'page' not in st.session_state:
    st.session_state.page = "input"


def create_prompt(budget: dict):
    with open("prompt_base.txt", "r") as file:
        prompt = file.read()
    with open("analysis_results.json", "r") as file:
        analysis = file.read()
    prompt = prompt.replace("**##**####**", analysis)
    prompt = prompt.replace("#fff#", f"${budget['Food']}")
    prompt = prompt.replace("#ggg#", f"${budget['Grocery']}")
    prompt = prompt.replace("#uuu#", f"${budget['Utilities']}")
    prompt = prompt.replace("#rrr#", f"${budget['Rent']}")
    prompt = prompt.replace("#mmm#", f"${budget['Mobile']}")
    prompt = prompt.replace("#sss#", f"${budget['Social']}")
    return prompt


def show_output_page():
    st.title("Finance Buddy")

    # Greeting
    st.markdown(f"## Hey, {greet_based_on_time()}")

    # Display output if available
    if st.session_state.res is not None:
        data = json.loads(st.session_state.res)

        # Page title
        st.title(data["title"])

        # CSS for fade-in animation
        st.markdown(
            """
            <style>
            .fade-in {
                animation: fadeIn 2s ease;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            </style>
            """, unsafe_allow_html=True
        )

        # Challenge 1 with fade-in effect
        st.markdown(
            f"""
            <div class="fade-in" style="padding: 10px; border-radius: 5px; margin-bottom: 20px;">
                <h3>💡 Challenge 1</h3>
                <p>{data["challenge1_text"]}</p>
                <div style="background-color: #808080; padding: 10px; border-radius: 5px;">
                    <strong>Hints:</strong> {data["challenge1_hints"]}
                </div>
            </div>
            """, unsafe_allow_html=True
        )

        # Challenge 2 with fade-in effect
        st.markdown(
            f"""
            <div class="fade-in" style="padding: 10px; border-radius: 5px;">
                <h3>💡 Challenge 2</h3>
                <p>{data["challenge2_text"]}</p>
                <div style="background-color: #808080; padding: 10px; border-radius: 5px;">
                    <strong>Hints:</strong> {data["challenge2_hints"]}
                </div>
            </div>
            """, unsafe_allow_html=True
        )

    # Go back button
    if st.button("Go Back"):
        st.session_state.page = "input"  # Update the page state to return to the input page


def show_home_page():
    st.markdown("## How much can you spend next month?")

    # Arrange inputs into two balanced columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Basic Expenses")

        st.write("Food")
        food = st.number_input('', key='food_id', min_value=5, label_visibility="collapsed")

        st.write("Utilities")
        utility = st.number_input('', key='utility_id', min_value=5, label_visibility="collapsed")

        st.write("Mobile")
        mobile = st.number_input('', key='mobile_id', min_value=5, label_visibility="collapsed")

    with col2:
        st.subheader("Living & Social")

        st.write("Groceries")
        groceries = st.number_input('', key='groceries_id', min_value=5, label_visibility="collapsed")

        st.write("Rent")
        rent = st.number_input('', key='rent_id', min_value=100, label_visibility="collapsed")

        st.write("Social activities")
        social = st.number_input('', key='social_id', min_value=5, label_visibility="collapsed")

    # "Advise Me" button to move to output page
    if st.button("Advise Me"):
        click_button(food, groceries, utility, rent, mobile, social)


def click_button(food, groceries, utility, rent, mobile, social):
    # Collect budget input data and create the prompt
    budget = {"Food": food, "Grocery": groceries, "Utilities": utility, "Rent": rent, "Mobile": mobile,
              "Social": social}
    prompt = create_prompt(budget)

    # Make the API call
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{prompt}."}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        st.session_state.res = str(response['choices'][0]['message']['content'])
    except Exception as e:
        st.session_state.res = f"OpenAI API error: {e}"

    # Navigate to output page
    st.session_state.page = "output"


# Main Streamlit app
if __name__ == "__main__":
    OPENAI_API_KEY = "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"
    openai.api_key = OPENAI_API_KEY
    download_data()
    analyze()

    # Show pages based on session state
    if st.session_state.page == "input":
        show_home_page()  # Display only the input page
    elif st.session_state.page == "output":
        show_output_page()  # Display only the output page

import streamlit as st
import openai
import os

import openai

openai.api_key = "add your api key"



# Fine-Tuned Model ID
fine_tuned_model = "ft:gpt-4o-mini-2024-07-18:meead-sultan::BN4X6bXE"

# Initialize Streamlit UI
st.title("🍏 AI Diet Plan Generator")
st.write("Enter patient details to generate a personalized diet plan.")

# User Input
user_input = st.text_input("💬 Enter patient details (e.g., Create a diet plan for a 30-year-old male with diabetes)")

# Function to Generate Diet Plan Using Streaming
def generate_diet_plan(user_prompt):
    try:
        response = openai.ChatCompletion.create(
            model=fine_tuned_model,
            messages=[
                {"role": "system", "content": "You are a professional dietitian and fitness coach."},
                {"role": "user", "content": user_prompt}
            ],
            stream=True  # Enable Streaming
        )

        # Return streamed text output
        for chunk in response:
            if "choices" in chunk and chunk["choices"]:
                yield chunk["choices"][0]["delta"].get("content", "")

    except openai.error.AuthenticationError:
        yield "❌ **Authentication Error: Invalid API Key.** Please check your API key and try again."

# Generate Button
if st.button("🔍 Generate Diet Plan"):
    if user_input:
        st.write("⏳ **Generating diet plan...**")

        # Display streamed text
        diet_plan_text = st.empty()
        full_text = ""

        for text_chunk in generate_diet_plan(user_input):
            full_text += text_chunk
            diet_plan_text.markdown(full_text)  # Update text in Streamlit

        st.success("✅ Diet plan generated successfully!")
    else:
        st.warning("⚠️ Please enter patient details!")

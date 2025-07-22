import os
import groq
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Fetch API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Streamlit Page Configuration
st.set_page_config(page_title="AI Fitness App", layout="wide")

# Streamlit Title
st.title("🏋️‍♂️ PeakForm AI Fitness App")
st.write("Generate personalized meal and workout plans using AI!")

# Load and display UI image
try:
    image = Image.open("fitness_ui.png")  # Ensure this file is in the correct directory
    st.image(image, caption="AI-Powered Fitness UI", use_container_width=True)  # Fixed image fit
except FileNotFoundError:
    st.warning("⚠️ UI Image not found. Make sure 'fitness_ui.png' is in the project folder.")

# Debugging: Check if the API key is loaded
if not GROQ_API_KEY:
    st.error("❌ API Key not found. Please check your .env file.")
    st.stop()

# Initialize Groq client
client = groq.Client(api_key=GROQ_API_KEY)

# Function to generate meal plan
def generate_meal_plan(goal, preferences, age, weight, height, gender):
    st.write("⚡ Generating Meal Plan...")

    prompt = f"""
    Create a detailed meal plan for a {age}-year-old {gender} with the goal of {goal}.
    Weight: {weight} kg, Height: {height} cm.
    Dietary preferences: {preferences}.
    Provide breakfast, lunch, dinner, and snacks.
    Include macronutrient breakdown (protein, carbs, fats).
    """

    response = client.chat.completions.create(
        model="llama3-70b-8192",  
        messages=[{"role": "system", "content": "You are a certified nutritionist."},
                  {"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# Function to generate workout plan
def generate_workout_plan(goal, preferences, intensity):
    st.write("⚡ Generating Workout Plan...")

    prompt = f"""
    Create a structured workout plan for a person whose goal is {goal}.
    Workout Intensity Level: {intensity}.
    Preferences: {preferences}.
    Provide a 7-day workout schedule with strength, cardio, and flexibility exercises.
    """

    response = client.chat.completions.create(
        model="llama3-70b-8192",  
        messages=[{"role": "system", "content": "You are a professional fitness trainer."},
                  {"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# Function for AI chatbot
def ask_ai(query):
    response = client.chat.completions.create(
        model="llama3-70b-8192",  
        messages=[{"role": "system", "content": "You are a fitness and nutrition expert."},
                  {"role": "user", "content": query}]
    )
    return response.choices[0].message.content

# **Ask AI Section (Placed Below Image)**
st.subheader("💬 Ask AI Anything")
user_query = st.text_area("Type your fitness question here...")
if st.button("Ask AI 🤖"):
    ai_response = ask_ai(user_query)
    st.write("🤖 AI Answer:")
    st.write(ai_response)

# Sidebar for User Inputs
st.sidebar.header("🎯 Personalize Your Plan")

goal = st.sidebar.selectbox("🏆 Select Your Goal", ["Weight Gain", "Weight Loss"])
preferences = st.sidebar.text_area("🥗 Dietary Preferences", "High-protein, vegetarian, no dairy")
age = st.sidebar.number_input("🎂 Age", min_value=10, max_value=100, value=25)
weight = st.sidebar.number_input("⚖️ Weight (kg)", min_value=30, max_value=200, value=70)
height = st.sidebar.number_input("📏 Height (cm)", min_value=100, max_value=250, value=175)
gender = st.sidebar.radio("🧑‍⚕️ Gender", ["Male", "Female", "Other"])
intensity = st.sidebar.radio("🔥 Workout Intensity", ["Beginner", "Intermediate", "Advanced"])

# Button to Generate Plans
if st.sidebar.button("Generate Plans 🚀"):
    meal_plan = generate_meal_plan(goal, preferences, age, weight, height, gender)
    workout_plan = generate_workout_plan(goal, preferences, intensity)

    # Two Tabs for Meal Plan & Workout Plan
    tab1, tab2 = st.tabs(["🍽️ Meal Plan", "💪 Workout Plan"])

    with tab1:
        st.subheader("🍽️ Personalized Meal Plan")
        st.write(meal_plan)
        st.download_button(label="📥 Download Meal Plan", data=meal_plan, file_name="meal_plan.txt", mime="text/plain")

    with tab2:
        st.subheader("💪 Personalized Workout Plan")
        st.write(workout_plan)
        st.download_button(label="📥 Download Workout Plan", data=workout_plan, file_name="workout_plan.txt", mime="text/plain")

# Alternative Meals (Swapping)
st.sidebar.subheader("🍏 Swap Meals")
swap_meal = st.sidebar.text_input("Enter Meal to Replace")
if st.sidebar.button("Swap Meal"):
    st.sidebar.success(f"🔄 Suggested Alternative for '{swap_meal}': Grilled Salmon with Quinoa.")

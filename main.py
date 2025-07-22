import os
import groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Debugging: Check if the API key is loaded
if not GROQ_API_KEY:
    raise ValueError("❌ Error: API Key not found. Check your .env file.")

# Initialize Groq client
client = groq.Client(api_key=GROQ_API_KEY)

# Function to generate meal plan using Groq's LLaMA 3
def generate_meal_plan(goal, preferences):
    prompt = f"""
    Create a detailed meal plan for a person with the goal of {goal}.
    Consider these dietary preferences: {preferences}.
    Provide a structured plan with breakfast, lunch, dinner, and snacks.
    Include macronutrient breakdown (protein, carbs, fats) for each meal.
    """

    response = client.chat.completions.create(
        model="llama3-70b-8192",  
        messages=[{"role": "system", "content": "You are a certified nutritionist."},
                  {"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# Function to generate workout plan using Groq's LLaMA 3
def generate_workout_plan(goal, preferences):
    prompt = f"""
    Create a structured workout plan for a person whose goal is {goal}.
    Consider these workout preferences: {preferences}.
    Provide a 7-day workout schedule with strength, cardio, and flexibility exercises.
    """

    response = client.chat.completions.create(
        model="llama3-70b-8192",  
        messages=[{"role": "system", "content": "You are a professional fitness trainer."},
                  {"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# ---- Execution ----
print("Starting fitness app...")

# User Input
goal = "weight gain"  # Change to "weight loss" if needed
preferences = "high-protein, vegetarian, no dairy"

print("Generating meal plan...")
meal_plan = generate_meal_plan(goal, preferences)
print("\n📌 Meal Plan:\n", meal_plan)

print("\nGenerating workout plan...")
workout_plan = generate_workout_plan(goal, preferences)
print("\n📌 Workout Plan:\n", workout_plan)

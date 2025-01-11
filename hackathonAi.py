import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Placeholder for user data
user_data = {
    "calories_consumed": 0,
    "calories_burned": 0,
    "exercise_plan": "",
    "progress": [],
}

# Function to estimate calories from a meal photo
def estimate_calories(image_path):
    api_url = r"http:codezilla.com"  # Replace with actual API URL
    api_key = r"sk-87933f1c7ac04c60bc8ef089c1b01a9e"  # Add your API key
    headers = {"Authorization": f"Bearer {api_key}"}
    files = {"image": open(image_path, "rb")}
    
    try:
        response = requests.post(api_url, headers=headers, files=files)
        if response.status_code == 200:
            return response.json().get("calories", 0)
        else:
            print(f"API Error: {response.status_code}")
            return 0
    except Exception as e:
        print(f"Error: {e}")
        return 0

# Function to fetch calories burned from a wearable device
def get_calories_burned():
    api_url = r"http:codezilla.com"  # Replace with actual API URL
    api_key = r"sk-87933f1c7ac04c60bc8ef089c1b01a9e"  # Add your API key
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json().get("calories_burned", 0)
        else:
            print(f"API Error: {response.status_code}")
            return 0
    except Exception as e:
        print(f"Error: {e}")
        return 0

# Function to recommend exercises based on calories to burn
def recommend_exercise(calories_to_burn):
    exercises = [
        {"name": "Running", "calories_per_minute": 10},
        {"name": "Cycling", "calories_per_minute": 8},
        {"name": "Jumping Jacks", "calories_per_minute": 12},
    ]
    for exercise in exercises:
        minutes = round(calories_to_burn / exercise["calories_per_minute"])
        return f"{exercise['name']} for {minutes} minutes"

# Function to update user progress
def update_progress(calories_consumed, calories_burned):
    today = datetime.now().strftime("%Y-%m-%d")
    user_data["progress"].append({
        "date": today,
        "calories_consumed": calories_consumed,
        "calories_burned": calories_burned,
    })

# Function to visualize progress
def plot_progress():
    dates = [entry["date"] for entry in user_data["progress"]]
    calories_consumed = [entry["calories_consumed"] for entry in user_data["progress"]]
    calories_burned = [entry["calories_burned"] for entry in user_data["progress"]]
    
    plt.plot(dates, calories_consumed, label="Calories Consumed", color="red")
    plt.plot(dates, calories_burned, label="Calories Burned", color="green")
    plt.xlabel("Date")
    plt.ylabel("Calories")
    plt.title("Fitness Progress")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main workflow
def daily_workflow(image_path):
    # Step 1: Calculate calories consumed
    user_data["calories_consumed"] = estimate_calories(image_path)
    
    # Step 2: Fetch calories burned
    user_data["calories_burned"] = get_calories_burned()
    
    # Step 3: Recommend exercise
    calories_to_burn = max(0, user_data["calories_consumed"] - user_data["calories_burned"])
    user_data["exercise_plan"] = recommend_exercise(calories_to_burn)
    
    # Step 4: Update progress
    update_progress(user_data["calories_consumed"], user_data["calories_burned"])
    
    # Step 5: Visualize progress
    plot_progress()
    
    # Summary
    print(f"Calories Consumed: {user_data['calories_consumed']} kcal")
    print(f"Calories Burned: {user_data['calories_burned']} kcal")
    print(f"Recommended Exercise: {user_data['exercise_plan']}")

# Example usage
# Replace 'meal.jpg' with the path to your meal photo
daily_workflow("meal.jpg")

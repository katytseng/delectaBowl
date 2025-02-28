'''
version: 0.0.1
'''

import pandas as pd
from flask import Flask, request, jsonify
import joblib

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "Recipe Recommendation API is running!"

# Load dataset (Ensure "RAW_recipes.csv" exists)
df_recipes = pd.read_csv("RAW_recipes.csv")

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Get user preferences from request
        data = request.get_json()

        # Copy the full dataset to filter
        filtered_recipes = df_recipes.copy()

        # Filter by dietary preference
        if "vegetarian" in data and data["vegetarian"]:
            filtered_recipes = filtered_recipes[filtered_recipes["tags"].str.contains("vegetarian", case=False, na=False)]

        # Filter by appliances (if provided)
        if "appliances" in data and data["appliances"]:
            filtered_recipes = filtered_recipes[filtered_recipes["tags"].apply(
                lambda tags: any(appliance.lower() in tags for appliance in data["appliances"])
            )]

        # Filter by maximum prep time
        if "max_time" in data and isinstance(data["max_time"], (int, float)):
            filtered_recipes = filtered_recipes[filtered_recipes["minutes"] <= data["max_time"]]

        # Convert result to JSON
        return jsonify({'recipes': filtered_recipes[["name", "minutes", "tags"]].to_dict(orient='records')})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

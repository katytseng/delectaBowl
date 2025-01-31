import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD

# Load dataset
df = pd.read_csv("dataset/interactions_train.csv")  # Ensure columns: user_id, recipe_id, rating

# Count number of ratings per recipe
recipe_counts = df.groupby("recipe_id")["rating"].count()

# Convert to DataFrame and sort
popular_recipes = recipe_counts.reset_index().rename(columns={"rating": "num_reviews"})
popular_recipes = popular_recipes.sort_values(by="num_reviews", ascending=False)

# Display top 10 most-reviewed recipes
#print(popular_recipes.head(20))


# Keep recipes with at least 100 reviews
min_reviews = 500
popular_recipe_ids = popular_recipes[popular_recipes["num_reviews"] >= min_reviews]["recipe_id"]

# Filter the original dataset
filtered_df = df[df["recipe_id"].isin(popular_recipe_ids)]


# Display new dataset size
#print(f"Original dataset size: {df.shape}")
#print(f"Filtered dataset size: {filtered_df.shape}")

# Create user-item matrix
user_item_matrix = filtered_df.pivot(index="user_id", columns="recipe_id", values="rating").fillna(0)
#print(user_item_matrix.head(10))
#print(len(user_item_matrix))

# Apply SVD
svd = TruncatedSVD(n_components=18, random_state=42)
user_features = svd.fit_transform(user_item_matrix)

# Reconstruct rating matrix
predicted_ratings = np.dot(user_features, svd.components_)


# Convert predictions to DataFrame
predictions_df = pd.DataFrame(predicted_ratings, index=user_item_matrix.index, columns=user_item_matrix.columns)
#print(predictions_df.head(10))

# Function to recommend top recipes for a user
def recommend_svd(user_id, n=5):
    user_row = predictions_df.loc[user_id]
    recommended_items = user_row.sort_values(ascending=False).head(n).index.tolist()
    return recommended_items

# Example usage
user_id = 4439
rec_output = pd.DataFrame({'id': recommend_svd(user_id)})

rawRecipe = pd.read_csv('dataset/RAW_recipes.csv')
merged_df = rec_output.merge(rawRecipe, on="id", how="left")
print(merged_df)

#print("Recommended recipes:", recommend_svd(user_id))
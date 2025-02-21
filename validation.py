import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error

# Load datasets
df = pd.read_csv("dataset/interactions_train.csv")  # Ensure columns: user_id, recipe_id, rating
validation_df = pd.read_csv("dataset/interactions_validation.csv")  # Same structure as train.csv

# Count number of ratings per recipe
recipe_counts = df.groupby("recipe_id")["rating"].count()

# Convert to DataFrame and sort
popular_recipes = recipe_counts.reset_index().rename(columns={"rating": "num_reviews"})
popular_recipes = popular_recipes.sort_values(by="num_reviews", ascending=False)

# Keep recipes with at least 500 reviews
min_reviews = 500
popular_recipe_ids = popular_recipes[popular_recipes["num_reviews"] >= min_reviews]["recipe_id"]

# Filter datasets
filtered_df = df[df["recipe_id"].isin(popular_recipe_ids)]
filtered_val_df = validation_df[validation_df["recipe_id"].isin(popular_recipe_ids)]

# Create user-item matrix
user_item_matrix = filtered_df.pivot(index="user_id", columns="recipe_id", values="rating").fillna(0)

# K-Fold Cross-Validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)
rmse_scores = []

for train_index, test_index in kf.split(user_item_matrix):
    train_data, test_data = user_item_matrix.iloc[train_index], user_item_matrix.iloc[test_index]

    # Apply SVD
    svd = TruncatedSVD(n_components=18, random_state=42)
    user_features = svd.fit_transform(train_data)

    # Reconstruct rating matrix for the full dataset
    reconstructed_ratings = np.dot(user_features, svd.components_)

    # Convert to DataFrame
    predictions_df = pd.DataFrame(reconstructed_ratings, index=train_data.index, columns=train_data.columns)

    # Handle missing test users by filling with column means
    test_users = test_data.index
    missing_users = [u for u in test_users if u not in predictions_df.index]

    if missing_users:
        # Create a DataFrame with mean predictions for missing users
        mean_predictions = pd.DataFrame(
            np.tile(predictions_df.mean(axis=0).values, (len(missing_users), 1)),
            index=missing_users,
            columns=predictions_df.columns,
        )
        predictions_df = pd.concat([predictions_df, mean_predictions])

    # Align predictions with test users and test recipes
    test_predictions = predictions_df.loc[test_users, test_data.columns]

    # Convert to NumPy arrays
    actual_ratings = test_data.to_numpy()
    predicted_ratings = test_predictions.to_numpy()

    # Only evaluate known ratings (non-zero)
    mask = actual_ratings > 0
    if np.sum(mask) > 0:  # Avoid division by zero
        rmse = np.sqrt(mean_squared_error(actual_ratings[mask], predicted_ratings[mask]))
        rmse_scores.append(rmse)

# Print final validation results
print(f"Average RMSE across folds: {np.mean(rmse_scores):.4f}")

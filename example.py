import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD

# Example user-item matrix
user_item_matrix = np.array([
    [5, 0, 3, 0, 1],
    [0, 4, 0, 3, 2],
    [1, 0, 2, 5, 0],
    [1, 5, 5, 1, 5]
])

# Apply SVD
svd = TruncatedSVD(n_components=3)  # Keep top 2 latent factors
U = svd.fit_transform(user_item_matrix)
S = np.diag(svd.singular_values_)
V = svd.components_

# Reconstruct predicted ratings
predicted_ratings = np.dot(np.dot(U, S), V)

# Convert to DataFrame
predictions_df = pd.DataFrame(predicted_ratings, columns=["Pizza", "Sushi", "Burger", "Pasta", "Cookie"])

print(predictions_df.head())
# Recommend top 2 recipes for user 1 (Alice)
print(predictions_df.iloc[1].sort_values(ascending=False).head())
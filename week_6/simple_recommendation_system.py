import pandas as pd
import numpy as np

# -------------------------
# Load datasets
# -------------------------
print("Loading datasets...")
podcast_df = pd.read_csv("podcasts_large.csv")
users_df = pd.read_csv("users_large.csv")
interactions_df = pd.read_csv("interactions_large.csv")
podcast_df.set_index("podcast_id", inplace=True)
print(f"Loaded {podcast_df.shape[0]} podcasts, {users_df.shape[0]} users, {interactions_df.shape[0]} interactions.\n")

# -------------------------
# Create user-item matrix
# -------------------------
print("Creating user-item rating matrix...")
user_item_matrix = interactions_df.pivot_table(index="user_id", columns="podcast_id", values="rating")
print("User-item matrix shape:", user_item_matrix.shape, "\n")

# -------------------------
# Cosine similarity
# -------------------------
def cosine_similarity_matrix(matrix):
    """Compute pairwise cosine similarity between rows (users)"""
    print("Computing cosine similarity matrix...")
    # Fill NaN with 0
    filled = matrix.fillna(0)
    norms = np.linalg.norm(filled, axis=1)
    sim = np.dot(filled, filled.T) / (norms[:, None] * norms[None, :] + 1e-9)
    return pd.DataFrame(sim, index=matrix.index, columns=matrix.index)

user_similarity = cosine_similarity_matrix(user_item_matrix)
print("Cosine similarity matrix computed.\n")

# -------------------------
# Recommend podcasts
# -------------------------
def recommend_podcasts_pivot(user_id, top_k_neighbors=5, top_n_podcasts=10):
    print(f"Generating recommendations for user {user_id}...")
    
    # Get top K neighbors
    neighbors = user_similarity[user_id].drop(user_id).sort_values(ascending=False).head(top_k_neighbors)
    print(f"Top {top_k_neighbors} similar users:\n", neighbors, "\n")
    
    # Weighted sum of ratings
    neighbor_ratings = user_item_matrix.loc[neighbors.index].fillna(0)  # Fill NaN with 0
    weighted_ratings = neighbor_ratings.T.dot(neighbors) / neighbors.sum()
    
    # Remove already rated podcasts
    already_rated = user_item_matrix.loc[user_id].dropna().index
    recommendations = weighted_ratings.drop(already_rated, errors="ignore").sort_values(ascending=False)
    
    # Join with podcast metadata
    recommendations_df = recommendations.to_frame(name="predicted_rating").join(podcast_df)
    
    print(f"Top {top_n_podcasts} podcast recommendations for user {user_id}:\n")
    print(recommendations_df.head(top_n_podcasts))
    print("\n")
    
    return recommendations_df


# -------------------------
# Example usage
# -------------------------
SAMPLE_USER_ID = 9
recommendations = recommend_podcasts_pivot(SAMPLE_USER_ID, top_k_neighbors=5, top_n_podcasts=10)

# -------------------------
# Add a new user
# -------------------------
def add_new_user_pivot(user_id, user_data):
    """
    user_data: list of tuples [(podcast_id, rating), ...]
    """
    global interactions_df, user_item_matrix, user_similarity
    print(f"Adding new user {user_id} with {len(user_data)} ratings...")
    
    new_df = pd.DataFrame(user_data, columns=["podcast_id", "rating"])
    new_df["user_id"] = user_id
    interactions_df = pd.concat([interactions_df, new_df], ignore_index=True)
    
    # Update user-item matrix
    user_item_matrix = interactions_df.pivot_table(index="user_id", columns="podcast_id", values="rating")
    
    # Update similarity matrix
    user_similarity = cosine_similarity_matrix(user_item_matrix)
    print(f"New user {user_id} added and similarity matrix updated.\n")

# Example: adding a new user
NEW_USER_ID = 1011
new_user_data = [(1, 5), (3, 4), (5, 2)]
add_new_user_pivot(NEW_USER_ID, new_user_data)

# Recommendations for new user
recommendations_new_user = recommend_podcasts_pivot(NEW_USER_ID, top_k_neighbors=5, top_n_podcasts=10)

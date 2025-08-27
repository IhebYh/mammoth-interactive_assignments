import pandas as pd
import random
from faker import Faker

fake = Faker()

# Categories and languages
categories = [
    "Technology", "Health", "Business", "Comedy", "Education", "Sports", 
    "Music", "News", "Science", "History", "Society", "Philosophy", 
    "Politics", "Lifestyle", "True Crime"
]
languages = [
    "English", "Spanish", "French", "German", "Italian", "Arabic", 
    "Portuguese", "Hindi", "Chinese", "Russian"
]

# -------- Podcasts (1000) --------
podcasts = []
for i in range(1, 1001):
    podcasts.append({
        "podcast_id": i,
        "title": fake.sentence(nb_words=4),
        "host": fake.name(),
        "category": random.choice(categories),
        "language": random.choice(languages),
        "avg_rating": round(random.uniform(2.0, 5.0), 2),
        "num_episodes": random.randint(10, 1000),
        "release_year": random.randint(2005, 2025)
    })
df_podcasts = pd.DataFrame(podcasts)
df_podcasts.to_csv("podcasts_large.csv", index=False)

# -------- Users (500) --------
users = []
for i in range(1, 501):
    users.append({
        "user_id": i,
        "name": fake.name(),
        "age": random.randint(16, 70),
        "country": fake.country(),
        "preferred_category": random.choice(categories),
        "preferred_language": random.choice(languages),
        "avg_listening_time_min": random.randint(30, 600)
    })
df_users = pd.DataFrame(users)
df_users.to_csv("users_large.csv", index=False)

# -------- Interactions (~15k) --------
interactions = []
for user_id in range(1, 501):
    # Each user listens to 20–50 podcasts
    listened_podcasts = random.sample(range(1, 1001), random.randint(20, 50))
    for podcast_id in listened_podcasts:
        interactions.append({
            "user_id": user_id,
            "podcast_id": podcast_id,
            "rating": round(random.uniform(1.0, 5.0), 1),
            "listen_time_min": random.randint(5, 180),
            "is_favorite": random.choice([0, 1])
        })
df_interactions = pd.DataFrame(interactions)
df_interactions.to_csv("interactions_large.csv", index=False)

print("Datasets generated successfully!")
print("podcasts_large.csv:", df_podcasts.shape)
print("users_large.csv:", df_users.shape)
print("interactions_large.csv:", df_interactions.shape)

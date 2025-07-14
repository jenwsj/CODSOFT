import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import os
import zipfile
import urllib.request

# Download and unzip MovieLens 100k dataset if not already present
if not os.path.exists("ml-100k"):
    print("Downloading dataset...")
    url = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"
    urllib.request.urlretrieve(url, "ml-100k.zip")
    with zipfile.ZipFile("ml-100k.zip", 'r') as zip_ref:
        zip_ref.extractall(".")

# Load ratings
ratings = pd.read_csv("ml-100k/u.data", sep="\t", names=["user_id", "movie_id", "rating", "timestamp"])

# Load movie titles
movies = pd.read_csv("ml-100k/u.item", sep="|", encoding="latin-1", header=None, usecols=[0, 1])
movies.columns = ["movie_id", "title"]

# Merge datasets
df = pd.merge(ratings, movies, on="movie_id")

# Create user-movie matrix
user_movie_matrix = df.pivot_table(index="user_id", columns="title", values="rating").fillna(0)

# Compute cosine similarity
user_similarity = cosine_similarity(user_movie_matrix)

# Recommend movies based on similar users
def recommend_movies(user_id, num_recommendations=5):
    similarity_scores = list(enumerate(user_similarity[user_id - 1]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similar_users = [i[0] + 1 for i in similarity_scores[1:6]]
    similar_users_data = df[df["user_id"].isin(similar_users)]
    top_movies = (similar_users_data.groupby("title")["rating"]
                  .mean().sort_values(ascending=False)
                  .head(num_recommendations))
    return top_movies

# Example usage
print("Recommended movies for user 1:")
print(recommend_movies(user_id=1))

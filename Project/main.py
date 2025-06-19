import os
import pandas as pd
from Modules.DataHandler import DataHandler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_handler = DataHandler(BASE_DIR)

merged_df = data_handler.merge_data()

# vectorizes df
vectorizer = TfidfVectorizer()
tag_genre_matrix = vectorizer.fit_transform(merged_df["tags_genres"])

# factorizes
n_components = 400  # play with this
svd = TruncatedSVD(n_components=n_components, random_state=42)
reduced_matrix = svd.fit_transform(tag_genre_matrix)

# matches onto merged so movieId is maintained
reduced_df = pd.DataFrame(reduced_matrix)
reduced_df["movieId"] = merged_df["movieId"].values

def get_similar_movies(target_movie_id, top_n=5):
    # find the row index for the movie
    row_id = merged_df.index[merged_df["movieId"] == target_movie_id][0]

    # get cosine similarity just for this movie
    target_vector = reduced_matrix[row_id].reshape(1, -1)

    sim_vector = cosine_similarity(target_vector, reduced_matrix).flatten()

    sim_df = pd.DataFrame(sim_vector)

    # get indices of top 5 similar movies (excluding the movie itself)
    similar_indices = sim_vector.argsort()[::-1][1:5 + 1]

    # return movieIds and scores
    recs = [(merged_df.iloc[i]["movieId"], sim_vector[i]) for i in similar_indices]
    cleaned_recs = [(int(mid), float(score)) for mid, score in recs]

    for movie_id, score in recs:
        print(f"Movie ID: {data_handler.get_title_by_id(movie_id)}, Similarity Score: {score:.3f}")


get_similar_movies(5816)
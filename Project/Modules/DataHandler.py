import pandas as pd
import os

class DataHandler():
    def __init__(self, base_dir):
        self.tags_df = pd.read_csv(os.path.join(base_dir, 'Data', 'tags.csv'))
        self.movies_df = pd.read_csv(os.path.join(base_dir, 'Data', 'movies.csv'))
        self.merged_df = pd.DataFrame

    def get_title_by_id(self, movieId):
        row = self.movies_df[self.movies_df["movieId"] == movieId]
        title = row["title"].values[0]
        return title
    
    def get_id_by_title(self, title):
        row = self.movies_df[self.movies_df["title"] == title]
        id = row["movieId"].values[0]
        return id
    
    # creates df with movieId, string-ifed genres+tags
    def merge_data(self) -> pd.DataFrame:

        # Group tags into lists
        tags_grouped_df = self.tags_df.groupby("movieId")["tag"].apply(list).reset_index()

        # Split genres string into lists
        self.movies_df["genres"] = self.movies_df["genres"].apply(
            lambda x: x.split("|") if isinstance(x, str) else []
        )

        # Merge the dataframes
        self.merged_df = pd.merge(self.movies_df[["movieId", "genres"]], tags_grouped_df, on="movieId")

        # Combine genres and tags, remove duplicates
        self.merged_df["tags_genres"] = self.merged_df.apply(
            lambda row: list(set(row["genres"] + row["tag"])),
            axis=1
        )

        # makes sure each is a list
        self.merged_df["tags_genres"] = self.merged_df["tags_genres"].apply(
            lambda x: x if isinstance(x, list) else []
        )

        # now lowercase everything
        self.merged_df["tags_genres"] = self.merged_df["tags_genres"].apply(
            lambda lst: [str(item).lower() for item in lst]
        )

        # drops not needed solumns
        self.merged_df = self.merged_df.drop(columns=["tag", "genres"])

        # turns list into string for tf-idf
        self.merged_df["tags_genres"] = self.merged_df["tags_genres"].apply(
            lambda items: " ".join(items)
        )

        return self.merged_df
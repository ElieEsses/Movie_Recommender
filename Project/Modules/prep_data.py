import pandas as pd
import os

def prep_data(base_dir) -> pd.DataFrame:
    tags_csv_path = os.path.join(base_dir, 'Data', 'tags.csv')
    movies_csv_path = os.path.join(base_dir, 'Data', 'movies.csv')

    tags_df = pd.read_csv(tags_csv_path)
    movies_df = pd.read_csv(movies_csv_path)

    # Group tags into lists
    tags_grouped_df = tags_df.groupby("movieId")["tag"].apply(list).reset_index()

    # Split genres string into lists
    movies_df["genres"] = movies_df["genres"].apply(
        lambda x: x.split("|") if isinstance(x, str) else []
    )

    # Merge the dataframes
    merged_df = pd.merge(movies_df[["movieId", "genres"]], tags_grouped_df, on="movieId")

    # Combine genres and tags, remove duplicates
    merged_df["tags_genres"] = merged_df.apply(
        lambda row: list(set(row["genres"] + row["tag"])),
        axis=1
    )

    # makes sure each is a list
    merged_df["tags_genres"] = merged_df["tags_genres"].apply(
        lambda x: x if isinstance(x, list) else []
    )

    # now lowercase everything
    merged_df["tags_genres"] = merged_df["tags_genres"].apply(
        lambda lst: [str(item).lower() for item in lst]
    )

    # drops not needed solumns
    merged_df = merged_df.drop(columns=["tag", "genres"])

    # turns list into string for tf-idf
    merged_df["tags_genres"] = merged_df["tags_genres"].apply(
        lambda items: " ".join(items)
    )

    return merged_df
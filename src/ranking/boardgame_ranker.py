import pandas as pd
import numpy as np


class BoardGameRanker:
    def __init__(self, min_votes=50):
        """
        Initialize the BoardGameRanker with minimum votes and feature weights.
        
        Parameters:
        min_votes (int): Minimum votes required for reliability.
        """
        self.min_votes = min_votes
        self.weights = {
            "average": 0.25,
            "bayesian_score": 0.3,
            "bgg_rank": 0.3,
            "stddev": 0.1,
            "review_consistency": 0.1,
            "num_reviews": 0.05,
        }

    def calculate_score(self, row, global_mean, max_rank):
        """
        Calculate the advanced score based parameters and weights.

        Parameters:
        row (pd.Series): A row of the DataFrame containing game data.
        global_mean (float): Global mean rating across all games.
        max_rank (int): Maximum BGG rank for normalization.

        Returns:
        float: The calculated score for the game.
        """
        # Core components
        R = row["average"]
        v = row["usersrated"]
        m = self.min_votes
        bayesian_score = (v / (v + m)) * R + (m / (v + m)) * global_mean

        # Additional components
        bgg_rank_norm = 1 - (row["Board Game Rank"] / max_rank) if row["Board Game Rank"] > 0 else 0
        stddev_inverse = 1 / row["stddev"] if row["stddev"] > 0 else 0
        review_consistency = 1 / row["review_variance"] if row["review_variance"] > 0 else 0
        num_reviews = row["num_reviews"]

        # Weighted score
        score = (
            self.weights["average"] * R +
            self.weights["bayesian_score"] * bayesian_score +
            self.weights["bgg_rank"] * bgg_rank_norm +
            self.weights["stddev"] * stddev_inverse +
            self.weights["review_consistency"] * review_consistency +
            self.weights["num_reviews"] * num_reviews
        )
        return score

    def rank_games(self, game_data, reviews_data):
        """
        Rank games based on the our scoring formula.

        Parameters:
        game_data (pd.DataFrame): The DataFrame containing game data.
        reviews_data (pd.DataFrame): The DataFrame containing reviews data.

        Returns:
        pd.DataFrame: The ranked DataFrame.
        """
        # Aggregate review data
        reviews_summary = reviews_data.groupby("ID").agg(
            num_reviews=("rating", "count"),
            avg_review_rating=("rating", "mean"),
            review_variance=("rating", "var"),
        ).reset_index()

        # Merge review data with game data
        game_data = pd.merge(game_data, reviews_summary, left_on="id", right_on="ID", how="left")
        game_data["review_variance"] = game_data["review_variance"].fillna(0)
        game_data["num_reviews"] = game_data["num_reviews"].fillna(0)


        # Compute advanced scores
        global_mean = game_data["average"].mean()
        max_rank = game_data["Board Game Rank"].max()
        game_data["advanced_score"] = game_data.apply(
            lambda row: self.calculate_score(row, global_mean, max_rank), axis=1
        )

        # Rank games
        game_data["advanced_rank"] = game_data["advanced_score"].rank(ascending=False)
        return game_data.sort_values(by="advanced_score", ascending=False)


# Load datasets
game_details = pd.read_csv("project_data/processed/cleaned_game_details.csv")
reviews = pd.read_csv("project_data/processed/cleaned_reviews_19m.csv")

# Create ranker instance
ranker = BoardGameRanker(min_votes=50)

# Rank games
ranked_games = ranker.rank_games(game_details, reviews)


# Save the ranked data
ranked_games.to_csv("project_data/processed/ranked_games.csv", index=False)

import os
import sys
sys.path.append('src/data_ingestion/')
sys.path.append('src/ranking/')
sys.path.append('src/visualization/')
from data_loading import DataLoader
from data_cleaning import DataCleaner
from boardgame_ranker import BoardGameRanker
from streamlit_app import VisualizationApp

def preprocess_and_rank(config_path, processed_data_path, ranked_games_file):
     data_loader = DataLoader(config_path)
     data_cleaner = DataCleaner(save_path=processed_data_path)

     reviews_data = data_loader.load_data("reviews_19m")
     game_details = data_loader.load_data("game_details")

     if reviews_data is not None and game_details is not None:
        # Clean data
        reviews_data = data_cleaner.remove_duplicates(reviews_data, subset=["user", "ID", "rating"])
        reviews_data = data_cleaner.fill_missing_values(reviews_data)
        data_cleaner.ensure_save_path()
        data_cleaner.save_data(reviews_data, "cleaned_reviews_19m.csv")

        columns_to_drop = [
            "War Game Rank", "Children's Game Rank", "Accessory Rank",
            "Video Game Rank", "Amiga Rank", "Commodore 64 Rank"
        ]
        game_details = data_cleaner.remove_redundant_columns(game_details, columns_to_drop)
        game_details = data_cleaner.remove_low_rated_rows(game_details, column="usersrated", min_threshold=50)
        game_details = data_cleaner.fill_missing_values(game_details)
        game_details = data_cleaner.remove_duplicates(game_details, subset=["id"])
        data_cleaner.save_data(game_details, "cleaned_game_details.csv")

        # Rank games
        ranker = BoardGameRanker(min_votes=50)
        ranked_games = ranker.rank_games(game_details, reviews_data)
        ranked_games.to_csv(ranked_games_file, index=False)
        print(f"Ranked games saved at {ranked_games_file}.")
        
def main():
    config_path = "config.json"
    processed_data_path = "project_data/processed/"
    ranked_games_file = os.path.join(processed_data_path, "ranked_games.csv")

    # Preprocess and rank if not already done
    if not os.path.exists(ranked_games_file):
        preprocess_and_rank(config_path, processed_data_path, ranked_games_file)

    # Visualize results
    app = VisualizationApp(ranked_games_file)
    app.load_data()
    app.run()

if __name__ == "__main__":
    main()
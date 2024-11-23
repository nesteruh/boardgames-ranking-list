# boardgames-ranking-list
Board Game Ranking Project: This project creates a custom ranking for board games using BoardGameGeek data. It considers both average rating and review count for fair ranking. The project includes data import, a custom ranking algorithm, visualization comparisons, and versioned updates with structured branching

---

## Project Structure

```
project_root/
|│  .gitignore
|│  config.json
|│  main.py
|│  README.md
|│  requirements.txt
|
├── project_data/
|   |│  raw/
|   |   |│  bgg-19m-reviews.csv
|   |   |│  games_detailed_info.csv
|   |│  processed/
|       |│  (contains cleaned and ranked datasets)
|
├── src/
    |├── data_ingestion/
    |   |│  data_loading.py
    |   |│  data_cleaning.py
    |
    |├── ranking/
    |   |│  boardgame_ranker.py
    |
    |├── visualization/
        |│  streamlit_app.py
```

---

## Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Key Dependencies:
- pandas
- numpy
- matplotlib
- streamlit

---

## Datasets

This project relies on the following datasets from Kaggle:

1. **BoardGameGeek Reviews (19M Reviews)**: [Link to dataset](https://www.kaggle.com/datasets/jvanelteren/boardgamegeek-reviews?select=bgg-19m-reviews.csv)
2. **Detailed Game Info**: [Link to dataset](https://www.kaggle.com/datasets/jvanelteren/boardgamegeek-reviews?select=games_detailed_info.csv)

### Steps to Add Datasets:
1. Download the datasets from the provided links.
2. Place the files in the `project_data/raw/` directory:
   - `bgg-19m-reviews.csv`
   - `games_detailed_info.csv`

---

## Configuration

The `config.json` file specifies the paths to the datasets. Ensure it is properly configured before running the project. Example:

```json
{
    "reviews_19m": "project_data/raw/bgg-19m-reviews.csv",
    "game_details": "project_data/raw/games_detailed_info.csv"
}
```

---

## How to Run the Project

### Step 1: Preprocessing and Ranking

Run the main pipeline to preprocess the data, calculate rankings, and save the results:

```bash
python main.py
```

### Step 2: Start Visualization

The project uses Streamlit for visualizing the results. Start the Streamlit app using the following command:

```bash
streamlit run main.py
```

---

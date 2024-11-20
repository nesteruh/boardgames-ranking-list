import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class VisualizationApp:
    
    def __init__(self, ranked_data_path):
        """
        Initializes the VisualizationApp with the path to the ranked games data.
        """
        self.ranked_data_path = ranked_data_path
        self.data = None
    
    def load_data(self):
        """
        Loads the ranked games data only when needed.
        """
        if self.data is None:
            try:
                self.data = pd.read_csv(self.ranked_data_path)
            except Exception as e:
                print(f"Error loading ranked games data: {e}")
                self.data = None

    def calculate_comparisons(self):
        """
        Adds columns for rank differences and computes average rank differences.
        """
        self.data["rank_difference"] = self.data["Board Game Rank"] - self.data["advanced_rank"]
        self.data["average_rank_difference"] = self.data["Board Game Rank"] - self.data["average"]

    def scatter_comparison(self):
        """
        Displays a scatterplot comparing Advanced Rank and Official BGG Rank.
        """
        st.subheader("Advanced Rank vs Official BGG Rank")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(
            self.data["Board Game Rank"], 
            self.data["advanced_rank"], 
            s=self.data["usersrated"] / 100, 
            alpha=0.6
        )
        ax.set_title("Advanced Rank vs Official BGG Rank")
        ax.set_xlabel("BGG Rank")
        ax.set_ylabel("Advanced Rank")
        st.pyplot(fig)

    def rank_difference_distribution(self):
        """
        Displays a histogram showing the distribution of rank differences.
        """
        st.subheader("Rank Difference Distribution")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(self.data["rank_difference"], bins=50, color="blue", alpha=0.7)
        ax.axvline(0, color="red", linestyle="--", label="No Difference")
        ax.set_title("Distribution of Rank Differences (BGG Rank - Advanced Rank)")
        ax.set_xlabel("Rank Difference")
        ax.set_ylabel("Frequency")
        ax.legend()
        st.pyplot(fig)

    def cumulative_rank_analysis(self):
        """
        Displays a cumulative distribution plot comparing Advanced Rank and Average Rating Rank.
        """
        st.subheader("Cumulative Distribution: Advanced Rank vs Average Rating Rank")
        sorted_advanced_rank = np.sort(self.data["advanced_rank"])
        sorted_avg_rating_rank = np.sort(self.data["average"])

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(
            sorted_advanced_rank, 
            np.arange(1, len(sorted_advanced_rank) + 1) / len(sorted_advanced_rank), 
            label="Advanced Rank"
        )
        ax.plot(
            sorted_avg_rating_rank, 
            np.arange(1, len(sorted_avg_rating_rank) + 1) / len(sorted_avg_rating_rank), 
            label="Average Rating Rank", 
            linestyle="--"
        )
        ax.set_title("Cumulative Rank Distribution")
        ax.set_xlabel("Rank")
        ax.set_ylabel("Cumulative Percentage")
        ax.legend()
        st.pyplot(fig)
        
    def run(self):
        """
        Run the Streamlit app.
        """
        self.calculate_comparisons()

        st.title("Board Game Rankings Visualization")
        st.sidebar.title("Navigation")
        plot_type = st.sidebar.radio(
            "Choose a Visualization",
            [
                "Scatter Plot: Advanced vs BGG Rank",
                "Rank Difference Distribution",
                "Cumulative Rank Analysis",
            ],
        )

        if plot_type == "Scatter Plot: Advanced vs BGG Rank":
            self.scatter_comparison()
        elif plot_type == "Rank Difference Distribution":
            self.rank_difference_distribution()
        elif plot_type == "Cumulative Rank Analysis":
            self.cumulative_rank_analysis()

#   CSCE 670 Discord Recommender

##   Overview

This project is a Streamlit application created to help users on a Discord server discover other members who share their enthusiasm for specific video games.  It addresses the challenge of finding like-minded gamers within a Discord server, where the platform excels at communication but lacks built-in tools for identifying shared game interests.  This application aims to bridge that gap, particularly benefiting club Discords and similar communities by making it easier for members to connect over their gaming hobbies. 

The application analyzes Discord chat logs to extract information about game mentions, filters out messages expressing negative sentiment towards games, and ranks users based on the relevance of their game discussions to a user's search. 

##   Features

* **Game Mention Extraction:** The system identifies mentions of specific games within Discord chat messages. 
* **Sentiment Filtering:** To focus on positive engagement, the application filters out messages that convey negative feelings about video games. 
* **Phrase-Level Tokenization:** Game titles are precisely identified using phrase-level tokenization, ensuring that titles like "League of Legends" are recognized as complete terms. 
* **User Ranking:** Users are ranked according to their relevance to a game query, using algorithms like BM25 or BERT embeddings. 
* **Interactive User Interface:** A web-based interface allows users to input the names of games and view a ranked list of the most relevant users. 

##   Installation

1.  **Obtain Discord Chat Log Data:**
    * The application requires a source of Discord chat data, such as a database or CSV file, containing message content and associated user information.

2.  **Set up the environment and install dependencies:**

    *(Follow the standard Python installation steps as previously described, ensuring you have `streamlit`, `pandas`, `sentence_transformers`, etc., installed.)*

3.  **Run the Streamlit application:**

    ```bash
    streamlit run app.py  # or app2.py
    ```

4.  **Access the application:** Open a web browser to the URL provided by Streamlit.

##   Usage

1.  **Enter games:** Users input the names of games they are interested in via the web interface (e.g., "Overwatch, League of Legends"). 
2.  **View results:** The application displays a ranked list of users who have demonstrated interest in those games through their positive chat mentions. 

##   Project Structure

    ```
        CSCE670_Discord_Recommender/
    ├── app.py           # Streamlit application ( using BM25)
    ├── app2.py          # Streamlit application ( using  embeddings)
    ├── discord_author_game_mu... # Data file 
    ├── discord_author_game.csv # Data file 
    ├── evaluate.ipynb   # Evaluation
    ├── process.ipynb    # Data processing
    ├── requirements.txt # Python dependencies
    └── README.md      # This file
    ```
    ##   Recommendation Strategy

The application employs several strategies for recommending users:

* **TF-IDF:** This method serves as a baseline for determining content-based similarity. 
* **BM25:** This ranking function is particularly effective for short text segments, such as individual chat messages. 
* **Matrix Factorization:** This technique is used to address data sparsity and uncover underlying user preferences. 
* **BERT Embedding:** This approach helps to overcome differences in vocabulary and identify connections across semantically related game topics. 

##   Evaluation

To assess the effectiveness of the recommendations, a multi-source proxy label approach is utilized. "Friendship" proxies are calculated from:

* **@mentions:** Frequency with which users tag each other. 
* **Chat Frequency:** The amount of interaction between users within the same channels. 
* **Time Overlap:** The degree to which users are active at similar times. 
* **Interactive Replies:** How often users quickly respond to one another. 

The validity of this evaluation method is supported by findings that pairs with high proxy scores exhibit significantly greater cosine similarity compared to randomly selected user pairs. 
##   Key Takeaways and Potential Improvements

* The tool is capable of identifying users with strong engagement in specific games. 
* Further development could explore:
    * Incorporating Discord's user "status" to reflect currently played games. 
    * Analyzing the overall positivity of user messages to better understand social connection needs.
    * Refining the sentiment analysis to account for cases where negative language expresses passion rather than disinterest.

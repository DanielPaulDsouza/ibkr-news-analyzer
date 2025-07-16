# IBKR Historical News Analyzer

A powerful and robust Python tool to fetch, analyze, and perform advanced topic modeling & sentiment analysis on historical news data from Interactive Brokers.

This repository contains the full development history of the project. The latest stable version is **v1.1**.

---

### Official Releases

You can browse the code, documentation, and download the source for each official version by clicking the links below.

| Version | Key Feature                 | Browse Files & README                                                      | View Release Notes & Downloads                                             |
| :------ | :-------------------------- | :------------------------------------------------------------------------- | :------------------------------------------------------------------------- |
| **V1.1** | **Advanced Topic Modeling** | [**Browse V1.1 Files**](https://github.com/DanielPaulDsouza/ibkr-news-analyzer/tree/v1.1) | [**V1.1 Release Notes**](https://github.com/DanielPaulDsouza/ibkr-news-analyzer/releases/tag/v1.1) |
| **V1.0** | **Stable Harvester** | [Browse V1.0 Files](https://github.com/DanielPaulDsouza/ibkr-news-analyzer/tree/v1.0)   | [V1.0 Release Notes](https://github.com/DanielPaulDsouza/ibkr-news-analyzer/releases/tag/v1.0)   |

---

## About the Latest Version (V1.1)

This project has evolved from a simple data harvester into a sophisticated analysis engine. It connects to the IBKR API, downloads news for multiple symbols over a specified date range, and then applies a professional-grade Natural Language Processing (NLP) pipeline to each article. It also analyzes every article for sentiment and flags articles that match your keywords. The final output is a single, rich CSV file containing sentiment scores, keyword flags, and a discovered "Topic ID" for each article, enabling deep thematic analysis, further analysis or visualization.

## Features

-   **Multi-Contract Support:** Fetch news for multiple symbols (e.g., 'SPY', 'QQQ', 'AAPL') in a single, automated run.
-   **Robust API Rate-Limit Handling:** Politely handles API limits by processing articles in configurable batches with pauses, ensuring reliable data collection without being blocked.
-   **✨ New in V1.1: Advanced NLP Pre-processing:** Utilizes a professional pipeline including boilerplate removal, lemmatization (reducing words to their root form), and bigram detection to produce cleaner data for analysis.
-   **✨ New in V1.1: Advanced Topic Modeling:** Implements Latent Dirichlet Allocation (LDA) with TF-IDF vectorization to automatically discover and categorize the underlying themes in the news articles.
-   **Sentiment Scoring:** Uses `TextBlob` to perform sentiment analysis on every article, providing `Sentiment` (Positive, Negative, Neutral) and `Polarity` score columns.
-   **Keyword Flagging:** Includes a `Matches_Keywords` (True/False) column. This allows you to either analyze all news for a symbol or easily filter for articles relevant to your specific interests in a downstream tool like Pandas or Excel.
-   **Fully Configurable:** Easily change all parameters (dates, keywords, contract symbols, batch sizes, number of topics for LDA, etc.) in a simple `config.py` file.
-   **Combined Outputs:** Saves all results from all symbols into a single, detailed CSV file and creates a separate `topic_summary.txt` file that describes the discovered topics for each run.

## What's New in v1.1: Advanced Topic Modeling

This version introduces a powerful topic modeling feature using Latent Dirichlet Allocation (LDA) with an advanced pre-processing pipeline.

-   **Automated Boilerplate Detection:** Automatically finds and removes common, repetitive phrases (e.g., news provider disclaimers) to reduce noise.

-   **Advanced Text Cleaning:** Uses Lemmatization and Bigram detection to treat words like "rates" and "rate" as the same concept, and to understand that "rate_hike" is a single, important idea.

-   **TF-IDF Vectorization:** Employs TF-IDF to intelligently weigh words, giving more importance to terms that are significant to a specific document rather than just frequent overall.

-   **Tunable Model:** Allows the user to easily configure the number of topics to discover, enabling both high-level and granular thematic analysis.

## How does v1.1 Work

The script connects to a running instance of Interactive Brokers' Trader Workstation (TWS) or IB Gateway. For each symbol in the configuration, it makes a request for the ~300 most recent historical news headlines within the specified date range. It then processes these headlines in batches, requesting the full article text for each one while pausing to respect API rate limits. Each article is then cleaned using advanced NLP techniques. This cleaned articles are analyzed using LDA and TF - IDF to discover and categorize underlying themes.

The articles are further analyzed for sentiment and checked against the keyword list before being added to a master results list, which is then saved to a single CSV file.

## How Topic Modeling Works & Tuning Guide

The script first collects all news articles. Then, it cleans the text by removing boilerplate, common "stopwords," and noise like numbers. It then uses TF-IDF to represent the importance of words in each document. Finally, the LDA algorithm analyzes these representations to discover a set number of underlying "topics" (i.e., clusters of words that frequently appear together). Each article in the final CSV is assigned a `Topic_ID` corresponding to its dominant theme.

### Tuning Your Topic Model

The quality of these topics is highly dependent on a few key settings which you can tune in your project:

* **`NUM_TOPICS`** (in `config.py`): This is the most important setting. It defines how many distinct themes the model should look for. A smaller number (~10-15) will produce broad themes. A larger number (25+) will produce more specific, granular themes. It is recommended to start with a smaller number and increase it as you refine your data cleaning.
* **`CUSTOM_STOP_WORDS`** (in `topic_modeler.py`): This is a powerful list where you can add domain-specific words you want the model to ignore. This is the best place to add generic market commentary verbs (e.g., `rose`, `fell`, `climbed`) or other noise you discover.
* **`max_df` / `min_df`** (in `topic_modeler.py`): These parameters in the `TfidfVectorizer` are powerful filters.
    * `max_df=0.85` tells the model to ignore words that appear in more than 85% of all articles. Lowering this value is an effective way to remove overly common words and force the model to find more nuanced themes.
    * `min_df=2` tells the model to ignore words that appear in fewer than 2 documents, which helps remove rare words and potential typos.

## Architectural Choice: `ib_insync` vs. Native `ibapi`

This project is built using the `ib_insync` library rather than the native `ibapi` for a specific architectural reason.

* The **native `ibapi`** is a low-level, purely **event-driven** system. It is powerful for real-time applications that need to react instantly to live data streams pushed from the server.
* **`ib_insync`** is a higher-level library that provides a clean, **synchronous-style (request/response)** interface. It handles the complex asynchronous background work, making it the ideal tool for tasks that follow a linear logic, such as "request a list of data, then process each item."

For this project, which focuses on harvesting and analyzing historical data, the request/response model of `ib_insync` is the superior choice. It allows the code to be simpler, more readable, and more focused on the core tasks of data processing and analysis, rather than on managing complex event loops and callbacks.

## Prerequisites

-   Python 3.8+
-   An Interactive Brokers account (live or paper)
-   Trader Workstation (TWS) or IB Gateway installed and running.

## Setup & Installation

1.  **Clone the repository (or download the ZIP):**
    ```bash
    git clone https://github.com/DanielPaulDsouza/ibkr-news-analyzer.git
    cd ibkr-news-analyzer
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1.  **Log in to TWS or IB Gateway.** Make sure the API connection is enabled.
    -   In TWS: Go to `File -> Global Configuration -> API -> Settings` and check "Enable ActiveX and Socket Clients".

2.  **Edit the configuration file.** Open `config.py` and adjust the settings to your needs. You can change the date range, the keywords, and the list of stock symbols.

3.  **Run the application.** From your terminal, simply run:
    ```bash
    python main.py
    ```

4.  **Check the output.** The script will print its progress in the terminal. Once finished, you will find a CSV file & a .txt file in the `reports` folder with the combined, analyzed news data.

## Output CSV Columns

| Column           | Description                                                              |
| ---------------- | ------------------------------------------------------------------------ |
| `Symbol`         | The contract symbol (e.g., 'SPY') the news is for.                       |
| `Date`           | The publication date of the article.                                     |
| `Time`           | The publication time of the article.                                     |
| `Provider`       | The news provider code (e.g., 'FLY', 'BRFG').                            |
| `Matches_Keywords` | `True` if the article contains any of your keywords, otherwise `False`.    |
| **`Topic_ID`** | **(New in V1.1)** The ID of the topic cluster the article belongs to.      |
| `Sentiment`      | The sentiment classification: 'Positive', 'Negative', or 'Neutral'.      |
| `Polarity`       | The sentiment polarity score (from -1.0 for negative to 1.0 for positive). |
| `Headline`       | The headline of the news article.                                        |
| `Article`        | The full text of the news article (or an error message if unavailable).  |

## Project Roadmap (Future Development)

This project is under active development. The following major features are planned for future versions:

### V2.0: The Advanced Analyzer

-   **Feature:** Upgrade the sentiment analysis engine from `TextBlob` to a finance-specific transformer model like `FinBERT`. Merge the Topic Modeling and FinBERT features into a single, powerful pipeline.
-   **Goal:** To create a comprehensive analysis tool that can not only determine the sentiment of news with high accuracy but also identify the specific economic or financial themes driving that sentiment.

## Disclaimer

This tool is for educational and informational purposes only. Financial markets are complex and risky. Past performance is not indicative of future results. The author is not responsible for any financial losses incurred as a result of using this software. Always do your own research.
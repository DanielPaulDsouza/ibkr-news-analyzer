# IBKR Historical News Analyzer (V1.0)

A powerful and robust Python tool to fetch, analyze, and perform sentiment analysis on historical news data from Interactive Brokers for multiple financial contracts.

This tool is designed as a data collection engine. It connects to the IBKR API, downloads recent news for one or more symbols over a specified date range, analyzes every article for sentiment, flags articles that match your keywords, and saves the rich data into a single, clean CSV file ready for further analysis or visualization.

## Features

-   **Multi-Contract Support:** Fetch news for multiple symbols (e.g., 'SPY', 'QQQ', 'AAPL') in a single, automated run.
-   **Robust API Rate-Limit Handling:** Politely handles API limits by processing articles in configurable batches with pauses, ensuring reliable data collection without being blocked.
-   **Full Article Analysis:** Fetches and analyzes the full text of every article, not just the headlines.
-   **Sentiment Scoring:** Uses `TextBlob` to perform sentiment analysis on every article, providing `Sentiment` (Positive, Negative, Neutral) and `Polarity` score columns.
-   **Keyword Flagging:** Includes a `Matches_Keywords` (True/False) column. This allows you to either analyze all news for a symbol or easily filter for articles relevant to your specific interests in a downstream tool like Pandas or Excel.
-   **Fully Configurable:** Easily change all parameters (dates, keywords, contract symbols, batch sizes, etc.) in a simple `config.py` file.
-   **Combined CSV Export:** Saves all results from all symbols into a single, detailed CSV file with a descriptive filename, perfect for loading into other tools.

## How It Works

The script connects to a running instance of Interactive Brokers' Trader Workstation (TWS) or IB Gateway. For each symbol in the configuration, it makes a request for the ~300 most recent historical news headlines within the specified date range. It then processes these headlines in batches, requesting the full article text for each one while pausing to respect API rate limits. Each article is analyzed for sentiment and checked against the keyword list before being added to a master results list, which is then saved to a single CSV file.

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

4.  **Check the output.** The script will print its progress in the terminal. Once finished, you will find a CSV file in the `reports` folder with the combined, analyzed news data.

## Output CSV Columns

| Column           | Description                                                              |
| ---------------- | ------------------------------------------------------------------------ |
| `Symbol`         | The contract symbol (e.g., 'SPY') the news is for.                       |
| `Date`           | The publication date of the article.                                     |
| `Time`           | The publication time of the article.                                     |
| `Provider`       | The news provider code (e.g., 'FLY', 'BRFG').                            |
| `Matches_Keywords` | `True` if the article contains any of your keywords, otherwise `False`.    |
| `Sentiment`      | The sentiment classification: 'Positive', 'Negative', or 'Neutral'.      |
| `Polarity`       | The sentiment polarity score (from -1.0 for negative to 1.0 for positive). |
| `Headline`       | The headline of the news article.                                        |
| `Article`        | The full text of the news article (or an error message if unavailable).  |

## Project Roadmap (Future Development)

This project is under active development. The following major features are planned for future versions:

### V1.1: The Topic Modeler

-   **Feature:** Implement Latent Dirichlet Allocation (LDA) topic modeling.
-   **Goal:** To automatically discover and categorize the underlying themes in the news articles (e.g., "Monetary Policy," "Geopolitical Risk," "Corporate Earnings"). This will add a new `Topic_ID` column to the output, allowing for a deeper, more thematic analysis of market narratives.

### V2.0: The Advanced Analyzer

-   **Feature:** Upgrade the sentiment analysis engine from `TextBlob` to a finance-specific transformer model like `FinBERT`. Merge the Topic Modeling and FinBERT features into a single, powerful pipeline.
-   **Goal:** To create a comprehensive analysis tool that can not only determine the sentiment of news with high accuracy but also identify the specific economic or financial themes driving that sentiment.

## Disclaimer

This tool is for educational and informational purposes only. Financial markets are complex and risky. Past performance is not indicative of future results. The author is not responsible for any financial losses incurred as a result of using this software. Always do your own research.
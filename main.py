import os
import datetime
import pandas as pd
from ib_insync import IB, util

# Import our custom modules and configuration
import config
from news_fetcher import fetch_historical_news, get_full_article
from sentiment_analyzer import analyze_sentiment

def main():
    """
    Main function to orchestrate the news fetching and analysis process.
    """
    ib = IB()
    all_symbols_results = [] # Master list to hold results from all symbols

    try:
        # --- Connect to IBKR ---
        print(f"Connecting to IBKR on {config.IB_HOST}:{config.IB_PORT}...")
        ib.connect(config.IB_HOST, config.IB_PORT, clientId=config.CLIENT_ID)
        print("Connection successful.")

        # Loop through each symbol specified in the config file
        for symbol in config.CONTRACT_SYMBOLS:
            print(f"\n{'='*20} Processing: {symbol} {'='*20}")
        
            # --- Fetch News Headlines ---
            contract_details = {
                'symbol': symbol,  # Use the symbol from the loop
                'secType': config.CONTRACT_TYPE,
                'exchange': config.EXCHANGE,
                'currency': config.CURRENCY
            }
            all_headlines = fetch_historical_news(ib, contract_details, config.START_DATE, config.END_DATE)

            if not all_headlines:
                print(f"No headlines found for {symbol}. Skipping.")
                continue

            # --- Analyze ALL articles and flag keyword matches ---
            print(f"\nAnalyzing all {len(all_headlines)} articles for {symbol}...")
            
            # Sort headlines by time, newest first
            sorted_headlines = sorted(all_headlines, key=lambda h: h.time, reverse=True)

            # --- NEW: Batch processing logic to avoid rate limiting ---
            BATCH_SIZE = 200  # Process 200 articles at a time
            BATCH_PAUSE = 2 # Pause for 2 seconds between batches

            for i in range(0, len(sorted_headlines), BATCH_SIZE):
                batch = sorted_headlines[i:i + BATCH_SIZE]
                print(f"\n--- Processing Batch {i//BATCH_SIZE + 1}/{len(sorted_headlines)//BATCH_SIZE + 1} ---")

                for headline in batch:
                    if not (config.START_DATE <= headline.time <= config.END_DATE):
                        continue
                
                    # Get full article text
                    article_text = get_full_article(ib, headline)
                    content_to_search = (headline.headline + ' ' + article_text).lower()

                    # Determine if the article matches the keywords
                    matches_keywords = any(keyword.lower() in content_to_search for keyword in config.KEYWORDS_TO_SEARCH)
                
                    # Perform sentiment analysis on every article
                    sentiment, polarity = analyze_sentiment(content_to_search)

                    # Add to results
                    ts = headline.time
                    all_symbols_results.append({
                        'Symbol': symbol,
                        'Date': ts.strftime('%Y-%m-%d'),
                        'Time': ts.strftime('%H:%M:%S'),
                        'Provider': headline.providerCode,
                        'Matches_Keywords': matches_keywords,
                        'Sentiment': sentiment,
                        'Polarity': round(polarity, 4),
                        'Headline': headline.headline,
                        'Article': article_text.replace('\n', ' ').strip()
                    })
                
                    # A more useful progress indicator for batches
                    print(f"  -> Processed: {headline.headline[:60]}...", end='\r')
                    ib.sleep(0.1) # Small pause between each article

                # After a batch is done, check if it's not the very last one
                if i + BATCH_SIZE < len(sorted_headlines):
                    print(f"\n--- Batch complete. Pausing for {BATCH_PAUSE} seconds to respect API limits... ---")
                    ib.sleep(BATCH_PAUSE)
            
            print(f"\n\n{'='*20} Finished processing: {symbol} {'='*20}")

            # Don't pause after the very last symbol
            if symbol != config.CONTRACT_SYMBOLS[-1]:
                print("Pausing before next symbol to respect API rate limits...")
                ib.sleep(5) # CRITICAL: Longer pause between symbols

        # --- Save Combined Report to CSV ---
        if all_symbols_results:
            print("\nSaving combined report to CSV...")
            if not os.path.exists(config.OUTPUT_DIRECTORY):
                os.makedirs(config.OUTPUT_DIRECTORY)

            start_str = config.START_DATE.strftime('%Y%m%d-%H%M%S')
            end_str = config.END_DATE.strftime('%Y%m%d-%H%M%S')
            filename = f"news_report_combined_from_{start_str}_to_{end_str}.csv"
            filepath = os.path.join(config.OUTPUT_DIRECTORY, filename)

            # Create and save DataFrame
            df = pd.DataFrame(all_symbols_results)
            # Reorder columns to put Symbol first
            df = df[['Symbol', 'Date', 'Time', 'Provider', 'Matches_Keywords', 'Sentiment', 'Polarity', 'Headline', 'Article']]
            df.to_csv(filepath, index=False, encoding='utf-8')
            print(f"\nSuccessfully saved the report to '{os.path.abspath(filepath)}'")
        else:
            print("\nNo articles found across all symbols. No CSV file was generated.")

    except ConnectionRefusedError:
        print(f"\nError: Connection refused. Is TWS or IB Gateway running on {config.IB_HOST}:{config.IB_PORT}?")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        if ib.isConnected():
            print("Disconnecting from IBKR.")
            ib.disconnect()

if __name__ == "__main__":
    # ib_insync requires an asyncio event loop to run.
    # util.startLoop() is a helper for running it in scripts.
    util.startLoop()
    main()
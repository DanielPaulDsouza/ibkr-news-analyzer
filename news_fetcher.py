import datetime
from ib_insync import IB, Contract


def fetch_historical_news(ib: IB, contract_details: dict, start_date: datetime, end_date: datetime) -> list:
    """
    Makes a single request to fetch the most recent batch of historical news
    within a given date range.

    NOTE: The IBKR API limits this request to approximately 300 of the most
    recent articles within the specified timeframe. But I have kept a limit of
    100000

    Args:
        ib: An active and connected ib_insync IB instance.
        contract_details: A dictionary with contract info (symbol, type, etc.).
        start_date: The start date for the news search window.
        end_date: The end date for the news search window.

    Returns:
        A list of news headline objects found.
    """
    # 1. Get available news providers for the account
    print("Fetching available news providers...")
    providers = ib.reqNewsProviders()
    if not providers:
        print("Error: No news providers found for this account.")
        return []
    provider_codes = '+'.join([p.code for p in providers])
    print(f"Found providers: {[p.code for p in providers]}")

    # 2. Qualify the contract to get its conId
    contract = Contract(
        symbol=contract_details['symbol'],
        secType=contract_details['secType'],
        exchange=contract_details['exchange'],
        currency=contract_details['currency']
    )
    ib.qualifyContracts(contract)
    if not contract.conId:
        print(f"Error: Could not resolve contract for {contract_details['symbol']}.")
        return []
    print(f"Successfully qualified contract for {contract_details['symbol']} (conId: {contract.conId})")

    # 3. Make a single, direct request for historical news
    start_str = start_date.strftime('%Y%m%d %H:%M:%S')
    end_str = end_date.strftime('%Y%m%d %H:%M:%S')
    print(f"\nRequesting news from {start_str} to {end_str}...")
    print("(Note: API is limited to the ~300 most recent articles in this range)")

    try:
        news_headlines = ib.reqHistoricalNews(
            conId=contract.conId,
            providerCodes=provider_codes,
            startDateTime=start_str,
            endDateTime=end_str,
            totalResults=100000
        )
    except Exception as e:
        print(f"  -> API Error fetching headlines: {e}")
        return []

    if not news_headlines:
        news_headlines = []

    print(f"\nTotal headlines received from API: {len(news_headlines)}")
    return news_headlines


def get_full_article(ib: IB, headline) -> str:
    """
    Fetches the full text of a single news article, with error handling.

    Args:
        ib: An active and connected ib_insync IB instance.
        headline: The news headline object.

    Returns:
        The full text of the article as a string.
    """
    try:
        news_article_body = ib.reqNewsArticle(
            providerCode=headline.providerCode,
            articleId=headline.articleId
        )
        return news_article_body.articleText if news_article_body else ""
    except Exception as e:
        # This will catch the "Not allowed" error and handle it gracefully
        # print(f"\nWarning: Could not fetch article {headline.articleId}. Reason: {e}")
        return "Full article text not available (subscription may be required)."
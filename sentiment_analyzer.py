from textblob import TextBlob

def analyze_sentiment(text: str) -> tuple[str, float]:
    """
    Analyzes the sentiment of a given text.

    Args:
        text: The text (headline or article) to analyze.

    Returns:
        A tuple containing the sentiment label ('Positive', 'Negative', 'Neutral')
        and the polarity score (from -1.0 to 1.0).
    """
    if not text:
        return 'Neutral', 0.0

    # Create a TextBlob object
    analysis = TextBlob(text)

    # Get the polarity score
    polarity = analysis.sentiment.polarity

    # Classify the sentiment based on the polarity score
    if polarity > 0.1:
        sentiment = 'Positive'
    elif polarity < -0.1:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return sentiment, polarity
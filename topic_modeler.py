# topic_modeler.py

import re
import nltk
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def download_nltk_packages():
    """Checks if necessary NLTK packages are downloaded and gets them if not."""
    required_packages = ['stopwords', 'punkt', 'wordnet', 'omw-1.4']
    for package in required_packages:
        try:
            if package in ['punkt', 'wordnet', 'omw-1.4']:
                 nltk.data.find(f'tokenizers/{package}' if package == 'punkt' else f'corpora/{package}')
            else:
                 nltk.data.find(f'corpora/{package}')
        except LookupError:
            print(f"Downloading NLTK package: {package}...")
            nltk.download(package)

def lemmatize_and_tokenize(text: str, lemmatizer):
    """Tokenizes and lemmatizes a string of text, returning a list of tokens."""
    tokens = nltk.word_tokenize(text.lower())
    return [lemmatizer.lemmatize(token) for token in tokens]

def find_common_phrases(texts: list, n: int = 5, top_k: int = 10) -> list:
    """Finds the most common n-grams (phrases) to identify boilerplate."""
    print(f"Identifying top {top_k} common {n}-word phrases to treat as stopwords...")
    all_ngrams = []
    for text in texts:
        # Simple tokenization for n-gram finding
        tokens = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        if len(tokens) >= n:
            for i in range(len(tokens) - n + 1):
                all_ngrams.append(tuple(tokens[i:i+n]))
    
    most_common = [ngram for ngram, count in Counter(all_ngrams).most_common(top_k)]
    
    # Add individual words from the common phrases to the stopword list
    boilerplate_stopwords = set()
    for phrase in most_common:
        print(f"  -> Identified common phrase: {' '.join(phrase)}")
        for word in phrase:
            boilerplate_stopwords.add(word)
    
    return list(boilerplate_stopwords)

def perform_topic_modeling(texts: list, num_topics: int) -> tuple[list, list]:
    """
    Performs LDA Topic Modeling using advanced pre-processing, including
    lemmatization, bigrams, and automated boilerplate removal.

    Args:
        texts: A list of strings, where each string is an article's content.
        num_topics: The number of topics to discover.

    Returns:
        A tuple containing:
        - A list of topic IDs for each text.
        - A list of the top words for each discovered topic.
    """
    if not texts:
        return [], []

    download_nltk_packages()

    # --- 1. Advanced Text Cleaning ---
    print("\nCleaning and pre-processing article text...")
    
    # Automatically find and add common boilerplate phrases to the stopword list
    boilerplate_words = find_common_phrases(texts)
    
    lemmatizer = nltk.stem.WordNetLemmatizer()
    nltk_stop_words = list(nltk.corpus.stopwords.words('english'))

    # --- Create a custom list of words to ignore ---
    # Add any other meaningless words you find to this list.
    # This list WILL always be never-ending .... :p
    CUSTOM_STOP_WORDS = [
        'com', 'story', 'news', 'fly', 'edt', 'theflyonthewall', '00', 'yet',
        'copyright', 'free', '30', 'br', 'apos', 'www', 'wsj', 'writes', 'take',
        'likely', 'wants', 'et', 'according', 'would', 'basis', 'due', 'god',
        'bless', 'https', 'states', 'starting', 'sent', 'instead', 'see', 'thefly',
        'go', 'rest', 'permalinks', 'entry', 'php', 'another', 'event', 'events',
        'like', 'well', 'may', 'us', 'final', 'noted', 'read', 'minutes', 'finished',
        'last', '000', 'years', 'year', 'plans', 'set', 'weeks', 'reference', 'href',
        'called', 'effects', 'near', 'says', 'say', 'make', '000', 'said', 'remains', 'also',
        'seen', 'get', 'time', 'generally', 'looking', 'nice', 'post', 'yesterday',
        'working', 'worked', 'works', 'made', 'great', 'gov', 'briefing', 'authors',
        'div', 'following', 'told', 'made', 'tell', 'comments', 'good', 'speaking',
        'http', 'able', 'place', 'many', 'slipped', 'shed', 'rose', 'higher', 'lower',
        'gains', 'falls', 'rising', 'falling', 'snapped', 'climbs', 'declines', 'closes',
        'fox', 'reuters', 'tells', 'interview', 'bring', 'reporter', 'work', 'long',
        'effect', 'previously', 'move', 'going', 'mod', 'link', 'avoiding', 'new',
        'old', 'done', 'want', 'along', 'accept', 'could', 'stance', 'announces',
        'meanwhile', 'marginally', 'fresh', 'buzz', 'dow', 'jones', 'trading', 'share',
        'pre', 'believed', 'method', 'expected', 'several', 'suggested', 'observed',
        'saying', 'give', 'really', 'earlier', 'think', 'live', 'know', 'held',
        'familiar', 'include', 'citing', 'keep', 'know', 'opted', 'among', 'known',
        'slightly', 'stated', 'shame', 'amp'
    ]
    
    stop_words = nltk_stop_words + CUSTOM_STOP_WORDS + boilerplate_words

    # --- 2. Lemmatization ---
    # Lemmatize AFTER finding boilerplate to catch the original phrases
    lemmatized_texts = [' '.join(lemmatize_and_tokenize(text, lemmatizer)) for text in texts]

    # --- 3. Vectorization using TF-IDF and Bigrams ---

    print(f"Performing Topic Modeling to discover {num_topics} topics...")

    # TF-IDF is more advanced than a simple count. It weighs words based on
    # how important they are to a specific document, not just how frequent they are.
    # Also, we ignore words that appear in less than 2 documents or more than 85% of documents.
    # The token_pattern considers words of 3+ letters.
    vectorizer = TfidfVectorizer(
        max_df=0.85, min_df=2, stop_words=stop_words,
        token_pattern=r'\b[a-zA-Z]{3,}\b'
    )

    dtm = vectorizer.fit_transform(lemmatized_texts)

    # 4. Build and fit the LDA model
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(dtm)

    # 5. Get the dominant topic for each document
    topic_results = lda.transform(dtm)
    dominant_topic_per_document = topic_results.argmax(axis=1)

    # 6. Get the top words/phrases for each topic for display
    feature_names = vectorizer.get_feature_names_out()
    top_words_per_topic = []
    for topic_idx, topic in enumerate(lda.components_):
        # Get the top 10 words/phrases for this topic
        top_words = [feature_names[i].replace(' ', '_') for i in topic.argsort()[:-10 - 1:-1]]
        top_words_per_topic.append(top_words)
        print(f"  -> Discovered Topic #{topic_idx}: {', '.join(top_words)}")

    return dominant_topic_per_document.tolist(), top_words_per_topic
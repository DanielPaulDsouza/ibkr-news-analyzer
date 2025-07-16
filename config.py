import datetime

# =============================================================================
# USER CONFIGURATION
# =============================================================================

# --- Connection Settings ---
# Make sure TWS or IB Gateway is running and API connections are enabled.
IB_HOST = '127.0.0.1'
IB_PORT = 7497  # 7497 for TWS Paper, 7496 for TWS Live, 4002 for IB Gateway Paper, 4001 for IB Gateway Live
CLIENT_ID = 123 # Use a unique client ID for each running script

# --- Contract To Analyze ---
# The stock/ETF symbol you want to fetch news for.
# In the CONTRACT_SYMBOLS you can add ONLY ONE or MULTIPLE contracts. 
CONTRACT_SYMBOLS = ['SPY', 'QQQ', 'DIA'] # Add 1 or many symbols, you want.
CONTRACT_TYPE = 'STK' # 'STK' for stock/ETF, 'FUT' for future, etc.
EXCHANGE = 'SMART'
CURRENCY = 'USD'

# --- News Search Parameters ---
# If you leave this list empty, then the Matches_Keywords column in the CSV
# will return false.
KEYWORDS_TO_SEARCH = [
    'earnings', 'fed', 'inflation', 'rate cut', 'geopolitical', 'supply chain',
    'buyback', 'guidance', 'downgrade', 'upgrade'
]

# --- Topic Modeling Settings ---
# This defines how many distinct topics the LDA model will try to discover
# in the collection of news articles. There is no single "correct" number.
# - A small number (e.g., 5) will result in very broad, high-level topics.
# - A large number (e.g., 20-30) will result in more specific, granular topics.
NUM_TOPICS = 20

# --- Time Frame for News Search ---
# This script uses naive local datetimes

# --- CHOOSE YOUR END DATE ---
# This will get the date and time right now in your local timezone.
# We subtract timedelta(days=1) to look at news ending yesterday.
# You can change the number of days to go back further or keep it 
# at 0 to have the end date at current time.
END_DATE = datetime.datetime.now() - datetime.timedelta(days=0)

# Set the START_DATE relative to your chosen END_DATE.
# Change this number to adjust to the period you want.
START_DATE = END_DATE - datetime.timedelta(days=100)

# --- Output File ---
# The script will create a filename based on the contract, start date and end date,
# and start time and end time.
OUTPUT_DIRECTORY = 'reports' # A subfolder to keep reports organized


#NOTES

"""
You can search between specific hours and specific minutes too and aren't limited
to searching between days. See example below for the code modification -

END_DATE = datetime.datetime(2025, 7, 5, 16, 0, 0) # July 5, 4:00 PM
# Search for the previous 2 hours
START_DATE = END_DATE - datetime.timedelta(hours=2)

"""
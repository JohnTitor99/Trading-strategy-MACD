# ----- BOT CONFIG -----

TOKEN = '6122912690:AAF95dCPgUdN27uNXSgrN4Fzmo9IU-WtWLo'
CHAT_ID = 862289283



# ----- BASE CONFIG -----

# currencies, crypto, metals, stocks
MARKET = [
    # currencies
    'EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'USDCAD=X', 'USDCHF=X', 'NZDUSD=X', 'EURJPY=X',
    'GBPJPY=X', 'EURGBP=X', 'EURCAD=X', 'EURCHF=X',
    # crypto
    'BTC-USD', 'ETH-USD',
    # futures (metals, oil, indices)
    'GC=F', 'SI=F', 'PL=F', 'HG=F', 'BZ=F', 'NQ=F', 'RTY=F', 'ES=F', 'YM=F',
    # stocks
    # 'INTC', 'PFE', 'PYPL', 'MRNA', 'DIS', 'ADBE',
    # 'TSLA', 'MSFT', 'GOOG', 'META', 'AMD', 'F', 'NVDA', 'AMZN', 'BAC', 'GM',
    # 'KO', 'JNJ', 'V', 'BA', 'IBM', 'MA', 'EBAY',
    # 'NFLX', 'ZM', 'PEP', 'COIN', 'DELL',
]

PERIOD = '3mo'
INTERVAL = '1h'



# ----- MACD SETTINGS -----

S_EMA = 12 # short ema
L_EMA = 26 # long ema
M_EMA = 9 # macd signal line ema
EMA_200 = 200

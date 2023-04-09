# ----- BOT CONFIG -----

TOKEN = '6122912690:AAF95dCPgUdN27uNXSgrN4Fzmo9IU-WtWLo'
chat_id = 862289283



# ----- BASE CONFIG -----

# currencies, crypto, metals, stocks
market = [
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

period = '3mo'
interval = '1h'


# macd settings
s_ema = 12 # short ema
l_ema = 26 # long ema
m_ema = 9 # macd signal line ema
ema_200 = 200


# stochastic settings
kp = 10 # stochastic period
mp = 3 # stochastic ma period

ema_21 = 21 # ema 21 for finding up and down trend
ema_50 = 50 # ema 50 for finding up and down trend

# Tg Bot for trading signals MACD

There are a lot of trading strategies using technical indicators, like MACD, Stochastic, Bollinger Bands, EMA etc. But whatever strategy you use, it's really exhausting to check all the currencies on market looking for good situation for you manually.

I've made this bot for automatic searching buy and sell signals using MACD indicator. It used for finding situations like below:

Buy:
![Screenshot](screenshot.png)

Sell:
![Screenshot](screenshot.png)
## General Info

This bot calculates indicators values for the last 3 month (it needed for getting precise values) using data from YFinanace API. It checks all currencies, crypto, futures and stocks you need every hour and send you in telegram message with currency pair and signal for buying or selling it. It's not perfect, so you need at least learn how this strategy works and look at the chart to see how really good signal is, check support and resistance levels etc. The video with this strategy explanation is at the bottom.
## Strategy Explanation

The strategy use MACD indicator and 200-period EMA. When MACD line (blue) crosses a signal line (red) below the zero line, it's a signal for buying. And when MACD line crosses a signal line above the zero line, then it's sell. But only MACD by itself is not so usefull. When it's downtrend and MACD gives signals for buying, then the most of this will be false signals. So, for avoiding this, we use a 200-period ema, which will help us to define a trend direction. Here's how the all strategy looks like: When MACD line crosses the signal line below the zero line and current price is above 200-period ema (it shows an uptrend), it's a signal for buying. Opposite for selling.
## Technologies

- numpy==1.24.2
- pandas==2.0.0
- pyTelegramBotAPI==4.10.0
- yfinance==0.2.14
## Running the project

At first, you should have installed Python on your computer. Not necessary, but advised to create a virtual environment, so you store your projects dependecies apart for avoiding conflicts beetwen packages.
```shell
pip install virtualenv
```
Clone this repository and open it in any text editor. To create virtualenv, run the command below in a Windows terminal:
```shell
python -m venv venv
```
or if you're on Linux or Mac:
```shell
virtualenv env
```
To activate virtualenv, run
```shell
venv\Scripts\activate.bat
```
Linux or Mac
```shell
source env/bin/active
```
Than install project dependencies
```shell
pip install -r requirements.txt
```
It is presumed that you have obtained an [API token with @BotFather](https://core.telegram.org/bots#botfather)

Now put your token in config.py file in variable 'TOKEN'. And put your message id in 'CHAT_ID'.

Then you can now run file 'trade_bot.py'. If you've done everything good, you'll receive a message from bot: 'Bot is now running. To see available commands: /help'.
# Sources

The strategy used in this bot was taken from this [video](https://www.youtube.com/watch?v=rf_EQvubKlk&list=LL&index=1).
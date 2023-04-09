import os
import telebot
import pandas as pd

import schedule
import time

import market
import macd

import config


bot = telebot.TeleBot(config.TOKEN)


pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)


# write the last row of each currency in file 'last_data.csv'
def get_last_data():
    # write data in csv file
    for pair in os.listdir('Market'):
        last_line = pd.read_csv(f"Market/{pair}").tail(1)
        last_line.to_csv('last_data.csv', index = False, header = False, mode='a')

    # write in txt file
    last_data = pd.read_csv('last_data.csv')
    with open('last_data.txt', 'w') as F:
        F.write(last_data.to_string(index=False))


def get_signals(signal):
    df = pd.read_csv('last_data.csv')
    # dict with signals; {'BTC-USD': '1.0'...}
    signals_dict = {row['Pair']: row[signal] for index, row in df.iterrows() if row[signal] != 0.0}

    return signals_dict


# chat_id = message.chat.id
def send_message():
    # get existing column names and make an empty 'last_data.csv'
    col_names = list(pd.read_csv('last_data.csv').columns.values)
    with open('last_data.csv', 'w') as f:
        f.write(','.join(col_names) + '\n')

    market.main() # get market data
    macd.main() # get macd and emas values
    get_last_data() # write the last row of each currency in file

    macd_signals = get_signals('macd_signal') # get a dict where currency is a key and signal is value

    message = '' # the message that will be sent in tg bot

    # create a message and send it
    for key, value in macd_signals.items():
        message += str(key) + ': ' + str(value) + '\n'
    if len(message) > 0:
        message = "MACD\n--------------------\n{0}\n".format(message)

    print(message)

    if len(message) > 0:
        bot.send_message(config.chat_id, message)


def main():
    # launch the script every hour
    # schedule.every().hour.at(":01").do(send_message)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    send_message()



if __name__ == '__main__':
    main()

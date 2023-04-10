import pandas as pd
import numpy as np

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import *


pd.set_option('display.max_rows', None) # when print a dataframe, it will print all columns, not only first and last 5 by default
pd.set_option('mode.chained_assignment', None) # avoiding a copy error


# to get ema we need to find sma at first
def get_sma(symbol_df):
    # calculation
    short_sma = pd.to_numeric(symbol_df['Close'].head(S_EMA)).mean()
    long_sma = pd.to_numeric(symbol_df['Close'].head(L_EMA)).mean()
    sma_200 = pd.to_numeric(symbol_df['Close'].head(EMA_200)).mean()

    # creating columns
    symbol_df[f"{S_EMA}ema"] = np.nan
    symbol_df[f"{L_EMA}ema"] = np.nan
    symbol_df[f"{EMA_200}ema"] = np.nan

    # write data in columns
    symbol_df.loc[S_EMA - 1, f"{S_EMA}ema"] = short_sma
    symbol_df.loc[L_EMA - 1, f"{L_EMA}ema"] = long_sma
    symbol_df.loc[EMA_200 - 1, f"{EMA_200}ema"] = sma_200


# this func finds ema for all required periods
def get_ema(symbol_df, ema_period, index):
    e = index
    for i in range(len(symbol_df) - index):
        multiplier = 2 / (ema_period + 1)
        ema_value = (float(symbol_df.iloc[e]['Close']) * multiplier) + (float(symbol_df.iloc[e-1][f"{ema_period}ema"]) * (1 - multiplier))
        symbol_df.loc[e, f"{ema_period}ema"] = ema_value
        e += 1


# macd line equals to 12ema - 26ema
def macd_line(symbol_df, index):
    h = index
    for i in range(len(symbol_df) - index):
        macd = symbol_df.iloc[h]['12ema'] - symbol_df.iloc[h]['26ema']
        symbol_df.loc[h, 'macd'] = macd
        h += 1


# macd signal line is ema of macd line, so it needs to create sma first
def macd_signal_line_sma(symbol_df):
    signal_line_sma = pd.to_numeric(symbol_df['macd'].head(M_EMA + L_EMA - 1)).mean()
    symbol_df['signal_line'] = np.nan
    symbol_df.loc[M_EMA + L_EMA - 2, 'signal_line'] = signal_line_sma


# 9 period ema of macd line
def macd_signal_line(symbol_df, index):
    # calculating macd signal line
    g = index
    for i in range(len(symbol_df) - index):
        m_multiplier = 2 / (M_EMA + 1)
        signal_line = (float(symbol_df.iloc[g]['macd']) * m_multiplier) + (float(symbol_df.iloc[g-1]['signal_line']) * (1 - m_multiplier))
        symbol_df.loc[g, 'signal_line'] = signal_line
        g += 1


# if values satisfy a required conditions, in column 'macd_signal' will be 1.0 if buy and -1.0 if sell; else 0.0
def macd_signal(symbol_df, index):
    n = index
    for i in range(n, len(symbol_df)):
        if float(symbol_df.iloc[i]['macd']) <= 0 and \
            float(symbol_df.iloc[i]['macd']) > float(symbol_df.iloc[i]['signal_line']) and \
            float(symbol_df.iloc[i-1]['macd']) < float(symbol_df.iloc[i-1]['signal_line']) and \
            float(symbol_df.iloc[i]['Close']) > float(symbol_df.iloc[i]['200ema']):
            symbol_df.loc[i, 'macd_signal'] = 1.0

        elif  float(symbol_df.iloc[i]['macd']) >= 0 and \
            float(symbol_df.iloc[i]['macd']) < float(symbol_df.iloc[i]['signal_line']) and \
            float(symbol_df.iloc[i-1]['macd']) > float(symbol_df.iloc[i-1]['signal_line']) and \
            float(symbol_df.iloc[i]['Close']) < float(symbol_df.iloc[i]['200ema']):
            symbol_df.loc[i, 'macd_signal'] = -1.0
        else:
            symbol_df.loc[i, 'macd_signal'] = 0.0


# get rows that don't have indicators values
def get_new_data(symbol_df):
    new_df = symbol_df[0:0] # a new df with needed rows

    i = -1
    # get rows without indicators values + 1 previous with indicators (for calculating ema must be its previous value)
    while True:
        if str(symbol_df.iloc[i]['macd']) == str(np.nan):
            new_df.loc[len(new_df)] = symbol_df.iloc[i]
        else:
            new_df.loc[len(new_df)] = symbol_df.iloc[i]
            break
        
        i -= 1

    new_df = new_df.iloc[::-1] # reverse a df
    new_df = new_df.reset_index(drop=True)

    return new_df


def macd_trade_logic():
    count = len(os.listdir('Market')) - 1

    # write indicators values in files for each currrency
    for pair in os.listdir('Market'):
        pair = pair.replace('.csv', '')
        symbol_df = pd.read_csv(f"Market/{pair}.csv")

        cols = list(symbol_df.columns.values)
        
        # calculations in missing rows until current date if file already exists
        if 'macd' in cols:
            new_df = None
            # calculate required data for missing rows
            if str(symbol_df.iloc[-1]['macd']) == str(np.nan):
                new_df = get_new_data(symbol_df)

                get_ema(new_df, S_EMA, 1) # short ema
                get_ema(new_df, L_EMA, 1) # long ema
                get_ema(new_df, EMA_200, 1) # 200 ema
                macd_line(new_df, 1)
                macd_signal_line(new_df, 1)
                macd_signal(new_df, 1)

            # write data in file
            if new_df is not None:
                # deleting rows with no indicators data to replace them
                old_data = pd.read_csv(f"Market/{pair}.csv")
                old_data.drop(old_data.tail(len(new_df)).index, inplace=True)
                old_data.to_csv(f"Market/{pair}.csv", index=False)

                new_df.to_csv(f"Market/{pair}.csv", mode='a', header=False, index=False) # add new rows to csv file

            # print progress of process
            if count > 0:
                print(f"MACD | {pair} - done | Left: {count}")
            else:
                print(f"MACD | {pair} - done | End\n")

        # calculation for all rows
        else:
            get_sma(symbol_df) # first sma (for calculating ema its required the previous ema value, so very first value must be sma)
            get_ema(symbol_df, S_EMA, S_EMA) # short ema
            get_ema(symbol_df, L_EMA, L_EMA) # long ema
            get_ema(symbol_df, EMA_200, EMA_200) # 200 period ema
            macd_line(symbol_df, L_EMA - 1)
            macd_signal_line_sma(symbol_df)
            macd_signal_line(symbol_df, M_EMA + L_EMA - 1)
            macd_signal(symbol_df, EMA_200 - 1)

            # write data in file
            if count > 0:
                print(f"MACD | {pair} - done | Left: {count}")
            else:
                print(f"MACD | {pair} - done | End\n")

            symbol_df.to_csv(f"Market/{pair}.csv", index=False)

        count -= 1


def main():
    macd_trade_logic()



if __name__ == "__main__":
    main()

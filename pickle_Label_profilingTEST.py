import pickle
import pandas as pd
import yfinance as yf
import datetime
from pandas_profiling import ProfileReport


# import numpy as np


def sp500():


    """
    creating a date structure
    and downloading the S&P500/Stocks prices as the date structure
    """
    start = datetime.datetime(2021, 1, 15)
    end = datetime.datetime(2021, 6, 30)
    data = pd.DataFrame(yf.download('^GSPC', start, end))
    prices = data.stack().reset_index().rename(index=str, columns={"level_1": "Symbol"}).sort_values(['Symbol', 'Date'])

    '''
    take the unique values and convert them to 'time'

    '''
    dates = prices['Date'].unique()
    dates = pd.to_datetime(dates)
    dates = dates.strftime("%d %b %Y")

    data.index = dates
    # x = pd.date_range(start=start, end=end)
    # print(data.index)
    # snp500Indexes = data.index
    # SP500 = reader.DataReader(['sp500'], 'fred', start, end)

    '''
    SP500 Close Prices df as 'close'
    '''
    close = data['Close']

    return close, data


def data_frame_fix(close, sp500_data, senti_df, df):


    """

        insert the dates to the DF's

    """
    # df = df.to_string(df) # very dangerous

    dates_index = pd.to_datetime(df.index)
    dates_index = dates_index.strftime("%d %b %Y")
    df.index = dates_index
    df.insert(loc=1, column="Date", value=dates_index)
    df.insert(loc=0, column="Close", value=close)

    '''
        sort the DF by dates column
    '''

    '''
    df = df.rename(columns={'Dates': 'Close'}) #rename a column 

    '''

    '''
    Trying to insert the 'Close' prices to the original DF.
    (also to fix the NaN values)

    '''
    sp500_dates = pd.to_datetime(sp500_data.index)
    sp500_dates = sp500_dates.strftime("%d %b %Y")

    for date in range(len(df['Date'])):
        for d in range(len(sp500_dates)):
            if str(df['Date'][date]) == str(sp500_dates[d]):
                df.at[df['Date'][date], 'Close'] = sp500_data.at[sp500_dates[d], 'Close']

    for date in range(len(df['Date'])):
        if str(df.at[df['Date'][date], 'Close']) == 'nan':
            df.at[df['Date'][date], 'Close'] = int(df.at[df['Date'][date - 1], 'Close'])

    # df = df.reset_index() # reset the index to 0,1,2,3

    # 'fix' the sentiment DATA FRAME
    dates_index = pd.to_datetime(senti_df.index)
    dates_index = dates_index.strftime("%d %b %Y")
    senti_df.index = dates_index
    senti_df.insert(loc=0, column="S&P500", value=df['Close'])
    senti_df.insert(loc=0, column="Dates", value=df['Date'])
    df2 = senti_df
    # df2 = df2.rename({0:'Sentiment'})
    # df['Date'] = pd.to_datetime(df['Date'])

    df.index = pd.to_datetime(df.index)
    df.index = df.index.strftime("%d %b %Y")
    # df2 = df2.drop(columns=['Dates'])

    return df, df2


def DataProfiler(df, senti_df):

    # Sort by dates
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')
    senti_df['Dates'] = pd.to_datetime(senti_df['Dates'])
    senti_df = senti_df.sort_values(by='Dates')

    # df = df.drop(columns=['Date']) to delete specific column
    profile = ProfileReport(df)
    profile.to_file("NGRAM report.html")

    profile2 = ProfileReport(senti_df)
    profile2.to_file("Sentimental report.html")

    # correlations = profile.description_set["correlations"]
    # print(correlations.keys(), '\n', correlations["pearson"])

    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print(df.iloc[:, 0:10]) #  SHOWS ALL DF


def xlsxwritter(df, senti_df):
    try:
        df.to_excel("Ngram report.xlsx")
        senti_df.to_excel("Sentimental report.xlsx")
    except ValueError:
        print("This sheet is too big...")






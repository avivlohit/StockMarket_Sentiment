'''


        DATE |NGRAM1        |NGRAM2...NGRAMN
        08.03|count(ngram1)|


        dir={date:[(ngrams),(ngrams),,,],date2:[(ngrams),(ngrams),,,],...}


        Sentiment:

        dir= {date1:0.54,date2:0.012...}

'''

import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import pickle
from nltk.corpus import stopwords
import pickle_Label_profilingTEST as plpTEST


# import numpy as np

def data_organizer():
    stop_words = stopwords.words('english')

    data = pd.read_excel('theData (copy).xlsx', usecols=[1, 2], header=None)

    # for test, This is make you able to control the amount of data you want to forward
    data = data.iloc[0:150, :]

    date = data.iloc[:, 0]
    date = date.str.split(',')

    tmplst = []
    # Cleaning the date string to just 'Jun 13' for example
    for d in date:
        tmp = d[0:2]
        tmp = ''.join(tmp)
        tmplst.append(tmp)
    data.iloc[:, 0] = tmplst
    '''
     dates = data.iloc[:, 0] # all the dates
    '''
    unique_dates = data.iloc[:, 0].unique()
    unique_dates.sort()
    headlines_dict = {}

    '''
     headlines = data.iloc[:, 1] # all the Headlines
    '''
    # Creating the list for NGRAM procces
    headlines = data.iloc[:, 1]
    headlines = ' '.join(str(i) for i in headlines)
    headlines = headlines.split()
    headlines = [headline for headline in headlines if
                 headline.isalnum() and headline not in stop_words]  # all the headlines split with only alnum(NO !@#,.?/)

    headlines = ' '.join(headlines)  # all the headlines as 1 string to make it NGRAM
    date_headline_tuplelst = list(zip(data.iloc[:, 0], data.iloc[:, 1]))  # make them as tuple (date,headline)

    # creating a dictionary that hold a unique date with his relative headlines
    for unique_date in unique_dates:
        tmplst = []
        for date, headline in date_headline_tuplelst:

            # if same date add the headline to the list
            if unique_date == date:
                tmplst.append(headline)

        # Adding the templst of the headlines as the value of the same Key of the relative date. unique:headlines
        headlines_dict[unique_date] = tmplst

    print('DICT OF ALL Unique days and Headlines has BEEN CREATED')

    return headlines_dict, headlines, unique_dates


def sentiment(headlines_dict):
    """
        we want to calculate the avarage sentiment of
        each day and to correlation
        test to the actual price.
        We got a dictionary  that holds unique_date:[list of headlines].
    """

    # create new dir
    avarage_dict = {}
    sum = 0
    print('Calculate the sentiment avarage')
    for date, headlinelst in headlines_dict.items():

        print('{:.0%}'.format(sum / len(headlines_dict.keys())))
        sum += 1
        ss_sum = 0
        headlines = headlines_dict[date]  # lst of all the headline in the same date
        for headline in headlines:
            sid = SentimentIntensityAnalyzer()
            ss = sid.polarity_scores(headline)
            ss_sum += ss['compound']

        avarage = (ss_sum / len(headlines))

        avarage_dict[date] = avarage
    return avarage_dict


def ngram(headlines_dict, headlines):
    # -------------------------------------------------------------------
    #   Ngram
    #
    # --------------------------------------------------------------------
    headlines_dict_ngram = headlines_dict
    # STOP WORDS FOR BETTER RUN :3
    stop_words = stopwords.words('english')

    # implanting Ngram by NLTK for from all data
    NGRAMS_ALL_DATA = list(ngrams(sequence=nltk.word_tokenize(headlines), n=3))  # NGRAMS OF ALL DATA
    print('NGRAM OF ALL DATA has BEEN CREATED')

    # CREATE the ENV(environment) for NGRAMS per day
    for date, v in headlines_dict_ngram.items():
        # NGRAMS OF THE DATA PER DAY
        tmp_headlines = list(headlines_dict_ngram[date])
        tmp_headlines = ' '.join(str(i) for i in tmp_headlines)
        tmp_headlines = tmp_headlines.split()
        tmp_headlines = [t for t in tmp_headlines if
                         t.isalnum() and t not in stop_words]  # all the headlines split with only alnum(NO !@#,.?/)

        tmp_headlines = ' '.join(tmp_headlines)  # all the headlines as 1 str
        NGRAMS_V = list(ngrams(sequence=nltk.word_tokenize(tmp_headlines), n=3))  # NGRAMS OF THE DATA PER DAY
        # make the NGRAMS per day AS STRINGS ('a' , 'b' , 'c') ---> (a b c)
        lst = []
        for a, b, c in NGRAMS_V:
            tmpstring = a + ' ' + b + ' ' + c
            lst.append(tmpstring)
        headlines_dict_ngram[date] = lst

        # make the NGRAMS ALL DATA AS STRINGS ('a' , 'b' , 'c') ---> (a b c)

        lst = []
        for a, b, c in NGRAMS_ALL_DATA:  # ('a','b','c')
            tmpstring = a + ' ' + b + ' ' + c
            lst.append(tmpstring)

    # make unique list of ngrams
    lst_set = set(lst)
    unique_ngrams = list(lst_set)
    print('NGRAM OF ALL DATA by DATES has BEEN CREATED')

    return unique_ngrams, headlines_dict_ngram


def pd_organizer(unique_dates, unique_ngrams, headlines_dict_ngram, avarage_dict):
    df = pd.DataFrame(index=unique_dates, columns=unique_ngrams)

    senti_df = pd.DataFrame.from_dict(avarage_dict, orient='index')

    print('Starting the SUM function...')
    sum = 0
    for date, n_list in headlines_dict_ngram.items():
        print('{:.0%}'.format(sum / len(headlines_dict_ngram.keys())))
        sum += 1
        for n in range(len(n_list)):
            df.at[date, str(n_list[n])] = headlines_dict_ngram[date].count(n_list[n])

    # df = df.fillna(0)

    # make the value as int. ===> PD profiling test
    print('Printing the DATA FRAME.\nPrinting the DATA FRAME..\nPrinting the DATA FRAME...')

    return df, senti_df

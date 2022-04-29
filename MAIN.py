

import pickle_Label_profilingTEST as plpTEST
import data_sentiment_ngram


def main():
    headlines_dict, headlines, unique_dates = data_sentiment_ngram.data_organizer()
    unique_ngrams, headlines_dict_ngram = data_sentiment_ngram.ngram(headlines_dict, headlines)
    avarage_dict = data_sentiment_ngram.sentiment(headlines_dict)
    df, senti_df = data_sentiment_ngram.pd_organizer(unique_dates, unique_ngrams, headlines_dict_ngram, avarage_dict)

    #  Another File.

    _, close, sp500_data = plpTEST.sp500() # _ means no need to this var
    df, senti_df = plpTEST.data_frame_fix(close, sp500_data, senti_df, df)
    plpTEST.DataProfiler(df, senti_df)
    plpTEST.xlsxwritter(df, senti_df)

main()



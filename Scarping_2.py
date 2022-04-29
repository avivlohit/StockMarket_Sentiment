from bs4 import BeautifulSoup
import requests
# import xlsxwriter
# import pandas as pd
# import csv
from datetime import datetime
from datetime import timedelta


def main():
    theData = HTMLScraping_PRNEWS()


def HTMLScraping_PRNEWS():
    headlinesList = []
    httpRequest = requests.Session()
    switch = True

    while switch:
        try:

            # input start and end "d/m/Y"
            # prnews working with pages, each day has avarage of 2 pages of news.

            print("Please enter the dates in this format: d/m/Y")
            date_start = input("please enter the starting date you want to gather data from")
            date_end = input("please enter the ending date you want to gather data")

            # date_start = '05/05/2000'
            # date_end = '06/05/2000'

            date_start = datetime.strptime(date_start, "%d/%m/%Y")  # convert
            date_end = datetime.strptime(date_end, "%d/%m/%Y")  # convert
            switch = False


        except ValueError:
            print('Try again please')


    delta = timedelta(days=1)
    dates = []

    while date_start <= date_end:
        date = date_start.strftime("%d %m %Y")
        dates.append(date)
        date_start += delta

    for date in dates:
        page = 1
        day = date.split(' ')[0]
        month = date.split(' ')[1]
        print(day, month)

        while page <= 2:
            url = "https://www.prnewswire.com/news-releases/news-releases-list/?page=" + str(
                page) + "&pagesize=100&month=0" + month + "&day=" + day + "&year=2021&hour=00"

            htmlCode = httpRequest.get(url)
            coverPage = htmlCode.text

            print(url + "\n" + "Month: " + str(month), ",Day: " + str(day), ",Page: " + str(page))

            soup1 = BeautifulSoup(coverPage, "lxml")
            headLines = soup1.find_all('h3')
            if headLines == "[<h3>Journalists and Bloggers</h3>]" or len(headLines) == 0:  # cleaning from empty pages
                page += 1
                continue

            for headline in headLines:
                tmpHeadline = headline.text  # convert the html format to text
                if tmpHeadline == "Journalists and Bloggers":  # cleaning from empty pages
                    continue
                tmpHeadline = tmpHeadline.split("\n")  # split the string in the \n and making it as list
                tmpHeadline = [h for h in tmpHeadline if h != '']  # Cleaning the '' from the lists
                # print(tmpHeadline)
                if tmpHeadline in headlinesList or len(tmpHeadline) <= 1:  # cleaning from same headlines
                    continue
                elif tmpHeadline not in headlinesList:
                    headlinesList.append(tmpHeadline)
            page += 1

    print(headlinesList)
    return headlinesList


'''
1)Need to add functions of other websites and scarp them all, then write it as different excel format automaticly


'''

main()

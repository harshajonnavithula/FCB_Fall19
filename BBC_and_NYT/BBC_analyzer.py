from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
import requests
import os
''' Author: Matt Krivansky
    Date: 11/05/2019

    This python3 script will be used to analyze the BBC data collected from BBC_scraper.py. 
'''
def csv_to_list(filename):
    with open(filename, 'r') as file:
        datareader = csv.reader(file, delimiter = ',')
        data = []
        for row in datareader:
            data.append(row)    
        return data

def sort_keyword_totals():
    sorted_output = open('sorted_keyword_totals.csv', 'w')
    unsorted_keyword_totals = csv_to_list('keyword_totals.csv')
    sorted_keyword_totals = []
    nonzero_keyword_totals = []
    for i in range(len(unsorted_keyword_totals)):
        if int(unsorted_keyword_totals[i][1]) > 0:
            nonzero_keyword_totals.append(unsorted_keyword_totals[i])
    i = 0
    lowest = int(nonzero_keyword_totals[0][1])
    lowest_keyword = nonzero_keyword_totals[0]

    while len(nonzero_keyword_totals) > 0:
        if  int(nonzero_keyword_totals[i][1]) < lowest:
            lowest = int(nonzero_keyword_totals[i][1])
            lowest_keyword = nonzero_keyword_totals[i]
        i += 1
        if i == len(nonzero_keyword_totals):
            sorted_keyword_totals.append(lowest_keyword)
            nonzero_keyword_totals.remove(lowest_keyword)
            if nonzero_keyword_totals:
                lowest = int(nonzero_keyword_totals[0][1])
                lowest_keyword = nonzero_keyword_totals[0]
            i = 0
    print(sorted_keyword_totals)
    writer = csv.writer(sorted_output)
    writer.writerows(sorted_keyword_totals)   
    sorted_output.close()

sort_keyword_totals()
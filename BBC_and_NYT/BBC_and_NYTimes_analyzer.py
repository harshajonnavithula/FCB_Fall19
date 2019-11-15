from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
import requests
import os
import time
''' Author: Matt Krivansky
    Date: 11/05/2019

    This python3 script will be used to analyze the BBC data collected from BBC_scraper.py. 
'''
list_of_files = []
def make_files_list():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if f.endswith('.csv') and f.startswith('20'):
            list_of_files.append(str(f))

def main():
    print('Initializing analysis...')
    time.sleep(3)
    print('\tIntitialized.')
    time.sleep(3)
    print('\tGenerating list of files...')
    make_files_list()
    print('\n')
    print('\tProceeding with analysis.')
    time.sleep(2)
    keywords = open('keywords.txt', 'r')
    j = 0
    data_list = [[]]
    print('Counting:')
    time.sleep(1)
    for keyword in keywords:
        print('\t>> {}'.format(keyword))
        time.sleep(0.5)
        keyword = keyword.strip('\n')
        count = 0
        for i in range(len(list_of_files)):
            csv_file = open(list_of_files[i], 'r')
            csv_list = list(csv.reader(csv_file))
            del csv_list[0]
            count += int(csv_list[j][1])
        data_list.append([keyword, count])
        j += 1
    del data_list[0]
    print('Counting terminated.')
    print('\n')
    time.sleep(1)
    print('Finding top hits...')
    time.sleep(2)
    sort_data(data_list)
    print('Analysis Complete!')

def sort_data(data):
    lowest_count = data[0][1]
    lowest = data[0]
    ordered_data = []
    i = 0
    print('\n')
    while len(data) > 0:
        if  data[i][1] < lowest_count:
            lowest_count = data[i][1]
            lowest = data[i]
        i += 1
        if i == len(data):
            ordered_data.append(lowest)
            data.remove(lowest)
            if data:
                lowest_count = data[0][1]
                lowest = data[0]
            i = 0
    output = open('BBC_and_NYT_keyword_totals.csv', 'w+')
    writer = csv.writer(output)
    writer.writerows(ordered_data)
    print('Top hits!')
    time.sleep(0.5)
    print('\t1. {}: {}'.format(ordered_data[len(ordered_data) - 1][0], ordered_data[len(ordered_data) - 1][1]))
    time.sleep(0.5)
    print('\t2. {}: {}'.format(ordered_data[len(ordered_data) - 2][0], ordered_data[len(ordered_data) - 2][1]))
    time.sleep(0.5)
    print('\t3. {}: {}'.format(ordered_data[len(ordered_data) - 3][0], ordered_data[len(ordered_data) - 3][1]))
    time.sleep(0.5)
    print('\t4. {}: {}'.format(ordered_data[len(ordered_data) - 4][0], ordered_data[len(ordered_data) - 4][1]))
    time.sleep(0.5)
    print('\t5. {}: {}'.format(ordered_data[len(ordered_data) - 5][0], ordered_data[len(ordered_data) - 5][1]))
    time.sleep(0.5)

main()
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
import requests
import os
import time
import math
import nltk 
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import wordcloud
from wordcloud import WordCloud, STOPWORDS
import numpy as npy
import PIL
from PIL import Image

''' Author: Matt Krivansky
    Date: 11/05/2019

    This python3 script will be used to analyze the BBC data collected from BBC_scraper.py. 
'''
list_of_files = []
keywords = []
def make_files_list(file_ext):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if f.endswith(file_ext) and f.startswith('20'):
            list_of_files.append(str(f))

def main():
    print('Initializing analysis...')
    time.sleep(3)
    print('\tIntitialized.')
    time.sleep(3)
    print('\tGenerating list of files...')
    make_files_list('.csv')
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
    sort_data(data_list, 'BBC_and_NYT_keyword_totals.csv')
    print('Analysis Complete!')

def sort_data(data, output):
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
    output = open(output, 'w+')
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

def freq_counter():
    make_files_list('.txt')
    print(len(list_of_files))
    words = []
    words_count = []
    for i in range(len(list_of_files)):
        print(list_of_files[i])
        with open(list_of_files[i]) as text:
            count = 0
            for line in text:
                sentence = line.split()
                for word in sentence:
                    count += 1
                    word = replace_characters(word)
                    word = word.lower()
                    if word not in words:
                        words.append(word)
                        words_count.append([word, 1])
                    else:
                        for j in range(len(words_count)):
                            if str(words_count[j][0]) == str(word):
                                words_count[j][1] += 1
    sort_data(words_count, 'temp_keywords_tfidf.csv')

def replace_characters(text):
    characters = ['.', ',', ':', ':', '\"', '!', '"', "'", "(", ")", '/', '[', ']', '-', "\'"]
    for i in characters:
        text = text.replace(i, '')
    return text

def tf(keyword, filename):
    n = 0
    count = 0
    with open(filename) as file:
        for line in file:
            sentence = line.split()
            for word in sentence:
                if str(word) == str(keyword):
                    n += 1
                count += 1
    if (n != 0) and (count != 0):
        tf = n / count
        return tf
    return 0

def idf(keyword):
    make_files_list('.txt')
    N = len(list_of_files)
    df = 0
    for i in range(len(list_of_files)):
        found = False
        with open(list_of_files[i]) as file:
            if found:
                continue
            else:
                for line in file:
                    sentence = line.split()
                    if found:
                        break
                    for word in sentence:
                        if str(word) == str(keyword) and not found:
                            df += 1
                            found = True
                            break
    if df != 0:
        idf = math.log10(N / df)
    else:
        idf = 0
    return idf

stop_words_list = []
def make_stop_words_list():
    stop_words_list = stopwords.words("english")
    stop_words_list.append('dont')
    stop_words_list.append('a')
    stop_words_list.append('i')
    stop_words_list.append('cant')
    stop_words_list.append('wont')
    stop_words_list.append('isnt')
    stop_words_list.append('didnt')
    stop_words_list.append('doesnt')
    stop_words_list.append('couldnt')
    stop_words_list.append('couldve')
    stop_words_list.append('im')
    stop_words_list.append('ive')
    stop_words_list.append('theres')
    stop_words_list.append('wasnt')
    stop_words_list.append('wouldnt')
    stop_words_list.append('also')

def identify_keywords():
    make_files_list('.txt')
    with open('keywords_tfidf.csv') as freq_csv:
        keywords = list(csv.reader(freq_csv))[26512:]
        for i in range(len(keywords)):
            del keywords[i][1]
            keywords[i] = keywords[i][0]
        return keywords

def tfidf():
    print('Calculating TFIDF score...\n')
    time.sleep(1)
    words = []
    words_tfidf = []
    print('Generating stopwords...\n')
    make_stop_words_list()
    time.sleep(1)
    print('Creating keywords list...\n')
    keywords = identify_keywords()
    time.sleep(1)
    print('Beginning TFIDF Sequence:')
    for i in range(len(keywords)):
        keyword = replace_characters(keywords[i])
        keyword = keyword.lower()
        if keyword not in words and keyword not in stop_words_list:
            words.append(keyword)
            tfidf = tf(keyword, list_of_files[i]) * idf(keyword)
            print('\t', keyword, ': ', tfidf)
            words_tfidf.append([keyword, tfidf])
    sort_data(words_tfidf, 'tfidf.csv')

d = {}
def make_wordcloud(file):
    with open(file) as data:
        data = list(csv.reader(data))
        for keyword, score in data:
            d[keyword] = float(score) 
        wordcloud = WordCloud(background_color = "white")
        wordcloud.generate_from_frequencies(frequencies = d)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

#main()
#freq_counter()
#idf('food')
#tf('food', '20191022-why-bolivia-is-the-next-food-hotspot.txt')
#make_stop_words_list()
#identify_keywords()
#tfidf()
#make_wordcloud('keywords_freq_count.csv')
#make_wordcloud('sorted_keyword_totals.csv')
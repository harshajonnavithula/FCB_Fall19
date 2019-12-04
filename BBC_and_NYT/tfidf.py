'''
    Calculates TF-IDF for BBC and NYT article text.

    The formulas I used was from https://www.freecodecamp.org/news/how-to-process-textual-data-using-tf-idf-in-python-cd2bbc0a94a3/

    Matthew Krivansky
'''
import os
from nltk.corpus import stopwords
import csv
import math


def tfidf(filename):
    print('Calculating TFIDF score...\n')
    words = []
    words_tfidf = []
    print('Generating stopwords...\n')
    make_stop_words_list()
    print('Creating keywords list...\n')
    keywords = identify_keywords()
    print('Beginning TFIDF Sequence:')
    for i in range(len(keywords)):
        keyword = replace_characters(keywords[i])
        keyword = keyword.lower()
        if keyword not in words and keyword not in stop_words_list:
            words.append(keyword)
            tfidf = tf(keyword, list_of_files[i]) * idf(keyword)
            print('\t', keyword, ': ', tfidf)
            words_tfidf.append([keyword, tfidf])
    sort_data(words_tfidf, filename)

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

list_of_files = []
keywords = []
def make_files_list(file_ext):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if f.endswith(file_ext) and f.startswith('20'):
            list_of_files.append(str(f))

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

def replace_characters(text):
    characters = ['.', ',', ':', ':', '\"', '!', '"', "'", "(", ")", '/', '[', ']', '-', "\'"]
    for i in characters:
        text = text.replace(i, '')
    return text

def identify_keywords():
    make_files_list('.txt')
    with open('keywords_tfidf.csv') as freq_csv:
        keywords = list(csv.reader(freq_csv))[26512:]
        for i in range(len(keywords)):
            del keywords[i][1]
            keywords[i] = keywords[i][0]
        return keywords

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
    print('\t1. {}: {}'.format(ordered_data[len(ordered_data) - 1][0], ordered_data[len(ordered_data) - 1][1]))
    print('\t2. {}: {}'.format(ordered_data[len(ordered_data) - 2][0], ordered_data[len(ordered_data) - 2][1]))
    print('\t3. {}: {}'.format(ordered_data[len(ordered_data) - 3][0], ordered_data[len(ordered_data) - 3][1]))
    print('\t4. {}: {}'.format(ordered_data[len(ordered_data) - 4][0], ordered_data[len(ordered_data) - 4][1]))
    print('\t5. {}: {}'.format(ordered_data[len(ordered_data) - 5][0], ordered_data[len(ordered_data) - 5][1]))

tf_idf_output_filename = input('Enter the name for the TF-IDF output file: ')
tfidf(tf_idf_output_filename)
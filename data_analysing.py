import os
import subprocess

import pandas as pd
import numpy as np
from wordcloud import WordCloud
import ntlk
import matplotlib.pyplot as plt
import sklearn as sk
from sklearn.model_selection import train_test_split
import nltk
nltk.download('stopwords')


def main():
    df = get_data("Dataset\hotel-reviews.csv")
    #describe_data(df)
    #print("Training data converted to lower case: ")
    #data_to_lower(df)
    #describe_data(df)
    #convert_words(df)
    #df.to_csv(r'Dataset/hotel-reviews-cleansed.csv', index = False)
    split_data(df)
    return

def split_data(df):
    train, test = train_test_split(df, test_size=0.3) #70, 30 train test split
    describe_data(train)
    describe_data(test)
    test.to_csv(r'Dataset/test.csv', index=False)
    train.to_csv(r'Dataset/train.csv', index=False)
    return

def convert_words(df):
    dataset = df
    eng_stopwords = set(stopwords.words("english"))
    sub_text = dataset[dataset.Is_Response == "not happy"].Description.values
    non_text = dataset[dataset.Is_Response == "happy"].Description.values
    from collections import Counter
    c_sub = Counter()
    for sent in sub_text:
        c_sub.update(sent.split())
    c_non = Counter()
    for sent in non_text:
        c_non.update(sent.split())
    inter_words = set(c_non).intersection(set(c_sub))
    inter_words.difference_update(eng_stopwords)
    print("Common words use in both: %d" % (len(inter_words)))
    inter_words
    sus_wd = []
    for wd in inter_words:
        if c_sub[wd] >= c_non[wd] * 3:
            sus_wd.append(wd)
    print(sus_wd)

def describe_data(df):
    l_train = len(df)
    print(df.head(10))
    print(df.info())
    print(l_train)
    print("Label distribution of training data:")
    print((df.Is_Response.value_counts() / l_train))
    return

def data_to_lower(df):
    df.Description = df.Description.str.lower()
    return

def impute_data(df):
    print("Null check on training data:")
    null_check = df.isna().sum()
    if (null_check):
        print("Null Values Found")
    return df

def plot_data(df):
    # matplotlib inline
    dataset = df
    eng_stopwords = set(stopwords.words("english"))

    plt.figure(figsize=(20, 20))
    plt.subplot(121)
    sub_text = dataset[dataset.Is_Response == "happy"].Description.values
    subwc = WordCloud(background_color="black", max_words=2000, stopwords=eng_stopwords)
    subwc.generate(" ".join(sub_text))
    plt.axis("off")
    plt.title("Words frequented of happy reviews", fontsize=20)
    plt.imshow(subwc.recolor(colormap='gist_earth', random_state=244), alpha=0.98)
    plt.subplot(122)
    non_text = dataset[dataset.Is_Response == "not happy"].Description.values
    nonwc = WordCloud(background_color="black", max_words=2000, stopwords=eng_stopwords)
    nonwc.generate(" ".join(non_text))
    plt.axis("off")
    plt.title("Words frequented of unhappy reviews", fontsize=20)
    plt.imshow(nonwc.recolor(colormap='Reds', random_state=244), alpha=0.98)
    plt.savefig('Dataset/word_cloud.png', bbox_inches='tight', dpi=600)
    return

def get_data(name):
    #Get the data, from local csv
    if os.path.exists(name):
        print(name + " found locally")
        df = pd.read_csv(name)

        return df
    else:
        print("File does not exist")
        return 0

if __name__ == "__main__":
    main()
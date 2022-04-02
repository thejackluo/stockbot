"""
The goal of this is to rank individual sentences based on the word approach 
and calculate the polarity of the sentence based on the word
"""

'''All libraries'''
# import libraries
from itertools import chain
from numpy import dot
from numpy.linalg import norm

# basic python libraires
import string
import re
import math

"""IO"""
# import data
stock_words = open("stock_related_words.txt", encoding="utf8")
stock_related_words = stock_words.readlines()
converted_stock_related_words = []
for word in stock_related_words:
    converted_stock_related_words.append(word.strip())

# Initialize Data Points
post_score = 0

# Retrieve post
post = open("testpost.txt", encoding="utf8")
post_content = str(post.read())
post_content = post_content.replace("\n", " ")
# Convert post into sentences using a regex expresion
post_sentence = re.split("(?<=[.!?]) +", post_content)
# print(post_sentence)
post.close()


# Convert the sentences into words and applies a vector function
def word_tokenize(sentence):
    return sentence.split(" ")
# Create a word_list (a list of each sentence with each token as an array)
word_list = list(map(word_tokenize, post_sentence))
vocab = sorted(set(token.lower() for token in chain(*word_list)))
vocab = ["".join(letter for letter in word if letter not in string.punctuation) for word in vocab]
print(vocab)

# Create a topic list and keyword target
stock_related_vec = {}
keys = range(len(converted_stock_related_words))
for i in keys:
    if converted_stock_related_words[i] in vocab:
        stock_related_vec[str(converted_stock_related_words[i])] = [1 if str(converted_stock_related_words[i]) in token.lower() else 0 for token in vocab]

# positive word vec
positive = open("positive_words.txt", encoding="utf8")
positive_words_list = positive.readlines()
converted_positive_word_list = []
for word in positive_words_list:
    converted_positive_word_list.append(word.strip())

keys = range(len(converted_positive_word_list))

positive_word_vec = {}
for i in keys:
    if converted_positive_word_list[i] in vocab:
        positive_word_vec[str(converted_positive_word_list[i])] = [1 if str(converted_positive_word_list[i]) in token.lower() else 0 for token in vocab]

# negative word vec
negative = open("negative_words.txt", encoding="utf8")
negative_words_list = negative.readlines()
converted_negative_word_list = []
for word in negative_words_list:
    converted_negative_word_list.append(word.strip())

keys = range(len(converted_negative_word_list))

negative_word_vec = {}
for i in keys:
    if converted_negative_word_list[i] in vocab:
        negative_word_vec[str(converted_negative_word_list[i])] = [1 if str(converted_negative_word_list[i]) in token.lower() else 0 for token in vocab]



"""Determining process"""
# Check each sentence
cos_sim = lambda x, y: dot(x,y)/(norm(x)*norm(y))
line_number = 1
sentence_score_list = []
sentence_word_number = []

positive_score_total = 0
negative_score_total = 0

for line in post_sentence:
    # Set up
    relevance_score, sentence_score = 0, 0

    # Set up line vector for linear algebra regression and comparison
    line_token = [token.lower() for token in word_tokenize(line)]
    line_vec = [1 if token in line_token else 0 for token in vocab]
    print(line_number)
    print("\t" + line)
    line_number += 1
    
    # Relevance score calculation
    for name, topic_vec in stock_related_vec.items():
        relevance_score += cos_sim(line_vec, topic_vec)
    # print("\t Relevance_score:", relevance_score)

    # Check the opinion of each sentence
    polarity_score, positive_score, positive_words, negative_score, negative_words = 0, 0, 0, 0, 0
    for name, positive_vec in positive_word_vec.items():
        positive_score += cos_sim(line_vec, positive_vec)
        if (cos_sim(line_vec, positive_vec) != 0):
            positive_words += 1
    positive_score *= positive_words
    # print("\t Positive Score: ", positive_score)

    for name, negative_vec in negative_word_vec.items():
        negative_score += cos_sim(line_vec, negative_vec)
        if (cos_sim(line_vec, negative_vec) != 0):
            negative_words += 1
    negative_score *= negative_words
    # print("\t Negative Score: ", negative_score)

    POST_CONSTANT = sentence_score * (len(line.split()) / len(post_content.split()))
    # print("Post Constant" + str(POST_CONSTANT))
    # Calculating polarity score
    if positive_score > negative_score:
        if negative_score != 0:
            polarity_score = positive_score / negative_score
        else:
            polarity_score = positive_score / (math.sqrt(1/len(line.split())))
    elif positive_score < negative_score:
        if positive_score != 0:
            polarity_score = -negative_score / negative_score
        else: 
            polarity_score = -negative_score / (math.sqrt(1/len(line.split())))
    else:
        polarity_score = POST_CONSTANT * positive_score

    #  Constant to be calculated based on groups of posts, person posting, etc
    POST_CREDIBILITY_SCORE = 0.01
    positive_score_total += positive_score
    negative_score_total += negative_score
    # print("\t Positive Score: ", positive_score)
    # print("\t Negative Score: ", negative_score)
    # print("\t Polarity Score: ", polarity_score)
    if relevance_score != 0:
        sentence_score = polarity_score * relevance_score
    else:
        sentence_score = polarity_score * POST_CREDIBILITY_SCORE
    sentence_score_list.append(sentence_score)
    sentence_word_number.append(len(line.split()))


"""Post score calculation"""
for i in range(len(sentence_score_list)):
    weighted_sentence_score = sentence_score_list[i] * sentence_word_number[i]
    post_score += weighted_sentence_score
post_score /= len(post_sentence)
print("Post Score: " + str(post_score))
# print("Post Positive" + str(positive_score_total))
# print("Post Negative" + str(negative_score_total))


"""Testing"""
# print(converted_negative_word_list)

# Backup and testing code

# # Do a calculation of each sentence
# for line in post_content:
#     # Figure out the relevance of a sentence
#     keyword_count = 0
#     for word in word_list:
#         keyword_count += line.lower.count(word)
#     relevance_score = keyword_count

    
#     # Check whether the sentence is on topic or not


# Old code on converting word into a vector

# for word in converted_positive_word_list:
#     positive_word_vec[word] = [1 if str(word) in token.lower() else 0 for token in vocab]

# Old brute force testing method

# apple = [1 if "apple" in token.lower() else 0 for token in vocab]
# # print(apple)
# stock = [1 if "stock" in token.lower() else 0 for token in vocab]
# topics = {
#     "apple": apple,
#     "stock": stock
# }
# print(topics)

# Useless function

# def remove_new_line(word):
#     return word[0, word.len() - 1]
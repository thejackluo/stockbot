# # Test 1: Post to sentence

# x = "Machine learning is the science of getting computers to act without being explicitly programmed. Machine learning is so pervasive today that you probably use it dozens of times a day without knowing it. Many researchers also think it is the best way to make progress towards human-level AI."

# l = ['computer', 'researcher']

# for line in x.split('.'):
#     for word in l:
#         if word in line:
#             print(line)
#             break

# Test 2: Algorithm for seperating vocab

from itertools import chain

def word_tokenize(sentence):
    return sentence.split(" ")
s1 = "Lecture was engaging"
s2 = "Tutor is very nice and active"
s3 = "The content of lecture was too much for 2 hours."
s4 = "Exam seem to be too difficult compare with weekly lab."
vocab = sorted(set(token.lower() for token in chain(*list(map(word_tokenize, [s1, s2, s3, s4])))))
print(vocab)
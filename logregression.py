from itertools import groupby
import nltk
import statsmodels.api as sm
import pandas as pd
from numpy import mean
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation

def read_file_lines(textfile):
    with open(textfile) as text_file:
        contents = text_file.readlines()
    return contents

def read_file(textfile):
    with open(textfile) as text_file:
        contents = text_file.read()
    return contents

def predLog(MSL, MWL):
    global simple
    global complex
    X_new = [MSL, MWL, 1]
    Probability = result.predict(X_new)
    if Probability > 0.5:
        print("Complex")
        complex += 1
    else:
        print("Simple")
        simple = simple + 1
    print(Probability)

simple = 0
complex = 0

text = read_file("input.txt")

paragraphs = text.split('\n\n')
meanSentenceLength = []
meanWordLength = []

for para in paragraphs:
    # Split it into sentences
    sentences = sent_tokenize(para)
    sentenceLength = []
    wordLength = []
    sentcount = 0
    # Splits into words
    for words in sentences:
        number = [word for word in word_tokenize(words) if word not in punctuation]
        sentenceLength.append(len(number))
        sentcount += 1
        wordcount = 0

        numberOfWords = len(number)

        for character in number:
            wordcount += len(character)

        wordLength.append(wordcount/numberOfWords)
    meanWordLength.append(sum(wordLength)/sentcount)
    meanSentenceLength.append((sum(sentenceLength))/sentcount)

print(meanWordLength)
print(meanSentenceLength)
# Plug these into the algorithm

input_file = "ExcelData.csv"
data = pd.read_csv(input_file)
data.columns = ["Complex", "Sentence Length", "Word"]
data['intercept'] = 1.0
train_cols = data.columns[1:]
print(train_cols)
# Apply logistic regression algorith
logit = sm.Logit(data['Complex'], data[train_cols])

result = logit.fit()
# result.summary()

for x in range(len(meanWordLength)):
    predLog(meanSentenceLength[x], meanWordLength[x])

ComplexIndex = complex/(complex+simple)
print("Complex index is:",ComplexIndex)

if ComplexIndex >0.7 or ComplexIndex < 0.3:
    print("Not Plagiarised")
else:
    print("Suspected Plagiarised")

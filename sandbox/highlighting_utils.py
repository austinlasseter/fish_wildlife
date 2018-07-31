'''Utility functions for email category viewer'''
import plotly.graph_objs as go
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import WhitespaceTokenizer
# Tip of the hat to this page https://stackoverflow.com/questions/31668493/get-indices-of-original-text-from-nltk-word-tokenize
import dash
import dash_html_components as html
import csv

#----------------------------------------------------------------------#
# Globals                                                              #
#----------------------------------------------------------------------#
snowballStemmer = SnowballStemmer("english", ignore_stopwords=True)
myTokenizer = WhitespaceTokenizer()


#-------------------------------------------------------------------------#
# Using same stemmer and preprocessor definition as used in NB classifier #
#-------------------------------------------------------------------------#
def stripPunctuation(text):
    return (text.translate({ord(c):'' for c in string.punctuation}))

def preprocess(text):
    lower_text = ''
    if (type(text)== str):
        lower_text = text.lower()
    return lower_text

def myTokenize(text, removeStopwords=True):
    global snowballStemmer
    global myTokenizer

    tokens = []
    filtered = []
    stemmed = []

    cleaned = preprocess(text)

    #Generate a list of tokens and also the spans from the preprocessed text
    rawTokens = myTokenizer.tokenize(cleaned)
    span_generator = myTokenizer.span_tokenize(cleaned)
    rawSpans = [span for span in span_generator]

    cleanedTokens = []
    cleanedSpans = []
    for i in range(0,len(rawTokens)):
        #Strip out punctuation from tokens
        cleanToken = stripPunctuation(rawTokens[i])
        #Discard tokens which only contained punctuation
        if (len(cleanToken) > 0):
            cleanedTokens.append(cleanToken)
            cleanedSpans.append(rawSpans[i])

    tokens_with_spans = zip(cleanedTokens, cleanedSpans)

    #Remove stop words
    if (removeStopwords):
        filtered = [(w,s) for (w,s) in tokens_with_spans if not w in stopwords.words('english')]
    else:
        filtered = [(w,s) for (w,s) in tokens_with_spans]

    #Stem each token

    stemmedTerms = [snowballStemmer.stem(item[0]) for item in filtered]
    spans = [item[1] for item in filtered]
    stemmed = list(zip(stemmedTerms, spans))
    return stemmed


#------------------------------------------------#
# Highlight all terms in string matching list
# wrap with span tags and highlight class
# lifting methods from here https://stackoverflow.com/questions/34956423/python-tkinter-change-text-background-of-some-textual-spans?rq=1
#------------------------------------------------#
def highlightTerms(textString, topic1, topic2, topic3, topic4, topic5, topic6, topic7, topic8, topic9, topic10):
    '''
    Highlight all terms in input string matching list of terms in 2nd arg
    '''

    rawText = textString

    #Only highlight top message, not replies
    pos = rawText.find(' From:')
    if pos == -1:
        top = rawText
        rest = ''
    else:
        top = rawText[:(pos-1)]
        rest = rawText[pos:]

    highlightedText = [] #empty for now

    inputTerms_with_spans = myTokenize(top, removeStopwords=False)
    currentOffset = 0

    for (token, span) in inputTerms_with_spans:
        if (token in topic1):
            start = span[0]
            end = span[1]
            highlightedText += top[currentOffset:start]
            highlightedText += list("<span style=\"background-color: #9999ff\">")
            highlightedText += top[start:end]
            highlightedText += list("</span>")
            currentOffset = (end)

        elif (token in topic2):
            start = span[0]
            end = span[1]
            highlightedText += top[currentOffset:start]
            highlightedText += list("<span style=\"background-color: yellow\">")
            highlightedText += top[start:end]
            highlightedText += list("</span>")
            currentOffset = (end)
            
        elif (token in topic3):
            start = span[0]
            end = span[1]
            highlightedText += top[currentOffset:start]
            highlightedText += list("<span style=\"background-color: #50e246\">")
            highlightedText += top[start:end]
            highlightedText += list("</span>")
            currentOffset = (end)

        elif (token in topic4):
            start = span[0]
            end = span[1]
            highlightedText += top[currentOffset:start]
            highlightedText += list("<span style=\"background-color: #5ef9f2\">")
            highlightedText += top[start:end]
            highlightedText += list("</span>")
            currentOffset = (end)
            
        elif (token in topic5):
            start = span[0]
            end = span[1]
            highlightedText += top[currentOffset:start]
            highlightedText += list("<span style=\"background-color: blue\">")
            highlightedText += top[start:end]
            highlightedText += list("</span>")
            currentOffset = (end)            

        elif (token in topic6):
            start = span[0]
            end = span[1]
            highlightedText += top[currentOffset:start]
            highlightedText += list("<span style=\"background-color: #e67cea\">")
            highlightedText += top[start:end]
            highlightedText += list("</span>")
            currentOffset = (end)
            
        elif (token in topic7):
            start = span[0]
            end = span[1]
            highlightedText += top[currentOffset:start]
            highlightedText += list("<span style=\"background-color: orange\">")
            highlightedText += top[start:end]
            highlightedText += list("</span>")
            currentOffset = (end)

        elif (token in topic8):
            start = span[0]
            end = span[1]
            highlightedText += top[currentOffset:start]
            highlightedText += list("<span style=\"background-color: #f20410\">")
            highlightedText += top[start:end]
            highlightedText += list("</span>")
            currentOffset = (end)
            
        elif (token in topic9):
            start = span[0]
            end = span[1]
            highlightedText += top[currentOffset:start]
            highlightedText += list("<span style=\"background-color: gray\">")
            highlightedText += top[start:end]
            highlightedText += list("</span>")
            currentOffset = (end)   

        elif (token in topic10):
            start = span[0]
            end = span[1]
            highlightedText += top[currentOffset:start]
            highlightedText += list("<span style=\"background-color: purple\">")
            highlightedText += top[start:end]
            highlightedText += list("</span>")
            currentOffset = (end)   
            
            
    highlightedText += top[currentOffset:]

    return(''.join(highlightedText) + '<i>' + rest + '</i>')

#########################
# Generate a table
##########################

def generate_table(dataframe):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))]
    )

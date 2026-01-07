import re

CONTRACTIONS = {
    "can't": "cannot",
    "won't": "will not",
    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "haven't": "have not",
    "hasn't": "has not",
    "hadn't": "had not",
    "i'm": "i am",
    "i've": "i have",
    "i'll": "i will",
    "i'd": "i would",
    "you're": "you are",
    "you've": "you have",
    "you'll": "you will",
    "you'd": "you would",
    "he's": "he is",
    "she's": "she is",
    "it's": "it is",
    "we're": "we are",
    "they're": "they are",
    "that's": "that is",
    "there's": "there is",
    "what's": "what is",
}

def expand_contractions(text):
    pattern = re.compile(r'\b(' + '|'.join(CONTRACTIONS.keys()) + r')\b')
    return pattern.sub(lambda x: CONTRACTIONS[x.group()], text)

def clean_text(s):
    s = s.lower()

    # expand contractions FIRST
    s = expand_contractions(s)

    # remove urls
    s = re.sub(r'http\S+|www\S+', ' ', s)

    # remove html tags
    s = re.sub(r'<.*?>', ' ', s)

    # remove punctuation / non-alphanumeric chars
    s = re.sub(r'[^a-z0-9\s]', ' ', s)

    # collapse multiple spaces
    s = re.sub(r'\s+', ' ', s)

    # strip leading/trailing whitespace
    return s.strip()
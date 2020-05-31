import re

from recipy.settings import CLEANED_STOP_WORDS, LEMMATIZER


def clean_text_and_tokenize(text):
    # Build the whole string and remove digits from it
    if isinstance(text, list):
        whole_string = re.sub(r'\d+', '', ' '.join(text).lower())
    else:
        whole_string = text.lower()

    # Remove punctuations from the string
    cleaned_string = whole_string.translate(str.maketrans('', '', r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{}~"""))

    # Tokenize and remove the stop-words from the instructions
    tokens = set(w for w in re.split(r'[\\|\s\n\r]', cleaned_string) if w) - CLEANED_STOP_WORDS

    # Lemmatize the string and save the results to the DB
    return sorted(set(LEMMATIZER.lemmatize(token) for token in tokens) - CLEANED_STOP_WORDS)

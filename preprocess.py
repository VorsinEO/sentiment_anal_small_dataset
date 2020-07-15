import re
from collections import Counter
import nltk
nltk.download('wordnet')
nltk.download('punkt')
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

normalizer = WordNetLemmatizer()

# функция для нахождения наиболее вероятной части речи через синонимы
def get_part_of_speech(word):
    probable_part_of_speech = wordnet.synsets(word)
    pos_counts = Counter()
    pos_counts["n"] = len(  [ item for item in probable_part_of_speech if item.pos()=="n"]  )
    pos_counts["v"] = len(  [ item for item in probable_part_of_speech if item.pos()=="v"]  )
    pos_counts["a"] = len(  [ item for item in probable_part_of_speech if item.pos()=="a"]  )
    pos_counts["r"] = len(  [ item for item in probable_part_of_speech if item.pos()=="r"]  )
    most_likely_part_of_speech = pos_counts.most_common(1)[0][0]
    return most_likely_part_of_speech

#шаблон для замены
special_chars = re.compile(r'[^A-Za-z_\d,.?!;:$\- \'\"]', re.IGNORECASE)

# препроцессинг
def preprocess_text(text):
    #чистка текста
    text = text.lower()
    text = text.replace("``", '"').replace("''", '"').replace("`", "'")
    text = text.replace("n 't", "n't").replace("can not", "cannot")
    text = special_chars.sub(' ', text)
    text = re.sub(' +', ' ', text)
    # токенизация
    tokenized = word_tokenize(text)
    # Лемматизация с использованием наиболее вероятной части речи
    normalized = " ".join([normalizer.lemmatize(token, get_part_of_speech(token)) for token in tokenized])
    return normalized

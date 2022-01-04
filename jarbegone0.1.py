##################################################################
# JarBeGone version 0.1
#  usage: jarbegone0.1.py [-h] file threshold
#
#  positional arguments:
#    file        The TeX filepath to analyse
#    threshold   Upper threshold to highlight infrequent words (percentage)), default=10
#
# TODO:
#  - Missing sectioning, at the moment only outputs word stems
#
# 2022 MIT LICENCE
##################################################################

import argparse
import re

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    # does this leave open file handle? maybe, but it takes stdin
    parser.add_argument(
        "file", type=argparse.FileType("r"), help="The TeX filepath to analyse"
    )
    parser.add_argument(
        "threshold",
        type=float,
        default=10.0,
        help="Upper threshold to highlight infrequent words (percentage))",
    )
    args = parser.parse_args()
    threshold = args.threshold / 100
    raw = args.file.readlines()

    # check correct module installation
    try:
        import nltk
    except ModuleNotFoundError:
        print("Please install nltk, e.g. 'pip install nltk'")
    try:
        from TexSoup import TexSoup
    except ModuleNotFoundError:
        print("Please install TexSoup, e.g. 'pip install TexSoup'")

    # check nltk corpora downloaded
    try:
        nltk.data.find("corpora/brown.zip")
    except LookupError:
        nltk.download("brown")
    try:
        nltk.data.find("corpora/stopwords.zip")
    except LookupError:
        nltk.download("stopwords")

    # nltk set up
    from nltk.stem import PorterStemmer
    from nltk.corpus import brown, stopwords

    porter = PorterStemmer()
    from nltk.probability import *

    words = FreqDist()
    stops = stopwords.words("english")
    stops = stops + ["section", "subsection"]

    print("Building frequency distribution")
    for sentence in brown.sents():
        for word in sentence:
            stemmed = porter.stem(word)
            if stemmed not in stops:
                words[stemmed] += 1
    corpus_total = 0
    for word in words:
        corpus_total += words[word]

    # preprocessing
    THRESHOLD = (
        threshold * corpus_total
    )  # words seen <20% in the corpus [warning corpus is still dirty]
    r = re.compile("(?<!\S)[A-Za-z]+(?!\S)|(?<!\S)[A-Za-z]+(?=:(?!\S))")
    annoying_chars = {ord(x): "" for x in ["\n", ":", "'"]}

    print("Extracting words from TeX document")
    a = TexSoup(raw)
    b = " ".join(TexSoup(a.text)).split(" ")

    print("Cleaning...")
    c = [s.translate(annoying_chars).lower() for s in b]
    d = list(filter(r.match, c))

    print("Stemming...")
    tex_words = [porter.stem(word) for word in d if word not in stops]

    print("Possible Jargon words:")
    for tex_word in tex_words:
        freq = words.freq(tex_word)
        if freq < THRESHOLD:
            print(f"  {tex_word} - {freq}")

    print("Done.")

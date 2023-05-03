import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """The Indian Premier League (IPL) (also known as the TATA IPL for sponsorship reasons) is a men's Twenty20 (T20) cricket league that is annually held in India and contested by ten city-based franchise teams.[3][4] The Board of Control for Cricket in India (BCCI) founded the league in 2007. The competition is usually held between March and May every year, and has an exclusive window in the ICC Future Tours Programme; fewer international cricket tours take place during IPL seasons.[5]

The IPL is the most-popular cricket league in the world; in 2014, it was ranked sixth by average attendance among all sports leagues.[6][needs update] In 2010, the IPL became the first sporting event to be broadcast live on YouTube.[7][8] The brand value of the IPL in 2022 was ₹90,038 crore (US$11 billion).[9] According to BCCI, the 2015 IPL season contributed ₹1,150 crore (US$140 million) to the gross domestic product (GDP) of the economy of India.[10] In December 2022, the IPL became a decacorn valued at US$10.9 billion, registering a 75% growth in dollar terms since 2020 when it was valued at $6.2 billion, according to a report by consulting firm D & P Advisory.[11]

"""


def summarizer(rawdocs):

    stopwords = list(STOP_WORDS)
    # rint(stopwords)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    # print(doc)
    tokens = [token.text for token in doc]
    # print(tokens)
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower()not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    # print(word_freq)

    max_freq = max(word_freq.values())
    # print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    # print(word_freq)

    sent_tokens = [sent for sent in doc.sents]
    # print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    # print(sent_scores)

    select_len = int(len(sent_tokens) * 0.3)
    # print(select_len)

    summary = nlargest(select_len, sent_scores, key=sent_scores.get)
    # print(summary)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    # print(summary)

    # print("Length of original text", len(text.split(' ')))
    # print("Length of summary", len(summary.split(' ')))

    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))
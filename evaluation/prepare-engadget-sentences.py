import json
import sys
import os
from spacy.lang.en import English

if not os.path.exists('./out'):
    os.makedirs('./out')

## file the splitted to upload them to github
with open('./data/engadget-articles-a.json') as f1:
    data1 = json.load(f1)
with open('./data/engadget-articles-b.json') as f2:
    data2 = json.load(f2)



data = data1 + data2
articles = [i['text'] for i in data if i and i['text']]  # 62'082 articles with 899'164 sentences in total


nlp = English()
sentencizer = nlp.create_pipe("sentencizer")
nlp.add_pipe(sentencizer)

with open("./out/engadget-corpus.txt", "w") as f:
    l = len(articles)
    for ix, article in enumerate(articles, start=1):
        try:
            sents = list(nlp(article).sents)

            for sent in sents:
                f.write("%s\n" % (sent.text.strip()))
            f.write("\n")
        except:
            pass  # empty string
        sys.stdout.write("\r%s of %s" % (ix,l))
        sys.stdout.flush()

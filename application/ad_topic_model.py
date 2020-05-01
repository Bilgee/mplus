import fnmatch
import json
import gensim
import nltk
from gensim import corpora
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')


wordnet_lemmatizer = WordNetLemmatizer()


class AdTopicModel:
    def __init__(self):
        """init class object

        Arguments:
            model -- [Topics]
            Tdictionary  -- [Topic words dictionary] 
        """
        with open("application/Newtopic.txt") as json_file:
            self.model = json.load(json_file)
        with open("application/Tdictionary.txt") as json_file:
            self.Tdictionary = json.load(json_file)

    def topics_temp(self, category, score, total, index):
        temp = {'Category': category, 'Score': round((score / total), 4), 'Index': index}
        return temp

    def topic_score(self, page, tdictionary, dictionary):
        total = 0
        t = {}  # topic buriin niit score
        for word in page:
            w = dictionary[word[0]]
            w = wordnet_lemmatizer.lemmatize(w)
            syns = wordnet.synsets(w)
            dd = set()
            try:
                syn = syns[0]
                if fnmatch.fnmatch(syn.name(), "*.n.*"):
                    for s in syn.lemmas():
                        dd.add(s.name())
            except:
                dd.add(w)
            s = {}
            for ug in dd:
                try:
                    temp2 = tdictionary[ug]
                except KeyError:
                    continue
                for q in temp2:
                    j = 1
                    i = 0
                    for p in range(word[1]):
                        i += q['Score'] * j
                        j *= 0.9
                    try:
                        if i > s[q['Index']][0]:
                            s[q['Index']][0] = i
                        if q['Score'] > s[q['Index']][1]:
                            s[q['Index']][1] = q['Score']
                    except KeyError:
                        s[q['Index']] = []
                        s[q['Index']].append(i)
                        s[q['Index']].append(q['Score'])
            for wo in s:
                total += s[wo][0]
                try:
                    t[wo][0] += s[wo][0]
                    t[wo][1] += s[wo][1]
                except KeyError:
                    t[wo] = []
                    t[wo].append(s[wo][0])
                    t[wo].append(s[wo][1])
        return t, total

    def score(self, temp, tlist, total):
        for t in tlist:
            temp['Topics'].append(self.topics_temp(t[2], t[0], total, t[1]))
        return temp

    def topic_predict(self, bow_corpus, dictionary):
        predicted = [] 
        for page in bow_corpus:
            temp = {'Topics': []}
            t, total = self.topic_score(page, self.Tdictionary, dictionary)
            tlist = []
            for q in t:
                temp2 = self.model['Topics'][q]['Category']  # q ni topiciin index
                if t[q][1] > 0.05:
                    tlist.append([t[q][0], q, temp2])
                else:
                    total -= t[q][0]
            tlist.sort(reverse=True)
            if total == 0 or len(tlist) == 0:
                temp2 = {'Category': 'Unknown', 'Score': 0}
                a = {"Text": "", "Score": 0}
                temp2['Words'] = [a]
                temp['Topics'].append(temp2)
                predicted.append(temp)
                continue
            temp = self.score(temp, tlist, total)
            predicted.append(temp)
        return predicted

    def predict(self, clean_text, ad_numbers):
        dictionary = corpora.Dictionary(clean_text)
        bow_corpus = [dictionary.doc2bow(doc) for doc in clean_text]
        topic_predictions = self.topic_predict(bow_corpus, dictionary)
        predicted = []
        cnt = 0
        for doc in topic_predictions:
            temp2 = {"Topic": doc['Topics'], "ad_number": ad_numbers[cnt]}
            cnt += 1
            predicted.append(temp2)
        return predicted

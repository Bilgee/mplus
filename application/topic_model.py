import fnmatch
import json
import gensim
import nltk
from gensim import corpora
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')


wordnet_lemmatizer = WordNetLemmatizer()


class TopicModel:
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

    def topics_words(self, index, number, model_topics):
        temp = []
        j = 0
        for word in model_topics['Topics'][index]['Words']:
            if j == number:
                break
            a = {"Text": word[0], "Score": round(word[1], 4)}
            temp.append(a)
            j += 1
        return temp

    def topics_temp(self, category, score, total):
        temp = {'Category': category, 'Score': round((score / total), 4)}
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

    def max_score(self, temp, tlist, model_topics, total):
        temp['Topics'].append(self.topics_temp(tlist[-1][2], tlist[-1][0], total))
        temp['Topics'][0]['Words'] = self.topics_words(tlist[-1][1], 10, model_topics)
        temp['Topics'][0]['Index'] = tlist[-1][1]
        try:
            temp['Topics'].append(self.topics_temp(tlist[-2][2], tlist[-2][0], total))
            temp['Topics'][1]['Words'] = self.topics_words(tlist[-2][1], 10, model_topics)
            temp['Topics'][1]['Index'] = tlist[-2][1]
        except IndexError:
            return temp
        return temp

    def max_category(self, temp, tlist, model_topics, total):
        if not tlist[-2][2] == tlist[-3][2] or tlist[-3][0] + tlist[-2][0] < tlist[-1][0]:
            temp = self.max_score(temp, tlist, model_topics, total)
            return temp
        temp['Topics'].append(self.topics_temp(tlist[-2][2], tlist[-3][0] + tlist[-2][0], total))
        temp['Topics'][0]['Words'] = []
        j = 0
        ug = []
        temp['Topics'][0]['Index'] = tlist[-2][1]
        for word, score in model_topics['Topics'][tlist[-2][1]]['Words']:
            if j == 10:
                break
            ug.append([score, word])
            j += 1
        j = 0
        for word, score in model_topics['Topics'][tlist[-3][1]]['Words']:
            if j == 10:
                break
            ug.append([score, word])
            j += 1
        ug.sort()
        temp['Topics'][0]['Words'].append(ug[-1][1])
        j = 0
        for i in range(len(ug) - 1):
            if ug[(-1) * i - 2][1] == ug[(-1) * i - 1][1]:
                continue
            if j == 10:
                break
            j += 1
            a = {"Text": ug[(-1) * i - 2][1], "Score": round(ug[(-1) * i - 2][0], 4)}
            temp['Topics'][0]['Words'].append(a)
        temp['Topics'].append(self.topics_temp(tlist[-1][2], tlist[-1][0], total))
        temp['Topics'][1]['Words'] = self.topics_words(tlist[-1][1], 10, model_topics)
        temp['Topics'][1]['Index'] = tlist[-1][1]
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
            tlist.sort()
            if total == 0 or len(tlist) == 0:
                temp2 = {'Category': 'Unknown', 'Score': 0}
                a = {"Text": "", "Score": 0}
                temp2['Words'] = [a]
                temp['Topics'].append(temp2)
                predicted.append(temp)
                continue
            if len(tlist) == 1 or len(tlist) == 2:
                temp = self.max_score(temp, tlist, self.model, total)
                predicted.append(temp)
                continue
            elif tlist[-1][0] * 0.8 > tlist[-2][0] or tlist[-1][2] == tlist[-2][2]:
                temp = self.max_score(temp, tlist, self.model, total)
                predicted.append(temp)
                continue
            else:
                temp = self.max_category(temp, tlist, self.model, total)
                predicted.append(temp)
                continue
        return predicted

    def predict(self, clean_text, ner, page_numbers):
        dictionary = corpora.Dictionary(clean_text)
        bow_corpus = [dictionary.doc2bow(doc) for doc in clean_text]
        topic_predictions = self.topic_predict(bow_corpus, dictionary)
        predicted = []
        # tf_idf
        tf_idf = gensim.models.TfidfModel(bow_corpus)
        corpus_tfidf = tf_idf[bow_corpus]
        top_8_or_so_words = []
        for doc in corpus_tfidf:
            doc.sort(key=lambda x: x[1], reverse=True)
            tmp = []
            cnt = 0
            for word in doc:
                tmp += [dictionary[word[0]]]
                cnt += 1
                if cnt == 8:
                    break
            top_8_or_so_words += [tmp]
        cnt = 0
        for doc in topic_predictions:
            temp2 = {"Topic": doc['Topics'], "Named Entity": []}
            for word in ner[cnt]:
                temp = {}
                if word == '':
                    continue
                temp["Text"] = word[0]
                temp["Label"] = word[1]
                temp2["Named Entity"].append(temp)
            temp2["Keywords"] = top_8_or_so_words[cnt]
            temp2["page_number"] = page_numbers[cnt]
            cnt += 1
            predicted.append(temp2)
        return predicted

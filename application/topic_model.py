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
            model -- [topics]
            Tdictionary  -- [Topic words dictionary] 
        """
        with open("application/Newtopic.txt") as json_file:
            self.model = json.load(json_file)
        with open("application/Tdictionary.txt") as json_file:
            self.Tdictionary = json.load(json_file)

    def topics_words(self, index, number, model_topics):
        temp = []
        j = 0
        for word in model_topics['topics'][index]['words']:
            if j == number:
                break
            a = {"text": word[0], "score": round(word[1], 4)}
            temp.append(a)
            j += 1
        return temp

    def topics_temp(self, category, score, total):
        temp = {'category': category, 'score': round((score / total), 4)}
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
                        i += q['score'] * j
                        j *= 0.9
                    try:
                        if i > s[q['index']][0]:
                            s[q['index']][0] = i
                        if q['score'] > s[q['index']][1]:
                            s[q['index']][1] = q['score']
                    except KeyError:
                        s[q['index']] = []
                        s[q['index']].append(i)
                        s[q['index']].append(q['score'])
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
        temp['topics'].append(self.topics_temp(tlist[-1][2], tlist[-1][0], total))
        temp['topics'][0]['words'] = self.topics_words(tlist[-1][1], 10, model_topics)
        temp['topics'][0]['index'] = tlist[-1][1]
        try:
            temp['topics'].append(self.topics_temp(tlist[-2][2], tlist[-2][0], total))
            temp['topics'][1]['words'] = self.topics_words(tlist[-2][1], 10, model_topics)
            temp['topics'][1]['index'] = tlist[-2][1]
        except IndexError:
            return temp
        return temp

    def max_category(self, temp, tlist, model_topics, total):
        if not tlist[-2][2] == tlist[-3][2] or tlist[-3][0] + tlist[-2][0] < tlist[-1][0]:
            temp = self.max_score(temp, tlist, model_topics, total)
            return temp
        temp['topics'].append(self.topics_temp(tlist[-2][2], tlist[-3][0] + tlist[-2][0], total))
        temp['topics'][0]['words'] = []
        j = 0
        ug = []
        temp['topics'][0]['index'] = tlist[-2][1]
        for word, score in model_topics['topics'][tlist[-2][1]]['words']:
            if j == 10:
                break
            ug.append([score, word])
            j += 1
        j = 0
        for word, score in model_topics['topics'][tlist[-3][1]]['words']:
            if j == 10:
                break
            ug.append([score, word])
            j += 1
        ug.sort()
        temp['topics'][0]['words'].append(ug[-1][1])
        j = 0
        for i in range(len(ug) - 1):
            if ug[(-1) * i - 2][1] == ug[(-1) * i - 1][1]:
                continue
            if j == 10:
                break
            j += 1
            a = {"text": ug[(-1) * i - 2][1], "score": round(ug[(-1) * i - 2][0], 4)}
            temp['topics'][0]['words'].append(a)
        temp['topics'].append(self.topics_temp(tlist[-1][2], tlist[-1][0], total))
        temp['topics'][1]['words'] = self.topics_words(tlist[-1][1], 10, model_topics)
        temp['topics'][1]['index'] = tlist[-1][1]
        return temp

    def topic_predict(self, bow_corpus, dictionary):
        predicted = [] 
        for page in bow_corpus:
            temp = {'topics': []}
            t, total = self.topic_score(page, self.Tdictionary, dictionary)
            tlist = []
            for q in t:
                temp2 = self.model['topics'][q]['category']  # q ni topiciin index
                if t[q][1] > 0.05:
                    tlist.append([t[q][0], q, temp2])
                else:
                    total -= t[q][0]
            tlist.sort()
            if total == 0 or len(tlist) == 0:
                temp2 = {'category': 'unknown', 'score': 0}
                a = {"text": "", "score": 0}
                temp2['words'] = [a]
                temp['topics'].append(temp2)
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
            temp2 = {"topic": doc['topics'], "named entity": []}
            for word in ner[cnt]:
                temp = {}
                if word == '':
                    continue
                temp["text"] = word[0]
                temp["label"] = word[1]
                temp2["named entity"].append(temp)
            temp2["keywords"] = top_8_or_so_words[cnt]
            temp2["page_number"] = page_numbers[cnt]
            cnt += 1
            predicted.append(temp2)
        return predicted

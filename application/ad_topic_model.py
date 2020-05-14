import json
from gensim import corpora


class AdTopicModel:
    def __init__(self, language):
        """init class object

        Arguments:
            model -- [topics]
            Tdictionary  -- [topic words dictionary]
        """
        with open("application/language/Sdictionary_"+language+".txt") as json_file:
            self.lang = json.load(json_file)
        with open("application/Newtopic.txt") as json_file:
            self.model = json.load(json_file)
        with open("application/Tdictionary.txt") as json_file:
            self.Tdictionary = json.load(json_file)

    def topic_score(self, page, tdictionary, dictionary):
        """

        Parameters
        ----------
        page : list
            text list of 1 page
        tdictionary : dict
            topic dictionary from Tdictionary file
        dictionary : object of gensim.corpora.dictionary
            dictionary of magazine

        Returns
        -------
        list
            topic tus buriin niit score
        float
            buh topic-n niilber onoo
        """
        total = 0
        t = {}  # topic buriin niit score
        for word in page:
            ug = dictionary[word[0]]
            s = {}
            if self.lang.get(ug):
                syn = self.lang.get(ug)
            else:
                continue
            temp2 = tdictionary.get(syn[0])
            s = {}
            for q in temp2:
                j = 1
                i = 0
                for p in range(word[1]):
                    i += q['score'] * syn[1] * j
                    j *= 0.9
                if s.get(q['index']):
                    if i > s[q['index']][0]:
                        s[q['index']][0] = i
                    if q['score'] * syn[1] > s[q['index']][1]:
                        s[q['index']][1] = q['score'] * syn[1]
                else:
                    s[q['index']] = []
                    s[q['index']].append(i)
                    s[q['index']].append(q['score'] * syn[1])
        for wo in s:
            total += s[wo][0]
            if t.get(wo):
                t[wo][0] += s[wo][0]
                t[wo][1] += s[wo][1]
            else:
                t[wo] = []
                t[wo].append(s[wo][0])
                t[wo].append(s[wo][1])
        return t, total

    def topic_predict(self, bow_corpus, dictionary):
        """

        Parameters
        ----------
        bow_corpus : list
            bag of words (ad)
        dictionary : object of gensim.corpora.dictionary
            dictionary of ad

        Returns
        -------
        list
            predicted topics of ad
        """
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
            tlist.sort(reverse=True)
            if total == 0 or len(tlist) == 0:
                temp2 = {'category': 'unknown', 'score': 0}
                a = {"text": "", "score": 0}
                temp2['Words'] = [a]
                temp['topics'].append(temp2)
                predicted.append(temp)
                continue
            for t in tlist:
                temp['topics'].append({'category': t[2], 'score': round((t[0] / total), 4), 'index': t[1]})
            predicted.append(temp)
        return predicted

    def predict(self, clean_text, ad_numbers):
        """

        Parameters
        ----------
        clean_text : list
            tokenized word list
        ad_numbers : list
            id list of ad

        Returns
        -------
        list
            predicted topics of ad (json format)
        """
        dictionary = corpora.Dictionary(clean_text)
        bow_corpus = [dictionary.doc2bow(doc) for doc in clean_text]
        topic_predictions = self.topic_predict(bow_corpus, dictionary)
        predicted = []
        cnt = 0
        for doc in topic_predictions:
            temp2 = {"topic": doc['topics'], "ad_number": ad_numbers[cnt]}
            cnt += 1
            predicted.append(temp2)
        return predicted

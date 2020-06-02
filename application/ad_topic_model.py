import json
from gensim import corpora


class AdTopicModel:
    def __init__(self):
        """init class object

        Arguments:
            model -- [topics]
            Tdictionary  -- [topic words dictionary]
        """
        self.languages = ["en", "ja"]
        self.langs = {}
        self.Tdictionarys = {}
        self.models = {}
        for language in self.languages:
            with open("application/language/Newtopic_" + language + ".txt") as json_file:
                self.models[language] = json.load(json_file)
            with open("application/language/Sdictionary_" + language + ".txt") as json_file:
                self.langs[language] = json.load(json_file)
            with open("application/language/Tdictionary_" + language + ".txt") as json_file:
                self.Tdictionarys[language] = json.load(json_file)
        self.lang = self.langs["en"]
        self.Tdictionary = self.Tdictionarys["en"]
        self.model = self.models["en"]

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
        s = {}  # topic buriin niit score
        for word in page:
            ug = dictionary[word[0]]
            ug = ug.lower()
            if self.lang.get(ug):
                syn = self.lang.get(ug)
            else:
                continue
            temp2 = tdictionary.get(syn[0])
            for q in temp2:
                j = 1
                i = 0
                for p in range(word[1]):
                    i += q['score'] * j
                    j *= 0.9
                i *= syn[1]
                if s.get(q['index']):
                    s[q['index']][0] += i
                    if q['score'] * syn[1] > s[q['index']][1]:
                        s[q['index']][1] = q['score'] * syn[1]
                else:
                    s[q['index']] = []
                    s[q['index']].append(i)
                    s[q['index']].append(q['score'] * syn[1])
                total += i
        return s, total

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
                temp2['words'] = [a]
                temp['topics'].append(temp2)
                predicted.append(temp)
                continue
            for t in tlist:
                temp['topics'].append({'category': t[2], 'score': round((t[0] / total), 4), 'index': t[1]})
            predicted.append(temp)
        return predicted

    def predict(self, clean_text, ad_number, adlang):
        """

        Parameters
        ----------
        clean_text : list
            tokenized word list
        ad_number : list
            id list of ad
        adlang : basestring
            ad language
        Returns
        -------
        list
            predicted topics of ad (json format)
        """
        if adlang is None:
            adlang = "en"
        self.lang = self.langs[adlang]
        self.Tdictionary = self.Tdictionarys[adlang]
        self.model = self.models[adlang]
        dictionary = corpora.Dictionary(clean_text)
        bow_corpus = [dictionary.doc2bow(doc) for doc in clean_text]
        topic_predictions = self.topic_predict(bow_corpus, dictionary)
        cnt = 0
        for doc in topic_predictions:
            temp2 = {"topic": doc['topics'], "ad_number": ad_number}
            cnt += 1
            return temp2

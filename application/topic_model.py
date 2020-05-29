import json
import gensim
from gensim import corpora


class TopicModel:
    def __init__(self):
        """init class object

        Arguments:
            model -- [topics]
            Tdictionary  -- [Topic words dictionary]
        """
        self.languages = ["en", "ja"]
        self.langs = {}
        self.Tdictionarys = {}
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

    @staticmethod
    def topics_words(index, number, model_topics):
        """

        Parameters
        ----------
        index : int
            topic index
        number : int
            butsaah ugiin too
        model_topics : dict
            topic word,category etc.. from Newtopic file
        Returns
        -------
        list
            list of topic words
        """
        temp = []
        j = 0
        for word in model_topics['topics'][index]['words']:
            if j == number:
                break
            a = {"text": word[0], "score": round(word[1], 4)}
            temp.append(a)
            j += 1
        return temp

    @staticmethod
    def topics_temp(category, score, total):
        """

        Parameters
        ----------
        category : string
            topic category
        score : float
            score of 1 topic
        total : float
            score of all topic

        Returns
        -------
        dict
            huwichilsan onoo
        """
        return {'category': category, 'score': round((score / total), 4)}

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
            if temp2 is None:
                continue
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

    def max_score(self, temp, tlist, model_topics, total):
        """Hamgiin ih onootoi 2 topiciin onoonii zuruu ih tohioldold top 2iig ene function-r songono.

        Parameters
        ----------
        temp : list
            top topics list
        tlist : list
            topics list(score,topic index,category)
        model_topics : dict
            topic word,category etc.. from Newtopic file
        total : float
            total score of all topics
        Returns
        -------
        list
            temp(top topics list)
        """
        temp['topics'].append(self.topics_temp(tlist[-1][2], tlist[-1][0], total))
        temp['topics'][0]['words'] = self.topics_words(tlist[-1][1], 10, model_topics)
        temp['topics'][0]['index'] = tlist[-1][1]
        if len(tlist) > 1:
            temp['topics'].append(self.topics_temp(tlist[-2][2], tlist[-2][0], total))
            temp['topics'][1]['words'] = self.topics_words(tlist[-2][1], 10, model_topics)
            temp['topics'][1]['index'] = tlist[-2][1]
        else:
            return temp
        return temp

    def max_category(self, temp, tlist, model_topics, total):
        """Hamgiin ih onootoi 2 topiciin onoonii zuruu baga tohioldold top 2iig ene function-r songono.

        Parameters
        ----------
        temp : list
            top topics list
        tlist : list
            topics list(score,topic index,category)
        model_topics : dict
            topic word,category etc.. from Newtopic file
        total : float
            total score of all topics
        Returns
        -------
        list
            temp(top topics list)
        """
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
        """

        Parameters
        ----------
        bow_corpus : list
            bag of words ( magazine )
        dictionary : object of gensim.corpora.dictionary
            dictionary of magazine

        Returns
        -------
        list
            predicted topics
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
            tlist.sort()
            if total <= 0 or len(tlist) == 0:
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

    def predict(self, clean_text, ner, page_numbers, maglang):
        """

        Parameters
        ----------
        clean_text : list
            tokenized word list
        ner : list
            NER words of deeppavlov
        page_numbers : list
            page numbers list
        maglang : basestring
            magazine language
        Returns
        -------
        list
            predicted topics json format
        """
        if maglang is None:
            maglang = "en"
        self.lang = self.langs[maglang]
        self.Tdictionary = self.Tdictionarys[maglang]
        self.model = self.models[maglang]
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

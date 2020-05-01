from application.ad_topic_model import AdTopicModel
import time

from nltk.corpus import wordnet


class AdMatch:
    def topic(self, ad):
        ad_text = []
        ad_id = []
        for temp in ad:
            ad_text.append(temp['Words'])
            ad_id.append(temp['Id'])
        topic_model_ad = AdTopicModel()
        ad_topic = topic_model_ad.predict(ad_text, ad_id)
        return ad_topic

    def ad_compare(self, lis, ads, synset):
        result = {}
        for i in lis:
            for index, ad in enumerate(ads):
                for j in ad['Words']:
                    try:
                        ad_syn = synset[j]
                    except:
                        try:
                            synset[j] = wordnet.synsets(j)[0]
                            ad_syn = synset[j]
                        except:
                            synset[j] = None
                            ad_syn = None
                    try:
                        word_syn = synset[i]
                    except:
                        try:
                            synset[i] = wordnet.synsets(i)[0]
                            word_syn = synset[i]
                        except:
                            synset[i] = None
                            word_syn = None
                    try:
                        wup_score = ad_syn.wup_similarity(word_syn)
                    except:
                        wup_score = 0
                    if i == j or (wup_score is not None and wup_score > 0.85):
                        try:
                            result[str(ad['Id'])] += [i, j]
                        except KeyError:
                            result[str(ad['Id'])] = [i, j]
        return result

    def keyword_match(self, ads, magazines):
        key_words = {}
        synset = {}
        start_time = time.time()
        for magazine in magazines:
            key_words[str(magazine['Id'])] = []
            for page in magazine['Pages']:
                page_keywords = []
                page_keywords1 = []
                for entity in page['Named Entity']:
                    page_keywords.append(entity['Text'].lower())
                for tfidfWord in page['Keywords']:
                    if tfidfWord == '':
                        continue
                    page_keywords1.append(tfidfWord.lower())
                match = self.ad_compare(page_keywords, ads, synset)
                match1 = self.ad_compare(page_keywords1, ads, synset)
                key_words[str(magazine['Id'])].append([match, match1])
        print('\n\n---------- adCompare finished: took ', str(time.time() - start_time), ' seconds')
        return key_words

    def predict(self, data):
        """
            {
            "ad": [{ "Id": 52,
                 "Words": ["watch" , "collection" , "blancpain" , "wristwatch" , "women"] },
                 ....
               ] (advertisement format example),

           "magazines": [{   "Id": 12,
                           "Pages":  [{"Topic": [{"Category": "Luxury",
                                            "Score": 0.7195,
                                            "Words": ....,
                                            "Index": 180}...]
                                   "Named Entity": [],
                                   "Keywords": ["blancpain", "collection", "watch", "women", "wristwatch"],
                                   "page_number": 53}.. ]
                   }, ...] (magazine format example)}
        """
        ad = data['ad']
        magazines = data['magazines']
        ad_topic = self.topic(ad)
        ad_keywords = self.keyword_match(ad, magazines)

        predict = []
        for a in ad_topic:
            temp = {}
            match = []
            temp['Ad_number'] = a['ad_number']
            for magazine in magazines:
                cnt = 0
                temp2 = ad_keywords[str(magazine['Id'])]
                for i in magazine["Pages"]:
                    score = 0
                    for q in a['Topic']:
                        for j in i['Topic']:
                            if not j['Category'] == 'Unknown' and j['Index'] == q['Index']:
                                score += (j['Score'] + q['Score']) / 2
                                break
                    score *= 0.7
                    if temp2[cnt][0].get(str(temp['Ad_number'])) is not None:
                        score += 0.2
                    if temp2[cnt][1].get(str(temp['Ad_number'])) is not None:
                        score += 0.1
                    match.append([score, i['page_number'], magazine['Id']])
                    cnt += 1
            match.sort(reverse=True)
            temp['Ad_page_match'] = []
            for score, i, id2 in match[:5]:
                temp['Ad_page_match'].append({"Score": score, "Page_number": i, "Magazine_id": id2})
            predict.append(temp)
        return predict

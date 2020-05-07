from application.ad_topic_model import AdTopicModel
import time

from nltk.corpus import wordnet


def calculate_wup_score(word1, word2, synset, calculation_needed):
    if calculation_needed is False:
        return 0
    if word2 in synset:
        word2_syn = synset[word2]
    else:
        try:
            synset[word2] = wordnet.synsets(word2)[0]
            word2_syn = synset[word2]
        except:
            synset[word2] = None
            word2_syn = None
    if word1 in synset:
        word1_syn = synset[word1]
    else:
        try:
            synset[word1] = wordnet.synsets(word1)[0]
            word1_syn = synset[word1]
        except:
            synset[word1] = None
            word1_syn = None
    try:
        wup_score = word2_syn.wup_similarity(word1_syn)
    except AttributeError:
        wup_score = 0
    if wup_score is None:
        wup_score = 0
    return wup_score


class AdMatch:
    def topic(self, ad):
        ad_text = []
        ad_id = []
        for temp in ad:
            ad_text.append(temp['words'])
            ad_id.append(temp['id'])
        topic_model_ad = AdTopicModel()
        ad_topic = topic_model_ad.predict(ad_text, ad_id)
        return ad_topic

    def ad_compare(self, lis, ads, synset, calculate_word_similarity=True):
        result = {}
        for i in lis:
            for ad in ads:
                for j in ad['words']:
                    wup_score = calculate_wup_score(i, j, synset, calculate_word_similarity)
                    if i == j or wup_score > 0.85:
                        try:
                            result[str(ad['id'])] += [[i, j]]
                        except KeyError:
                            result[str(ad['id'])] = [[i, j]]
        return result

    def keyword_match(self, ads, magazines):
        key_words = {}
        synset = {}
        start_time = time.time()
        for magazine in magazines:
            key_words[str(magazine['id'])] = []
            for page in magazine['pages']:
                page_keywords = []
                page_keywords1 = []
                for entity in page['named entity']:
                    page_keywords.append(entity['text'].lower())
                for tfidfWord in page['keywords']:
                    if tfidfWord == '':
                        continue
                    page_keywords1.append(tfidfWord.lower())
                match = self.ad_compare(page_keywords, ads, synset, calculate_word_similarity=False)
                match1 = self.ad_compare(page_keywords1, ads, synset)
                key_words[str(magazine['id'])].append([match, match1])
        print('\n\n---------- adCompare finished: took ', str(time.time() - start_time), ' seconds')
        return key_words

    def predict(self, data, top):
        """
            {
            "ad": [{ "id": 52,
                 "words": ["watch" , "collection" , "blancpain" , "wristwatch" , "women"] },
                 ....
               ] (advertisement format example),

           "magazines": [{   "id": 12,
                           "pages":  [{"topic": [{"category": "Luxury",
                                            "score": 0.7195,
                                            "words": ....,
                                            "index": 180}...]
                                   "named entity": [],
                                   "keywords": ["blancpain", "collection", "watch", "women", "wristwatch"],
                                   "page_number": 53}.. ]
                   }, ...] (magazine format example)}
        """
        ad = data['ad']
        magazines = data['magazines']
        ad_topic = self.topic(ad)
        ad_keywords = self.keyword_match(ad, magazines)
        predict = []
        for magazine in magazines:
            temp2 = ad_keywords[str(magazine['id'])]
            for a in ad_topic:
                cnt = 0
                temp = {'ad_page_match': [], 'ad_number': a['ad_number']}
                match = []
                for i in magazine["pages"]:
                    score = 0
                    for q in a['topic']:
                        for j in i['topic']:
                            if not j['category'] == 'unknown' and j['index'] == q['index']:
                                score += (j['score'] + q['score']) / 2
                                break
                    score *= 0.7
                    ner_match = temp2[cnt][0].get(str(temp['ad_number']))
                    if ner_match is not None:
                        number_of_match = len(ner_match)
                        if number_of_match == 1:
                            score += 0.15
                        if number_of_match == 2:
                            score += 0.18
                        if number_of_match >= 3:
                            score += 0.2
                    keyword_match = temp2[cnt][1].get(str(temp['ad_number']))
                    if keyword_match is not None:
                        number_of_match = len(keyword_match)
                        if number_of_match == 1:
                            score += 0.04
                        if number_of_match == 2:
                            score += 0.08
                        if number_of_match >= 3:
                            score += 0.1
                    if score != 0:
                        match.append([score, i['page_number'], magazine['id']])
                    cnt += 1
                match.sort(reverse=True)
                for score, i, id2 in match[:top]:
                    temp['ad_page_match'].append({"score": round(score, 5), "page_number": i, "magazine_id": id2})
            predict.append({"magazine_id": magazine['id'], "ad_match": temp})
        return predict

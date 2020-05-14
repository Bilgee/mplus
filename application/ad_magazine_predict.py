from application.ad_topic_model import AdTopicModel
import time
from log import logger

from nltk.corpus import wordnet


def calculate_wup_score(word1, word2, synset, calculation_needed):
    """Calculating similarity score between word1 and word2

    Parameters
    ----------
    word1: str
    word2: str
    synset: dict
        saves synonym set of nltk.wordnet to save time on multiple call
    calculation_needed: bool
        if false returns 0

    Returns
    -------
    float
        number between 0 and 1
    """
    if calculation_needed is False:
        return 0
    if word2 not in synset:
        if wordnet.synsets(word2):
            synset[word2] = wordnet.synsets(word2)[0]
        else:
            synset[word2] = None
    word2_syn = synset[word2]

    if word1 not in synset:
        if wordnet.synsets(word1):
            synset[word1] = wordnet.synsets(word1)[0]
        else:
            synset[word1] = None
    word1_syn = synset[word1]
    if word1_syn and word2_syn:
        wup_score = word2_syn.wup_similarity(word1_syn)
        if wup_score is None:
            wup_score = 0
    else:
        wup_score = 0

    return wup_score


def topic(ad):
    """

    Parameters
    ----------
    ad : list
        ad data
    Returns
    -------
    list
        predicted topics of ad
    """
    ad_text = []
    ad_id = []
    for temp in ad:
        ad_text.append(temp['words'])
        ad_id.append(temp['id'])
    topic_model_ad = AdTopicModel("en")
    ad_topic = topic_model_ad.predict(ad_text, ad_id)
    return ad_topic


def ad_compare(lis, ads, synset, calculate_word_similarity=True):
    """Match similar words from list to ad's words

    Parameters
    ----------
    lis : list
        list containing strings
    ads : list
        list containing ads
    synset : dict
        saves synonym set of nltk.wordnet to save time on multiple call
    calculate_word_similarity : bool, optional
        false if words have to exact same. ==

    Returns
    -------
    set
        set with tuples of matched words. i.e. {(wordFromLis1, wordFromAds1),(wfl2,wfa2)}
    """
    result = {}
    for ad in ads:
        result[str(ad['id'])] = set()
        for i in lis:
            for j in ad['words']:
                wup_score = calculate_wup_score(i, j, synset, calculate_word_similarity)
                if i == j or wup_score > 0.85:
                    result[str(ad['id'])].add((i, j))
    return result


def match_keywords(ads, magazines):
    """match magazine keywords, and Named Entities with Ads description words

    Parameters
    ----------
    ads: list[dict]
        input from json, list of dict
    magazines: list[dict]
        input from json, list of dict
    Returns
    -------
    dict
        dictionary with magazine ids as keys, and matched words as values
    """
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
            match = ad_compare(page_keywords, ads, synset, calculate_word_similarity=False)
            match1 = ad_compare(page_keywords1, ads, synset)
            key_words[str(magazine['id'])].append([match, match1])
    logger.info(f'adCompare finished: took {time.time() - start_time} seconds')
    return key_words


class AdMatch:

    def predict(self, data, top):
        """

        Parameters
        ----------
        data : dict
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
        top : int
            butsaah top page iin too

        Returns
        -------
        list
            Predictions
        """
        ad = data['ad']
        magazines = data['magazines']
        ad_topic = topic(ad)
        ad_keywords = match_keywords(ad, magazines)
        predict = []
        for magazine in magazines:
            temp2 = ad_keywords[str(magazine['id'])]
            temp3 = {"magazine_id": magazine['id'], "ad_match": []}
            for a in ad_topic:
                cnt = 0
                temp = {'ad_page_match': [], 'ad_number': a['ad_number']}
                match = []
                for i in magazine["pages"]:
                    score = 0
                    for q in a['topic']:
                        if q['category'] == 'unknown':
                            continue
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
                    if score < 0.15:
                        break
                    temp['ad_page_match'].append({"score": round(score, 5), "page_number": i, "magazine_id": id2})
                temp3["ad_match"].append(temp)
            predict.append(temp3)
        return predict

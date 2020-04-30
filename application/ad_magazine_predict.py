from application.topic_model import TopicModel
from nltk.corpus import wordnet


class AdMatch:
    def topic(self, ad):
        ad_text = []
        ad_id = []
        ner_text = []
        for temp in ad:
            ad_text.append(temp['Words'])
            ad_id.append(temp['Id'])
            ner_text.append("")
        topic_model_en2 = TopicModel()
        ad_topic = topic_model_en2.predict(ad_text, ner_text, ad_id)
        return ad_topic

    def ad_compare(self, lis, ads):
        result = {}
        for i in lis:
            for index, ad in enumerate(ads):
                for j in ad['Words']:
                    try:
                        wup_score = wordnet.synsets(i)[0].wup_similarity(wordnet.synsets(j)[0])
                    except:
                        wup_score = 0
                    if i == j or (wup_score is not None and wup_score > 0.8):
                        try:
                            result[str(ad['Id'])] += [i, j]
                        except:
                            result[str(ad['Id'])] = [i, j]
        return result

    def keyword_match(self, ads, magazines):
        key_words = {}
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
                match = self.ad_compare(page_keywords, ads)
                match1 = self.ad_compare(page_keywords1, ads)
                key_words[str(magazine['Id'])].append([match, match1])
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
            temp['Ad_number'] = a['page_number']
            for q in a['Topic']:
                for magazine in magazines:
                    cnt = 0
                    temp2 = ad_keywords[str(magazine['Id'])]
                    for i in magazine["Pages"]:
                        for j in i['Topic']:
                            if not j['Category'] == 'Unknown' and j['Index'] == q['Index']:
                                score = (j['Score'] + q['Score']) / 2 * 0.7
                                if temp2[cnt][0].get(str(temp['Ad_number'])) is not None:
                                    score += 0.2
                                if temp2[cnt][1].get(str(temp['Ad_number'])) is not None:
                                    score += 0.1
                                temp3={"Score": score,"Page_number": i['page_number'],"Magazine_id": magazine['Id']}
                                match.append(temp3)
                        cnt += 1
            match.sort(reverse=True)
            temp['Ad_page_match'] = match[:5]
            predict.append(temp)
        return predict

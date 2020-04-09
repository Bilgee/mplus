import json
from log import logger
import gensim
from gensim import corpora

class TopicModel:
    def __init__(self, model):
        """init class object

        Arguments:
            model_path {string} -- [a path to read a trained model]
            features {list} -- [list of features as a string]
        """
        self.model = gensim.models.LdaModel.load(model)
        with open("application/Topics.json") as json_file:
            self.Topics_genre = json.load(json_file)
    def predict(self, clean_text, ner):
        dictionary = corpora.Dictionary(clean_text)
        bow_corpus = [dictionary.doc2bow(doc) for doc in clean_text]
        topic_predictions = self.model[bow_corpus]
        top_number = 2
        best_topics = [[(topic, round(wt, 3))
                        for topic, wt in sorted(topic_predictions[i],
                                                key=lambda row: -row[1]) [:top_number]]
                            for i in range(len(topic_predictions))]
        Predicted=[]
        # tf_idf
        tf_idf = gensim.models.TfidfModel(bow_corpus)
        corpus_tfidf = tf_idf[bow_corpus]
        top_8_or_so_words = []
        for doc in corpus_tfidf:
            doc.sort(key = lambda x: x[1],reverse=True)
            tmp = []
            cnt = 0
            for word in doc:
                tmp+=[dictionary[word[0]]]
                cnt+=1
                if cnt == 8:
                    break
            top_8_or_so_words+=[tmp]
        cnt=0
        for doc in best_topics:
            temp=[]
            for top in doc:
                page={}
                page["Score"]=top[1]
                page["Category"]=self.Topics_genre['Topics'][top[0]]['Category']
                page["Words"]=[]
                for word in self.Topics_genre['Topics'][top[0]]['Topic']:
                    temp2={}
                    temp2["Text"]=word[0]
                    temp2["Score"]=round(word[1], 3)
                    page["Words"].append(temp2)
                temp.append(page)
            temp2={}
            temp2["Topic"]=temp
            temp2["Named Entity"]=[]
            for word in ner[cnt]:
                temp={}
                if word == '':
                    continue
                temp["Text"]=word[0]
                temp["Label"]=word[1]
                temp2["Named Entity"].append(temp)
            temp2["Keywords"]=top_8_or_so_words[cnt]
            cnt+=1
            Predicted.append(temp2)
        return Predicted

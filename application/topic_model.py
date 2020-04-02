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
        
    def predict(self, clean_text, ner):
        dictionary = corpora.Dictionary(clean_text)
        bow_corpus = [dictionary.doc2bow(doc) for doc in clean_text]
        topic_predictions = self.model[bow_corpus]
        best_topics = [[(topic, round(wt, 3))
                        for topic, wt in sorted(topic_predictions[i],
                                                key=lambda row: -row[1]) [:2]]
                            for i in range(len(topic_predictions))]
        with open("application/Topics.json") as json_file:
            Topics_genre = json.load(json_file)
        Predicted=[]
        cnt=0
        for doc in best_topics:
            temp=[]
            for top in doc:
                page={}
                page["Score"]=top[1]
                page["Category"]=Topics_genre['Topics'][top[0]]['Category']
                page["Words"]=Topics_genre['Topics'][top[0]]['Topic']
                temp.append(page)
            temp2={}
            temp2["Topic:"]=temp
            temp2["Named Entity:"]=ner[cnt]
            cnt+=1
            Predicted.append(temp2)
        return Predicted

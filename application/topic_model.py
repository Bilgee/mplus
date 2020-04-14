import json
from log import logger
import gensim
from gensim import corpora
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

class TopicModel:
    def __init__(self, model):
        """init class object

        Arguments:
            model -- [Topics]
            Tdictionary  -- [Topic words dictionary] 
        """
        with open("application/Newtopic.txt") as json_file:
            self.model = json.load(json_file)
        with open("application/Tdictionary.txt") as json_file:
            self.Tdictionary = json.load(json_file)
    
    def Topics_Words(self,index,number,Model_topics):
        temp=[]
        j=0
        for word in Model_topics['Topics'][index]['Words']:
            if j==number:
                break
            a={}
            a["Text"]=word[0]
            a["Score"]=round(word[1],4)
            temp.append(a)
            j+=1
        return temp
    
    def Topics_temp(self,category,score,total):
        temp={}
        temp['Category']=category
        temp['Score']=round((score/total),4)
        return temp
    
    def Topic_score(self,page,Tdictionary,dictionary):
        total=0
        t={} # topic buriin niit score
        for word in page:
            w=dictionary[word[0]]
            w=wordnet_lemmatizer.lemmatize(w)
            try:
                temp2=Tdictionary[w]
            except KeyError:
                continue
            for q in temp2:
                j=1
                i=0
                for p in range(word[1]):
                    i+=q['Score']*j
                    j*=0.9
                total+=i
                try:
                    t[q['Index']][0]+=i # t[0]+=0.05*2 -- 0 ni topiciin index, 0.05 ni ugiin onoo, 2 ni paged orson tuhain ugnii too 
                    t[q['Index']][1]+=q['Score']
                except KeyError:
                    t[q['Index']]=[]
                    t[q['Index']].append(i)
                    t[q['Index']].append(0)
        return t,total
    
    def Max_score(self,temp,tlist,Model_topics,total):
        temp['Topics'].append(self.Topics_temp(tlist[-1][2],tlist[-1][0],total))
        temp['Topics'][0]['Words']=self.Topics_Words(tlist[-1][1],10,Model_topics)
        try:
            temp['Topics'].append(self.Topics_temp(tlist[-2][2],tlist[-2][0],total))
            temp['Topics'][1]['Words']=self.Topics_Words(tlist[-2][1],10,Model_topics)
        except:
            return temp
        return temp
    
    def Max_category(self,temp,tlist,Model_topics,total):
        if not tlist[-2][2]==tlist[-3][2] or tlist[-3][0]+tlist[-2][0]<tlist[-1][0]:
            temp=self.Max_score(temp,tlist,Model_topics,total)
            return temp
        temp['Topics'].append(self.Topics_temp(tlist[-2][2],tlist[-3][0]+tlist[-2][0],total))
        temp['Topics'][0]['Words']=[]
        j=0
        ug=[]
        for word,score in Model_topics['Topics'][tlist[-2][1]]['Words']:
            if j==10:
                break
            ug.append([score,word])
            j+=1
        j=0
        for word,score in Model_topics['Topics'][tlist[-3][1]]['Words']:
            if j==10:
                break
            ug.append([score,word])
            j+=1
        ug.sort()
        temp['Topics'][0]['Words'].append(ug[-1][1])
        j=0
        for i in range(len(ug)-1):
            if ug[(-1)*i-2][1]==ug[(-1)*i-1][1]:
                continue
            if j==10:
                break
            j+=1
            a={}
            a["Text"]=ug[(-1)*i-2][1]
            a["Score"]=round(ug[(-1)*i-2][0],4)
            temp['Topics'][0]['Words'].append(a)
        temp['Topics'].append(self.Topics_temp(tlist[-1][2],tlist[-1][0],total))
        temp['Topics'][1]['Words']=self.Topics_Words(tlist[-1][1],10,Model_topics)
        return temp
    
    def topic_predict(self,bow_corpus,dictionary):
        Predicted=[] # Huudas bureer hamaaragdah topiciin huwiig oruulna
        for page in bow_corpus:
            temp={}
            temp['Topics']=[]
            t,total=self.Topic_score(page,self.Tdictionary,dictionary)
            tlist=[]
            for q in t:
                temp2=self.model['Topics'][q]['Category'] # q ni topiciin index
                if t[q][1]>0.05:
                    tlist.append([t[q][0],q,temp2])
                else:
                    total-=t[q][1]
            tlist.sort()
            if total==0 or len(tlist)==0:
                temp2={}
                temp2['Category']='Unknown'
                temp2['Score']=0
                a={}
                a["Text"]=""
                a["Score"]=0
                temp2['Words']=[a]
                temp['Topics'].append(temp2)
                Predicted.append(temp)
                continue
            clist=[]
            if len(tlist)==1 or len(tlist)==2:
                temp=self.Max_score(temp,tlist,self.model,total)
                Predicted.append(temp)
                continue
            elif tlist[-1][0]*0.8>tlist[-2][0] or tlist[-1][2]==tlist[-2][2]:
                temp=self.Max_score(temp,tlist,self.model,total)
                Predicted.append(temp)
                continue
            else:
                temp=self.Max_category(temp,tlist,self.model,total)
                Predicted.append(temp)
                continue
        return Predicted
    
    def predict(self, clean_text, ner, page_numbers):
        dictionary = corpora.Dictionary(clean_text)
        bow_corpus = [dictionary.doc2bow(doc) for doc in clean_text]
        topic_predictions = self.topic_predict(bow_corpus,dictionary)
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
        for doc in topic_predictions:
            temp2={}
            temp2["Topic"]=doc['Topics']
            temp2["Named Entity"]=[]
            for word in ner[cnt]:
                temp={}
                if word == '':
                    continue
                temp["Text"]=word[0]
                temp["Label"]=word[1]
                temp2["Named Entity"].append(temp)
            temp2["Keywords"]=top_8_or_so_words[cnt]
            temp2["page_number"] = page_numbers[cnt]
            cnt+=1
            Predicted.append(temp2)
        return Predicted

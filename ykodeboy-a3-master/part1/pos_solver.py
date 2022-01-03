###################################
# CS B551 Spring 2021, Assignment #3
#
# Your names and user ids:
#
# (Based on skeleton code by D. Crandall)
#


import random
import math
import sys
import numpy as np



# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

    def __init__(self):
        self.log_p_word_given_speech={}
        self.posterior_simple=0
        self.transition_p={}
        self.dict_speech_count={}
        self.log_word_given_speech2={}
        self.log_speech_prob={}


    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        if model == "Simple":
            simple_posterior=0
            for i in range(0,len(sentence)):
                if("'s" in sentence[i] and sentence[i] not in self.log_p_word_given_speech):
                    word=sentence[i].replace("'s","")
                else:
                    word=sentence[i]
                simple_posterior= simple_posterior+self.log_p_word_given_speech.get(word,{}).get(label[i],-16)+self.log_speech_prob.get(label[i])
            return simple_posterior
            # return -999
        elif model == "HMM":
            word=sentence[0]
            if("'s" in word and word not in self.log_p_word_given_speech):
                word=word.replace("'s","")
            hmm_value=math.log(self.transition_p['s'].get(label[0]))+self.log_p_word_given_speech.get(word,{}).get(label[0],-16)
            for i in range(1,len(sentence)):
                word=sentence[i]
                if("'s" in word and word not in self.log_p_word_given_speech):
                    word=word.replace("'s","")
                hmm_value=hmm_value+math.log(self.transition_p[label[i-1]].get(label[i],0.0000000000000001))+self.log_p_word_given_speech.get(word,{}).get(label[i],-16)
            return hmm_value
            # return -999
        elif model == "Complex":
            return self.cal_posterior_gibs(label,sentence)
            # return -999
        else:
            print("Unknown algo!")
    
    def posterior_simple_cal(self,sentence):     
        speech_list=[]
        speech_parts=list(self.dict_speech_count.keys())
        for word in sentence:
            if("'s" in word and word not in self.log_p_word_given_speech):
                word=word.replace("'s","")
            values=[]
            for k in range(0,len(speech_parts)):
                values.append(self.log_p_word_given_speech.get(word,{}).get(speech_parts[k],-16)+self.log_speech_prob.get(speech_parts[k]))
            max_index=values.index(max(values))
            speech_list.append(speech_parts[max_index])
        return speech_list

    def maxium_select(self,l,i,j,parts_of_speech):
        max_value=-sys.maxsize
        for k in range(0,len(parts_of_speech)):
            # change default value
            p=l[k][j-1]+math.log(self.transition_p[parts_of_speech[k]].get(parts_of_speech[i],0.0000000000000001))
            if(p>max_value):
                max_value=p
                max_speech=k
        return [max_value,max_speech]


    def posterior_viterbi_cal(self,sentence):
        parts_speech= list(self.dict_speech_count.keys())
        list_speech=[]
        l=[[0 for i in range(0,len(sentence))] for j in range(0,len(parts_speech))]
        selected_speech=[[0 for i in range(0,len(sentence))] for j in range(0,len(parts_speech))]
        for i in range(0,len(parts_speech)):
            # change default value
            word=sentence[0]
            if("'s" in word and word not in self.log_p_word_given_speech):
                word=word.replace("'s","")
            l[i][0]=math.log(self.transition_p['s'].get(parts_speech[i]),0.0000000000000001)+self.log_p_word_given_speech.get(word,{}).get(parts_speech[i],-16)
        for j in range(1,len(sentence)):
            word=sentence[j]
            if("'s" in word and word not in self.log_p_word_given_speech):
                word=word.replace("'s","")
            for i in range(0,len(parts_speech)):
                [max_value,max_speech]=self.maxium_select(l,i,j,parts_speech)
                selected_speech[i][j]=max_speech
                l[i][j]=self.log_p_word_given_speech.get(word,{}).get(parts_speech[i],-16)+ max_value 
        
        max_value=l[0][len(sentence)-1]
        max_speech=0
        for k in range(1,len(parts_speech)):
            if(max_value<l[k][len(sentence)-1]):
                max_value=l[k][len(sentence)-1]
                max_speech=k
        
        list_speech.append(parts_speech[max_speech])
        k=max_speech
        for i in range(len(sentence)-1,0,-1):
            list_speech.append(parts_speech[selected_speech[k][i]])
            k=selected_speech[k][i]
        list_speech.reverse()
        return list_speech

    def cal_posterior_gibs(self,labels,sentence):
        sum_posterior=0
        for i in range(0,len(labels)):
            word=sentence[i]
            if("'s" in word and word not in self.log_p_word_given_speech):
                word=word.replace("'s","")
            if(i==0):
                # sum_posterior=sum_posterior+math.log(self.transition_p['s'].get(labels[i],0.0000000000000001))
                sum_posterior=sum_posterior+math.log(self.transition_p['s'].get(labels[i],0.0000000000000001))+self.log_p_word_given_speech.get(word,{}).get(labels[i],-16)
            else:
                # sum_posterior=sum_posterior+self.log_word_given_speech2[word].get(labels[i-1]+','+labels[i],-16)
                # sum_posterior=sum_posterior+math.log(self.transition_p[labels[i-1]].get(labels[i],0.0000001))+self.log_p_word_given_speech[word].get(labels[i],-16)
                sum_posterior=sum_posterior+math.log(self.transition_p[labels[i-1]].get(labels[i],0.0000000000000001))+self.log_word_given_speech2.get(word,{}).get(labels[i]+','+labels[i-1],-16)
        return sum_posterior

    # professors video
    def sample(self,distro):
        dist=list(distro.items())
        return np.random.choice([dist[i][0] for i in range(len(dist))],p=[dist[i][1] for i in range(len(dist))])

    def get_posterior_gibs_s(self,labels,sentence,s):
        sum_posterior=0
        prob_value=0
        # for i in range(0,len(labels)):
        word=sentence[s]
        if("'s" in word and word not in self.log_p_word_given_speech):
            word=word.replace("'s","")
        if(s==0):
            if len(sentence)==1:
                prob_value=math.log(self.transition_p['s'].get(labels[s],0.0000000000000001))+self.log_p_word_given_speech.get(word,{}).get(labels[s],-16)
            else:
                front_word=sentence[s+1]
                if("'s" in front_word and front_word not in self.log_p_word_given_speech):
                    front_word=front_word.replace("'s","")
                prob_value=math.log(self.transition_p['s'].get(labels[s],0.0000000000000001))+math.log(self.transition_p[labels[s]].get(labels[s+1],0.0000000000000001))+self.log_p_word_given_speech.get(word,{}).get(labels[s],-16)+self.log_word_given_speech2.get(front_word,{}).get(labels[s+1]+','+labels[s],-16)
                # prob_value=self.transition_p['s'].get(labels[s],0.0000000000000001)*self.transition_p[labels[s]].get(labels[s+1],0.0000000000000001)*self.log_p_word_given_speech.get(word,{}).get(labels[s],-16)+self.log_word_given_speech2.get(front_word,{}).get(labels[s+1]+','+labels[s],-16)
        elif s==len(sentence)-1:
            prob_value=math.log(self.transition_p[labels[s-1]].get(labels[s],0.0000000000000001))+self.log_word_given_speech2.get(word,{}).get(labels[s]+','+labels[s-1],-16)
        else:
            front_word=sentence[s+1]
            if("'s" in front_word and front_word not in self.log_p_word_given_speech):
                front_word=front_word.replace("'s","")
            prob_value=math.log(self.transition_p[labels[s-1]].get(labels[s],0.0000000000000001))+math.log(self.transition_p[labels[s]].get(labels[s+1],0.0000000000000001))+self.log_word_given_speech2.get(word,{}).get(labels[s]+','+labels[s-1],-16)+self.log_word_given_speech2.get(front_word,{}).get(labels[s+1]+','+labels[s],-16)
        return prob_value



    def posterior_gibbs_cal(self,sentence):
        list_speech=[]
        parts_speech= list(self.dict_speech_count.keys())
        for i in range(0,len(sentence)):
            r=random.randint(0, 9)
            list_speech.append("noun")
        list2=list_speech.copy()
        for i in range(0,1000):            
            for j in range(0,len(list2)):
                values=[]
                value_prob=[]
                for k in range(0,len(parts_speech)):
                    list2[j]=parts_speech[k]
                    cal_value=self.get_posterior_gibs_s(list2,sentence,j)
                    value_prob.append(math.exp(cal_value))
                distro_values={parts_speech[i]:float(value_prob[i])/sum(value_prob) for i in range(0,len(parts_speech))}
                selected_speech=self.sample(distro_values)
                # max_value=max(values)
                list2[j]=selected_speech
        return list2
    # def posterior_gibbs_cal(self,sentence):
    #     list_speech=[]
    #     parts_speech= list(self.dict_speech_count.keys())
    #     for i in range(0,len(sentence)):
    #         r=random.randint(0, 9)
    #         list_speech.append("noun")
    #     list2=list_speech.copy()
    #     for i in range(0,1000):            
    #         for j in range(0,len(list2)):
    #             values=[]
    #             value_prob=[]
    #             for k in range(0,len(parts_speech)):
    #                 list2[j]=parts_speech[k]
    #                 cal_value=self.cal_posterior_gibs(list2,sentence)
    #                 values.append(cal_value)
    #                 # value_prob.append(math.exp(cal_value))
    #             # for i in values:
    #             #     value_prob.append(math.exp(i))
    #             # distro_values={parts_speech[i]:float(value_prob[i])/sum(value_prob) for i in range(0,len(parts_speech))}
    #             # selected_speech=self.sample(distro_values)
    #             max_value=max(values)
    #             # list2[j]=selected_speech
    #             list2[j]=parts_speech[values.index(max_value)]
    #             # print(self.cal_posterior_gibs(list2,sentence))
    #     return list2



                
        
        

    # Do the training!
    #
    def train(self, data):
        dict_word_speech_count={}
        log_p_word_given_speech={}
        dict_word_count={}
        dict_speech_count={}
        dict_p_transition={}
        dict_p_word_given_2speech={}
        for item in data:
            for i in range(0,len(item[0])):
                dict_word_speech_count[item[0][i]]=dict_word_speech_count.get(item[0][i],{})
                dict_word_speech_count[item[0][i]][item[1][i]]=dict_word_speech_count[item[0][i]].get(item[1][i],0)+1
                dict_speech_count[item[1][i]]=dict_speech_count.get(item[1][i],0)+1
                if i==0:
                    dict_p_transition["s"]=dict_p_transition.get("s",{})
                    dict_p_transition["s"][item[1][i]]=dict_p_transition["s"].get(item[1][i],0)+1

                if i+1 <len(item[0]):
                    dict_p_transition[item[1][i]]=dict_p_transition.get(item[1][i],{})
                    dict_p_transition[item[1][i]][item[1][i+1]]=dict_p_transition[item[1][i]].get(item[1][i+1],0)+1
                if(i!=0):
                    dict_p_word_given_2speech[item[0][i]]=dict_p_word_given_2speech.get(item[0][i],{})
                    dict_p_word_given_2speech[item[0][i]][item[1][i]+','+item[1][i-1]]=dict_p_word_given_2speech[item[0][i]].get(item[1][i]+','+item[1][i-1],0)+1

        self.dict_speech_count=dict_speech_count
        for word in dict_word_speech_count:
            log_p_word_given_speech[word]=log_p_word_given_speech.get(word,{})
            for speech in dict_word_speech_count[word].keys():
                value=math.log(dict_word_speech_count[word].get(speech,0))- math.log(dict_speech_count[speech])
                log_p_word_given_speech[word][speech]=value
        self.log_p_word_given_speech=log_p_word_given_speech
        # transition probability
        for item in dict_p_transition["s"]:
            dict_p_transition["s"][item]=dict_p_transition["s"][item]/len(data)
        for speech in dict_speech_count:
            for item in dict_p_transition[speech]:
                dict_p_transition[speech][item]= dict_p_transition[speech][item]/dict_speech_count[speech]
        self.transition_p=dict_p_transition
        # probability word given two speeches
        for word in dict_p_word_given_2speech:
            for item in list(dict_p_word_given_2speech[word].keys()):
                [part_i,part_i_1]=item.split(',')
                dict_p_word_given_2speech[word][item]= math.log(dict_p_word_given_2speech[word][item])-math.log(dict_p_transition[part_i_1].get(part_i,0.0000000000000001))
        self.log_word_given_speech2=dict_p_word_given_2speech
        for s in dict_speech_count:
            self.log_speech_prob[s]=self.log_speech_prob.get(s,0)+math.log(dict_speech_count[s])-math.log(sum(dict_speech_count.values()))
        
        
    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        max_speech=self.posterior_simple_cal(sentence)
        return max_speech

    def hmm_viterbi(self, sentence):
        return self.posterior_viterbi_cal(sentence)

    def complex_mcmc(self, sentence):
        return self.posterior_gibbs_cal(sentence)



    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")


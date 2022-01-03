# classify.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAMES AND USER IDs HERE
#
# Based on skeleton code by D. Crandall, March 2021
#

import sys
import math

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")
    
    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to documents
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each document
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def get_class_probability(train_data):
    classA_east_count=train_data["labels"].count("EastCoast")
    classB_west_count=train_data["labels"].count("WestCoast")
    classA_PA= classA_east_count/(classA_east_count+classB_west_count)
    classB_PB= classB_west_count/(classA_east_count+classB_west_count)
    return[classA_PA,classB_PB]

def get_words(sentence):
    words = sentence.split(' ')
    for i in range(0,len(words)):
        words[i]=(''.join(e for e in words[i] if e.isalnum())).lower()
    # words = [ elem for elem in words if elem != '']
    return words


def get_word_count(train_data):
    dA={}
    dB={}
    TotalA=0
    TotalB=0
    words_A=[]
    words_B=[]
    vocabulary=[]
    for i in range(0, len(train_data["labels"])):
        k=train_data["objects"][i]
        words=get_words(train_data["objects"][i])
        vocabulary.extend(words)
        if train_data["labels"][i] == "EastCoast":
            for word in words:
                if word not in dA:
                    dA[word]=1
                else:
                    dA[word]=dA[word]+1
            # TotalA=TotalA+len(words)
            words_A.extend(words)
        elif train_data["labels"][i] == "WestCoast":
            for word in words:
                if word not in dB:
                    dB[word]=1
                else:
                    dB[word]=dB[word]+1
            words_B.extend(words)
    vocabulary=set(vocabulary)
    TotalA=len(words_A)
    TotalB=len(words_B)
    return [dA,dB,TotalA,TotalB,len(dA),len(dB),len(vocabulary)]  

def get_word_given_class(word_count,class_word_count,distinct_count,P,total_vocab):
    dict_word_given_class={}
    # for word in word_count.keys():
    #     # k=word_count[word]/class_word_count
    #     dict_word_given_class[word]=word_count[word]/class_word_count
    # laplacian
    for word in word_count.keys():
        dict_word_given_class[word]=(word_count[word]+1)/(class_word_count+ (1* total_vocab))
    return dict_word_given_class

def get_prob_test(word,word_count,class_word_count,distinct_count,P,total_vocab):   
    A=(word_count.get(word,0)+1)/(class_word_count+ (1* total_vocab))
    return A




def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!
    # get_class_probability(train_data)
    [PA,PB]= get_class_probability(train_data)
    [wordA_count,wordB_count,TotalA,TotalB,distinct_A,distinct_B,total_vocab]=get_word_count(train_data)
    l=[]
    for i in range(0,len(test_data["objects"])):
        classA=PA
        classB=PB
        log_A= math.log(PA)
        log_B= math.log(PB)
        words=get_words(test_data["objects"][i])
        for word in words:
            A=get_prob_test(word,wordA_count,TotalA,distinct_A,PA,total_vocab)
            B=get_prob_test(word,wordB_count,TotalB,distinct_B,PB,total_vocab)
            classA=classA*A
            log_A=log_A+math.log(A)
            classB=classB*B
            log_B=log_B+math.log(B)
        # ratio=classA/classB
        ratio=math.exp(log_A-log_B)
        if(ratio>1):
            l.append("EastCoast")
        else:
            l.append("WestCoast")

    return l
    # return [test_data["classes"][0]] * len(test_data["objects"])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # train_file="./part3/tweets.location.train.txt"
    # test_file="./part3/tweets.location.test.txt"
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(train_data["classes"] != test_data["classes"] or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))

        

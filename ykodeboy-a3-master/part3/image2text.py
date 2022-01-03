#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (insert names here)
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import math

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25

def read_data(fname):
    exemplars = []
    file = open(fname, 'r');
    for line in file:
        data = tuple([w for w in line.split()])
        exemplars += [ (data[0::2]), ]
    return exemplars

def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

def get_probability_shape_given_letter(train_list,test_list):
    noise=0
    match=0.9
    not_match=0.1
    probability=1
    for i in range(0,CHARACTER_HEIGHT):
        for j in range(0,CHARACTER_WIDTH):
            if train_list[i][j]!=test_list[i][j]:
                probability=probability*not_match
            else:
                probability=probability*match
    return probability
    # return ((CHARACTER_WIDTH*CHARACTER_HEIGHT)-noise*13)
    # # return ((400)-noise*10)
    # return (1-((noise*8)/(CHARACTER_WIDTH*CHARACTER_HEIGHT)))


# def train_data1(data):
#     transition_prob={}
#     letter_count={}
#     letter_probability={}
#     word_list=[]
#     for item in data:
#         words=list(item)
#         for i in range(0,len(words)):
#             if words[i]=="''":
#                 words[i]='"'
#             elif words[i]=="``":
#                 words[i]='"'
#             elif words[i]=="`":
#                 words[i]="'"
#         word_list.extend(words)
#     word_list=list(set(word_list))
#     for word in word_list:
#         for i in range(0,len(word)):
#             letter_count[word[i]]=letter_count.get(word[i],0)+1
#             if i==0:
#                 transition_prob[" "]=transition_prob.get(" ",{})
#                 transition_prob[" "][word[i]]=transition_prob[" "].get(word[i],0)+1
#             if i+1 < len(word):
#                 transition_prob[word[i]]=transition_prob.get(word[i],{})
#                 transition_prob[word[i]][word[i+1]]=transition_prob[word[i]].get(word[i+1],0)+1
#             if i==len(word)-1:
#                 transition_prob[word[i]]=transition_prob.get(word[i],{})
#                 transition_prob[word[i]][" "]=transition_prob[word[i]].get(" ",0)+1
#     for item in transition_prob[" "]:
#         transition_prob[" "][item]=transition_prob[" "][item]/len(word_list)
#     letter_keys=list(transition_prob.keys())
#     letter_keys.remove(" ")
#     for key in letter_keys:
#         for item in transition_prob[key]:
#             transition_prob[key][item]=(transition_prob[key][item])/(letter_count[key])
#             # transition_prob[key][item]=math.log(transition_prob[key][item])-math.log(letter_count[key])
#     for letter in letter_count:
#         letter_probability[letter]=letter_probability.get(letter,0)+((letter_count[letter])/(sum(list(letter_count.values()))))
#         # letter_probability[letter]=letter_probability.get(letter,0)+math.log(letter_count[letter])-math.log(sum(list(letter_count.values())))

#     return (transition_prob,letter_probability)


def train_data(data):
    transition_prob={}
    letter_count={}
    letter_probability={}
    word_list=[]
    for item in data:
        words=list(item)
        for i in range(0,len(words)):
            if words[i]=="''":
                words[i]='"'
            elif words[i]=="``":
                words[i]='"'
            elif words[i]=="`":
                words[i]="'"
        sentence=" ".join(words)
        for i in range(0,len(sentence)):
            letter_count[sentence[i]]=letter_count.get(sentence[i],0)+1
            if i==0:
                transition_prob["start"]=transition_prob.get("start",{})
                transition_prob["start"][sentence[i]]=transition_prob["start"].get(sentence[i],0)+1
            if i+1 < len(sentence):
                transition_prob[sentence[i]]=transition_prob.get(sentence[i],{})
                transition_prob[sentence[i]][sentence[i+1]]=transition_prob[sentence[i]].get(sentence[i+1],0)+1
            if i==len(sentence)-1:
                transition_prob[sentence[i]]=transition_prob.get(sentence[i],{})
                transition_prob[sentence[i]]["end"]=transition_prob[sentence[i]].get("end",0)+1
    for item in transition_prob["start"]:
        transition_prob["start"][item]=math.log(transition_prob["start"][item])-math.log(len(data))
        # transition_prob["start"][item]=transition_prob["start"][item]/len(data)
        # transition_prob["start"][item]=transition_prob["start"][item]
        # transition_prob["start"][item]=math.log(transition_prob["start"][item])-math.log(len(data))
    letter_keys=list(transition_prob.keys())
    letter_keys.remove("start")
    for key in letter_keys:
        for item in transition_prob[key]:
            transition_prob[key][item]=math.log(transition_prob[key][item])-math.log(letter_count[key])
            # transition_prob[key][item]=transition_prob[key][item]/letter_count[key]
            # transition_prob[key][item]=transition_prob[key][item]
    for letter in letter_count:
        letter_probability[letter]=letter_probability.get(letter,0)+math.log(letter_count[letter])-math.log(sum(list(letter_count.values())))
        # letter_probability[letter]=letter_probability.get(letter,0)+(letter_count[letter]/(sum(list(letter_count.values()))))
        # letter_probability[letter]=letter_probability.get(letter,0)+letter_count[letter]
        # letter_probability[letter]=letter_probability.get(letter,0)+math.log(letter_count[letter])-math.log(sum(list(letter_count.values())))
    return (transition_prob,letter_probability)



def maxium_select(l,i,j,TRAIN_LETTERS,transition_log_prob):
    max_value=-sys.maxsize
    for k in range(0,len(TRAIN_LETTERS)):
        # change default value
        p=l[k][j-1]+transition_log_prob[TRAIN_LETTERS[k]].get(TRAIN_LETTERS[i],-30)
        # p=l[k][j-1]*transition_log_prob[TRAIN_LETTERS[k]].get(TRAIN_LETTERS[i],0.000000000000001)
        if(p>max_value):
            max_value=p
            max_letter=k
    return [max_value,max_letter]


def veterbi_hmm(train_letters,test_letters,letter_log_probability,transition_log_prob):
    list_words=[]
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    l=[[0 for i in range(0,len(test_letters))] for j in range(0,len(TRAIN_LETTERS))]
    selected_letter=[[0 for i in range(0,len(test_letters))] for j in range(0,len(TRAIN_LETTERS))]
    for i in range(0,len(TRAIN_LETTERS)):
        l[i][0]=transition_log_prob['start'].get(TRAIN_LETTERS[i],-30)+math.log(get_probability_shape_given_letter(train_letters[TRAIN_LETTERS[i]],test_letters[0]))
        # l[i][0]=transition_log_prob['start'].get(TRAIN_LETTERS[i],0.000000000000001)*get_probability_shape_given_letter(train_letters[TRAIN_LETTERS[i]],test_letters[0])
    for j in range(1,len(test_letters)):
        for i in range(0,len(TRAIN_LETTERS)):
            [max_value,max_letter]=maxium_select(l,i,j,TRAIN_LETTERS,transition_log_prob)
            selected_letter[i][j]=max_letter
            l[i][j]=math.log(get_probability_shape_given_letter(train_letters[TRAIN_LETTERS[i]],test_letters[j]))+ max_value
            # l[i][j]=get_probability_shape_given_letter(train_letters[TRAIN_LETTERS[i]],test_letters[j])* max_value
            
    max_value=l[0][len(test_letters)-1]
    max_letter=0
    for k in range(1,len(TRAIN_LETTERS)):
        if(max_value<l[k][len(test_letters)-1]):
            max_value=l[k][len(test_letters)-1]
            max_letter=k
    list_words.append(TRAIN_LETTERS[max_letter])
    k=max_letter
    for i in range(len(test_letters)-1,0,-1):
        list_words.append(TRAIN_LETTERS[selected_letter[k][i]])
        k=selected_letter[k][i]
    list_words.reverse()
    return list_words






def simple(train_letters,test_letters,letter_log_probability):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    selected_letters=[]
    for item in test_letters:
        letters_prob=[]
        for letter in TRAIN_LETTERS:           
            p=letter_log_probability[letter]+math.log(get_probability_shape_given_letter(train_letters[letter],item))
            # p=get_probability_shape_given_letter(train_letters[letter],item)
            # p=math.log(get_probability_shape_given_letter(train_letters[letter],item))
            # p=get_probability_shape_given_letter(train_letters[letter],item)
            letters_prob.append(p)
        selected_index=letters_prob.index(max(letters_prob))
        selected_letters.append(TRAIN_LETTERS[selected_index])
    return selected_letters

    
#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)
data=read_data(train_txt_fname)
(transition_log_prob,letter_log_probability)=train_data(data)
s=simple(train_letters,test_letters,letter_log_probability)
s1=veterbi_hmm(train_letters,test_letters,letter_log_probability,transition_log_prob)
# k=get_probability_shape_given_letter(train_letters["s"],train_letters["s"])

## Below is just some sample code to show you how the functions above work. 
# You can delete this and put your own code here!


# Each training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:
print("\n".join([ r for r in train_letters['a'] ]))

# Same with test letters. Here's what the third letter of the test data
#  looks like:
print("\n".join([ r for r in test_letters[2] ]))



# The final two lines of your output should look something like this:
print("Simple: " + "".join(s))
print("   HMM: " + "".join(s1)) 



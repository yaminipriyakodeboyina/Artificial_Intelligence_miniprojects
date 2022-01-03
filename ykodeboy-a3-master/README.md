# a3

## Part 1:

### Parts of speech tagging

#### simple posterior probability
Figure 1b:

* Si= max(p(S)*p(S/Wi)) where i= all words in sentence
* Calculated maximun posterioor probability of each word and tool maximum  of all parts of speech and appended which provides parts speech of sentence
* For posterior probability added all the invidual posterior probabilities sigma Si

#### HMM:
Figure:1a:
* Used Viterbi algorithm to calculate the parts of speech
* Did backtracking to get all maximum values to obtain parts of speech
* Posterior probability=p(s1)p(s1/w1)p(s2/s1)p(s2/w2)....

#### Gibbs Sampling:
Figure 1c:
* Took random parts of speech and produced 1000 samples, burnout iterations are also included in 1000 interations.
* The values in gibbs will be eventually converges into a definite solution.
* The values are calculated using:
    P(s2)=p(s2/s1)p(s3/s2)p(w2/s1,s2)p(w3/s1,s3)
    p(s1)=p(s1)p(s2/s1)p(s1/w1)  (only for start state)
    p(sn)=p(sn/sn-1)p(wn/sn-1,sn) (only for last state)
* posteror probability of gibbs id calculated by =p(s)p(w1/s1)p(s2/s1)p(w2/s2,s1)p(s3/s2)p(w3/s2,s3)...
* Output image is in part1 repository

* calculated values for simple,hmms and gibbs
    * gibbs value are different from simple and hmm because of different transition probabilities p(w2/s1,s2) are small, so the value varied


## Part2
### Mountain Finding

* P(e/s)=emmission probability= edge strength/max edge strenth in that columm

#### For Bayes net in figure 1a:

* Take the row with max emmision probability in that particular and draw a red line
* P(e/s) is emission probability and p(s) is same for all rows. So take row with max(p(e/s)) for red line

#### For Figure 1b without human points:

* Used veterbi algorithm to get points of blue line
* transition probability is Gaussian Distribution  = (exp(-(x-mu)**2))/(sigma ** 2). After taking log value becomes -((x-mu) ** 2)/(sigma ** 2), sigma is considered as 10. for better values

#### For Figure 1b with human points:

* Calculated in couple of different ways:
    * 1st method:- simple use above veterbi algorithm and change the emission probability of the that point to maximum(0.99999999) and rest of the points in that column to minimum 0.00000001
    * 2nd method:- Now we now the edge probability of mountain so I calculated relative edge probability of all other points and used this as the emission probability and also change the emission probability of the that point to maximum(0.99999999) and rest of the points in that column to minimum 0.00000001. By use veterbi algorithm found the green line

* In method2, the relative emission probality is calculated by 1-((abs(emission probability-known point emission probability))/1000) here we take 1000, it may vary by input or it will cause problem while calculation log if given value is negetive. This value 1-((abs(emission probability-known point emission probability))/1000) should always be positive. (works fine with given inputs).
* Method 2 is working pretty well than method1
* Images for all 10 outputs are in part2 repository
**Please ignore green line if you are not giving human points**



## Part3
###  Reading text
* Emission probability:- probabilty of how similar the train letter is equal to tests letter
    * This is calculated by if corresponding pixels are equal multiply probability by 0.9 or multiply by lower probability 0.1
    * faced few scaling problems when considered 1-(abs(noise)/total pixels) as probability here noise=(equal pixels-unequal pixels)

* Calculated transition probability using part1 training data.

* Simple method is calculated max of prboilility(Oi/li) probability(li) for each letter, that how we get the simple output.
* For HMM
    * Used veterbi algorithm to find the letters
    * Problems faced:- As there are somany spaces, the probaility of letter space is nore than all other letters. The transition probability of letter after space or before space is more. So transition probability is domibnating emission probability and because of the noise the test letter are tend to be space in training(more emission probability for space). We are ending up getting more spaces for few outputs
    * Further Improved my using effective emission by using different probability for *s and spaces






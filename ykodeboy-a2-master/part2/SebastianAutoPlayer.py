# Automatic Sebastian game player
# B551 Fall 2020
# PUT YOUR NAME AND USER ID HERE!
#
# Based on skeleton code by D. Crandall
#
#
# This is the file you should modify to create your new smart player.
# The main program calls this program three times for each turn. 
#   1. First it calls first_roll, passing in a Dice object which records the
#      result of the first roll (state of 5 dice) and current Scorecard.
#      You should implement this method so that it returns a (0-based) list 
#      of dice indices that should be re-rolled.
#   
#   2. It then re-rolls the specified dice, and calls second_roll, with
#      the new state of the dice and scorecard. This method should also return
#      a list of dice indices that should be re-rolled.
#
#   3. Finally it calls third_roll, with the final state of the dice.
#      This function should return the name of a scorecard category that 
#      this roll should be recorded under. The names of the scorecard entries
#      are given in Scorecard.Categories.
#

from SebastianState import Dice
from SebastianState import Scorecard
import random

class SebastianAutoPlayer:

      def __init__(self):
            self.special_cats={"company","prattle","squadron","triplex","quadrupla","quintuplicatam"}
            pass  

      def sum_bonus(self,scorecard):
            num=list(Scorecard.Numbers.keys())
            bonus=0
            for i in scorecard.scorecard.keys():
                  if i in num:
                        bonus=bonus+scorecard.scorecard[i]
            return bonus
      def get_category_scores(self,dice,categories,scorecard):
            d={}
            counts = [dice.count(i) for i in range(1,7)]
            for category in categories:
                  if category in Scorecard.Numbers:
                        d[category] = counts[Scorecard.Numbers[category]-1] * Scorecard.Numbers[category]
                        # check for bonus- no bonus add 35
                        if self.sum_bonus(scorecard)<63:
                              if counts[Scorecard.Numbers[category]-1] >=3:
                                    # d[category]=d[category]+(1.8*counts[Scorecard.Numbers[category]-1])
                                    d[category]=d[category]+35

                  elif category == "company":
                        d[category]= 40 if sorted(dice) == [1,2,3,4,5] or sorted(dice) == [2,3,4,5,6] else 0
                  elif category == "prattle":
                        d[category] = 30 if (len(set([1,2,3,4]) - set(dice)) == 0 or len(set([2,3,4,5]) - set(dice)) == 0 or len(set([3,4,5,6]) - set(dice)) == 0) else 0
                  elif category == "squadron":
                        d[category] = 25 if (2 in counts) and (3 in counts) else 0
                  elif category == "triplex":
                        d[category] = sum(dice) if max(counts) >= 3 else 0
                  elif category == "quadrupla":
                        d[category] = sum(dice) if max(counts) >= 4 else 0
                  elif category == "quintuplicatam":
                        d[category] = 50 if max(counts) == 5 else 0
                  elif category == "pandemonium":
                        d[category] = sum(dice)
            return d
      
      

      def get_probability(self,Categories,dice):
            d={}
            rdp={}
            counts = [dice.count(i) for i in range(1,7)]
            for category in Categories:
                  if category in Scorecard.Numbers:
                        if counts[Scorecard.Numbers[category]-1]==0:
                              d[category]= 4651/(6**5)
                        elif counts[Scorecard.Numbers[category]-1]==1:
                              d[category]=3125/(6**5)
                        elif counts[Scorecard.Numbers[category]-1]==2:
                              d[category]=1250/(6**5)
                        elif counts[Scorecard.Numbers[category]-1]==3:
                              d[category]=250/(6**5)
                        elif counts[Scorecard.Numbers[category]-1]==4:
                              d[category]=25/(6**5)
                        elif counts[Scorecard.Numbers[category]-1]==5:
                              d[category]=1/(6**5)
                        # elif counts[Scorecard.Numbers[category]-1]==6:
                        # 276/6**4

                        # d[category] = counts[Scorecard.Numbers[category]-1] * Scorecard.Numbers[category]
                  elif category == "company":
                        d[category]= 40/(6**4)
                  elif category == "prattle":
                        d[category] = 45/(6**4)
                  elif category == "squadron":
                        d[category] = 50/(6**4)
                  elif category == "triplex":
                        d[category] = 100/(6**4)
                  elif category == "quadrupla":
                        d[category] = 25/(6**4)
                  elif category == "quintuplicatam":
                        d[category] = 1/(6**4)
                  elif category == "pandemonium":
                        d[category] = 1
            return d
      


      def score_calculated_max(self,outcome,scorecard):
            categories=list(set(Scorecard.Categories) - set(scorecard.scorecard.keys()))

            # d=self.get_category_scores(outcome,categories)
            # for i in scorecard.scorecard.keys():
            #       del d[i]
            # l=sorted(d,key=lambda k:d[k])
            # while len(d)>0:
            #       max_value=max(d.items(), key = lambda k : k[1])
            #       max_cats=[k for k,v in d.items() if v == max_value[1]
            #       for item in max_cats:
            max_value=max(d.items(), key = lambda k : k[1])
            return max_value
      def select_category(self,p,max_value,scorecard,dice):
            counts = [dice.count(i) for i in range(1,7)]
            l=sorted(p,key=lambda k:p[k])
            max_cat=None
            for category in l:
                  if category in Scorecard.Numbers:
                        if self.sum_bonus(scorecard) < 63:
                              if counts[Scorecard.Numbers[category]-1]>=3:
                                    max_cat=(category,max_value)
                                    break
                        else:
                              max_cat=(category,max_value)
                              break
                  elif category == "company" and max_value!=0:
                        max_cat=(category,max_value)
                        break
                  elif category == "prattle" and max_value!=0:
                        max_cat=(category,max_value)
                        break
                  elif category == "squadron" and max_value!=0:
                        max_cat=(category,max_value)
                        break
                  elif category == "triplex" and max_value!=0:
                        max_cat=(category,max_value)
                        break
                  elif category == "quadrupla" and max_value!=0:
                        max_cat=(category,max_value)
                        break
                  elif category == "quintuplicatam" and max_value!=0:
                        max_cat=(category,max_value)
                        break
                  elif category == "pandemonium":
                        if len(scorecard.scorecard)==12 or max_value >17.5:
                              max_cat=(category,max_value)
                              break
            # if not self.bonusflag and len(set(Scorecard.Numbers.keys()) - set(self.scorecard.keys())) == 0:
            # self.bonusscore = 35 if sum([ self.scorecard[i] for i in Scorecard.Numbers ]) >= 63 else 0
            # self.bonusflag = True
            # self.totalscore += self.bonusscore
            return max_cat

      # def get_bonus_flags(scorecard):
      #       if not bonusflag and len(set(Scorecard.Numbers.keys()) - set(scorecard.scorecard.keys())) == 0:
      #       self.bonusscore = 35 if sum([ self.scorecard[i] for i in Scorecard.Numbers ]) >= 63 else 0
      #       self.bonusflag = True
      def max_value_cats(self):
            d={}
            for category in Scorecard.Categories:
                  if category == "company":
                        d[category]=40
                  elif category == "prattle":
                        d[category]=30
                  elif category == "squadron":
                        d[category]=25
                  elif category == "triplex":
                        d[category]=36
                  elif category == "quadrupla":
                        d[category]=36
                  elif category == "quintuplicatam":
                        d[category]=50
            return d
      def cal_quit(self,scorecard):
            l=[]
            d=self.max_value_cats()
            for item in scorecard.scorecard.keys():
                  if  item in self.special_cats and scorecard.scorecard[item] == 0:
                        l.append(item)
            s=0
            for  i in l:
                  s=s+d[i]
            left_categories=list(set(self.special_cats) - set(scorecard.scorecard.keys()))
            if (len(left_categories)!=0):
                  min_value=100
                  min_cat=None
                  for cat in left_categories:
                        if min_value>d[cat]:
                              min_value=d[cat]
                              min_cat=cat
                  if(s+d[min_cat]>98):
                        return False
                  return True
            return False
            


      def score_calculated(self,outcome,scorecard):
            categories=list(set(Scorecard.Categories) - set(scorecard.scorecard.keys()))
            
            # bonus=get_bonus_flags(scorecard)
            d=self.get_category_scores(outcome,categories,scorecard)
            m=None
            d_new=d.copy()
            # for i in scorecard.scorecard.keys():
            #       del d[i]
            # l=sorted(d,key=lambda k:d[k])
            while len(d)>0:
                  max_value=max(d.items(), key = lambda k : k[1])
                  max_cats=[k for k,v in d.items() if v == max_value[1]]
                  for k in max_cats:
                        del d[k]
                  p=self.get_probability(max_cats,outcome)
                  m=self.select_category(p,max_value[1],scorecard,outcome)
                  if(m!=None):
                        break
            if m == None:
                  if(self.cal_quit(scorecard)):
                        p=self.get_probability(categories,outcome) 
                        min_p=min(p.items(), key = lambda k : k[1]) 
                        m=(min_p[0],d_new[min_p[0]])
                  else:
                        quit_cats=set(categories)-set(self.special_cats)
                        if "pandemonium" in quit_cats:
                              m=("pandemonium",d_new["pandemonium"])
                        elif len(quit_cats)!=0:
                              # min_cats=[k for k,v in p.items() if v == min_p[1]]
                              # if len(min_cats) > 1:
                              min_n=min(quit_cats,key = lambda k: scorecard.Numbers[k])
                              m=(min_n,d_new[min_n])
                        else:
                              p=self.get_probability(categories,outcome) 
                              min_p=min(p.items(), key = lambda k : k[1]) 
                              m=(min_p[0],d_new[min_p[0]])      
            return m


                  
            




      # def expected_value_category():
      def expected_value(self,roll,reroll,scorecard):
            exp=0
            outcome_count=0
            for outcome_1 in ((roll[0],) if not reroll[0] else range(1,7)):
                  for outcome_2 in ((roll[1],) if not reroll[1] else range(1,7)):
                        for outcome_3 in ((roll[2],) if not reroll[2] else range(1,7)):
                              for outcome_4 in ((roll[3],) if not reroll[3] else range(1,7)):
                                    for outcome_5 in ((roll[4],) if not reroll[4] else range(1,7)):
                                          outcome_count=outcome_count+1
                                          exp=exp+self.score_calculated([outcome_1,outcome_2,outcome_3,outcome_4,outcome_5],scorecard)[1]
            return exp/outcome_count



 


      def first_roll(self, dice, scorecard):
            l=[]
            max_value=(0,0)
            possible_rolls=[(roll_1,roll_2,roll_3,roll_4,roll_5) for roll_1 in (True,False) for roll_2 in (True,False)  for roll_3 in (True,False) for roll_4 in (True,False) for roll_5 in (True,False)]
            for item in possible_rolls:
                  expec_value=self.expected_value(dice.dice,item,scorecard)
                  if(expec_value > max_value[0]):
                        max_value =(expec_value,item)
            for i in range(0,len(max_value[1])):
                  if max_value[1][i]==True:
                        l.append(i)
            return l


      def second_roll(self, dice, scorecard):
            l=[]
            max_value=(0,0)
            possible_rolls=[(roll_1,roll_2,roll_3,roll_4,roll_5) for roll_1 in (True,False) for roll_2 in (True,False)  for roll_3 in (True,False) for roll_4 in (True,False) for roll_5 in (True,False)]
            for item in possible_rolls:
                  expec_value=self.expected_value(dice.dice,item,scorecard)
                  if(expec_value > max_value[0]):
                        max_value =(expec_value,item)
            for i in range(0,len(max_value[1])):
                  if max_value[1][i]==True:
                        l.append(i)
            return l
            # return [1, 2] # always re-roll second and third dice (blindly)
      
      def third_roll(self, dice, scorecard):
            max=self.score_calculated(dice.dice,scorecard)
            # scorecard.record(max[0],dice)
            return max[0]

# k=SebastianAutoPlayer()

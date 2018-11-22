# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 16:27:25 2018

@author: Cody Torgerson
"""
#First import all relevent libraries#
import pandas as pd
import numpy as np
import statsmodels.api as sm


#Read in beer review data from 'beer_review.csv' as a pandas dataframe#
data = pd.read_csv('beer_reviews.csv')
#remove rows with null values if any exsist.  This removes incomplete reviews from the dataset.#
data.dropna(axis=0)
#The data set contains no unique columns so an artifical index can be added to improve computaitonal speed#
data['new_index'] = range(0, len(data))
data.set_index('new_index',inplace=True)



#Change pandas dataframe formatting options to show all 12 columns of data present in the file 'beer_review.csv'#
pd.set_option('display.max_columns',12)


def basic_column_stats(data):
    
#use pandas describe function to observe some basic stastics for each column #
#which contain data that can be numerically parsed 
    
    bstat = data.describe()
    return bstat

####START QUESTION 1#####
   #Prompt:Which brewery produces the strongest beers by ABV%?#
   
#To find which brewery makes the strongest beer                                     #
#the average abv of all unique beers form a brewery will be calculated and displayed#  
   
#create a new data frame containg the information need to determine which brewery produces the strongest beer#

top_abv = data[["brewery_name","beer_name","beer_abv"]]
#use drop duplicate function to ensure beers are not counted more than once#
top_abv.drop_duplicates(['beer_name','brewery_name'],keep='first')

#Use Pivot Table function to create a data set which containts the average abv of all unique beers produced by each brewery
pt1 = top_abv.pivot_table(values=["beer_abv"], index=["brewery_name"],aggfunc=np.mean)
pt1 = pt1.sort_values(['beer_abv'],ascending=[True])
print(pt1.tail(1))

####ANSWER QUESTION 1: the last row of the pivot table shows Schorschbräu produces the strongest beers #####

####END QUESTION 1####


####START QUESTION 2:####

###Prompt If you had to pick 3 beers to recommend using only this data, which would you pick? 

##Answer will be found by taking the weighted average of each beers overall score.
## The beers with the top 3 weighted averages will be my recomendation

q2 = data[['beer_name','review_overall']]
q2.set_index('beer_name')
q2f = q2.groupby('beer_name').beer_name.count()
q2s = q2.groupby('beer_name').review_overall.sum()
q2 = pd.DataFrame(data=dict(_count=q2f, _sum=q2s))
trs = q2._count.sum()
q2['weighted_average'] = (q2['_sum']) / trs
pt2 = q2.pivot_table(values=['weighted_average'], index=['beer_name'])
pt2 = pt2.sort_values(['weighted_average'], ascending= [True])
print(pt2.tail(3))

###ANSWER QUESTION 2###
#the last 3 rows of the pivot table show my recommendations.
#Below is a list sorted by rank of which beers people think are the best to drink
#1st: 90 Minute IPA
#2nd: Old Rasputin Russian Imperial Stout
#3rd: Sierra Nevada Celebration Ale

####END QUESTION 2####

####START QUESTION 3####

###Which of the factors (aroma, taste, appearance, palette) are most important in determining the overall quality of a beer?

##A Function will be called to perform multivariate linear regression for question 3
def Multivariate_Linear_Regression():


##to determine if variables review_aroma,review_appearance,review_palate,review_taste
##are stastitically significantly variables in the review_overall score.
##This result will also show how much each variable, if at all, influences the review_overall score

#Load user inputs into Variable X.  This Array of variables will be used as the independ variables in the regression.
    X = data[["review_aroma","review_appearance","review_palate","review_taste"]]
    
#load output review_overall into variable Y. This 1d array will be used as the dependent variable in the regression
    Y = data['review_overall']
    
#use Statsmodels ols and fit function to fit the data to a linear regression model
## h0:  There will be no significant prediction of review_overall score by variables review_aroma,review_appearance,review_palate,review_taste
## h1:  Varaibles variables review_aroma,review_appearance,review_palate,review_taste may significantly influence review_overall score
    model = sm.OLS(Y, X).fit()
    
#Outputs the results of the OLS regression model
    model_summary= model.summary()
  ###ANSWER QUESTION 3###
## The output of the model shows all inputs significantly influence the overall score
## the coef output of the table is the mean change to the output variable by changing the input variable by 1 unit
## This means variables review_taste and review_palate have the highest weight on the overall perceived quality of the beer
## This insight shows that aroma and appearnce are significant factors to the overall quality of the beer, but not the most important.
    return model_summary

print(Multivariate_Linear_Regression())

####END QUESTION 3####


####START QUESTION 4####

###Promt: Lastly, if I typically enjoy a beer due to its aroma and appearance, which beer style should I try? 

## The beers with the top 3 culmultative weighted averages will be my recomendation
q4 = data[['beer_name','review_aroma','review_appearance']]
q4.set_index('beer_name')
q4f = q4.groupby('beer_name').beer_name.count()
q4ap = q4.groupby('beer_name').review_appearance.sum()
q4ar = q4.groupby('beer_name').review_aroma.sum()
q4 = pd.DataFrame(data=dict(_count=q4f, _sumap=q4ap,_sumar=q4ar))
trs = q4._count.sum()
w1 = q4ar / (q4ap + q4ar)
w2 = q4ap / (q4ap + q4ar)
q4['weighted_average'] = (q4['_sumar']*w1 + q4['_sumap']*w2)/trs
pt4 = q4.pivot_table(values=['weighted_average'], index=['beer_name'])
pt4 = pt4.sort_values(['weighted_average'], ascending= [True])
print(pt4.tail(3))

    ###ANSWER QUESTION 4####
#the last 3 rows of the pivot table show my recommendations.
#Below is a list sorted by rank of which beers people think are the best to drink
#1st: 90 Minute IPA
#2nd: Old Rasputin Russian Imperial Stout
#3rd: Sierra Nevada Celebration Ale 

####END QUESTION 4####

#####END CHALLENGE#####

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 01:57:26 2020

@author: Deep Patel 

Characteristics of patients affecting the BMI and Insurance Expenses 

Descriptive Statistical Analysis with Data Aggregation and 
using numpy and pandas libraries 

"""

import numpy as np
import pandas as pd

arr=np.loadtxt('insurance.txt', dtype={'names':('age','sex','bmi','children',
                                                'smoker','region','expenses'),
                                       'formats':[np.float,'S100',np.float,
                                                  np.float,'S100','S100',
                                                  np.float]},skiprows=1)
# Mean, standard deviation and median of age
age_mean= np.mean(arr['age'])
age_std= np.std(arr['age'])
age_median= np.median(arr['age'])

a1 = 'Basic analysis of AGE'
a2 = "The mean age is " + format(age_mean,'.2f') + '\n' \
      "The median age is " + format(age_median,'.2f') + '\n' \
      "The standard deviation of age is " + format(age_std,'.2f') + '\n'

a3 = "---------------------------------------------------------------------\n"

# Mean, standard deviation and median of BMI
BMI_mean= np.mean(arr['bmi'])
BMI_std= np.std(arr['bmi'])
BMI_median= np.median(arr['bmi'])

a4 = 'Basic analysis of BMI'
a5 = "The mean BMI is " + format(BMI_mean,'.2f') + '\n' \
      "The median BMI is " + format(BMI_median,'.2f') + '\n' \
      "The standard deviation of BMI is " + format(BMI_std,'.2f') + '\n'

a6 = "---------------------------------------------------------------------\n"

# Converting array to dataframe for ease in filtering

df=pd.DataFrame(arr)
df['smoker']=df['smoker'].str.decode('utf-8')
df['region']=df['region'].str.decode('utf-8')
df['sex']=df['sex'].str.decode('utf-8')

# Mean, standard deviation and median of BMI grouped by sex
a7 = "The mean, median and standard deviation of BMI for sex " \
    "is as follows: \n"
Sex_Groupby= df.groupby(['sex']).agg({'bmi':['mean','median','std']}).round(2)
a8= Sex_Groupby.to_string() + '\n'

a9= "----------------------------------------------------------------------\n"

# Mean, standard deviation and median of BMI for smokers and non-smokers

Smoke_yes= df[(df['smoker']=='yes')]
Smoke_no= df[(df['smoker']=='no')]

a10="The mean, median and standard deviation of BMI of smokers is " \
      "as follows: \n"
ysmoke= Smoke_yes.agg({'bmi':['mean','median','std']}).round(2)
a11= ysmoke.to_string() + '\n'

a12="The mean, median and standard deviation of BMI of non-smokers is " \
      "as follows: \n"
nsmoke= Smoke_no.agg({'bmi':['mean','median','std']}).round(2)
a13= nsmoke.to_string() + '\n'

#Groupby
#df.groupby(['smoker']).agg({'bmi':['mean','median','std']})
a14= "---------------------------------------------------------------------\n"

# Mean, standard deviation and median of BMI grouped by region
a15= "The mean, median and standard deviation of BMI by region is " \
      "as follows: \n"
Region_Groupby= df.groupby(['region']).agg({'bmi':['mean',
                                                   'median','std']}).round(2)
a16= Region_Groupby.to_string() + '\n'

a17= "---------------------------------------------------------------------\n"

# Mean, standard deviation and median of BMI of those w/ more than 2 childrens
two_children= df[(df['children']>2)]
a18= "The mean, median and standard deviation of BMI of those who have " \
      "more than two children is as follows: \n"
two_child= two_children.agg({'bmi':['mean','median','std']}).round(2)
a19= two_child.to_string() + '\n'

a20="----------------------------------------------------------------------\n"

#Sorting by expenses (highest to lowest) in new dataframe
exp= df.sort_values(['expenses'], ascending=False)

exp_top20= exp.head(int(len(exp)*0.20))
exp_bottom80= exp.tail(int(len(exp)*0.80))

# Calculations for cases in top 20% of expenses. 
a21= "The mean, median and standard deviation of BMI for the top 20% " \
      "of the expenses as follows: \n"
expt20= exp_top20.agg({'bmi':['mean','median','std']}).round(2)
expt20_mode=exp_top20.agg({'smoker':['mode'],'region':['mode']})
a22= expt20.to_string() +  '\n'
a23= expt20_mode.to_string() +'\n'

a24= "--------------------------------------------------------------------\n"

# Calculations for cases in bottom 80% of expenses.
a25= "The mean, median and standard deviation of BMI for the rest 80% " \
      "of the expenses as follows: \n"
expb80= exp_bottom80.agg({'bmi':['mean','median','std']}).round(2)
expb80_mode=exp_bottom80.agg({'smoker':['mode'],'region':['mode']})
a26= expb80.to_string() + '\n'
a27= expb80_mode.to_string() + '\n'

# Storing the results as a single variable
results=(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,
          a20,a21,a22,a23,a24,a25,a26,a27)

# Creating a new file
results_file = open('results.txt', 'w')

# Writing the results variable to the file.  Then closing the file.
with open('results.txt','a') as file:
    for line in results:
        results_file.write(str(line))
        results_file.write("\n")
results_file.close()


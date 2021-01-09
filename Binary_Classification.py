# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 09:23:37 2020

Binary Classification with OneR Classification Algorithm

Authors: Deep Patel and Kenneth Hora
"""

# Imports the necessary libraries
import pandas as pd
#import numpy as np
import os

os.chdir("C:\\Users\\deepp\\Google Drive")

# Reads the training and test files
training = pd.read_excel('titanic_traning.xlsx')
test = pd.read_excel('titanic_test.xlsx')

# Making the index of the test dataframe the same as the ID number
start_test_index = test["ID"][0]
end_test_index = test["ID"][len(test["ID"])-1]
test_index_list = list(range(start_test_index, (end_test_index+1)))
test.index = test_index_list

# Machine learning for gender
female_survive = 0
female_dead = 0
male_survive = 0
male_dead = 0

# Counts the number of survivors among the genders
for i in range(len(training["ID"])):
    if training["gender"][i] == 'female' and training["survived"][i] == 1:
        female_survive += 1
    elif training["gender"][i] == 'female' and training["survived"][i] == 0:
        female_dead += 1
    elif training["gender"][i] == 'male' and training["survived"][i] == 1:
        male_survive += 1
    elif training["gender"][i] == 'male' and training["survived"][i] == 0:
        male_dead += 1

# Determines the gender votes
if (female_survive)/(female_survive + female_dead) > .5:
    female_vote = 1
else:
    female_vote = -1

if (male_survive)/(male_survive + male_dead) > .5:
    male_vote = 1
else:
    male_vote = -1

# Machine learning for pclass
# Initilized the plcass vote variables
class1_vote = 0
class2_vote = 0
class3_vote = 0

# Counts the difference between survivors and casualties among the pclass 
# feature. 
for i in range(len(training["ID"])):
    if training["pclass"][i] == 1 and training["survived"][i] == 1:
        class1_vote += 1
    elif training["pclass"][i] == 1 and training["survived"][i] == 0:
        class1_vote -= 1
    elif training["pclass"][i] == 2 and training["survived"][i] == 1:
        class2_vote += 1
    elif training["pclass"][i] == 2 and training["survived"][i] == 0:
        class2_vote -= 1
    elif training["pclass"][i] == 3 and training["survived"][i] == 1:
        class3_vote += 1
    elif training["pclass"][i] == 3 and training["survived"][i] == 0:
        class3_vote -= 1

# Determines the pclass votes
if class1_vote > 0:
    class1_vote = 1
elif class1_vote < 0:
    class1_vote = -1
else:
    class1_vote = 0
if class2_vote > 0:
    class2_vote = 1
elif class2_vote < 0:
    class2_vote = -1
else:
    class2_vote = 0
if class3_vote > 0:
    class3_vote = 1
elif class3_vote < 0:
    class3_vote = -1
else:
    class3_vote = 0

# Machine learning for parch
# Determines the max value in the parch feature
max_parch = max(training["parch"])

# Initilizes a list for parch votes
parch_votes = list(range(0,(max_parch +1)))

# Counts the difference between survivors and casualties among the parch 
# feature. 
for i in range(len(training["ID"])):
    val = training["parch"][i]
    if training["survived"][i] == 1:
        parch_votes[val] += 1
    elif training["survived"][i] == 0:
        parch_votes[val] -= 1

# Machine learning for sibsp
# Determines the max value for the sibsp feature
max_sibsp = max(training["sibsp"])

# Initilizes a list for sibsp votes
sibsp_votes = list(range(0,(max_sibsp +1)))

# Counts the difference between survivors and casualties among the sibsp 
# feature. 
for i in range(len(training["ID"])):
    val = training["sibsp"][i]
    if training["survived"][i] == 1:
        sibsp_votes[val] += 1
    elif training["survived"][i] == 0:
        sibsp_votes[val] -= 1

# Machine learning for embarked status
# Initilizes a list for embarked votes
embarked_votes = pd.Series([0,0,0], index = ('C', 'Q', 'S'))

# Counts the difference between survivors and casualties among the embarked 
# feature.
for i in range(len(training["ID"])):
    val = training["embarked"][i]
    if training["survived"][i] == 1:
        embarked_votes[val] += 1
    elif training["survived"][i] == 0:
        embarked_votes[val] -= 1

# Making prediction for gender
gender_prediction = pd.Series(test_index_list, index = test_index_list)

for i in test["ID"]:
    if test["gender"][i] == 'female':
        gender_prediction[i] = female_vote
    elif test["gender"][i] == 'male':
        gender_prediction[i] = male_vote
    else:
        gender_prediction[i] = 0


# Making prediction for pclass
pclass_prediction = pd.Series(test_index_list, index = test_index_list)

for i in test["ID"]:
    if test["pclass"][i] == 1:
        pclass_prediction[i] = class1_vote
    elif test["pclass"][i] == 2:
        pclass_prediction[i] = class2_vote
    elif test["pclass"][i] == 3:
        pclass_prediction[i] = class3_vote
    else:
        pclass_prediction[i] = 0

# Making prediction for parch
parch_prediction = pd.Series(test_index_list, index = test_index_list)
for i in test["ID"]:
    if test["parch"][i] > 0:
        parch_prediction[i] = 1
    elif test["parch"][i] == 0:
        parch_prediction[i] = -1
    else:
        parch_prediction[i] = 0


# Making prediction for sibsp
# sibsp values of 5 do not get a vote in either direction because the value
# of sib_votes[5] is 0 and most values below it are negative and most values
# above it are positive.  
sibsp_prediction = pd.Series(test_index_list, index = test_index_list)
for i in test["ID"]:
    if test["sibsp"][i] == 1 or test["sibsp"][i] > 5:
        sibsp_prediction[i] = 1
    elif test["sibsp"][i] < 5:
        sibsp_prediction[i] = -1
    else:
        sibsp_prediction[i] = 0

# Making prediction for embark
embarked_prediction = pd.Series(test_index_list, index = test_index_list)
for i in test["ID"]:
    if test["embarked"][i] == 'C':
        embarked_prediction[i] = 1
    elif test["embarked"][i] == 'Q' or test["embarked"][i] == 'S':
        embarked_prediction[i] = -1
    else:
        embarked_prediction[i] = 0

# Making final prediction based on 5 features
final_prediction = pd.Series(test_index_list, index = test_index_list)
for i in test["ID"]:
    if gender_prediction[i] + pclass_prediction[i] + parch_prediction[i] \
        + sibsp_prediction[i] + embarked_prediction[i] > 0:
            final_prediction[i] = 1
    else:
        final_prediction[i] = 0

# Reads the feature based prediction sheets
gender_pred = pd.read_excel('titanic_test_predictions.xlsx', \
                    sheet_name = 'Gender_Based_Prediction')
pclass_pred = pd.read_excel('titanic_test_predictions.xlsx', \
                    sheet_name = 'pclass_Based_Prediction')
parch_pred = pd.read_excel('titanic_test_predictions.xlsx', \
                    sheet_name = 'parch_Based_Prediction')
sibsp_pred = pd.read_excel('titanic_test_predictions.xlsx', \
                    sheet_name = 'sibsp_Based_Prediction')
embarked_pred = pd.read_excel('titanic_test_predictions.xlsx', \
                    sheet_name = 'embarked_Based_Prediction')

# Makes the indices the same as the ID number
gender_pred.index = test_index_list
pclass_pred.index = test_index_list
parch_pred.index = test_index_list
sibsp_pred.index = test_index_list
embarked_pred.index = test_index_list

# Fills out the "Prediction" column in the feature based prediciton dataframes
gender_pred["Prediction"] = gender_prediction
pclass_pred["Prediction"] = pclass_prediction
parch_pred["Prediction"] = parch_prediction
sibsp_pred["Prediction"] = sibsp_prediction
embarked_pred["Prediction"] = embarked_prediction

# Corrects the value assignment in each "Prediction" column
for i in test_index_list:
    if gender_pred["Prediction"][i] == -1:
        gender_pred["Prediction"][i] = 0
    if pclass_pred["Prediction"][i] == -1:
        pclass_pred["Prediction"][i] = 0
    if parch_pred["Prediction"][i] == -1:
        parch_pred["Prediction"][i] = 0
    if sibsp_pred["Prediction"][i] == -1:
        sibsp_pred["Prediction"][i] = 0
    if embarked_pred["Prediction"][i] == -1:
        embarked_pred["Prediction"][i] = 0

# Initilizes the successful prediction count for each feature
gender_count = 0
pclass_count = 0
sibsp_count = 0
parch_count = 0
embarked_count = 0

# Counts the successful predictions for each features
for i in test["ID"]:
    if gender_pred["Prediction"][i] == gender_pred["Ground truth"][i]:
        gender_count += 1
    if pclass_pred["Prediction"][i] == pclass_pred["Ground truth"][i]:
        pclass_count += 1
    if parch_pred["Prediction"][i] == parch_pred["Ground truth"][i]:
        parch_count += 1
    if sibsp_pred["Prediction"][i] == sibsp_pred["Ground truth"][i]:
        sibsp_count += 1
    if embarked_pred["Prediction"][i] == embarked_pred["Ground truth"][i]:
        embarked_count += 1


# Calculates the success rate for each feature
gender_success = round(gender_count/len(test), 3)
pclass_success =  round(pclass_count/len(test), 3)
sibsp_success = round(sibsp_count/len(test), 3)
parch_success = round(parch_count/len(test), 3)
embarked_success = round(embarked_count/len(test), 3)


# Creates a data dictionary for success rate
data = {'Feature':  ['Gender_Based_Prediction', 'pclass_Based_Prediction', \
                     'sibsp_Based_Prediction', 'parch_Based_Prediction', \
                         'embarked_Based_Prediction'],
        'Success Rate': [gender_success, pclass_success, sibsp_success, \
                         parch_success, embarked_success]
        }
    
# Creates the dataframe for the success rate
success_rate = pd.DataFrame(data)


# Writes the data frames to the excel file
with pd.ExcelWriter('titanic_test_predictions_Team4.xlsx') as writer:
    gender_pred.to_excel(writer, sheet_name = 'gender_Based_Prediction', \
                         index = False)
    pclass_pred.to_excel(writer, sheet_name = "pclass_Based_Prediction", \
                         index = False)
    sibsp_pred.to_excel(writer, sheet_name = "sibsp_Based_Prediction", \
                        index = False)
    parch_pred.to_excel(writer, sheet_name = "parch_Based_Prediction", \
                        index = False)
    embarked_pred.to_excel(writer, sheet_name = "embarked_Based_Prediction", \
                           index = False)
    success_rate.to_excel(writer, sheet_name = "Prediction Success Rate", \
                          index = False)
        
    # Adjusts column widths within sheets
    workbook=writer.book
    worksheet1=writer.sheets['gender_Based_Prediction']
    worksheet1.set_column('B:C',12)
    worksheet2=writer.sheets['pclass_Based_Prediction']
    worksheet2.set_column('B:C',12)
    worksheet3=writer.sheets['sibsp_Based_Prediction']
    worksheet3.set_column('B:C',12)
    worksheet4=writer.sheets['parch_Based_Prediction']
    worksheet4.set_column('B:C',12)
    worksheet4=writer.sheets['embarked_Based_Prediction']
    worksheet4.set_column('B:C',12)
    worksheet5=writer.sheets['Prediction Success Rate']
    worksheet5.set_column('A:A',25)
    worksheet5.set_column('B:B',12)
      
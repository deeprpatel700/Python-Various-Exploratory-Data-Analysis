# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 09:36:57 2020

Authors: Deep Patel and Kenneth Hora
Determing Severity of Missing and Inconsistent Data
"""

# Imports the necessary libraries
import pandas as pd
#import numpy as np
import os

os.chdir("C:\\Users\\deepp\\Google Drive")
# Reads the file
training = pd.read_csv('titanic_traning.csv')

# Making the index of the test dataframe the same as the ID number
start_training_index = training["ID"][0]
end_training_index = training["ID"][len(training["ID"])-1]
training_index_list = list(range(start_training_index, 
                                 (end_training_index+1)))
training.index = training_index_list

n = len(training)

# Initilizes the table of missing/inconsistent values
MIV_table = pd.DataFrame()
MIV_table['Feature'] = training.columns[1:]
MIV_table['Missing Values (MV)'] = [0, 0, 0, 0, 0, 0, 0, 0]
MIV_table['% of MV (MV/n)'] = [0, 0, 0, 0, 0, 0, 0, 0]
MIV_table['Inconsistency Values (IV)'] = [0, 0, 0, 0, 0, 0, 0, 0]
MIV_table['% of IV (IV/n)'] = [0, 0, 0, 0, 0, 0, 0, 0]

# Making the index the same as the feature
MIV_table.index = training.columns[1:]

# Counts the missing values in each feature and calcualtes the % MV
for i in training.columns[1:]:
    MIV_table.loc[[i], 'Missing Values (MV)'] = \
        len(training[i][training[i].isnull()])
    MIV_table.loc[[i], '% of MV (MV/n)'] = \
        round(((MIV_table.loc[[i], 'Missing Values (MV)'])/n)*100, 3)

# Initilizes list of indeces of rows with MV or IV
MIV_index = []

# Counts the inconsistent values in each feature and tracks the indeces of IV
for i in training.index:
    if training['pclass'][i] not in [1, 2, 3]:
        MIV_table.loc[['pclass'], 'Inconsistency Values (IV)'] += 1
        if i not in MIV_index:
            MIV_index.append(i)

    if training['sex'][i] not in ['male', 'female']:
        MIV_table.loc[['sex'], 'Inconsistency Values (IV)'] += 1
        if i not in MIV_index:
            MIV_index.append(i)

    if training['embarked'][i] not in ['C', 'Q', 'S']:
        MIV_table.loc[['embarked'], 'Inconsistency Values (IV)'] += 1
        if i not in MIV_index:
            MIV_index.append(i)

    if training['sibsp'][i] not in list(range(0,12)):
        MIV_table.loc[['sibsp'], 'Inconsistency Values (IV)'] += 1
        if i not in MIV_index:
            MIV_index.append(i)

    if training['parch'][i] not in list(range(0,12)):
        MIV_table.loc[['parch'], 'Inconsistency Values (IV)'] += 1
        if i not in MIV_index:
            MIV_index.append(i)

    if training['survived'][i] not in [0, 1]:
        MIV_table.loc[['survived'], 'Inconsistency Values (IV)'] += 1
        if i not in MIV_index:
            MIV_index.append(i)

# Float values of age are treated as inconsistent.  They will be trunked later
    if training['age'][i] not in list(range(1,99)):
        MIV_table.loc[['age'], 'Inconsistency Values (IV)'] += 1
        if i not in MIV_index:
            MIV_index.append(i)

# The IV for age needs to be corrected by subtracting MV because the method 
# for finding IV in age counted both IV and MV.
MIV_table.loc[['age'], 'Inconsistency Values (IV)'] = \
    MIV_table.loc[['age'], 'Inconsistency Values (IV)'] - \
        len(training['age'][training['age'].isnull()])


import decimal
def drange(x, y, jump):
  while x < y:
    yield float(x)
    x += decimal.Decimal(jump)

# Float values greater than 1 decimal place of fare are treated as 
# inconsistent.
for i in training.index:
    if training['fare'][i] not in list(drange(0,550, 
                                              decimal.Decimal('0.1'))):
        MIV_table.loc[['fare'], 'Inconsistency Values (IV)'] += 1
        if i not in MIV_index:
            MIV_index.append(i)

# The IV for fare needs to be corrected by subtracting MV because the method 
# for finding IV in age counted both IV and MV.
MIV_table.loc[['fare'], 'Inconsistency Values (IV)'] = \
    MIV_table.loc[['fare'], 'Inconsistency Values (IV)'] - \
        len(training['fare'][training['fare'].isnull()])

# Calculates the % of IV for each feature
for i in training.columns[1:]:
    MIV_table.loc[[i], '% of IV (IV/n)'] = \
        round(((MIV_table.loc[[i], 'Inconsistency Values (IV)'])/n)*100,3)


# age has NAs and floats (.5) and floats less than zero.
# fare has zero, NA and missing values...
# embarked just has Queenstown spelled out
# nothing wrong in sibsp
# nothing wrong in parch
# nothing wrong in survived

# Creates a dataframe of the M/I values.
MIV_frame = training.loc[MIV_index, training.columns]

# Creates replacement values for M/I values
fare_mean = round(training['fare'].mean(), 2)
age_mean = int(round(training['age'].mean(), 0))
sibsp_mean = int(round(training['sibsp'].mean(), 0))
parch_mean = int(round(training['parch'].mean(), 0))
pclass_mode = training['pclass'].mode()[0]
sex_mode = training['sex'].mode()[0]
embarked_mode = training['embarked'].mode()[0]

# Replaces missing values
training['fare']=training['fare'].fillna(fare_mean)
training['age']=training['age'].fillna(age_mean)
training['sibsp']=training['sibsp'].fillna(sibsp_mean)
training['parch']=training['parch'].fillna(parch_mean)
training['pclass']=training['pclass'].fillna(pclass_mode)
training['sex']=training['sex'].fillna(sex_mode)
training['embarked']=training['embarked'].fillna(embarked_mode)

# Replace inconsistent values
for i in training.index:
    if training['sex'][i] == 'Male':
        training.at[i, 'sex'] = 'male'
    elif training['sex'][i] == 'Female':
        training.at[i, 'sex'] = 'female'

for i in training.index:
    if training['embarked'][i] == 'Queenstown':
        training.at[i, 'embarked'] = 'Q'

# Truncates float values in age
for i in training['age']:
    training['age'] = training['age']//1

# Writing the cleaned data to a .csv file
training.to_csv('cleaned_titanic.csv', index = False)

# Writes the MIV summary table and records of MIV to a .xlsx file
with pd.ExcelWriter('displays.xlsx') as writer:
    MIV_table.to_excel(writer, sheet_name = 'MIV_table', index = False)
    MIV_frame.to_excel(writer, sheet_name = 'MIV_frame', index = False)
        
    workbook=writer.book
    worksheet1=writer.sheets['MIV_table']
    worksheet1.set_column('B:E',21)
    worksheet2=writer.sheets['MIV_frame']
    worksheet2.set_column('H:I',11)
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 18:27:38 2020

@author: Deep Patel
Data Analysis of Adult Literacy (Various Data Queries)

"""

import pandas as pd
#import numpy as np
import os
from datetime import datetime
#from datetime import date


os.chdir("C:\\Users\\deepp\\Google Drive")


# Reading the excel file for each dataset
student = pd.read_excel('Student.xlsx')
tutor = pd.read_excel('Tutor.xlsx')
match_history = pd.read_excel('Match_History.xlsx')


# Question 1
# Filters Dataframe for Tutors with Dropped Status and specified date criteria
tutor_drop = tutor[(tutor['TutorStatus']=='Dropped') & 
                   (tutor['CertDate']>'2018-04-01')]
print("Q1: Tutors IDs of Tutors who have a Dropped status and have achieved "
      "their certification after 4/01/2018 are ", list(tutor_drop['TutorID']),
      "\n"*2)



# Question 2

# Replacing NA/missing End Dates with current date 
today= datetime.today().strftime('%Y-%m-%d')
match_history['EndDate'] = (match_history['EndDate'].fillna(today))
match_history['EndDate']=pd.to_datetime(match_history['EndDate'], 
                                        format= '%Y-%m-%d')

# Converting Start Date and End Date to datetime for arithmetic operations
match_history['EndDate']=pd.to_datetime(match_history['EndDate'])
match_history['StartDate']=pd.to_datetime(match_history['StartDate'])

# Creating new column to count number of days between start date and end date
match_history['Length']= (match_history['EndDate'] 
                          - match_history['StartDate']).dt.days

# Counts the average length of number of tutoting days
average_length= match_history['Length'].mean()
print ("Q2: The average length of time student stayed (or has stayed) in "\
       "the program is: ", average_length, "\n"*2)
                                          

    
    
# Question 3

# Merges two dataframes by column name
match_tutor = pd.merge(match_history,tutor, on="TutorID")

# Filters Dataframe with Temp Stop Status of Tutor and specified date criteria
student_match= match_tutor[(match_tutor['TutorStatus']=='Temp Stop') &
                           (match_tutor['StartDate']>='2018-01-01')]
# Creating new dataframe to see relevant columns
student_temp= student_match[['StudentID','StartDate','EndDate',
                             'TutorID','TutorStatus']]
print ("Q3: The query for students who have been matched in 2018 with a "
       "tutor whose status is Temp Stop. is as follows: \n", 
       student_temp, "\n")
print("The list of IDs of these students is ", 
      list(student_temp['StudentID']), "\n"*2)


    
# Question 4

# Mereges two dataframes by column name
score_join = pd.merge(match_tutor, student, on="StudentID")

# Filters Dataframe with Dropped status of Tutor 
score_match= score_join[(score_join['TutorStatus']=='Dropped')]

# Creating new dataframe to see relevant columns
score_status_dropped = score_match[['ReadScore','StudentID','TutorStatus']]

print ("Q4: The query for read scores of students who were ever taught by "\
       "tutors whose status is Dropped is as follows: \n", 
       score_status_dropped, "\n")
print("The list of Read Scores for these students is: ", 
      list(score_status_dropped['ReadScore']), "\n"*2)


# Question 5

# Filters dataframe with repeated TutorIDs in TutorID column
tutor_2students = match_history[match_history.duplicated(subset=['TutorID'],
                                                         keep=False)]

print("Q5: The query for tutors who taught two or more students is displayed "
      "below: \n", tutor_2students, "\n")
print("The list of these tutors by thier tutor ID is: ",
      list(set(list(tutor_2students['TutorID']))), "\n"*2)


# Question 6

# Creating new dataframe to see relevant columns for the specified query
student_tutor = score_join[['StudentID', 'ReadScore', 
                            'TutorID', 'TutorStatus']]

print("Q6: List of all students, their read score, their tutors, and "
      "tutors status is shown below and the file data is stored in "
      ".xlsx file: \n", student_tutor, "\n"*2)

# Writes the information the .xslx file
student_tutor.to_excel('Student_Tutor.xlsx', index=False)


# Question 7

# Creating new dataframe to see relevant columns for the specified query
group_filter= score_join[['StudentGroup','TutorID']]

# Tallies Tutors across different Student Groups
tutors_tally= pd.crosstab(group_filter['StudentGroup'],
                          group_filter['TutorID'], margins=True)

# Keeps only relevant columns and rows for the specified query
tally_filter = tutors_tally[['All']]
num_of_tutors= tally_filter[:-1]
number_of_tutors= num_of_tutors.rename(columns={'All':'Number of Tutors'})
number_of_tutors.columns.name=None

print("Q7: The number of tutors who have been matched with each Student "
      "Group is shown below: \n", number_of_tutors,"\n"*2 )


# Question 8

# Filters dataframe with for active students with specified date criteria
active= match_history[(match_history['StartDate']>='2018-05-01') &
                      (match_history['StartDate']<='2018-06-30') &
                      (match_history['EndDate']==today)]

# Creating new dataframe for active students with relevant columns
active_students= active[['StudentID','StartDate','EndDate']]
print("Q8: The query for all active students who started in May and June "
      "is shown below: \n", active_students,"\n")
print("The list of IDs of these active students is: ", 
      list(active_students['StudentID']), '\n'*2)


# Question 9

# Merges two dataframes by column name and keeping all values
student_tutor= pd.merge(student,match_history, on='StudentID', how='outer')

# Creating new dataframe with relevant columns for the query
student_tutor_filter= student_tutor[['StudentID','TutorID']]

# Filters students who has not been tutored yet
no_tutor= student_tutor_filter[(student_tutor_filter['TutorID'].isnull())]

print("Q9: The students IDs of students who has not been tutored yet are ", 
      list(no_tutor['StudentID']), "\n"*2)



# Question 10

# Merges two dataframes by column name and keeping all values
tutor_student=  pd.merge(tutor,match_history, on='TutorID', how='outer')

# Creating new dataframe with relevant columns for the query
tutor_student_filter= tutor_student[['TutorID','StudentID']]

# Filters tutors who has not tutored yet
no_students= tutor_student_filter[tutor_student_filter['StudentID'].isnull()]

print("Q10: The tutor IDs of tutors who did not tutor any students are ", 
      list(no_students['TutorID']), "\n"*2)










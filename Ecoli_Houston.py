# -*- coding: utf-8 -*-
"""
@author: Deep Patel

Chemical factors affecting the presence of E-coli bacteria in city’s waterways 

"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir("C:\\Users\\deepp\\Google Drive")

# Reading the excel file for Ecoli Data
ecoli= pd.read_excel('Ecoli Data.xlsx')

# Creating New Dataframe for Date and E.coli only
ecoli_date= ecoli[["Date Collected","E.coli"]]
Ecoli= ecoli_date.rename(columns={'Date Collected':'Date_Collected'})
Ecoli['Date_Collected']=pd.to_datetime(Ecoli['Date_Collected'])
Ecoli.dropna()  #drops missing values

# Average amount of E-coli per year in Houston
Ecoli_Year_Avg= Ecoli.groupby(
    [Ecoli.Date_Collected.dt.strftime('%Y')]
    )['E.coli'].mean().reset_index(name='Ecoli Yearly Average')
print(Ecoli_Year_Avg)

# Bar graph of E-coli amount by year
plot1= Ecoli_Year_Avg.set_index('Date_Collected')
plot1a= plot1.plot.bar()
plot1a.set_xlabel("Year")
plot1a.set_ylabel("E-coli Average Amount (#/100mL)")
plt.title("Amount of E.coli per year in Houston")
#plt.savefig('Ecoli_Year.jpg')  #To save graph in the current directory

print("---------------------------------------------------------------------")
Ecoli['Year']=Ecoli.Date_Collected.dt.year
Ecoli['Month']=Ecoli.Date_Collected.dt.strftime('%b')

Ecoli_Month_Avg= Ecoli.groupby(['Month','Year']
                               )['E.coli'].mean().reset_index(
                                   name='Ecoli Monthly Average')

# Creating list to match for sorting the data by months 
months=['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug', 
        'Sep','Oct', 'Nov','Dec']
Ecoli_Month_Avg['Month'] = pd.CategoricalIndex(Ecoli_Month_Avg['Month'],
                                               categories=months, ordered=True)

Ecoli_sort=Ecoli_Month_Avg.sort_values(["Month","Year"])

Ecoli_new= pd.pivot_table(Ecoli_sort, 
                          index=["Month","Year"],
                          values=["Ecoli Monthly Average"])

# Average amount of E-coli per month in Houston (grouped by year)
print(Ecoli_new)


# Bar graph of each month compared from 2013 to 2016
plot2= Ecoli_new.unstack().plot(kind='bar', width=0.8)
plot2.set_xlabel("Month")
plot2.set_ylabel("Ecoli Average Monthly Amount (#/100mL)")
plt.legend(labels=['2013','2014','2015','2016'],loc='upper left')
plt.title("Amount of E.coli per month in Houston over different years ")
# plt.savefig('Ecoli_Month_grouped.jpg') #To save graph in current directory



#----------------------------------------------------------------------------
# Creating new Dataframe for chemical factors and E.coli 
Ecoli_selected= ecoli[['E.coli','PH', 'Dissolved Oxygen','Phosphorous',
                      'Specific Conductance','Chloride', 'Ammonia Nitrogen',
                      'Nitrate Nitrogen','Sulfate']]

# checking the distribution of the features 
plt.figure()
f, axes= plt.subplots(3,3)
sns.distplot(Ecoli_selected['E.coli'],bins=10,color='k', ax=axes[0,0])
sns.distplot(Ecoli_selected['PH'],bins=10,color='k',ax=axes[0,1])
sns.distplot(Ecoli_selected['Dissolved Oxygen'],bins=10,
             color='k', ax=axes[0,2])
sns.distplot(Ecoli_selected['Phosphorous'],bins=10,color='k',ax=axes[1,0])
sns.distplot(Ecoli_selected['Specific Conductance'],bins=10,
             color='k',ax=axes[1,1])
sns.distplot(Ecoli_selected['Chloride'],bins=10,color='k',ax=axes[1,2])
sns.distplot(Ecoli_selected['Ammonia Nitrogen'],bins=10,color='k',ax=axes[2,0])
sns.distplot(Ecoli_selected['Nitrate Nitrogen'],bins=10,color='k',ax=axes[2,1])
sns.distplot(Ecoli_selected['Sulfate'],bins=10,color='k',ax=axes[2,2])
# plt.savefig('Distributions.jpg')


# From the distribution plots we can see that E.coli, Specific Conductance,
# Chloride, Ammonia nitrogen, Sulfate are concerntrated at one point and not
# distributed well. Therefore, performing data transformation may be good idea.


# Data transformation on selected features and omitting missing values
Ecoli_clean= np.log(Ecoli_selected).diff().dropna()  

corr= Ecoli_clean.corr(method="pearson")
#pd.set_option('display.max_columns',4)\
print("Correlation Matrix showing correlation between chemical factors "\
      "and Ecoli in first column or first row")
print(corr)   #prints correlation matrix

# Correlation Matrix heatmap using seaborn
plt.figure()
sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)
plt.title("Heatmap of Correlation Matrix")

# plt.savefig('Correlation_Matrix_Heatmap.jpg')

print("From correlation matrix and heatmap, we can see that the "\
      "correlation between Ecoli and chemical factors are weak. "\
      "The correlation between Ecoli and Specific condutance, between "\
      "Ecoli and Chloride, and between Ecoli and Sulfate are moderate "\
      "negative correlation wheareas correlation between Ecoli and "\
      "Phosporous, and Ecoli and Ammonia Nitrogen is weakest.\n")

#-----------------------------------------------------------------------------

# Extra plots to see the relationship between chemical factors & E.coli
print("Additional analysis: The regression plots and pairs plot are just "\
      "to further confirm the relationship patterns observed with "\
          "correlation values")
#-----------------------------------------------------------------------------

# Based on the correlations, specific features are selected and 
# Using regression plot to see the relationship

# Uncomment lines 143 to  162 to see the regression plots

# plt.figure()
# f, axes= plt.subplots(ncols=2)
# sns.regplot('PH','E.coli', data=Ecoli_clean, 
#             scatter_kws={'s':2},ax=axes[0])
# sns.regplot('Specific Conductance','E.coli', data=Ecoli_clean, 
#             scatter_kws={'s':2}, ax=axes[1])
# plt.title('Changes in log %s and log %s versus log %s' 
#           %('PH', 'Specific Conductance','E.coli'))
# #plt.savefig('Regplots1.jpg')


# plt.figure()
# f, axes= plt.subplots(ncols=2)
# sns.regplot('Chloride','E.coli', data=Ecoli_clean, 
#             scatter_kws={'s':2}, ax=axes[0])
# sns.regplot('Sulfate','E.coli', data=Ecoli_clean, 
#             scatter_kws={'s':2}, ax=axes[1])
# plt.title('Changes in log%s and log %s versus log %s' 
#           %('Chloride','Sulfate', 'E.coli'))
# #plt.savefig('Regplots2.jpg')


# Making new dataframe for pairs plot
Ecoli_select2= Ecoli_clean[['E.coli','PH', 
                            'Specific Conductance','Chloride','Sulfate']]
# Pairs plot (Scatterplot matrix of selected chemical factors & Ecoli)
sns.pairplot(Ecoli_select2,diag_kind='kde')
plt.title("Pairs plot")
#plt.savefig('PairsPlot.jpg')


# From the regression plots and pairs plot, we can see that there is 
# not sufficient evidence of relationship between Ecoli and selected features
# with chemical factors.





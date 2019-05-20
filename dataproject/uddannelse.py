#Uddannelse

import numpy as np
import pandas as pd
import pydst
import matplotlib.pyplot as plt

#DATACLEANING#

#We use pydst to use an API to Denmark's statistics
Dst = pydst.Dst(lang='en')
Dst.get_data(table_id='INDKP107')
Vars = Dst.get_variables(table_id='INDKP107')


All_data = Dst.get_data(table_id="INDKP107", variables={"OMRÅDE":['000','01','02','03','04','05','06','07','08','09','10','11'], "ENHED":["116"], "KOEN":["M", "K"], "UDDNIV":["*"], "TID":["*"], "INDKOMSTTYPE":["100"] }).rename(columns={'KOEN':'Gender','OMRÅDE':'Municipality', 'UDDNIV':'Edulvl', 'TID':'Year', 'INDHOLD':'disposable income'})

#test indexes 
municipalindex_all_data = All_data.set_index('Municipality')
edulvlindex_all_data = All_data.set_index('Edulvl')
yearindex_all_data = All_data.set_index('Year')

#Sort
Sortet_mun = municipalindex_all_data[['Year','Gender','Edulvl','disposable income']]
Sortet_edu = edulvlindex_all_data[['Municipality','Year','Gender','disposable income']]
Sortet_year = yearindex_all_data[['Municipality','Edulvl','Gender','disposable income']]


#Genderspecific 
Men = Sortet_year[Sortet_year['Gender']=='Men'].sort_values(['Municipality','Year','Edulvl']).rename(columns={'disposable income':'disposable_income_men'})

Women = Sortet_year[Sortet_year['Gender']=='Women'].sort_values(['Municipality', 'Year','Edulvl']).rename(columns={'disposable income':'disposable_income_women'})

#We don't want year to appear twice when we concat:
Women_without_year = Women[['Gender', 'disposable_income_women']]

#Concatenate the two tables:
Concatenated_table = pd.concat([Men, Women_without_year], axis=1)

#Remove gender
Final_table = Concatenated_table[['Municipality','Edulvl','disposable_income_men','disposable_income_women']]

#TEST

#Creates a function with provides the difference between the genders in %:
def f(x):
    """Gives the procentual difference between the genders"""
    return round((x['disposable_income_men']/x['disposable_income_women']-1)*100, 2)

#Applying the function to the end of the table:
Final_table['Difference in %']=Final_table.apply(f, axis=1)

Sortet_table = Final_table.sort_values(by=(["Municipality", "Edulvl"])).groupby("Year", as_index=True).first()

unik_mun = Final_table.index.unique()
d = {}

for i in unik_mun:
    d.update( {i : Final_table.loc[i]})

def Difference(Region):
    #Simply plotting the difference against years to see the evolution
    plt.plot(d[Region]['Year'],d[Region]['Difference in %'])
    plt.xlabel('Year')
    plt.ylabel('Difference in %')
    plt.title(f'Difference in disposable_income for {str(Region)}')
    plt.axis([2004,2018,6,36])
    plt.grid(True)
    return plt.show()


#We now wish to create a individual table for each province and education level, and do it like this:
#We start by finding the unique values in the table AKA all the provinces and all the educationlevels

#unik_edu = Final_table.Edulvl.unique()


#DET ENESTE DER SKAL OPDATERES ER EN DIC DER PASSER MED BÅDE MUN OG EDU

#Making an empty dictionary which will contain our unique values with their seperate table later


#Filling the empty dictionary


#We can now plot the difference between men and women in a graph like this:

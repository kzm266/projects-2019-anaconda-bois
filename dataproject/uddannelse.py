#Uddannelse

import numpy as np
import pandas as pd
import pydst
import matplotlib.pyplot as plt
import itertools
#DATACLEANING#

#We use pydst to use an API to Denmark's statistics
Dst = pydst.Dst(lang='en')
Dst.get_data(table_id='INDKP107')
Vars = Dst.get_variables(table_id='INDKP107')

#We pickout the table we want to analyse, and sort the values we want to inspect
All_data = Dst.get_data(table_id="INDKP107", variables={"OMRÅDE":['000','01','02','03','04','05','06','07','08','09','10','11'], "ENHED":["116"], "KOEN":["M", "K"], "UDDNIV":["*"], "TID":["*"], "INDKOMSTTYPE":["100"] }).rename(columns={'KOEN':'Gender','OMRÅDE':'Municipality', 'UDDNIV':'Edulvl', 'TID':'Year', 'INDHOLD':'disposable income'})

#We index by year in order to streamline the data 
yearindex_all_data = All_data.set_index('Year')

#Sort the data 
Sortet_year = yearindex_all_data[['Municipality','Edulvl','Gender','disposable income']]


#Creathe genderspecific data 
Men = Sortet_year[Sortet_year['Gender']=='Men'].sort_values(['Municipality','Year','Edulvl']).rename(columns={'disposable income':'disposable_income_men'})

Women = Sortet_year[Sortet_year['Gender']=='Women'].sort_values(['Municipality', 'Year','Edulvl']).rename(columns={'disposable income':'disposable_income_women'})

#We don't want year to appear twice when we concat, so we use the following function:
Women_without_year = Women[['Gender', 'disposable_income_women']]

#Concatenate the two tables:
Concatenated_table = pd.concat([Men, Women_without_year], axis=1)

#Remove gender
Final_table1 = Concatenated_table[['Municipality','Edulvl','disposable_income_men','disposable_income_women']]

#Creates a function which provides the difference between the genders in %:
def f(x):
    """Gives the procentual difference between the genders"""
    return round((x['disposable_income_men']/x['disposable_income_women']-1)*100, 2)

#Applying the function to the end of the table:
Final_table1['Difference in %']=Final_table1.apply(f, axis=1)

#Rename the labels for more beautiful result
Final_table1 = Final_table1.replace("10 BASIC SCHOOL 8-10 grade","BASIC SCHOOL 8-10 grade").replace("20+25 UPPER SECONDARY SCHOOL","UPPER SECONDARY SCHOOL").replace("35 VOCATIONAL EDUCATION","VOCATIONAL EDUCATION").replace("40 SHORT-CYCLE HIGHER EDUCATION","SHORT-CYCLE HIGHER EDUCATION").replace("50+60 MEDIUM-CYCLE HIGHER EDUCATION, BACHLEOR","MEDIUM-CYCLE HIGHER EDUCATION BACHLEOR").replace("65 LONG-CYCLE HIGHER EDUCATION","LONG-CYCLE HIGHER EDUCATION")

#Define the function for the difference graph
def Difference(Municipality,Edulvl):
    pd.DataFrame(Final_table1).groupby(by=["Municipality","Edulvl"], as_index=True).get_group((Municipality,Edulvl)).plot(by="Difference in %",y="Difference in %")
    plt.xlabel('Year')
    plt.ylabel('Difference in %')
    plt.title(f'Difference in disposable income for {str(Municipality)} with educationlevel {str(Edulvl)}')
    plt.grid(True)
    return plt.show()

#Define the function that shows both men and women 
def MenWomen(Municipality,Edulvl):
    pd.DataFrame(Final_table1).groupby(by=["Municipality","Edulvl"], as_index=True).get_group((Municipality,Edulvl)).plot(y=["disposable_income_men","disposable_income_women"])
    plt.xlabel('Year')
    plt.ylabel('Average disposable income')
    plt.title(f'Disposable income for men and women from {str(Municipality)} with educationlevel {str(Edulvl)}')
    plt.grid(True)
    return plt.show()
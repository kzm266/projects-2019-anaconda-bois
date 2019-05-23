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
Final_table1 = Concatenated_table[['Municipality','Edulvl','disposable_income_men','disposable_income_women']]
#Final_table = Final_table1().replace("10 BASIC SCHOOL 8-10 grade","BASIC SCHOOL 8-10 grade").replace("20+25 UPPER SECONDARY SCHOOL","UPPER SECONDARY SCHOOL").replace("35 VOCATIONAL EDUCATION","VOCATIONAL EDUCATION").replace("40 SHORT-CYCLE HIGHER EDUCATION","SHORT-CYCLE HIGHER EDUCATION").replace("50+60 MEDIUM-CYCLE HIGHER EDUCATION, BACHLEOR","MEDIUM-CYCLE HIGHER EDUCATION BACHLEOR").replace("65 LONG-CYCLE HIGHER EDUCATION","LONG-CYCLE HIGHER EDUCATION") 

All = slice(None)

#Creates a function which provides the difference between the genders in %:
def f(x):
    """Gives the procentual difference between the genders"""
    return round((x['disposable_income_men']/x['disposable_income_women']-1)*100, 2)

#Applying the function to the end of the table:
Final_table1['Difference in %']=Final_table1.apply(f, axis=1)


def Difference(Municipality,Edulvl):
    #Simply plotting the difference against years to see the evolution
    #pd.DataFrame(Final_table1).groupby(["Municipality","Edulvl"], as_index=True)
    pd.DataFrame(Final_table1).groupby(by=["Municipality","Edulvl"], as_index=True).get_group((Municipality,Edulvl)).plot(by="Difference in %")
    plt.xlabel('Year')
    plt.ylabel('Difference in %')
    plt.title(f'Difference in disposable income for {str(Municipality)} with educationlevel {str(Edulvl)}')
    plt.axis([2003,2018,0,50])
    plt.grid(True)
    return plt.show()




#We now wish to create a individual table for each province and education level, and do it like this:
#We start by finding the unique values in the table AKA all the provinces and all the educationlevels

#unik_edu = Final_table.Edulvl.unique()


#DET ENESTE DER SKAL OPDATERES ER EN DIC DER PASSER MED BÅDE MUN OG EDU

#Making an empty dictionary which will contain our unique values with their seperate table later


#Filling the empty dictionary


#We can now plot the difference between men and women in a graph like this:



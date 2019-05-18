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
Men = Sortet_mun[Sortet_mun['Gender']=='Men'].sort_values(['Municipality','Year','Edulvl']).rename(columns={'disposable income':'disposable_income_men'})

Women = Sortet_mun[Sortet_mun['Gender']=='Women'].sort_values(['Municipality', 'Year','Edulvl']).rename(columns={'disposable income':'disposable_income_women'})

#Merge tables
merged_table = pd.merge(Men, Women, on=['Year','Edulvl', 'Municipality'], how='outer')

#Final
#Final_table = 



#We don't want year to appear twice when we concat:
#Women_without_year = Women[['Gender', 'disposable_income_women']]

#Concatenate the two tables:
#Concatenated_table = pd.concat([Men, Women_without_year], axis=1)

#Remove gender
#Final_table = Concatenated_table[['disposable_income_men','disposable_income_women']]

#TEST

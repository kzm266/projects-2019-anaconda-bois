import numpy as np
import pandas as pd
import pydst
import matplotlib.pyplot as plt

Dst = pydst.Dst(lang='en')
Dst.get_data(table_id='INDKP101')
Vars = Dst.get_variables(table_id='INDKP101')
Everything = Dst.get_data(table_id = 'INDKP101', variables={'OMRÅDE':['000','11'], 'KOEN':['M','K'], 'TID':['*'], 'ENHED':['116'], 'INDKOMSTTYPE':['100']}).rename(columns={'OMRÅDE':'Municipality'})
#Changing the index to Municipality:
New_index = Everything.set_index('Municipality')
#Picking out the neccesary variables:
Sortet = New_index[['TID','KOEN','INDHOLD']].rename(columns={'KOEN':'Gender', 'TID':'Year', 'INDHOLD':'Disposal income'})
#Making a table for each gender:
Men = Sortet[Sortet['Gender']=='Men'].sort_values(['Municipality','Year']).rename(columns={'Disposal income':'Disposal income men'})
Women = Sortet[Sortet['Gender']=='Women'].sort_values(['Municipality', 'Year']).rename(columns={'Disposal income':'Disposal income women'})
#We don't want year to appear twice when we concat:
Women_without_year = Women[['Gender', 'Disposal income women']]
#Concatenate the two tables:
Concatenated_table = pd.concat([Men, Women_without_year], axis=1)
#Removing the gender nicer look:
Final_table = Concatenated_table[['Year','Disposal income men','Disposal income women']]
Final_table
#Creates a function with provides the difference between the genders in %:
def f(x):
    """Gives the procentual difference between the genders"""
    return (x['Disposal income men']/x['Disposal income women']-1)*100
Final_table['Difference in %']=Final_table.apply(f, axis=1)
Final_table.loc['All Denmark'].head()
#Example on finding the numbers for All Denmark:
Whole_country = Final_table.loc['All Denmark']
Final_table['Province']

#Nice graf
plt.plot(Whole_country['Year'],Whole_country['Difference in %'])
plt.xlabel('Year')
plt.ylabel('Difference in %')
plt.title('Difference in disposal income for all Denmark')
plt.grid(True)
plt.show()


Copenhagen = Final_table.loc['Copenhagen']
def standard_for_men(Municipality):
    """Creates a standard normal distribution for men's disposal income in the chosen municipality"""
    s = np.random.normal(Municipality['Disposal income men'].mean(), Municipality['Disposal income men'].std(), 10000)
    count, bins, ignored = plt.hist(s, 30, density=True)
    plt.plot(bins, 1/(Municipality['Disposal income men'].std() *np.sqrt(2*np.pi)) * np.exp(-(bins-Municipality['Disposal income men'].mean())**2 / (2 * Municipality['Disposal income men'].std()**2)), linewidth = 2)
    return plt.show

def standard_for_women(Municipality):
    """Creates a standard normal distribution for women's disposal income in the chosen municipality"""
    s = np.random.normal(Municipality['Disposal income women'].mean(), Municipality['Disposal income women'].std(), 10000)
    count, bins, ignored = plt.hist(s, 30, density=True)
    plt.plot(bins, 1/(Municipality['Disposal income women'].std() *np.sqrt(2*np.pi)) * np.exp(-(bins-Municipality['Disposal income women'].mean())**2 / (2 * Municipality['Disposal income women'].std()**2)), linewidth = 2)
    return plt.show



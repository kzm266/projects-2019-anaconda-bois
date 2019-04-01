import numpy as np
import pandas as pd
import pydst
import matplotlib.pyplot as plt

Dst = pydst.Dst(lang='en')
Dst.get_data(table_id='INDKP101')
Vars = Dst.get_variables(table_id='INDKP101')

Everything = Dst.get_data(table_id = 'INDKP101', variables={'OMRÅDE':['*'], 'KOEN':['M','K'], 'TID':['*'], 'INDKOMSTTYPE':['100']}).rename(columns={'OMRÅDE':'Municipality'})
#Changing the index to AREA:
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
#Creates a function with provides the difference between the genders in %:
def f(x):
    """Gives the procentual difference between the genders"""
    return (x['Disposal income women']/x['Disposal income men']-1)*100
Final_table['Difference in %']=Final_table.apply(f, axis=1)
Final_table.loc['All Denmark'].head()
#Example on finding the numbers for All Denmark:
Whole_country = Final_table.loc['All Denmark']

#Nice graf
plt.plot(Whole_country['Year'],Whole_country['Difference in %'])
plt.xlabel('Year')
plt.ylabel('Difference in %')
plt.title('Difference in disposal income for all Denmark')
plt.grid(True)
plt.show()


def standard(mu, sigma):
    """Creates a standard normal distribution, where you can choose your own mean and variation"""
    s = np.random.normal(mu, sigma, 10000)
    count, bins, ignored = plt.hist(s, 30, density=True)
    plt.plot(bins, 1/(sigma *np.sqrt(2*np.pi)) * np.exp(-(bins-mu)**2 / (2 * sigma**2)), linewidth = 2)
    return plt.show

#Finding the normal distribution for Copenhagen and all Denmark:
Copenhagen.mean()
Copenhagen.std()
Whole_country.mean()
Whole_country.std()
plt.show(standard(205228.58, 16782.75), standard(214377.2, 82925.37))

#Import the neccesary packages
import numpy as np
import pandas as pd
import pydst
import matplotlib.pyplot as plt

#We use pydst to use an API to Denmark's statistics
Dst = pydst.Dst(lang='en')
Dst.get_data(table_id='INDKP101')
Vars = Dst.get_variables(table_id='INDKP101')

#To find the variables we need, we inspect the table that we have imported:
Vars.values

#After picking out values, we can get our data:
Everything = Dst.get_data(table_id = 'INDKP101', variables={'OMRÅDE':['000','01','02','03','04','05','06','07','08','09','10','11'], 'KOEN':['M','K'], 'TID':['*'], 'ENHED':['116'], 'INDKOMSTTYPE':['100']}).rename(columns={'OMRÅDE':'Municipality'})

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

#Applying the function to the end of the table:
Final_table['Difference in %']=Final_table.apply(f, axis=1)

#Example on finding the numbers for All Denmark:
All_Denmark = Final_table.loc['All Denmark']
print(All_Denmark.head())

#We can show this in a graph like this:
def Difference(Region):
    #Simply plotting the difference against years to see the evolution
    plt.plot(d[Region]['Year'],d[Region]['Difference in %'])
    plt.xlabel('Year')
    plt.ylabel('Difference in %')
    plt.title('Difference in disposal income')
    plt.grid(True)
    return plt.show()

#Finding the unique values in the table AKA all the provinces
unik = Final_table.index.unique()

#Making an empty dictionary which will contain our unique values with their seperate table later
d = {}

#Filling the empty dictionary
for i in unik:
    d.update( {i : Final_table.loc[i]})


#To compare the genders visually, we create two standard normal distributions where the standard deviation is shown in the legend:
def standard(Region):
    
    #Making subplots to be shown in the same figure:
    plt.subplot(2,1,1)
    
    #Creating the normal distribution for the men:
    s = np.random.normal(d[Region]['Disposal income men'].mean(), d[Region]['Disposal income men'].std(), 10000)
    count, bins, ignored = plt.hist(s, 30, density=True)
    
    #Plotting the distribution:
    plt.plot(bins, 1/(d[Region]['Disposal income men'].std() *np.sqrt(2*np.pi)) * np.exp(-(bins-d[Region]['Disposal income men'].mean())**2 / (2 * d[Region]['Disposal income men'].std()**2)), linewidth = 4)
    
    #Some formal stuff
    plt.title('Men')
    plt.xlabel('Disposal income')
    plt.axis([0,300000,0,0.000011])
    
    #The other subplot:
    plt.subplot(2,1,2)
    
    #Creating the normal distribution for the women:
    s = np.random.normal(d[Region]['Disposal income women'].mean(), d[Region]['Disposal income women'].std(), 10000)
    count, bins, ignored = plt.hist(s, 30, density=True)
   
   #Plotting the distribution:
    plt.plot(bins, 1/(d[Region]['Disposal income women'].std() *np.sqrt(2*np.pi)) * np.exp(-(bins-d[Region]['Disposal income women'].mean())**2 / (2 * d[Region]['Disposal income women'].std()**2)), linewidth = 4)
    
    #Formal figure stuff again
    plt.title('Women')
    plt.xlabel('Disposal income')
    plt.axis([0,300000,0,0.000011])
    plt.subplots_adjust(top=2, bottom=0, left=0, right=1, hspace=0.2)
       
    return plt.show(), print('For men, the mean is ','{0:.0f}'.format(d[Region]['Disposal income men'].mean()), 'and the standard deviation is ','{0:.0f}'.format(d[Region]['Disposal income men'].std())), print('For women, the mean is ','{0:.0f}'.format(d[Region]['Disposal income women'].mean()), 'and the standard deviation is ','{0:.0f}'.format(d[Region]['Disposal income women'].std()))

#We can now see the two normal distributions in the same figure, with the standard deviation in the legend:
standard('Province Fyn')
import numpy as np
import pandas as pd
import pydst
import matplotlib.pyplot as plt

Dst = pydst.Dst(lang='da')
Dst.get_data(table_id='INDKP101')
Vars = Dst.get_variables(table_id='INDKP101')

Alt = Dst.get_data(table_id = 'INDKP101', variables={'OMRÅDE':['*'], 'KOEN':['M','K'], 'TID':['*'], 'INDKOMSTTYPE':['100']})
#Skifter index til OMRÅDE i stedet for:
Alti = Alt.set_index('OMRÅDE')
#Udvælger ting så de andre ting ikke kommer med:
Sorteret = Alti[['TID','KOEN','INDHOLD']].rename(columns={'KOEN':'Køn', 'TID':'År', 'INDHOLD':'Disp. indkomst'})
#Laver en tabel for hvert køn seperat:
Mænd = Sorteret[Sorteret['Køn']=='Mænd'].sort_values(['OMRÅDE','År']).rename(columns={'Disp. indkomst':'Disp. indkomst mænd'})
Kvinder = Sorteret[Sorteret['Køn']=='Kvinder'].sort_values(['OMRÅDE', 'År']).rename(columns={'Disp. indkomst':'Disp. indkomst kvinder'})
#Skal ikke have år med 2 gange når vi sammensætter:
SortKvinder = Kvinder[['Køn', 'Disp. indkomst kvinder']]
#Sammensæt de to tabeller:
Pænt = pd.concat([Mænd, SortKvinder], axis=1)
#Fjern køn #NoGenderAssuming
Endnu_pænere = Pænt[['År','Disp. indkomst mænd','Disp. indkomst kvinder']]
#Funktion der giver forskellen i pct.
def f(x):
    return (x['Disp. indkomst kvinder']/x['Disp. indkomst mænd']-1)*100
Endnu_pænere['Forskel i %']=Endnu_pænere.apply(f, axis=1)
Endnu_pænere.loc['Hele landet'].head()
#Eksempel på at finde tal fra København
København = Endnu_pænere.loc['København']
#For hele landet:
Hele_Landet = Endnu_pænere.loc['Hele landet']

#Fed graf
plt.plot(København['År'],København['Forskel i %'])
plt.xlabel('År')
plt.ylabel('Procentvis forskel')
plt.title('Forskel i disponibel indkomst for København')
plt.grid(True)
plt.show()


def standard(mu,sigma): 
    #Laver normalfordeling   
    s = np.random.normal(mu, sigma, 10000)
    count, bins, ignored = plt.hist(s, 30, density=True)
    plt.plot(bins, 1/(sigma *np.sqrt(2*np.pi)) * np.exp(-(bins-mu)**2 / (2 * sigma**2)), linewidth = 2)
    return plt.show

#Finder normalfordelingen for København og hele landet:
København.mean()
København.std()
Hele_Landet.mean()
Hele_Landet.std()
plt.show(standard(205228.58, 16782.75), standard(214377.2, 82925.37))

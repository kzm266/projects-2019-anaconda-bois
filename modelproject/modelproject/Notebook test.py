#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'modelproject'))
	print(os.getcwd())
except:
	pass

#%%
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
# You can load your python module as this:
import modelproject.example


#%%



#%%
med dig jeg hedder Kaj


#%%
fafoihan


#%%
fjfpoaj



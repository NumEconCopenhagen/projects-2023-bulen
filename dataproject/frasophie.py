# %% [markdown]

# # Dataproject - "Alderskorrigeret mordrate"



# %% [markdown]

# > **Note the following:** 

# > 1. This is *not* meant to be an example of an actual **data analysis project**, just an example of how to structure such a project.

# > 1. Remember the general advice on structuring and commenting your code

# > 1. The `dataproject.py` file includes a function which can be used multiple times in this notebook.



# %% [markdown]

# Imports and set magics:



# %%



%pip install git+https://github.com/elben10/pydst

%pip install pandas-datareader

%pip install matplotlib-venn



import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import ipywidgets as widgets

from matplotlib_venn import venn2



# autoreload modules when code is run

%load_ext autoreload

%autoreload 2





# user written modules



import pandas_datareader



import pydst

import dataproject





# %% [markdown]

# ### 1.1. <a id='toc1_1_'></a>[Import data from Denmark Statistics](#toc0_)



# %% [markdown]

# Import your data, either through an API or manually, and load it. 



# %%

Dst = pydst.Dst(lang='da')

Dst.get_subjects()





# %%

tables = Dst.get_tables(subjects=['4'])

print(type(tables))

display(tables)





# %%

tables[tables.id == 'STRAF40']



# %%

straf = Dst.get_variables(table_id='STRAF40')

straf



# %%

straf = Dst.get_variables(table_id='STRAF40')



for id in ['OVERTRÆD','AFGØRELSE','ALDER','KØN','Tid']:

print(id)

values = straf.loc[straf.id == id,['values']].values[0,0]

for value in values: 

print(f' id = {value["id"]}, text = {value["text"]}')



# %%

variables = {'OVERTRÆD':['1230'],'AFGØRELSE':['1', '11', '111', '112', '113', '114', '115', '116'],'KØN':['M'],'ALDER':['16', '17', '18', '19', '20', '21', '22', '23'],'Tid':['*']}

straf_40 = Dst.get_data(table_id = 'STRAF40', variables=variables)

straf_40.sort_values(by=['TID', 'KØN', 'ALDER'], inplace=True)

straf_40.head(5)

straf_40_ny = straf_40.assign(C=1)

straf_40_ny.head(5)



# %%

ny_straf = pd.pivot_table(straf_40_ny, values = ['C'], index = ['ALDER'], columns = ['TID'], aggfunc= 'sum')

ny_straf.head(5)





# %% [markdown]

# ## Explore each data set



# %% [markdown]

# In order to be able to **explore the raw data**, you may provide **static** and **interactive plots** to show important developments 



# %% [markdown]

# **Interactive plot** :



# %%

def plot_func():

# Function that operates on data set

pass



widgets.interact(plot_func, 

# Let the widget interact with data through plot_func() 

); 





# %% [markdown]

# Explain what you see when moving elements of the interactive plot around. 



# %% [markdown]

# # Merge data sets



# %% [markdown]

# Now you create combinations of your loaded data sets. Remember the illustration of a (inner) **merge**:



# %%

plt.figure(figsize=(15,7))

v = venn2(subsets = (4, 4, 10), set_labels = ('Data X', 'Data Y'))

v.get_label_by_id('100').set_text('dropped')

v.get_label_by_id('010').set_text('dropped' )

v.get_label_by_id('110').set_text('included')

plt.show()



# %% [markdown]

# Here we are dropping elements from both data set X and data set Y. A left join would keep all observations in data X intact and subset only from Y. 

# 

# Make sure that your resulting data sets have the correct number of rows and columns. That is, be clear about which observations are thrown away. 

# 

# **Note:** Don't make Venn diagrams in your own data project. It is just for exposition. 



# %% [markdown]

# # Analysis



# %% [markdown]

# To get a quick overview of the data, we show some **summary statistics** on a meaningful aggregation. 



# %% [markdown]

# MAKE FURTHER ANALYSIS. EXPLAIN THE CODE BRIEFLY AND SUMMARIZE THE RESULTS.



# %% [markdown]

# # Conclusion



# %% [markdown]

# ADD CONCISE CONLUSION.


# coding: utf-8

# In[ ]:


# Dependencies
import pandas as pd
import numpy as np
import os


# In[ ]:


# Store filepath in a variable
hawaii_measurements_file = "Resources/hawaii_measurements.csv"
hawaii_stations_file = "Resources/hawaii_stations.csv"

# Read our Data file with the pandas library
# Not every CSV requires an encoding, but be aware this can come up
hawaii_measurements_df = pd.read_csv(hawaii_measurements_file, encoding = "ISO-8859-1")
hawaii_stations_df = pd.read_csv(hawaii_stations_file, encoding = "ISO-8859-1")


# In[ ]:


hawaii_measurements_df.head(5)


# In[ ]:


hawaii_stations_df.head(5)


# In[ ]:


A_hawaii_measurements_df = hawaii_measurements_df.dropna(how = 'any')
A_hawaii_measurements_df.head(2)


# In[ ]:


A_hawaii_stations_df = hawaii_stations_df.dropna(how = 'any')
A_hawaii_stations_df.head(2)


# In[ ]:


print(A_hawaii_measurements_df.isnull().values.any())
print(A_hawaii_stations_df.isnull().values.any())


# In[ ]:


clean_hawaii_measurements_df = A_hawaii_measurements_df.copy()
clean_hawaii_stations_df = A_hawaii_stations_df.copy()


# In[ ]:


#clean_hawaii_measurements_df.head(2)
#clean_hawaii_stations_df.head(2)


# In[ ]:


# Export file as a CSV, without the Pandas index, but with the header
clean_hawaii_measurements_df.to_csv("Output/clean_hawaii_measurements.csv", index=False, header=True)
clean_hawaii_stations_df.to_csv("Output/clean_hawaii_stations.csv", index=False, header=True)


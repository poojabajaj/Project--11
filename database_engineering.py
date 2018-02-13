
# coding: utf-8

# In[ ]:


get_ipython().system('rm hawaii.sqlite')


# In[ ]:


#dependecies
from sqlalchemy import Column, Float, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

import pandas as pd
import numpy as np
import os


# In[ ]:


# Store filepath in a variable
clean_hawaii_measurements = "Output/clean_hawaii_measurements.csv"
clean_hawaii_stations = "Output/clean_hawaii_stations.csv"


# In[ ]:


# Read our Data file with the pandas library
# Not every CSV requires an encoding, but be aware this can come up
clean_hawaii_measurements_df = pd.read_csv(clean_hawaii_measurements, encoding = "ISO-8859-1")
clean_hawaii_stations_df = pd.read_csv(clean_hawaii_stations, encoding = "ISO-8859-1")


# In[ ]:


#print cokumn names in a dataframe using list
print(list(clean_hawaii_measurements_df))
print(list(clean_hawaii_stations_df))


# In[ ]:


clean_hawaii_measurements_df['id'] = pd.Series(clean_hawaii_measurements_df.index).apply(lambda x: x+1)


# In[ ]:


clean_hawaii_stations_df['id'] = pd.Series(clean_hawaii_stations_df.index).apply(lambda x: x+1)


# In[ ]:


# Creates Classes which will serve as the anchor points for our Tables
class Measurement(Base):
    __tablename__ = 'measurements_table'
    id = Column(Integer, primary_key=True)
    station = Column(String(255))
    date = Column(String)
    prcp = Column(Float)
    tobs = Column(Integer)


# In[ ]:


# Creates Classes which will serve as the anchor points for our Tables
class Station(Base):
    __tablename__ = 'stations_table'
    id = Column(Integer, primary_key=True)
    station = Column(String(255))
    name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)


# In[ ]:


# Use a Session to test the class
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///hawaii.sqlite")
Base.metadata.create_all(engine)


# In[ ]:


# Create a session
session = Session(engine)


# In[ ]:


session.commit()


# In[ ]:


clean_hawaii_measurements_df.to_sql('measurements_table', engine, if_exists='append', index = Measurement.date)


# In[ ]:


clean_hawaii_stations_df.to_sql('stations_table', engine, if_exists = 'append', index = Station.id)


# In[ ]:


session.query(Measurement).filter(Measurement.prcp > 0.05).all()


# In[ ]:


# Use the session to query measurements table and display the first 5 locations
for row in session.query(Measurement).limit(5).all():
    print(vars(row))


# In[ ]:


session.query(Station).all()


# In[ ]:


for row in session.query(Station).limit(5).all():
    print(vars(row))


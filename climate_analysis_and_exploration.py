
# coding: utf-8

# In[ ]:


#dependecies
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, desc
###
from sqlalchemy import Column, Float, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

import pandas as pd
import numpy as np
import os

from datetime import datetime as dt
from statistics import mean

# Import Matplot lib and use the `nbagg` backend
### BEGIN SOLUTION
import matplotlib
matplotlib.use('nbagg')
from matplotlib import style
style.use('seaborn')
import matplotlib.pyplot as plt
### END SOLUTION


# In[ ]:


engine = create_engine("sqlite:///hawaii.sqlite")
Base.metadata.create_all(engine)


# In[ ]:


# Create a session
session = Session(engine)


# In[ ]:


# Create the inspector and connect it to the engine
inspector = inspect(engine)


# In[ ]:


# Collect the names of tables within the database
inspector.get_table_names()


# In[ ]:


# Declare a Base using `automap_base()`
Base = automap_base()


# In[ ]:


# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)


# In[ ]:


# # Assign the class to a variable 
Measurement = Base.classes.measurements_table
Station = Base.classes.stations_table


# In[ ]:


#Use SQLAlchemy automap_base() to reflect your tables into classes 
#and save a reference to those classes called Station and Measurement.


# In[ ]:


# Print all of the classes mapped to the Base
Base.classes.keys()


# In[ ]:


# Using the inspector to print the column names within the 'dow' table and its types
columns = inspector.get_columns('measurements_table')
print(columns)
#date.min()


# In[ ]:


#Choose a start date and end date for your trip. Make sure that your vacation range is approximately 3-15 days total.
start_date = '2010-01-01'
end_date = '2010-01-10'


# In[ ]:


#session.query(Measurement).filter(Measurement.date>'2016-8-22').filter(Measurement.date<='2017-8-23').all()
print(session.query(Measurement).count())
print(session.query(Station).count())


# In[ ]:


results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between('2016-08-23', '2017-08-23'))
#print(results[0])
#print(vars(results))


# In[ ]:


results.all()


# In[ ]:


session.query(Measurement.date).filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()


# In[ ]:


# Unpack the prcp and date from results and save into separate lists
### BEGIN SOLUTION
prcp = [result.prcp for result in results]

#print(prcp)
date_string = [result.date for result in results]
date = [dt.strptime(d,'%Y-%m-%d').date() for d in date_string]
#date_list.dt.strftime('%Y%m%d').astype(int)
#date_list= date_list.apply(lambda x: x.strftime('%Y-%m-%d')).astype(int)
#print(date_list)
### END SOLUTION
date


# In[ ]:


print(type(prcp[0]))
print(type(date[0]))


# In[ ]:


# Load the results into a pandas dataframe. Set the index to the date
### BEGIN SOLUTION
#prcp_year_df = pd.DataFrame(results, columns = ['date', 'prcp'])
prcp_year_df = pd.DataFrame(prcp, date, columns = ["Precipitation"])
#prcp_year_df.set_index(date, inplace=True)
#prcp_year_df.index = pd.to_datetime(prcp_year_df.index)

### END SOLUTION
prcp_year_df.head(10)


# In[ ]:


#prcp_year_df.to_csv("a.csv")


# In[ ]:


prcp_year_df.index.values
#plt.xticks(prcp_year_df['Precipitation'], prcp_year_df.index.values)


# In[ ]:


#prcp_year_df.drop_duplicates()


# In[ ]:


#prcp_year_df.to_csv("b.csv")


# In[ ]:


#Precipitation analysis graph shows two lines which is because of multiple values of precipitation for a particular 
#date. Below analysis depicts multiple stations as we have not picked one particular station. 
precipation, = plt.plot(prcp_year_df.index.values, prcp_year_df['Precipitation'], color = 'blue', alpha = 0.5)
plt.legend(handles=[precipation], loc="best")
plt.xticks(rotation=45)
plt.title("Precipitation Analysis")
plt.xlabel("Date")
plt.ylabel("Precipitation")
plt.savefig("PrecipitationAnalysis.png")
plt.show()


# In[ ]:


#Use Pandas to print the summary statistics for the precipitation data.
prcp_year_df.describe()


# In[ ]:


#Station Analysis
#Design a query to calculate the total number of stations.
NoOfStations = session.query(Station).count()
NoOfStations


# In[ ]:


#Design a query to find the most active stations.
ListActiveStationsAndcount = session.query(Measurement.station, func.sum(Measurement.tobs).label('freq')).group_by(Measurement.station).order_by(desc('freq'))

#unpacking the tuple
MostActiveStations = [idx for idx, val in ListActiveStationsAndcount.limit(5).all()]
MostActiveStations

MostActiveStations


# In[ ]:


#List the stations and observation counts in descending order
ListActiveStationsAndcount.all()


# In[ ]:


#Which station has the highest number of observations?
StationsObservation = session.query(Measurement.station, func.sum(Measurement.tobs).label('obs')).group_by(Measurement.station).order_by(desc('obs'))

StationsWithHighestObservation= StationsObservation.limit(1).all()[0][0]
StationsWithHighestObservation


# In[ ]:


#Design a query to retrieve the last 12 months of temperature observation data (tobs).
Last12TobsDate = session.query(Measurement).filter(Measurement.date.between('2016-08-23', '2017-08-23'))

tobs = [result.tobs for result in Last12TobsDate]
date = [result.date for result in Last12TobsDate]


# In[ ]:


#Filter by the station with the highest number of observations.
#HighestTobsRecord = session.query(Measurement).\
#filter(Measurement.station ==StationsWithHighestObservation)

HighestTobsRecord = Last12TobsDate.filter(Measurement.station ==StationsWithHighestObservation)
HighestTobsRecord = [result.tobs for result in HighestTobsRecord]
HighestTobsRecord


# In[ ]:


#Plot the results as a histogram with bins=12.
#plots the histogram
fig, ax1 = plt.subplots()
plt.hist(HighestTobsRecord, bins = 12, alpha=0.5)
ax1.set_xlim(50,90)
ax1.set_ylabel("Frequency")
plt.tight_layout()
plt.savefig("HighestTobsRecord_hist.png")
plt.show()


# In[ ]:


#Write a function called calc_temps that will accept a start date and end date in the format %Y-%m-%d 
#and return the minimum, average, and maximum temperatures for that range of dates.
def calc_temps(startDate, endDate):
    results = session.query(Measurement).filter(Measurement.date.between(startDate, endDate))
    temp = [result.tobs for result in results]
    return min(temp), mean(temp), max(temp) 


# In[ ]:


minm, avg, maxm = calc_temps('2010-01-01', '2010-01-10')
#print(minm, avg, maxm)


# In[ ]:


#plt.figure(figsize=(2,5))
x_axis = 1
fig, ax = plt.subplots(figsize=plt.figaspect(1.))
ax.bar(x_axis, avg, width=0.5, color='r', alpha=0.35, align="center", yerr = (maxm-minm))
ax.set_xlim(0, 2)
ax.set_ylim(0, 100)
plt.title("Trip average temperature")
plt.ylabel("Temp F")

# Print our chart to the screen
plt.show()


# In[ ]:





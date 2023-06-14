# -*- coding: utf-8 -*-
"""
Created on Thu May 25 20:27:17 2023

@author: Jack Tattersall

CONNECTION PUNCTUALITY CALCULATOR
"""

# Required  modules to support calculations
import geopandas as geo
import pandas as pd
import r5py
import numpy as np
import os
import datetime as dt
from zipfile import ZipFile

'''
# GTFS Format:
Zip files must be of name AGENCYID_DATE.zip
Constituent files routes.txt and agencies.txt must include
column titled agency_id with correct AGENCYID in each entry.

Failure to adhere to these specs may lead to code issues.
'''
# Collect GTFS
Date = str("2022DEC14")     # Date of analysis as string YYYYMMMDD
# Specify list of agencies in analysis
scope = ['TTC','GO','YRT','DRT','HSR','BT','MilT','OakT','BurT','UPExpress']

# Initialize region-wide GTFS dataframes
operators = pd.empty()
agencies = pd.empty()
routes = pd.empty()
stops = pd.empty()
trips = pd.empty()
times = pd.empty()
dates = pd.empty()
shapes = pd.empty()
calendar = pd.empty()

for Agency in scope:
    ZipFile.extractall(f'{Agency}_{Date}_gtfs.zip')

    # Import as dataframes and add agency_id    
    agency = pd.read_table(f'{Agency}_{Date}_gtfs\\agency.txt')  
    Routes = pd.read_table(f'{Agency}_{Date}_gtfs\\routes.txt')
    Trips = pd.read_table(f'{Agency}_{Date}_gtfs\\trips.txt')
    Trips['agency_id'] = Agency
    Stops = pd.read_table(f'{Agency}_{Date}_gtfs\\stops.txt')
    Stops['agency_id'] = Agency
    Times = pd.read_table(f'{Agency}_{Date}_gtfs\\stop_times.txt')
    Times['agency_id'] = Agency
    Calendar = pd.read_table(f'{Agency}_{Date}_gtfs\\calendar.txt')
    calendar['agency_id'] = Agency
    Dates = pd.read_table(f'{Agency}_{Date}_gtfs\\dates.txt')
    Dates['agency_id'] = Agency
    Shapes = pd.read_table(f'{Agency}_{Date}_gtfs\\shapes.txt')
    Shapes['agency_id'] = Agency
    operators['agency_name'] = agency['agency_name']
    operators['agency_id'] = agency['agency_id']
    # Append to single region-wide GTFS dataframes
    agencies = pd.append(agency)
    routes = pd.append(Routes)
    stops = pd.append(Stops)
    trips = pd.append(Trips)
    times = pd.append(Times)
    dates = pd.append(Dates)
    shapes = pd.append(Shapes)
    calendar = pd.append(Calendar)


# Interchange Identification
'''
Search for main terminals/stations with common names
Check list of interchange hubs made up of stations/terminals with trigger words:
    Station, Terminal,
    
Note, Village Station Rd is a street in Toronto with corresponding bus stop 
'''
inter = pd.empty()
inter = stops.loc[stops['stop_name'].str.contains("Station", case=False)]
inter = stops.loc[stops['stop_name'].str.contains("Terminal", case=False)]
inter = stops.loc[stops['stop_name'].str.contains("Bus Terminal", case=False)]
interchange = inter[['agency_id','stop_id','stop_name','stop_lat', 'stop_lon']]
interchange.rename(columns={'agency_id':'to_agency','stop_name':'to_stop_name',
                             'stop_lat': 'to_stop_lat', 'stop_lon':'to_stop_lon'},
                    inplace=True)
fakehub = ['Station Rd', 'Station Ave', 'Station St', 
           'Terminal Rd', 'Terminal Ave', 'Terminal St']
for i in len(fakehub):
    inter = inter[inter.stop_name.contains(fakehub) == False]   

'''
THOUGHTS:
    Including high-frequency services may be problematic especially in reverse
    Metric will punish connections from hgih-frequency to low-frequency services 
        because most services will not meet a connection taker (low-frequncy service)
        
    Imagine:
        Route A calls at 00, 05, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55
        Route 1 calls at 03, 33             e.g. MinCT = 2, MaxCT = 2*H = 10
        Then 05, 10, 15, 20, 35, 40, 45, 50 arrivals would report 0 connection
        But a connection would never have been possible in the first place.
    So, then a denominator is required that reports what connections can exist in the first place 
        i.e. departures per hour
        thus, 12 tph connection to 2 tph only gives 2 connections possible in the first place
        At this: 2/2 = 100% CONNECTION PUNCTUALITY
'''

'''
Collect stops corresponding to the same interchange to create to/from selection

Hub list gives interchnages that are not published as such (Newcastle Street at Royal York Rd / Mimico GO;
                                                            Long Branch GO / Long Branch Loop)

'''
hub_list = pd.read_csv('GTHA_ConnectionHubs.csv')
# check hub list first
for i in range(len(hub_list)):
    pt = interchange.loc[interchange['stop_name'] == hub_list.hub[i]]
    addition = stops.loc[stops['stop_name'].str.contains(hub_list.althub1)]
    if hub_list.althub2[i].notna() == True:
        Addition = stops.iloc[i].str.contains(hub_list.althub2[i])
        Addition = pd.concat(addition,Addition, axis = 0)
        if hub_list.althub3[i].notna() == True:
            ADDITION = stops.iloc[i].str.contains(hub_list.althub3[i])
            addhub = pd.concat(ADDITION,Addition, axis = 0)
        else:
            addhub = Addition.copy()
    else:
        addhub = addition.copy()
  
connex = pd.empty()
for idx,hub in enumerate(interchange['stop_name']):
    key = find(' - ')
    if key != -1:
        if find('Station - ') != -1:
            Hub = hub[:key]
            Add = stops.loc[stops['stop_name'].str.contains(Hub, case=False)]['stop_name','stop_lat','stop_lon']
            Add['stop_name_to'] = hub
            
        else:
            Hub = hub[key:]
            Add = stops.loc[stops['stop_name'].str.contains(Hub, case=False)]['stop_name','stop_lat','stop_lon']
            Add['stop_name_to'] = hub
    cross = find(' at ')
    link = find(' and ')
    linx = find(' & ')
    if cross != -1:
        x1 = hub[:cross]
        x2 = hub[cross:]
        Add = stops.loc[stops['stop_name'].str.contains(x1, case=False) and 
                        stops['stop_name'].str.contains(x2, case=False)]['stop_name','stop_lat','stop_lon']
        add['stop_name_to'] = hub
    elif link != -1:
        x1 = hub[:link]
        x2 = hub[link:]
        Add = stops.loc[stops['stop_name'].str.contains(x1, case=False) and 
                        stops['stop_name'].str.contains(x2, case=False)]['stop_name','stop_lat','stop_lon']
        Add['stop_name_to'] = hub
    elif linx != -1:
        x1 = hub[:linx]
        x2 = hub[linx:]
        Add = stops.loc[stops['stop_name'].str.contains(x1, case=False) and 
                        stops['stop_name'].str.contains(x2, case=False)]['stop_name','stop_lat','stop_lon']
        Add['stop_name_to'] = hub
    else:
        pass

    # Code added 2023/06/13. Review functionality satisfies objectives.
    rep = len(interchange['stop_name'] == hub)
    interchange.loc[interchange.index.repeat(rep)].reset_index(drop=True)
    connex = pd.concat(connex,Add)
    
interchanges = pd.merge(interchange,connex,left_on = 'stop_name',right_on = 'stop_name_to',
                        suffixes=('_to', '_from'))

# Review arrangement of final output interchanges dataframe and simplify as beneficial: remove unneeded rows, check GPS coord format for R5Py

######## HERE :) ########  

# Inputs
# Review syntax for importing transportnetwork from OSM for R5Py
gtha = r5py.TransportNetwork('GTHA_OSM20230525.osm.pbf',, 
                             settings
                             )


def minimumCT(stop1, stop2):
    minCT
    # Determine walking distance between stops/stations
    # R5py using 1m/s walking speed on OpenStreetMap
    
def maximumCT(stop1,stop2):
    maxCT
    # Define based on a fixed value
    # Define based on multiple of headway. 
    
# Perform analysis

# Output results
pd.connex.to_csv('GTHA_connections.csv')
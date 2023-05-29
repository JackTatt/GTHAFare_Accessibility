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
operators = pd.empty()
agency = pd.empty()
routes = pd.empty()
stops = pd.empty()
trips = pd.empty()
times = pd.empty()
dates = pd.empty()
shapes = pd.empty()
calendar = pd.empty()

for Agency in scope:
    zipfile.extractall(f'{Agency}_{Date}_gtfs.zip')
    agency_{i} = pd.read_table(f'{Agency}_{Date}_gtfs\\agency.txt')  
    routes_{i} = pd.read_table(f'{Agency}_{Date}_gtfs\\routes.txt')
    trips_{i} = pd.read_table(f'{Agency}_{Date}_gtfs\\trips.txt')
    trips[agency_id] = Agency
    stops_{i} = pd.read_table(f'{Agency}_{Date}_gtfs\\stops.txt')
    stops[agency_id] = Agency
    times_{i} = pd.read_table(f'{Agency}_{Date}_gtfs\\stop_times.txt')
    times[agency_id] = Agency
    calendar_{i} = pd.read_table(f'{Agency}_{Date}_gtfs\\calendar.txt')
    calendar[agency_id] = Agency
    dates_{i} = pd.read_table(f'{Agency}_{Date}_gtfs\\dates.txt')
    dates[agency_id] = Agency
    shapes_{i} = pd.read_table(f'{Agency}_{Date}_gtfs\\shapes.txt')
    shapes[agency_id] = Agency
    operators.agency_name = agency_{i}['agency_name']
    operators.agency_id = agency_{i}['agency_id']
    
    agency = pd.append(agency_{i})
    routes = pd.append(routes_{i})
    stops = pd.append(stops_{i})
    trips = pd.append(trips_{i})
    times = pd.append(times_{i})
    dates = pd.append(dates_{i})
    shapes = pd.append(shapes_{i})
    calendar = pd.append(calendar_{i})

# Inputs
regionmap ##Path to OSM pbf
gtfs # List of paths to GTFS zips
settings # TNBuilderConfig
gtha = r5py.TransportNetwork(regionmap,gtfs, settings)

# Interchange Identification
'''
Search for main terminals/stations with common names
Check list of interchange hubs made up of stations/terminals with muliple names 

Collect list of all stops corresponding to each interchange

'''

def minimumCT(stop1, stop2):
    minCT
    # Determine walking distance between stops/stations
    # R5py using 1m/s walking speed on OpenStreetMap
    
def maximumCT(stop1,stop2):
    maxCT
    # Define based on a fixed value
    # Define based on multiple of headway. 
    
# Perform analysis

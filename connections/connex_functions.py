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
    # Determine walking distance between stops/stations
    # R5py using 1m/s walking speed on OpenStreetMap
    
def maximumCT(stop1,stop2):
    # Define based on a fixed value
    # Define based on multiple of headway. 
    
# Perform analysis

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

def minimumCT(stop1, stop2):
    # Determine walking distance between stops/stations
    # R5py using 1m/s walking speed on OpenStreetMap
    

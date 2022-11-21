#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 15:33:32 2022

@author: erika_ishizuka
"""

import os
import pandas as pd

#read files
base_path = '/Users/erika_ishizuka/Desktop/python_final_project'
vax_file = 'who_vax.csv'
em_yr_file = 'excess_yr.csv'
em_sex_file = 'excess_sex_age.csv'
em_mon_file = 'excess_yr_month.csv'
death_rate_file = 'crude_death.csv'

vax = pd.read_csv(os.path.join(base_path, vax_file))
em_yr = pd.read_csv(os.path.join(base_path, em_yr_file), skiprows=8)
em_sex = pd.read_csv(os.path.join(base_path, em_sex_file), skiprows=11)
em_mon = pd.read_csv(os.path.join(base_path, em_mon_file), skiprows=12)
crude_death = pd.read_csv(os.path.join(base_path, death_rate_file))

#cleaning
sa_iso = ['ARG', 'BOL', 'BRA', 'CHL', 'COL', 'ECU', 'GUY', 'PER', 'PRY', 'SUR', 
          'URY', 'VEN']

vax_cols = ['PRODUCT_NAME', 'COMPANY_NAME', 'AUTHORIZATION_DATE', 'END_DATE', 
            'COMMENT', 'DATA_SOURCE']
vax = vax.loc[vax['ISO3'].isin(sa_iso)].drop(vax_cols, axis=1).dropna()
vax = vax.rename(columns={'VACCINE_NAME': 'vaccine', 'START_DATE': 'start date', 
                          'ISO3': 'iso3'}).sort_values(by=['iso3'])
vax['year'] = pd.DatetimeIndex(vax['start date']).year
vax = vax.loc[vax['year'] != 2022]
result_vax = vax.groupby('iso3')['start date'].min().to_frame().reset_index()
new_vax = result_vax.merge(vax, how='outer', on=['iso3', 'start date']).iloc[0:13]
new_vax['month'] = pd.DatetimeIndex(new_vax['start date']).month

em_yr_cols = ['Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'excess.low', 'excess.high']
em_yr = em_yr.loc[em_yr['iso3'].isin(sa_iso)].drop(em_yr_cols, axis=1)
em_yr = em_yr.rename(columns={'pop.e5': 'population', 
                              'excess.mean': 'excess mean'})
em_yr = em_yr[em_yr['year'].str.contains('2020-2021')==False]
em_yr['year']=em_yr['year'].astype(int)

em_sex_cols= ['country', 'Nx', 'expected.mean', 'acm.mean', 'type']
em_sex = em_sex.loc[em_sex['iso3'].isin(sa_iso)].drop(em_sex_cols, 
                                                      axis=1).rename(columns={'excess.mean': 
                                                                              'excess mean'})

em_mon_cols = ['country', 'type', 'expected.mean', 'acm.mean', 'cumul.excess.mean', 
               'cumul.excess.low', 'cumul.excess.high']
em_mon = em_mon.drop(em_mon_cols, axis=1).dropna()
em_mon = em_mon.loc[em_mon['iso3'].isin(sa_iso)].rename(columns={'excess.mean': 
                                                                 'excess mean'})
    
crude_cols = ['notes_ids', 'source_id']
crude_death = crude_death.drop(crude_cols, 
                               axis=1).rename(columns={'Years__ESTANDAR': 'year', 'Country__ESTANDAR': 'Country'})


#merging
merge_vax = new_vax.merge(em_mon, 
                          how='outer', on=['iso3', 'year', 'month']).sort_values(by=['iso3', 'year', 'month'])

merge_yr_crude = crude_death.merge(em_yr, how='outer', on=['Country', 'year'])








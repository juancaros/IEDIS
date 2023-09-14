#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
import requests
from pytrends.request import TrendReq
import time

INTEREST_BY_REGION_URL = 'https://trends.google.com/trends/api/widgetdata/comparedgeo'


def interest_by_city(self, inc_low_vol=True, time_frame=None):
    """Request data from Google's Interest by City section and return a dataframe"""

    # make the request
    resolution = 'CITY'
    region_payload = dict()
    self.interest_by_region_widget['request'][
        'resolution'] = resolution

    self.interest_by_region_widget['request'][
        'includeLowSearchVolumeGeos'] = inc_low_vol

    # convert to string as requests will mangle
    region_payload['req'] = json.dumps(
        self.interest_by_region_widget['request'])
    region_payload['token'] = self.interest_by_region_widget['token']
    region_payload['tz'] = self.tz

    # parse returned json
    req_json = self._get_data(
        url=TrendReq.INTEREST_BY_REGION_URL,
        method='get',
        trim_chars=5,
        params=region_payload,
    )
    df = pd.DataFrame(req_json['default']['geoMapData'])
    if (df.empty):
        return df

    # rename the column with the search keyword
    df = df[['geoName', 'coordinates', 'value', 'hasData']].set_index(
        ['geoName']).sort_index()
    # split list columns into separate ones, remove brackets and split on comma
    result_df = df['value'].apply(lambda x: pd.Series(
        str(x).replace('[', '').replace(']', '').split(',')))

    # rename each column with its search term
    for idx, kw in enumerate(self.kw_list):
        result_df[kw] = result_df[idx].astype('int')
        del result_df[idx]
    result_df['time_frame'] = time_frame
    return result_df

def get_interest_by_city_panel(pytrends, kw_list, time_frame):
    # Split the time frame into start and end dates
    start_date, end_date = time_frame.split()

    # Initialize an empty DataFrame to store the results
    panel_df = pd.DataFrame()

    for date in pd.date_range(start=start_date, end=end_date):
        start_date = date.strftime('%Y-%m-%d')
        end_date = (date + pd.DateOffset(days=1)).strftime('%Y-%m-%d')
        current_timeframe = start_date + ' ' + end_date
        
        print(current_timeframe)
        time.sleep(wait)
        pytrends.build_payload(kw_list, cat=0, timeframe=current_timeframe, geo='ES', gprop='')
        city_data = interest_by_city(pytrends, time_frame=current_timeframe)
        panel_df = pd.concat([panel_df, city_data], axis=0)

    return panel_df

panel_data = pd.DataFrame()

pytrends = TrendReq(hl='es', tz=360)
kw_list = ["ansiedad"]

time_frame = '2018-06-01 2018-06-05'
wait = 6

# Get the interest by city panel data
city_panel_data = get_interest_by_city_panel(pytrends, kw_list, time_frame)

# Pivot the data to have cities as columns and dates as rows
city_panel_data_pivoted = city_panel_data.pivot_table(index='time_frame', columns='geoName')

print(city_panel_data_pivoted)

# Exportar el DataFrame a un archivo CSV
city_panel_data_pivoted.to_csv('panel_data.csv')

print("Datos exportados a panel_data.csv")

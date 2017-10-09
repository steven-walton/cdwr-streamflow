import requests
import datetime as dt
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import matplotlib.pyplot as plt


def get_streamflow(station_id, start, end):
    """
    Requests tabular streamflow discharge data from Colorado Department of Water Resources for a
    given station ID over a specified date range. Date range is limited to one year of data.

    Example:
        request_streamflow('BOCOROCO', '2010/01/01', '2011/01/01)

    :param station_id: CWDR Station Abbreviation
    :type station_id: str
    :param start: Start date string in the ISO 8601 format 'YYYY/MM/DD'
    :type start: str
    :param end: End date string in the ISO 8601 format 'YYYY/MM/DD'
    :type end: str
    :return: Pandas DataFrame object
    """

    data = pd.DataFrame()
    url = 'http://www.dwr.state.co.us/SurfaceWater/data/export_tabular.aspx'
    dates = _date_split(start, end)
    for index, date in enumerate(dates[:-1]):
        payload = {'ID': station_id,
                   'MTYPE': 'DISCHRG',
                   'INTERVAL': '1',
                   'START': dates[index],
                   'END': dates[index+1]}
        r = requests.get(url, params=payload)
        rdata = pd.read_csv(StringIO(r.text), sep='\t', skiprows=15)
        data = data.append(rdata)
    data.columns = ['Station', 'Date', 'Discharge']
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.set_index('Date')
    data['Discharge'] = pd.to_numeric(data['Discharge'], errors='coerce')
    return data


def _date_split(start, end):
    """
    Uses a specified start and end date as strings and splits it into a list of dates as strings
    with a maximum difference of 365 days between entries.

    Since tabular CWDR data is limited to a range of one-year, this function is used to split a
    longer request into several, smaller requests.

    :param start: Start date string in ISO 8601 format 'YYYY/MM/DD'
    :type start: str
    :param end: End date string in the ISO 8601 format 'YYYY/MM/DD'
    :type end: str
    :return: List of date strings
    """
    start_date, end_date = dt.datetime.strptime(start, '%Y/%m/%d'),\
                           dt.datetime.strptime(end, '%Y/%m/%d')
    dates = [start_date]
    tdelta = dt.timedelta(days=365)
    while dates[-1] < end_date:
        dates.append(dates[-1] + tdelta)
    dates[-1] = end_date
    return dates

def _get_station_dict():
    url = 'http://www.dwr.state.co.us/SurfaceWater/default.aspx'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    options = soup.find_all('option')
    station_id = [option['value'] for option in options]
    station_name = [option.text for option in options]
    station_dict = dict(zip(station_id, station_name))
    return station_dict


def get_station_list():
    station_dict = _get_station_dict()
    station_list = [station_dict[key] for key in station_dict]
    return station_list


def search_station(string):
    result = None
    station_dict = _get_station_dict()
    for key in station_dict:
        if (string.lower() in station_dict[key].lower()) or (string.lower() in key.lower()):
            result = key
            print(station_dict[key])
    if result is None:
        print(f'No results found for {string}')
    return result


def plot_ts(data, ax=None, fig=None, fig_kwargs=None):

    # Grab station information to use in plot title
    station_id = data['Station'][0]
    station_dict = _get_station_dict()
    station_name = station_dict[station_id]

    # Create figure and/or axis if no existing figure/axis objects are passed
    if fig_kwargs is None:
        fig_kwargs = dict(figsize=(11, 8.5))

    if fig is None:
        fig = plt.figure(**fig_kwargs)

    if ax is None:
        ax = fig.add_subplot(1, 1, 1)

    # Plot on axis
    ax.plot(data.index, data['Discharge'])
    ax.set_ylim([0, 1.2*data['Discharge'].max()])
    ax.set_xlabel('Date')
    ax.set_ylabel('Discharge (cfs)')
    ax.set_title(station_name)
    return fig, ax

# Test
# data = request_streamflow('BOCOROCO', '2010/01/01', '2010/02/01')
# fig, ax = plot_ts(data)
# plt.show()
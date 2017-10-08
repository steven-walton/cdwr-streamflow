import requests
import datetime as dt
import pandas as pd
from io import StringIO

def request_streamflow(station_id, start, end):
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

df = request_streamflow('BOCOROCO', '2010/01/01', '2015/06/01')
print(df)
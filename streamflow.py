import requests
from datetime import datetime


def request_streamflow(station_id, start, end):
    """
    Requests tabular streamflow discharge data from Colorado Department of Water Resources for a given station ID
    over a specified date range. Date range is limited to one year of data.

    Example:
        request_streamflow('BOCOROCO', '2010/01/01', '2011/01/01)

    :param station_id: CWDR Station Abbreviation
    :type station_id: str
    :param start: Start date string in the ISO 8601 format 'YYYY/MM/DD'
    :type start: str
    :param end: End date string in the ISO 8601 format 'YYYY/MM/DD'
    :type end: str
    :return:
    """


def _date_split(start, end):
    """
    Uses a specified start and end date as strings and splits it into a list of dates as strings with
    difference of 365 days between entries.

    Since tabular CWDR data is limited to a range of one-year, this function is used to split a longer
    request into several, smaller requests.

    :param start: Start date string in ISO 8601 format 'YYYY/MM/DD'
    :type start: str
    :param end: End date string in the ISO 8601 format 'YYYY/MM/DD'
    :type end: str
    :return: List of date strings
    """
    start_date, end_date = datetime.strptime(start, '%Y/%m/%d'), datetime.strptime(end, '%Y/%m/%d')


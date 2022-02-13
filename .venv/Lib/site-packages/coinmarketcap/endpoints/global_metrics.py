# -*- coding: utf-8 -*-

from .parser import args
from os.path import join as urljoin


class Quotes:
    """ Get the latest or historic quote of aggregated market metrics. """

    def __init__(self, request, endpoint):
        self.request = lambda x, y: request(
            urljoin(endpoint, "quotes", x), args(**y))

    def historical(
        self, time_start=None, time_end=None, count=10, interval="1d", convert="USD"
    ):
        """ Get an interval of aggregate 24 hour volume and market cap data
        globally based on time and interval parameters.

        Notes
        -----
        * A historic quote for every "interval" period between your "time_start"
        and "time_end" will be returned.
        * If a "time_start" is None, the "interval" will be applied in
        reverse from "time_end".
        * If "time_end" is not supplied, it defaults to the current time.
        * At each "interval" period, the historic quote that is closest in time to
        the requested time will be returned.
        * If no historic quotes are available in a given "interval" period up
        until the next interval period, it will be skipped.

        Parameters
        ----------
        time_start : `datetime.datetime` or `float`, optional
            Timestamp (datetime obj or Unix) to start returning quotes for.
            Optional, if none is passed it return quotes calculated in
            reverse from "time_end".
        time_end : `datetime.datetime` or `float`, optional
            Timestamp (datetime obj or Unix) to stop returning quotes for
            (inclusive). Optional, if None is passed, it defaults to current
            time. If "time_start" is None, it return quotes in reverse order
            starting from this time.
        count : `int`, optional
            The number of interval periods to return results for. Optional,        Request()

            required if both "time_start" and "time_end" aren't supplied.
            The default is 10 items. The current query limit is 10000.
        interval : `str`, optional
            Interval of time to return data points for.
            Supported minutes intervals: {"5m", "10m", "15m", "30m", "45m"}.
            Supported hour intervals: {"1h", "2h", "3h", "6h", "12h"}.
            Supported day intervals: {"1d", "2d", "3d", "7d", "14d", "15d",
            "30d", "60d", "90d", "365d"}.
            Other supported time periods: {"hourly", "daily", "weekly",
            "monthly", "yearly"}.
        convert : `str`, optional
            Calculate market quotes in another fiat currency or cryptocurrency..
            A list of supported fiat options can be found here.
            https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1GlobalmetricsQuotesHistorical

        Raises
        ------
        ValueError
            If arguments are not parseable

        requests.exceptions.HTTPError
            If status code is not 200
        """
        params = locals()
        if time_start is None:
            del params["time_start"]
        if time_end is None:
            del params["time_end"]

        return self.request("historical", params)

    def latest(self, convert="USD"):
        """ Get the latest quote of aggregate market metrics. Use the
        "convert" argument to return market values in multiple fiat and
        cryptocurrency conversions in the same call.

        Parameters
        ----------
        convert : `str` or `list` of `str`, optional
            Calculate market quotes in up to 40 currencies at once. Each
            additional convert option beyond the first requires an additional
            call credit. Each conversion is returned in its own "quote"
            object. A list of supported fiat options can be found here.
            https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1GlobalmetricsQuotesLatest

        Raises
        ------
        ValueError
            If argument is not parseable.

        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request("latest", locals())


class GlobalMetrics:
    """ API for global aggregated market data."""

    def __init__(self, request):
        args = (request, "global-metrics")
        self.quotes = Quotes(*args)

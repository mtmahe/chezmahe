# -*- coding: utf-8 -*-

from .parser import args
from typing import Union
from os.path import join as urljoin


class Info:
    """ Returns all static metadata for one or more exchanges including logo
    and homepage URL."""

    def __init__(self, request, endpoint):
        self.request = lambda x: request(urljoin(endpoint, "info"), args(**x))

    def ids(self, id: Union[list, str, int]):
        """ Returns all static metadata for one or more exchanges including
        logo and homepage URL.

        Parameters
        ----------
        id : `int`, `str` or `list` of `str` or `int`
            One or a list of CoinMarketCap cryptocurrency exchange ids.
            Example: [1, 2]

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1ExchangeInfo

        Raises
        ------
        ValueError
            If argument is not parseable.
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request(locals())

    def slugs(self, slug: Union[list, str]):
        """ Returns all static metadata for one or more exchanges including
        logo and homepage URL.

        Parameters
        ----------
        slug : `str` or `list` of `str`
            One or a list of exchanges slug (lowercase name with spaces
            replaced with dashes). Example: ["binance", "bittrex"]

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1ExchangeInfo

        Raises
        ------
        ValueError
            If argument is not parseable.
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request(locals())


class Map:
    """ Returns a list of all cryptocurrency exchanges by CoinMarketCap ID.
    It is recommended to use this endpoint to lookup and utilize exchange id
    across all endpoints as typical exchange identifiers may change over time.
    """

    def __init__(self, request, endpoint):
        self.request = lambda x: request(urljoin(endpoint, "map"), x)

    def active_start(self, start=1, limit=100):
        """ Returns a list of all cryptocurrency exchanges by CoinMarketCap ID.
        It is recommended to use this endpoint to lookup and utilize exchange
        id across all endpoints as typical exchange identifiers may change
        over time.

        Parameters
        ----------
        start : `int`, optional
            Start (1-based index) of the list of items to return.
        limit : `int`, optional
            Specify the number of results to return. Use this parameter to
            determine the list size.

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1ExchangeMap

        Raises
        ------
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request(args(**locals()))

    def active_slugs(self, slug: Union[list, str]):
        """ Returns a list of all cryptocurrency exchanges by CoinMarketCap ID.
        It is recommended to use this endpoint to lookup and utilize exchange
        id across all endpoints as typical exchange identifiers may change
        over time.

        Parameters
        ----------
        slug : `str` or `list` of `str`
            One or a list of exchanges slug (lowercase name with spaces
            replaced with dashes). Example: ["binance", "bittrex"]

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1ExchangeMap

        Raises
        ------
        ValueError
            If argument is not parseable.
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request(args(**locals()))

    def inactive(self):
        """ List over inactive exchanges.

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1ExchangeMap

        Raises
        ------
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request({"listing_status": "inactive"})


class Listings:
    """ Get a list of all cryptocurrency exchanges with latest or historical
    market data.
    """

    def __init__(self, request, endpoint):
        self.request = lambda x, y: request(
            urljoin(endpoint, "listings", x), args(**y))

    def historical_start(self):
        """ Get a list of all cryptocurrency exchanges with historical market
        data for a given point in time.

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1ExchangeListingsHistorical

        Raises
        ------
        NotImplementedError
            This endpoint is not yet available. It is slated for release in
            Q1 2019.
        """
        raise NotImplementedError

    def latest_start(
        self,
        start=1,
        limit=100,
        sort="volume_24h",
        sort_dir="desc",
        market_type="all",
        convert="USD",
    ):
        """
        Get a list of all cryptocurrency exchanges including the latest
        aggregate market data for each exchange.

        Notes
        -----
        * Use the "convert" option to return market values in multiple fiat
        and cryptocurrency conversions in the same call.
        * Use this endpoint if you need a sorted and a list of exchanges. If
        you want to query for market data on a few specific exchanges use
        quotes/latest which is optimized for that purpose. The response data
        between these endpoints is otherwise the same.

        Parameters
        ----------
        start : `int`, optional
            Start (1-based index) of the list of items to return.
        limit : `int`, optional
            Specify the number of results to return. Use this parameter to
            determine the list size.
        sort : `str`, optional
            What field to sort the list of exchanges by.
            Supported values: {"name", "volume_24h", "volume_24h_adjusted"}.
        sort_dir : `str`, optional
            The direction in which to order exchanges against the specified
            sort. Supported values: {"asc" ,"desc"}.
        market_type : `str`, optional
            The type of exchange markets to include in rankings. This field
            is deprecated. Please use "all" for accurate sorting.
            Supported values: {"fees", "no_fees", "all"}.
        convert : `str` or `list` of `str`, optional
            Calculate market quotes in up to 40 currencies at once. Each
            additional convert option beyond the first requires an additional
            call credit. Each conversion is returned in its own "quote"
            object. A list of supported fiat options can be found here.
            https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1ExchangeListingsLatest

        Raises
        ------
        ValueError
            If arguments are not parseable
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request("latest", locals())


class Pairs:
    """
    Get a list of active market pairs for an exchange. Active means the market
    pair is open for trading.
    """

    def __init__(self, request, endpoint):
        self.request = lambda x: request(
            urljoin(endpoint, "market-pairs/latest"), args(**x)
        )

    def id(self, id: Union[list, str, int], start=1, limit=100, convert="USD"):
        """ Get a list of active market pairs for an exchange. Active means
        the market pair is open for trading

        Parameters
        ----------
        id : `int` or `str`
            A CoinMarketCap exchange ID. Example: 1
        start : `int`, optional
            Start (1-based index) of the list of items to return.
        limit : `int`, optional
            Specify the number of results to return. Use this parameter to
            determine the list size.
        convert : `str` or `list` of `str`, optional
            Calculate market quotes in up to 40 currencies at once. Each
            additional convert option beyond the first requires an additional
            call credit. Each conversion is returned in its own "quote"
            object. A list of supported fiat options can be found here.
            https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1ExchangeMarketpairsLatest

        Raises
        ------
        ValueError
            If arguments are not parseable
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request(locals())

    def slug(self, slug: Union[list, str], start=1, limit=100, convert="USD"):
        """ Get a list of active market pairs for an exchange. Active means
        the market pair is open for trading

        Parameters
        ----------
        slug : `str`
            A slug (lowercase name with spaces replaced with dashes).
            Example: "binance".
        start : `int`, optional
            Start (1-based index) of the list of items to return.
        limit : `int`, optional
            Specify the number of results to return. Use this parameter to
            determine the list size.
        convert : `str` or `list` of `str`, optional
            Calculate market quotes in up to 40 currencies at once. Each
            additional convert option beyond the first requires an additional
            call credit. Each conversion is returned in its own "quote"
            object. A list of supported fiat options can be found here.
            https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1ExchangeMarketpairsLatest

        Raises
        ------
        ValueError
            If arguments are not parseable
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request(locals())


class Quotes:
    """ Returns an interval of latest and historic quotes for any exchange
    based on time and interval parameters."""

    def __init__(self, request, endpoint):
        self.request = lambda x, y: request(
            urljoin(endpoint, "quotes", x), args(**y))

    def historical_id(
        self,
        id: Union[str, int],
        time_start=None,
        time_end=None,
        count=10,
        interval="5m",
        convert="USD",
    ):
        """ Returns an interval of historic quotes for any exchange based on
        time and interval parameters.

        Notes
        -----
        * A historic quote for every "interval" period between your
        "time_start" and "time_end" will be returned.
        * If a "time_start" is not supplied, the "interval" will be
        applied in reverse from "time_end".
        * If "time_end" is not supplied, it defaults to the current time.
        * At each "interval" period, the historic quote that is closest in
        time to the requested time will be returned.
        * If no historic quotes are available in a given "interval" period up
        until the next interval period, it will be skipped.

        Parameters
        ----------
        id : `int`
            A CoinMarketCap exchange ID. Example: 1.
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
            The number of interval periods to return results for. Optional,
            required if both "time_start" and "time_end" aren't supplied.
            The default is 10 items. The current query limit is 10000.
        interval : `int`, optional
            Interval of time to return data points for.
            Supported minutes intervals: {"5m", "10m", "15m", "30m", "45m"}.
            Supported hour intervals: {"1h", "2h", "3h", "6h", "12h"}.
            Supported day intervals: {"1d", "2d", "3d", "7d", "14d", "15d",
            "30d", "60d", "90d", "365d"}.
            Other supported time periods: {"hourly", "daily", "weekly",
            "monthly", "yearly"}.
        convert : `str`, optional
            Calculate market quotes in another fiat currency or cryptocurrency.
            A list of supported fiat options can be found here.
            https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1ExchangeQuotesHistorical

        Raises
        ------
        requests.exceptions.HTTPError
            If status code is not 200
        """
        params = locals()
        if time_start is None:
            del params["time_start"]
        if time_end is None:
            del params["time_end"]

        return self.request("historical", params)

    def historical_slug(
        self,
        slug: str,
        time_start: None,
        time_end: None,
        count=10,
        interval="5m",
        convert="USD",
    ):
        """ Returns an interval of historic quotes for any exchange based on
        time and interval parameters.

        Notes
        -----
        * A historic quote for every "interval" period between your
        "time_start" and "time_end" will be returned.
        * If a "time_start" is not supplied, the "interval" will be
        applied in reverse from "time_end".
        * If "time_end" is not supplied, it defaults to the current time.
        * At each "interval" period, the historic quote that is closest in
        time to the requested time will be returned.
        * If no historic quotes are available in a given "interval" period up
        until the next interval period, it will be skipped.

        Parameters
        ----------
        slug : `str`
            A slug (lowercase name with spaces replaced with dashes).
            Example: "binance".
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
            The number of interval periods to return results for. Optional,
            required if both "time_start" and "time_end" aren't supplied.
            The default is 10 items. The current query limit is 10000.
        interval : `int`, optional
            Interval of time to return data points for.
            Supported minutes intervals: {"5m", "10m", "15m", "30m", "45m"}.
            Supported hour intervals: {"1h", "2h", "3h", "6h", "12h"}.
            Supported day intervals: {"1d", "2d", "3d", "7d", "14d", "15d",
            "30d", "60d", "90d", "365d"}.
            Other supported time periods: {"hourly", "daily", "weekly",
            "monthly", "yearly"}.
        convert : `str`, optional
            Calculate market quotes in another fiat currency or cryptocurrency.
            A list of supported fiat options can be found here.
            https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1ExchangeQuotesHistorical

        Raises
        ------
        requests.exceptions.HTTPError
            If status code is not 200
        """
        params = locals()
        if time_start is None:
            del params["time_start"]
        if time_end is None:
            del params["time_end"]
        return self.request("historical", locals())

    def latest_ids(self, id: Union[list, str, int], convert="USD"):
        """ Get the latest aggregate market data for exchanges.

        Parameters
        ----------
        id : `int`, `str` or `list` of `str` or `int`
            One or a list of CoinMarketCap cryptocurrency exchange ids.
            Example: [1, 2]
        convert : `str` or `list` of `str`, optional
            Calculate market quotes in up to 40 currencies at once. Each
            additional convert option beyond the first requires an additional
            call credit. Each conversion is returned in its own "quote"
            object. A list of supported fiat options can be found here.
            https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1ExchangeQuotesLatest

        Raises
        ------
        ValueError
            If arguments are not parseable
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request("latest", locals())

    def latest_slugs(self, slug: Union[list, str], convert="USD"):
        """ Get the latest aggregate market data for exchanges.

        Parameters
        ----------
        slug : `str` or `list` of `str`
            One or a list of exchanges slug (lowercase name with spaces
            replaced with dashes). Example: ["binance", "bittrex"]
        convert : `str` or `list` of `str`, optional
            Calculate market quotes in up to 40 currencies at once. Each
            additional convert option beyond the first requires an additional
            call credit. Each conversion is returned in its own "quote"
            object. A list of supported fiat options can be found here.
            https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1ExchangeQuotesLatest

        Raises
        ------
        ValueError
            If arguments are not parseable
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request("latest", locals())


class Exchange:
    def __init__(self, request):
        args = (request, "exchange")
        self.info = Info(*args)
        self.map = Map(*args)
        self.listings = Listings(*args)
        self.pairs = Pairs(*args)
        self.quotes = Quotes(*args)

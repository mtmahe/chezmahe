# -*- coding: utf-8 -*-

from os.path import join as urljoin
from typing import Union
import datetime

# local
from .parser import args


class Info:
    """ Returns all static metadata for one or more cryptocurrencies including
    name, symbol, logo, and its various registered URLs.
    """

    def __init__(self, request, endpoint):
        self.request = lambda x: request(urljoin(endpoint, "info"), args(**x))

    def ids(self, id: Union[list, str, int]):
        """ Returns all static metadata for one or more cryptocurrencies
        including name, symbol, logo, and its various registered URLs.

        Parameters
        ----------
        id : `int`, `str` or `list` of `str` or `int`
            One or a list of CoinMarketCap cryptocurrency ids.
            Example: [1, 2]

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyInfo

        Raises
        ------
        ValueError
            If argument is not parseable.
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request(locals())

    def symbols(self, symbol: Union[list, str]):
        """ Returns all static metadata for one or more cryptocurrencies
        including name, symbol, logo, and its various registered URLs.

        Parameters
        ----------
        symbol : `str` or `list` of `str`
            One or a list of cryptocurrency symbols. Example: ["BTC", "ETH"].

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyInfo

        Raises
        ------
        ValueError
            If argument is not parseable.
        requests.exceptions.HTTPError
            If status code is not 200

        """
        return self.request(locals())


class Map:
    """ Returns a list of all cryptocurrencies by CoinMarketCap ID. It is
    recommended to use endpoint to lookup and utilize unique cryptocurrency
    id across all endpoints as typical identifiers like ticker symbols can
    match multiple cryptocurrencies and change over time.
    """

    def __init__(self, request, endpoint):
        self.request = lambda x: request(urljoin(endpoint, "map"), x)

    def active_start(self, start=1, limit=100):
        """ Returns a list of all active cryptocurrencies by CoinMarketCap ID.
        It is recommended to use endpoint to lookup and utilize unique
        cryptocurrency id across all endpoints as typical identifiers like
        ticker symbols can match multiple cryptocurrencies and change over
        time.

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
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyMap

        Raises
        ------
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request(args(**locals()))

    def active_symbols(self, symbol: Union[list, str]):
        """ Returns a list of all active cryptocurrencies by CoinMarketCap ID.
        It is recommended to use endpoint to lookup and utilize unique
        cryptocurrency id across all endpoints as typical identifiers like
        ticker symbols can match multiple cryptocurrencies and change over
        time.

        Parameters
        ----------
        symbol : `str` or `list` of `str`
            One or a list of cryptocurrency symbols. Example: ["BTC", "ETH"].

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyMap

        Raises
        ------
        ValueError
            If argument is not parseable.
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request(args(**locals()))

    def inactive(self):
        """ Returns a list of all inactive cryptocurrencies by
        CoinMarketCap ID.

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyMap

        Raises
        ------
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request({"listing_status": "inactive"})


class Listings:
    """ Get a list of all cryptocurrencies with market data for a latest or
    given historical time.
    """

    def __init__(self, request, endpoint):
        self.request = lambda x, y: request(
            urljoin(endpoint, "listings", x), args(**y))

    def historical_start(self):
        """ Get a list of all cryptocurrencies with market data for a given
        historical time.

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyListingsHistorical

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
        convert="USD",
        sort="market_cap",
        sort_dir="desc",
        cryptocurrency_type="all",
    ):
        """ Get a list of all cryptocurrencies with latest market data.

        Parameters
        ----------
        start : `int`, optional
            Start (1-based index) of the list of items to return.
        limit : `int`, optional
            Specify the number of results to return. Use this parameter to
            determine the list size.
         convert : `str` or `list` of `str`
            Calculate market quotes in up to 40 currencies at once. Each
            additional convert option beyond the first requires an additional
            call credit. Each conversion is returned in its own "quote"
            object. A list of supported fiat options can be found here.
            https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions
        sort : `str`, optional
            What field to sort the list of cryptocurrencies by.
            Supported values: {"name", "symbol", "date_added", "marekt_cap",
            "price", "circulating_supply", "total_supply", "max_supply",
            "num_market
            _pairs", "volume_24h", "percent_change_1h",
            "percent_change_24h", "percent_change_7d"}.
        sort_dir : `str`, optional
            The direction in which to order cryptocurrencies against the
            specified sort. Valid values: {"asc", "desc"}.
        cryptocurrency_type : `str`, optional
            The type of cryptocurrency to include. Valid values: {"all",
            "coins", "tokens"}.

        Returns
        -------
        json object
            Respone schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyListingsLatest

        Raises
        ------
        ValueError
            If arguments are not parseable
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request("latest", locals())


class Pairs:
    """ Lists all market pairs across all exchanges for the specified
    cryptocurrency with associated stats. Use the "convert" option to return
    market values in multiple fiat and cryptocurrency conversions in the same
    call.
    """

    def __init__(self, request, endpoint):
        self.request = lambda x: request(
            urljoin(endpoint, "market-pairs/latest"), args(**x)
        )

    def id(self, id: Union[str, int], start=1, limit=100, convert="USD"):
        """ Lists all market pairs across all exchanges for the specified
        cryptocurrency with associated stats. Use the "convert" option to
        return market values in multiple fiat and cryptocurrency conversions
        in the same call.

        Parameters
        ----------
        id : `int` or `str`
            A CoinMarketCap cryptocurrency ids. Example: 1
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
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyMarketpairsLatest

        Raises
        ------
        ValueError
            If arguments are not parseable
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request(locals())

    def symbol(self, symbol: str, start=1, limit=100, convert="USD"):
        """ Lists all market pairs across all exchanges for the specified
        cryptocurrency with associated stats. Use the "convert" option to
        return market values in multiple fiat and cryptocurrency conversions
        in the same call.

        Parameters
        ----------
        symbol : `str`
            A cryptocurrency symbol. Example: "BTC".
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
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyMarketpairsLatest

        Raises
        ------
        ValueError
            If arguments are not parseable
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request(locals())


class Ohlcv:
    """ Return historical and latest OHLCV (Open, High, Low, Close, Volume) data
    along with market cap for any cryptocurrency using time interval
    parameters. Currently daily and hourly OHLCV periods are supported.
    Volume is only supported with daily periods at this time.
    """

    def __init__(self, request, endpoint):
        self.request = lambda x, y: request(
            urljoin(endpoint, "ohlcv", x), args(**y))

    def historical_id(
        self,
        id: Union[str, int],
        time_start=None,
        time_end=None,
        time_period="daily",
        count=10,
        interval="daily",
        convert="USD",
    ):
        """Return historical OHLCV (Open, High, Low, Close, Volume) data along
        with market cap for any cryptocurrency using time interval parameters.
        Currently daily and hourly OHLCV periods are supported. Volume is only
        supported with daily periods at this time.

        Notes
        -----
        * Only the date portion of the timestamp is used for daily OHLCV so
        it's recommended to send an ISO date format like "2018-09-19" without
        time for this "time_period".
        * One OHLCV quote will be returned for every "time_period" between
        your "time_start" (exclusive) and "time_end" (inclusive).
        * If a "time_start" is `None`, the "time_period" will be
        calculated in reverse from "time_end" using the "count" parameter
        which defaults to 10 results.
        * If "time_end" is `None`, it defaults to the current time.
        * If you don't need every "time_period" between your dates you may
        adjust the frequency that "time_period" is sampled using the
        "interval" parameter. For example with "time_period" set to "daily"
        you may set "interval" to "2d" to get the daily OHLCV for every other
        day. You could set "interval" to "monthly" to get the first daily
        OHLCV for each month, or set it to "yearly" to get the daily OHLCV
        value against the same date every year.

        Parameters
        ----------
        id : `int` or `str`
            A CoinMarketCap cryptocurrency ids. Example: 1
        time_start : `datetime.datetime`, `float` or `str`, optional
            Timestamp (datetime, Unix, ISO 8601 str) to start returning OHLCV
            time periods for. Only the date portion of the timestamp is used
            for daily OHLCV.
        time_end : `datetime.datetime`, `float` or `str`, optional
            Timestamp (datetime, Unix, ISO 8601 str) to stop returning OHLCV
            time periods for (inclusive). Optional, if not passed we'll
            default to the current time. Only the date portion of the
            timestamp is used for daily OHLCV.
        time_period : `str`
            Time period to return OHLCV data for.
            Valid values: {"daily", "hourly"}.
        count : `int`, optional
            Limit the number of time periods to return results for. The
            cucount : `int`, optional
            Limit the number of time periods to return results for. The
            current query limit is 10000 items.rrent query limit is 10000
            items.
        interval : `str`, optional
            Adjust the interval that "time_period" is sampled.
            Valid values: {"hourly", "daily", "weekly", "monthly", "yearly",
            "1h", "2h", "3h", "4h", "6h", "12h", "1d", "2d", "3d", "7d", "14d",
            "15d", "30d", "60d", "90d", "365d"}
        convert : `str`, optional
            Calculate market quotes in another fiat currency or cryptocurrency.
            A list of supported fiat options can be found here.
            https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyOhlcvHistorical

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

    def historical_symbol(
        self,
        symbol: str,
        time_start=None,
        time_end=None,
        time_period="daily",
        count=10,
        interval="daily",
        convert="USD",
    ):
        """Return historical OHLCV (Open, High, Low, Close, Volume) data along
        with market cap for any cryptocurrency using time interval parameters.
        Currently daily and hourly OHLCV periods are supported. Volume is only
        supported with daily periods at this time.

        Notes
        -----
        * Only the date portion of the timestamp is used for daily OHLCV so
        it's recommended to send an ISO date format like "2018-09-19" without
        time for this "time_period".
        * One OHLCV quote will be returned for every "time_period" between
        your "time_start" (exclusive) and "time_end" (inclusive).
        * If a "time_start" is `None`, the "time_period" will be
        calculated in reverse from "time_end" using the "count" parameter
        which defaults to 10 results.
        * If "time_end" is `None`, it defaults to the current time.
        * If you don't need every "time_period" between your dates you may
        adjust the frequency that "time_period" is sampled using the
        "interval" parameter. For example with "time_period" set to "daily"
        you may set "interval" to "2d" to get the daily OHLCV for every other
        day. You could set "interval" to "monthly" to get the first daily
        OHLCV for each month, or set it to "yearly" to get the daily OHLCV
        value against the same date every year.

        Parameters
        ----------
        symbol : `str`
            A cryptocurrency symbols. Example: "BTC".
        time_start : `datetime.datetime`, `float` or `str`, optional
            Timestamp (datetime, Unix, ISO 8601 str) to start returning OHLCV
            time periods for. Only the date portion of the timestamp is used
            for daily OHLCV.
        time_end : `datetime.datetime`, `float` or `str`, optional
            Timestamp (datetime, Unix, ISO 8601 str) to stop returning OHLCV
            time periods for (inclusive). Optional, if not passed we'll
            default to the current time. Only the date portion of the
            timestamp is used for daily OHLCV.
        time_period : `str`
            Time period to return OHLCV data for.
            Valid values: {"daily", "hourly"}.
        count : `int`, optional
            Limit the number of time periods to return results for. The
            current query limit is 10000 items.
        interval : `str`, optional
            Adjust the interval that "time_period" is sampled.
            Valid values: {"hourly", "daily", "weekly", "monthly", "yearly",
            "1h", "2h", "3h", "4h", "6h", "12h", "1d", "2d", "3d", "7d", "14d",
            "15d", "30d", "60d", "90d", "365d"}
        convert : `str`, optional
            Calculate market quotes in another fiat currency or cryptocurrency.
            A list of supported fiat options can be found here.
            https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyOhlcvHistorical

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

    def latest_ids(self, id: Union[list, str, int], convert="USD"):
        """ Return the latest OHLCV (Open, High, Low, Close, Volume) market
        values for one or more cryptocurrencies for the current UTC day. Since
        the current UTC day is still active these values are updated
        frequently. You can find the final calculated OHLCV values for the
        last completed UTC day along with all historic days using
        /cryptocurrency/ohlcv/historical.

        Parameters
        ----------
        id : `int`, `str` or `list` of `str` or `int`
            One or a list of CoinMarketCap cryptocurrency ids.
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
            Schema -  https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyOhlcvLatest

        Raises
        ------
        ValueError
            If arguments are not parseable
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request("latest", locals())

    def latest_symbols(self, symbol: Union[list, str], convert="USD"):
        """ Return the latest OHLCV (Open, High, Low, Close, Volume) market
        values for one or more cryptocurrencies for the current UTC day. Since
        the current UTC day is still active these values are updated
        frequently. You can find the final calculated OHLCV values for the
        last completed UTC day along with all historic days using
        /cryptocurrency/ohlcv/historical.

        Parameters
        ----------
        symbol : `str` or `list` of `str`
            One or a list of cryptocurrency symbols. Example: ["BTC", "ETH"].
        convert : `str` or `list` of `str`, optional
            Calculate market quotes in up to 40 currencies at once. Each
            additional convert option beyond the first requires an additional
            call credit. Each conversion is returned in its own "quote"
            object. A list of supported fiat options can be found here.
            https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions

        Returns
        -------
        `json obj`
            Schema -  https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyOhlcvLatest

        Raises
        ------
        ValueError
            If arguments are not parseable
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request("latest", locals())


class Quotes:
    """ Returns an interval of latest and historic market quotes for any
    cryptocurrency based on time and interval parameters.
    """

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
        """ Returns an interval of historic market quotes for any
        cryptocurrency based on tuime and interval parameters.

        Notes
        -----
        * A historic quote for every "interval" period between your
        "time_start" and "time_end" will be returned.
        * If a "time_start" is None, the "interval" will be applied in reverse
        from "time_end".
        * If "time_end" is `None`, it defaults to the current time.
        * At each "interval" period, the historic quote that is closest in
        time to the requested time will be returned.
        * If no historic quotes are available in a given "interval" period up
        until the next interval period, it will be skipped.

        Parameters
        ----------
        id : `int` or `str`
            A CoinMarketCap cryptocurrency ids. Example: 1
        time_start : `datetime.datetime`, `float` or `str`, optional
            Timestamp (datetime, Unix, ISO 8601 str) to start returning OHLCV
            time periods for. Only the date portion of the timestamp is used
            for daily OHLCV.
        time_end : `datetime.datetime`, `float` or `str`, optional
            Timestamp (datetime, Unix, ISO 8601 str) to stop returning OHLCV
            time periods for (inclusive). Optional, if not passed we'll
            default to the current time. Only the date portion of the
            timestamp is used for daily OHLCV.
        count : `int`, optional
            Limit the number of time periods to return results for. The
            current query limit is 10000 items.
        interval : `str`, optional
            Interval of time to return data points for.
            Valid values: {"yearly", "monthly", "weekly", "daily", "hourly",
            "5m", "10m", "15m", "30m", "45m", "1h", "2h", "3h", "6h", "12h",
            "24h", "1d", "2d", "3d", "7d", "14d", "15d", "30d", "60d", "90d",
            "365d"}.
        convert : `str`, optional
            Calculate market quotes in another fiat currency or cryptocurrency.
            A list of supported fiat options can be found here.
            https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyQuotesHistorical

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

    def historical_symbol(
        self,
        symbol: str,
        time_start=None,
        time_end=None,
        count=10,
        interval="daily",
        convert="USD",
    ):
        """ Returns an interval of historic market quotes for any
        cryptocurrency based on tuime and interval parameters.

        Notes
        -----
        * A historic quote for every "interval" period between your
        "time_start" and "time_end" will be returned.
        * If a "time_start" is None, the "interval" will be applied in reverse
        from "time_end".
        * If "time_end" is `None`, it defaults to the current time.
        * At each "interval" period, the historic quote that is closest in
        time to the requested time will be returned.
        * If no historic quotes are available in a given "interval" period up
        until the next interval period, it will be skipped.

        Parameters
        ----------
        symbol : `str`
            A cryptocurrency symbols. Example: "BTC".
        time_start : `datetime.datetime`, `float` or `str`, optional
            Timestamp (datetime, Unix, ISO 8601 str) to start returning OHLCV
            time periods for. Only the date portion of the timestamp is used
            for daily OHLCV.
        time_end : `datetime.datetime`, `float` or `str`, optional
            Timestamp (datetime, Unix, ISO 8601 str) to stop returning OHLCV
            time periods for (inclusive). Optional, if not passed we'll
            default to the current time. Only the date portion of the
            timestamp is used for daily OHLCV.
        count : `int`, optional
            Limit the number of time periods to return results for. The
            current query limit is 10000 items.
        interval : `str`, optional
            Interval of time to return data points for.
            Valid values: {"yearly", "monthly", "weekly", "daily", "hourly",
            "5m", "10m", "15m", "30m", "45m", "1h", "2h", "3h", "6h", "12h",
            "24h", "1d", "2d", "3d", "7d", "14d", "15d", "30d", "60d", "90d",
            "365d"}.
        convert : `str`, optional
            Calculate market quotes in another fiat currency or cryptocurrency.
            A list of supported fiat options can be found here.
            https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyQuotesHistorical

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

    def latest_ids(self, id: Union[list, str, int], convert="USD"):
        """
        Parameters
        ----------
        id : `int`, `str` or `list` of `str` or `int`
            One or a list of CoinMarketCap cryptocurrency ids.
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
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyQuotesLatest

        Raises
        ------
        ValueError
            If arguments are not parseable
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request("latest", locals())

    def latest_symbols(self, symbol: Union[list, str], convert="USD"):
        """
        Parameters
        ----------
        symbol : `str` or `list` of `str`
            One or a list of cryptocurrency symbols. Example: ["BTC", "ETH"].
        convert : `str` or `list` of `str`, optional
            Calculate market quotes in up to 40 currencies at once. Each
            additional convert option beyond the first requires an additional
            call credit. Each conversion is returned in its own "quote"
            object. A list of supported fiat options can be found here.
            https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions

        Returns
        -------
        `json obj`
            Schema - https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyQuotesLatest

        Raises
        ------
        ValueError
            If arguments are not parseable
        requests.exceptions.HTTPError
            If status code is not 200
        """
        return self.request("latest", locals())


class Cryptocurrency:
    def __init__(self, request):
        args = (request, "cryptocurrency")
        self.info = Info(*args)
        self.map = Map(*args)
        self.pairs = Pairs(*args)
        self.listings = Listings(*args)
        self.ohlcv = Ohlcv(*args)
        self.quotes = Quotes(*args)

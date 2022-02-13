# -*- coding: utf-8 -*-

from requests import Request
from json import loads
from os.path import join as urljoin
from requests.exceptions import HTTPError

# local
from .endpoints import Cryptocurrency, Exchange, GlobalMetrics, Tools
from .environment import Sandbox, Production, Throttler


class Client(Sandbox, Production):
    """ Client allows you to request all CoinMarketCap's endpoints ->
    cryptocurrency, exchange, global-metrics and tools.

    You need an API key to the CoinMarketCap API, see the parameter section on
    how to load your key. The Client also supports throttling of requests and
    a sandbox environment. If you want to specify your own requests, use the
    "request method".

    Parameters
    ----------
    apikey : `str`, optional
        The API key to CoinMarketCap can be loaded in several ways.
        1. passed as argument
        2. try to laod $HOME/.coinmarketcap.json. keys are:
        {"sandbox": "API_KEY", "production": "API_KEY"}
        3. check COINMARKETCAP_{SANDBOX or PRODUCTION} environment variables.
    expire : `int`, optional
        Seconds for cached requests to be removed.
    sandbox : `bool`, optional
        Init coinmarketcap sandbox environment.
    throttle : `str`, optional
        Throttle coinmarketcap requests are a bit weird due to their
        levels of requests limitations.
        Valid values: {"minute", "daily", "monthly"}
    plan : `str`, optional
        Since the API do not provide any metadata regarding accounts,
        you need to pass the correct plan if and only if throttling of
        requests are activated.
        Valid values: {"basic", "hobbyist", "startup", "standard",
        "professional", "enterprise"}. If you have passed the "enterprise",
        be sure to set your own params for requests using the method "plan".
    block : `str`, optional
        block if the request limit is exceeded.

    Raises
    ------
    ValueError
        If one of the arguments could not be parsed.

    """

    def __init__(
        self,
        apikey=None,
        expire=3600,
        plan="basic",
        sandbox=False,
        throttle=None,
        block=True,
    ):
        if sandbox:
            Sandbox.__init__(self, apikey, expire)
        else:
            Production.__init__(self, apikey, expire)

        self.cryptocurrency = Cryptocurrency(self.request)
        self.global_metrics = GlobalMetrics(self.request)
        self.exchange = Exchange(self.request)
        self.tools = Tools(self.request)
        self._throttler = Throttler(plan, throttle, block)

    def request(self, urn: str, params: dict):
        """ Send a request to CoinMarketCap

        Parameters
        ----------
        urn : `str`
            the endpoints, E.g "cryptocurrency/info"
        params : `dict`
            the parameters for the request

        Raises
        ------
        requests.exceptions.HTTPError
            If status code is not 200
        """
        url = Request("GET", urljoin(self._url, urn),
                      params=params).prepare().url
        # NOTE: race condition, but it should be harmless
        if self._session.cache.has_url(url):
            response = self._request_cache(url)
        else:
            response = self._request_throttle(url)

        res = loads(response.text)
        if response.status_code == 200:
            res["cached"] = response.from_cache
            return res
        else:
            raise response.raise_for_status()

    def _request_cache(self, url):
        return self._session.get(url)

    def _request_throttle(self, url):
        self._throttler.throttle()
        return self._session.get(url)

    @property
    def plan(self):
        return self._throttler.plan

    @plan.setter
    def plan(self, minute=0, daily=0, monthly=0):
        self._throttler.plan(minute, daily, monthly)

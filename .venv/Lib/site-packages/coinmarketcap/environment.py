# -*- coding: utf-8 -*-

from os.path import join
from pathlib import Path
from tempfile import gettempdir
from requests_cache.core import CachedSession as session
from threading import Lock
from json import load
from os import environ
from ratelimit import limits, sleep_and_retry
from datetime import datetime
from calendar import monthrange

FILE = ".coinmarketcap.json"


class Session:
    def __init__(self, apikey, expire, cf):
        self._session = session(cf, "sqlite", expire)
        self._session.headers.update({"X-CMC_PRO_API_KEY": apikey})
        self._session.headers.update({"Accept": "application/json"})
        self._session.headers.update({"Accept-Encoding": "deflate, gzip"})

    def clear_cache(self):
        self._session.cache.clear()


class Sandbox(Session):
    def __init__(self, apikey, expire):
        self._url = "https://sandbox-api.coinmarketcap.com/v1/"
        cf = join(gettempdir(), "CoinMarketCap_sandbox")
        if apikey is None:
            try:
                with open(join(Path.home(), FILE), "r") as fp:
                    keys = load(fp)
                apikey = keys["sandbox"]

            except FileNotFoundError:
                try:
                    apikey = environ["COINMARKETCAP_SANDBOX"]
                except KeyError:
                    raise KeyError("Can not locate key.")

        Session.__init__(self, apikey, expire, cf)


class Production(Session):
    def __init__(self, apikey, expire):
        self._url = "https://pro-api.coinmarketcap.com/v1/"
        cf = join(gettempdir(), "CoinMarketCap_production")
        if apikey is None:
            try:
                with open(join(Path.home(), FILE), "r") as fp:
                    keys = load(fp)
                apikey = keys["production"]

            except FileNotFoundError:
                try:
                    apikey = environ["COINMARKETCAP_PRODUCTION"]
                except KeyError:
                    raise KeyError("Can not locate key.")

        Session.__init__(self, apikey, expire, cf)


class Plan:
    __plans = {
        "basic": (10, 333, 10000),
        "hobbyist": (60, 1333, 40000),
        "startup": (60, 4000, 120000),
        "standard": (60, 16666, 500000),
        "professional": (60, 100000, 3000000),
        "enterprise": (0, 0, 0),
    }

    def __init__(self, plan):
        if plan not in self.__plans:
            raise ValueError
        self._plan = self.__plans[plan]

    @property
    def plan(self):
        return self._plan

    @plan.setter
    def plan(self, minute=0, daily=0, monthly=0):
        self._plan = (minute, daily, monthly)

    @property
    def minute(self):
        period = 60
        calls = self.plan[0]
        return calls, period

    @property
    def daily(self):
        period = (86400 / self.plan[1]) * self.plan[0]
        calls = self.plan[0]
        return calls, period

    @property
    def monthly(self):
        now = datetime.now()
        days = monthrange(now.year, now.month)[1]

        period = ((days * 86400) / self.plan[2]) * self.plan[0]
        calls = self.plan[0]
        return calls, period


class Throttler(Plan):
    def __init__(self, plan, throttle, block):
        Plan.__init__(self, plan)

        self.lock = Lock()
        scheme = (0, 0)
        self.throttling = True
        if throttle is None:
            self.throttling = False
        elif throttle == "minute":
            scheme = self.minute
        elif throttle == "daily":
            scheme = self.daily
        elif throttle == "monthly":
            scheme = self.monthly
        else:
            raise ValueError("Argument throttle must be either ")

        self.limit = limits(*scheme, raise_on_limit=block)(lambda: None)
        self.sleep = sleep_and_retry(self.limit)
        self.block = block

    def throttle(self):
        if self.throttling:
            with self.lock:
                if self.block:
                    self.sleep()
                else:
                    self.limit()

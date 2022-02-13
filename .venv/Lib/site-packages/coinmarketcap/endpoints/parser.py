# -*- coding: utf-8 -*-

from typing import Union
import datetime
import sys


def args(**kwarg) -> dict:
    params = {}
    for method_name, arg in kwarg.items():
        try:
            params[method_name] = getattr(
                sys.modules[__name__], method_name)(arg)
        except AttributeError:
            continue
    return params


def id(arg: Union[int, str, list]) -> int:
    if isinstance(arg, int) or isinstance(arg, str):
        return str(arg)
    elif isinstance(arg, list):
        if all(isinstance(id, int) for id in arg):
            return ",".join(map(str, arg))
        if all(isinstance(id, str) for id in arg):
            return ",".join(arg)
        else:
            raise ValueError
    else:
        return str(arg)


def symbol(arg: Union[str, list]) -> str:
    if isinstance(arg, str):
        return arg
    elif isinstance(arg, list):
        if all(isinstance(symbol, str) for symbol in arg):
            return ",".join(arg)
        else:
            raise ValueError
    else:
        return str(arg)


def convert(arg: Union[str, list]) -> str:
    if isinstance(arg, str):
        return arg
    if isinstance(arg, list):
        if all(isinstance(slug, str) for slug in arg):
            return ",".join(arg)
        else:
            raise ValueError
    else:
        return str(arg)


def start(arg: int) -> str:
    return str(arg)


def limit(arg: int) -> str:
    return str(arg)


def sort(arg: str) -> str:
    return str(arg)


def sort_dir(arg: str) -> str:
    return str(arg)


def cryptocurrency_type(arg: str) -> str:
    return str(arg)


def time(arg: Union[datetime.datetime, float, str]) -> str:
    if isinstance(arg, datetime.datetime):
        return arg.isoformat()
    if isinstance(arg, float):
        return datetime.datetime.fromtimestamp(arg).isoformat()
    else:
        return str(arg)


def time_start(arg: Union[datetime.datetime, float, str]) -> str:
    return time(arg)


def time_end(arg: Union[datetime.datetime, float, str]) -> str:
    return time(arg)


def time_period(arg: str) -> str:
    return str(arg)


def count(arg: int) -> int:
    return str(arg)


def interval(arg: str) -> str:
    return str(arg)


def slug(arg: Union[str, list]) -> str:
    if isinstance(arg, str):
        return arg
    elif isinstance(arg, list):
        if all(isinstance(slug, str) for slug in arg):
            return ",".join(arg)
        else:
            raise ValueError
    else:
        return str(arg)


def market_type(arg: str) -> str:
    return str(arg)


def amount(arg: Union[float, int, str]) -> str:
    return str(arg)

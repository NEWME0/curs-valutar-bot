import logging
from typing import List, Iterable
from datetime import date

import requests
from requests.exceptions import RequestException, BaseHTTPError
from pydantic import parse_obj_as, ValidationError
from app.common.models import BankItem, CoinItem, RateItem


HOST = 'https://www.live.curs-valutar.xyz'


logger = logging.Logger(name='API-Requests', level=logging.ERROR)


class SuppressRequestsExceptions:
    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return True

        if exc_type == RequestException:
            logger.error(f'{exc_type} {exc_val} {exc_tb}')
            return True

        if exc_type == BaseHTTPError:
            logger.error(f'{exc_type} {exc_val} {exc_tb}')
            return True


class SuppressValidationExceptions:
    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        # No exception raised
        if exc_type is None:
            return True

        if exc_type == ValidationError:
            logger.error(f'{exc_type} {exc_val} {exc_tb}')
            return True


def request_banks_all() -> List[BankItem]:
    with SuppressRequestsExceptions():
        data = requests.get(f'{HOST}/exchange/banks/').json()

    with SuppressValidationExceptions():
        result = parse_obj_as(List[BankItem], data)

    if 'result' not in locals():
        return []

    return result


def request_banks_with_ids(bank_ids) -> List[BankItem]:
    params = {
        'id__in': ','.join(map(str, bank_ids)),
    }
    with SuppressRequestsExceptions():
        data = requests.get(f'{HOST}/exchange/banks/').json()

    with SuppressValidationExceptions():
        result = parse_obj_as(List[BankItem], data)

    if 'result' not in locals():
        return []

    return result


def request_coins_all() -> List[CoinItem]:
    with SuppressRequestsExceptions():
        data = requests.get(f'{HOST}/exchange/coins/').json()

    with SuppressValidationExceptions():
        result = parse_obj_as(List[CoinItem], data)

    if 'result' not in locals():
        return []

    return result


def request_coins_with_abbr(abbr: str) -> List[CoinItem]:
    params = {
        'abbr': abbr
    }

    with SuppressRequestsExceptions():
        data = requests.get(f'{HOST}/exchange/coins/', params=params).json()

    with SuppressValidationExceptions():
        result = parse_obj_as(List[CoinItem], data)

    if 'result' not in locals():
        return []

    return result


def request_coins_of_bank(bank_id: int) -> List[CoinItem]:
    params = {
        'bank': bank_id,
    }

    with SuppressRequestsExceptions():
        data = requests.get(f'{HOST}/exchange/coins/', params=params).json()

    with SuppressValidationExceptions():
        result = parse_obj_as(List[CoinItem], data)

    if 'result' not in locals():
        return []

    return result


def request_rates_of_coin(coin_id: int, date_from: date = date.today()) -> List[RateItem]:
    params = {
        'currency': coin_id,
        'date__gte': date_from,
    }

    with SuppressRequestsExceptions():
        data = requests.get(f'{HOST}/exchange/rates/', params=params).json()

    with SuppressValidationExceptions():
        result = parse_obj_as(List[RateItem], data)

    if 'result' not in locals():
        return []

    return result


def request_rates_of_coins(coin_ids: Iterable[int], date_from: date = date.today()) -> List[RateItem]:
    params = {
        'currency__in': ','.join(map(str, coin_ids)),
        'date__gte': date_from,
    }

    with SuppressRequestsExceptions():
        data = requests.get(f'{HOST}/exchange/rates/', params=params).json()

    with SuppressValidationExceptions():
        result = parse_obj_as(List[RateItem], data)

    if 'result' not in locals():
        return []

    return result

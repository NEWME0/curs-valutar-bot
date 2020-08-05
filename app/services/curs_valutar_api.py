import logging
from typing import List, Tuple, Iterable
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


# Old API
from app.common.models import BankPage, CoinPage, RatePage


DOMAIN = 'https://www.live.curs-valutar.xyz'


def request_bank_list() -> Tuple[bool, List[BankItem]]:
    """ Request list of banks """
    # TODO: Rewrite to parse all pages and return request ok or not
    try:
        response = requests.get(f'{DOMAIN}/banks/bank')
    except (RequestException, BaseHTTPError) as exception:
        return False, []

    page: BankPage = BankPage.parse_raw(response.content)

    return True, page.results


def request_coin_list(bank_id) -> Tuple[bool, List[CoinItem]]:
    """ Request list of coins of specified band """
    # TODO: Rewrite to parse all pages and return request ok or not
    try:
        response = requests.get(f'{DOMAIN}/banks/coin/{bank_id}')
    except (RequestException, BaseHTTPError) as exception:
        return False, []

    page: CoinPage = CoinPage.parse_raw(response.content)

    return True, page.results


def request_rate_list(coin_id, days=7) -> Tuple[bool, List[RateItem]]:
    """ Request list of rates of specified coin for a number of days """
    # TODO: Rewrite to parse all pages and return request ok or not
    try:
        response = requests.get(f'{DOMAIN}/banks/rate/{coin_id}/{days}')
    except (RequestException, BaseHTTPError) as exception:
        return False, []

    page: RatePage = RatePage.parse_raw(response.content)

    return True, page.results


def request_actual_rates(bank_id) -> Tuple[bool, List[Tuple[CoinItem, RateItem]]]:
    """ Request actual rates of all coins of a bank """
    # TODO: Rewrite to parse all pages and return request ok or not
    request_ok, coin_list = request_coin_list(bank_id)
    if request_ok is False:
        return False, []

    result = list()

    for coin in coin_list:
        request_ok, rate_list = request_rate_list(coin.id, days=1)

        if request_ok is False:
            result = None
            return False, []

        result.append((coin, rate_list[-1]))

    return True, result


def request_best_rates(coin_abbr) -> Tuple[bool, List[Tuple[BankItem, RateItem]]]:
    request_ok, bank_list = request_bank_list()
    if request_ok is False:
        return False, []

    result = list()

    for bank in bank_list:
        request_ok, coin_list = request_coin_list(bank.id)
        if request_ok is False:
            return False, []

        for coin in coin_list:
            if coin.abbr == coin_abbr:
                request_ok, rate_list = request_rate_list(coin.id, days=1)
                if request_ok is False:
                    return False, []

                result.append((bank, rate_list[-1]))

    return True, result

import typing
import datetime
import pydantic


class BankItem(pydantic.BaseModel):
    id: int
    registered_name: str
    short_name: str
    website: str


class CoinItem(pydantic.BaseModel):
    id: int
    name: str
    abbr: str
    bank: int


class RateItem(pydantic.BaseModel):
    id: int
    rate_sell: float
    rate_buy: float
    date: datetime.date
    currency: int


class BasePage(pydantic.BaseModel):
    count: int
    next: typing.Union[None, str]
    previous: typing.Union[None, str]
    results: typing.List

    class Config:
        arbitrary_types_allowed = True


class BankPage(BasePage):
    results: typing.List[BankItem]


class CoinPage(BasePage):
    results: typing.List[CoinItem]


class RatePage(BasePage):
    results: typing.List[RateItem]

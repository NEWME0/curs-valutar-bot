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

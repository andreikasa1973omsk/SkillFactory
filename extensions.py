import json
import requests
from config import KEYS


class APIException(Exception):
    pass


class CurrencyConvertor:
    @staticmethod
    def get_price(quote: str, base: str) -> float:

        response = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote}&tsyms={base}')
        return json.loads(response.content)[base]

    @staticmethod
    def handle_message(text: str) -> str:
        values = text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров')

        quote, base, amount = values
        if quote == base:
            return amount

        try:
            quote_ticker = KEYS[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = KEYS[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            amount_count = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        price = CurrencyConvertor.get_price(quote_ticker, base_ticker)

        return f'{amount} {quote} = {price * amount_count} {base}'
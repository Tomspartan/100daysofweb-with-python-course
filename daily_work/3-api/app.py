import json
from typing import List

from apistar import App, Route, types, validators
from apistar.http import JSONResponse

def _load_stocks_data():
    with open('MOCK_DATA.json') as f:
        stocks = json.loads(f.read())
        return {stock["symbol"]: stock for stock in stocks}

stocks = _load_stocks_data()

STOCK_NOT_FOUND = 'Stock not found'

class Stock(types.Type):
    name = validators.String()
    sector = validators.String(allow_null=True) 
    market = validators.String()
    symbol = validators.String()

#API Methods

def list_stocks() -> List[Stock]:
    return [Stock(stock[1]) for stock in sorted(stocks.items())]

def create_stock(stock: Stock) -> JSONResponse:
    stocks[stock.symbol] = stock
    return JSONResponse(Stock(stock), status_code=201)


def get_stock(symbol) -> JSONResponse:
    stock = stocks.get(symbol)
    if not stock:
        error = {'error': STOCK_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    return JSONResponse(Stock(stock), status_code=200)


def update_stock(symbol, stock: Stock) -> JSONResponse:
    if not stocks.get(symbol):
        error = {'error': STOCK_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    stocks[stock.symbol] = stock
    return JSONResponse(Stock(stock), status_code=200)


def delete_stock(symbol) -> JSONResponse:
    if not stocks.get(symbol):
        error = {'error': STOCK_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    del stocks[symbol]
    return JSONResponse({}, status_code=204)


routes = [
    Route('/', method='GET', handler=list_stocks),
    Route('/', method='POST', handler=create_stock),
    Route('/{symbol}/', method='GET', handler=get_stock),
    Route('/{symbol}/', method='PUT', handler=update_stock),
    Route('/{symbol}/', method='DELETE', handler=delete_stock),
]

app = App(routes=routes)


if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)

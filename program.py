
from stockmarket import *
from agent import Agent

if __name__ == "__main__":
    market: StockMarket = StockMarket()
    buyer: Agent = Agent()
    buyer.earn(40)
    buyer.buy(market, 3, Execution.LIMIT, 13)
    print(buyer.money)
    print(market.buy_orders)
    seller: Agent = Agent()
    seller.shares = 3
    seller.sell(market, 2, Execution.MARKET)
    print(buyer.money)
    print(buyer.shares)
    print(seller.money)
    print(seller.shares)
    print(market.buy_orders)
    print(market.sell_orders)

from stockmarket import *


class Agent(Investor):
    def __init__(self, money=0, shares=0):
        super().__init__(money, shares)
        self.consumed: int = 0

    def earn(self, amount: int):
        self.money += amount

    def consume(self, amount: int):
        if amount > self.money:
            raise ValueError("Trying to consume ${} but has only ${}".format(amount, self.money))
        self.money -= amount
        self.consumed += amount

    def get_dividend(self):
        self.money += int(self.shares*0.01)

    def buy(self, market: StockMarket, amount: int, execution: Execution = Execution.MARKET, price: int = None):
        if price is not None and amount*price > self.money:
            raise ValueError("Trying to buy stock for ${}, but has only ${}".format(amount*price, self.money))
        market.buy(Order(self, OrderType.BUY, execution, amount, price))

    def sell(self, market: StockMarket, amount: int, execution: Execution = Execution.MARKET, price: int = None):
        if self.shares < amount:
            raise ValueError("Trying to sell {} shares, but has only {} shares".format(amount, self.shares))
        market.sell(Order(self, OrderType.SELL, execution, amount, price))

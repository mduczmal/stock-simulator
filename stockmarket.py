from heapq import *
from enum import Enum
from typing import List
from typing import Tuple
from typing import Optional

MAX_PRICE = 1000000000


class Investor:
    def __init__(self, money=0, shares=0):
        self.money: int = money
        self.shares: int = shares


class OrderType(Enum):
    BUY = 1
    SELL = 2


class Execution(Enum):
    MARKET = 1
    LIMIT = 2


class Order:
    def __init__(self, agent: Investor, order_type: OrderType, execution: Execution, amount: int, price: int = None):
        if execution == Execution.MARKET and price is not None:
            raise ValueError("Market order specifies price: ${}".format(price))
        self.agent: Investor = agent
        self.order_type: OrderType = order_type
        self.execution: Execution = execution
        self.amount: int = amount
        if price is not None:
            self.price: int = price
        elif execution == execution.MARKET:
            if order_type == order_type.BUY:
                self.price = MAX_PRICE
            elif order_type == order_type.SELL:
                self.price = 0
        else:
            raise ValueError("Price not set for order with execution type {}".format(execution))

    def __str__(self):
        str_type = ""
        if self.order_type == OrderType.BUY:
            str_type = "BUY"
        elif self.order_type == OrderType.SELL:
            str_type = "SELL"
        return "{} ${} x {}".format(str_type, self.price, self.amount)

    def execute(self, amount: int, price: int):
        if amount > self.amount:
            raise ValueError("Trying to execute order of {} shares but only {} shares left".format(amount, self.amount))
        elif self.order_type == OrderType.BUY and price > self.price:
            raise ValueError("Trying to buy for ${} but price ${} set".format(price, self.price))
        elif self.order_type == OrderType.SELL and price < self.price:
            raise ValueError("Trying to sell for ${} but price ${} set".format(price, self.price))
        elif self.order_type == OrderType.BUY:
            self.agent.money -= price*amount
            self.agent.shares += amount
            self.amount -= amount
        elif self.order_type == OrderType.SELL:
            self.agent.shares -= amount
            self.agent.money += price*amount
            self.amount -= amount


def are_matched(sell_order: Order, buy_order: Order) -> bool:
    if sell_order.order_type != OrderType.SELL:
        raise ValueError("Sell order has type {}".format(sell_order.order_type))
    if buy_order.order_type != OrderType.BUY:
        raise ValueError("Buy order has type {}".format(buy_order.order_type))
    if sell_order.price <= buy_order.price:
        return True
    else:
        return False


class OrderHeap:
    def __init__(self, order_type: OrderType):
        if order_type not in [OrderType.BUY, OrderType.SELL]:
            raise ValueError("Please provide order_type argument OrderType.BUY or OrderType.SELL")
        self.order_type = order_type
        self.orders: List[Tuple[int, Order]] = []
        self.reversed = False

    def __len__(self):
        return len(self.orders)

    def __iter__(self):
        if self.reversed:
            for order in reversed(self.orders):
                yield order[1]
        else:
            for order in self.orders:
                yield order[1]

    def __reversed__(self):
        self.reversed = not self.reversed
        return self

    def __str__(self):
        str_repr = ""
        if len(self.orders) == 0:
            return "No orders"
        else:
            for order in self.orders:
                str_repr += str(order[1])
                str_repr += "\n"
            return str_repr

    def push(self, order: Order):
        if order.order_type != self.order_type:
            raise ValueError("Trying to insert order of type {} into heap accepting {}".format(
                order.order_type, self.order_type))
        if self.order_type == OrderType.BUY:
            heappush(self.orders, (-order.price, order))
        elif self.order_type == OrderType.SELL:
            heappush(self.orders, (order.price, order))

    def pop(self) -> Order:
        return heappop(self.orders)[1]


class StockMarket:
    def __init__(self):
        self.buy_orders: OrderHeap = OrderHeap(OrderType.BUY)
        self.sell_orders: OrderHeap = OrderHeap(OrderType.SELL)
        self.last_price: Optional[int] = None

    def execute(self, sell_order: Order, buy_order: Order, price: int):
        if sell_order.order_type == buy_order.order_type:
            raise ValueError("{} order matched with {} order".format(sell_order.order_type, buy_order.order_type))
        amount: int = min(sell_order.amount, buy_order.amount)
        sell_order.execute(amount, price)
        buy_order.execute(amount, price)
        self.last_price = price

    def buy(self, buy_order: Order):
        if buy_order.order_type != OrderType.BUY:
            raise ValueError("Buy order of type {}".format(buy_order.order_type))
        else:
            if len(self.sell_orders) > 0:
                sell_order: Order = self.sell_orders.pop()
                while are_matched(sell_order, buy_order):
                    self.execute(sell_order, buy_order, sell_order.price)
                    if buy_order.amount == 0:
                        if sell_order.amount > 0:
                            self.sell_orders.push(sell_order)
                        break
                    elif len(self.sell_orders) == 0:
                        break
                    else:
                        sell_order = self.sell_orders.pop()
                else:
                    self.sell_orders.push(sell_order)
            if buy_order.amount > 0:
                self.buy_orders.push(buy_order)

    def sell(self, sell_order: Order):
        if sell_order.order_type != OrderType.SELL:
            raise ValueError("SELL order of type {}".format(sell_order.order_type))
        else:
            if len(self.buy_orders) > 0:
                buy_order: Order = self.buy_orders.pop()
                while are_matched(sell_order, buy_order):
                    self.execute(buy_order, sell_order, buy_order.price)
                    if sell_order.amount == 0:
                        if buy_order.amount > 0:
                            self.buy_orders.push(buy_order)
                        break
                    elif len(self.sell_orders) == 0:
                        break
                    else:
                        buy_order = self.buy_orders.pop()
                else:
                    self.buy_orders.push(buy_order)
            if sell_order.amount > 0:
                self.sell_orders.push(sell_order)



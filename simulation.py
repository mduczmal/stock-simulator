import matplotlib.pyplot as plt
from stockmarket import *
from agent import Agent
from typing import List


def agents_consume():
    agents: List[Agent] = []
    for i in range(10):
        agent: Agent = Agent(1000, 10)
        if i%2 == 0:
            agent.consume(200)
            print(agent.money, agent.shares)
        agents.append(agent)
    #show_agents(agents)

def simulate():
    market: StockMarket = StockMarket()
    market.last_price = 20
    a: Agent = Agent()
    a.earn(100000)
    a.buy(market, 20, Execution.LIMIT, 15)
    a.buy(market, 17, Execution.LIMIT, 13)
    b: Agent = Agent()
    b.shares = 300
    b.sell(market, 50, Execution.LIMIT, 73)
    b.sell(market, 50, Execution.LIMIT, 34)
    b.sell(market, 50, Execution.LIMIT, 62)
    b.sell(market, 50, Execution.LIMIT, 26)
    print(market.buy_orders)
    print(market.sell_orders)
    show_book(market)

def show_agents(agents: List[Agent]):
    consumed = [agent.consumed for agent in agents]
    plt.hist(consumed)
    plt.show()

def show_book(market: StockMarket):
    cellText: List = []
    colors: List = []
    cellText.append(["Sell orders"])
    colors.append([(1, 0.35, 0.25)])
    for sell_order in reversed(market.sell_orders):
        cellText.append([sell_order.price])
        colors.append([(1, 1, 0.75)])
    cellText.append([""])
    colors.append([(1, 1, 1)])
    for buy_order in market.buy_orders:
        cellText.append([buy_order.price])
        colors.append([(1, 1, 0.75)])
    cellText.append(["Buy orders"])
    colors.append([(0.35, 1, 0.35)])
    plt.table(cellText=cellText, cellColours=colors, loc="center")
    plt.show()



if __name__ == "__main__":
    simulate()

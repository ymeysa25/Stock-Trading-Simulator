class StockTransaction:
    def __init__(self, m, k, d, stock_detail):
        self.m = m
        self.k = k
        self.d = d
        self.stock_detail = stock_detail

        self.buy_stock = []
        self.sell_stock = []

    def mean(self, prices):
        return sum(prices) / len(prices)

    def start(self):
        state = []

        buy_money = 0  # will be add to account in the next day

        for stock, detail in self.stock_detail.items():
            owned = detail['owned']
            prices = detail['prices']
            last_price = prices[-1]

            curr_avg_prices = detail['avg_prices']

            avg_price = self.mean(prices)

            if owned > 0 and last_price > avg_price and last_price > curr_avg_prices:
                cmd = f'{stock} SELL {owned}'

                buy_money += owned * last_price
                self.sell_stock.append(stock)
                state.append(cmd)
        buy = {}

        while self.m > 0:
            smallest = 0
            not_interest = 0
            for stock, detail in self.stock_detail.items():
                prices = detail['prices']
                last_price = prices[-1]

                avg_price = self.mean(prices)

                if self.m > 0 and last_price < avg_price:
                    if self.m - last_price > 0:
                        if stock not in buy:
                            buy[stock] = {
                                "total" : 0,
                                "price" : 0
                            }

                        buy[stock]['total'] += 1
                        buy[stock]['price'] = last_price

                        self.m -= 1 * last_price
                        continue
                    else:
                        not_interest += 1

                if self.m < last_price:
                    smallest += 1

                if self.m > last_price or last_price > avg_price:
                    not_interest += 1
            if smallest == self.k:
                break
            if not_interest == self.k:
                break

        for stock, total in buy.items():
            cmd = f'{stock} BUY {total["total"]}'
            state.append(cmd)

        print(len(state))
        for s in state:
            print(s)

        if self.d == 1:
            for stock, detail in self.stock_detail.items():
                owned = detail['owned']
                prices = detail['prices']
                last_price = prices[-1]

                buy_money += owned * last_price
                self.sell_stock.append(stock)

        self.m += buy_money
        self.buy_stock = buy
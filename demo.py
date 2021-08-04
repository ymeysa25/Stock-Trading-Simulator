import os

import pandas as pd
from stock_transaction import StockTransaction


def calculate_mean(old_avg, old_total, new_price, total_buy):
    return ((old_avg * old_total) + (new_price * total_buy)) / (old_total + total_buy)


def num2currency(num):
    return 'Rp. {:0,.0f}'.format(num)


is_example = False
if is_example:
    files = os.listdir('example')
else:
    files = os.listdir('saham_indonesia')

stock_inputs = {}
for file in files:
    stock_name, _ = os.path.splitext(file)
    if is_example:
        data = pd.read_excel(f'example/{file}')
    else:
        data = pd.read_csv(f'saham_indonesia/{file}')

    stock_inputs[stock_name] = {
        "owned": 0,
        "price": [d for d in data['Close'].values],
        "avg_price": 0
    }

print(len([d for d in data['Close'].values]))

list_stock = stock_inputs.keys()

if is_example:
    # in dollar
    money = 100
    start_day = 0
    end_day = 5
else:
    # in rupiah
    money = 5000
    start_day = 0
    end_day = 100

start_money = money
day_left = 40
k = len(list_stock)

print("Modal awal : ", num2currency(money * 100))

for day in range(day_left, 0, -1):
    values = f'{money} {k} {day}'

    for stock in list_stock:
        owned = stock_inputs[stock]['owned']
        prices = stock_inputs[stock]['price'][start_day:end_day]
        prices = [str(p) for p in prices]
        prices = ' '.join(prices)
        values += '\n' + f'{stock} {owned} {prices}'

    values = values.split("\n")
    m, k, d = [float(i) for i in values[0].strip().split(" ")]
    k = int(k)
    d = int(d)

    stocks_details = {}
    for i in range(1, k + 1):
        temp = values[i].strip().split(" ")
        name = temp[0]
        owned = temp[1]
        prices = [float(p) for p in temp[2:]]
        stocks_details[name] = {
            "owned": int(owned),
            "prices": prices,
            "avg_prices": stock_inputs[name]['avg_price']
        }

    transaction = StockTransaction(m, k, d, stocks_details)
    transaction.start()

    money = round(transaction.m, 1)
    if is_example:
        print(money)
    else:
        print(num2currency(money * 100))

    for stock, total in transaction.buy_stock.items():
        old_total = stock_inputs[stock]['owned']
        avg_price = stock_inputs[stock]['avg_price']
        buy_price = total['price']

        new_avg_price = calculate_mean(avg_price, old_total, buy_price, total['total'])

        stock_inputs[stock]['owned'] += total['total']
        stock_inputs[stock]['avg_price'] = new_avg_price

    for stock in transaction.sell_stock:
        stock_inputs[stock]['owned'] = 0
        stock_inputs[stock]['avg_price'] = 0

    for stock, detail in stock_inputs.items():
        owned = detail['owned']
        print(f"{stock} {owned} ", end=" ")

    print()
    print("============")
    # start_day += 1
    end_day += 1

print("Modal Awal  :", num2currency(start_money * 100))
print("Modal Akhir :", num2currency(money * 100))

state = "" if money > start_money else "-"
gain = abs(money - start_money)
gain = (gain / start_money) * 100

print(f"Percentages : {state}{gain}%")

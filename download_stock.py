# import modules
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt

# initialize parameters
start_date = datetime(2021, 1, 1)
end_date = datetime(2021, 7, 30)

stocks = ["BBRI", "TLKM", "BRIS", "ANTM", "ACES",
          "ADRO", "BBCA", "BBTN", "INCO", "BMRI"]

for stock in stocks:
    stock_name = f'{stock}.JK'

    data = yf.download(stock_name, start=start_date,
                   end=end_date)

    data.to_csv(f"{stock}.csv")
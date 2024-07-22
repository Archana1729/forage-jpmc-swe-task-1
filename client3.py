import json
import random
import urllib.request

# Server API URLs
QUERY = "http://localhost:8080/query?id={}"

# 500 server requests
N = 500


def getDataPoint(quote):
    """ Produce all the needed values to generate a datapoint """
    stock = quote['stock']
    bid_price = float(quote['top_bid']['price'])
    ask_price = float(quote['top_ask']['price'])
    # To get a representative price, we can use the average of bid and ask prices
    price = (bid_price + ask_price) / 2
    return stock, bid_price, ask_price, price


def getRatio(price_a, price_b):
    """ Get ratio of price_a and price_b """
    if price_b == 0:
        return float('inf')  # Avoid division by zero
    return price_a / price_b


# Main
if __name__ == "__main__":
    prices = {}  # To store prices for ratio calculation
    
    # Query the price once every N seconds.
    for _ in range(N):
        quotes = json.loads(urllib.request.urlopen(QUERY.format(random.random())).read())

        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            prices[stock] = price  # Store the latest price for each stock
            print(f"Quoted {stock} at (bid:{bid_price}, ask:{ask_price}, price:{price})")
        
        # Calculate and print the ratio of the prices for each pair of stocks
        stock_keys = list(prices.keys())
        for i in range(len(stock_keys)):
            for j in range(i + 1, len(stock_keys)):
                stock_a = stock_keys[i]
                stock_b = stock_keys[j]
                ratio = getRatio(prices[stock_a], prices[stock_b])
                print(f"Ratio of {stock_a} to {stock_b} is {ratio}")

        print("------")

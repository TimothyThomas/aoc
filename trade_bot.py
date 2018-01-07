import numpy as np
import pandas as pd
import requests
import time
import logging
from twilio.rest import Client


exchange_urls = {'gdax': 'https://api.gdax.com/',
                 'bitstamp': 'https://www.bitstamp.net/api/v2/trading-pairs-info',
                }

account_sid = 'AC28216c64968409b6edbfa4683db1349b'
auth_token = 'cccd1d71d80cc581f64be7743741c28f'
client = Client(account_sid, auth_token)
myTwilioNumber = '+14342772099'
myCellPhone = '+14342297973'

PRICE_CHECK_INTERVAL = 20   # how frequently to check prices, seconds
SMS_INTERVAL = 3600   # how frequently to send SMS, seconds
TARGET_SPREAD = .03  # fraction 

TARGET_PAIRS = ['BTC-USD', 
               'BCH-USD',
               'LTC-USD',
               'LTC-BTC',
               'ETH-USD',
               'ETH-BTC',
               ]

class GDAXTrader():
    def __init__(self):
        self.base_url = 'https://api.gdax.com/'


class BitstampTrader():
    def __init__(self):
        self.base_url = 'https://www.bitstamp.net/api/v2/trading-pairs-info'
#
#    def get_trading_pairs(self):
#        return
#
#    def get_last_price(pair):
#        return
#
#    def 
#
#        



def gdax_price_all_pairs():
    products = requests.get('https://api.gdax.com/products').json()
    pairs = [p['id'] for p in products]
    
    prices = {}
    for pair in pairs:
        if pair in TARGET_PAIRS:
            ticker = requests.get(f'https://api.gdax.com/products/{pair}/ticker').json()
            prices[pair] = float(ticker['price'])
            logging.info(f"GDAX price for {pair}: {prices[pair]}")
    return prices 


def bitstamp_price_all_pairs():
    pairs = requests.get('https://www.bitstamp.net/api/v2/trading-pairs-info').json()
    url_symbols = [pair['url_symbol'] for pair in pairs]
    prices = {}
    for url_symbol in url_symbols:
        pair = url_symbol[:3].upper() + '-' + url_symbol[3:].upper()
        if pair in TARGET_PAIRS:
            ticker = requests.get(f'https://www.bitstamp.net/api/v2/ticker/{url_symbol}/').json()
            prices[pair] = float(ticker['last'])
            logging.info(f"Bitstamp price for {pair}: {prices[pair]}")
    return prices 

def calculate_spreads():
    gdax_prices = gdax_price_all_pairs()
    bitstamp_prices = bitstamp_price_all_pairs()
    spreads = {}
    for pair in gdax_prices:
        try:
            spread = np.abs(1 - gdax_prices[pair] / bitstamp_prices[pair])
            spreads[pair] = {'spread': spread, 
                             'gdax_price': gdax_prices[pair], 
                             'bitstamp_price': bitstamp_prices[pair]}
            logging.info(f"Spread for {pair}: {spread*100:.2f}%")
        except KeyError:
            continue
    return spreads



def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Staring arbitrage opportunity monitor.  Terminate with CTRL-C")
    time_last_sms = 0.0
    max_spread_this_session = 0.0
    while True:
        logging.info("Checking prices...")
        spreads = calculate_spreads()
        max_spread = 0.0
        for pair in spreads:
            if spreads[pair]['spread'] > max_spread:
                max_spread = spreads[pair]['spread']
                max_pair = pair

                if max_spread > max_spread_this_session:
                    max_spread_this_session = max_spread

        if max_spread > TARGET_SPREAD:
            if spreads[max_pair]['gdax_price'] < spreads[max_pair]['bitstamp_price']:
                buy_xchg = 'GDAX'
                buy_price = spreads[max_pair]['gdax_price']
                sell_xchg = 'Bitstamp'
                sell_price = spreads[max_pair]['bitstamp_price']
            else:
                buy_xchg = 'Bitstamp'
                buy_price = spreads[max_pair]['bitstamp_price']
                sell_xchg = 'GDAX'
                sell_price = spreads[max_pair]['gdax_price']
            msg = f"Arbitrage opportunity for {max_pair}!\n" \
                  f"Buy on {buy_xchg} @ {buy_price}\n" \
                  f"Sell on {sell_xchg} @ {sell_price}\n" \
                  f"Spread:  {max_spread*100:.2f}%"
            logging.info(msg)

            if time.time() - time_last_sms > SMS_INTERVAL:
                logging.info("Sending SMS...")
                msg_body = msg 
                message = client.messages.create(body=msg_body, from_=myTwilioNumber, to=myCellPhone)
                time_last_sms = time.time()
        else: 
            logging.info(f"No aribtrage opp detected. Current best spread is {max_spread*100:.2f}%. " \
                         f"Best spread this session: {max_spread_this_session*100:.2f}%.")
        time.sleep(PRICE_CHECK_INTERVAL)

# for all exchanges being tracked:
#     for all trading pairs being tracked:
#         get last price data
#         get trading status (available/unavailable)
# for all trading pairs being tracked: 
#     check for favorable spread between exchanges
#     if favorable and trading is available on both exchanges:  
#         initiate small market trade on both exchanges


if __name__ == "__main__":
    main()


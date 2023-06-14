import base64
import json
import logging
import os

import requests


def get_future_assets():
    asset_list_raw = requests.get(
        'https://fapi.binance.com/fapi/v1/ticker/price').json()

    asset_list_full = []
    for item in asset_list_raw:
        if (item['symbol'][-4:] == 'USDT' or item['symbol'][-4:] == 'BUSD'):
            # print(item)
            asset_list_full.append(item["symbol"])

    return asset_list_raw

    
def build_request(ticker, type, price, stop_loss_p, take_profit_p, valid_until):
    token = f"{os.environ.get('BINANCE_API_KEY')};{os.environ.get('BINANCE_API_SECRET')}"

    price = float(price)
    stop_loss_p = float(stop_loss_p)
    take_profit_p = float(take_profit_p)

    if type == "BUY":
        stop_loss = price * (1 - (stop_loss_p / 100))
        take_profit = price * (1 + (take_profit_p / 100))
    elif type == "SELL":
        stop_loss = price * (1 + (stop_loss_p / 100))
        take_profit = price * (1 - (take_profit_p / 100))
    else:
        logging.error("wrong stops bruh")
        return

    data = {
        "token": token,
        "ticker": ticker,
        "type": type,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "strategy": "simple_gap_finder",
        "valid_until": valid_until
    }
    return data


def request_it(request) -> str:
    
    request = base64.b64encode(bytes(json.dumps(request), "utf-8"))
    request = request.decode()
    send_data ={"message": {"data": request}}
    send_data = json.dumps(send_data)
    
    
    logging.info(send_data)
    
    resp = requests.post(
                            os.environ.get('BINANCE_ORDERS_ENDPOINT', ""), 
                            data=send_data
                            )
    
    logging.info(resp.text)
    
    return resp.text
    
    
def send_order(ticker, type, price, stop_loss_p, take_profit_p, valid_until) -> str:
    req = build_request(ticker, type, price, stop_loss_p, take_profit_p, valid_until)
    ans = request_it(req)
    
    return ans
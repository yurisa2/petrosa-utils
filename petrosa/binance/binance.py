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

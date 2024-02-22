import requests
import json


def format_binance_api(res):
    trade_user = res.get("advertiser").get("nickName")
    trade_method = ", ".join(
        [
            bm["tradeMethodName"]
            for bm in res.get("adv").get("tradeMethods")
            if bm.get("tradeMethodName")
        ]
    )
    trade_rate = res.get("adv").get("price")
    trade_fiat_unit = res.get("adv").get("fiatUnit")
    trade_amount = res.get("adv").get("surplusAmount")
    trade_type = res.get("adv").get("tradeType")
    trade_asset = res.get("adv").get("asset")
    return (
        f"""
        <tr>
            <td>{trade_type}</td>
            <td>{trade_user}</td>
            <td>{trade_rate} {trade_fiat_unit}</td>
            <td>{trade_amount} {trade_asset}</td>
            <td>{trade_method}</td>
        </tr>
        """
    )


def get_binance_data(trade_type = "BUY"):
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    headers = {"Content-Type": "application/json"}
    data = {
        "fiat": "MMK",
        "page": 1,
        "rows": 10,
        "tradeType": trade_type,
        "asset": "USDT",
        "countries": [],
        "proMerchantAds": False,
        "shieldMerchantAds": False,
        "publisherType": None,
        "payTypes": [],
        "classifies": ["mass", "profession"],
    }
    return requests.post(url, headers=headers, json=data).json()

